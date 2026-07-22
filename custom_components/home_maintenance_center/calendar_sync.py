"""
Sync maintenance items to an external (local) calendar entity.

Home Maintenance Center Pro's own ``calendar`` entity only ever
exposes the single next event via its ``event`` property, and the
frontend agenda/list views need a proper non-zero-duration event per
day. Some users prefer routing everything to a plain
``local_calendar`` entity instead (e.g. ``calendar.manutenzioni_casa``)
so it behaves like any other calendar in Home Assistant.

This manager creates one all-day event per maintenance item on its
``next_maintenance`` date, and re-creates it whenever that date
changes (e.g. after "Segna come fatta"). It never deletes past
events, so the target calendar also doubles as a history log.
"""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .models.maintenance_item import MaintenanceItem

_LOGGER = logging.getLogger(__name__)

CONF_LOCAL_CALENDAR_ENTITY = "local_calendar_entity"

# Chiave salvata in item.metadata per ricordare quale data è già
# stata scritta sul calendario locale, ed evitare duplicati ad ogni
# aggiornamento del coordinator.
SYNC_META_KEY = "_synced_calendar_date"


class CalendarSyncManager:
    """Keep a local calendar entity in sync with maintenance items."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator,
        config_entry: ConfigEntry,
    ) -> None:
        self.hass = hass
        self.coordinator = coordinator
        self.entry = config_entry

    @property
    def target_entity(self) -> str | None:
        """Return the configured target calendar entity, if any."""

        return (
            self.entry.options.get(CONF_LOCAL_CALENDAR_ENTITY)
            or None
        )

    async def async_sync_all(self) -> None:
        """Sync every enabled item with a pending due date."""

        target = self.target_entity

        if not target:
            return

        if not self.hass.services.has_service(
            "calendar", "create_event"
        ):
            _LOGGER.warning(
                "Il servizio calendar.create_event non è "
                "disponibile: impossibile sincronizzare su %s",
                target,
            )
            return

        for item in self.coordinator.items:
            await self._sync_item(item, target)

    async def _sync_item(
        self,
        item: MaintenanceItem,
        target: str,
    ) -> None:
        """Create a calendar event for one item, if not already done."""

        if not item.enabled or item.next_maintenance is None:
            return

        current_date = item.next_maintenance.isoformat()

        if item.metadata.get(SYNC_META_KEY) == current_date:
            # Già sincronizzato per questa scadenza.
            return

        description = (
            f"Categoria: {item.category}\n"
            f"Priorità: {item.priority}"
        )

        try:
            await self.hass.services.async_call(
                "calendar",
                "create_event",
                {
                    "entity_id": target,
                    "summary": item.name,
                    "description": description,
                    "start_date": item.next_maintenance.isoformat(),
                    "end_date": (
                        item.next_maintenance
                        + timedelta(days=1)
                    ).isoformat(),
                },
                blocking=True,
            )
        except Exception as err:  # noqa: BLE001
            _LOGGER.warning(
                "Impossibile creare l'evento calendario per "
                "'%s' su %s: %s",
                item.name,
                target,
                err,
            )
            return

        item.metadata[SYNC_META_KEY] = current_date

        # Scriviamo solo su storage, senza passare da
        # coordinator.async_update_item: quello forzerebbe un
        # refresh completo che richiamerebbe di nuovo async_sync_all,
        # generando un giro superfluo (anche se innocuo, dato che il
        # secondo giro non troverebbe più nulla da sincronizzare).
        await self.coordinator.storage.update_item(item)

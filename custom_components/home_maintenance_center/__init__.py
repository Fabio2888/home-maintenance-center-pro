"""
Home Maintenance Center Pro.

Custom integration for Home Assistant.

Copyright (c) 2026 Fabio2888
Licensed under the MIT License.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_track_time_change

from .calendar_sync import CONF_LOCAL_CALENDAR_ENTITY, CalendarSyncManager
from .const import DOMAIN, PLATFORMS
from .coordinator import HomeMaintenanceCoordinator
from .notify import NotificationManager
from .repairs import async_check_repairs
from .services import (
    async_register_services,
    async_unregister_services,
)

_LOGGER = logging.getLogger(__name__)

LOCAL_CALENDAR_NAME = "Manutenzioni Casa"
_PROVISION_FLAG = "_local_calendar_provisioned"


async def async_setup(
    hass: HomeAssistant,
    config: dict[str, Any],
) -> bool:
    """Set up the Home Maintenance integration."""

    hass.data.setdefault(DOMAIN, {})

    _LOGGER.debug("Initializing %s", DOMAIN)

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Home Maintenance Center Pro from a config entry."""

    coordinator = HomeMaintenanceCoordinator(
        hass=hass,
        config_entry=entry,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    entry.async_on_unload(
        entry.add_update_listener(async_reload_entry)
    )

    # --- Servizi (add_item, mark_completed, ecc.) --------------------
    # In precedenza non venivano mai registrati: i servizi
    # home_maintenance_center.* non esistevano affatto in Home
    # Assistant, per quanto documentati in services.yaml.
    await async_register_services(hass, coordinator)

    # --- Sincronizzazione su calendario locale ------------------------
    calendar_sync = CalendarSyncManager(hass, coordinator, entry)
    hass.data[DOMAIN][f"{entry.entry_id}_calendar_sync"] = (
        calendar_sync
    )

    def _handle_coordinator_update() -> None:
        hass.async_create_task(calendar_sync.async_sync_all())
        hass.async_create_task(async_check_repairs(hass, entry))

    entry.async_on_unload(
        coordinator.async_add_listener(_handle_coordinator_update)
    )

    await calendar_sync.async_sync_all()
    await async_check_repairs(hass, entry)

    # Se non è ancora stato scelto (o creato) nessun calendario
    # locale, ne creiamo uno automaticamente in background. È
    # "best effort": in caso di problemi (versione di HA diversa,
    # integrazione local_calendar non disponibile, ecc.) l'errore
    # viene solo loggato e l'utente può sempre impostarlo a mano
    # dalle Opzioni, senza che il resto dell'integrazione ne risenta.
    entry.async_create_background_task(
        hass,
        _async_ensure_local_calendar(hass, entry),
        "home_maintenance_local_calendar_setup",
    )

    # --- Notifiche (persistenti + push sui dispositivi scelti) -------
    # Anche il motore di notifica esisteva già nel codice ma non era
    # mai schedulato: nessuna notifica veniva mai inviata.
    notification_manager = NotificationManager(
        hass, coordinator, entry
    )
    hass.data[DOMAIN][f"{entry.entry_id}_notify"] = (
        notification_manager
    )

    notification_hour = entry.options.get(
        "notification_hour", 9
    )

    async def _scheduled_notification_check(now) -> None:
        await notification_manager.async_check_notifications()

    entry.async_on_unload(
        async_track_time_change(
            hass,
            _scheduled_notification_check,
            hour=notification_hour,
            minute=0,
            second=0,
        )
    )

    _LOGGER.info(
        "Loaded Home Maintenance Center Pro (%s)",
        entry.entry_id,
    )

    return True


async def _async_ensure_local_calendar(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Best-effort auto-creation of a local_calendar entry.

    Runs once per config entry (tracked via entry.data), so it never
    repeats on subsequent restarts even if it failed or the user
    later removes the calendar it created.
    """

    if entry.data.get(_PROVISION_FLAG):
        return

    if entry.options.get(CONF_LOCAL_CALENDAR_ENTITY):
        # L'utente ha già scelto (o questo processo ha già creato)
        # un calendario: non serve fare nulla.
        hass.config_entries.async_update_entry(
            entry,
            data={**entry.data, _PROVISION_FLAG: True},
        )
        return

    new_options = dict(entry.options)

    try:
        result = await hass.config_entries.flow.async_init(
            "local_calendar",
            context={"source": "user"},
            data={"calendar_name": LOCAL_CALENDAR_NAME},
        )

        if result.get("type") == "create_entry":
            new_entry_id = result["result"].entry_id

            ent_reg = er.async_get(hass)

            for entity in ent_reg.entities.values():
                if (
                    entity.config_entry_id == new_entry_id
                    and entity.domain == "calendar"
                ):
                    new_options[CONF_LOCAL_CALENDAR_ENTITY] = (
                        entity.entity_id
                    )

                    _LOGGER.info(
                        "Creato automaticamente il calendario "
                        "locale %s per Home Maintenance Center Pro",
                        entity.entity_id,
                    )

                    break
        else:
            _LOGGER.debug(
                "local_calendar non creato automaticamente "
                "(%s): puoi impostarne uno dalle Opzioni "
                "dell'integrazione.",
                result.get("reason", result.get("type")),
            )

    except Exception as err:  # noqa: BLE001
        _LOGGER.warning(
            "Creazione automatica del calendario locale non "
            "riuscita (puoi impostarlo manualmente dalle "
            "Opzioni dell'integrazione): %s",
            err,
        )

    hass.config_entries.async_update_entry(
        entry,
        data={**entry.data, _PROVISION_FLAG: True},
        options=new_options,
    )


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        hass.data[DOMAIN].pop(
            f"{entry.entry_id}_calendar_sync", None
        )
        hass.data[DOMAIN].pop(f"{entry.entry_id}_notify", None)

        await async_unregister_services(hass)

        _LOGGER.info(
            "Unloaded Home Maintenance Center Pro (%s)",
            entry.entry_id,
        )

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload a config entry."""

    await hass.config_entries.async_reload(entry.entry_id)

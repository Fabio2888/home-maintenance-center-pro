"""
Notification engine for Home Maintenance Center Pro.
"""

from __future__ import annotations

import logging
from datetime import date

from homeassistant.core import HomeAssistant
from homeassistant.components import persistent_notification

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_NOTIFICATION_DAYS = (30, 15, 7, 3, 1)

CONF_NOTIFY_SERVICE = "notify_service"


class NotificationManager:
    """Manage maintenance notifications."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator,
        config_entry,
    ) -> None:
        self.hass = hass
        self.coordinator = coordinator
        self.entry = config_entry

    @property
    def _notify_service(self) -> str | None:
        """Return the configured notify.* service name, if any."""

        return (
            self.entry.options.get(CONF_NOTIFY_SERVICE)
            or None
        )

    async def _dispatch(
        self,
        title: str,
        message: str,
        notification_id: str,
    ) -> None:
        """Send a persistent notification and, if configured, a push."""

        persistent_notification.async_create(
            self.hass,
            message=message,
            title=title,
            notification_id=notification_id,
        )

        service = self._notify_service

        if not service:
            return

        if not self.hass.services.has_service(
            "notify", service
        ):
            _LOGGER.warning(
                "Servizio notify.%s non trovato: controlla "
                "il dispositivo scelto nelle opzioni "
                "dell'integrazione.",
                service,
            )
            return

        try:
            await self.hass.services.async_call(
                "notify",
                service,
                {
                    "title": title,
                    "message": message,
                },
                blocking=True,
            )
        except Exception as err:  # noqa: BLE001
            _LOGGER.warning(
                "Invio notifica push tramite notify.%s "
                "fallito: %s",
                service,
                err,
            )

    async def async_check_notifications(self) -> None:
        """Check all maintenance items."""

        notification_days = tuple(
            self.entry.options.get(
                "notification_days",
                DEFAULT_NOTIFICATION_DAYS,
            )
        )

        repeat_overdue = self.entry.options.get(
            "repeat_notifications",
            True,
        )

        today = date.today()

        for item in self.coordinator.items:

            if not item.enabled:
                continue

            if not item.notify:
                continue

            if item.next_maintenance is None:
                continue

            remaining = (
                item.next_maintenance - today
            ).days

            if remaining in notification_days:
                await self._notify_due(
                    item,
                    remaining,
                )

            elif remaining < 0 and repeat_overdue:
                await self._notify_overdue(
                    item,
                    abs(remaining),
                )

    async def _notify_due(
        self,
        item,
        remaining: int,
    ) -> None:
        """Notify upcoming maintenance."""

        title = f"Manutenzione: {item.name}"

        message = (
            f"La manutenzione '{item.name}' "
            f"scade tra {remaining} giorno/i.\n\n"
            f"Categoria: {item.category}\n"
            f"Prossima manutenzione: {item.next_maintenance}"
        )

        await self._dispatch(
            title,
            message,
            notification_id=f"{DOMAIN}_{item.item_id}",
        )

    async def _notify_overdue(
        self,
        item,
        overdue_days: int,
    ) -> None:
        """Notify overdue maintenance."""

        title = f"Manutenzione scaduta: {item.name}"

        message = (
            f"La manutenzione '{item.name}' "
            f"è scaduta da {overdue_days} giorno/i.\n\n"
            f"Data prevista: {item.next_maintenance}"
        )

        await self._dispatch(
            title,
            message,
            notification_id=f"{DOMAIN}_{item.item_id}_overdue",
        )
"""
Notification engine for Home Maintenance Center Pro.
"""

from __future__ import annotations

from datetime import date

from homeassistant.core import HomeAssistant
from homeassistant.components import persistent_notification

from .const import DOMAIN


DEFAULT_NOTIFICATION_DAYS = (30, 15, 7, 3, 1)


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

        title = f"Maintenance: {item.name}"

        message = (
            f"The maintenance '{item.name}' "
            f"is due in {remaining} day(s).\n\n"
            f"Category: {item.category}\n"
            f"Next maintenance: {item.next_maintenance}"
        )

        persistent_notification.async_create(
            self.hass,
            message=message,
            title=title,
            notification_id=f"{DOMAIN}_{item.item_id}",
        )

    async def _notify_overdue(
        self,
        item,
        overdue_days: int,
    ) -> None:
        """Notify overdue maintenance."""

        title = f"Maintenance overdue: {item.name}"

        message = (
            f"The maintenance '{item.name}' "
            f"is overdue by {overdue_days} day(s).\n\n"
            f"Scheduled date: {item.next_maintenance}"
        )

        persistent_notification.async_create(
            self.hass,
            message=message,
            title=title,
            notification_id=f"{DOMAIN}_{item.item_id}_overdue",
        )
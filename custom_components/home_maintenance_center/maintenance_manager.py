"""
Business logic manager for Home Maintenance Center Pro.
"""

from __future__ import annotations

from datetime import timedelta

from .history import HistoryManager
from .models.maintenance_item import MaintenanceItem
from .notify import NotificationManager
from .statistics import StatisticsManager
from .validators import validate_item


class MaintenanceManager:
    """Main business logic manager."""

    def __init__(
        self,
        coordinator,
        storage,
        config_entry,
        hass,
    ) -> None:
        self.coordinator = coordinator
        self.storage = storage

        self.history = HistoryManager()
        self.statistics = StatisticsManager(self.history)
        self.notifications = NotificationManager(
            hass,
            coordinator,
            config_entry,
        )

    async def add_item(
        self,
        item: MaintenanceItem,
    ) -> None:
        """Add a maintenance item."""

        errors = validate_item(item)

        if errors:
            raise ValueError(errors)

        self.coordinator.items.append(item)

        await self.storage.async_save(
            self.coordinator.items
        )

        await self.coordinator.async_request_refresh()

    async def update_item(
        self,
        item: MaintenanceItem,
    ) -> None:
        """Update an existing item."""

        errors = validate_item(item)

        if errors:
            raise ValueError(errors)

        for index, existing in enumerate(
            self.coordinator.items
        ):
            if existing.item_id == item.item_id:
                self.coordinator.items[index] = item
                break

        await self.storage.async_save(
            self.coordinator.items
        )

        await self.coordinator.async_request_refresh()

    async def delete_item(
        self,
        item_id: str,
    ) -> None:
        """Delete a maintenance item."""

        self.coordinator.items = [
            item
            for item in self.coordinator.items
            if item.item_id != item_id
        ]

        self.history.delete_history(item_id)

        await self.storage.async_save(
            self.coordinator.items
        )

        await self.coordinator.async_request_refresh()

    async def mark_completed(
        self,
        item_id: str,
        *,
        notes: str | None = None,
        cost: float | None = None,
        performed_by: str | None = None,
    ) -> None:
        """Mark maintenance as completed."""

        item = self.coordinator.get_item(item_id)

        if item is None:
            raise ValueError(item_id)

        self.history.add_entry(
            item_id=item.item_id,
            notes=notes,
            cost=cost,
            performed_by=performed_by,
        )

        item.last_maintenance = item.next_maintenance

        if item.last_maintenance:
            item.next_maintenance = (
                item.last_maintenance
                + timedelta(days=item.interval_days)
            )

        await self.storage.async_save(
            self.coordinator.items
        )

        await self.coordinator.async_request_refresh()

    async def postpone(
        self,
        item_id: str,
        days: int,
    ) -> None:
        """Postpone maintenance."""

        item = self.coordinator.get_item(item_id)

        if (
            item is None
            or item.next_maintenance is None
        ):
            return

        item.next_maintenance += timedelta(
            days=days
        )

        await self.storage.async_save(
            self.coordinator.items
        )

        await self.coordinator.async_request_refresh()

    async def check_notifications(self) -> None:
        """Run notification engine."""

        await self.notifications.async_check_notifications()

    def statistics_summary(self):
        """Return current statistics."""

        return self.statistics.calculate(
            self.coordinator.items
        )
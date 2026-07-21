"""
Coordinator for Home Maintenance Center Pro.
"""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN
from .managers.storage_manager import StorageManager
from .models.maintenance_item import MaintenanceItem

_LOGGER = logging.getLogger(__name__)


class HomeMaintenanceCoordinator(DataUpdateCoordinator[dict]):
    """Main coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize coordinator."""

        self.config_entry = config_entry
        self.storage = StorageManager(hass)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self) -> dict:
        """Fetch latest data from storage."""

        try:
            await self.storage.async_load()

            items = self.storage.get_items()

            return {
                "items": items,
                "count": len(items),
            }

        except Exception as err:
            raise UpdateFailed(
                f"Unable to update maintenance data: {err}"
            ) from err

    # ---------------------------------------------------------------------
    # Base data
    # ---------------------------------------------------------------------

    @property
    def items(self) -> list[MaintenanceItem]:
        """Return all maintenance items."""

        return self.data.get("items", [])

    @property
    def enabled_items(self) -> list[MaintenanceItem]:
        """Return enabled maintenance items."""

        return [
            item
            for item in self.items
            if item.enabled
        ]

    @property
    def disabled_items(self) -> list[MaintenanceItem]:
        """Return disabled maintenance items."""

        return [
            item
            for item in self.items
            if not item.enabled
        ]

    @property
    def item_count(self) -> int:
        """Return total maintenance items."""

        return len(self.items)

    @property
    def enabled_count(self) -> int:
        """Return enabled maintenance count."""

        return len(self.enabled_items)

    @property
    def disabled_count(self) -> int:
        """Return disabled maintenance count."""

        return len(self.disabled_items)

    # ---------------------------------------------------------------------
    # Maintenance status
    # ---------------------------------------------------------------------

    @property
    def due_items(self) -> list[MaintenanceItem]:
        """Return maintenance items due within 30 days."""

        return [
            item
            for item in self.enabled_items
            if 0 <= item.days_remaining <= 30
        ]

    @property
    def overdue_items(self) -> list[MaintenanceItem]:
        """Return overdue maintenance items."""

        return [
            item
            for item in self.enabled_items
            if item.overdue
        ]

    @property
    def ok_items(self) -> list[MaintenanceItem]:
        """Return maintenance items not requiring attention."""

        return [
            item
            for item in self.enabled_items
            if item.days_remaining > 30
        ]

    @property
    def due_count(self) -> int:
        """Return due maintenance count."""

        return len(self.due_items)

    @property
    def overdue_count(self) -> int:
        """Return overdue maintenance count."""

        return len(self.overdue_items)

    @property
    def ok_count(self) -> int:
        """Return maintenance items in good status."""

        return len(self.ok_items)

    @property
    def attention_required(self) -> bool:
        """Return True if any maintenance requires attention."""

        return self.overdue_count > 0

    @property
    def next_due_item(self) -> MaintenanceItem | None:
        """Return the next maintenance item due."""

        candidates = [
            item
            for item in self.enabled_items
            if item.next_maintenance is not None
        ]

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda item: item.next_maintenance,
        )

    @property
    def next_due_name(self) -> str | None:
        """Return next maintenance name."""

        item = self.next_due_item

        if item is None:
            return None

        return item.name

    @property
    def next_due_days(self) -> int | None:
        """Return days until next maintenance."""

        item = self.next_due_item

        if item is None:
            return None

        return item.days_remaining

    # ---------------------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------------------

    async def async_add_item(
        self,
        item: MaintenanceItem,
    ) -> None:
        """Add a maintenance item."""

        await self.storage.add_item(item)

        await self.async_request_refresh()

    async def async_update_item(
        self,
        item: MaintenanceItem,
    ) -> None:
        """Update a maintenance item."""

        await self.storage.update_item(item)

        await self.async_request_refresh()

    async def async_delete_item(
        self,
        item_id: str,
    ) -> None:
        """Delete a maintenance item."""

        await self.storage.delete_item(item_id)

        await self.async_request_refresh()

    async def async_reload(self) -> None:
        """Reload coordinator."""

        await self.async_request_refresh()

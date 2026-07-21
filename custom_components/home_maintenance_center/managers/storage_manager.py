"""
Storage Manager for Home Maintenance Center Pro.
"""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from ..const import DOMAIN, STORAGE_KEY, STORAGE_VERSION
from ..default_items import get_default_items
from ..models.maintenance_item import MaintenanceItem

_LOGGER = logging.getLogger(__name__)


class StorageManager:
    """Handle persistent storage."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize storage."""

        self.hass = hass

        self.store: Store = Store(
            hass,
            STORAGE_VERSION,
            STORAGE_KEY,
        )

        self.items: dict[str, MaintenanceItem] = {}

    async def async_load(self) -> None:
        """Load stored data."""

        data = await self.store.async_load()

        if not data:

            _LOGGER.info(
                "First start detected, creating default maintenance items."
            )

            self.items = {
                item.item_id: item
                for item in get_default_items()
            }

            await self.async_save()
            return

        self.items = {
            item["item_id"]: MaintenanceItem.from_dict(item)
            for item in data.get("items", [])
        }

        _LOGGER.info(
            "Loaded %s maintenance items.",
            len(self.items),
        )

    async def async_save(self) -> None:
        """Save data."""

        for item in self.items.values():
            item.calculate_next_maintenance()

        await self.store.async_save(
            {
                "items": [
                    item.to_dict()
                    for item in self.items.values()
                ]
            }
        )

    def get_items(self) -> list[MaintenanceItem]:
        """Return all items."""

        return list(self.items.values())

    def get_item(
        self,
        item_id: str,
    ) -> MaintenanceItem | None:
        """Return one item."""

        return self.items.get(item_id)

    async def add_item(
        self,
        item: MaintenanceItem,
    ) -> None:
        """Add a maintenance item."""

        item.calculate_next_maintenance()

        self.items[item.item_id] = item

        await self.async_save()

    async def update_item(
        self,
        item: MaintenanceItem,
    ) -> None:
        """Update maintenance item."""

        item.calculate_next_maintenance()

        self.items[item.item_id] = item

        await self.async_save()

    async def delete_item(
        self,
        item_id: str,
    ) -> None:
        """Delete maintenance item."""

        self.items.pop(item_id, None)

        await self.async_save()

    async def clear(self) -> None:
        """Remove all maintenance items."""

        self.items.clear()

        await self.async_save()

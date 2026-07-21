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
        """
        Fetch latest data.

        The coordinator never performs business logic.
        It simply exposes the current storage state.
        """

        try:
            await self.storage.async_load()

            return {
                "items": self.storage.get_items(),
                "count": len(self.storage.get_items()),
            }

        except Exception as err:
            raise UpdateFailed(
                f"Unable to update maintenance data: {err}"
            ) from err

    @property
    def items(self):
        """Return all maintenance items."""

        return self.data.get("items", [])

    @property
    def item_count(self) -> int:
        """Return number of items."""

        return self.data.get("count", 0)

    async def async_add_item(self, item) -> None:
        """Add new maintenance item."""

        await self.storage.add_item(item)

        await self.async_request_refresh()

    async def async_update_item(self, item) -> None:
        """Update maintenance item."""

        await self.storage.update_item(item)

        await self.async_request_refresh()

    async def async_delete_item(
        self,
        item_id: str,
    ) -> None:
        """Delete maintenance item."""

        await self.storage.delete_item(item_id)

        await self.async_request_refresh()

    async def async_reload(self) -> None:
        """Force reload."""

        await self.async_request_refresh()
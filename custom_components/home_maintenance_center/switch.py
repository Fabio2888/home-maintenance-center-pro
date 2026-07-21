"""
Switch platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import HomeMaintenanceCoordinator
from .entity import HomeMaintenanceEntity
from .models.maintenance_item import MaintenanceItem


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Home Maintenance switch entities."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    async_add_entities(
        [
            MaintenanceEnabledSwitch(
                coordinator,
                item,
            )
            for item in coordinator.items
        ]
    )


class MaintenanceEnabledSwitch(
    HomeMaintenanceEntity,
    SwitchEntity,
):
    """Enable or disable maintenance tracking."""

    _attr_translation_key = "enabled"
    _attr_icon = "mdi:calendar-check"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item: MaintenanceItem,
    ) -> None:
        """Initialize the switch."""

        super().__init__(
            coordinator,
            item,
        )

        self._entity_suffix = "enabled"

    @property
    def is_on(self) -> bool:
        """Return True if monitoring is enabled."""

        return self.item.enabled

    async def async_turn_on(
        self,
        **kwargs: Any,
    ) -> None:
        """Enable maintenance monitoring."""

        self.item.enabled = True

        await self.coordinator.async_update_item(
            self.item
        )

    async def async_turn_off(
        self,
        **kwargs: Any,
    ) -> None:
        """Disable maintenance monitoring."""

        self.item.enabled = False

        await self.coordinator.async_update_item(
            self.item
        )

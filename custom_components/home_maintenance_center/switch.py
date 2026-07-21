"""
Switch platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import HomeMaintenanceCoordinator
from .entity import HomeMaintenanceEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch entities."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    entities = [
        MaintenanceEnabledSwitch(
            coordinator,
            item,
        )
        for item in coordinator.items
    ]

    async_add_entities(entities)


class MaintenanceEnabledSwitch(
    HomeMaintenanceEntity,
    SwitchEntity,
):
    """Enable or disable maintenance tracking."""

    _attr_icon = "mdi:calendar-check"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item,
    ) -> None:
        """Initialize switch."""

        super().__init__(coordinator, item)

        self._attr_name = "Monitoring Enabled"

    @property
    def is_on(self) -> bool:
        """Return if monitoring is enabled."""

        return self.item.enabled

    async def async_turn_on(self, **kwargs) -> None:
        """Enable monitoring."""

        self.item.enabled = True

        await self.coordinator.async_update_item(
            self.item
        )

    async def async_turn_off(self, **kwargs) -> None:
        """Disable monitoring."""

        self.item.enabled = False

        await self.coordinator.async_update_item(
            self.item
        )
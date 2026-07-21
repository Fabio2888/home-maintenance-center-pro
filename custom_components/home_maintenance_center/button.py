"""
Button platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
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
    """Set up Home Maintenance buttons."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    async_add_entities(
        [
            MaintenanceDoneButton(
                coordinator,
                item,
            )
            for item in coordinator.items
        ]
    )


class MaintenanceDoneButton(
    HomeMaintenanceEntity,
    ButtonEntity,
):
    """Button used to register a completed maintenance."""

    _attr_name = "Mark Maintenance Done"

    _attr_icon = "mdi:check-circle-outline"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item: MaintenanceItem,
    ) -> None:
        """Initialize button."""

        super().__init__(
            coordinator,
            item,
        )

    async def async_press(self) -> None:
        """Mark maintenance as completed."""

        self.item.mark_completed()

        await self.coordinator.async_update_item(
            self.item
        )

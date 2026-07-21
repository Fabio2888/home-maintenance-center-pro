"""
Button platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from datetime import date, timedelta

from homeassistant.components.button import ButtonEntity
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
    """Set up Home Maintenance buttons."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    entities = [
        MaintenanceDoneButton(
            coordinator,
            item,
        )
        for item in coordinator.items
    ]

    async_add_entities(entities)


class MaintenanceDoneButton(
    HomeMaintenanceEntity,
    ButtonEntity,
):
    """Button used to register a completed maintenance."""

    _attr_icon = "mdi:check-circle-outline"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item,
    ) -> None:
        """Initialize button."""

        super().__init__(coordinator, item)

        self._attr_name = "Mark Maintenance Done"

    async def async_press(self) -> None:
        """Handle button press."""

        today = date.today()

        self.item.last_maintenance = today
        self.item.next_maintenance = (
            today + timedelta(days=self.item.interval_days)
        )

        await self.coordinator.async_update_item(
            self.item
        )
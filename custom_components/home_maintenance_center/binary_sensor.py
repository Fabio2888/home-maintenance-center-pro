"""
Binary Sensor platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
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
    """Set up binary sensors."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    async_add_entities(
        [
            entity
            for item in coordinator.items
            for entity in (
                MaintenanceDueBinarySensor(
                    coordinator,
                    item,
                ),
                MaintenanceOverdueBinarySensor(
                    coordinator,
                    item,
                ),
            )
        ]
    )


class MaintenanceDueBinarySensor(
    HomeMaintenanceEntity,
    BinarySensorEntity,
):
    """Maintenance due sensor."""

    _attr_name = "Maintenance Due"

    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    _attr_icon = "mdi:calendar-alert"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item: MaintenanceItem,
    ) -> None:
        """Initialize entity."""

        super().__init__(
            coordinator,
            item,
        )

    @property
    def is_on(self) -> bool:
        """Return True if maintenance is approaching."""

        if self.item.days_remaining is None:
            return False

        return self.item.days_remaining <= 30


class MaintenanceOverdueBinarySensor(
    HomeMaintenanceEntity,
    BinarySensorEntity,
):
    """Maintenance overdue sensor."""

    _attr_name = "Maintenance Overdue"

    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    _attr_icon = "mdi:alert-circle"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item: MaintenanceItem,
    ) -> None:
        """Initialize entity."""

        super().__init__(
            coordinator,
            item,
        )

    @property
    def is_on(self) -> bool:
        """Return True if maintenance is overdue."""

        return self.item.overdue

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
    """Set up Home Maintenance binary sensors."""

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
    """Maintenance due binary sensor."""

    _attr_translation_key = "due"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:calendar-alert"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item: MaintenanceItem,
    ) -> None:
        """Initialize the binary sensor."""

        super().__init__(
            coordinator,
            item,
        )

        self._entity_suffix = "due"

    @property
    def is_on(self) -> bool:
        """Return True if maintenance is due soon."""

        if self.item.days_remaining is None:
            return False

        return 0 <= self.item.days_remaining <= 30


class MaintenanceOverdueBinarySensor(
    HomeMaintenanceEntity,
    BinarySensorEntity,
):
    """Maintenance overdue binary sensor."""

    _attr_translation_key = "overdue"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:alert-circle"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item: MaintenanceItem,
    ) -> None:
        """Initialize the binary sensor."""

        super().__init__(
            coordinator,
            item,
        )

        self._entity_suffix = "overdue"

    @property
    def is_on(self) -> bool:
        """Return True if maintenance is overdue."""

        return self.item.overdue

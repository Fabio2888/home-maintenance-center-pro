"""
Binary Sensor platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from datetime import date

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


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensors."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    entities = []

    for item in coordinator.items:
        entities.extend(
            [
                MaintenanceDueBinarySensor(
                    coordinator,
                    item,
                ),
                MaintenanceOverdueBinarySensor(
                    coordinator,
                    item,
                ),
            ]
        )

    async_add_entities(entities)


class MaintenanceDueBinarySensor(
    HomeMaintenanceEntity,
    BinarySensorEntity,
):
    """Maintenance due sensor."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:calendar-alert"

    def __init__(
        self,
        coordinator,
        item,
    ) -> None:
        super().__init__(coordinator, item)

        self._attr_name = "Maintenance Due"

    @property
    def is_on(self) -> bool:
        """Return True if maintenance is approaching."""

        if self.item.next_maintenance is None:
            return False

        days = (
            self.item.next_maintenance
            - date.today()
        ).days

        return days <= 30


class MaintenanceOverdueBinarySensor(
    HomeMaintenanceEntity,
    BinarySensorEntity,
):
    """Maintenance overdue sensor."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:alert-circle"

    def __init__(
        self,
        coordinator,
        item,
    ) -> None:
        super().__init__(coordinator, item)

        self._attr_name = "Maintenance Overdue"

    @property
    def is_on(self) -> bool:
        """Return True if maintenance is overdue."""

        if self.item.next_maintenance is None:
            return False

        return self.item.next_maintenance < date.today()
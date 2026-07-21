"""
Sensor platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
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
    """Set up Home Maintenance sensors."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    async_add_entities(
        [
            DaysRemainingSensor(
                coordinator,
                item,
            )
            for item in coordinator.items
        ]
    )


class DaysRemainingSensor(
    HomeMaintenanceEntity,
    SensorEntity,
):
    """Days remaining sensor."""

    _attr_translation_key = "days_remaining"
    _attr_icon = "mdi:calendar-clock"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTime.DAYS

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item: MaintenanceItem,
    ) -> None:
        """Initialize the sensor."""

        super().__init__(
            coordinator,
            item,
        )

        self._entity_suffix = "days_remaining"

    @property
    def native_value(self) -> int | None:
        """Return the remaining days before maintenance."""

        return self.item.days_remaining

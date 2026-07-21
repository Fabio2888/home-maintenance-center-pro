"""
Sensor platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from datetime import date

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


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Home Maintenance sensors."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    entities = []

    for item in coordinator.items:
        entities.append(
            DaysRemainingSensor(
                coordinator,
                item,
            )
        )

    async_add_entities(entities)


class DaysRemainingSensor(
    HomeMaintenanceEntity,
    SensorEntity,
):
    """Days remaining sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    _attr_native_unit_of_measurement = UnitOfTime.DAYS

    _attr_icon = "mdi:calendar-clock"

    def __init__(
        self,
        coordinator,
        item,
    ) -> None:
        """Initialize sensor."""

        super().__init__(
            coordinator,
            item,
        )

        self._attr_name = "Days Remaining"

    @property
    def native_value(self):
        """Return days remaining."""

        if self.item.next_maintenance is None:
            return None

        return (
            self.item.next_maintenance
            - date.today()
        ).days
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

    _attr_name = "Days Remaining"

    _attr_icon = "mdi:calendar-clock"

    _attr_state_class = SensorStateClass.MEASUREMENT

    _attr_native_unit_of_measurement = UnitOfTime.DAYS

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item,
    ) -> None:
        """Initialize sensor."""

        super().__init__(
            coordinator,
            item,
        )

    @property
    def native_value(self) -> int | None:
        """Return days remaining."""

        if self.item.next_maintenance is None:
            return None

        return (
            self.item.next_maintenance
            - date.today()
        ).days

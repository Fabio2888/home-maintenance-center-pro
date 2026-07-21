"""
Number platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from datetime import timedelta

from homeassistant.components.number import (
    NumberEntity,
    NumberMode,
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
    """Set up Home Maintenance number entities."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    async_add_entities(
        [
            MaintenanceIntervalNumber(
                coordinator,
                item,
            )
            for item in coordinator.items
        ]
    )


class MaintenanceIntervalNumber(
    HomeMaintenanceEntity,
    NumberEntity,
):
    """Maintenance interval number entity."""

    _attr_translation_key = "interval"
    _attr_icon = "mdi:calendar-edit"

    _attr_native_min_value = 1
    _attr_native_max_value = 3650
    _attr_native_step = 1

    _attr_mode = NumberMode.BOX

    _attr_native_unit_of_measurement = UnitOfTime.DAYS

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item: MaintenanceItem,
    ) -> None:
        """Initialize the number entity."""

        super().__init__(
            coordinator,
            item,
        )

        self._entity_suffix = "interval"

    @property
    def native_value(self) -> float:
        """Return the maintenance interval."""

        return float(self.item.interval_days)

    async def async_set_native_value(
        self,
        value: float,
    ) -> None:
        """Update the maintenance interval."""

        self.item.interval_days = int(value)

        if self.item.last_maintenance is not None:
            self.item.next_maintenance = (
                self.item.last_maintenance
                + timedelta(days=self.item.interval_days)
            )

        await self.coordinator.async_update_item(
            self.item
        )

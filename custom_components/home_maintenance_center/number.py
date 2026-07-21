"""
Number platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from datetime import timedelta

from homeassistant.components.number import NumberEntity, NumberMode
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
    """Set up number entities."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    entities = [
        MaintenanceIntervalNumber(
            coordinator,
            item,
        )
        for item in coordinator.items
    ]

    async_add_entities(entities)


class MaintenanceIntervalNumber(
    HomeMaintenanceEntity,
    NumberEntity,
):
    """Maintenance interval number."""

    _attr_icon = "mdi:calendar-edit"
    _attr_native_min_value = 1
    _attr_native_max_value = 3650
    _attr_native_step = 1
    _attr_mode = NumberMode.BOX
    _attr_native_unit_of_measurement = UnitOfTime.DAYS

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item,
    ) -> None:
        """Initialize entity."""

        super().__init__(coordinator, item)

        self._attr_name = "Maintenance Interval"

    @property
    def native_value(self) -> float:
        """Return interval."""

        return self.item.interval_days

    async def async_set_native_value(
        self,
        value: float,
    ) -> None:
        """Update interval."""

        self.item.interval_days = int(value)

        if self.item.last_maintenance is not None:
            self.item.next_maintenance = (
                self.item.last_maintenance
                + timedelta(days=self.item.interval_days)
            )

        await self.coordinator.async_update_item(
            self.item
        )
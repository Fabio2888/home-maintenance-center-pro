"""
Date platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from datetime import date, timedelta

from homeassistant.components.date import DateEntity
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
    """Set up date entities."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    entities = [
        LastMaintenanceDate(
            coordinator,
            item,
        )
        for item in coordinator.items
    ]

    async_add_entities(entities)


class LastMaintenanceDate(
    HomeMaintenanceEntity,
    DateEntity,
):
    """Last maintenance date."""

    _attr_icon = "mdi:calendar-check"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item,
    ) -> None:
        """Initialize entity."""

        super().__init__(coordinator, item)

        self._attr_name = "Last Maintenance"

    @property
    def native_value(self) -> date | None:
        """Return last maintenance date."""

        return self.item.last_maintenance

    async def async_set_value(
        self,
        value: date,
    ) -> None:
        """Update maintenance date."""

        self.item.last_maintenance = value

        self.item.next_maintenance = (
            value
            + timedelta(days=self.item.interval_days)
        )

        await self.coordinator.async_update_item(
            self.item
        )
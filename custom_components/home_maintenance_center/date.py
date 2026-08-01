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
from .dynamic_entities import async_setup_dynamic_item_entities
from .entity import HomeMaintenanceEntity
from .models.maintenance_item import MaintenanceItem


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Home Maintenance date entities."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    async_setup_dynamic_item_entities(
        coordinator,
        async_add_entities,
        lambda item: [LastMaintenanceDate(coordinator, item)],
    )


class LastMaintenanceDate(
    HomeMaintenanceEntity,
    DateEntity,
):
    """Last maintenance date entity."""

    _attr_translation_key = "last_maintenance"
    _attr_icon = "mdi:calendar-check"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item: MaintenanceItem,
    ) -> None:
        """Initialize the date entity."""

        super().__init__(
            coordinator,
            item,
        )

        self._entity_suffix = "last_maintenance"

    @property
    def native_value(self) -> date | None:
        """Return the last maintenance date."""

        return self.item.last_maintenance

    async def async_set_value(
        self,
        value: date,
    ) -> None:
        """Update the last maintenance date."""

        self.item.last_maintenance = value
        self.item.next_maintenance = (
            value
            + timedelta(days=self.item.interval_days)
        )

        await self.coordinator.async_update_item(
            self.item
        )

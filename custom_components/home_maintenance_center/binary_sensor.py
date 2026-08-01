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
from .dynamic_entities import async_setup_dynamic_item_entities
from .entity import (
    HomeMaintenanceEntity,
    HomeMaintenanceSummaryEntity,
)
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
            AttentionRequiredBinarySensor(coordinator),
            HealthyBinarySensor(coordinator),
        ]
    )

    def _entities_for_item(item: MaintenanceItem):
        return [
            MaintenanceDueBinarySensor(coordinator, item),
            MaintenanceOverdueBinarySensor(coordinator, item),
        ]

    async_setup_dynamic_item_entities(
        coordinator,
        async_add_entities,
        _entities_for_item,
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
        """Initialize entity."""

        super().__init__(
            coordinator,
            item,
        )

        self._entity_suffix = "due"

    @property
    def is_on(self) -> bool:
        """Return True if maintenance is due."""

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
        """Initialize entity."""

        super().__init__(
            coordinator,
            item,
        )

        self._entity_suffix = "overdue"

    @property
    def is_on(self) -> bool:
        """Return True if maintenance is overdue."""

        return self.item.overdue


class AttentionRequiredBinarySensor(
    HomeMaintenanceSummaryEntity,
    BinarySensorEntity,
):
    """Binary sensor indicating that maintenance requires attention."""

    _attr_translation_key = "attention_required"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:alert"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:
        """Initialize entity."""

        super().__init__(coordinator)

        self._entity_suffix = "attention_required"

        self._attr_suggested_object_id = (
            f"{DOMAIN}_attention_required"
        )

    @property
    def is_on(self) -> bool:
        """Return True if attention is required."""

        return self.coordinator.attention_required


class HealthyBinarySensor(
    HomeMaintenanceSummaryEntity,
    BinarySensorEntity,
):
    """Binary sensor indicating that everything is healthy."""

    _attr_translation_key = "healthy"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:check-circle"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:
        """Initialize entity."""

        super().__init__(coordinator)

        self._entity_suffix = "healthy"

        self._attr_suggested_object_id = (
            f"{DOMAIN}_healthy"
        )

    @property
    def is_on(self) -> bool:
        """Return True if no maintenance requires attention."""

        return not self.coordinator.attention_required

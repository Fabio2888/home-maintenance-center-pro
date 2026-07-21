"""
Base entity for Home Maintenance Center Pro.
"""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    MANUFACTURER,
    MODEL,
    VERSION,
)
from .coordinator import HomeMaintenanceCoordinator
from .models.maintenance_item import MaintenanceItem


class HomeMaintenanceEntity(
    CoordinatorEntity[HomeMaintenanceCoordinator]
):
    """Base entity for Home Maintenance Center Pro entities."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item: MaintenanceItem,
    ) -> None:
        """Initialize the entity."""

        super().__init__(coordinator)

        self.item = item

        # This value will be overridden by each platform
        # (sensor, binary_sensor, button, etc.)
        self._entity_suffix = "entity"

        self._attr_suggested_object_id = (
            f"{DOMAIN}_{item.item_id}"
        )

    @property
    def unique_id(self) -> str:
        """Return the unique ID."""

        return (
            f"{DOMAIN}_"
            f"{self.item.item_id}_"
            f"{self._entity_suffix}"
        )

    @property
    def name(self) -> str:
        """Return the device name."""

        return self.item.name

    @property
    def available(self) -> bool:
        """Return entity availability."""

        return super().available and self.item.enabled

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""

        return DeviceInfo(
            identifiers={(DOMAIN, self.item.item_id)},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name=self.item.name,
            sw_version=VERSION,
            configuration_url=(
                "https://github.com/Fabio2888/"
                "home-maintenance-center-pro"
            ),
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return common entity attributes."""

        return {
            "item_id": self.item.item_id,
            "category": self.item.category,
            "priority": self.item.priority,
            "interval_days": self.item.interval_days,
            "last_maintenance": self.item.last_maintenance,
            "next_maintenance": self.item.next_maintenance,
            "days_remaining": self.item.days_remaining,
            "overdue": self.item.overdue,
            "location": self.item.location,
            "model": self.item.model,
            "serial_number": self.item.serial_number,
            "estimated_cost": self.item.estimated_cost,
            "notes": self.item.notes,
            "manual_url": self.item.manual_url,
            "purchase_url": self.item.purchase_url,
            "notify": self.item.notify,
            "tags": self.item.tags,
        }

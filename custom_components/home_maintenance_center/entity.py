"""
Base entities for Home Maintenance Center Pro.
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
    """Base entity for a maintenance item."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item: MaintenanceItem,
    ) -> None:
        """Initialize entity."""

        super().__init__(coordinator)

        self.item = item

        self._entity_suffix = "entity"

        self._attr_suggested_object_id = (
            f"{DOMAIN}_{item.item_id}"
        )

    @property
    def unique_id(self) -> str:
        """Return unique id."""

        return (
            f"{DOMAIN}_"
            f"{self.item.item_id}_"
            f"{self._entity_suffix}"
        )

    @property
    def name(self) -> str:
        """Return maintenance item name."""

        return self.item.name

    @property
    def available(self) -> bool:
        """Return availability."""

        return (
            super().available
            and self.item.enabled
        )

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
        """Return common attributes."""

        return {
            "item_id": self.item.item_id,
            "category": self.item.category,
            "priority": self.item.priority,
            "enabled": self.item.enabled,
            "interval_days": self.item.interval_days,
            "last_maintenance": self.item.last_maintenance,
            "next_maintenance": self.item.next_maintenance,
            "days_remaining": self.item.days_remaining,
            "overdue": self.item.overdue,
            "location": self.item.location,
            "model": self.item.model,
            "serial_number": self.item.serial_number,
            "estimated_cost": self.item.estimated_cost,
            "notify": self.item.notify,
            "notes": self.item.notes,
            "manual_url": self.item.manual_url,
            "purchase_url": self.item.purchase_url,
            "image": self.item.image,
            "tags": self.item.tags,
        }


class HomeMaintenanceSummaryEntity(
    CoordinatorEntity[HomeMaintenanceCoordinator]
):
    """Base class for integration summary entities."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:
        """Initialize summary entity."""

        super().__init__(coordinator)

        self._entity_suffix = "summary"

        self._attr_suggested_object_id = DOMAIN

    @property
    def unique_id(self) -> str:
        """Return unique id."""

        return (
            f"{DOMAIN}_{self._entity_suffix}"
        )

    @property
    def name(self) -> str | None:
        """Use translation_key as entity name."""

        return None

    @property
    def available(self) -> bool:
        """Return availability."""

        return super().available

    @property
    def device_info(self) -> DeviceInfo:
        """Return integration device."""

        return DeviceInfo(
            identifiers={(DOMAIN, DOMAIN)},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name="Home Maintenance Center Pro",
            sw_version=VERSION,
            configuration_url=(
                "https://github.com/Fabio2888/"
                "home-maintenance-center-pro"
            ),
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return summary attributes."""

        next_item = self.coordinator.next_due_item

        return {
            "total_items": self.coordinator.item_count,
            "enabled_items": self.coordinator.enabled_count,
            "disabled_items": self.coordinator.disabled_count,
            "due_items": self.coordinator.due_count,
            "overdue_items": self.coordinator.overdue_count,
            "ok_items": self.coordinator.ok_count,
            "attention_required": self.coordinator.attention_required,
            "next_due_name": (
                next_item.name
                if next_item
                else None
            ),
            "next_due_date": (
                next_item.next_maintenance
                if next_item
                else None
            ),
            "next_due_days": self.coordinator.next_due_days,
        }

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
    """Set up Home Maintenance sensors."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    #
    # Global summary sensors
    #

    async_add_entities(
        [
            TotalSensor(coordinator),
            EnabledSensor(coordinator),
            DisabledSensor(coordinator),
            DueSensor(coordinator),
            OverdueSensor(coordinator),
            OkSensor(coordinator),
            NextDueSensor(coordinator),
            NextDueDaysSensor(coordinator),
        ]
    )

    #
    # One sensor per maintenance item, including any item created
    # later on (no restart required).
    #

    async_setup_dynamic_item_entities(
        coordinator,
        async_add_entities,
        lambda item: [DaysRemainingSensor(coordinator, item)],
    )


#
# ------------------------------------------------------------------
# Maintenance item sensors
# ------------------------------------------------------------------
#


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
        """Initialize sensor."""

        super().__init__(
            coordinator,
            item,
        )

        self._entity_suffix = "days_remaining"

    @property
    def native_value(self) -> int |None:
        """Return remaining days."""

        return self.item.days_remaining


#
# ------------------------------------------------------------------
# Summary sensors
# ------------------------------------------------------------------
#


class TotalSensor(
    HomeMaintenanceSummaryEntity,
    SensorEntity,
):
    """Total maintenance items."""

    _attr_translation_key = "total"
    _attr_icon = "mdi:format-list-numbered"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:

        super().__init__(coordinator)

        self._entity_suffix = "total"

        self._attr_suggested_object_id = (
            f"{DOMAIN}_total"
        )

    @property
    def native_value(self) -> int:
        return self.coordinator.item_count


class EnabledSensor(
    HomeMaintenanceSummaryEntity,
    SensorEntity,
):
    """Enabled maintenance items."""

    _attr_translation_key = "enabled"
    _attr_icon = "mdi:check-circle"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:

        super().__init__(coordinator)

        self._entity_suffix = "enabled"

        self._attr_suggested_object_id = (
            f"{DOMAIN}_enabled"
        )

    @property
    def native_value(self) -> int:
        return self.coordinator.enabled_count


class DisabledSensor(
    HomeMaintenanceSummaryEntity,
    SensorEntity,
):
    """Disabled maintenance items."""

    _attr_translation_key = "disabled"
    _attr_icon = "mdi:close-circle"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:

        super().__init__(coordinator)

        self._entity_suffix = "disabled"

        self._attr_suggested_object_id = (
            f"{DOMAIN}_disabled"
        )

    @property
    def native_value(self) -> int:
        return self.coordinator.disabled_count


class DueSensor(
    HomeMaintenanceSummaryEntity,
    SensorEntity,
):
    """Maintenance due."""

    _attr_translation_key = "due"
    _attr_icon = "mdi:calendar-alert"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:

        super().__init__(coordinator)

        self._entity_suffix = "due"

        self._attr_suggested_object_id = (
            f"{DOMAIN}_due"
        )

    @property
    def native_value(self) -> int:
        return self.coordinator.due_count


class OverdueSensor(
    HomeMaintenanceSummaryEntity,
    SensorEntity,
):
    """Maintenance overdue."""

    _attr_translation_key = "overdue"
    _attr_icon = "mdi:alert-circle"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:

        super().__init__(coordinator)

        self._entity_suffix = "overdue"

        self._attr_suggested_object_id = (
            f"{DOMAIN}_overdue"
        )

    @property
    def native_value(self) -> int:
        return self.coordinator.overdue_count


class OkSensor(
    HomeMaintenanceSummaryEntity,
    SensorEntity,
):
    """Maintenance OK."""

    _attr_translation_key = "ok"
    _attr_icon = "mdi:check"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:

        super().__init__(coordinator)

        self._entity_suffix = "ok"

        self._attr_suggested_object_id = (
            f"{DOMAIN}_ok"
        )

    @property
    def native_value(self) -> int:
        return self.coordinator.ok_count


class NextDueSensor(
    HomeMaintenanceSummaryEntity,
    SensorEntity,
):
    """Next maintenance due."""

    _attr_translation_key = "next_due"
    _attr_icon = "mdi:calendar-arrow-right"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:

        super().__init__(coordinator)

        self._entity_suffix = "next_due"

        self._attr_suggested_object_id = (
            f"{DOMAIN}_next_due"
        )

    @property
    def native_value(self) -> str | None:
        return self.coordinator.next_due_name


class NextDueDaysSensor(
    HomeMaintenanceSummaryEntity,
    SensorEntity,
):
    """Days until next maintenance."""

    _attr_translation_key = "next_due_days"
    _attr_icon = "mdi:calendar-clock"
    _attr_native_unit_of_measurement = UnitOfTime.DAYS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:

        super().__init__(coordinator)

        self._entity_suffix = "next_due_days"

        self._attr_suggested_object_id = (
            f"{DOMAIN}_next_due_days"
        )

    @property
    def native_value(self) -> int | None:
        return self.coordinator.next_due_days

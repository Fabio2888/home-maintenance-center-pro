"""
Calendar platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from datetime import datetime, time

from homeassistant.components.calendar import (
    CalendarEntity,
    CalendarEvent,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    MANUFACTURER,
    MODEL,
    VERSION,
)
from .coordinator import HomeMaintenanceCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Home Maintenance calendar."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    async_add_entities(
        [
            HomeMaintenanceCalendar(
                coordinator,
            )
        ]
    )


class HomeMaintenanceCalendar(
    CoordinatorEntity[HomeMaintenanceCoordinator],
    CalendarEntity,
):
    """Home Maintenance calendar."""

    _attr_name = "Manutenzioni Casa"

    _attr_icon = "mdi:calendar-check"

    _attr_suggested_object_id = "manutenzioni_casa"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:
        """Initialize calendar."""

        super().__init__(coordinator)

        self._attr_unique_id = f"{DOMAIN}_calendar"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""

        return DeviceInfo(
            identifiers={(DOMAIN, "calendar")},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name="Home Maintenance Center Pro",
            sw_version=VERSION,
        )

    @property
    def event(self) -> CalendarEvent | None:
        """Return next upcoming maintenance."""

        upcoming = [
            item
            for item in self.coordinator.items
            if item.enabled
            and item.next_maintenance is not None
        ]

        if not upcoming:
            return None

        item = min(
            upcoming,
            key=lambda x: x.next_maintenance,
        )

        return self._create_event(item)

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return all maintenance events."""

        events: list[CalendarEvent] = []

        for item in self.coordinator.items:

            if (
                not item.enabled
                or item.next_maintenance is None
            ):
                continue

            start = datetime.combine(
                item.next_maintenance,
                time.min,
            )

            if start_date <= start <= end_date:
                events.append(
                    self._create_event(item)
                )

        return sorted(
            events,
            key=lambda event: event.start,
        )

    def _create_event(
        self,
        item,
    ) -> CalendarEvent:
        """Create a calendar event."""

        start = datetime.combine(
            item.next_maintenance,
            time.min,
        )

        end = datetime.combine(
            item.next_maintenance,
            time.max,
        )

        description = "\n".join(
            filter(
                None,
                [
                    f"Categoria: {item.category}",
                    f"Posizione: {item.location}"
                    if item.location
                    else "",
                    f"Priorità: {item.priority}",
                    "",
                    item.notes,
                ],
            )
        )

        return CalendarEvent(
            summary=item.name,
            start=start,
            end=end,
            description=description,
        )

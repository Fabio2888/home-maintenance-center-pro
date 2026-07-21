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
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
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


class HomeMaintenanceCalendar(CalendarEntity):
    """Home Maintenance calendar."""

    _attr_name = "Home Maintenance"
    _attr_icon = "mdi:calendar-check"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:
        """Initialize calendar."""

        self.coordinator = coordinator

        self._attr_unique_id = (
            f"{DOMAIN}_calendar"
        )

    @property
    def event(self) -> CalendarEvent | None:
        """Return next upcoming maintenance."""

        upcoming = [
            item
            for item in self.coordinator.items
            if item.next_maintenance is not None
        ]

        if not upcoming:
            return None

        item = min(
            upcoming,
            key=lambda x: x.next_maintenance,
        )

        start = datetime.combine(
            item.next_maintenance,
            time.min,
        )

        end = datetime.combine(
            item.next_maintenance,
            time.max,
        )

        return CalendarEvent(
            summary=item.name,
            start=start,
            end=end,
            description=item.notes or "",
        )

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return all maintenance events."""

        events = []

        for item in self.coordinator.items:

            if item.next_maintenance is None:
                continue

            start = datetime.combine(
                item.next_maintenance,
                time.min,
            )

            end = datetime.combine(
                item.next_maintenance,
                time.max,
            )

            if start_date <= start <= end_date:

                events.append(
                    CalendarEvent(
                        summary=item.name,
                        start=start,
                        end=end,
                        description=item.notes or "",
                    )
                )

        return sorted(
            events,
            key=lambda event: event.start,
        )
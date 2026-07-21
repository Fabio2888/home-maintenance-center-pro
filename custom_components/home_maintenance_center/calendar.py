"""
Calendar platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from datetime import date

from homeassistant.components.calendar import (
    CalendarEntity,
    CalendarEvent,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HomeMaintenanceCoordinator
from .models.maintenance_item import MaintenanceItem


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

    _attr_name = "Home Maintenance"

    _attr_icon = "mdi:calendar-check"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:
        """Initialize calendar."""

        super().__init__(coordinator)

        self._attr_unique_id = f"{DOMAIN}_calendar"

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
        start_date,
        end_date,
    ) -> list[CalendarEvent]:
        """Return maintenance events."""

        events: list[CalendarEvent] = []

        for item in self.coordinator.items:

            if (
                not item.enabled
                or item.next_maintenance is None
            ):
                continue

            if (
                start_date.date()
                <= item.next_maintenance
                <= end_date.date()
            ):
                events.append(
                    self._create_event(item)
                )

        return sorted(
            events,
            key=lambda event: event.start,
        )

    def _create_event(
        self,
        item: MaintenanceItem,
    ) -> CalendarEvent:
        """Create calendar event."""

        description = "\n".join(
            filter(
                None,
                [
                    f"Category: {item.category}",
                    f"Priority: {item.priority}",
                    f"Location: {item.location}"
                    if item.location
                    else "",
                    "",
                    item.notes,
                ],
            )
        )

        return CalendarEvent(
            summary=item.name,
            start=item.next_maintenance,
            end=item.next_maintenance,
            description=description,
        )

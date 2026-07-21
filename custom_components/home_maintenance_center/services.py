"""
Services for Home Maintenance Center Pro.
"""

from __future__ import annotations

from datetime import date, timedelta

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .coordinator import HomeMaintenanceCoordinator


SERVICE_MARK_COMPLETED = "mark_completed"
SERVICE_ADD_ITEM = "add_item"
SERVICE_REMOVE_ITEM = "remove_item"
SERVICE_POSTPONE_ITEM = "postpone_item"
SERVICE_RESET_ITEM = "reset_item"
SERVICE_RELOAD = "reload"


MARK_COMPLETED_SCHEMA = vol.Schema(
    {
        vol.Required("item_id"): cv.string,
    }
)

REMOVE_ITEM_SCHEMA = vol.Schema(
    {
        vol.Required("item_id"): cv.string,
    }
)

POSTPONE_SCHEMA = vol.Schema(
    {
        vol.Required("item_id"): cv.string,
        vol.Required("days"): vol.All(
            vol.Coerce(int),
            vol.Range(min=1, max=3650),
        ),
    }
)

RESET_SCHEMA = vol.Schema(
    {
        vol.Required("item_id"): cv.string,
    }
)

ADD_ITEM_SCHEMA = vol.Schema(
    {
        vol.Required("name"): cv.string,
        vol.Optional("category", default="General"): cv.string,
        vol.Optional("interval_days", default=180): vol.All(
            vol.Coerce(int),
            vol.Range(min=1, max=3650),
        ),
    }
)


async def async_register_services(
    hass: HomeAssistant,
    coordinator: HomeMaintenanceCoordinator,
) -> None:
    """Register Home Maintenance services."""

    async def mark_completed(call: ServiceCall) -> None:
        """Mark maintenance as completed."""

        item = coordinator.get_item(call.data["item_id"])

        if item is None:
            return

        item.last_maintenance = date.today()
        item.next_maintenance = (
            item.last_maintenance
            + timedelta(days=item.interval_days)
        )

        await coordinator.async_update_item(item)

    async def add_item(call: ServiceCall) -> None:
        """Add new maintenance item."""

        await coordinator.async_add_item(
            name=call.data["name"],
            category=call.data["category"],
            interval_days=call.data["interval_days"],
        )

    async def remove_item(call: ServiceCall) -> None:
        """Remove maintenance item."""

        await coordinator.async_delete_item(
            call.data["item_id"]
        )

    async def postpone_item(call: ServiceCall) -> None:
        """Postpone maintenance."""

        item = coordinator.get_item(call.data["item_id"])

        if item is None:
            return

        item.next_maintenance += timedelta(
            days=call.data["days"]
        )

        await coordinator.async_update_item(item)

    async def reset_item(call: ServiceCall) -> None:
        """Reset maintenance."""

        item = coordinator.get_item(call.data["item_id"])

        if item is None:
            return

        item.last_maintenance = None
        item.next_maintenance = None

        await coordinator.async_update_item(item)

    async def reload(call: ServiceCall) -> None:
        """Reload integration."""

        await coordinator.async_reload()

    hass.services.async_register(
        DOMAIN,
        SERVICE_MARK_COMPLETED,
        mark_completed,
        schema=MARK_COMPLETED_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_ITEM,
        add_item,
        schema=ADD_ITEM_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_REMOVE_ITEM,
        remove_item,
        schema=REMOVE_ITEM_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_POSTPONE_ITEM,
        postpone_item,
        schema=POSTPONE_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_RESET_ITEM,
        reset_item,
        schema=RESET_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_RELOAD,
        reload,
    )


async def async_unregister_services(
    hass: HomeAssistant,
) -> None:
    """Remove all registered services."""

    for service in (
        SERVICE_MARK_COMPLETED,
        SERVICE_ADD_ITEM,
        SERVICE_REMOVE_ITEM,
        SERVICE_POSTPONE_ITEM,
        SERVICE_RESET_ITEM,
        SERVICE_RELOAD,
    ):
        if hass.services.has_service(DOMAIN, service):
            hass.services.async_remove(
                DOMAIN,
                service,
            )
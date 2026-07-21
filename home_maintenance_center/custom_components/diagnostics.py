"""
Diagnostics support for Home Maintenance Center Pro.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


TO_REDACT = {
    "serial_number",
    "manual_url",
    "purchase_url",
    "notes",
    "metadata",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    items = []

    for item in coordinator.items:
        items.append(
            async_redact_data(
                item.to_dict(),
                TO_REDACT,
            )
        )

    return {
        "entry": {
            "entry_id": entry.entry_id,
            "title": entry.title,
            "version": entry.version,
            "minor_version": entry.minor_version,
        },
        "statistics": {
            "total_items": len(coordinator.items),
            "enabled_items": sum(
                1 for item in coordinator.items if item.enabled
            ),
            "disabled_items": sum(
                1 for item in coordinator.items if not item.enabled
            ),
        },
        "items": items,
    }
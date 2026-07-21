"""
Home Maintenance Center Pro.

Custom integration for Home Assistant.

Copyright (c) 2026 Fabio2888
Licensed under the MIT License.
"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import HomeMaintenanceCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: tuple[Platform, ...] = (
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.DATE,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SWITCH,
    Platform.CALENDAR,
)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up Home Maintenance Center Pro."""

    hass.data.setdefault(DOMAIN, {})

    _LOGGER.info("Home Maintenance Center Pro initialized")

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Home Maintenance Center Pro from a config entry."""

    coordinator = HomeMaintenanceCoordinator(
        hass=hass,
        config_entry=entry,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    entry.async_on_unload(
        entry.add_update_listener(async_reload_entry)
    )

    _LOGGER.info("Configuration loaded successfully")

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    _LOGGER.info("Configuration unloaded")

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload configuration."""

    await async_unload_entry(hass, entry)

    await async_setup_entry(hass, entry)
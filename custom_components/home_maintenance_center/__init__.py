"""
Home Maintenance Center Pro.

Custom integration for Home Assistant.

Copyright (c) 2026 Fabio2888
Licensed under the MIT License.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_change

from .calendar_sync import CalendarSyncManager
from .const import DOMAIN, PLATFORMS
from .coordinator import HomeMaintenanceCoordinator
from .notify import NotificationManager
from .services import (
    async_register_services,
    async_unregister_services,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(
    hass: HomeAssistant,
    config: dict[str, Any],
) -> bool:
    """Set up the Home Maintenance integration."""

    hass.data.setdefault(DOMAIN, {})

    _LOGGER.debug("Initializing %s", DOMAIN)

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

    # --- Servizi (add_item, mark_completed, ecc.) --------------------
    # In precedenza non venivano mai registrati: i servizi
    # home_maintenance_center.* non esistevano affatto in Home
    # Assistant, per quanto documentati in services.yaml.
    await async_register_services(hass, coordinator)

    # --- Sincronizzazione su calendario locale ------------------------
    calendar_sync = CalendarSyncManager(hass, coordinator, entry)
    hass.data[DOMAIN][f"{entry.entry_id}_calendar_sync"] = (
        calendar_sync
    )

    def _handle_coordinator_update() -> None:
        hass.async_create_task(calendar_sync.async_sync_all())

    entry.async_on_unload(
        coordinator.async_add_listener(_handle_coordinator_update)
    )

    await calendar_sync.async_sync_all()

    # --- Notifiche (persistenti + push su dispositivo scelto) --------
    # Anche il motore di notifica esisteva già nel codice ma non era
    # mai schedulato: nessuna notifica veniva mai inviata.
    notification_manager = NotificationManager(
        hass, coordinator, entry
    )
    hass.data[DOMAIN][f"{entry.entry_id}_notify"] = (
        notification_manager
    )

    notification_hour = entry.options.get(
        "notification_hour", 9
    )

    async def _scheduled_notification_check(now) -> None:
        await notification_manager.async_check_notifications()

    entry.async_on_unload(
        async_track_time_change(
            hass,
            _scheduled_notification_check,
            hour=notification_hour,
            minute=0,
            second=0,
        )
    )

    _LOGGER.info(
        "Loaded Home Maintenance Center Pro (%s)",
        entry.entry_id,
    )

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
        hass.data[DOMAIN].pop(entry.entry_id, None)
        hass.data[DOMAIN].pop(
            f"{entry.entry_id}_calendar_sync", None
        )
        hass.data[DOMAIN].pop(f"{entry.entry_id}_notify", None)

        await async_unregister_services(hass)

        _LOGGER.info(
            "Unloaded Home Maintenance Center Pro (%s)",
            entry.entry_id,
        )

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload a config entry."""

    await hass.config_entries.async_reload(entry.entry_id)

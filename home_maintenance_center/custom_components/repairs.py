"""
Repairs support for Home Maintenance Center Pro.
"""

from __future__ import annotations

from collections.abc import Iterable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.issue_registry import (
    IssueSeverity,
    async_create_issue,
    async_delete_issue,
)

from .const import DOMAIN


ISSUE_INVALID_INTERVAL = "invalid_interval"
ISSUE_MISSING_NEXT_DATE = "missing_next_date"
ISSUE_DUPLICATE_IDS = "duplicate_item_ids"


async def async_check_repairs(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Run all repair checks."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    await _check_duplicate_ids(
        hass,
        coordinator.items,
    )

    await _check_invalid_interval(
        hass,
        coordinator.items,
    )

    await _check_missing_next_date(
        hass,
        coordinator.items,
    )


async def _check_duplicate_ids(
    hass: HomeAssistant,
    items: Iterable,
) -> None:
    """Detect duplicate IDs."""

    ids = [item.item_id for item in items]

    if len(ids) != len(set(ids)):
        async_create_issue(
            hass,
            DOMAIN,
            ISSUE_DUPLICATE_IDS,
            severity=IssueSeverity.ERROR,
            is_fixable=False,
            translation_key="duplicate_item_ids",
        )
    else:
        async_delete_issue(
            hass,
            DOMAIN,
            ISSUE_DUPLICATE_IDS,
        )


async def _check_invalid_interval(
    hass: HomeAssistant,
    items: Iterable,
) -> None:
    """Detect invalid intervals."""

    invalid = any(
        item.interval_days <= 0
        for item in items
    )

    if invalid:
        async_create_issue(
            hass,
            DOMAIN,
            ISSUE_INVALID_INTERVAL,
            severity=IssueSeverity.ERROR,
            is_fixable=False,
            translation_key="invalid_interval",
        )
    else:
        async_delete_issue(
            hass,
            DOMAIN,
            ISSUE_INVALID_INTERVAL,
        )


async def _check_missing_next_date(
    hass: HomeAssistant,
    items: Iterable,
) -> None:
    """Detect items without next maintenance."""

    invalid = any(
        item.enabled
        and item.next_maintenance is None
        for item in items
    )

    if invalid:
        async_create_issue(
            hass,
            DOMAIN,
            ISSUE_MISSING_NEXT_DATE,
            severity=IssueSeverity.WARNING,
            is_fixable=False,
            translation_key="missing_next_date",
        )
    else:
        async_delete_issue(
            hass,
            DOMAIN,
            ISSUE_MISSING_NEXT_DATE,
        )
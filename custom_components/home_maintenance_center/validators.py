"""
Validation helpers for Home Maintenance Center Pro.
"""

from __future__ import annotations

import re
from datetime import date
from urllib.parse import urlparse

from .models.maintenance_item import MaintenanceItem


MIN_INTERVAL_DAYS = 1
MAX_INTERVAL_DAYS = 3650

MAX_NAME_LENGTH = 100
MAX_CATEGORY_LENGTH = 50
MAX_LOCATION_LENGTH = 100
MAX_MODEL_LENGTH = 100
MAX_SERIAL_LENGTH = 100


def validate_name(name: str) -> bool:
    """Validate maintenance name."""

    if not isinstance(name, str):
        return False

    name = name.strip()

    return (
        len(name) > 0
        and len(name) <= MAX_NAME_LENGTH
    )


def validate_category(category: str) -> bool:
    """Validate category."""

    if category is None:
        return True

    return len(category.strip()) <= MAX_CATEGORY_LENGTH


def validate_interval(interval_days: int) -> bool:
    """Validate interval."""

    return (
        isinstance(interval_days, int)
        and MIN_INTERVAL_DAYS
        <= interval_days
        <= MAX_INTERVAL_DAYS
    )


def validate_date(value: date | None) -> bool:
    """Validate date."""

    return value is None or isinstance(value, date)


def validate_url(url: str | None) -> bool:
    """Validate URL."""

    if not url:
        return True

    parsed = urlparse(url)

    return bool(
        parsed.scheme
        and parsed.netloc
    )


def validate_serial(serial: str | None) -> bool:
    """Validate serial number."""

    if not serial:
        return True

    return (
        len(serial)
        <= MAX_SERIAL_LENGTH
    )


def validate_priority(priority: str) -> bool:
    """Validate priority."""

    return priority in (
        "Low",
        "Normal",
        "High",
        "Critical",
    )


def validate_item(item: MaintenanceItem) -> list[str]:
    """Validate a maintenance item."""

    errors: list[str] = []

    if not validate_name(item.name):
        errors.append("invalid_name")

    if not validate_category(item.category):
        errors.append("invalid_category")

    if not validate_interval(item.interval_days):
        errors.append("invalid_interval")

    if not validate_date(item.last_maintenance):
        errors.append("invalid_last_maintenance")

    if not validate_date(item.next_maintenance):
        errors.append("invalid_next_maintenance")

    if not validate_url(item.manual_url):
        errors.append("invalid_manual_url")

    if not validate_url(item.purchase_url):
        errors.append("invalid_purchase_url")

    if not validate_serial(item.serial_number):
        errors.append("invalid_serial_number")

    if not validate_priority(item.priority):
        errors.append("invalid_priority")

    return errors


def validate_unique_ids(
    items: list[MaintenanceItem],
) -> bool:
    """Validate unique IDs."""

    ids = [
        item.item_id
        for item in items
    ]

    return len(ids) == len(set(ids))


def sanitize_filename(name: str) -> str:
    """Convert a string into a safe filename."""

    return re.sub(
        r"[^a-zA-Z0-9_-]",
        "_",
        name,
    )
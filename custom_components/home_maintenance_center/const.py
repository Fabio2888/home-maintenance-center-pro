"""Constants for Home Maintenance Center Pro."""

from __future__ import annotations

from homeassistant.const import Platform

#
# -----------------------------------------------------------------------------
# Basic information
# -----------------------------------------------------------------------------
#

DOMAIN = "home_maintenance"

NAME = "Home Maintenance Center Pro"

MANUFACTURER = "Fabio2888"

MODEL = "Home Maintenance Center Pro"

VERSION = "2.2.0"

#
# -----------------------------------------------------------------------------
# Platforms
# -----------------------------------------------------------------------------
#

PLATFORMS: tuple[Platform, ...] = (
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.DATE,
    Platform.SWITCH,
    Platform.SELECT,
    Platform.TEXT,
    Platform.CALENDAR,
)

#
# -----------------------------------------------------------------------------
# "Add new item" form categories (shared by select.py and the config/options
# selectors so the list only needs to be maintained in one place)
# -----------------------------------------------------------------------------
#

NEW_ITEM_CATEGORIES: tuple[str, ...] = (
    "HVAC",
    "Water",
    "Electrical",
    "Lighting",
    "Kitchen",
    "Bathroom",
    "Garden",
    "Security",
    "Appliances",
    "Vehicle",
    "IT",
    "Cleaning",
    "Other",
)

#
# -----------------------------------------------------------------------------
# Storage
# -----------------------------------------------------------------------------
#

STORAGE_VERSION = 1

STORAGE_KEY = f"{DOMAIN}_storage"

#
# -----------------------------------------------------------------------------
# Config Entry
# -----------------------------------------------------------------------------
#

CONF_ITEMS = "items"

CONF_HISTORY = "history"

CONF_NOTIFY_SERVICES = "notify_services"

CONF_NOTIFICATIONS_ENABLED = "notifications_enabled"

CONF_WARNING_DAYS = "warning_days"

CONF_LANGUAGE = "language"

#
# -----------------------------------------------------------------------------
# Defaults
# -----------------------------------------------------------------------------
#

DEFAULT_NOTIFY_SERVICES = ""

DEFAULT_WARNING_DAYS = [30, 15, 7, 3, 1]

DEFAULT_LANGUAGE = "it"

DEFAULT_CATEGORY = "general"

DEFAULT_PRIORITY = "normal"

DEFAULT_INTERVAL_DAYS = 180

#
# -----------------------------------------------------------------------------
# Status
# -----------------------------------------------------------------------------
#

STATUS_OK = "ok"

STATUS_WARNING = "warning"

STATUS_OVERDUE = "overdue"

STATUS_COMPLETED = "completed"

#
# -----------------------------------------------------------------------------
# Priority
# -----------------------------------------------------------------------------
#

PRIORITY_LOW = "low"

PRIORITY_NORMAL = "normal"

PRIORITY_HIGH = "high"

PRIORITY_CRITICAL = "critical"

#
# -----------------------------------------------------------------------------
# Categories
# -----------------------------------------------------------------------------
#

CATEGORY_GENERAL = "general"

CATEGORY_WATER = "water"

CATEGORY_HVAC = "hvac"

CATEGORY_BATHROOM = "bathroom"

CATEGORY_ELECTRICAL = "electrical"

CATEGORY_GARDEN = "garden"

CATEGORY_APPLIANCES = "appliances"

CATEGORY_SECURITY = "security"

CATEGORY_OTHER = "other"

#
# -----------------------------------------------------------------------------
# Colors
# -----------------------------------------------------------------------------
#

COLOR_OK = "#43A047"

COLOR_WARNING = "#FB8C00"

COLOR_OVERDUE = "#E53935"

COLOR_INFO = "#1E88E5"

COLOR_DISABLED = "#9E9E9E"

#
# -----------------------------------------------------------------------------
# Events
# -----------------------------------------------------------------------------
#

EVENT_MAINTENANCE_COMPLETED = f"{DOMAIN}_maintenance_completed"

EVENT_MAINTENANCE_CREATED = f"{DOMAIN}_maintenance_created"

EVENT_MAINTENANCE_UPDATED = f"{DOMAIN}_maintenance_updated"

EVENT_MAINTENANCE_DELETED = f"{DOMAIN}_maintenance_deleted"

#
# -----------------------------------------------------------------------------
# Services
# -----------------------------------------------------------------------------
#

SERVICE_MARK_COMPLETED = "mark_completed"

SERVICE_ADD_ITEM = "add_item"

SERVICE_REMOVE_ITEM = "remove_item"

SERVICE_EXPORT = "export"

SERVICE_IMPORT = "import"

#
# -----------------------------------------------------------------------------
# Entity attributes
# -----------------------------------------------------------------------------
#

ATTR_ITEM_ID = "item_id"

ATTR_NAME = "name"

ATTR_CATEGORY = "category"

ATTR_PRIORITY = "priority"

ATTR_STATUS = "status"

ATTR_LAST_DONE = "last_done"

ATTR_NEXT_DUE = "next_due"

ATTR_INTERVAL = "interval"

ATTR_PROGRESS = "progress"

ATTR_NOTES = "notes"

ATTR_MANUAL = "manual"

ATTR_IMAGE = "image"

ATTR_COST = "cost"

ATTR_LINK = "link"

ATTR_MODEL = "model"

ATTR_SERIAL = "serial"

#
# -----------------------------------------------------------------------------
# Icons
# -----------------------------------------------------------------------------
#

ICON_OK = "mdi:check-circle"

ICON_WARNING = "mdi:alert"

ICON_OVERDUE = "mdi:alert-circle"

ICON_CALENDAR = "mdi:calendar"

ICON_HISTORY = "mdi:history"

ICON_SETTINGS = "mdi:cog"

ICON_FILTER = "mdi:water-filter"

ICON_CO2 = "mdi:gas-cylinder"

ICON_HVAC = "mdi:air-conditioner"

ICON_BATHROOM = "mdi:toilet"

ICON_ELECTRICAL = "mdi:flash"

ICON_GARDEN = "mdi:flower"

ICON_APPLIANCE = "mdi:washing-machine"

ICON_SECURITY = "mdi:shield-home"

#
# -----------------------------------------------------------------------------
# Notification tags
# -----------------------------------------------------------------------------
#

NOTIFICATION_TAG = DOMAIN

NOTIFICATION_GROUP = DOMAIN

#
# -----------------------------------------------------------------------------
# Diagnostics
# -----------------------------------------------------------------------------
#

DIAGNOSTICS_REDACT = {
    CONF_NOTIFY_SERVICES,
}

#
# -----------------------------------------------------------------------------
# Logger
# -----------------------------------------------------------------------------
#

LOGGER_NAME = "custom_components.home_maintenance"

"""
Shared selectors for Home Maintenance Center Pro.
"""

from __future__ import annotations

from homeassistant.helpers.selector import (
    BooleanSelector,
    BooleanSelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
)


CATEGORY_SELECTOR = SelectSelector(
    SelectSelectorConfig(
        options=[
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
        ],
        mode=SelectSelectorMode.DROPDOWN,
    )
)


PRIORITY_SELECTOR = SelectSelector(
    SelectSelectorConfig(
        options=[
            "Low",
            "Normal",
            "High",
            "Critical",
        ],
        mode=SelectSelectorMode.DROPDOWN,
    )
)


INTERVAL_SELECTOR = NumberSelector(
    NumberSelectorConfig(
        min=1,
        max=3650,
        step=1,
        mode=NumberSelectorMode.BOX,
    )
)


NOTIFICATION_HOUR_SELECTOR = NumberSelector(
    NumberSelectorConfig(
        min=0,
        max=23,
        step=1,
        mode=NumberSelectorMode.BOX,
    )
)


BOOLEAN_SELECTOR = BooleanSelector(
    BooleanSelectorConfig()
)


TEXT_SELECTOR = TextSelector(
    TextSelectorConfig()
)
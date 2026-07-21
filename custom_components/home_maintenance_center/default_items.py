"""
Default maintenance items.

Home Maintenance Center Pro
"""

from __future__ import annotations

from datetime import date, timedelta

from .models.maintenance_item import MaintenanceItem


def get_default_items() -> list[MaintenanceItem]:
    """Return default maintenance items."""

    today = date.today()

    def item(
        item_id: str,
        name: str,
        interval: int,
        category: str,
    ) -> MaintenanceItem:

        return MaintenanceItem(
            item_id=item_id,
            name=name,
            category=category,
            interval_days=interval,
            last_maintenance=today,
            next_maintenance=today + timedelta(days=interval),
        )

    return [

        item(
            "bombola_co2",
            "Bombola CO₂",
            365,
            "water",
        ),

        item(
            "filtri_depuratore",
            "Filtri depuratore",
            180,
            "water",
        ),

        item(
            "climatizzatore_camera",
            "Climatizzatore Camera",
            180,
            "climate",
        ),

        item(
            "climatizzatore_salone",
            "Climatizzatore Salone",
            180,
            "climate",
        ),

        item(
            "geberit_bagno",
            "Geberit Bagno",
            365,
            "bathroom",
        ),

        item(
            "geberit_bagno_camera",
            "Geberit Bagno Camera",
            365,
            "bathroom",
        ),
    ]
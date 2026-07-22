"""
Coordinator for Home Maintenance Center Pro.
"""

from __future__ import annotations

import logging
from datetime import date, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.util import slugify

from .const import DOMAIN, NEW_ITEM_CATEGORIES
from .managers.storage_manager import StorageManager
from .models.maintenance_item import MaintenanceItem

_LOGGER = logging.getLogger(__name__)


class HomeMaintenanceCoordinator(DataUpdateCoordinator[dict]):
    """Main coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize coordinator."""

        self.config_entry = config_entry
        self.storage = StorageManager(hass)

        # Stato in memoria del form "Aggiungi manutenzione" esposto
        # tramite le entità native text/select/number + il pulsante
        # "Crea manutenzione" (vedi text.py, select.py, number.py,
        # button.py). Non serve persistenza: si azzera ad ogni
        # riavvio, comportamento voluto per un form vuoto.
        self.new_item_draft: dict = {
            "name": "",
            "category": NEW_ITEM_CATEGORIES[-1],
            "interval_days": 180,
        }

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self) -> dict:
        """Load latest data."""

        try:
            await self.storage.async_load()

            items = self.storage.get_items()

            return {
                "items": items,
                "count": len(items),
            }

        except Exception as err:
            raise UpdateFailed(
                f"Unable to update maintenance data: {err}"
            ) from err

    # ---------------------------------------------------------------------
    # Base data
    # ---------------------------------------------------------------------

    @property
    def items(self) -> list[MaintenanceItem]:
        """Return all maintenance items."""

        return self.data.get("items", [])

    @property
    def enabled_items(self) -> list[MaintenanceItem]:
        """Return enabled maintenance items."""

        return [
            item
            for item in self.items
            if item.enabled
        ]

    @property
    def disabled_items(self) -> list[MaintenanceItem]:
        """Return disabled maintenance items."""

        return [
            item
            for item in self.items
            if not item.enabled
        ]

    @property
    def item_count(self) -> int:
        """Return total maintenance items."""

        return len(self.items)

    def get_item(
        self,
        item_id: str,
    ) -> MaintenanceItem | None:
        """Return a single maintenance item by id."""

        for item in self.items:
            if item.item_id == item_id:
                return item

        return None

    async def async_add_item_by_fields(
        self,
        name: str,
        category: str,
        interval_days: int,
    ) -> MaintenanceItem:
        """Build and add a new maintenance item from raw field values.

        Shared by the ``home_maintenance.add_item`` service and the
        native "Crea manutenzione" button, so both stay in sync.
        """

        base_id = slugify(name) or "manutenzione"
        item_id = base_id
        counter = 1

        while self.get_item(item_id) is not None:
            counter += 1
            item_id = f"{base_id}_{counter}"

        item = MaintenanceItem(
            item_id=item_id,
            name=name,
            category=category,
            interval_days=interval_days,
            last_maintenance=date.today(),
        )

        item.calculate_next_maintenance()

        await self.async_add_item(item)

        return item

    @property
    def enabled_count(self) -> int:
        """Return enabled maintenance items."""

        return len(self.enabled_items)

    @property
    def disabled_count(self) -> int:
        """Return disabled maintenance items."""

        return len(self.disabled_items)

    # ---------------------------------------------------------------------
    # Status
    # ---------------------------------------------------------------------

    @property
    def due_items(self) -> list[MaintenanceItem]:
        """Return items due within 30 days."""

        return [
            item
            for item in self.enabled_items
            if item.days_remaining is not None
            and 0 <= item.days_remaining <= 30
        ]

    @property
    def overdue_items(self) -> list[MaintenanceItem]:
        """Return overdue items."""

        return [
            item
            for item in self.enabled_items
            if item.overdue
        ]

    @property
    def ok_items(self) -> list[MaintenanceItem]:
        """Return items not requiring attention."""

        return [
            item
            for item in self.enabled_items
            if item.days_remaining is not None
            and item.days_remaining > 30
        ]

    @property
    def due_count(self) -> int:
        """Return due count."""

        return len(self.due_items)

    @property
    def overdue_count(self) -> int:
        """Return overdue count."""

        return len(self.overdue_items)

    @property
    def ok_count(self) -> int:
        """Return ok count."""

        return len(self.ok_items)

    @property
    def attention_required(self) -> bool:
        """Return True if any maintenance requires attention."""

        return (
            self.due_count > 0
            or self.overdue_count > 0
        )

    @property
    def next_due_item(self) -> MaintenanceItem | None:
        """Return next scheduled maintenance."""

        candidates = [
            item
            for item in self.enabled_items
            if item.next_maintenance is not None
        ]

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda item: item.next_maintenance,
        )

    @property
    def next_due_name(self) -> str | None:
        """Return next maintenance name."""

        item = self.next_due_item

        return None if item is None else item.name

    @property
    def next_due_days(self) -> int | None:
        """Return days until next maintenance."""

        item = self.next_due_item

        return None if item is None else item.days_remaining

    # ---------------------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------------------

    async def async_add_item(
        self,
        item: MaintenanceItem,
    ) -> None:
        """Add maintenance item."""

        await self.storage.add_item(item)

        await self.async_request_refresh()

    async def async_update_item(
        self,
        item: MaintenanceItem,
    ) -> None:
        """Update maintenance item."""

        await self.storage.update_item(item)

        await self.async_request_refresh()

    async def async_delete_item(
        self,
        item_id: str,
    ) -> None:
        """Delete maintenance item."""

        await self.storage.delete_item(item_id)

        await self.async_request_refresh()

    async def async_reload(self) -> None:
        """Reload coordinator."""

        await self.async_request_refresh()

"""
Button platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import HomeMaintenanceCoordinator
from .entity import HomeMaintenanceEntity, HomeMaintenanceSummaryEntity
from .models.maintenance_item import MaintenanceItem


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Home Maintenance buttons."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    async_add_entities(
        [
            MaintenanceDoneButton(
                coordinator,
                item,
            )
            for item in coordinator.items
        ]
        + [
            CreateItemButton(coordinator),
        ]
    )


class MaintenanceDoneButton(
    HomeMaintenanceEntity,
    ButtonEntity,
):
    """Button used to register a completed maintenance."""

    _attr_translation_key = "mark_done"
    _attr_icon = "mdi:check-circle-outline"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
        item: MaintenanceItem,
    ) -> None:
        """Initialize the button."""

        super().__init__(
            coordinator,
            item,
        )

        self._entity_suffix = "mark_done"

    async def async_press(self) -> None:
        """Mark maintenance as completed."""

        self.item.mark_completed()

        await self.coordinator.async_update_item(
            self.item
        )


class CreateItemButton(
    HomeMaintenanceSummaryEntity,
    ButtonEntity,
):
    """Button that creates a new item from the native add-item form."""

    _attr_translation_key = "create_item"
    _attr_icon = "mdi:plus-circle"

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:
        """Initialize the button."""

        super().__init__(coordinator)

        self._entity_suffix = "create_item"

    async def async_press(self) -> None:
        """Create the new maintenance item and reset the form."""

        draft = self.coordinator.new_item_draft

        name = (draft.get("name") or "").strip()

        if not name:
            # Niente da creare senza un nome: non facciamo nulla,
            # invece di generare un item senza titolo.
            return

        await self.coordinator.async_add_item_by_fields(
            name=name,
            category=draft.get("category", "Other"),
            interval_days=int(
                draft.get("interval_days", 180)
            ),
        )

        draft["name"] = ""
        draft["category"] = "Other"
        draft["interval_days"] = 180

        self.coordinator.async_update_listeners()

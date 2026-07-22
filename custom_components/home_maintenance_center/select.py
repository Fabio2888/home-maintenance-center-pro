"""
Select platform for Home Maintenance Center Pro.
"""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, NEW_ITEM_CATEGORIES
from .coordinator import HomeMaintenanceCoordinator
from .entity import HomeMaintenanceSummaryEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Home Maintenance select entities."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    entities: list[SelectEntity] = [
        NewItemCategorySelect(coordinator),
    ]

    async_add_entities(entities)


class NewItemCategorySelect(
    HomeMaintenanceSummaryEntity,
    SelectEntity,
):
    """Category field for the new-item creation form."""

    _attr_translation_key = "new_item_category"
    _attr_icon = "mdi:shape"
    _attr_options = list(NEW_ITEM_CATEGORIES)

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:
        """Initialize the entity."""

        super().__init__(coordinator)

        self._entity_suffix = "new_item_category"

    @property
    def current_option(self) -> str:
        """Return the currently selected category."""

        return self.coordinator.new_item_draft.get(
            "category",
            NEW_ITEM_CATEGORIES[-1],
        )

    async def async_select_option(self, option: str) -> None:
        """Store the selected category."""

        self.coordinator.new_item_draft["category"] = option

        self.coordinator.async_update_listeners()

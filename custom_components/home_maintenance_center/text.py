"""
Text platform for Home Maintenance Center Pro.

Hosts the "Nome" field of the native "Aggiungi manutenzione" form
(see also select.py for "Categoria", number.py for "Intervallo" and
button.py for the "Crea manutenzione" button). Together these four
entities let a new maintenance item be created straight from a
dashboard, with no input_text/input_select/input_number helper or
script needed.
"""

from __future__ import annotations

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import HomeMaintenanceCoordinator
from .entity import HomeMaintenanceSummaryEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Home Maintenance text entities."""

    coordinator: HomeMaintenanceCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]

    async_add_entities(
        [
            NewItemNameText(coordinator),
        ]
    )


class NewItemNameText(
    HomeMaintenanceSummaryEntity,
    TextEntity,
):
    """Name field for the new-item creation form."""

    _attr_translation_key = "new_item_name"
    _attr_icon = "mdi:pencil"
    _attr_native_max = 100

    def __init__(
        self,
        coordinator: HomeMaintenanceCoordinator,
    ) -> None:
        """Initialize the entity."""

        super().__init__(coordinator)

        self._entity_suffix = "new_item_name"

    @property
    def native_value(self) -> str:
        """Return the currently typed name."""

        return self.coordinator.new_item_draft.get(
            "name", ""
        )

    async def async_set_value(self, value: str) -> None:
        """Store the typed name."""

        self.coordinator.new_item_draft["name"] = value

        self.coordinator.async_update_listeners()

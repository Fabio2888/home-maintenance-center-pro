"""
Dynamic entity registration helper for Home Maintenance Center Pro.

Every per-item platform (sensor, binary_sensor, date, number, button)
needs the same behaviour: create entities for every item that exists
at startup, AND automatically create entities for any item added
later (e.g. via the native "Crea manutenzione" button, or the
``home_maintenance.add_item`` service) — without requiring a restart
of Home Assistant.

This module centralizes that logic so every platform stays in sync
with the coordinator's item list.
"""

from __future__ import annotations

from typing import Callable

from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .models.maintenance_item import MaintenanceItem


def async_setup_dynamic_item_entities(
    coordinator,
    async_add_entities: AddEntitiesCallback,
    entity_factory: Callable[[MaintenanceItem], list[Entity]],
) -> None:
    """Add entities for current items, and keep adding them for new ones.

    ``entity_factory`` takes a single :class:`MaintenanceItem` and
    returns the list of entities that represent it on this platform
    (usually one, but e.g. binary_sensor has two per item).
    """

    known_item_ids: set[str] = set()

    def _add_missing() -> None:
        new_entities: list[Entity] = []

        for item in coordinator.items:
            if item.item_id in known_item_ids:
                continue

            known_item_ids.add(item.item_id)
            new_entities.extend(entity_factory(item))

        if new_entities:
            async_add_entities(new_entities)

    # Elementi già presenti all'avvio.
    _add_missing()

    @callback
    def _handle_coordinator_update() -> None:
        _add_missing()

    # Richiamato ad ogni refresh del coordinator (che include il
    # momento subito dopo la creazione di un nuovo elemento, grazie
    # al request_refresh già presente in async_add_item).
    coordinator.async_add_listener(_handle_coordinator_update)

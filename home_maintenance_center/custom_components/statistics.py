"""
Statistics engine for Home Maintenance Center Pro.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date

from .history import HistoryManager
from .models.maintenance_item import MaintenanceItem


@dataclass(slots=True)
class MaintenanceStatistics:
    """Aggregated maintenance statistics."""

    total_items: int = 0
    enabled_items: int = 0
    disabled_items: int = 0

    upcoming_items: int = 0
    due_today: int = 0
    overdue_items: int = 0

    completed_operations: int = 0

    total_cost: float = 0.0
    average_cost: float = 0.0

    categories: dict[str, int] | None = None


class StatisticsManager:
    """Calculate maintenance statistics."""

    def __init__(
        self,
        history: HistoryManager,
    ) -> None:
        self._history = history

    def calculate(
        self,
        items: list[MaintenanceItem],
    ) -> MaintenanceStatistics:
        """Calculate statistics."""

        today = date.today()

        stats = MaintenanceStatistics()

        stats.total_items = len(items)

        stats.enabled_items = sum(
            item.enabled
            for item in items
        )

        stats.disabled_items = (
            stats.total_items
            - stats.enabled_items
        )

        categories = Counter()

        for item in items:

            categories[item.category] += 1

            if not item.enabled:
                continue

            if item.next_maintenance is None:
                continue

            days = (
                item.next_maintenance - today
            ).days

            if days > 0:
                stats.upcoming_items += 1

            elif days == 0:
                stats.due_today += 1

            else:
                stats.overdue_items += 1

        stats.categories = dict(categories)

        stats.completed_operations = (
            self._history.total_entries
        )

        stats.total_cost = (
            self._history.total_cost
        )

        if stats.completed_operations:
            stats.average_cost = round(
                stats.total_cost
                / stats.completed_operations,
                2,
            )

        return stats

    def upcoming_items(
        self,
        items: list[MaintenanceItem],
        days: int,
    ) -> list[MaintenanceItem]:
        """Return items due within X days."""

        today = date.today()

        result = []

        for item in items:

            if not item.enabled:
                continue

            if item.next_maintenance is None:
                continue

            remaining = (
                item.next_maintenance - today
            ).days

            if 0 <= remaining <= days:
                result.append(item)

        result.sort(
            key=lambda item: item.next_maintenance
        )

        return result

    def overdue_items(
        self,
        items: list[MaintenanceItem],
    ) -> list[MaintenanceItem]:
        """Return overdue items."""

        today = date.today()

        result = [
            item
            for item in items
            if (
                item.enabled
                and item.next_maintenance
                and item.next_maintenance < today
            )
        ]

        result.sort(
            key=lambda item: item.next_maintenance
        )

        return result

    def category_costs(self) -> dict[str, float]:
        """Return costs grouped by category."""

        costs: dict[str, float] = {}

        for history in self._history._history.values():

            for entry in history:

                if entry.cost is None:
                    continue

                category = "Unknown"

                costs[category] = (
                    costs.get(category, 0.0)
                    + entry.cost
                )

        return {
            key: round(value, 2)
            for key, value in costs.items()
        }
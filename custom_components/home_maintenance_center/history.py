"""
Maintenance history manager for Home Maintenance Center Pro.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class MaintenanceHistoryEntry:
    """Represents one maintenance execution."""

    item_id: str
    timestamp: datetime
    performed_by: str | None = None
    notes: str | None = None
    cost: float | None = None
    duration_minutes: int | None = None
    attachments: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""

        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "MaintenanceHistoryEntry":
        """Create from dictionary."""

        return cls(
            item_id=data["item_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            performed_by=data.get("performed_by"),
            notes=data.get("notes"),
            cost=data.get("cost"),
            duration_minutes=data.get("duration_minutes"),
            attachments=list(data.get("attachments", [])),
        )


class HistoryManager:
    """Manage maintenance history."""

    def __init__(self) -> None:
        self._history: dict[
            str,
            list[MaintenanceHistoryEntry],
        ] = {}

    def add_entry(
        self,
        item_id: str,
        *,
        performed_by: str | None = None,
        notes: str | None = None,
        cost: float | None = None,
        duration_minutes: int | None = None,
        attachments: list[str] | None = None,
    ) -> MaintenanceHistoryEntry:
        """Add a history entry."""

        entry = MaintenanceHistoryEntry(
            item_id=item_id,
            timestamp=datetime.now(UTC),
            performed_by=performed_by,
            notes=notes,
            cost=cost,
            duration_minutes=duration_minutes,
            attachments=attachments or [],
        )

        self._history.setdefault(item_id, []).append(entry)

        return entry

    def get_history(
        self,
        item_id: str,
    ) -> list[MaintenanceHistoryEntry]:
        """Return history for an item."""

        return list(
            self._history.get(item_id, [])
        )

    def get_last_entry(
        self,
        item_id: str,
    ) -> MaintenanceHistoryEntry | None:
        """Return latest history entry."""

        history = self._history.get(item_id)

        if not history:
            return None

        return history[-1]

    def delete_history(
        self,
        item_id: str,
    ) -> None:
        """Delete history for an item."""

        self._history.pop(item_id, None)

    def clear(self) -> None:
        """Delete every history entry."""

        self._history.clear()

    def export(self) -> dict[str, list[dict[str, Any]]]:
        """Export history."""

        return {
            item_id: [
                entry.to_dict()
                for entry in entries
            ]
            for item_id, entries in self._history.items()
        }

    def import_history(
        self,
        data: dict[str, list[dict[str, Any]]],
    ) -> None:
        """Import history."""

        self._history = {
            item_id: [
                MaintenanceHistoryEntry.from_dict(entry)
                for entry in entries
            ]
            for item_id, entries in data.items()
        }

    @property
    def total_entries(self) -> int:
        """Return total history records."""

        return sum(
            len(entries)
            for entries in self._history.values()
        )

    @property
    def total_cost(self) -> float:
        """Return total maintenance cost."""

        total = 0.0

        for entries in self._history.values():
            for entry in entries:
                if entry.cost is not None:
                    total += entry.cost

        return round(total, 2)
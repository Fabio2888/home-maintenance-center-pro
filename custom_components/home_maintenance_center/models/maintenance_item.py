"""
Data model for a maintenance item.

Home Maintenance Center Pro
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass(slots=True)
class MaintenanceItem:
    """Represent a maintenance item."""

    item_id: str
    name: str

    category: str = "general"
    priority: str = "normal"

    interval_days: int = 180

    last_maintenance: date | None = None
    next_maintenance: date | None = None

    enabled: bool = True

    notes: str = ""

    manual_url: str = ""

    image: str = ""

    purchase_url: str = ""

    model: str = ""

    serial_number: str = ""

    location: str = ""

    estimated_cost: float = 0.0

    notify: bool = True

    tags: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert object to dictionary."""

        return {
            "item_id": self.item_id,
            "name": self.name,
            "category": self.category,
            "priority": self.priority,
            "interval_days": self.interval_days,
            "last_maintenance": (
                self.last_maintenance.isoformat()
                if self.last_maintenance
                else None
            ),
            "next_maintenance": (
                self.next_maintenance.isoformat()
                if self.next_maintenance
                else None
            ),
            "enabled": self.enabled,
            "notes": self.notes,
            "manual_url": self.manual_url,
            "image": self.image,
            "purchase_url": self.purchase_url,
            "model": self.model,
            "serial_number": self.serial_number,
            "location": self.location,
            "estimated_cost": self.estimated_cost,
            "notify": self.notify,
            "tags": self.tags,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MaintenanceItem":
        """Create object from dictionary."""

        last = (
            date.fromisoformat(data["last_maintenance"])
            if data.get("last_maintenance")
            else None
        )

        next_due = (
            date.fromisoformat(data["next_maintenance"])
            if data.get("next_maintenance")
            else None
        )

        return cls(
            item_id=data["item_id"],
            name=data["name"],
            category=data.get("category", "general"),
            priority=data.get("priority", "normal"),
            interval_days=data.get("interval_days", 180),
            last_maintenance=last,
            next_maintenance=next_due,
            enabled=data.get("enabled", True),
            notes=data.get("notes", ""),
            manual_url=data.get("manual_url", ""),
            image=data.get("image", ""),
            purchase_url=data.get("purchase_url", ""),
            model=data.get("model", ""),
            serial_number=data.get("serial_number", ""),
            location=data.get("location", ""),
            estimated_cost=data.get("estimated_cost", 0.0),
            notify=data.get("notify", True),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
        )
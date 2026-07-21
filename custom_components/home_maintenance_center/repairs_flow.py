"""
Repair flows for Home Maintenance Center Pro.
"""

from __future__ import annotations

from homeassistant.components.repairs import RepairsFlow
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class HomeMaintenanceRepairFlow(RepairsFlow):
    """Repair flow."""

    def __init__(self, issue_id: str) -> None:
        """Initialize repair flow."""
        self.issue_id = issue_id

    async def async_step_init(
        self,
        user_input=None,
    ) -> FlowResult:
        """Show repair information."""

        return self.async_show_menu(
            step_id="init",
            menu_options=["confirm"],
        )

    async def async_step_confirm(
        self,
        user_input=None,
    ) -> FlowResult:
        """Display repair instructions."""

        return self.async_create_entry(
            title=self._issue_title(),
            data={},
        )

    def _issue_title(self) -> str:
        """Return a readable issue title."""

        mapping = {
            "duplicate_item_ids":
                "Duplicate maintenance IDs",

            "invalid_interval":
                "Invalid maintenance interval",

            "missing_next_date":
                "Missing next maintenance date",
        }

        return mapping.get(
            self.issue_id,
            "Maintenance issue",
        )


async def async_create_fix_flow(
    hass,
    issue_id: str,
):
    """Create repair flow."""

    return HomeMaintenanceRepairFlow(issue_id)
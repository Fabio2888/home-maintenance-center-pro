"""
Options Flow for Home Maintenance Center Pro.
"""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlowResult, OptionsFlow

CONF_NOTIFICATION_DAYS = "notification_days"
CONF_NOTIFICATION_HOUR = "notification_hour"
CONF_REPEAT_NOTIFICATIONS = "repeat_notifications"


class HomeMaintenanceOptionsFlow(OptionsFlow):
    """Handle Home Maintenance options."""

    async def async_step_init(
        self,
        user_input: dict | None = None,
    ) -> ConfigFlowResult:
        """Manage the options."""

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_NOTIFICATION_DAYS,
                    default=self.config_entry.options.get(
                        CONF_NOTIFICATION_DAYS,
                        "30,15,7,3,1",
                    ),
                ): str,
                vol.Optional(
                    CONF_NOTIFICATION_HOUR,
                    default=self.config_entry.options.get(
                        CONF_NOTIFICATION_HOUR,
                        9,
                    ),
                ): vol.All(
                    int,
                    vol.Range(min=0, max=23),
                ),
                vol.Optional(
                    CONF_REPEAT_NOTIFICATIONS,
                    default=self.config_entry.options.get(
                        CONF_REPEAT_NOTIFICATIONS,
                        True,
                    ),
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )

"""
Options Flow for Home Maintenance Center Pro.
"""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlowResult, OptionsFlow
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

CONF_NOTIFICATION_DAYS = "notification_days"
CONF_NOTIFICATION_HOUR = "notification_hour"
CONF_REPEAT_NOTIFICATIONS = "repeat_notifications"
CONF_NOTIFY_SERVICE_1 = "notify_service_1"
CONF_NOTIFY_SERVICE_2 = "notify_service_2"
CONF_NOTIFY_SERVICE_3 = "notify_service_3"
CONF_LOCAL_CALENDAR_ENTITY = "local_calendar_entity"


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

        notify_services = sorted(
            service
            for service in self.hass.services.async_services().get(
                "notify", {}
            )
            if service not in ("notify", "send_message")
        )

        notify_selector = SelectSelector(
            SelectSelectorConfig(
                options=notify_services,
                mode=SelectSelectorMode.DROPDOWN,
                custom_value=True,
            )
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
                vol.Optional(
                    CONF_NOTIFY_SERVICE_1,
                    default=self.config_entry.options.get(
                        CONF_NOTIFY_SERVICE_1,
                        "",
                    ),
                ): notify_selector,
                vol.Optional(
                    CONF_NOTIFY_SERVICE_2,
                    default=self.config_entry.options.get(
                        CONF_NOTIFY_SERVICE_2,
                        "",
                    ),
                ): notify_selector,
                vol.Optional(
                    CONF_NOTIFY_SERVICE_3,
                    default=self.config_entry.options.get(
                        CONF_NOTIFY_SERVICE_3,
                        "",
                    ),
                ): notify_selector,
                vol.Optional(
                    CONF_LOCAL_CALENDAR_ENTITY,
                    default=self.config_entry.options.get(
                        CONF_LOCAL_CALENDAR_ENTITY,
                        "",
                    ),
                ): EntitySelector(
                    EntitySelectorConfig(domain="calendar")
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )

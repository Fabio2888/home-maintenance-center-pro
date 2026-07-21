"""
Config flow for Home Maintenance Center Pro.
"""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.const import CONF_NAME

from .const import DOMAIN


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(
            CONF_NAME,
            default="Home Maintenance Center",
        ): str,
    }
)


class HomeMaintenanceConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        if self._async_current_entries():
            return self.async_abort(
                reason="single_instance_allowed"
            )

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
        )

    async def async_step_import(
        self,
        user_input: dict,
    ) -> ConfigFlowResult:
        """Handle YAML import."""

        return self.async_abort(
            reason="yaml_not_supported"
        )

    @staticmethod
    def async_get_options_flow(
        config_entry,
    ):
        """Return the options flow."""

        from .options_flow import (
            HomeMaintenanceOptionsFlow,
        )

        return HomeMaintenanceOptionsFlow()

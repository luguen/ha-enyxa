"""UI setup for ENYXA."""
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .api import EnyxaClient, EnyxaAuthError, EnyxaError
from .const import DOMAIN, CONF_URL, CONF_TOKEN, DEFAULT_URL, CONF_SCAN_INTERVAL, SCAN_OPTIONS_MINUTES

class EnyxaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            url = user_input[CONF_URL].strip().rstrip("/")
            token = user_input[CONF_TOKEN].strip()
            if not url.startswith("https://"):
                errors["base"] = "https_required"
            else:
                try:
                    client = EnyxaClient(async_get_clientsession(self.hass), url, token)
                    await client.devices()
                except EnyxaAuthError:
                    errors["base"] = "invalid_auth"
                except EnyxaError:
                    errors["base"] = "cannot_connect"
                else:
                    await self.async_set_unique_id(url.lower())
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(title="ENYXA", data={CONF_URL:url, CONF_TOKEN:token})
        schema = vol.Schema({
            vol.Required(CONF_URL, default=DEFAULT_URL): str,
            vol.Required(CONF_TOKEN): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    def async_get_options_flow(config_entry):
        return EnyxaOptionsFlow()

class EnyxaOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        current = self.config_entry.options.get(CONF_SCAN_INTERVAL, 5)
        schema = vol.Schema({vol.Required(CONF_SCAN_INTERVAL, default=current): vol.In(SCAN_OPTIONS_MINUTES)})
        return self.async_show_form(step_id="init", data_schema=schema)

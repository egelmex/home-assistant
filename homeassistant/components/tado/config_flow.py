"""Config flow for Tado component."""
import logging
import urllib

from PyTado.interface import Tado
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback

from .const import CONF_FALLBACK, DOMAIN

_LOGGER = logging.getLogger(__name__)


@callback
def configured_instances(hass):
    """Return a set of configured Tado instances."""
    return set(
        entry.data[CONF_USERNAME] for entry in hass.config_entries.async_entries(DOMAIN)
    )


class TadoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for tado component."""

    async def async_step_user(self, info):
        """Handle a flow initialized by the user."""
        errors = {}
        if info is not None:
            identifier = info[CONF_USERNAME]
            if identifier in configured_instances(self.hass):
                return await self.async_abort({"base": "identifier_exists"})

            try:
                Tado(info[CONF_USERNAME], info[CONF_PASSWORD])
                return self.async_create_entry(title=identifier, data=info)
            except (RuntimeError, urllib.error.HTTPError) as exc:
                _LOGGER.error("Unable to connect: %s", exc)
                errors["base"] = "auth_error"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_FALLBACK, default=False): bool,
                }
            ),
            errors=errors,
        )

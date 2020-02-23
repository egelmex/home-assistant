"""Config flow for Tado component."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback

from .const import DOMAIN


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
        if info is not None:
            identifier = info[CONF_USERNAME]
            if identifier in configured_instances(self.hass):
                return await self._show_form({"base": "identifier_exists"})

            return self.async_create_entry(title=identifier, data=info)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required("fallback"): bool,
                }
            ),
        )
        pass

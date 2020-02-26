"""Test the Tado config flow."""
from asynctest import patch

from homeassistant import config_entries, setup
from homeassistant.components.tado.const import DOMAIN


async def test_form(hass):
    """Test the form."""

    await setup.async_setup_component(hass, "persistent_notification", {})
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == "form"
    assert result["errors"] == {}

    with patch(
        "homeassistant.components.tado.TadoConnector.connect", return_value=True,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {"username": "test-email", "password": "test-password"},
        )

    assert result2["type"] == "form"

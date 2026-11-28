"""Tests for the diagnostics data provided by LG webOS TV."""

import pytest
from pytest_homeassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_homeassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from homeassistant.components.webostv.const import CONF_SOURCES, CONF_WAKE_ON_LAN
from homeassistant.const import CONF_BROADCAST_ADDRESS, CONF_MAC
from homeassistant.core import HomeAssistant

from . import setup_webostv


@pytest.mark.usefixtures("client")
async def test_diagnostics(
    hass: HomeAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    entry = await setup_webostv(
        hass,
        options={
            CONF_SOURCES: ["Input01"],
            CONF_WAKE_ON_LAN: {
                CONF_MAC: "aa:bb:cc:dd:ee:ff",
                CONF_BROADCAST_ADDRESS: "192.168.10.255",
            },
        },
    )
    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot(
        exclude=props("created_at", "modified_at", "entry_id")
    )

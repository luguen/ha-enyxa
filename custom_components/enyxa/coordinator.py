"""Poll ENYXA every five minutes."""
from __future__ import annotations
import asyncio
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import EnyxaAuthError, EnyxaError
from .const import SCAN_INTERVAL_SECONDS

class EnyxaCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client, interval_minutes=5):
        super().__init__(hass, logger=__import__("logging").getLogger(__name__), name="ENYXA", update_interval=timedelta(minutes=interval_minutes))
        self.client = client

    async def _async_update_data(self):
        try:
            devices = await self.client.devices()
            valid = [d for d in devices if isinstance(d, dict) and d.get("id") and d.get("paired")]
            responses = await asyncio.gather(*(self.client.latest(str(d["id"])) for d in valid), return_exceptions=True)
            result = {}
            for device, response in zip(valid, responses):
                did = str(device["id"])
                if isinstance(response, Exception):
                    # Keep previously fetched measurements but mark this device unavailable.
                    previous = (self.data or {}).get(did, {})
                    result[did] = {"device":device, "measurement":previous.get("measurement"), "ok":False}
                else:
                    result[did] = {"device":device, "measurement":response.get("measurement"), "ok":True}
            return result
        except (EnyxaAuthError, EnyxaError) as exc:
            raise UpdateFailed(str(exc)) from exc

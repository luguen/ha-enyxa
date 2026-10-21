"""Minimal async ENYXA REST client."""
from __future__ import annotations
from urllib.parse import quote
import aiohttp

class EnyxaError(Exception):
    """Communication or response error."""

class EnyxaAuthError(EnyxaError):
    """Invalid token or insufficient permissions."""

class EnyxaClient:
    def __init__(self, session: aiohttp.ClientSession, url: str, token: str):
        self.session = session
        self.url = url.rstrip("/")
        self.token = token

    async def get(self, path: str):
        try:
            async with self.session.get(
                self.url + "/v1/" + path,
                headers={"Authorization": "Bearer " + self.token},
                timeout=aiohttp.ClientTimeout(total=20),
            ) as response:
                if response.status in (401, 403):
                    raise EnyxaAuthError("ENYXA token rejected or lacks scopes")
                if response.status != 200:
                    raise EnyxaError(f"ENYXA HTTP {response.status}")
                try:
                    return await response.json(content_type=None)
                except (ValueError, aiohttp.ContentTypeError) as exc:
                    raise EnyxaError("Invalid ENYXA JSON response") from exc
        except (aiohttp.ClientError, TimeoutError) as exc:
            raise EnyxaError("Unable to contact ENYXA") from exc

    async def devices(self):
        result = await self.get("devices")
        if not isinstance(result, list):
            raise EnyxaError("Unexpected devices response")
        return result

    async def latest(self, device_id: str):
        result = await self.get("devices/" + quote(device_id, safe="") + "/latest")
        if not isinstance(result, dict):
            raise EnyxaError("Unexpected latest response")
        return result

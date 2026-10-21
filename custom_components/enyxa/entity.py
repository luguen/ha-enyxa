"""Common ENYXA device entity."""
from __future__ import annotations
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

class EnyxaEntity(CoordinatorEntity):
    _attr_has_entity_name = True
    def __init__(self, coordinator, device_id, key):
        super().__init__(coordinator)
        self.device_id = device_id
        self._attr_unique_id = f"{device_id}_{key}"

    @property
    def device_info(self):
        device = self.coordinator.data.get(self.device_id, {}).get("device", {})
        return DeviceInfo(identifiers={(DOMAIN,self.device_id)}, name=device.get("name", "ENYXA device"), manufacturer="ENYXA", model="Windows / Android agent")

    @property
    def available(self):
        row = self.coordinator.data.get(self.device_id)
        return bool(super().available and row and row.get("ok"))

    @property
    def measurement(self):
        return self.coordinator.data.get(self.device_id, {}).get("measurement") or {}

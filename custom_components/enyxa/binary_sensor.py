"""Charging and connectivity binary sensors."""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.entity import EntityCategory
from .const import DOMAIN
from .entity import EnyxaEntity

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator=hass.data[DOMAIN][entry.entry_id]
    known=set()
    def add_new():
        entities=[]
        for did,row in coordinator.data.items():
            uid=(did,"online")
            if uid not in known:
                known.add(uid); entities.append(EnyxaOnline(coordinator,did))
            for i,battery in enumerate((row.get("measurement") or {}).get("batteries") or []):
                key=str(battery.get("id") or f"battery_{i}")
                uid=(did,"charging",key)
                if uid not in known:
                    known.add(uid); entities.append(EnyxaCharging(coordinator,did,key,i))
        if entities: async_add_entities(entities)
    add_new()
    entry.async_on_unload(coordinator.async_add_listener(add_new))

class EnyxaOnline(EnyxaEntity, BinarySensorEntity):
    _attr_name="Online"
    _attr_device_class=BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category=EntityCategory.DIAGNOSTIC
    def __init__(self, coordinator, did): super().__init__(coordinator,did,"online")
    @property
    def is_on(self):
        raw=self.coordinator.data.get(self.device_id,{}).get("device",{}).get("last_seen")
        if not raw: return False
        try:
            dt=datetime.fromisoformat(raw.replace("Z","+00:00"))
            if dt.tzinfo is None: return False
            return datetime.now(timezone.utc)-dt < timedelta(minutes=65)
        except (ValueError,TypeError): return False

class EnyxaCharging(EnyxaEntity, BinarySensorEntity):
    _attr_device_class=BinarySensorDeviceClass.BATTERY_CHARGING
    def __init__(self, coordinator, did, key, index):
        super().__init__(coordinator,did,f"battery_{key}_charging")
        self.key=key;self.index=index;self._attr_name=f"{key} charging"
    @property
    def is_on(self):
        batteries=self.measurement.get("batteries") or []
        item=next((b for b in batteries if str(b.get("id") or "")==self.key),batteries[self.index] if self.index<len(batteries) else {})
        return item.get("charging") if isinstance(item.get("charging"),bool) else None

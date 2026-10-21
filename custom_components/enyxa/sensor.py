"""Battery, storage and last-seen sensors."""
from __future__ import annotations
from datetime import datetime
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import PERCENTAGE, UnitOfInformation
from homeassistant.helpers.entity import EntityCategory
from .const import DOMAIN
from .entity import EnyxaEntity

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    known = set()
    def add_new():
        entities = []
        for did, row in coordinator.data.items():
            measurement = row.get("measurement") or {}
            for i, battery in enumerate(measurement.get("batteries") or []):
                key = str(battery.get("id") or f"battery_{i}")
                for metric in ("level",):
                    uid = (did,"battery",key,metric)
                    if uid not in known:
                        known.add(uid); entities.append(EnyxaBattery(coordinator,did,key,i))
            for i, disk in enumerate(measurement.get("storage") or []):
                key = str(disk.get("name") or f"storage_{i}")
                for metric in ("used_percent","free_gb"):
                    uid = (did,"storage",key,metric)
                    if uid not in known:
                        known.add(uid); entities.append(EnyxaStorage(coordinator,did,key,i,metric))
            uid = (did,"last_seen")
            if uid not in known:
                known.add(uid); entities.append(EnyxaLastSeen(coordinator,did))
        if entities: async_add_entities(entities)
    add_new()
    entry.async_on_unload(coordinator.async_add_listener(add_new))

def find_item(items, key, index, field):
    for item in items:
        if str(item.get(field) or "") == key: return item
    return items[index] if index < len(items) else {}

class EnyxaBattery(EnyxaEntity, SensorEntity):
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    def __init__(self, coordinator, did, key, index):
        super().__init__(coordinator,did,f"battery_{key}_level")
        self.key=key; self.index=index
        self._attr_name=f"{key} battery"
    @property
    def native_value(self):
        item=find_item(self.measurement.get("batteries") or [],self.key,self.index,"id")
        v=item.get("level")
        return v if isinstance(v,(int,float)) and not isinstance(v,bool) and 0 <= v <= 100 else None

class EnyxaStorage(EnyxaEntity, SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    def __init__(self, coordinator, did, key, index, metric):
        super().__init__(coordinator,did,f"storage_{key}_{metric}")
        self.key=key;self.index=index;self.metric=metric
        self._attr_name=f"{key} {'used' if metric == 'used_percent' else 'free'}"
        self._attr_native_unit_of_measurement=PERCENTAGE if metric=="used_percent" else UnitOfInformation.GIGABYTES
    @property
    def native_value(self):
        item=find_item(self.measurement.get("storage") or [],self.key,self.index,"name")
        total=item.get("total_bytes"); used=item.get("used_bytes"); free=item.get("free_bytes")
        if self.metric=="used_percent":
            if isinstance(total,(int,float)) and total>0 and isinstance(used,(int,float)):
                return round(100*used/total,1)
            return None
        if isinstance(free,(int,float)) and free>=0: return round(free/1e9,2)
        if isinstance(total,(int,float)) and isinstance(used,(int,float)) and total>=used>=0:
            return round((total-used)/1e9,2)
        return None

class EnyxaLastSeen(EnyxaEntity, SensorEntity):
    _attr_name = "Last synchronization"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    def __init__(self, coordinator, did): super().__init__(coordinator,did,"last_seen")
    @property
    def native_value(self):
        raw=self.coordinator.data.get(self.device_id,{}).get("device",{}).get("last_seen")
        if not raw: return None
        try:
            value=datetime.fromisoformat(raw.replace("Z","+00:00"))
            return value if value.tzinfo else None
        except (ValueError,TypeError): return None

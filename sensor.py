"""Platform Sensor Integration."""

from homeassistant.components.sensor import SensorEntity
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
  """Add Sensor."""
  hub = hass.data[DOMAIN][config_entry.entry_id]

  device = QCAvailabilitySensor(hub.QC)

  async_add_entities([device])


class QCAvailabilitySensor(SensorEntity):
  """QC Availavility check."""

  _attr_has_entity_name = True
  _attr_name = None

  def __init__(self, qc):
    """Init."""
    self._qc = qc
    self._attr_unique_id = f"{self._qc.id}_availability_sensor"
    # self._attr_name = f"{self._qc.name} Sensor"
    self._native_value = self._qc.status

  @property
  def native_value(self):
    """Navtive Value."""
    return self._qc.status

  @property
  def device_info(self):
    """Device Info."""
    return {
      "identifiers": {(DOMAIN, self._qc.id)},
      "name": f"{self._qc.id} {self._qc.name} Availability Sensor"
    }

  async def async_added_to_hass(self):
    """Add to callback."""
    await self._qc.register_callback(self.async_write_ha_state)

  async def async_will_remove_from_hass(self):
    """Remove from callback."""
    await self._qc.remove_callback(self.async_write_ha_state)
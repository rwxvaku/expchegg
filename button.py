"""Platform Button Integration."""

from homeassistant.components.button import ButtonEntity
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
  """Add Button."""
  hub = hass.data[DOMAIN][config_entry.entry_id]

  qc_device = QCAvailabilityCheck(hub.QC)
  qa_device = QCAvailabilityCheck(hub.QA)

  async_add_entities([qc_device, qa_device])


class QCAvailabilityCheck(ButtonEntity):
  """QC Availavility check."""

  _attr_has_entity_name = True
  _attr_name = None

  def __init__(self, q):
    """Init."""
    self._q = q
    self._attr_unique_id = f"{self._q.id}_availability_button"
    # self._attr_name = f"{self._qc.name} Button"

  @property
  def device_info(self):
    """Device Info."""
    return {
      "identifiers": {(DOMAIN, self._q.id)},
      "name": f"{self._q.id} {self._q.name} Availability Button"
    }
    
  async def async_press(self) -> None:
    """Handle Push."""
    await self._q.check()
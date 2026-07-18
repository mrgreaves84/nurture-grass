import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import slugify

from .const import DOMAIN, CONF_SITE_NAME
from .utils import clean_site_name

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            NurtureRefreshButton(
                coordinator,
                entry,
            )
        ]
    )


class NurtureRefreshButton(ButtonEntity):

    _attr_icon = "mdi:refresh"
    def __init__(
        self,
        coordinator,
        entry,
    ):
        self.coordinator = coordinator

        site_name = clean_site_name(
            entry.data.get(
                CONF_SITE_NAME,
                "Nurture Site",
            )
        )

        self._attr_name = (
            f"{site_name} Refresh Schedule"
        )

        self._attr_unique_id = (
            f"{slugify(site_name)}_refresh_schedule"
        )

    async def async_press(self) -> None:
        await self.coordinator.async_request_refresh()
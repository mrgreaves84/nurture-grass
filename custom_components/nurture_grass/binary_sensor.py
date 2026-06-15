from datetime import datetime

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import (
    CONF_NOTIFY_DAYS,
    CONF_SITE_NAME,
    DEFAULT_NOTIFY_DAYS,
    DOMAIN,
)
from .utils import clean_site_name


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    site_name = clean_site_name(
        entry.data.get(
            CONF_SITE_NAME,
            "Nurture Site",
        )
    )

    entities = []

    for activity_name in coordinator.data:
        entities.append(
            ActivityDueSoonBinarySensor(
                coordinator,
                activity_name,
                site_name,
            )
        )

    async_add_entities(entities)


class ActivityDueSoonBinarySensor(
    CoordinatorEntity,
    BinarySensorEntity,
):

    def __init__(
        self,
        coordinator,
        activity_name,
        site_name,
    ):
        super().__init__(coordinator)

        self.activity_name = activity_name
        self.site_name = site_name
        self.activity_slug = slugify(activity_name)
        self.site_slug = slugify(site_name)

    @property
    def name(self):
        return (
            f"{self.site_name} "
            f"{self.activity_name} "
            f"Due Soon"
        )

    @property
    def unique_id(self):
        return (
            f"{self.site_slug}_"
            f"{self.activity_slug}_"
            f"due_soon"
        )

    @property
    def icon(self):
        if self.is_on:
            return "mdi:alert-circle"
        return "mdi:check-circle"

    @property
    def is_on(self):
        activity = self.coordinator.data.get(
            self.activity_name,
            {},
        )

        date_text = activity.get(
            "next_visit",
            "",
        )

        try:
            date_text = (
                date_text
                .replace("Week commencing:", "")
                .strip()
            )

            next_date = datetime.strptime(
                date_text,
                "%d/%m/%Y",
            ).date()

            days = (
                next_date
                - datetime.now().date()
            ).days

            notify_days = (
                self.coordinator.config_entry.options.get(
                    CONF_NOTIFY_DAYS,
                    DEFAULT_NOTIFY_DAYS,
                )
            )

            return days <= notify_days

        except Exception:
            return False

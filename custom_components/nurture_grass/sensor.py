from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import DOMAIN, CONF_SITE_NAME
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
        entities.extend(
            [
                ActivityNextVisitSensor(coordinator, activity_name, site_name),
                ActivityLastVisitSensor(coordinator, activity_name, site_name),
                ActivityDaysUntilSensor(coordinator, activity_name, site_name),
            ]
        )

    entities.extend(
        [
            LastRefreshSensor(coordinator, site_name),
            NextActivitySensor(coordinator, site_name),
            NextActivityDateSensor(coordinator, site_name),
            DaysUntilNextActivitySensor(coordinator, site_name),
            LastActivitySensor(coordinator, site_name),
            LastActivityDateSensor(coordinator, site_name),
            DaysSinceLastActivitySensor(coordinator, site_name),
        ]
    )

    async_add_entities(entities)


class ActivityBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, activity_name, site_name):
        super().__init__(coordinator)
        self.activity_name = activity_name
        self.site_name = site_name
        self.activity_slug = slugify(activity_name)
        self.site_slug = slugify(site_name)

    @property
    def activity(self):
        return self.coordinator.data.get(self.activity_name, {})


class ActivityNextVisitSensor(ActivityBaseSensor):
    _attr_icon = "mdi:calendar-arrow-right"
    @property
    def name(self):
        return f"{self.site_name} {self.activity_name} Next Visit"

    @property
    def unique_id(self):
        return f"{self.site_slug}_{self.activity_slug}_next_visit"

    @property
    def native_value(self):
        return self.activity.get("next_visit", "Unknown")


class ActivityLastVisitSensor(ActivityBaseSensor):
    _attr_icon = "mdi:calendar-check"
    @property
    def name(self):
        return f"{self.site_name} {self.activity_name} Last Visit"

    @property
    def unique_id(self):
        return f"{self.site_slug}_{self.activity_slug}_last_visit"

    @property
    def native_value(self):
        return self.activity.get("last_visit", "Unknown")


class ActivityDaysUntilSensor(ActivityBaseSensor):
    _attr_icon = "mdi:timer-sand"
    _attr_native_unit_of_measurement = "days"
    _attr_state_class = SensorStateClass.MEASUREMENT
    @property
    def name(self):
        return f"{self.site_name} {self.activity_name} Days Until Visit"

    @property
    def unique_id(self):
        return f"{self.site_slug}_{self.activity_slug}_days_until_visit"

    @property
    def native_value(self):
        date_text = self.activity.get("next_visit", "")

        try:
            date_text = date_text.replace("Week commencing:", "").strip()
            next_date = datetime.strptime(date_text, "%d/%m/%Y").date()
            return (next_date - datetime.now().date()).days

        except Exception:
            return None


class LastRefreshSensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:refresh-circle"
    def __init__(self, coordinator, site_name):
        super().__init__(coordinator)
        self.site_name = site_name

    @property
    def name(self):
        return f"{self.site_name} Last Refresh"

    @property
    def unique_id(self):
        return f"{slugify(self.site_name)}_last_refresh"

    @property
    def native_value(self):
        if self.coordinator.last_refresh is None:
            return None

        return self.coordinator.last_refresh.strftime("%d/%m/%Y %H:%M:%S")


class NextActivitySensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:calendar-arrow-right"
    def __init__(self, coordinator, site_name):
        super().__init__(coordinator)
        self.site_name = site_name

    @property
    def name(self):
        return f"{self.site_name} Next Activity"

    @property
    def unique_id(self):
        return f"{slugify(self.site_name)}_next_activity"

    def _get_next_activity_data(self):
        soonest_activity = None
        soonest_date = None
        soonest_next_visit = None

        for activity_name, activity in self.coordinator.data.items():
            date_text = activity.get("next_visit", "")

            try:
                cleaned_date = date_text.replace("Week commencing:", "").strip()
                next_date = datetime.strptime(cleaned_date, "%d/%m/%Y").date()

                if soonest_date is None or next_date < soonest_date:
                    soonest_date = next_date
                    soonest_activity = activity_name
                    soonest_next_visit = date_text

            except Exception:
                continue

        return soonest_activity, soonest_date, soonest_next_visit

    @property
    def native_value(self):
        activity_name, _, _ = self._get_next_activity_data()
        return activity_name

    @property
    def extra_state_attributes(self):
        activity_name, next_date, next_visit = self._get_next_activity_data()

        if not activity_name or next_date is None:
            return {}

        return {
            "site": self.site_name,
            "activity": activity_name,
            "next_visit": next_visit,
            "next_visit_date": next_date.strftime("%d/%m/%Y"),
            "days_until": (next_date - datetime.now().date()).days,
        }


class NextActivityDateSensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:calendar-clock"
    def __init__(self, coordinator, site_name):
        super().__init__(coordinator)
        self.site_name = site_name

    @property
    def name(self):
        return f"{self.site_name} Next Activity Date"

    @property
    def unique_id(self):
        return f"{slugify(self.site_name)}_next_activity_date"

    @property
    def native_value(self):
        activity_name, next_date, _ = NextActivitySensor(
            self.coordinator,
            self.site_name,
        )._get_next_activity_data()

        if not activity_name or next_date is None:
            return None

        return next_date.strftime("%d/%m/%Y")


class DaysUntilNextActivitySensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:timer-sand"
    _attr_native_unit_of_measurement = "days"
    _attr_state_class = SensorStateClass.MEASUREMENT
    def __init__(self, coordinator, site_name):
        super().__init__(coordinator)
        self.site_name = site_name

    @property
    def name(self):
        return f"{self.site_name} Days Until Next Activity"

    @property
    def unique_id(self):
        return f"{slugify(self.site_name)}_days_until_next_activity"

    @property
    def native_value(self):
        activity_name, next_date, _ = NextActivitySensor(
            self.coordinator,
            self.site_name,
        )._get_next_activity_data()

        if not activity_name or next_date is None:
            return None

        return (next_date - datetime.now().date()).days


class LastActivitySensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:calendar-check"
    def __init__(self, coordinator, site_name):
        super().__init__(coordinator)
        self.site_name = site_name

    @property
    def name(self):
        return f"{self.site_name} Last Activity"

    @property
    def unique_id(self):
        return f"{slugify(self.site_name)}_last_activity"

    def _get_last_activity_data(self):
        latest_activity = None
        latest_date = None
        latest_last_visit = None

        for activity_name, activity in self.coordinator.data.items():
            date_text = activity.get("last_visit", "")

            try:
                cleaned_date = date_text.replace("Week commencing:", "").strip()
                last_date = datetime.strptime(cleaned_date, "%d/%m/%Y").date()

                if latest_date is None or last_date > latest_date:
                    latest_date = last_date
                    latest_activity = activity_name
                    latest_last_visit = date_text

            except Exception:
                continue

        return latest_activity, latest_date, latest_last_visit

    @property
    def native_value(self):
        activity_name, _, _ = self._get_last_activity_data()
        return activity_name

    @property
    def extra_state_attributes(self):
        activity_name, last_date, last_visit = self._get_last_activity_data()

        if not activity_name or last_date is None:
            return {}

        return {
            "site": self.site_name,
            "activity": activity_name,
            "last_visit": last_visit,
            "last_visit_date": last_date.strftime("%d/%m/%Y"),
            "days_since": (datetime.now().date() - last_date).days,
        }


class LastActivityDateSensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:history"
    def __init__(self, coordinator, site_name):
        super().__init__(coordinator)
        self.site_name = site_name

    @property
    def name(self):
        return f"{self.site_name} Last Activity Date"

    @property
    def unique_id(self):
        return f"{slugify(self.site_name)}_last_activity_date"

    @property
    def native_value(self):
        activity_name, last_date, _ = LastActivitySensor(
            self.coordinator,
            self.site_name,
        )._get_last_activity_data()

        if not activity_name or last_date is None:
            return None

        return last_date.strftime("%d/%m/%Y")


class DaysSinceLastActivitySensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:timeline-clock"
    _attr_native_unit_of_measurement = "days"
    _attr_state_class = SensorStateClass.MEASUREMENT
    def __init__(self, coordinator, site_name):
        super().__init__(coordinator)
        self.site_name = site_name

    @property
    def name(self):
        return f"{self.site_name} Days Since Last Activity"

    @property
    def unique_id(self):
        return f"{slugify(self.site_name)}_days_since_last_activity"

    @property
    def native_value(self):
        activity_name, last_date, _ = LastActivitySensor(
            self.coordinator,
            self.site_name,
        )._get_last_activity_data()

        if not activity_name or last_date is None:
            return None

        return (datetime.now().date() - last_date).days

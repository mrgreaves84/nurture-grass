from datetime import datetime, timedelta

from homeassistant.components.calendar import (
    CalendarEntity,
    CalendarEvent,
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

    async_add_entities(
        [
            NurtureMaintenanceCalendar(
                coordinator,
                entry,
            )
        ]
    )


class NurtureMaintenanceCalendar(
    CoordinatorEntity,
    CalendarEntity,
):
    _attr_icon = "mdi:calendar-month"

    def __init__(
        self,
        coordinator,
        entry,
    ):
        super().__init__(coordinator)

        self.site_name = clean_site_name(
            entry.data.get(
                CONF_SITE_NAME,
                "Nurture Site",
            )
        )

        self._attr_name = (
            f"{self.site_name} Maintenance Calendar"
        )

        self._attr_unique_id = (
            f"{slugify(self.site_name)}_maintenance_calendar"
        )

        events = self._get_events()
        self._attr_event = events[0] if events else None

    @property
    def event(self):
        return self._attr_event

    async def async_update(self) -> None:
        events = self._get_events()
        self._attr_event = events[0] if events else None

    async def async_get_events(
        self,
        hass,
        start_date,
        end_date,
    ):
        events = []

        range_start = (
            start_date.date()
            if hasattr(start_date, "date")
            else start_date
        )

        range_end = (
            end_date.date()
            if hasattr(end_date, "date")
            else end_date
        )

        for event in self._get_events():
            if (
                event.start < range_end
                and event.end > range_start
            ):
                events.append(event)

        return events

    def _get_events(self):
        events = []

        for activity_name, activity in self.coordinator.data.items():
            date_text = activity.get("next_visit", "")

            try:
                clean_date = (
                    date_text
                    .replace("Week commencing:", "")
                    .strip()
                )

                start = datetime.strptime(
                    clean_date,
                    "%d/%m/%Y",
                ).date()

                end = start + timedelta(days=1)

                events.append(
                    CalendarEvent(
                        summary=(
                            f"{activity_name} - "
                            f"{self.site_name}"
                        ),
                        start=start,
                        end=end,
                        description=(
                            f"{activity_name} scheduled "
                            f"for week commencing "
                            f"{clean_date}."
                        ),
                        location=self.site_name,
                    )
                )

            except Exception:
                continue

        return sorted(
            events,
            key=lambda event: event.start,
        )
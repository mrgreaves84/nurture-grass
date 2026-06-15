from datetime import datetime, timedelta
import logging

import aiohttp
from bs4 import BeautifulSoup

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    BASE_URL,
    CONF_REFRESH_HOURS,
    CONF_SITE_ID,
    CONF_SITE_NAME,
    DEFAULT_REFRESH_HOURS,
)
from .repairs import (
    create_date_parse_issue,
    create_no_activities_issue,
    create_website_unavailable_issue,
    delete_date_parse_issue,
    delete_no_activities_issue,
    delete_website_unavailable_issue,
    create_site_not_found_issue,
    delete_site_not_found_issue,
    create_invalid_config_issue,
    delete_invalid_config_issue,
)

_LOGGER = logging.getLogger(__name__)


class NurtureCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass,
        config_entry,
    ):
        refresh_hours = config_entry.options.get(
            CONF_REFRESH_HOURS,
            DEFAULT_REFRESH_HOURS,
        )

        super().__init__(
            hass,
            logger=_LOGGER,
            name="nurture_grass",
            update_interval=timedelta(
                hours=refresh_hours
            ),
        )

        self.site_id = config_entry.data[CONF_SITE_ID]
        self.last_refresh = None
        self.config_entry = config_entry

        if not (
            config_entry.data.get(
                CONF_SITE_ID
            )
            and config_entry.data.get(
                CONF_SITE_NAME
            )
        ):
            create_invalid_config_issue(
                hass
            )
        else:
            delete_invalid_config_issue(
                hass
            )

    async def _async_update_data(self):
        url = (
            f"{BASE_URL}"
            f"/C004097/site-details/?sid={self.site_id}"
        )

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    },
                ) as response:
                    response.raise_for_status()
                    html = await response.text()

            delete_website_unavailable_issue(
                self.hass
            )

        except Exception as err:
            create_website_unavailable_issue(
                self.hass
            )

            raise err

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        page_text = soup.get_text(
            " ",
            strip=True,
        ).lower()

        site_not_found = any(
            phrase in page_text
            for phrase in (
                "site not found",
                "no site found",
                "invalid site",
                "no records found",
            )
        )

        if site_not_found:
            create_site_not_found_issue(
                self.hass
            )
        else:
            delete_site_not_found_issue(
                self.hass
            )

        activities = {}
        date_parse_failed = False

        for row in soup.find_all("tr"):
            cells = row.find_all("td")

            if len(cells) < 3:
                continue

            activity = cells[0].get_text(strip=True)
            last_visit = cells[1].get_text(strip=True)
            next_visit = cells[2].get_text(strip=True)

            if activity:
                for date_value in (
                    last_visit,
                    next_visit.replace(
                        "Week commencing:",
                        "",
                    ).strip(),
                ):
                    try:
                        datetime.strptime(
                            date_value,
                            "%d/%m/%Y",
                        )
                    except Exception:
                        date_parse_failed = True

                activities[activity] = {
                    "name": activity,
                    "last_visit": last_visit,
                    "next_visit": next_visit,
                }

        if not activities:
            create_no_activities_issue(
                self.hass
            )
        else:
            delete_no_activities_issue(
                self.hass
            )

        if date_parse_failed:
            create_date_parse_issue(
                self.hass
            )
        else:
            delete_date_parse_issue(
                self.hass
            )

        self.last_refresh = datetime.now()

        return activities

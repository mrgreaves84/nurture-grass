from __future__ import annotations

from urllib.parse import parse_qs, quote_plus, urlparse

import aiohttp
import voluptuous as vol
from bs4 import BeautifulSoup

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    BASE_URL,
    CONF_NOTIFY_DAYS,
    CONF_POSTCODE,
    CONF_REFRESH_HOURS,
    CONF_SITE_ID,
    CONF_SITE_NAME,
    DEFAULT_NOTIFY_DAYS,
    DEFAULT_REFRESH_HOURS,
    DOMAIN,
)


class NurtureGrassConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    VERSION = 1

    def __init__(self):
        self._postcode = None
        self._sites = {}

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return NurtureOptionsFlow()

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            self._postcode = user_input[CONF_POSTCODE].strip()
            self._sites = await self._async_find_sites(self._postcode)

            if len(self._sites) == 0:
                errors["base"] = "no_sites"

            elif len(self._sites) == 1:
                site_id = next(iter(self._sites))
                site_name = self._sites[site_id]

                return self.async_create_entry(
                    title=site_name,
                    data={
                        CONF_POSTCODE: self._postcode,
                        CONF_SITE_ID: site_id,
                        CONF_SITE_NAME: site_name,
                    },
                )

            else:
                return await self.async_step_site()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_POSTCODE): str,
                }
            ),
            errors=errors,
        )

    async def async_step_site(self, user_input=None):
        if user_input is not None:
            site_id = user_input[CONF_SITE_ID]
            site_name = self._sites[site_id]

            return self.async_create_entry(
                title=site_name,
                data={
                    CONF_POSTCODE: self._postcode,
                    CONF_SITE_ID: site_id,
                    CONF_SITE_NAME: site_name,
                },
            )

        return self.async_show_form(
            step_id="site",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SITE_ID): vol.In(self._sites),
                }
            ),
        )

    async def _async_find_sites(self, postcode):
        url = (
            f"{BASE_URL}/C004097/site-select/"
            f"?q={quote_plus(postcode)}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
            ) as response:
                html = await response.text()

        soup = BeautifulSoup(html, "html.parser")
        sites = {}

        for row in soup.select("table.ms-table tbody tr"):
            link = row.select_one("a[href*='site-details']")
            address = row.select_one("strong")

            if not link or not address:
                continue

            href = link.get("href", "")
            site_id = parse_qs(urlparse(href).query).get(
                "sid",
                [None],
            )[0]

            if not site_id:
                continue

            sites[site_id] = address.get_text(" ", strip=True)

        return sites


class NurtureOptionsFlow(config_entries.OptionsFlow):

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={
                    CONF_REFRESH_HOURS: int(
                        user_input[CONF_REFRESH_HOURS]
                    ),
                    CONF_NOTIFY_DAYS: int(
                        user_input[CONF_NOTIFY_DAYS]
                    ),
                },
            )

        current_refresh = str(
            self.config_entry.options.get(
                CONF_REFRESH_HOURS,
                DEFAULT_REFRESH_HOURS,
            )
        )

        current_notify = str(
            self.config_entry.options.get(
                CONF_NOTIFY_DAYS,
                DEFAULT_NOTIFY_DAYS,
            )
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_REFRESH_HOURS,
                        default=current_refresh,
                    ): vol.In(
                        {
                            "24": "24 hours",
                            "48": "48 hours",
                            "72": "72 hours",
                            "168": "7 days",
                        }
                    ),
                    vol.Required(
                        CONF_NOTIFY_DAYS,
                        default=current_notify,
                    ): vol.In(
                        {
                            "1": "1 day",
                            "3": "3 days",
                            "5": "5 days",
                            "7": "7 days",
                        }
                    ),
                }
            ),
        )

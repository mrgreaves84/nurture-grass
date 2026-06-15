from __future__ import annotations

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_NOTIFY_DAYS,
    CONF_POSTCODE,
    CONF_REFRESH_HOURS,
    CONF_SITE_ID,
    CONF_SITE_NAME,
    DEFAULT_NOTIFY_DAYS,
    DEFAULT_REFRESH_HOURS,
    DOMAIN,
)

TO_REDACT = {
    CONF_POSTCODE,
    CONF_SITE_ID,
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    diagnostics = {
        "integration": {
            "domain": DOMAIN,
            "version": "0.9.0",
            "data_source": "Nurture Landscapes",
        },
        "config_entry": {
            "title": entry.title,
            "data": dict(entry.data),
            "options": dict(entry.options),
        },
        "settings": {
            "refresh_hours": entry.options.get(
                CONF_REFRESH_HOURS,
                DEFAULT_REFRESH_HOURS,
            ),
            "notify_days": entry.options.get(
                CONF_NOTIFY_DAYS,
                DEFAULT_NOTIFY_DAYS,
            ),
        },
        "coordinator": {
            "last_refresh": (
                coordinator.last_refresh.isoformat()
                if coordinator.last_refresh
                else None
            ),
            "activities_found": len(coordinator.data or {}),
        },
        "activities": coordinator.data or {},
    }

    return async_redact_data(
        diagnostics,
        TO_REDACT,
    )

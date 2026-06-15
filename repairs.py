from homeassistant.helpers import issue_registry as ir

from .const import DOMAIN


def create_no_activities_issue(hass):
    ir.async_create_issue(
        hass,
        DOMAIN,
        "no_activities_found",
        is_fixable=False,
        severity=ir.IssueSeverity.WARNING,
        translation_key="no_activities_found",
    )


def delete_no_activities_issue(hass):
    ir.async_delete_issue(
        hass,
        DOMAIN,
        "no_activities_found",
    )


def create_website_unavailable_issue(hass):
    ir.async_create_issue(
        hass,
        DOMAIN,
        "website_unavailable",
        is_fixable=False,
        severity=ir.IssueSeverity.ERROR,
        translation_key="website_unavailable",
    )


def delete_website_unavailable_issue(hass):
    ir.async_delete_issue(
        hass,
        DOMAIN,
        "website_unavailable",
    )


def create_date_parse_issue(hass):
    ir.async_create_issue(
        hass,
        DOMAIN,
        "date_parse_failed",
        is_fixable=False,
        severity=ir.IssueSeverity.WARNING,
        translation_key="date_parse_failed",
    )


def delete_date_parse_issue(hass):
    ir.async_delete_issue(
        hass,
        DOMAIN,
        "date_parse_failed",
    )


def create_site_not_found_issue(hass):
    ir.async_create_issue(
        hass,
        DOMAIN,
        "site_not_found",
        is_fixable=False,
        severity=ir.IssueSeverity.ERROR,
        translation_key="site_not_found",
    )


def delete_site_not_found_issue(hass):
    ir.async_delete_issue(
        hass,
        DOMAIN,
        "site_not_found",
    )


def create_invalid_config_issue(hass):
    ir.async_create_issue(
        hass,
        DOMAIN,
        "invalid_configuration",
        is_fixable=False,
        severity=ir.IssueSeverity.ERROR,
        translation_key="invalid_configuration",
    )


def delete_invalid_config_issue(hass):
    ir.async_delete_issue(
        hass,
        DOMAIN,
        "invalid_configuration",
    )
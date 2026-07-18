from __future__ import annotations

from datetime import date, datetime, timedelta
import re

NEXT_VISIT_SCHEDULED = "scheduled"
NEXT_VISIT_NOT_SCHEDULED = "not_scheduled"
NEXT_VISIT_MISSING = "missing"
NEXT_VISIT_UNRECOGNISED = "unrecognised"

NO_SCHEDULED_VISIT_VALUES = {
    "no scheduled visit",
    "no scheduled visits",
    "no planned visit",
    "no visits scheduled",
    "not currently scheduled",
}

NEXT_VISIT_PARSE_FAILURE_STATUSES = frozenset(
    {
        NEXT_VISIT_MISSING,
        NEXT_VISIT_UNRECOGNISED,
    }
)

UK_POSTCODE_PATTERN = re.compile(
    r"^(GIR0AA|"
    r"(?:[A-PR-UWYZ][0-9][0-9A-HJKSTUW]?|"
    r"[A-PR-UWYZ][A-HK-Y][0-9][0-9ABEHMNPRVWXY]?)"
    r"[0-9][ABD-HJLNP-UW-Z]{2})$"
)


def parse_portal_date(value: str | None) -> date | None:
    """Parse a date supplied by the maintenance portal."""

    if not value:
        return None

    clean_value = re.sub(
        r"^week\s+commencing\s*:\s*",
        "",
        value.strip(),
        flags=re.IGNORECASE,
    )

    try:
        return datetime.strptime(clean_value, "%d/%m/%Y").date()
    except ValueError:
        return None


def normalise_next_visit(value: str | None) -> dict:
    """Classify a portal next-visit value while retaining its original text."""

    raw_value = (value or "").strip()
    parsed_date = parse_portal_date(raw_value)

    if parsed_date is not None:
        status = NEXT_VISIT_SCHEDULED
    elif not raw_value:
        status = NEXT_VISIT_MISSING
    elif " ".join(raw_value.casefold().split()) in NO_SCHEDULED_VISIT_VALUES:
        status = NEXT_VISIT_NOT_SCHEDULED
    else:
        status = NEXT_VISIT_UNRECOGNISED

    return {
        "next_visit": raw_value,
        "next_visit_raw": raw_value,
        "next_visit_status": status,
        "next_visit_date": (
            parsed_date.strftime("%d/%m/%Y")
            if parsed_date is not None
            else None
        ),
    }


def normalise_postcode(value: str) -> str:
    """Return a consistently formatted UK postcode."""

    compact = "".join(value.upper().split())

    if not UK_POSTCODE_PATTERN.fullmatch(compact):
        raise ValueError("invalid_postcode")

    return f"{compact[:-3]} {compact[-3:]}"


def week_commencing_window(start: date) -> tuple[date, date]:
    """Return an all-day Monday-Sunday window with an exclusive end."""

    return start, start + timedelta(days=7)


def clean_site_name(site_name: str) -> str:
    """Return a friendly site name."""

    parts = [
        part.strip()
        for part in site_name.split(",")
        if part.strip()
        and part.strip().upper() != "NULL"
        and not part.strip().startswith("(")
    ]

    return ", ".join(parts[:3])

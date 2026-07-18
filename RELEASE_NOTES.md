# Nurture Grass Schedule 1.5.0

Version 1.5 is a maintenance upgrade for the existing integration. It improves
portal resilience, calendar accuracy, and configuration usability without
introducing the Project Zero architecture planned for version 2.0.

## Highlights

- **Unscheduled visits are now valid data.** Portal text such as
  `No scheduled visit` is retained and classified as `not_scheduled` instead
  of triggering a date parsing repair.
- **Calendar entries represent the whole planned week.** A week-commencing
  visit is shown from Monday through Sunday, with the following Monday used as
  the calendar's exclusive end date.
- **Postcode entry is more forgiving.** Lowercase, missing spaces, and repeated
  spaces are accepted. Valid postcodes are stored in standard uppercase form.
- **Diagnostics are clearer.** Each activity includes the raw next-visit value,
  its normalised status, and a parsed date when one is available.

## Normalised next-visit states

| Status | Meaning |
| --- | --- |
| `scheduled` | The portal supplied a recognised visit date. |
| `not_scheduled` | The portal supplied a recognised no-visit status. |
| `missing` | The next-visit field was blank or absent. |
| `unrecognised` | The portal supplied text the integration does not understand. |

Only `missing` and `unrecognised` values raise the existing date parsing repair.
Unscheduled activities do not create calendar events and do not become due
soon.

## Upgrade notes

No configuration migration is required. Existing entity identifiers and the
original `next_visit` coordinator field remain unchanged for compatibility.

# Changelog

## 1.5.0

### Added

- Recognise valid unscheduled portal values, including `No scheduled visit`,
  without reporting a date parsing failure.
- Preserve the raw next-visit text and expose a normalised status and parsed
  date in coordinator data, diagnostics, and next-visit sensor attributes.
- Accept UK postcode input regardless of capitalisation or reasonable spacing,
  and store it in standard uppercase format.
- Add regression tests for portal-value classification, postcode
  normalisation, and calendar event duration.

### Changed

- Grass-cutting calendar events now cover the complete week commencing period,
  from Monday through Sunday. The event end is the following Monday because
  Home Assistant calendar end dates are exclusive.
- Use `manifest.json` as the authoritative integration version source, including
  diagnostics.

### Fixed

- A valid textual portal status no longer makes the integration report that it
  could not read a maintenance date.
- Unscheduled activities no longer create calendar events or activate due-soon
  binary sensors.

Version 2.0 remains reserved for the separate Project Zero reengineering work.

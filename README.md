# Nurture Grass Schedule

Home Assistant integration for the Vico Homes Grounds Maintenance Portal, providing maintenance schedules, calendars, notifications and activity tracking.

## Overview

Nurture Grass Schedule integrates the Vico Homes Grounds Maintenance Portal with Home Assistant, allowing residents to monitor upcoming grounds maintenance activities directly from their Home Assistant installation.

The integration automatically retrieves maintenance schedules and exposes them as Home Assistant entities, including sensors, binary sensors, calendar events, and notifications.

While initially developed for grass cutting schedules, the integration is designed to support additional maintenance activities such as hedge trimming and other grounds maintenance services as they become available through the portal.

## Features

* Automatic schedule retrieval from the Vico Homes Grounds Maintenance Portal
* Support for multiple maintenance activity types
* Calendar integration
* Next activity tracking
* Days until next activity sensors
* Due soon binary sensors
* Manual refresh button
* Config Flow support
* Options Flow support
* Diagnostics support
* Repairs support
* Translation framework for multiple languages
* Home Assistant dashboard ready

## Installation

### HACS Installation

1. Open HACS in Home Assistant.
2. Add this repository as a custom repository.
3. Select Integration.
4. Search for "Nurture Grass Schedule".
5. Install the integration.
6. Restart Home Assistant.

### Manual Installation

1. Download the latest release.
2. Copy the `custom_components/nurture_grass` folder into your Home Assistant `custom_components` directory.
3. Restart Home Assistant.
4. Add the integration through Settings → Devices & Services.

## Configuration

1. Add the integration.
2. Enter your postcode.
3. Select your maintenance site.
4. Configure optional refresh and notification settings.
5. Save the configuration.

## Entities

### Sensors

* Next Activity
* Next Activity Date
* Days Until Next Activity
* Last Refresh
* Activity Next Visit
* Activity Last Visit
* Activity Days Until Visit

### Binary Sensors

* Activity Due Soon

### Calendar

* Maintenance Calendar

### Button

* Refresh Schedule

## Notifications

The integration can generate notifications before scheduled maintenance visits using configurable lead times.

## Diagnostics

Diagnostics can be downloaded directly from the integration menu and are designed to assist with troubleshooting while avoiding unnecessary exposure of personal information.

## Repairs

The integration includes automatic Repairs support for:

* Website unavailable
* Site not found
* No activities found
* Date parsing failures
* Invalid configuration

## Supported Languages

Current translation framework includes:

* English
* Punjabi
* Romanian
* Latvian
* Lithuanian
* Kurdish
* Arabic
* Russian
* Chinese
* Slovak

Additional translations are welcome through community contributions.

## Screenshots

Screenshots and dashboard examples will be added in future releases.

## Roadmap

### Version 1.x

* Enhanced dashboard examples
* Additional maintenance activity support
* Expanded translations
* Improved diagnostics

## Disclaimer

This project is an independent Home Assistant integration and is not affiliated with, endorsed by, or maintained by Vico Homes or Tivoli.

# ENYXA for Home Assistant v0.2.1

Read-only Home Assistant integration for the ENYXA API. Discovers paired devices and provides battery, charging, storage and synchronization entities. Configurable polling interval: 1, 5, 10, 15 or 30 minutes.

## Installation with HACS

Add `https://github.com/luguen/ha-enyxa` as a custom Integration repository in HACS, install or update ENYXA, and restart Home Assistant. Existing ENYXA configuration entries should be retained; do not remove the integration from Devices & Services.

## Configuration

Use your ENYXA HTTPS URL and a personal API token with `devices:read`, `battery:read`, `storage:read`. Never commit tokens.

## Branding

`branding/` contains proposed icon and logo assets derived from the provided ENYXA SVG. **These files are publication assets, not an automatic Home Assistant icon registration.** To display branding in Home Assistant's integration UI, submit assets under the `enyxa` domain to the official Home Assistant brands repository following its current contribution requirements. A custom HACS repository alone does not guarantee branding display. The source SVG is included for further refinement.

## Changes in 0.2.1

- Updated GitHub documentation and issue links.
- Prepared ENYXA branding assets.
- No sensor, coordinator, entity-ID, API or polling logic changes relative to v0.2.0.

## License

No license has been added automatically. Select a license only if you have the rights to distribute the code and artwork under its terms.

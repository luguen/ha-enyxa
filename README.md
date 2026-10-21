# ENYXA for Home Assistant v0.2.0

Custom integration for ENYXA API. Read-only sensors and binary sensors for paired devices.

## Installation

**Manual:** copy `custom_components/enyxa` to `/config/custom_components/enyxa`, restart Home Assistant, then add ENYXA under Settings > Devices & services. Existing configuration entries should remain in place. Back up the existing directory first.

**HACS (custom repository):** publish the contents of this archive at the root of your own public GitHub repository. Replace `REPLACE_WITH_YOUR_USERNAME` in `manifest.json` with your GitHub username and repository path. In HACS, add the repository URL as a custom **Integration** repository, install ENYXA, and restart Home Assistant. This package has **not** been submitted to the HACS default catalog.

## Configuration

Provide ENYXA HTTPS URL and a read-only personal token with `devices:read`, `battery:read`, `storage:read`. Never commit tokens.

Configure polling in Settings > Devices & services > ENYXA > Configure: 1, 5, 10, 15, or 30 minutes. Default 5 minutes.

## Notes

- Device API errors retain the last measurement while marking that device unavailable. This is not yet a full offline-age policy.
- Existing sensors and entity identifiers are intended to remain stable, but this release has not been tested in your running Home Assistant instance.
- HACS packaging prepared; no GitHub repository has been created or published.

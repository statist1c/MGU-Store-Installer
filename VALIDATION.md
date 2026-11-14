# Validation — 0.1.0-preview

Date: 14 November 2026. AI implementation: Codex, GPT-6.1. Human review: pending.

- `assembleDebug` and Android lint: passed; remaining warnings concern English text localization and a redundant resource qualifier.
- Six Python tests: passed. Cover optional component selection, duplicate/unsafe catalog entries, size/SHA-256 mismatch rejection, deploy-manifest path/hash checks, coding rejection, and remote failure propagation.
- Public-release integration: passed against catalog commit `fc5750a8474359ad20c1c01cf29d997ff7f2d621`. Downloaded and verified all seven selected artifacts and their sizes/hashes. Verified deploy manifest files and assembled the 23-member kit (approximately 22.9 MB). **SSH was mocked; nothing was uploaded to a head unit.**
- Android x86-64 emulator: APK installed and launched. Embedded Python imported the installer and command data; SHA-256 worked; private-address/token URL validation passed; live HTTPS GitHub release metadata downloaded successfully.
- Native light/dark layout, tab navigation and launcher artwork visually inspected in the emulator.
- APK signature and package metadata verified with Android build tools.

Not validated: real-car SSH negotiation, host fingerprint comparison with a real unit, encrypted user keys on vehicle hardware, physical USB Ethernet routing, simultaneous car hotspot/mobile internet on a phone, install/restart results, real Phone access API end-to-end behavior, or ARM64 runtime execution. ARM64 native libraries are packaged. Upstream itself describes iDrive 8 real-car support as untested.

This is a working build and an experimental Android port, not a vehicle-certified release. Review `README.md` before use.

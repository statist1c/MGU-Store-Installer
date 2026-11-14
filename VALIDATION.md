# Validation — v0.2.0

Date: 15 November 2026. AI implementation: Codex, GPT-6.1. Human review: pending.

- Android assembleDebug, lint and instrumentation APK compilation: passed.
- Six Python installer tests: passed.
- Sixteen pure-Java SemVer precedence/validation cases: passed.
- Android x86-64 emulator: embedded Python, bundled upstream commands, SHA-256, private Phone access URL validation and live GitHub HTTPS metadata smoke checks passed.
- Replaced installed v0.1.0-preview (versionCode 1) with v0.2.0 (versionCode 2) using Android's in-place update: passed without uninstall.
- APK signing certificate matches original locally delivered v0.1.0-preview. SHA-256 certificate fingerprint: 8b7e339ac0b43580b6db9d5723d814c1df4102ca321db492b604c03eb60a4271.
- Settings update controls visible; Check now reached GitHub and reported no newer compatible release. Persisted periodic job 7101 registered for daily checks with a network constraint.
- Manifest/resource checks passed for protected job services, read-only APK provider and narrowly scoped permissions.
- No real-car operation was performed. A complete future-release download, verification and Android-install cycle and OEM background behavior remain unverified. APK is debug-signed and includes ARM64 and x86-64 libraries; ARM64 physical runtime was not tested.

## Original installer validation

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

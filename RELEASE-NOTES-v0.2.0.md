## MGU Store Installer v0.2.0

### New

- New MGU STORE icon with BMW logo, 7/8 label and motorsport styling.
- Settings → App updates with **Check now** and **Check daily for app updates**, enabled by default.
- Optional preview-release channel and notifications for available updates.
- Review release notes, choose Download, then install through Android's confirmation screen.
- APK size, SHA-256, app identity, version and signing-certificate checks before installation.
- Added the permissions needed for notifications, persisted update checks and user-approved APK installation. No broad storage permission or silent installation.

### Installation and compatibility

Download **MGU-Store-Installer-v0.2.0.apk** from this release. Android 8.0+ on ARM64 or x86-64 is required.

This APK uses the same signing certificate as the original locally supplied v0.1.0-preview APK; an in-place emulator upgrade passed. Independently built GitHub Actions APKs may use another debug key and cannot necessarily be updated with this APK. Do not uninstall an existing installation without backing up its private SSH key.

Existing v0.1.0 installations need a manual installation of v0.2.0 to gain the updater. Future updates require the same signing key, a higher versionCode and a GitHub release containing one universal APK with SHA-256 metadata. Android may delay daily checks and asks the user to allow this app as an installation source before its first app update.

### Validation and limitations

Android build/lint, six installer tests, 16 version-comparison cases and Android/Python emulator smoke checks passed. Manual GitHub checking and persisted daily scheduling were checked in the emulator.

This is an early, debug-signed release. Real-car installation and a complete future-release download/installation cycle on physical phones remain unverified. Root SSH access to the head unit is still required; this app does not root, flash firmware or restore coding.

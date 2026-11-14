# App updates — v0.2.0

Version 0.2.0 includes the MGU STORE / BMW icon and GitHub release updater. Android versionCode is 2.

## User-facing behavior

- Selected icon: **D — Motorsport**, revised to read **MGU STORE**, with BMW logo, 7/8 label and download arrow. Original selected artwork is `android/app/src/main/res/drawable-nodpi/ic_mgu_store_next.png`. The adaptive launcher uses inset artwork; monochrome launchers retain the simple download mark. The selected artwork is inset for Android adaptive launcher masks.
- Settings → App updates: daily automatic checks, optional preview channel, Check now, review release notes, explicit Download and explicit Install actions.
- Stable releases are the default. Version precedence uses SemVer, not string comparison. Drafts, malformed tags, older versions and releases without one universal APK and verification data are skipped.
- Daily checks are best effort via Android JobScheduler. Android may delay them during Doze, offline periods, battery restrictions or force-stop. App startup also checks when the last successful check is older than one day. No exact alarm or battery-optimization exemption is requested.
- GitHub network failures and rate limiting leave the installed app usable. Notifications open Settings for review. Declining notification permission still permits manual checks and in-app status. No automatic APK downloads or unattended installation.
- DownloadManager downloads after the user chooses Download, to the app's external private files directory. Completion schedules checksum/package verification and a ready-to-install notification. The foreground Settings screen also recovers download state after process death.
- Before installation: verify expected size, SHA-256, package name, a higher Android versionCode, SemVer matching the tag and exactly matching signing certificates. Unsupported signing-key rotation is rejected. Recheck the APK immediately before handing it to Android's package installer. Existing head-unit operations block starting an app download/install.
- When Android's per-app “Allow from this source” permission is disabled, Install opens that permission screen. Return to the app and tap Install again after granting it. Android still asks the user to confirm installation.

## Permissions and components

Existing: `INTERNET`, `ACCESS_NETWORK_STATE`, `POST_NOTIFICATIONS` (runtime request on Android 13+). New: `REQUEST_INSTALL_PACKAGES` for user-approved sideload installation; `RECEIVE_BOOT_COMPLETED` for persisted daily jobs. Two job services are protected with Android's `BIND_JOB_SERVICE` permission. The download receiver only accepts the tracked request and independently validates the result. A non-exported, URI-grant provider exposes exactly the verified update APK read-only.

No broad storage access, package inventory access, silent-install privilege, root permission or exact alarm permission is added. This updater is intended for the GitHub/sideload distribution channel.

## Publishing a compatible update

1. Use repository `statist1c/MGU-Store-Installer` GitHub **Releases**, not just Actions artifacts. Publish one standalone universal `.apk` asset containing ARM64 and x86-64 native libraries. Multiple APK assets are deliberately unsupported in this first updater implementation.
2. Tag releases using SemVer such as `v0.2.0`. The APK versionName must have matching SemVer precedence, and versionCode must increase. Preview tags must be marked prerelease; users opt into those checks.
3. GitHub's asset `digest` must contain `sha256:<64 hex digits>`. Alternatively attach an asset named exactly `SHA256SUMS.txt`, containing the APK's exact asset filename and SHA-256, for example `0123...<64 hex>  MGU-Store-Installer-v0.2.0.apk`. A real checksum must be computed from the final signed APK.
4. Sign every APK with the **same durable signing key**. The existing CI workflow generates debug-signed builds and is not a stable production release-signing pipeline. Set up durable release signing before offering updater-compatible releases. Never commit private signing keys. This source change does not create a key or alter CI to use one.
5. Existing local preview APKs and Actions APKs may have different debug certificates. Android cannot update one with the other. The app rejects that mismatch and does not offer uninstall/data-erasure as a workaround. Plan any one-time migration separately, preserving private SSH-key backups.
6. Current installed v0.1.0 APKs do not have this updater. Users must manually install the first compatible updater-enabled release. Version 0.2.0 must be installed manually on older versions that do not include an updater.

## Verification status

Android build and lint passed. Six installer tests, 16 semantic-version cases and embedded Android/Python smoke checks passed. An emulator accepted the same-key v0.1.0-to-v0.2.0 in-place update. The Settings manual check reached GitHub, and the persisted daily job was registered. Real future-release download-to-install operation, background behavior on physical phones and real-car installation remain unverified. See VALIDATION.md.

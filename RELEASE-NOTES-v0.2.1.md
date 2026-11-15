## MGU Store Installer v0.2.1

Reliability fixes following a comparison with mgu-store upstream commit `fc5750a8474359ad20c1c01cf29d997ff7f2d621`.

- Match the upstream temporary-folder naming convention so abandoned installation kits can be cleaned up by the deploy tool.
- Detect a head-unit restart refusal even when `nsm_control` exits with status zero. Report an active installation lock clearly.
- After installation or Read status, inspect the updater/optional services and upstream iDrive 7/8 Store-tile status. Show ready, restart required, blocked or unverified instead of treating a completed command as proof of readiness.
- Require catalog artifact filenames to match their component ID and version, as the upstream installer does.
- Show the upstream Phone access error message when a source operation is refused or the updater is unavailable.
- Include the full open-source license bundle and Settings license reader added to the repository after v0.2.0.

The selected icon and app-update controls are retained. This app still requires root SSH access; it does not root the head unit or restore coding. Real-car testing is pending. Status messages reflect the deploy tool's report and must be confirmed on the vehicle screen.

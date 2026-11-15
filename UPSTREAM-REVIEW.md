# Upstream compatibility review — v0.2.1

Reviewed 15 November 2026 against mgu-store HEAD `fc5750a8474359ad20c1c01cf29d997ff7f2d621`. This is the same upstream revision originally retained; this review fixes Android-port differences rather than claiming a new upstream release.

## Changes

1. **Abandoned installation kits:** upstream `deploy/unit/mgu-deploy.js` only cleans directories matching `mgu-deploy-kit-<digits>`. Android's `mgu-deploy-kit-android-<timestamp>` did not match. Android now uses a numeric timestamp suffix, while retaining unique private staging directories.
2. **Restart refusals:** upstream `offerRestart` checks both SSH exit status and `[Error. ...]` output because `nsm_control` can exit zero on refusal. Android now checks both, and reports an install-lock refusal explicitly.
3. **Post-install verification:** upstream checks service states plus the deploy tool's JSON tile/fallback report. Android now ports the ID7/ID8 tile rules, checks the selected services and reports ready, restart required, blocked or unknown. Missing/malformed status or a report that does not list the Store cannot produce a ready verdict. Read status uses the same interpretation. No restart happens automatically.
4. **Catalog identity:** upstream requires `<id>@<version>.tgz`, strict component IDs and x.y.z versions. Android now enforces that match, preventing multiple entries from aliasing a local artifact filename.
5. **Phone access errors:** upstream returns useful JSON errors for refused source operations and an unavailable updater. Android now includes those details instead of showing only an HTTP number. Its operation set remains limited to the upstream phone API; no nonexistent install/update endpoint has been added.

## Validation

- Thirteen Python regression tests passed, including numeric staging, a complete mocked installation, restart refusal with exit zero, install-lock refusal, component identity, and ID7/ID8 readiness cases.
- `tools/check_upstream_contract.py` verified verbatim RUN_SH / CODING_CHECK / RESTART data, seeded sources and ten tile cases against the retained upstream JavaScript itself.
- Current public catalog and all seven selected packages downloaded and passed size/SHA-256 checks. The generated deploy kit passed validation. SSH was mocked; no head unit was contacted.
- Android build/lint, full packaged license verification and emulator Python/network smoke checks passed.
- Same-certificate in-place emulator update from v0.2.0 to v0.2.1 passed. No private data was erased by uninstalling.

## Deliberate scope and limits

Existing root SSH, valid coding, stable power and a working vehicle route remain necessary. This Android app still does not implement the computer installer's diagnostic host discovery, SSH jump hosts, private-release authentication, offline kit import or full uninstall. The explicit legacy RSA option and host-key verification remain. The selected logo is unchanged.

Real-car installation, SSH negotiation against a real head unit, physical phone routing and hardware restart results remain unverified. A ready message is the deploy tool's report, not independent physical validation. No new GitHub Release is published by this review; the corrected APK and source are prepared for maintainer review/distribution.

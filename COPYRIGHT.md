# Attribution and licensing

The original **mgu-store** project is maintained by **Robert Nisipeanu and its contributors**: https://github.com/robertnisipeanu/mgu-store . The original authors retain their copyright.

The Android installer adapts upstream commit `fc5750a8474359ad20c1c01cf29d997ff7f2d621`:

- `vendor/mgu-install.js` retains the upstream installer source.
- `android/app/src/main/python/upstream_commands.json` retains its `RUN_SH`, `CODING_CHECK` and `RESTART` constants.
- `android/app/src/main/python/sources.json` retains the upstream source configuration.
- `android/app/src/main/python/installer.py` adapts first-install orchestration to Android using the upstream deploy process.

These files and the companion application's GPL-covered adaptations are available under the **GNU General Public License, version 3 or any later version**. See `LICENSE` for complete terms and the warranty disclaimer.

The Android UI, SSH integration and update flow were developed for **MGU Store Installer**, maintained at https://github.com/statist1c/MGU-Store-Installer . The UI follows the maintainer's MGU iDrive7-8 Root Companion design. AI assistance and validation are recorded in `VALIDATION.md` and repository history. This attribution notice does not transfer copyright ownership.

Third-party copyrights and license terms are retained verbatim in `LICENSES/`. `THIRD_PARTY_NOTICES.md` maps them to the components used. Those components remain the work of their respective authors.

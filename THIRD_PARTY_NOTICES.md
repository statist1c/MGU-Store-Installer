# Third-party notices

MGU Store Installer application code and adaptations of mgu-store are distributed under **GPL-3.0-or-later**. The full GPL text is [LICENSE](LICENSE). Components below retain their own licenses and original copyright notices; they are not relicensed as project-owned work. See [COPYRIGHT.md](COPYRIGHT.md) for upstream attribution.

Full texts are included in [LICENSES](LICENSES/), rather than depending on external links. [PROVENANCE.json](LICENSES/PROVENANCE.json) records their exact origin and SHA-256.

| Component | License / notice | Included text |
| --- | --- | --- |
| mgu-store installer and command/source data | GPL-3.0-or-later; Robert Nisipeanu and upstream contributors | [GPL-3.0.txt](LICENSES/GPL-3.0.txt) |
| JSch 2.28.8, mwiede fork | BSD-style; JCraft and contributors | [JSch-2.28.8.txt](LICENSES/JSch-2.28.8.txt) |
| JZlib bundled within JSch | BSD-style | [JZlib.txt](LICENSES/JZlib.txt) |
| jBCrypt bundled within JSch | ISC-style | [jBCrypt.txt](LICENSES/jBCrypt.txt) |
| Bouncy Castle bcprov-jdk18on 1.87 | Bouncy Castle MIT-style license | [Bouncy-Castle-1.87.txt](LICENSES/Bouncy-Castle-1.87.txt) |
| Chaquopy 17.2.0 | MIT; Chaquo Ltd and contributors | [Chaquopy-17.2.0.txt](LICENSES/Chaquopy-17.2.0.txt) |
| CPython Android runtime 3.13.16-0 | PSF and historical Python licenses | [CPython-3.13.16.txt](LICENSES/CPython-3.13.16.txt) |
| CPython incorporated software | Additional CPython notices, including expat, libmpdec, zlib, libffi, mimalloc and Unicode | [CPython-3.13.16-THIRD-PARTY.rst](LICENSES/CPython-3.13.16-THIRD-PARTY.rst) |
| pyelftools 0.26 in Chaquopy bootstrap | Public-domain / BSD notices as supplied upstream | [pyelftools-0.26.txt](LICENSES/pyelftools-0.26.txt) |
| setuptools 68.2.2 in Chaquopy bootstrap | MIT | [setuptools-68.2.2.txt](LICENSES/setuptools-68.2.2.txt) |
| OpenSSL 3.5.9 | Apache-2.0 | [OpenSSL-3.5.9.txt](LICENSES/OpenSSL-3.5.9.txt) |
| libffi 3.4.4 | MIT-style | [libffi-3.4.4.txt](LICENSES/libffi-3.4.4.txt) |
| bzip2 1.0.8 | bzip2 license | [bzip2-1.0.8.txt](LICENSES/bzip2-1.0.8.txt) |
| liblzma from XZ 5.4.6 | Public-domain library; package summary retained | [XZ-5.4.6.txt](LICENSES/XZ-5.4.6.txt) |
| SQLite | Public-domain dedication | [SQLite-public-domain.txt](LICENSES/SQLite-public-domain.txt) |
| Android C++ runtime / libc++ | LLVM/libc++ license text and exceptions | [libcxx.txt](LICENSES/libcxx.txt) |
| Gradle wrapper 8.9 (source/build tooling) | Apache-2.0 | [Gradle-8.9.txt](LICENSES/Gradle-8.9.txt) |
| Gradle wrapper notice | Gradle attribution | [Gradle-8.9-NOTICE.txt](LICENSES/Gradle-8.9-NOTICE.txt) |

The Python runtime version was resolved from the v0.2.0 build artifact `com.chaquo.python:target:3.13.16-0`. Native dependency versions follow Chaquopy 17.2.0's Python build recipe. The complete CPython incorporated-software notices are retained, including notices for optional code that may not be present in every Android build.

Gradle and the Android toolchain are build tools, not installed app components. Vehicle-side packages downloaded by the installer are not bundled into this APK and retain their own upstream notices/source distribution. See [SOURCE.md](SOURCE.md) for source locations and release mapping.

Version 0.2.1 APK builds package these texts and expose them through **Settings → Open-source licenses**. This GitHub update does not change an already published APK. Existing dependency license metadata is retained alongside the readable notice bundle. The app uses the unmodified distributed Chaquopy/Python runtime; Android runtime adaptations originate in Chaquopy, linked from SOURCE.md.

## Artwork and names

The selected launcher artwork includes the BMW roundel. BMW names and logos remain their respective owners' marks; the software license does not license those marks. The project is independent and does not claim BMW endorsement. Artwork is unchanged; branding review is deferred as requested by the maintainer.

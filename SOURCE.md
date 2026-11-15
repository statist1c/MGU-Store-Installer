# Source code and release provenance

Project source and build files: https://github.com/statist1c/MGU-Store-Installer

## Published v0.2.0 APK

- File: `MGU-Store-Installer-v0.2.0.apk`
- SHA-256: `dad6d235c41137e4b236611cadb4f1d7b5ff6794a1aa4154d0e88f5d0c60ddb9`
- Application version: `0.2.0`; Android versionCode: `2`.
- Corresponding application source: [`ef8e1507fd097c415871d4502699cf2c3c9779a3`](https://github.com/statist1c/MGU-Store-Installer/tree/ef8e1507fd097c415871d4502699cf2c3c9779a3).
- [Download that source revision](https://github.com/statist1c/MGU-Store-Installer/archive/ef8e1507fd097c415871d4502699cf2c3c9779a3.zip).

The release asset digest was checked against the locally built APK when this record was added. Later README/license improvements do not change that binary. The source includes Java/Python code, retained upstream installer, resources, Gradle wrapper and build configuration. Build instructions are in `README.md`.

## Dependency sources

| Component | Source |
| --- | --- |
| mgu-store | https://github.com/robertnisipeanu/mgu-store/tree/fc5750a8474359ad20c1c01cf29d997ff7f2d621 |
| JSch 2.28.8 | https://github.com/mwiede/jsch/tree/jsch-2.28.8 |
| Bouncy Castle 1.87 | https://github.com/bcgit/bc-java/tree/r1rv87 |
| Chaquopy 17.2.0 runtime, Android patches and build scripts | https://github.com/chaquo/chaquopy/tree/17.2.0 |
| CPython 3.13.16 | https://github.com/python/cpython/tree/v3.13.16 |
| Python native dependency build recipes | https://github.com/beeware/cpython-android-source-deps |
| OpenSSL 3.5.9 | https://github.com/openssl/openssl/tree/openssl-3.5.9 |
| libffi 3.4.4 | https://github.com/libffi/libffi/tree/v3.4.4 |
| bzip2 1.0.8 | https://sourceware.org/pub/bzip2/bzip2-1.0.8.tar.gz |
| XZ 5.4.6 | https://github.com/tukaani-project/xz/tree/v5.4.6 |
| SQLite | https://sqlite.org/download.html |
| Gradle 8.9 | https://github.com/gradle/gradle/tree/v8.9.0 |

Embedded pyelftools/setuptools and libc++ notices are included in `LICENSES/`; their integration is retained in Chaquopy's runtime/build recipe. The project uses the cited Chaquopy Android distribution, not a custom unpublished Python fork.

## Later releases

For each APK release, retain its exact source revision and build configuration, provide a matching source archive or immutable source link alongside the APK, preserve `LICENSE`, `COPYRIGHT.md` and dependency notices, and record the final signed APK's SHA-256. Recheck resolved dependency versions and notice files when upgrading them.

Never include SSH private keys, signing keystores or tokens in public archives. This license update does not rebuild or replace existing release assets.

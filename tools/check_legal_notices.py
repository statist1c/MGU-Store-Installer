"""Check retained notice hashes and, optionally, their exact APK asset bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apk', type=Path)
    args = parser.parse_args()
    records = json.loads((ROOT / 'LICENSES/PROVENANCE.json').read_text(encoding='utf-8'))
    for item in records:
        data = (ROOT / 'LICENSES' / item['file']).read_bytes()
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            raise SystemExit('Notice hash differs: ' + item['file'])
    if args.apk:
        with zipfile.ZipFile(args.apk) as apk:
            paths = [ROOT / name for name in ('LICENSE', 'COPYRIGHT.md', 'THIRD_PARTY_NOTICES.md', 'SOURCE.md')]
            paths += list((ROOT / 'LICENSES').glob('*'))
            for path in paths:
                if path.is_file():
                    name = 'assets/legal/' + path.relative_to(ROOT).as_posix()
                    if apk.read(name) != path.read_bytes():
                        raise SystemExit('APK notice differs: ' + name)
    print('PASS: retained notice hashes' + (' and complete APK notice assets' if args.apk else ''))


if __name__ == '__main__':
    main()

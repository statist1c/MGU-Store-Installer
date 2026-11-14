"""Android port of upstream first-install, using the release's own deploy tool.

Only a published catalog is accepted. All artifacts require size and SHA-256.
Shell scripts in upstream_commands.json are copied verbatim from mgu-install.js.
"""
import hashlib
import io
import json
import os
import re
import tarfile
import time
import urllib.request
from pathlib import Path

REPO = 'https://api.github.com/repos/robertnisipeanu/mgu-store'
HERE = Path(__file__).parent
COMMANDS = json.loads((HERE / 'upstream_commands.json').read_text())
ID = re.compile(r'[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}\Z')
NAME = re.compile(r'[a-zA-Z0-9][a-zA-Z0-9._@+-]{0,220}\.tgz\Z')
MAX_ARTIFACT = 160 * 1024 * 1024

def download(url, maximum, dest=None, accept='application/octet-stream'):
    if not url.startswith('https://'):
        raise ValueError('Package downloads require HTTPS')
    req = urllib.request.Request(url, headers={'Accept': accept, 'User-Agent': 'MGU-Store-Installer/0.1'})
    with urllib.request.urlopen(req, timeout=45) as response:
        if not response.url.startswith('https://'):
            raise ValueError('Refused insecure redirect')
        out = open(dest, 'wb') if dest else io.BytesIO()
        try:
            size = 0
            while True:
                data = response.read(128 * 1024)
                if not data:
                    break
                size += len(data)
                if size > maximum:
                    raise ValueError('Download exceeds size limit')
                out.write(data)
            return None if dest else out.getvalue()
        finally:
            out.close()

def validate_catalog(catalog, renderer=True, uplink=True):
    if catalog.get('schema') not in (1, 2) or not isinstance(catalog.get('components'), list):
        raise ValueError('Unsupported catalog schema')
    chosen, seen = [], set()
    for entry in catalog['components']:
        cid = entry.get('id', '')
        if not ID.fullmatch(cid) or cid in seen:
            raise ValueError('Invalid or duplicate component ID')
        seen.add(cid)
        a = entry.get('artifact', {})
        if not NAME.fullmatch(a.get('name', '')) or not re.fullmatch(r'[a-fA-F0-9]{64}', a.get('sha256', '')):
            raise ValueError('Catalog lacks safe filename or SHA-256')
        if type(a.get('size')) is not int or not 0 < a['size'] <= MAX_ARTIFACT:
            raise ValueError('Invalid artifact size')
        if entry.get('kind') not in ('app', 'tool'):
            raise ValueError('Invalid component kind')
        if entry.get('optional') and not ((cid == 'mgu-render' and renderer) or (cid == 'mgu-uplink' and uplink)):
            continue
        chosen.append(entry)
    if 'mgu-deploy' not in {e['id'] for e in chosen}:
        raise ValueError('Catalog has no deploy tool')
    return chosen

def checked_file(path, artifact):
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        for data in iter(lambda: stream.read(128 * 1024), b''):
            digest.update(data)
    if os.path.getsize(path) != artifact['size'] or digest.hexdigest().lower() != artifact['sha256'].lower():
        raise ValueError('Checksum or size mismatch: ' + artifact['name'])

def deploy_files(path):
    with tarfile.open(path, 'r:gz') as archive:
        members = archive.getmembers()
        if len(members) > 2000 or sum(m.size for m in members) > MAX_ARTIFACT:
            raise ValueError('Oversized deploy archive')
        names = [m.name for m in members]
        if len(names) != len(set(names)):
            raise ValueError('Duplicate deploy members')
        def read(name):
            member = archive.getmember(name)
            if not member.isfile():
                raise ValueError('Deploy member is not a regular file')
            return archive.extractfile(member).read()
        raw = read('component.json')
        manifest = json.loads(raw)
        if manifest.get('id') != 'mgu-deploy' or not isinstance(manifest.get('files'), list):
            raise ValueError('Invalid deploy manifest')
        result = [('component.json', raw, 0o644)]
        used = {'component.json', 'run.sh', 'sources.json', 'artifacts', 'with'}
        for entry in manifest['files']:
            name = entry['path']
            if not ID.fullmatch(name) or name in used:
                raise ValueError('Unsafe deploy member')
            used.add(name)
            data = read('files/' + name)
            if hashlib.sha256(data).hexdigest() != entry['sha256']:
                raise ValueError('Deploy manifest checksum mismatch')
            mode = int(entry['mode'], 8)
            if mode & ~0o777:
                raise ValueError('Unsafe deploy mode')
            result.append((name, data, mode))
        if 'mgu-deploy.sh' not in used:
            raise ValueError('Missing deploy script')
        return result

def add_bytes(archive, name, data, mode=0o644):
    info = tarfile.TarInfo(name)
    info.size, info.mode, info.mtime = len(data), mode, int(time.time())
    archive.addfile(info, io.BytesIO(data))

def execute(ssh, command, path='', timeout=120):
    reply = json.loads(str(ssh.run(command, path, timeout)))
    if reply['rc'] != 0:
        raise RuntimeError('Remote command failed (%s): %s' % (reply['rc'], reply['err'][-2500:]))
    return reply['out']

def install(root, ssh, callback, renderer=True, uplink=True):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    say = lambda text: callback.onLine(str(text))
    say('Checking head-unit coding…')
    coding = execute(ssh, COMMANDS['coding']).strip()
    if coding in ('default', 'invalid'):
        raise RuntimeError('Head-unit coding is %s. Restore HU_MGU coding before installing.' % coding)
    if coding != 'ok':
        raise RuntimeError('Coding check did not return a recognized result; installation stopped.')
    say('Reading published catalog…')
    release = json.loads(download(REPO + '/releases/tags/catalog', 8 << 20, accept='application/vnd.github+json'))
    asset = next((a for a in release.get('assets', []) if a['name'] == 'catalog.json'), None)
    if not asset:
        raise ValueError('No published catalog.json. Use the upstream computer installer for older releases.')
    catalog = json.loads(download(asset['browser_download_url'], 4 << 20))
    chosen = validate_catalog(catalog, renderer, uplink)
    files = []
    try:
        for entry in chosen:
            artifact = entry['artifact']
            say('Downloading and verifying ' + artifact['name'])
            path = root / artifact['name']
            files.append(path)
            download(artifact['url'], artifact['size'], path)
            checked_file(path, artifact)
        kit = root / 'install-kit.tgz'
        files.append(kit)
        deploy = next(e for e in chosen if e['id'] == 'mgu-deploy')
        with tarfile.open(kit, 'w:gz') as archive:
            for name, data, mode in deploy_files(root / deploy['artifact']['name']):
                add_bytes(archive, name, data, mode)
            for entry in chosen:
                name = entry['artifact']['name']
                folder = 'with' if entry['id'] in ('mgu-render', 'mgu-uplink') else 'artifacts'
                archive.add(root / name, arcname=folder + '/' + name, recursive=False)
            add_bytes(archive, 'run.sh', COMMANDS['run'].encode(), 0o755)
            add_bytes(archive, 'sources.json', (HERE / 'sources.json').read_bytes())
        stage = '/var/opt/mgu-deploy-kit-android-' + str(time.time_ns())
        say('Uploading verified kit. Keep the phone connected and vehicle on stable power.')
        # Only the generated staging directory is removed. No supplied values enter shell text.
        command = ('umask 022 && mkdir -m 700 ' + stage + ' && tar -xzf - -C ' + stage +
                   ' && { sh ' + stage + '/run.sh; st=$?; rm -rf ' + stage + '; exit $st; }')
        execute(ssh, command, str(kit), 3600)
        say('Install command completed. Reading deploy status…')
        result = execute(ssh, 'sh /var/opt/mgu-deploy/mgu-deploy.sh status', timeout=180)
        say(result)
        say('Installation finished. Check the Store tile; restart the head unit from the Store if required. Hardware result is not independently verified by this app.')
        return result
    finally:
        for path in files:
            path.unlink(missing_ok=True)

def restart(ssh):
    return execute(ssh, COMMANDS['restart'])

import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / 'android/app/src/main/python'))
import installer

def entry(cid='mgu-deploy', optional=False):
    return dict(id=cid, kind='tool', version='1.0.0', optional=optional, artifact=dict(name=cid+'@1.0.0.tgz', size=3, sha256=hashlib.sha256(b'abc').hexdigest(), url='https://example.org/file'))

class InstallerTests(unittest.TestCase):
    def test_optional_selection(self):
        c=dict(schema=2, components=[entry(),entry('mgu-render',True),entry('mgu-uplink',True),entry('other',True)])
        self.assertEqual([e['id'] for e in installer.validate_catalog(c)],['mgu-deploy','mgu-render','mgu-uplink'])
        self.assertEqual([e['id'] for e in installer.validate_catalog(c,False,False)],['mgu-deploy'])

    def test_catalog_refuses_unsafe_or_unverified_packages(self):
        for field,value in [('name','../bad.tgz'),('sha256',None),('size',-1),('size',True)]:
            e=entry();e['artifact'][field]=value
            with self.subTest(field=field,value=value),self.assertRaises((ValueError,TypeError)):
                installer.validate_catalog(dict(schema=2,components=[e]))
        with self.assertRaises(ValueError):
            installer.validate_catalog(dict(schema=2,components=[entry(),entry()]))

    def test_checksum_and_size(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'a';path.write_bytes(b'abc')
            installer.checked_file(path,entry()['artifact'])
            path.write_bytes(b'abd')
            with self.assertRaises(ValueError):installer.checked_file(path,entry()['artifact'])

    def make_deploy(self,path,name='mgu-deploy.sh',payload=b'echo ok',hash_value=None):
        manifest=dict(id='mgu-deploy',files=[dict(path=name,mode='0755',sha256=hash_value or hashlib.sha256(payload).hexdigest())])
        with tarfile.open(path,'w:gz') as t:
            installer.add_bytes(t,'component.json',json.dumps(manifest).encode())
            installer.add_bytes(t,'files/'+name,payload)

    def test_deploy_members_checked_without_extracting(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'deploy.tgz';self.make_deploy(path)
            self.assertEqual(installer.deploy_files(path)[1][0],'mgu-deploy.sh')
            self.make_deploy(path,name='../escape')
            with self.assertRaises(ValueError):installer.deploy_files(path)
            self.make_deploy(path,hash_value='0'*64)
            with self.assertRaises(ValueError):installer.deploy_files(path)

    def test_invalid_coding_stops_before_download(self):
        class Ssh:
            def run(self,*args):return json.dumps(dict(rc=0,out='default',err=''))
        class Log:
            def onLine(self,line):pass
        with tempfile.TemporaryDirectory() as d,self.assertRaisesRegex(RuntimeError,'coding'):
            installer.install(d,Ssh(),Log())

    def test_failure_is_not_reported_as_success(self):
        class Ssh:
            def run(self,*args):return json.dumps(dict(rc=2,out='',err='refused'))
        with self.assertRaisesRegex(RuntimeError,'refused'):
            installer.execute(Ssh(),'status')

    def test_component_identity_and_filename_must_agree(self):
        for name, version in [('other@1.0.0.tgz', '1.0.0'), ('mgu-deploy@2.0.0.tgz', '1.0.0'), ('mgu-deploy@1.0.0.tgz', '')]:
            e = entry(); e['version'] = version; e['artifact']['name'] = name
            with self.subTest(name=name, version=version), self.assertRaises(ValueError):
                installer.validate_catalog(dict(schema=2, components=[e]))

    def test_restart_refusal_even_with_success_exit(self):
        class Ssh:
            def run(self, *args): return json.dumps(dict(rc=0, out='[Error. restart refused]', err=''))
        with self.assertRaisesRegex(RuntimeError, 'restart refused'):
            installer.restart(Ssh())

    def test_restart_install_lock_and_normal_success(self):
        class Ssh:
            rc = 3
            def run(self, *args): return json.dumps(dict(rc=self.rc, out='', err=''))
        ssh = Ssh()
        with self.assertRaisesRegex(RuntimeError, 'install is running'): installer.restart(ssh)
        ssh.rc = 0
        self.assertEqual(installer.restart(ssh), '')

    def test_status_id7_fallback_and_service_checks(self):
        state = dict(unit=dict(hmi='ID7'), components=[dict(id='robertn_store',kind='app')], fallback=dict(apps=['robertn_store'], manager_runs_copy=False))
        self.assertEqual(installer.assess_status('active\n' + json.dumps(state), ['mgu-updater'])['state'], 'restart-required')
        state['fallback']['manager_runs_copy'] = True
        self.assertEqual(installer.assess_status('active\n' + json.dumps(state), ['mgu-updater'])['state'], 'ready')
        self.assertEqual(installer.assess_status('failed\n' + json.dumps(state), ['mgu-updater'])['state'], 'restart-required')
        state['fallback'].update(manager_runs_copy=False, refused='coding unavailable')
        self.assertEqual(installer.assess_status('active\n' + json.dumps(state), ['mgu-updater'])['state'], 'blocked')

    def test_status_id8_requires_store_tile(self):
        state = dict(unit=dict(hmi='ID8'), components=[dict(id='robertn_store',kind='app',tile_visible=False)],
                     fallback=dict(active=True, listed_by_manager=False, apps=[]))
        self.assertFalse(installer.tiles_show(state)['shown'])
        state['components'][0]['tile_visible'] = True
        self.assertTrue(installer.tiles_show(state)['shown'])
        state['components'][0]['tile_visible'] = False
        state['fallback']['active'] = False
        state['live_installs'] = dict(reason='off: provisioning refused')
        self.assertEqual(installer.tiles_show(state)['why'], 'provisioning refused')

    def test_incomplete_or_invalid_status_is_not_ready(self):
        for lines in ['', 'active', 'active\nnot-json', 'active\n[]', 'active\n{}', 'active\n{"unit":{"hmi":"ID7"},"components":[]}']:
            with self.subTest(lines=lines):
                self.assertEqual(installer.assess_status(lines, ['mgu-updater'])['state'], 'unknown')

    def test_install_kit_uses_upstream_cleanup_name_and_returns_readiness(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / 'source.tgz'; self.make_deploy(source)
            payload = source.read_bytes()
            e = entry(); e['artifact'].update(size=len(payload), sha256=hashlib.sha256(payload).hexdigest())
            catalog = dict(schema=2, components=[e])
            state = dict(unit=dict(hmi='ID7'), components=[dict(id='robertn_store',kind='app')],
                         fallback=dict(apps=['robertn_store'],manager_runs_copy=True))
            class Ssh:
                transferred = False
                def run(self, command, path, timeout):
                    if command == installer.COMMANDS['coding']: out = 'ok'
                    elif path:
                        self.transferred = True
                        self_case.assertRegex(command, r'/var/opt/mgu-deploy-kit-[0-9]+(?: |/)')
                        self_case.assertNotIn('mgu-deploy-kit-android-', command)
                        with tarfile.open(path) as archive:
                            self_case.assertIn('mgu-deploy.sh', archive.getnames())
                            self_case.assertIn('artifacts/mgu-deploy@1.0.0.tgz', archive.getnames())
                        out = ''
                    else: out = 'active\n' + json.dumps(state) + '\n'
                    return json.dumps(dict(rc=0,out=out,err=''))
            class Log:
                def onLine(self, line): pass
            def download(url, maximum, dest=None, **kwargs):
                if dest: Path(dest).write_bytes(payload); return None
                if url.endswith('/releases/tags/catalog'):
                    return json.dumps(dict(assets=[dict(name='catalog.json',browser_download_url='https://example.org/catalog')])).encode()
                return json.dumps(catalog).encode()
            self_case = self; ssh = Ssh()
            with patch.object(installer, 'download', side_effect=download):
                result = json.loads(installer.install(str(Path(d)/'kit'), ssh, Log()))
            self.assertTrue(ssh.transferred)
            self.assertEqual(result['state'], 'ready')
            self.assertEqual(list((Path(d)/'kit').iterdir()), [])

if __name__=='__main__':unittest.main()

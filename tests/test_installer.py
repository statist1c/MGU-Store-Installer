import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / 'android/app/src/main/python'))
import installer

def entry(cid='mgu-deploy', optional=False):
    return dict(id=cid, kind='tool', optional=optional, artifact=dict(name=cid+'@1.0.0.tgz', size=3, sha256=hashlib.sha256(b'abc').hexdigest(), url='https://example.org/file'))

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

if __name__=='__main__':unittest.main()

"""Verify current public packages and kit layout; no head unit is contacted."""
import sys, tempfile, json, tarfile, shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / 'android/app/src/main/python'))
import installer
class Log:
 def onLine(self,x): print(x,flush=True)
class Ssh:
 def run(self,command,path,timeout):
  if command==installer.COMMANDS['coding']:return json.dumps(dict(rc=0,out='ok',err=''))
  if path:
   with tarfile.open(path) as t:
    ns=t.getnames()
    assert 'mgu-deploy.sh' in ns and 'sources.json' in ns and 'run.sh' in ns
    assert sum(n.startswith('artifacts/') for n in ns)>0
    assert t.extractfile('run.sh').read().decode()==installer.COMMANDS['run']
    print('VERIFIED KIT: '+str(len(ns))+' members, '+str(Path(path).stat().st_size)+' bytes',flush=True)
   return json.dumps(dict(rc=0,out='MOCK remote command, no head unit contacted',err=''))
  return json.dumps(dict(rc=0,out='MOCK status',err=''))
with tempfile.TemporaryDirectory() as root:installer.install(root,Ssh(),Log())

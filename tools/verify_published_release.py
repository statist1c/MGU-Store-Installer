"""Verify current public packages and kit layout; no head unit is contacted."""
import sys, tempfile, json, tarfile, shutil
import re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / 'android/app/src/main/python'))
import installer
class Log:
 def onLine(self,x): print(x,flush=True)
class Ssh:
 def run(self,command,path,timeout):
  if command==installer.COMMANDS['coding']:return json.dumps(dict(rc=0,out='ok',err=''))
  if path:
   assert re.search(r'/var/opt/mgu-deploy-kit-[0-9]+(?: |/)', command)
   with tarfile.open(path) as t:
    ns=t.getnames()
    assert 'mgu-deploy.sh' in ns and 'sources.json' in ns and 'run.sh' in ns
    assert sum(n.startswith('artifacts/') for n in ns)>0
    assert t.extractfile('run.sh').read().decode()==installer.COMMANDS['run']
    print('VERIFIED KIT: '+str(len(ns))+' members, '+str(Path(path).stat().st_size)+' bytes',flush=True)
   return json.dumps(dict(rc=0,out='MOCK remote command, no head unit contacted',err=''))
  state=dict(unit=dict(hmi='ID7'),components=[dict(id='robertn_store',kind='app')],fallback=dict(apps=['robertn_store'],manager_runs_copy=True))
  services=1+len(re.findall(r'systemctl is-active mgu-(?:render|uplink)',command))
  return json.dumps(dict(rc=0,out='active\n'*services+json.dumps(state),err=''))
with tempfile.TemporaryDirectory() as root:
 result=json.loads(installer.install(root,Ssh(),Log()))
 assert result['state']=='ready'
 print('PASS: live package verification, cleanup-compatible staging and mocked ready state')

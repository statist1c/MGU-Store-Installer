"""Compare Android command data and tile logic with the retained upstream installer."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'android/app/src/main/python'))
import installer

cases = [
    {},
    dict(unit=dict(hmi='ID7'), fallback=dict(apps=[])),
    dict(unit=dict(hmi='ID7'), fallback=dict(apps=['robertn_store'], manager_runs_copy=False)),
    dict(unit=dict(hmi='ID7'), fallback=dict(apps=['robertn_store'], manager_runs_copy=True)),
    dict(unit=dict(hmi='ID7'), fallback=dict(apps=['robertn_store'], manager_runs_copy=False, refused='coding missing')),
    dict(unit=dict(hmi='ID7'), retired_leftovers=['old-app'], fallback=dict(apps=['old-app'], manager_runs_copy=False)),
]
for active in (False, True):
    for visible in (False, True):
        cases.append(dict(unit=dict(hmi='ID8'), fallback=dict(active=active, listed_by_manager=False, apps=[]),
                          components=[dict(id='robertn_store',kind='app',tile_visible=visible)], live_installs=dict(reason='off: disabled')))

script = r'''
const fs = require('fs'), Module = require('module');
const filename = process.argv[1], m = new Module(filename);
m.filename = filename; m.paths = module.paths;
m._compile(fs.readFileSync(filename, 'utf8') + '\nmodule.exports.androidCommands = {run:RUN_SH,coding:CODING_CHECK,restart:RESTART};', filename);
const cases = JSON.parse(fs.readFileSync(0, 'utf8'));
console.log(JSON.stringify({commands:m.exports.androidCommands,sources:m.exports.SOURCES,tiles:cases.map(c=>m.exports.tilesShow(JSON.stringify(c)))}));
'''
result = subprocess.run(['node', '-e', script, str(ROOT/'vendor/mgu-install.js')],
                        input=json.dumps(cases), text=True, capture_output=True, check=True)
upstream = json.loads(result.stdout)
assert upstream['commands'] == installer.COMMANDS, 'Copied upstream command data differs'
assert upstream['sources'] == json.loads((installer.HERE/'sources.json').read_text()), 'Source seed differs'
for case, expected in zip(cases, upstream['tiles']):
    actual = installer.tiles_show(case)
    assert actual['shown'] == expected.get('shown') and actual['why'] == expected.get('why'), case
print('PASS: upstream commands, source seed and 10 ID7/ID8 tile-status cases')

"""Compare saved actual API sessions; do not replace replay with static inspection."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
b=json.loads((root/'review/archive/2026-10-07/depth-cycle15-dialogue-before.json').read_text());a=json.loads((root/'review/archive/2026-10-07/depth-cycle15-dialogue-after.json').read_text())
assert (b['moves'],len(b['events']))==(a['moves'],len(a['events']))
for key in ['seals','hp','fatigue','xp','level','equipment','attributes']:assert b['final']['character'][key]==a['final']['character'][key],key
assert b['final']['inventory']==a['final']['inventory']
for before in b['checks']:
 if before['stage'] in ['initial','first_report']:
  after=next(row for row in a['checks'] if (row['npc'],row['topic'],row['stage'])==(before['npc'],before['topic'],before['stage']))
  assert (before['available'],before['narrative'])==(after['available'],after['narrative']),(before['npc'],before['stage'])
privates=['edran_daro','hoshai_daren','hoshai_luma','korven_taren','korven_ruma','veyra_seli','veyra_tov','veyra_nera','veyra_arel']
for npc in privates:
 before=next(row for row in b['checks'] if row['npc']==npc and row['stage']=='observer');after=next(row for row in a['checks'] if row['npc']==npc and row['stage']=='observer');assert (before['available'],before['narrative'])==(after['available'],after['narrative']),npc
for npc in ['edran_bren','edran_iria']:
 worker=next(row for row in a['checks'] if row['npc']==npc and row['stage']=='resolved');observer=next(row for row in a['checks'] if row['npc']==npc and row['stage']=='observer');assert worker['narrative'][0]==observer['narrative'][0],npc
changed=[]
for before in b['checks']:
 if before['stage'] in ['paid','resolved']:
  after=next(row for row in a['checks'] if (row['npc'],row['topic'],row['stage'])==(before['npc'],before['topic'],before['stage']))
  if before['narrative']!=after['narrative']:changed.append([before['npc'],before['topic']])
assert len(changed)==11,changed
report={'sameMoves':a['moves'],'sameActions':len(a['events']),'sameFinalSeals':a['final']['character']['seals'],'sameEconomyEquipmentAndRecovery':True,'initialEffectsAndInstructionsPreserved':True,'privateObserverResponsesUnchanged':privates,'sharedPhysicalResponsesConsistent':['edran_bren','edran_iria'],'changedResolvedTopics':changed}
(root/'review/archive/2026-10-07/depth-cycle15-dialogue-comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))

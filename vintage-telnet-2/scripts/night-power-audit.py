"""Compare real round mechanics using isolated, explicitly authored state inputs."""
import sys,json,copy
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from server import mechanics as m
class Fixed:
 def __init__(self,value):self.value=value
 def random(self):return self.value

def sample(cls,action,roll=.4):
 s=m.new_state('humano',cls,'isolated',0);s['_class']=cls;s['combat']={'profile':dict(m.PROFILES['espinajo_rastrojo']),'hp':40,'prepared':True,'round':0,'cooldown':0,'intervention':{'id':action}}
 events,outcome=m.resolve_round(s,{'name':'Espinajo'},Fixed(roll));combat=s['combat']
 return s,{'action':action,'outgoingDamage':40-combat['hp'],'incomingDamage':100-s['hp'],'fatigue':s['fatigue'],'enemyResponseAccuracy':combat['_response']['accuracy'],'guard':combat['_response']['guard'],'opening':combat.get('opening',False),'cooldown':combat['cooldown'],'events':events,'outcome':outcome}
results={}
for cls in m.CLASSES:
 s,power=sample(cls,'capacidad');_,attack=sample(cls,'atacar');results[cls]={'baselineAttack':attack,'signature':power}
s,_=sample('sombra','capacidad');s['combat']['intervention']={'id':'atacar'};m.resolve_round(s,{'name':'Espinajo'},Fixed(.66));_,normal=sample('sombra','atacar',.66)
results['sombra']['openingNextAttack']={'damageWithOpening':40-s['combat']['hp'],'damageWithoutOpening':normal['outgoingDamage'],'openingConsumed':not s['combat'].get('opening',False)}
results['levelOneDefenses']={a:sample('juramentado',a)[1] for a in ('atacar','esquivar','bloquear','resistir')}
assert results['arcano']['signature']['enemyResponseAccuracy']==40
assert results['juramentado']['signature']['incomingDamage']<results['juramentado']['baselineAttack']['incomingDamage']
assert results['sombra']['openingNextAttack']['damageWithOpening']>results['sombra']['openingNextAttack']['damageWithoutOpening']
assert results['artifice']['signature']['outgoingDamage']>0
out={'status':'PASS','scope':'Deterministic actual round comparison, not human play or new balance approval','sources':['GAMEPLAY §§20.5,36.4–36.7','CLASS_SIGNATURE_CANON_RECONCILIATION.md'],'results':results}
(root/'review/night-playtest/power-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print('PASS powers compared; arcano response accuracy',results['arcano']['signature']['enemyResponseAccuracy'])

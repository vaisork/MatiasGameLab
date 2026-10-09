"""Minor fauna of Lethra and Nhal (PR #669): catalogue, risk tiers, habitats, warnings, loot and art requests."""
import json,unittest,collections
from pathlib import Path
from server.content import Content
from server.engine import Engine
from server import mechanics as m

ROOT=Path(__file__).resolve().parents[1]
EXISTING=('pinzajunco','saltalodo','rondamusgo','hilaria_niebla')

class Zero:
 def random(self):return 0

class FaunaLethraNhal(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.content=Content(ROOT/'content')
 def pools(self,cid):return [rid for rid,r in self.content.rooms.items() if any(s['creature']==cid for s in r.get('wildlife_pool',[]))]

 def test_sixteen_new_species_in_three_risk_tiers(self):
  self.assertEqual(len(m.MINOR_FAUNA),16)
  tiers=collections.Counter(m.PROFILES[c]['category'] for c in m.MINOR_FAUNA)
  self.assertEqual(tiers,{'favorable':3,'comparable':7,'peligroso':6})
  for cid in m.MINOR_FAUNA:
   creature=self.content.creatures[cid]
   for key in ('description','warning','combat_intro','defeat_text','presagio'):self.assertTrue(creature.get(key),(cid,key))
   self.assertTrue(creature['loot'] and all(d['item'] in self.content.items for d in creature['loot']),cid)
   self.assertTrue(m.CREATURE_PROSE[cid]['hit'] and m.CREATURE_PROSE[cid]['miss'],cid)
   self.assertTrue(m.threat_observation(cid),cid)

 def test_every_species_lives_in_its_region_and_never_in_towns(self):
  towns={r['settlement'] for r in self.content.regions.values()}
  for cid in (*m.MINOR_FAUNA,*EXISTING):
   rooms=self.pools(cid);self.assertGreaterEqual(len(rooms),1,cid)
   for rid in rooms:
    room=self.content.rooms[rid]
    self.assertEqual(room['region'],self.content.creatures[cid]['region'],(cid,rid))
    self.assertNotIn(rid,towns);self.assertNotIn(room['kind'],('settlement','interior','home'))

 def test_existing_species_stay_non_combatant(self):
  for cid in EXISTING:self.assertNotIn(cid,m.PROFILES)
  self.assertNotIn('hilaria_niebla',m.MINOR_FAUNA)

 def test_nocturnal_species_only_appear_without_daylight(self):
  for cid in ('sombranutria','velomembrana'):
   for r in self.content.rooms.values():
    for s in r.get('wildlife_pool',[]):
     if s['creature']==cid:self.assertNotIn('día',s.get('requires_time',[]));self.assertTrue(s.get('requires_time'))

 def test_predators_warn_before_combat_and_can_be_avoided(self):
  now=12*3600;engine=Engine(self.content,lambda:now,Zero())
  state=m.new_state('vesperi','juramentado','home:1',now);state['location']='nhal_claro_silencio'
  char={'id':1,'name':'Prueba','species':'vesperi','class_id':'juramentado','state':state};world={'flags':[],'deaths':{},'version':0}
  world['wildlife']={'nhal_claro_silencio':{'signal':next(s for s in self.content.rooms['nhal_claro_silencio']['wildlife_pool'] if s['creature']=='tronchacolmillo'),'until':now+300}}
  ids=lambda:[(a['id'],a.get('target')) for a in engine.actions(char,world)]
  self.assertIn(('acercarse','tronchacolmillo'),ids());self.assertNotIn(('combatir','tronchacolmillo'),ids())
  engine.apply(char,world,{'id':'acercarse','target':'tronchacolmillo'})
  self.assertIn(('combatir','tronchacolmillo'),ids());self.assertIn(('retirarse','tronchacolmillo'),ids())

 def test_victory_tells_the_flight_and_leaves_regional_loot(self):
  now=12*3600;engine=Engine(self.content,lambda:now,Zero())
  state=m.new_state('marevyn','juramentado','home:1',now);state['location']='lethra_raices_observacion'
  char={'id':1,'name':'Prueba','species':'marevyn','class_id':'juramentado','state':state};world={'flags':[],'deaths':{},'version':0}
  profile=m.scaled(m.PROFILES['cienfango'],2);state['combat']={'creature':'cienfango','profile':profile,'hp':0,'round':1,'prepared':False,'cooldown':0}
  engine.victory(char,world,state['combat'],self.content.creatures['cienfango'])
  texts=[e['text'] for e in state['events']]
  self.assertIn(self.content.creatures['cienfango']['defeat_text'],texts)
  self.assertTrue(any(i.get('id')=='placa_cienfango' for i in state['inventory']))

 def test_art_requests_cover_all_twenty_species(self):
  data=json.loads((ROOT/'docs/colaboracion/arte-criaturas/SOLICITUDES_CRIATURAS.json').read_text(encoding='utf-8'))['solicitudes']
  self.assertTrue(all(r['tipo']=='creature' for r in data))
  self.assertEqual({r['id'] for r in data if r['encargo']=='ambiente'},{*m.MINOR_FAUNA,*EXISTING})
  self.assertEqual({r['id'] for r in data if r['encargo']=='ficha'},set(m.MINOR_FAUNA))

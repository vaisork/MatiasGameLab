import unittest
from pathlib import Path
from server import mechanics as m
from server.content import Content
from server.engine import Engine,RuleError
class FixedRandom:
 def random(self):return 0
class PostVictoryTests(unittest.TestCase):
 def setUp(self):
  self.now=43200;self.e=Engine(Content(Path(__file__).resolve().parents[1]/'content'),lambda:self.now,FixedRandom());self.s=m.new_state('humano','juramentado','home:test',self.now);self.s['location']='edran_surcos';self.s['visited'].append('edran_surcos');self.s['known'].append('edran_surcos');self.s['visits']['edran_surcos']=1;self.char={'id':999,'name':'Prueba','species':'humano','class_id':'juramentado','state':self.s};self.world={'flags':[],'deaths':{},'weather':{}}
 def test_real_victory_removes_live_actions_and_motion_until_respawn(self):
  self.e.apply(self.char,self.world,{'id':'mirar'});self.assertTrue(any(a['id']=='evaluar' for a in self.e.actions(self.char,self.world)))
  self.e.apply(self.char,self.world,{'id':'combatir','target':'espinajo_rastrojo'})
  for _ in range(12):
   self.now+=4;self.e.tick(self.char,self.world)
   if not self.s['combat']:break
  self.assertIn('espinajo',self.s['victories']);self.assertGreater(self.s['xp'],0)
  self.assertFalse(any(a['target']=='espinajo_rastrojo' for a in self.e.actions(self.char,self.world) if 'target' in a and a['id'] in ('evaluar','combatir','acercarse','examinar_criatura')))
  with self.assertRaises(RuleError):self.e.apply(self.char,self.world,{'id':'evaluar','target':'espinajo_rastrojo'})
  self.e.apply(self.char,self.world,{'id':'observar'});text=' '.join(e['text'] for e in self.s['events']);self.assertNotIn('Un movimiento bajo los tallos',text);self.assertIn('No hay movimiento',text)
  self.assertIn('ya no se mueven',self.e.room(self.char,self.world)['day'])
  self.now=self.world['deaths']['edran_surcos:espinajo_rastrojo']+1
  self.assertTrue(any(a['id']=='evaluar' and a.get('target')=='espinajo_rastrojo' for a in self.e.actions(self.char,self.world)))
  self.assertIn('se doblan contra el viento',self.e.room(self.char,self.world)['day'])
 def test_persistent_trace_does_not_allow_evaluating_absent_creature(self):
  self.s['bestiary']['espinajo_rastrojo']={'id':'espinajo_rastrojo'};self.e.content.rooms['edran_surcos']['signals'][0]['persistent_trace']=True;self.world['deaths']['edran_surcos:espinajo_rastrojo']=self.now+300
  self.assertFalse(any(a['id']=='evaluar' for a in self.e.actions(self.char,self.world)))
  self.world['deaths'].clear();self.world['creature_states']={'edran_surcos:espinajo_rastrojo':{'stage':'sheltered'}}
  self.assertFalse(any(a['id']=='evaluar' for a in self.e.actions(self.char,self.world)))
 def test_evaluation_uses_actual_levels_for_advanced_player(self):
  self.s['level']=30;self.e.apply(self.char,self.world,{'id':'mirar'});self.e.apply(self.char,self.world,{'id':'evaluar','target':'espinajo_rastrojo'});text=self.s['events'][0]['text'];self.assertIn('nivel 2',text);self.assertIn('Tu nivel: 30',text);self.assertNotIn('primera formación',text)

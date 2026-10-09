"""MUD loop: body armour, accessories, potions in combat, loot, rival levels, dead-end finds and secret passages."""
import unittest
from pathlib import Path
from server.content import Content
from server.engine import Engine
from server import mechanics as m

class Zero:
 def random(self):return 0

class CicloMud(unittest.TestCase):
 def setUp(self):
  self.content=Content(Path(__file__).resolve().parents[1]/'content');self.now=12*3600
  self.engine=Engine(self.content,lambda:self.now,Zero())
  self.state=m.new_state('humano','juramentado','home:1',self.now);self.state['seals']=2000
  self.char={'id':1,'name':'Prueba','species':'humano','class_id':'juramentado','state':self.state};self.world={'flags':[],'deaths':{},'version':0}
 def act(self,id,target=None,**kw):self.engine.apply(self.char,self.world,dict(id=id,target=target,**kw))
 def ids(self):return [(a['id'],a.get('target')) for a in self.engine.actions(self.char,self.world)]

 def test_every_body_part_adds_protection_up_to_the_cap(self):
  self.state['location']='vaisgard_mercado'
  for piece in ('yelmo_vaisgard','coraza_vaisgard','guanteletes_vaisgard','quijotes_vaisgard','botas_vaisgard','amuleto_raiz'):
   self.act('comprar',piece);self.act('equipar',piece)
  self.assertAlmostEqual(self.state['armor_reduction'],.42)
  self.assertEqual(m.hp_max(self.state),120)
  self.state['equipment']['armor']='legacy';self.assertLessEqual(m.armor_total(self.state),m.ARMOR_CAP)
  self.act('desequipar','torso');self.assertAlmostEqual(self.state['armor_reduction'],.28)

 def test_potion_can_be_drunk_as_a_combat_round(self):
  self.state['location']='vaisgard_mercado';self.act('comprar','pocion_vida')
  self.state['hp']=30;self.state['combat']={'creature':'espinajo_rastrojo','profile':m.scaled(m.PROFILES['espinajo_rastrojo'],1),'hp':40,'round':0,'next_round':self.now,'prepared':False,'cooldown':0,'intervention':{'id':'usar','target':'pocion_vida'}}
  self.state['_class']='juramentado'
  events,_=m.resolve_round(self.state,self.content.creatures['espinajo_rastrojo'],Zero(),respond=False)
  self.assertGreater(self.state['hp'],30);self.assertFalse(any(i['id']=='pocion_vida' for i in self.state['inventory']))
  self.assertIn('Usas Poción de vida',events[0]['text'])

 def test_levels_make_the_same_creature_harder(self):
  low,high=m.scaled(m.PROFILES['espinajo_rastrojo'],2),m.scaled(m.PROFILES['espinajo_rastrojo'],5)
  self.assertLess(low['hp'],high['hp']);self.assertLess(low['damage'],high['damage']);self.assertEqual(high['level'],5)
  self.assertEqual(m.scaled(m.PROFILES['cornalomo'],5),m.PROFILES['cornalomo'])

 def test_every_rival_creature_leaves_loot(self):
  for cid,profile in m.PROFILES.items():
   loot=self.content.creatures[cid].get('loot')
   self.assertTrue(loot,cid);self.assertTrue(all(d['item'] in self.content.items for d in loot),cid)

 def test_dead_end_rewards_once_and_reveals_its_passage(self):
  self.state['location']='edran_canal_repisa'
  self.assertNotIn(('pasaje_conducto_zanja',None),self.ids())
  self.act('buscar');self.assertTrue(any(i.get('catalog_id',i['id'])=='anillo_filo' for i in self.state['inventory']))
  self.assertIn(('pasaje_conducto_zanja',None),self.ids())
  self.act('pasaje_conducto_zanja');self.assertEqual(self.state['location'],'edran_zanja_antigua')
  self.assertIn(('pasaje_conducto_zanja_vuelta',None),self.ids())
  self.state['location']='edran_canal_repisa';self.state['searches']={};self.act('buscar')
  self.assertEqual(sum(1 for i in self.state['inventory'] if i.get('catalog_id',i['id'])=='anillo_filo'),1)

 def test_vaisgard_sells_every_tier_and_buys_loot(self):
  shop=self.content.rooms['vaisgard_mercado']['shop']
  for item in ('pocion_menor','coraza_vaisgard','espada_vaisgard','anillo_filo','botas_cuero'):self.assertIn(item,shop)
  self.state['location']='vaisgard_mercado';self.engine.add_item(self.state,'cuerno_cornalomo')
  self.assertIn(('vender','cuerno_cornalomo'),self.ids())

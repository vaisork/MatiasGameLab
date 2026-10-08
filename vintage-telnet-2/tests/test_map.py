"""Map knowledge and real directions through authenticated requests."""
import json
from pathlib import Path
import unittest
import test_engine as fixtures

class MapTests(unittest.TestCase):
 setUp=fixtures.JourneyTests.setUp
 post=fixtures.JourneyTests.post
 create=fixtures.JourneyTests.create
 action=fixtures.JourneyTests.action
 def test_home_frontier_has_no_hidden_destination(self):
  self.create();state=self.client.get('/api/state').json;map=state['map']
  self.assertEqual(len(map['nodes']),1);self.assertEqual(map['routes'],[])
  self.assertEqual(map['frontiers'],[{'from':state['room']['id'],'direction':'salir'}])
  self.assertNotIn('secret',json.dumps(map))
  self.assertTrue(all(set(e)=={'from','direction'} for e in map['frontiers']))
 def test_learned_home_return_and_unwalked_field(self):
  self.create();home=self.client.get('/api/state').json['room']['id'];state=self.action('mover','salir');map=state['map']
  self.assertIn({'from':home,'to':'town','direction':'salir'},map['routes'])
  self.assertIn({'from':'town','to':home,'direction':'hogar'},map['routes'])
  self.assertEqual(map['frontiers'],[{'from':'town','direction':'norte'}])
  home_node=next(n for n in map['nodes'] if n['id']==home)
  self.assertEqual(home_node['kind'],'home');self.assertNotEqual(home_node['name'],state['room']['name'])
  self.assertNotIn('field',json.dumps(map))
  town_node=next(n for n in map['nodes'] if n['id']=='town')
  self.assertEqual(town_node['unexplored_directions'],['norte'])
  self.action('mover','hogar');self.post(self.client,'/api/account/logout',{})
  self.post(self.client,'/api/account/login',{'username':'tester','password':'testpass123'})
  restored=self.client.get('/api/state').json
  self.assertEqual(restored['room']['id'],home)
  self.assertEqual(restored['map']['routes'],map['routes'])
 def test_reverse_direction_comes_from_actual_exit(self):
  p=Path(self.temp.name)/'content/world.json';d=json.loads(p.read_text());d['rooms']['field']['exits']={'oeste':'town'};p.write_text(json.dumps(d))
  self.create();self.action('mover','salir');state=self.action('mover','norte');routes=state['map']['routes']
  self.assertIn({'from':'town','to':'field','direction':'norte'},routes)
  self.assertIn({'from':'field','to':'town','direction':'oeste'},routes)
  self.assertNotIn({'from':'field','to':'town','direction':'sur'},routes)
  returned=self.action('mover','oeste');self.assertEqual(returned['room']['id'],'town')
 def test_one_way_exit_does_not_create_a_return_route(self):
  p=Path(self.temp.name)/'content/world.json';d=json.loads(p.read_text());d['rooms']['field']['exits']={};p.write_text(json.dumps(d))
  self.create();self.action('mover','salir');state=self.action('mover','norte')
  self.assertFalse(any(r['from']=='field' and r['to']=='town' for r in state['map']['routes']))
  self.assertEqual(state['map']['frontiers'],[])

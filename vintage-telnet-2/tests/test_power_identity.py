"""Distinct numerical responses and visible consequences for the four class powers."""
import unittest
from server import mechanics as m
import test_engine as fixtures

class PowerIdentityTests(unittest.TestCase):
 def test_four_powers_keep_different_effects_and_explain_them(self):
  results={}
  for cls in m.CLASSES:
   state=m.new_state('humano',cls,'home',0);state['_class']=cls
   state['combat']={'profile':dict(m.PROFILES['espinajo_rastrojo']),'hp':40,'prepared':True,'round':0,'cooldown':0,'intervention':{'id':'capacidad'}}
   lines,outcome=m.resolve_round(state,{'name':'Espinajo'},fixtures.FixedRandom(),respond=False)
   self.assertEqual(outcome,'ongoing');self.assertTrue(any(m.CLASSES[cls]['signature'] in line['text'] and len(line['text'])>len(m.CLASSES[cls]['signature'])+15 for line in lines))
   results[cls]=state['combat']
  self.assertGreater(results['juramentado']['_response']['guard'],0)
  self.assertFalse(results['arcano']['prepared']);self.assertLess(results['arcano']['_response']['accuracy'],60)
  self.assertLess(results['sombra']['_response']['accuracy'],results['arcano']['_response']['accuracy'])
  self.assertLess(results['artifice']['hp'],40);self.assertFalse(results['artifice']['prepared'])

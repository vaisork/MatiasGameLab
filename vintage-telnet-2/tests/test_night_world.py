"""Authored campaign invariants: real exits, bounded rewards, local contacts."""
import unittest
from pathlib import Path
from server.content import Content

class NightWorld(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.world=Content(Path(__file__).resolve().parents[1]/'content')

    def test_two_dungeons_return_to_same_route_and_offer_pacifist_paths(self):
        w=self.world
        for entrance,outside,objective in [('edran_canal_entrada','edran_zanja_antigua','edran_canal_repisa'),('korven_almacen_entrada','korven_peldanos_cortos','korven_almacen_fondo')]:
            self.assertIn(entrance,w.rooms[outside]['exits'].values())
            self.assertIn(outside,w.rooms[entrance]['exits'].values())
            visited={entrance};todo=[entrance]
            while todo:
                rid=todo.pop()
                for dest in w.rooms[rid]['exits'].values():
                    if dest not in visited:visited.add(dest);todo.append(dest)
            self.assertIn(objective,visited)
        self.assertEqual(w.creatures['forajido_camino']['combatant_kind'],'human')
        self.assertNotIn('material',w.creatures['forajido_camino'])
        self.assertTrue(self.world.rooms['edran_canal_compuerta']['actions'][0]['next'])
        self.assertTrue(self.world.rooms['korven_almacen_cruce']['actions'][0]['next'])

    def test_quest_objects_cannot_be_resold_and_rewards_cannot_be_repeated(self):
        for item in ['caja_cunas','placa_balanza']:
            self.assertEqual(self.world.items[item]['kind'],'quest')
            self.assertNotIn('sell_price',self.world.items[item])
        for rid in ['edran_canal_repisa','korven_almacen_fondo','edran_canal_entrada','korven_almacen_entrada']:
            for action in self.world.rooms[rid]['actions']:
                if action.get('give_items'):
                    self.assertTrue(action['forbids_flags'])
                    self.assertTrue(set(action['forbids_flags']) & set(action['set_flags']))
                    self.assertFalse(action.get('seals'))

    def test_local_merchants_remain_at_one_authored_location(self):
        for merchant in ['hoshai_luma','lethra_nera_mercado','nhal_varo','veyra_bela','edran_nela','korven_ruma']:
            rooms=[rid for rid,r in self.world.rooms.items() if merchant in r.get('npcs',[])]
            self.assertEqual(rooms,[self.world.npcs[merchant]['home_room']])
        for rid, room in self.world.rooms.items():
            for service in ['buyer', 'forge_service']:
                if room.get(service):
                    self.assertEqual(self.world.npcs[room[service]]['home_room'], rid)
                    self.assertIn(room[service], room['npcs'])
        for region in ['hoshai','lethra','nhal','veyra']:
            self.assertTrue(any(r.get('shop') and r.get('buyer') for r in self.world.rooms.values() if r['region']==region))

    def test_permissions_are_free_persistent_and_available_before_gate(self):
        for rid in ['edran_salida_huertos','korven_peldanos_cortos']:
            room=self.world.rooms[rid]
            flag=room['exit_requirements']['oeste']['requires_flags'][0]
            request=next(a for a in room['actions'] if flag in a.get('set_flags',[]))
            self.assertIn(flag,request['forbids_flags'])
            self.assertNotIn('requires_items',request)
            self.assertIn(request['requires_npc'],room['npcs'])

    def test_local_campaign_offers_short_jobs_and_distinct_choices(self):
        w=self.world
        for qid in ['khariel_polea','khariel_cornisa','velmora_recipiente','narevia_preparativos']:
            q=w.quests[qid]
            self.assertIn(q['payout'],[6,8])
            self.assertFalse(q['repeatable'])
            self.assertTrue(q['required_actions'])
            self.assertIn('encargo_pagado:'+qid,w.npcs[q['npc']]['memory'])
            for target in q['required_rooms']:
                start=w.regions[w.rooms[target]['region']]['settlement']
                seen={start};todo=[(start,0)];distance=None
                while todo:
                    rid,steps=todo.pop(0)
                    if rid==target:distance=steps;break
                    for dest in w.rooms[rid]['exits'].values():
                        if dest not in seen:seen.add(dest);todo.append((dest,steps+1))
                self.assertLessEqual(distance,6)
        self.assertIn('forbids_flags',w.npcs['hoshai_seran']['topics']['acuerdo'])
        alternatives=w.rooms['hoshai_cajas_camino']['actions']
        self.assertEqual(len(alternatives),2)
        self.assertTrue(all(a['forbids_flags']==['hoshai_polea_recogida'] for a in alternatives))
        self.assertIn('victoria:hoshai_campamento_lona:forajido_camino',alternatives[1]['requires_flags'])

    def test_personal_recipient_delivery_survives_public_story_completion(self):
        from server.engine import Engine
        from server import mechanics as mechanics
        content=Content(Path(__file__).resolve().parents[1]/'content')
        now=12*3600
        engine=Engine(content,lambda:now)
        for public_completed in [False,True]:
            state=mechanics.new_state('vesperi','sombra','home:review',now)
            state['location']='nhal_umbral_elin'
            character={'id':919,'name':'Review','species':'vesperi','class_id':'sombra','state':state}
            world={'flags':['nhal_recipiente_devuelto'] if public_completed else [],'deaths':{}}
            engine.add_item(state,'recipiente_elin')
            engine.apply(character,world,{'id':'nhal_entregar_recipiente','target':None})
            self.assertIn('nhal_entrega_elin_completada',state['flags'])
            self.assertNotIn('nhal_recipiente_devuelto',state['flags'])
            self.assertEqual(world['flags'],['nhal_recipiente_devuelto'] if public_completed else [])
            old=next(a for a in content.rooms['nhal_umbral_elin']['actions'] if a['id']=='nhal_devolver_recipiente')
            self.assertEqual(old['scope'],'world')
            self.assertEqual(old['set_flags'],['nhal_recipiente_devuelto'])

    def test_brumak_honing_belongs_to_local_smith_not_potter(self):
        smith=self.world.npcs['korven_beran']
        room=self.world.rooms[smith['home_room']]
        self.assertEqual(room['forge_service'],smith['id'])
        self.assertIn(smith['id'],room['npcs'])
        self.assertEqual(room['honing_material'],'piedra_veteada')
        potter=self.world.npcs['korven_taren']
        self.assertEqual(potter['role'],'alfarera de recipientes')
        self.assertNotIn('forge_service',self.world.rooms[potter['home_room']])

    def test_regional_markets_differ_and_purchased_materials_fit_local_work(self):
        shops=[self.world.rooms[r]['shop'] for r in ['hoshai_mercado_cintas','lethra_mercado_hojas','nhal_mercado_setas','vaisgard_mercado']]
        self.assertEqual(len({tuple(x)for x in shops}),4)
        self.assertTrue(all('provision_basica' in x for x in shops))
        for r in self.world.rooms.values():
            for item in r.get('buy_items',[]):
                self.assertEqual(self.world.items[item]['kind'],'material')
                self.assertTrue(1<=self.world.items[item]['sell_price']<=60)
        for id in ['vaisgard_aviso_carga','vaisgard_toldo','brumak_taza']:
            self.assertFalse(self.world.quests[id]['repeatable'])
            self.assertIn(self.world.quests[id]['payout'],[6,8])
        self.assertNotIn('sell_price',self.world.items['junco_prestado_seli'])
        self.assertEqual(self.world.items['junco_prestado_seli']['kind'],'quest')

    def test_each_origin_has_comparable_threat_within_four_real_steps(self):
        from collections import deque
        from server.mechanics import PROFILES
        comparable={id for id,p in PROFILES.items() if p['category']!='abrumador'}
        for rg in ['edran','hoshai','korven','lethra','nhal']:
            origin=self.world.regions[rg]['settlement']
            todo=deque([(origin,0)]);seen={origin};nearest=None
            while todo:
                rid,steps=todo.popleft();r=self.world.rooms[rid]
                if any(s['creature'] in comparable for s in r.get('signals',[])+r.get('wildlife_pool',[])):
                    nearest=steps;break
                for dest in r['exits'].values():
                    if dest not in seen:seen.add(dest);todo.append((dest,steps+1))
            self.assertLessEqual(nearest,4,rg)
        for rid in ['nhal_sendero_altura','lethra_ribera_oeste']:
            room=self.world.rooms[rid]
            self.assertTrue(all(PROFILES.get(s['creature'],{}).get('category')!='abrumador'for s in room['wildlife_pool']))
            act=room['actions'][-1]
            self.assertFalse(act.get('give_items'))
            self.assertFalse(act.get('payout'))
            self.assertEqual(act['forbids_flags'],act['set_flags'])
            human=next(s for s in room['wildlife_pool']if s['creature']=='forajido_camino')
            self.assertEqual(human['forbids_flags'],act['set_flags'])

    def test_each_community_has_safe_local_care_with_resident_caregiver(self):
        from collections import deque
        for region in self.world.regions.values():
            origin=region['settlement'];todo=deque([(origin,0)]);seen={origin};distance=None
            while todo:
                rid,steps=todo.popleft();room=self.world.rooms[rid]
                if room.get('recovery_service'):
                    distance=steps
                    self.assertTrue(room.get('safe',room['kind']=='interior'))
                    if room.get('recovery_npc'):
                        npc=self.world.npcs[room['recovery_npc']]
                        self.assertEqual(npc['home_room'],rid)
                        self.assertIn(npc['id'],room['npcs'])
                        self.assertNotIn('schedule',npc)
                    break
                for dest in room['exits'].values():
                    if dest not in seen:seen.add(dest);todo.append((dest,steps+1))
            self.assertLessEqual(distance,4,origin)

    def test_new_local_care_uses_existing_recovery_contract(self):
        from server.engine import Engine
        from server import mechanics as mechanics
        content=Content(Path(__file__).resolve().parents[1]/'content');now=12*3600
        engine=Engine(content,lambda:now)
        for rid in ['hoshai_sala_cuidados','korven_sala_cuidados','lethra_sala_cuidados','nhal_sala_cuidados','veyra_sala_cuidados']:
            state=mechanics.new_state('humano','juramentado','home:care-review',now)
            state.update(location=rid,seals=18,hp=20,fatigue=80,wound='moderada',rest_budget=0)
            character={'id':992,'name':'Review','species':'humano','class_id':'juramentado','state':state}
            world={'flags':[],'deaths':{}}
            self.assertTrue(any(a['id']=='recuperacion'for a in engine.actions(character,world)))
            engine.apply(character,world,{'id':'recuperacion','target':None})
            self.assertEqual(state['seals'],0)
            self.assertEqual(state['fatigue'],0)
            self.assertIsNone(state['rest_budget'])
            self.assertEqual(state['wound'],'leve')
            self.assertGreater(state['hp'],20)

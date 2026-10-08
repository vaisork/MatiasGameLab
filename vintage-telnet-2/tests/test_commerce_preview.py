"""Purchase previews match real equipment and recovery; only temporary test DBs."""
import unittest
import test_real_content as fixtures
from server.store import Store

class CommercePreviewTests(unittest.TestCase):
 setUp=fixtures.RealContentTests.setUp
 post=fixtures.RealContentTests.post
 create=fixtures.RealContentTests.create
 action=fixtures.RealContentTests.action
 walk=fixtures.RealContentTests.walk
 def snapshot(self):return self.client.get('/api/state').json
 def test_preview_tracks_real_honing_and_equipped_reference(self):
  self.create();self.walk('edran_surcos');self.action('combatir','espinajo_rastrojo')
  self.clock.now+=44;won=self.snapshot();self.assertIsNone(won['character']['combat']);self.assertTrue(any(i['id']=='fibra_espinajo' for i in won['inventory']))
  self.walk('valdren_fragua');honed=self.action('afinar','espada_juramento',confirmed=True)
  self.assertEqual(honed['character']['seals'],8)
  self.assertEqual(honed['inventory'][0]['damage'],11)
  preview=next(a for a in honed['actions'] if a['id']=='comprar' and a['target']=='espada_juramento')
  self.assertIn('daño base 10',preview['label']);self.assertIn('permite bloquear',preview['label'])
  # Funds overwrite reason, so essential attributes stay in the visible label.
  self.assertTrue(preview['disabled']);self.assertIn('Te faltan',preview['reason'])
  # Temporary funds fixture opens the affordable preview branch; prices stay real.
  with self.app.extensions['store'].transaction() as db:
   character=Store.load(db.execute('SELECT * FROM characters WHERE id=?',(honed['character']['id'],)).fetchone())
   character['state']['seals']=100;Store.save(db,character)
  preview=next(a for a in self.snapshot()['actions'] if a['id']=='comprar' and a['target']=='espada_juramento')
  self.assertIn('Tu arma activa tiene 11 de daño base',preview['reason'])
  bought=self.action('comprar','punal_camino');self.assertEqual(bought['character']['seals'],50)
  knife=next(i for i in bought['inventory'] if i.get('catalog_id',i['id'])=='punal_camino')
  equipped=self.action('equipar',knife['id']);self.assertEqual(equipped['character']['equipment']['weapon'],knife['id'])
  # The affordable knife now compares to the newly equipped piece.
  knife_preview=next(a for a in equipped['actions'] if a['id']=='comprar' and a['target']=='punal_camino')
  self.assertIn('Tu arma activa tiene 8 de daño base',knife_preview['reason'])
  self.assertEqual(next(i['damage'] for i in equipped['inventory'] if i['id']=='espada_juramento'),11)
  # Provision is affordable: its effect survives in reason as well as label.
  self.walk('valdren_comedor');food=next(a for a in self.snapshot()['actions'] if a['id']=='comprar')
  self.assertIn('hasta 18 vida',food['label']);self.assertIn('20 fatiga',food['label']);self.assertIn('No trata heridas',food['reason'])
  self.assertEqual(self.snapshot()['character']['seals'],50)

 def test_provision_preview_matches_caps_and_preserves_wound_and_prices(self):
  cid=self.create();self.walk('valdren_comedor')
  def injury(hp,fatigue):
   # Explicit temporary fixture for capped recovery, never economic resources.
   with self.app.extensions['store'].transaction() as db:
    character=Store.load(db.execute('SELECT * FROM characters WHERE id=?',(cid,)).fetchone())
    character['state'].update(hp=hp,fatigue=fatigue,wound='leve');Store.save(db,character)
  injury(90,12);preview=next(a for a in self.snapshot()['actions'] if a['id']=='comprar')
  self.assertEqual(preview['cost'],8);self.assertIn('hasta 18 vida',preview['label']);self.assertIn('No trata heridas',preview['reason'])
  self.action('comprar','provision_basica');used=self.action('usar','provision_basica')
  self.assertEqual(used['character']['hp'],100);self.assertEqual(used['character']['fatigue'],0);self.assertEqual(used['character']['wound'],'leve');self.assertEqual(used['character']['seals'],12)
  injury(50,35);self.action('comprar','provision_basica');used=self.action('usar','provision_basica')
  self.assertEqual(used['character']['hp'],68);self.assertEqual(used['character']['fatigue'],15);self.assertEqual(used['character']['wound'],'leve');self.assertEqual(used['character']['seals'],4)

if __name__=='__main__':unittest.main()

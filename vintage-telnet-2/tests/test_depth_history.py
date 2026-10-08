"""Causal text follows existing alternative decisions through the actual API."""
import unittest
import test_real_content as content_tests

class HistoryBranchTests(unittest.TestCase):
 def test_alternative_decisions_remain_visible_after_delivery(self):
  run=content_tests.RealContentTests('test_real_errand_social_economy_home_and_reconnect')
  run.setUp();self.addCleanup(run.doCleanups);run.create()
  def scene():return ' '.join(e['text'] for e in run.client.get('/api/state').json['scene'])
  run.walk('hoshai_mercado_cintas');run.action('aceptar','khariel_cornisa')
  run.walk('hoshai_balcon_valle');run.action('examinar','cornisa');run.action('hoshai_pedir_revision')
  run.walk('hoshai_mercado_cintas');run.action('hablar','hoshai_luma',topic='cornisa');run.action('cobrar','khariel_cornisa')
  run.walk('hoshai_balcon_valle');self.assertIn('revisar la cornisa',scene())
  run.walk('lethra_mercado_hojas');run.action('aceptar','narevia_preparativos')
  run.walk('lethra_plataforma_secado');run.action('examinar','costuras');run.action('lethra_elegir_paño')
  run.walk('lethra_cocina_reunion');run.action('hablar','lethra_nima',topic='preparativos')
  self.assertIn('paño',scene());self.assertNotIn('Los cuencos se agrupan en el rincón cubierto',scene())
  run.walk('lethra_mercado_hojas');run.action('cobrar','narevia_preparativos')
  run.walk('veyra_patio_senales');run.action('aceptar','vaisgard_aviso_carga')
  run.walk('veyra_puerta_piedra');run.action('hablar','veyra_tov',topic='aviso')
  run.walk('veyra_archivo_cargas');run.action('hablar','veyra_nera',topic='pedir_comprobacion')
  self.assertIn('respuesta de Tov',scene())
  run.walk('veyra_patio_senales');run.action('cobrar','vaisgard_aviso_carga')
  run.walk('veyra_calle_toldos');run.action('aceptar','vaisgard_toldo');run.action('examinar','costura');run.action('veyra_preparar_perchas')
  self.assertIn('Las perchas que preparaste',run.client.get('/api/state').json['room']['description'])
  run.action('cobrar','vaisgard_toldo')
  run.walk('korven_entrante_piezas');run.action('aceptar','brumak_taza');run.action('hablar','korven_taren',topic='medidas')
  run.walk('korven_horno_reposo');run.action('examinar','recipiente');run.action('korven_recomendar_aro')
  run.walk('korven_entrante_piezas');run.action('hablar','korven_taren',topic='recomendación')
  self.assertIn('base ligera',scene());self.assertNotIn('base más ancha',scene())
  run.action('cobrar','brumak_taza')

if __name__=='__main__':unittest.main()

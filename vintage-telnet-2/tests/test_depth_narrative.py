import unittest
from unittest.mock import Mock

from server.engine import Engine


class DepthNarrative(unittest.TestCase):
    def setUp(self):
        self.engine = Engine(Mock(), lambda: 43200)
        self.room = {
            'id': 'review', 'description': 'El camino bordea el canal.',
            'day': 'Una mujer remienda su red.', 'clear': 'El agua refleja el cielo.',
            'weather': {'niebla': 'Sólo ves el primer poste del canal.'},
            'return': 'La red que viste rota ya cuelga reparada.',
        }
        self.engine.room = Mock(return_value=self.room)
        self.engine.ambient = Mock(return_value={'time_of_day': 'Día', 'weather': 'Niebla'})
        self.engine.people = Mock(return_value=[])
        self.character = {'state': {'visits': {'review': 2}, 'arrival': True}}

    def test_observing_preserves_local_fog_instead_of_clear_sky(self):
        texts = [line['text'] for line in self.engine.narrative(self.character, {}, 'observar')]
        self.assertIn(self.room['weather']['niebla'], texts)
        self.assertNotIn(self.room['clear'], texts)

    def test_return_memory_is_visible_without_expanding_reader(self):
        texts = [line['text'] for line in self.engine.narrative(self.character, {})]
        self.assertEqual(len(texts), 3)
        self.assertIn(self.room['return'], texts)
        self.assertIn(self.room['weather']['niebla'], texts)

    def test_unknown_weather_does_not_claim_clear_skies(self):
        self.assertIsNone(self.engine.local_weather(self.room, {'weather': 'Nieve'}))

    def test_later_return_leaves_room_for_weather_and_life(self):
        self.character['state']['visits']['review'] = 3
        texts = [line['text'] for line in self.engine.narrative(self.character, {})]
        self.assertIn(self.room['day'], texts)
        self.assertIn(self.room['weather']['niebla'], texts)
        self.assertNotIn(self.room['return'], texts)

    def test_local_focus_cannot_displace_a_present_threat(self):
        self.room['focus'] = ['activity', 'weather']
        self.room['signals'] = [{'creature': 'espinajo_rastrojo', 'text': 'Afirma las patas para embestir.'}]
        self.engine.allowed = Mock(return_value=True)
        texts = [line['text'] for line in self.engine.narrative(self.character, {'deaths': {}})]
        self.assertIn('Afirma las patas para embestir.', texts)
        self.assertEqual(len(texts), 3)

    def test_visit_variants_use_current_place_and_do_not_mutate_visits(self):
        self.engine.content.rooms = {'review': self.room}
        state = {'location': 'review', 'flags': [], 'inventory': [], 'visits': {'review': 2, 'elsewhere': 10}}
        self.assertFalse(self.engine.allowed({'requires_visits': {'min': 3}}, state, {'flags': []}))
        self.assertTrue(self.engine.allowed({'requires_visits': {'min': 1, 'max': 2}}, state, {'flags': []}))
        state['visits']['review'] = 3
        self.assertTrue(self.engine.allowed({'requires_visits': {'min': 3}}, state, {'flags': []}))
        self.assertFalse(self.engine.allowed({'requires_visits': {'max': 2}}, state, {'flags': []}))
        self.assertEqual(state['visits'], {'review': 3, 'elsewhere': 10})

    def test_completed_history_leaves_room_for_weather_on_later_returns(self):
        self.room['memories'] = [{'text': 'La red reparada protege ahora el paso.'}]
        self.room['focus'] = ['activity']
        self.engine.allowed = Mock(return_value=True)
        self.character['state']['visits']['review'] = 3
        lines = self.engine.narrative(self.character, {})
        self.assertEqual(len(lines), 3)
        self.assertIn(self.room['day'], [line['text'] for line in lines])
        self.assertIn(self.room['weather']['niebla'], [line['text'] for line in lines])
        self.character['state']['visits']['review'] = 5
        self.assertIn(self.room['memories'][0]['text'], [line['text'] for line in self.engine.narrative(self.character, {})])

"""Editorial summaries must preserve explicit reading and authoritative changes."""
import unittest
from unittest.mock import Mock
from server.engine import Engine


class MudPilotTests(unittest.TestCase):
    def setUp(self):
        self.base = {'id': 'pilot', 'description': 'El canal llega a tres peldaños.',
                     'brief': 'Los tres peldaños del canal.', 'exits': {}}
        self.engine = Engine(Mock(), lambda: 43200)
        self.engine.content.rooms = {'pilot': self.base}
        self.character = {'state': {'location': 'pilot', 'home': 'home',
                                    'visits': {'pilot': 1}, 'flags': [], 'inventory': []}}
        self.world = {'flags': [], 'deaths': {}}
        self.engine.ambient = Mock(return_value={'time_of_day': 'Día', 'weather': 'Despejado'})
        self.engine.people = Mock(return_value=[])

    def test_first_visit_full_return_brief_and_deliberate_look_full(self):
        self.assertEqual(self.engine.narrative(self.character, self.world)[0]['text'], self.base['description'])
        self.character['state']['visits']['pilot'] = 2
        self.assertEqual(self.engine.narrative(self.character, self.world)[0]['text'], self.base['brief'])
        looked = self.engine.narrative(self.character, self.world, 'mirar')[0]
        self.assertEqual(looked['text'], self.base['description'])
        self.assertEqual(looked['kind'].upper(), 'LOOK')

    def test_changed_world_description_cannot_use_old_summary(self):
        self.base['states'] = [{'overrides': {'description': 'El canal ya no tiene agua.'}}]
        self.engine.allowed = Mock(return_value=True)
        self.character['state']['visits']['pilot'] = 2
        self.assertEqual(self.engine.narrative(self.character, self.world)[0]['text'], 'El canal ya no tiene agua.')
        self.assertIn('brief', self.base)

    def test_authored_changed_summary_is_used(self):
        self.base['states'] = [{'overrides': {'description': 'El canal ya no tiene agua.', 'brief': 'El canal seco.'}}]
        self.engine.allowed = Mock(return_value=True)
        self.character['state']['visits']['pilot'] = 2
        self.assertEqual(self.engine.narrative(self.character, self.world)[0]['text'], 'El canal seco.')

    def test_absent_creature_description_cannot_use_old_summary(self):
        self.base['absent_creatures'] = {'espinajo': {'description': 'Los tallos han quedado quietos.'}}
        self.world['deaths']['pilot:espinajo'] = 43260
        self.character['state']['visits']['pilot'] = 2
        self.assertEqual(self.engine.narrative(self.character, self.world)[0]['text'], 'Los tallos han quedado quietos.')

"""Read authored JSON, never import legacy engine modules."""
import json
from pathlib import Path

TABLES = ('regions','rooms','npcs','creatures','stories','items','quests')

class Content:
    def __init__(self, root):
        self.root = Path(root)
        self.data = {key:{} for key in TABLES}
        files = sorted((self.root/'regions').glob('*.json'))
        if (self.root/'world.json').is_file():
            files.insert(0,self.root/'world.json')
        for filename in files:
            document = json.loads(filename.read_text(encoding='utf-8'))
            for table in TABLES:
                for key, value in document.get(table, {}).items():
                    if key in self.data[table] and self.data[table][key] != value:
                        raise ValueError(f'Duplicate conflicting {table}:{key} in {filename.name}')
                    self.data[table][key] = value
        for key, room in self.rooms.items():
            if room.get('id',key) != key or room.get('region') not in self.regions:
                raise ValueError(f'Invalid room identity/region: {key}')
            for destination in room.get('exits',{}).values():
                if destination not in self.rooms:
                    raise ValueError(f'Unknown exit from {key}: {destination}')
            for npc in room.get('npcs',[]):
                if npc not in self.npcs:
                    raise ValueError(f'Unknown NPC {npc} in {key}')
            for signal in [*room.get('signals',[]),*room.get('wildlife_pool',[])]:
                if signal.get('creature') not in self.creatures:raise ValueError(f'Unknown creature in {key}')
            for item_id in room.get('shop',[]):
                if item_id not in self.items:raise ValueError(f'Unknown shop item {item_id} in {key}')
            for action in room.get('actions',[]):
                if action.get('next') and action['next'] not in self.rooms:raise ValueError(f'Unknown action destination in {key}')
                for destination in action.get('discover_rooms',[]):
                    if destination not in self.rooms:raise ValueError(f'Unknown discovery in {key}')
        for region_id,region in self.regions.items():
            if region.get('settlement') not in self.rooms:raise ValueError(f'Unknown settlement for {region_id}')
        for region_id,region in self.regions.items():
            for found in region.get('search',{}).get('finds',[]):
                if found.get('item') not in self.items:raise ValueError(f'Unknown search item for {region_id}')
        for quest_id,quest in self.quests.items():
            if quest.get('accept_room') not in self.rooms or not set(quest.get('required_rooms',[])).issubset(self.rooms):raise ValueError(f'Invalid quest rooms {quest_id}')

    def __getattr__(self, key):
        if key in TABLES:
            return self.data[key]
        raise AttributeError(key)

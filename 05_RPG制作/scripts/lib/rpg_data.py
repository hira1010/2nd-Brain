import json
import os

class RpgMap:
    """ツクールMZのMap*.jsonを安全に読み書きし、配列構造破壊（今回のエラー原因）を防ぐクラス"""
    
    def __init__(self, map_path):
        self.map_path = map_path
        if not os.path.exists(map_path):
            raise FileNotFoundError(f"Map file not found: {map_path}")
            
        with open(self.map_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
            
        # 初期読み込み時に配列構造を自動修復・担保
        self._rebuild_events()

    def _rebuild_events(self):
        """events配列のインデックスを event.id と一致させ、0番地をnullにする絶対ルール"""
        new_events = [None]
        for ev in self.data.get('events', []):
            if ev and isinstance(ev, dict) and 'id' in ev:
                # 必要な長さに拡張
                while len(new_events) <= ev['id']:
                    new_events.append(None)
                new_events[ev['id']] = ev
        
        self.data['events'] = new_events

    def get_event(self, event_id):
        if 0 <= event_id < len(self.data['events']):
            return self.data['events'][event_id]
        return None

    def add_or_update_event(self, event_data):
        if 'id' not in event_data:
            raise ValueError("Event data must contain an 'id'.")
        
        event_id = event_data['id']
        while len(self.data['events']) <= event_id:
            self.data['events'].append(None)
            
        self.data['events'][event_id] = event_data

    def delete_event(self, event_id):
        if 0 <= event_id < len(self.data['events']):
            self.data['events'][event_id] = None # 要素を削除せずNoneにする（ツクール仕様）

    def save(self):
        # 保存時にもう一度ルールを確認
        self._rebuild_events()
        with open(self.map_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"Map safely saved: {self.map_path}")

# テスト用
if __name__ == '__main__':
    print("RPG Maker Map Manager Lib loaded.")

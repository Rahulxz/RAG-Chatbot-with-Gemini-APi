import json, os

class HistoryManager:
    def __init__(self, session_id):
        self.file_path = f"chat_history/{session_id}.json"
        os.makedirs("chat_history", exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def load_history(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def save_turn(self, role, content):
        history = self.load_history()
        history.append({"role": role, "content": content})
        with open(self.file_path, 'w') as f:
            json.dump(history, f, indent=2)

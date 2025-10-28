import uuid

class SessionManager:
    def __init__(self, sessions_dict=None):
        # Use an external dict (like st.session_state['sessions']) or create new
        self.sessions = sessions_dict if sessions_dict is not None else {}

    def create_session(self, name=None):
        session_id = name if name else f"session_{uuid.uuid4().hex[:6]}"
        self.sessions[session_id] = []
        return session_id

    def rename_session(self, old_name, new_name):
        if old_name in self.sessions and new_name.strip():
            self.sessions[new_name] = self.sessions.pop(old_name)
            return new_name
        return old_name

    def save_turn(self, session_id, role, message):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append({"role": role, "content": message})
    
    def get_history(self, session_id):
        return self.sessions.get(session_id, [])

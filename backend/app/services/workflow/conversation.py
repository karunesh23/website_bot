"""
Conversation State Manager
"""


class ConversationManager:

    def __init__(self):

        self.state = {}

    def start(self, session_id, flow, preserve_data=True):

        existing_data = self.state.get(session_id, {}).get("data", {}) if preserve_data else {}
        self.state[session_id] = {
            "flow": flow,
            "step": None,
            "data": existing_data
        }

    def set_step(self, session_id, step):

        self.state[session_id]["step"] = step

    def save(self, session_id, key, value):

        self.state[session_id]["data"][key] = value

    def get(self, session_id):

        return self.state.get(session_id)

    def end(self, session_id):
        if session_id in self.state:
            del self.state[session_id]

    def to_knowledge(self, session_id):
        if session_id in self.state:
            self.state[session_id]["flow"] = "KNOWLEDGE"
            self.state[session_id]["step"] = None
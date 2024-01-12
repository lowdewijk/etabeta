import pickle
from src.session.session import Session


class Sessions:
    def __init__(self):
        self.sessions = {}

    def create_session(self, session: Session):
        self.sessions[session.get_session_id()] = session

    def get_session(self, session_id: str) -> Session:
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str):
        del self.sessions[session_id]

    def get_session_ids(self) -> list[str]:
        return self.sessions.keys()

    def save(self):
        with open("chat_data/sessions.pickle", "wb") as handle:
            pickle.dump(self.sessions, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        try:
            with open("chat_data/sessions.pickle", "rb") as handle:
                self.sessions = pickle.load(handle)
        except FileNotFoundError:
            return

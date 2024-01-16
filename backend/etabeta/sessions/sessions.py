import logging
import os
import os.path as path
import pickle
from etabeta.session.session import Session


log = logging.getLogger(__name__)


class Sessions:
    data_path: str
    sessions: dict[str, Session]

    def __init__(self, save_path):
        self.sessions = {}
        self.data_path = save_path
        if not path.exists(save_path):
            log.warning(f"Data path {save_path} did not exist. Creating it.")
            os.makedirs(save_path)
        if not path.isdir(save_path):
            log.error(f"Data path {save_path} is not a directory. Disabling saving.")
            self.data_path = ""

    def create_session(self, session: Session):
        self.sessions[session.get_session_id()] = session

    def get_session(self, session_id: str) -> Session | None:
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str):
        del self.sessions[session_id]

    def get_session_ids(self) -> list[str]:
        return list(self.sessions.keys())

    def save(self):
        if not path.isdir(self.data_path):
            return
        try:
            with open(path.join(self.data_path, "sessions.pickle"), "wb") as handle:
                pickle.dump(self.sessions, handle, protocol=pickle.HIGHEST_PROTOCOL)
        except:
            log.exception(f"Failed to save sessions data.")

    def load(self):
        chat_data_file = path.join(self.data_path, "sessions.pickle")
        if not path.isfile(chat_data_file):
            return
        try:
            with open(path.join(self.data_path, "sessions.pickle"), "rb") as handle:
                self.sessions = pickle.load(handle)
        except:
            log.exception(f"Failed to load sessions data.")

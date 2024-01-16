import logging
from etabeta.sessions.sessions import Sessions
import os

log = logging.getLogger(__name__)

data_path = os.getenv("ETABETA_DATA_PATH", "chat_data")
log.info(f"Using data path: {data_path}")

sessions = Sessions(data_path)
sessions.load()

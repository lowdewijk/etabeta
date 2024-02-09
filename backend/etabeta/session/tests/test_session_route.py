from etabeta.common.Clock import clock
from etabeta.common.Config import config
from etabeta.session.Session import Session
from etabeta.main import app
from fastapi.testclient import TestClient
from etabeta.common.chat_data import sessions

client = TestClient(app)

def test_join_leave_session():
    clock.set_fixed_timestamp(1)

    sessions.create_session(Session("test"))
    assert client.get("/api/session/test/join/lobo").status_code == 200

    response = client.get("/api/session/test/active_users")
    assert response.status_code == 200
    assert response.json() == {
        "users": [{
            "username": "lobo",
            "last_active": 1
        }],
        "ais": []
    }

    response = client.get("/api/session/test/leave/lobo")
    assert response.status_code == 200

    response = client.get("/api/session/test/active_users")
    assert response.status_code == 200
    assert response.json() == {
        "users": [],
        "ais": []
    }

def test_update_last_active_on_read_messages():
    clock.set_fixed_timestamp(1)
    sessions.create_session(Session("test"))

    assert client.get("/api/session/test/join/lobo").status_code == 200

    clock.set_fixed_timestamp(2)
    assert  client.get("/api/session/test/messages/lobo").status_code == 200

    response = client.get("/api/session/test/active_users")
    assert response.status_code == 200
    assert response.json() == {
        "users": [{
            "username": "lobo",
            "last_active": 2
        }],
        "ais": []
    }

def test_remove_inactive_users():
    clock.set_fixed_timestamp(1)
    config.prune_session_user_timeout = 1

    sessions.create_session(Session("test"))
    assert client.get("/api/session/test/join/lobo").status_code == 200
    assert client.get("/api/session/test/join/bobo").status_code == 200
    clock.set_fixed_timestamp(10)
    assert client.get("/api/session/test/messages/lobo").status_code == 200

    response = client.get("/api/session/test/active_users")
    assert response.status_code == 200
    assert response.json() == {
        "users": [{
            "username": "lobo",
            "last_active": 10
        }],
        "ais": []
    }

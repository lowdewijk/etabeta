from etabeta.common.Clock import clock
from etabeta.session.Session import Session
from etabeta.main import app
from fastapi.testclient import TestClient
from etabeta.common.chat_data import sessions

client = TestClient(app)

def test_join_leave_session():
    clock.set_fixed_timestamp(1)

    sessions.create_session(Session("test"))
    response = client.get("/api/session/test/join/lobo")
    assert response.status_code == 200

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

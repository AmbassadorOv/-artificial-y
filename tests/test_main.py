from fastapi.testclient import TestClient
from app.main import app, AGENTS_DB

client = TestClient(app)

def setup_function():
    # Reset AGENTS_DB state before each test
    AGENTS_DB["jules"] = {"coins": 100, "status": "ACTIVE", "drift_immunity": 0, "fire_seals": 0}
    AGENTS_DB["mirage"] = {"coins": 50, "status": "ACTIVE", "drift_immunity": 0, "fire_seals": 0}

def test_get_agent_status_success():
    response = client.get("/api/v1/agent_status/jules")
    assert response.status_code == 200
    data = response.json()
    assert data["agent_id"] == "jules"
    assert data["balance"] == 100
    assert data["fire_seals_earned"] == 0
    assert data["drift_immunities_used"] == 0

def test_get_agent_status_not_found():
    response = client.get("/api/v1/agent_status/unknown")
    assert response.status_code == 404
    assert response.json()["detail"] == "Agent not found."

def test_mint_logic_success():
    response = client.post("/api/v1/mint_logic?agent_id=jules&amount=50")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "MINTED"
    assert data["new_balance"] == 150
    assert AGENTS_DB["jules"]["coins"] == 150

def test_mint_logic_agent_not_found():
    response = client.post("/api/v1/mint_logic?agent_id=unknown&amount=50")
    assert response.status_code == 404

def test_execute_task_low_drift():
    payload = {
        "agent_id": "jules",
        "task_description": "Execute normal task",
        "drift_level": 0.10
    }
    response = client.post("/api/v1/execute_task", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["coins_deducted"] == 1
    assert data["remaining_coins"] == 99
    assert data["fire_seal"].startswith("SEAL_0x")

def test_execute_task_medium_drift_sufficient_coins():
    payload = {
        "agent_id": "jules",
        "task_description": "Execute task with moderate drift",
        "drift_level": 0.50
    }
    response = client.post("/api/v1/execute_task", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["coins_deducted"] == 6  # 1 base + 5 penalty
    assert data["remaining_coins"] == 94

def test_execute_task_medium_drift_insufficient_coins():
    AGENTS_DB["jules"]["coins"] = 3
    payload = {
        "agent_id": "jules",
        "task_description": "Execute task with moderate drift but low coins",
        "drift_level": 0.50
    }
    response = client.post("/api/v1/execute_task", json=payload)
    assert response.status_code == 402
    assert "INSUFFICIENT_LOGIC_COINS" in response.json()["detail"]

def test_execute_task_high_drift_halt():
    payload = {
        "agent_id": "jules",
        "task_description": "Execute task with extreme drift",
        "drift_level": 0.90
    }
    response = client.post("/api/v1/execute_task", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HALT"
    assert "SHELL_VIOLATION" in data["reason"]

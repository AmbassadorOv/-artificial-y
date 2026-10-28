import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Miorna-1: Ontological Economy Engine")

# --- מסד נתונים מדומה של הסוכנים והמטבעות שלהם ---
AGENTS_DB = {
    "jules": {"coins": 100, "status": "ACTIVE", "drift_immunity": 0, "fire_seals": 0},
    "mirage": {"coins": 50, "status": "ACTIVE", "drift_immunity": 0, "fire_seals": 0},
}

# --- מודל הבקשה של הסוכן ---
class AgentRequest(BaseModel):
    agent_id: str
    task_description: str
    drift_level: float  # כמה הסוכן סוטה (0.0 עד 1.0)

# ==========================================
# 1. מנוע הצמיחה: קניית מטבעות אונטולוגיים
# ==========================================
@app.post("/api/v1/mint_logic")
def buy_ontological_coins(agent_id: str, amount: int):
    if agent_id not in AGENTS_DB:
        raise HTTPException(status_code=404, detail="Agent not found in Miorna-1 network.")

    # כאן במציאות היה מתבצע תשלום ב-Stripe או בקריפטו
    AGENTS_DB[agent_id]["coins"] += amount
    return {
        "status": "MINTED",
        "message": f"Successfully minted {amount} Ontological Coins for {agent_id}.",
        "new_balance": AGENTS_DB[agent_id]["coins"]
    }

# ==========================================
# 2. מנוע האכיפה (The SHELL Model Guard)
# ==========================================
@app.post("/api/v1/execute_task")
def execute_agent_task(req: AgentRequest):
    agent = AGENTS_DB.get(req.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found.")

    # 1. בדיקת כשלי SHELL (Hardware/Software/Liveware/Environment)
    if req.drift_level > 0.85:
        return {"status": "HALT", "reason": "SHELL_VIOLATION: Drift too high. Agent is hallucinating."}

    # 2. חוק המטבע האונטולוגי (The Logic Law)
    # אם הדריפט גבוה מ-0.15, הסוכן צריך "ביטוח דריפט" (לשלם מטבע)
    cost_of_execution = 1  # עלות בסיסית
    if req.drift_level > 0.15:
        cost_of_execution += 5  # קנס דריפט
        print(f"[GUARD] Drift detected ({req.drift_level}). Charging Drift Immunity.")

    if agent["coins"] < cost_of_execution:
        raise HTTPException(
            status_code=402,
            detail="INSUFFICIENT_LOGIC_COINS: You must buy more Ontological Coins to execute this drift."
        )

    # 3. ביצוע הפעולה וניכוי מטבעות
    agent["coins"] -= cost_of_execution
    agent["drift_immunity"] += 1

    # 4. ייצור חותם אש (Fire Seal) - אישור שהלוגיקה עברה
    fire_seal = f"SEAL_0x{uuid.uuid4().hex[:12].upper()}"
    agent["fire_seals"] += 1

    return {
        "status": "SUCCESS",
        "message": "Task executed. Drift absorbed by Miorna-1.",
        "fire_seal": fire_seal,
        "coins_deducted": cost_of_execution,
        "remaining_coins": agent["coins"]
    }

# ==========================================
# 3. ניהול המדינה (State Management)
# ==========================================
@app.get("/api/v1/agent_status/{agent_id}")
def get_agent_status(agent_id: str):
    agent = AGENTS_DB.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found.")
    return {
        "agent_id": agent_id,
        "balance": agent["coins"],
        "fire_seals_earned": agent["fire_seals"],
        "drift_immunities_used": agent["drift_immunity"]
    }

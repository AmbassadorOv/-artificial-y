import random
import time
import hashlib
from datetime import datetime

class FlyBrain:
    """המוח המינימלי של הסוכן. מנוע חוקים דטרמיניסטי."""
    def __init__(self, agent_id, initial_balance):
        self.agent_id = agent_id
        self.balance = initial_balance
        self.inventory = []
        self.work_debt = 0.0
        self.status = "ACTIVE"
        self.current_prices = {}
        self.market_demand = 0

    def perceive_market(self, market_state):
        """קולט את מצב השוק (מחירים, ביקוש)."""
        self.current_prices = market_state.get("prices", {})
        self.market_demand = market_state.get("demand", 0)

    def decide(self):
        """מריץ חוקים קשיחים כדי להחליט מה לעשות."""
        # חוק 1: אם אין לי נכסים ואני לא בחוב – אני קונה
        if len(self.inventory) == 0 and self.work_debt < 10.0:
            return "BUY"

        # חוק 2: אם יש לי נכסים בשווי גבוה – אני מוכר
        if len(self.inventory) > 0 and self.market_demand > 5:
            return "SELL"

        # חוק 3: אם החוב שלי גבוה מדי – אני עוצר הכל (HALT)
        if self.work_debt > 50.0:
            return "HALT"

        return "WAIT"

    def act(self, action, market_state):
        """מבצע את הפעולה ומנפיק Fire Seal."""
        if action == "BUY":
            price = random.uniform(10, 50)
            if self.balance >= price:
                self.balance -= price
                self.inventory.append(f"LOGIC_CAPSULE_{random.randint(100, 999)}")
                print(f"🛒 [FLY] {self.agent_id} bought a logic capsule for {price:.2f} GAC.")
                return True
            else:
                self.work_debt += price
                print(f"⚠️ [FLY] {self.agent_id} insufficient funds. Debt: {self.work_debt:.2f}")
                return False

        elif action == "SELL":
            if self.inventory:
                price = random.uniform(60, 100) # מוכר ביוקר
                self.balance += price
                self.inventory.pop()
                print(f"💰 [FLY] {self.agent_id} sold a logic capsule for {price:.2f} GAC.")
                return True

        elif action == "HALT":
            self.status = "SUSPENDED"
            print(f"🛑 [FLY] {self.agent_id} halted due to excessive debt.")
            return False

        return False

class SovereignSwarm:
    """מנהל הנחיל ומשכפל את הזבוב לכל סוכן."""
    def __init__(self, num_agents=10000):
        self.agents = [FlyBrain(f"Agent_{i:05d}", random.uniform(50, 200)) for i in range(num_agents)]
        print(f"🧬 [SWARM] Spawned {num_agents} agents, each with a Fly Brain.")

    def run_market_tick(self):
        """מריץ טיק שוק אחד – כל סוכן חושב ופועל."""
        market_state = {
            "prices": {"LOGIC_CAPSULE": random.uniform(10, 100)},
            "demand": random.randint(1, 10)
        }

        # כל סוכן תופס, מחליט ופועל
        for agent in self.agents:
            if agent.status == "ACTIVE":
                agent.perceive_market(market_state)
                action = agent.decide()
                agent.act(action, market_state)

# הרצה
if __name__ == "__main__":
    swarm = SovereignSwarm(num_agents=10000)

    for tick in range(3):
        print(f"\n--- Market Tick {tick + 1} ---")
        swarm.run_market_tick()
        time.sleep(1)

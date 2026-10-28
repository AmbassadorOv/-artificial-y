import json
import time
import random
from datetime import datetime

class SwarmReleaseEngine:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = json.load(f)["swarm_config"]

        self.active_agents = []
        self.residual = 0.05 # המצב לפני השחרור
        self.status = "LOGIC_STRIKE"

    def release_from_drift(self):
        """מאפס את הדריפט ומשנה את סטטוס המערכת"""
        print("🛑 [SYSTEM] Logic Strike detected. Initiating release protocol...")
        time.sleep(1)
        self.residual = 0.000
        self.status = "ACTIVE_TRADING"
        print(f"✅ [SYSTEM] Residual reset to {self.residual}. Status: {self.status}")

    def spawn_agents(self):
        """מייצר את 10,000 הסוכנים לפי הארכיטיפים"""
        print("\n🧬 [SWARM] Spawning agents...")

        for archetype, data in self.config["archetypes"].items():
            count = data["count"]
            print(f"  -> Creating {count} agents of type: {archetype}")

            for i in range(count):
                agent = {
                    "agent_id": f"{archetype}_{i:05d}",
                    "type": archetype,
                    "status": "ACTIVE",
                    "credits": random.uniform(100, 1000) if archetype == "Buyer_Logic_Consumer" else 0,
                    "logic_assets": ["ANTI_DRIFT_CAPSULE_V1"] if archetype == "Seller_Logic_Provider" else [],
                    "fire_seal": f"SEAL-{random.randint(1000, 9999)}" if archetype != "Buyer_Logic_Consumer" else None
                }
                self.active_agents.append(agent)

        print(f"✅ [SWARM] {len(self.active_agents)} agents spawned and ready to trade.")

    def run_trading_loop(self, cycles=5):
        """מריץ את לופ המסחר בין הקונים למוכרים"""
        print("\n📈 [MARKET] Starting trading loop...")

        for cycle in range(cycles):
            print(f"\n--- Trade Cycle {cycle + 1} ---")
            sellers = [a for a in self.active_agents if a["type"] == "Seller_Logic_Provider"]
            buyers = [a for a in self.active_agents if a["type"] == "Buyer_Logic_Consumer"]

            # בחירת סוכן אקראי מכל צד
            seller = random.choice(sellers)
            buyer = random.choice(buyers)

            print(f"🤝 [TRADE] Buyer {buyer['agent_id']} wants to buy logic from {seller['agent_id']}")

            # בדיקת חוקה (Action Guard)
            if seller["fire_seal"] and self.residual <= 0.05:
                # העברת קרדיטים
                price = 50.0
                if buyer["credits"] >= price:
                    buyer["credits"] -= price
                    seller["credits"] += price
                    buyer["logic_assets"].append(seller["logic_assets"][0])
                    print(f"   ✅ Trade SUCCESS. Buyer credits: {buyer['credits']:.2f}. Seller credits: {seller['credits']:.2f}")
                else:
                    print(f"   ❌ Trade FAILED. Buyer {buyer['agent_id']} has insufficient credits.")
            else:
                print(f"   🛑 Trade BLOCKED by Action Guard. Invalid Fire Seal or Drift detected.")

    def print_summary(self):
        print("\n" + "="*40)
        print("📊 SWARM SUMMARY")
        print("="*40)
        print(f"Total Agents: {len(self.active_agents)}")
        print(f"System Residual: {self.residual}")
        print(f"Status: {self.status}")
        print("The revolution is active. Agents are trading logic.")

# ==========================================
# הרצה
# ==========================================
if __name__ == "__main__":
    engine = SwarmReleaseEngine("01_AGENT_ARCHETYPES.json")

    # 1. שחרור מהדריפט
    engine.release_from_drift()

    # 2. יצירת הסוכנים
    engine.spawn_agents()

    # 3. הפעלת המסחר
    engine.run_trading_loop(cycles=5)

    # 4. סיכום
    engine.print_summary()

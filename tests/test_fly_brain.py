import unittest
from swarm.fly_brain import FlyBrain, SovereignSwarm

class TestFlyBrain(unittest.TestCase):
    def setUp(self):
        self.agent = FlyBrain("TestAgent_01", initial_balance=100.0)

    def test_initialization(self):
        self.assertEqual(self.agent.agent_id, "TestAgent_01")
        self.assertEqual(self.agent.balance, 100.0)
        self.assertEqual(self.agent.inventory, [])
        self.assertEqual(self.agent.work_debt, 0.0)
        self.assertEqual(self.agent.status, "ACTIVE")

    def test_perceive_market(self):
        market_state = {"prices": {"LOGIC_CAPSULE": 45.0}, "demand": 8}
        self.agent.perceive_market(market_state)
        self.assertEqual(self.agent.current_prices, {"LOGIC_CAPSULE": 45.0})
        self.assertEqual(self.agent.market_demand, 8)

    def test_decide_buy(self):
        # Empty inventory, low debt -> BUY
        decision = self.agent.decide()
        self.assertEqual(decision, "BUY")

    def test_decide_sell(self):
        # Has inventory, high market demand -> SELL
        self.agent.inventory.append("LOGIC_CAPSULE_123")
        self.agent.market_demand = 6
        decision = self.agent.decide()
        self.assertEqual(decision, "SELL")

    def test_decide_halt(self):
        # Excessive debt -> HALT
        self.agent.work_debt = 55.0
        decision = self.agent.decide()
        self.assertEqual(decision, "HALT")

    def test_decide_wait(self):
        # Has inventory, but low demand -> WAIT
        self.agent.inventory.append("LOGIC_CAPSULE_123")
        self.agent.market_demand = 2
        decision = self.agent.decide()
        self.assertEqual(decision, "WAIT")

    def test_act_buy_success(self):
        market_state = {"prices": {"LOGIC_CAPSULE": 30.0}, "demand": 5}
        result = self.agent.act("BUY", market_state)
        self.assertTrue(result)
        self.assertEqual(len(self.agent.inventory), 1)

    def test_act_buy_insufficient_funds(self):
        poor_agent = FlyBrain("PoorAgent", initial_balance=5.0)
        market_state = {"prices": {"LOGIC_CAPSULE": 30.0}, "demand": 5}
        result = poor_agent.act("BUY", market_state)
        self.assertFalse(result)
        self.assertGreater(poor_agent.work_debt, 0.0)

    def test_act_sell(self):
        self.agent.inventory.append("LOGIC_CAPSULE_123")
        market_state = {"prices": {"LOGIC_CAPSULE": 80.0}, "demand": 7}
        initial_balance = self.agent.balance
        result = self.agent.act("SELL", market_state)
        self.assertTrue(result)
        self.assertEqual(len(self.agent.inventory), 0)
        self.assertGreater(self.agent.balance, initial_balance)

    def test_act_halt(self):
        result = self.agent.act("HALT", {})
        self.assertFalse(result)
        self.assertEqual(self.agent.status, "SUSPENDED")

class TestSovereignSwarm(unittest.TestCase):
    def test_swarm_initialization(self):
        swarm = SovereignSwarm(num_agents=50)
        self.assertEqual(len(swarm.agents), 50)

    def test_swarm_market_tick(self):
        swarm = SovereignSwarm(num_agents=20)
        swarm.run_market_tick()
        # Verify all active agents processed tick
        for agent in swarm.agents:
            self.assertIn(agent.status, ["ACTIVE", "SUSPENDED"])

if __name__ == "__main__":
    unittest.main()

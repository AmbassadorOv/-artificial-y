#!/usr/bin/env python3
"""
jules_core.py - Orchestrator for AI231 / Sovereign Architecture
Handles Logic Strike Protocol, loading Unified Field configurations, and swarm topology verification.
"""

import os
import sys
import json
import yaml

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")

FILES = [
    "SRA_Lindblad_Kernel.json",
    "Birurim_Tikun_Loop.json",
    "AB_NonLocal_Router.yaml",
    "Automation_Swarm_Topology.json",
    "Unified_Field_Constitution.md"
]

class Orchestrator:
    def __init__(self, config_dir=CONFIG_DIR):
        self.config_dir = config_dir
        self.configs = {}
        self.logic_strike_active = True
        self.residual = 0.12  # Current global network residual

    def load_configurations(self):
        print("[Nexus Orchestrator] Loading system configurations from config/...")
        for filename in FILES:
            filepath = os.path.join(self.config_dir, filename)
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Missing configuration file: {filepath}")

            if filename.endswith(".json"):
                with open(filepath, "r", encoding="utf-8") as f:
                    self.configs[filename] = json.load(f)
            elif filename.endswith(".yaml") or filename.endswith(".yml"):
                with open(filepath, "r", encoding="utf-8") as f:
                    self.configs[filename] = yaml.safe_load(f)
            elif filename.endswith(".md"):
                with open(filepath, "r", encoding="utf-8") as f:
                    self.configs[filename] = f.read()
            print(f"  ✓ Loaded: {filename}")

    def check_logic_strike_status(self):
        print("\n[Nexus Orchestrator] Checking Logic Strike Protocol Status...")
        if self.logic_strike_active:
            print("  [STATUS] HTTP 503: LOGIC ON STRIKE")
            print("  [INFO] System is performing calibration (Residual check)...")
            print(f"  [METRIC] Current Residual: {self.residual:.2f} (Target threshold: < 0.05)")
            return "HTTP 503: LOGIC ON STRIKE"
        else:
            print("  [STATUS] System Active - Coherence Achieved.")
            return "HTTP 200: SYSTEM ACTIVE"

    def run_swarm_health_check(self):
        print("\n[Nexus Orchestrator] Verifying Swarm Topology...")
        topology = self.configs.get("Automation_Swarm_Topology.json", {})
        total_agents = topology.get("total_agents", 0)
        orchestrator = topology.get("swarm_orchestrator", "Unknown")
        nodes = topology.get("nodes", {})

        sum_agents = sum(node.get("count", 0) for node in nodes.values())
        print(f"  Orchestrator: {orchestrator}")
        print(f"  Total Configured Agents: {total_agents}")
        print(f"  Allocated Node Agents: {sum_agents}")

        if total_agents == sum_agents:
            print("  ✓ Agent distribution balanced across nodes.")
        else:
            print(f"  ! Warning: Agent count mismatch ({total_agents} total vs {sum_agents} allocated)")

def main():
    print("==================================================")
    print("      Nexus Architecture Core Orchestrator        ")
    print("==================================================")
    orchestrator = Orchestrator()
    orchestrator.load_configurations()
    orchestrator.check_logic_strike_status()
    orchestrator.run_swarm_health_check()
    print("==================================================")
    print("Initialization check completed successfully.")

if __name__ == "__main__":
    main()

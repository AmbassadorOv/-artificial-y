# digital_agent/main.py
# Core logic for the Digital Agent, the exclusive executor of the Hex 6F and Cube S12 protocol.

import json
import hashlib

class DigitalAgent:
    """
    The Digital Agent, responsible for enforcing the sacred rules of the Genesis Protocol.
    """
    def __init__(self, config_path='digital_agent/config.json'):
        self.config = self.load_config(config_path)
        self.canonical_config_string = self.config['ConfigurationString']
        self.solvency_threshold = self.config['SolvencyMandateThreshold']
        print("Digital Agent Initialized. Canonical Configuration Loaded.")

    def load_config(self, path):
        """Loads the canonical configuration."""
        with open(path, 'r') as f:
            return json.load(f)

    def p0_initialization(self, raw_data):
        """P0 - LCE: Determines workflow direction."""
        print("\n--- P0: Initialization (LCE) ---")
        # This is a stub. In a real scenario, this would involve a complex check.
        workflow_direction = "Standard: A<B>C>D"
        print(f"Workflow Direction Determined: {workflow_direction}")
        return workflow_direction, raw_data

    def p1_mml_filtering(self, items):
        """P1 - Hex 6F Step A: MML Filtering and CF=+3."""
        print("\n--- P1: MML Filtering (CF=+3) ---")
        processed_items = []
        for item in items:
            # Stub for MML filtering and category assignment
            item['Category'] = 'Urgent'
            item['CF_History'] = [+3]
            processed_items.append(item)
            print(f"Item '{item['ItemID']}': Category='{item['Category']}', CF=+3")
        return processed_items

    def p2_cube_s12_allocation(self, items):
        """P2 - Hex 6F Step B: Cube S12 Allocation and CF=+4."""
        print("\n--- P2: Cube S12 Allocation (CF=+4) ---")
        # Stub for Cube S12 ordering and resource allocation
        for item in items:
            item['P'] = 0.12  # Placeholder value
            item['CF_History'].append(+4)
            print(f"Item '{item['ItemID']}': P={item['P']:.2f}, CF=+4")
        return items

    def p3_action_estimate(self, items):
        """P3 - Hex 6F Step C: Action Estimate and CF=+6."""
        print("\n--- P3: Action Estimate & Solvency (CF=+6) ---")
        total_estimate = 0
        for item in items:
            # Action Estimate = P^6
            item['ActionEstimate'] = item['P'] ** 6
            item['CF_History'].append(+6)
            total_estimate += item['ActionEstimate']
            print(f"Item '{item['ItemID']}': ActionEstimate={item['ActionEstimate']:.6f}, CF=+6")

        # Solvency Check
        avg_estimate = total_estimate / len(items)
        if avg_estimate >= self.solvency_threshold:
            print(f"SOLVENCY PASSED: Avg. Estimate ({avg_estimate:.4f}) >= Threshold ({self.solvency_threshold:.4f})")
            return items, True
        else:
            print(f"SOLVENCY FAILED: Avg. Estimate ({avg_estimate:.4f}) < Threshold ({self.solvency_threshold:.4f})")
            return items, False

    def p4_aggregation(self, items, config_string_to_embed):
        """P4 - AER: Produces the final report."""
        print("\n--- P4: Aggregation (AER) ---")
        report = []
        config_hash = hashlib.sha256(config_string_to_embed.encode()).hexdigest()
        for item in items:
            report.append(
                f"{item['ItemID']}\t{item['Category']}\t{item['CF_History'][0]}"
                f"\t{item['CF_History'][1]}\t{item['CF_History'][2]}\t{item['P']:.2f}"
                f"\t{item['ActionEstimate']:.6f}\t{config_hash}"
            )

        final_output = "\n".join(report)
        print("Final Tab-Separated Report Generated.")
        return final_output

    def run_full_cycle(self, raw_input_data, embedded_config_string):
        """Executes the full P0 -> P4 cycle."""
        # Self-Check: Verify embedded config string
        if embedded_config_string != self.canonical_config_string:
            raise ValueError("Configuration String Mismatch! Halting cycle.")

        print("Configuration String Verified. Starting Cycle.")

        _, items = self.p0_initialization(raw_input_data)
        items = self.p1_mml_filtering(items)
        items = self.p2_cube_s12_allocation(items)
        items, solvency_passed = self.p3_action_estimate(items)

        if solvency_passed:
            report = self.p4_aggregation(items, embedded_config_string)
            return report
        else:
            return "CYCLE FAILED: Solvency check not passed. No report generated."


if __name__ == '__main__':
    # --- Human-in-the-Loop I/O Bus Simulation ---

    # 1. Operator provides the XLS/Text input and the Configuration String
    #    (In a real scenario, this would come from the UI)
    xls_input = [
        {"ItemID": "123", "Description": "Task A"},
        {"ItemID": "124", "Description": "Task B"},
    ]

    # The agent expects the full config string to be passed in to start the cycle
    with open('digital_agent/config.json', 'r') as f:
        incoming_config_string = json.load(f)['ConfigurationString']

    # 2. Initialize and run the Digital Agent
    agent = DigitalAgent()
    final_report = agent.run_full_cycle(xls_input, incoming_config_string)

    # 3. Output is displayed to the operator
    print("\n--- FINAL P4 OUTPUT (for XLS/Text I/O Bus) ---")
    print("ItemID\tCategory\tCFP1\tCFP2\tCF_P3\tP\tActionEstimate\tConfigHash")
    print(final_report)

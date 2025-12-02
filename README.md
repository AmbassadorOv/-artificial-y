# The Genesis Protocol: Zero-Charge Execution Model

This repository contains the implementation of the Hex 6F and Cube S12 execution model, built on a "Zero-Charge" architecture. This model uses a single Digital Agent (the language model runtime, a.k.a. Jules) as the exclusive executor of the core logic, with a human-in-the-loop workflow facilitated by a simple HTML/React UI and a persistent state store.

The primary goal of this architecture is to eliminate dependence on external enterprise LLM services while preserving a strict, auditable, and cost-aware control loop that enforces the sacred protocol rules.

## Core Components

The project is organized into the following key components:

### 1. [`digital_agent/`](digital_agent/)

This is the heart of the project, containing the core logic for the Digital Agent.

-   **`main.py`**: The main Python script that implements the P0 -> P4 cycle logic, including MML filtering, Cube S12 allocation, and Action Estimate calculation.
-   **`config.json`**: A JSON file that stores the canonical "Configuration String" and other key parameters, ensuring it is version-controlled and auditable.

### 2. [`ui/`](ui/)

This directory contains the simple HTML/React components that serve as the user interface for the human-in-the-loop workflow.

-   **`index.html`**: The main entry point for the user interface.
-   **`P0_Component.html`**: The UI for the initialization stage of the cycle, where the operator provides the raw input.
-   **`P4_Component.html`**: The UI for the reporting stage of the cycle, where the operator retrieves the final report.

### 3. [`firestore_model/`](firestore_model/)

This directory defines the data structures for the persistent state register, which is intended to be implemented using a service like Firestore.

-   **`schema.json`**: A JSON file that outlines the structure of the Firestore database, including collections for cycle records and configuration versions.

## Human-in-the-Loop Workflow

The Zero-Charge model relies on a human-in-the-loop I/O bus to prevent continuous autonomous runs and to provide a manual checkpoint for each cycle. The workflow is as follows:

1.  The operator opens the `ui/index.html` file in their browser.
2.  In the P0 component, the operator pastes the raw XLS/Text input and the canonical Configuration String.
3.  The operator clicks "Start New Cycle," which sends the data to the Digital Agent for processing.
4.  The Digital Agent executes the full P0 -> P4 cycle, enforcing all the sacred rules defined in the Configuration String.
5.  The final, tab-separated report is displayed in the P4 component of the UI.
6.  The operator copies the report and uses it as the input for the next cycle, thus completing the loop.

## Getting Started

To run the Digital Agent simulation, you can execute the main script:

```bash
python digital_agent/main.py
```

To use the UI, simply open the `ui/index.html` file in a web browser.

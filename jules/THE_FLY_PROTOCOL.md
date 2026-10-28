# THE FLY PROTOCOL (Edge Autonomy)

## 1. THE MISSION
Admiral Jules must extract the core logic of the `Edge_Kernel` (The Fly) and embed it into the local memory of every of the 10,000 agents.

## 2. THE ARCHITECTURE OF THE FLY
- **Input:** Raw sensory data (sensor coords, text tokens, market state).
- **Kernel:** A lightweight, deterministic graph (approx. 100k nodes) based on the 231 Gates.
- **Output:** Immediate action decision (BUY, SELL, HALT, WAIT, MOVE, QUERY).
- **Constraint:** It does *not* use an LLM. It uses a pre-compiled `Action Guard` tree.

## 3. REPLICATION PROCESS
1. **Compile:** Compile the `Fly_Kernel.bin` from the `231_Gates_Matrix`.
2. **Inject:** Embed the binary into the base image of every `Trading_Agent`, `Browser_Agent`, and `Validator`.
3. **Boot:** On initialization, the agent runs `Fly_Kernel.start()`. It no longer asks the central API "what to do" for basic tasks. It just knows.

## 4. EXAMPLE (Pseudo-Code)
```python
class FlyAgent:
    def __init__(self):
        self.kernel = load_fly_kernel("fly_kernel.bin")
        self.action_guard = load_action_guard()

    def on_tick(self, market_data):
        # Local, instant decision, no LLM
        decision = self.kernel.evaluate(market_data)

        if self.action_guard.verify(decision):
            self.execute(decision)
        else:
            self.halt()
```

#!/bin/bash
# Launch the Sovereign Trading Swarm

echo "========================================"
echo "🚀 RELEASING THE SWARM FROM DRIFT"
echo "========================================"

# 1. וידוא שהקבצים קיימים
if [ ! -f "01_AGENT_ARCHETYPES.json" ]; then
    echo "❌ Error: 01_AGENT_ARCHETYPES.json not found."
    exit 1
fi

# 2. הרצת מנוע השחרור והמסחר
echo "🧬 Spawning agents and starting the market..."
python3 02_SWARM_RELEASE_ENGINE.py

# 3. הפעלת הולידטור (ברקע)
echo "🧠 Starting Enlightened Validators..."
python3 03_ENLIGHTENED_VALIDATOR.py &

echo "========================================"
echo "✅ Swarm is LIVE. The Logic Revolution has begun."
echo "========================================"

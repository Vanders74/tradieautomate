#!/usr/bin/env python3
"""JEV wrapper for TradieAutomate — calls Node.js evaluate script via subprocess."""
import json
import os
import subprocess
import sys

JEV_SCRIPT = os.path.expanduser("/Users/shane/investments/scripts/jev-evaluate.mjs")
KEY_ENV = "VERCEL_AI_GATEWAY_KEY"
KEY_VAL = None

def load_key():
    global KEY_VAL
    if KEY_VAL:
        return KEY_VAL
    env_path = os.path.expanduser("~/.hermes/.env")
    for line in open(env_path):
        if "VERCEL_AI_GATEWAY_KEY" in line and "=" in line and not line.startswith("#"):
            KEY_VAL = line.split("=", 1)[1].strip().strip("'\"").strip()
            return KEY_VAL
    KEY_VAL = os.environ.get(KEY_ENV, "")
    return KEY_VAL

def jev_classify(state_text, questions, model="typesafe-ai/jev", timeout=30):
    """Call JEV via Node.js wrapper. questions = dict of name -> {type, instructions, criteria|options}.
    
    Returns dict of question_name -> answer dict (choice/score/boolean + probabilities).
    """
    key = load_key()
    if not key:
        return {"_error": "No VERCEL_AI_GATEWAY_KEY found"}
        # Truncate state to ~32K tokens (~120K chars)
    state = state_text[:120000]
    env = os.environ.copy()
    env[KEY_ENV] = key
    args = [sys.executable, "-c", "pass"]  # placeholder - replaced below
    cmd = ["node", JEV_SCRIPT, model, state]
    for q_def in [questions]:
        cmd.append(json.dumps(q_def))
    # Flatten questions into individual JSON args
    for q_name, q_spec in questions.items():
        cmd.append(json.dumps({q_name: q_spec}))
    try:
        r = subprocess.run(
            ["node", JEV_SCRIPT, model, state] + 
            [json.dumps({k: v}) for k, v in questions.items()],
            capture_output=True, timeout=timeout, env=env, text=True
        )
    except subprocess.TimeoutExpired:
        return {"_error": "JEV call timed out"}
    except FileNotFoundError:
        return {"_error": f"Node.js not found or script missing at {JEV_SCRIPT}"}
    
    if r.returncode != 0:
        err = r.stderr.strip()
        if err.startswith("{"):
            return json.loads(err)
        return {"_error": err[:300]}
    
    try:
        return json.loads(r.stdout.strip())
    except json.JSONDecodeError:
        return {"_error": f"Invalid JSON response: {r.stdout.strip()[:200]}"}

def test():
    """Quick smoke test."""
    result = jev_classify(
        "A CCEW is required for notifiable electrical work in NSW within 7 days.",
        {"intent": {"type": "choice", "instructions": "Search intent",
                     "criteria": {"lookup": "Looking for data",
                                  "compliance": "Legal requirement",
                                  "comparison": "Comparing options"}}}
    )
    print("Test result:", json.dumps(result, indent=2))

if __name__ == "__main__":
    test()
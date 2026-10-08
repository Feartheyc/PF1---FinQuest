import streamlit as st

def init_game(persona):
    defaults = {
        "Student":  {"cash": 6000,   "savings": 2000,   "loan": 0, "investments": 1000, "stress": 25},
        "Farmer":   {"cash": 10000,  "savings": 5000,   "loan": 0, "investments": 1000, "stress": 10},
        "Employee": {"cash": 50000,  "savings": 20000,  "loan": 0, "investments": 1000, "stress": 40},
        "Founder":  {"cash": 100000, "savings": 20000,  "loan": 0, "investments": 1000, "stress": 60}
    }
    base = defaults.get(persona, defaults["Student"])
    return {
        "state": "MAP", 
        "persona": persona, 
        "event_index": 0,
        "cash": base['cash'], 
        "savings": base['savings'], 
        "loan": base['loan'],
        "investments": base['investments'], 
        "insurance": False,
        "confidence": 50, 
        "stress": base['stress'], 
        "regret": 0,
        "score_points": 100,  # Starting baseline prudence points
        "tech_skill": 0,
        "equity": 100,
        "history": [], 
        "last_feedback": None, 
        "feedback_type": "info", 
        "flags": {}
    }

def calculate_investable_pool(p):
    """
    Dynamic formula calculating investable surplus capital:
    Surplus = Base + (Savings * 0.4) + (Score * 250) * Stress Multiplier
    """
    stress_factor = max(0.1, (100 - p.get("stress", 0)) / 100.0)
    base = 1000
    savings_component = p.get("savings", 0) * 0.35
    score_component = max(0, p.get("score_points", 0)) * 250
    
    # Scale bonus based on persona scale
    persona_scale = {
        "Student": 0.2,
        "Farmer": 1.0,
        "Employee": 1.5,
        "Founder": 3.0
    }.get(p.get("persona", "Farmer"), 1.0)

    calculated = base + int((savings_component + score_component) * stress_factor * persona_scale)
    return max(1000, calculated)

def try_apply_effects(effects):
    p = st.session_state.game
    savings_deduction = effects.get("savings", 0)
    cash_deduction = effects.get("cash", 0)

    if savings_deduction < 0 and p["savings"] + savings_deduction < 0:
        return False, "❌ Insufficient savings!"

    if cash_deduction < 0:
        amount = abs(cash_deduction)
        if p["cash"] < amount:
            remaining = amount - p["cash"]
            if p["savings"] - remaining < 0:
                return False, "❌ Insufficient capital!"

    if effects.get("insurance") is False:
        p["insurance"] = False
    elif effects.get("insurance") is True:
        p["insurance"] = True

    for k, v in effects.items():
        if k == "cash" and v < 0:
            amount = abs(v)
            if p["cash"] >= amount:
                p["cash"] -= amount
            else:
                remaining = amount - p["cash"]
                p["cash"] = 0
                p["savings"] -= remaining
        elif k == "add_flag":
            p["flags"][v] = True
        elif k not in ("insurance", "__msg"):
            if k in p:
                p[k] += v

    # Stress clamp between 0% and 100%
    if "stress" in p:
        p["stress"] = max(0, min(100, p["stress"]))

    # Dynamic recalculation of investment power based on score and low stress
    p["investments"] = calculate_investable_pool(p)

    return True, "✅ Decision Recorded"
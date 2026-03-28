# ==================================================
# bot_gate_funktions.py
# Entry / Gate / Strategie Mechanik außerhalb von bot.py
# ==================================================
from config import Config
from debug_reader import dbr_debug

DEBUG = True
# --------------------------------------------------


def evaluate_entry_decision(bot, window, candle_state):

    # --------------------------------------------------
    # DUMMY ENTRY-SLOT
    # --------------------------------------------------
    # Erwartete Struktur für später:
    # decision = {
    #     "allow": True,
    #     "side": "LONG" oder "SHORT",
    #     "entry_price": float,
    #     "sl_price": float,
    #     "tp_price": float,
    # }
    decision = None

    if decision is None:
        return None

    if not decision.get("allow", False):
        return None

    side = str(decision.get("side", "")).upper().strip()
    entry_price = float(decision.get("entry_price", 0.0) or 0.0)
    sl_price = float(decision.get("sl_price", 0.0) or 0.0)
    tp_price = float(decision.get("tp_price", 0.0) or 0.0)

    if side not in ("LONG", "SHORT"):
        return None

    if entry_price <= 0.0 or sl_price <= 0.0 or tp_price <= 0.0:
        return None

    risk = abs(entry_price - sl_price)
    if risk <= 0.0:
        return None

    rr_value = abs(tp_price - entry_price) / risk
    

    return {
        "decision": side,
        "entry_price": entry_price,
        "tp_price": tp_price,
        "sl_price": sl_price,
        "rr_value": rr_value,
    }



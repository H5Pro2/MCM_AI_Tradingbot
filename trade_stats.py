# ==================================================
# trade_stats.py
# ==================================================
# PERSISTENTE TRADE-STATISTIK
# - wird vom Bot bei EXIT aufgerufen
# - speichert aggregierte Werte in JSON
# - keine Abhängigkeit vom Bot-State
# ==================================================

import json
import os
from config import Config

class TradeStats:
    def __init__(self, path="debug/trade_stats.json", csv_path="debug/trade_equity.csv", reset=True):
        from ph_ohlcv import create_exchange, get_account_value

        self.path = path
        self.csv_path = csv_path

        if str(getattr(Config, "MODE", "LIVE")).upper() == "LIVE":
            try:
                exchange = create_exchange()
                start_equity = float(get_account_value(exchange, Config.USDT))
            except Exception:
                start_equity = float(getattr(Config, "START_EQUITY", 0.0) or 0.0)
        else:
            start_equity = float(getattr(Config, "START_EQUITY", 0.0) or 0.0)

        self.data = {
            "trades": 0,
            "tp": 0,
            "sl": 0,
            "cancels": 0,
            "attempts": 0,
            "attempts_submitted": 0,
            "attempts_filled": 0,
            "attempts_cancelled": 0,
            "attempts_blocked": 0,
            "attempts_skipped": 0,
            "attempt_structure_zone": 0,
            "attempt_non_structure_zone": 0,
            "pnl_netto": start_equity,
            "pnl_tp": 0.0,
            "pnl_sl": 0.0,
            "current_timestamp": None,
            "last_outcome_decomposition": {},
            "recent_attempts": [],
        }

        if reset:
            # JSON zurücksetzen
            self._save()

            # CSV bei Neustart überschreiben
            if os.path.exists(self.csv_path):
                try:
                    os.remove(self.csv_path)
                except Exception:
                    pass
        else:
            self._load()

    # ─────────────────────────────────────────────
    def _load(self):
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                obj = json.load(f)
                if isinstance(obj, dict):
                    self.data.update(obj)
        except Exception:
            pass

    # ─────────────────────────────────────────────
    def _save(self):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass

    # ─────────────────────────────────────────────
    def _extract_structure_quality(self, context: dict) -> float:
        ctx = dict(context or {})
        world_state = dict(ctx.get("world_state", {}) or {})
        structure = dict(ctx.get("structure_perception_state", {}) or {})
        if not structure and isinstance(world_state.get("structure_perception_state"), dict):
            structure = dict(world_state.get("structure_perception_state", {}) or {})
        if not structure and isinstance(ctx.get("outer_visual_perception_state"), dict):
            structure = dict(ctx.get("outer_visual_perception_state", {}) or {})
        try:
            return float(structure.get("structure_quality", 0.0) or 0.0)
        except Exception:
            return 0.0

    # ─────────────────────────────────────────────
    def on_attempt(self, *, status: str, context: dict = None):
        status_key = str(status or "").strip().lower()

        self.data["attempts"] = int(self.data.get("attempts", 0) or 0) + 1
        if status_key == "submitted":
            self.data["attempts_submitted"] = int(self.data.get("attempts_submitted", 0) or 0) + 1
        elif status_key == "filled":
            self.data["attempts_filled"] = int(self.data.get("attempts_filled", 0) or 0) + 1
        elif status_key == "cancelled":
            self.data["attempts_cancelled"] = int(self.data.get("attempts_cancelled", 0) or 0) + 1
        elif status_key in ("blocked", "blocked_value_gate"):
            self.data["attempts_blocked"] = int(self.data.get("attempts_blocked", 0) or 0) + 1
        elif status_key == "skipped":
            self.data["attempts_skipped"] = int(self.data.get("attempts_skipped", 0) or 0) + 1

        structure_quality = self._extract_structure_quality(context or {})
        if structure_quality >= 0.55:
            self.data["attempt_structure_zone"] = int(self.data.get("attempt_structure_zone", 0) or 0) + 1
            structure_bucket = "zone"
        else:
            self.data["attempt_non_structure_zone"] = int(self.data.get("attempt_non_structure_zone", 0) or 0) + 1
            structure_bucket = "non_zone"

        recent = list(self.data.get("recent_attempts", []) or [])
        recent.append(
            {
                "status": status_key or "unknown",
                "structure_quality": float(structure_quality),
                "structure_bucket": structure_bucket,
            }
        )
        self.data["recent_attempts"] = recent[-200:]
        self._save()

    # ─────────────────────────────────────────────
    def on_exit(self, *, entry: float, tp: float, sl: float, reason: str, side: str = None, amount: float = 1.0, exploration_trade: bool = False, outcome_decomposition: dict = None):
        pnl = 0.0

        side = str(side).upper().strip() if side is not None else "LONG"

        if reason == "tp_hit":
            if side == "LONG":
                pnl = (tp - entry) * float(amount)
            elif side == "SHORT":
                pnl = (entry - tp) * float(amount)
            else:
                return
            self.data["tp"] += 1

            if exploration_trade:
                self.data["exploration_tp"] = int(self.data.get("exploration_tp", 0) or 0) + 1

        elif reason == "sl_hit":
            if side == "LONG":
                pnl = (sl - entry) * float(amount)
            elif side == "SHORT":
                pnl = (entry - sl) * float(amount)
            else:
                return
            self.data["sl"] += 1

            if exploration_trade:
                self.data["exploration_sl"] = int(self.data.get("exploration_sl", 0) or 0) + 1

        else:
            return

        # Fees berücksichtigen
        # pnl = pnl - Config.FEE_PER_TRADE

        # Fees berücksichtigen (prozentual pro Seite + optional fixer Abzug)
        exit_price = tp if reason == "tp_hit" else sl
        fee_rate = getattr(Config, "FEE_RATE", 0.0) or 0.0
        fees = (
            (entry * float(amount) * fee_rate) +
            (exit_price * float(amount) * fee_rate) +
            (Config.FEE_PER_TRADE or 0.0)
        )
        pnl = pnl - fees

        self.data["trades"] += 1
        self.data["last_outcome_decomposition"] = dict(outcome_decomposition or {})

        if exploration_trade:
            self.data["exploration_trades"] = int(self.data.get("exploration_trades", 0) or 0) + 1
            self.data["exploration_pnl"] = float(self.data.get("exploration_pnl", 0.0) or 0.0) + float(pnl)

        # GESAMT = Summe aller Trades (Gewinn + Verlust)
        self.data["pnl_netto"] += pnl

        # GEWINN = Summe nur positiver Trades
        if pnl > 0:
            self.data["pnl_tp"] += pnl

        # VERLUST = Summe nur negativer Trades
        if pnl < 0:
            self.data["pnl_sl"] += pnl

        self._save()

        # ---------------- CSV Equity Export ----------------
        try:
            os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)

            write_header = not os.path.exists(self.csv_path)

            with open(self.csv_path, "a", encoding="utf-8") as f:
                if write_header:
                    f.write("trade,pnl_netto,pnl_tp,pnl_sl\n")

                f.write(
                    f"{self.data['trades']},"
                    f"{self.data['pnl_netto']},"
                    f"{self.data['pnl_tp']},"
                    f"{self.data['pnl_sl']}\n"
                )
        except Exception:
            pass

    # ─────────────────────────────────────────────
    # Snapshot mit zusätzlichen Kennzahlen
    # ─────────────────────────────────────────────
    def snapshot(self) -> dict:
        """
        Aktuellen Stand zurückgeben (read-only Kopie)
        """
        data = dict(self.data)

        trades = data.get("trades", 0)
        pnl_tp = data.get("pnl_tp", 0.0)
        pnl_sl = data.get("pnl_sl", 0.0)

        avg_win = (pnl_tp / data.get("tp", 1)) if data.get("tp", 0) > 0 else 0.0
        avg_loss = (pnl_sl / data.get("sl", 1)) if data.get("sl", 0) > 0 else 0.0

        profit_factor = (
            abs(pnl_tp / pnl_sl)
            if pnl_sl != 0
            else 0.0
        )

        expectancy = (
            (data.get("pnl_netto", 0.0) / trades)
            if trades > 0
            else 0.0
        )

        exploration_trades = int(data.get("exploration_trades", 0) or 0)
        exploration_tp = int(data.get("exploration_tp", 0) or 0)
        exploration_sl = int(data.get("exploration_sl", 0) or 0)
        exploration_pnl = float(data.get("exploration_pnl", 0.0) or 0.0)

        exploration_avg = (
            exploration_pnl / exploration_trades
            if exploration_trades > 0
            else 0.0
        )

        data.update({
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "profit_factor": profit_factor,
            "expectancy": expectancy,
            "exploration_avg": exploration_avg,
            "normal_trades": max(0, trades - exploration_trades),
            "normal_tp": max(0, int(data.get("tp", 0) or 0) - exploration_tp),
            "normal_sl": max(0, int(data.get("sl", 0) or 0) - exploration_sl),
            "normal_cancels": max(0, int(data.get("cancels", 0) or 0) - int(data.get("exploration_cancels", 0) or 0)),
            "attempts_per_trade": (
                float(data.get("attempts", 0) or 0) / max(1, int(trades))
            ),
            "attempt_zone_share": (
                float(data.get("attempt_structure_zone", 0) or 0) / max(1, int(data.get("attempts", 0) or 0))
            ),
            "attempt_fill_rate": (
                float(data.get("attempts_filled", 0) or 0) / max(1, int(data.get("attempts", 0) or 0))
            ),
        })

        return data
    # ─────────────────────────────────────────────
    def on_cancel(self, *, order_id=None, cause: str = None, exploration_trade: bool = False, outcome_decomposition: dict = None):
        """
        Order wurde gecancelt bevor ein Trade/Exit stattgefunden hat.
        Keine PnL-Änderung – nur Zählung.
        """
        try:
            self.data["cancels"] = int(self.data.get("cancels", 0) or 0) + 1
            self.data["last_outcome_decomposition"] = dict(outcome_decomposition or {})
            if exploration_trade:
                self.data["exploration_cancels"] = int(self.data.get("exploration_cancels", 0) or 0) + 1

            self._save()
        except Exception:
            pass

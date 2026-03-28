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
            "pnl_netto": start_equity,
            "pnl_tp": 0.0,
            "pnl_sl": 0.0,
            "current_timestamp": None,
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
    def on_exit(self, *, entry: float, tp: float, sl: float, reason: str, side: str = None, amount: float = 1.0, exploration_trade: bool = False):
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
        })

        return data
    # ─────────────────────────────────────────────
    def on_cancel(self, *, order_id=None, cause: str = None, exploration_trade: bool = False):
        """
        Order wurde gecancelt bevor ein Trade/Exit stattgefunden hat.
        Keine PnL-Änderung – nur Zählung.
        """
        try:
            self.data["cancels"] = int(self.data.get("cancels", 0) or 0) + 1

            if exploration_trade:
                self.data["exploration_cancels"] = int(self.data.get("exploration_cancels", 0) or 0) + 1

            self._save()
        except Exception:
            pass

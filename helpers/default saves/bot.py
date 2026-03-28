# ==================================================
# bot.py
# Pipeline:
# OHLC
# -> Exit / Pending Handling
# -> Dummy Entry Slot
# -> TradeValueGate
# -> Order / Pending Entry
# ==================================================
from config import Config
from csv_feed import CSVFeed
from trade_stats import TradeStats
from bot_engine.exit_engine import ExitEngine
from bot_gates.trade_value_gate import TradeValueGate
from place_orders import place_order, consume_cancelled, get_active_order_snapshot, is_order_active
from debug_reader import dbr_debug
from ph_ohlcv import _build_candle_state
from bot_gate_funktions import evaluate_entry_decision


DEBUG = True
# --------------------------------------------------


class Bot:

    def __init__(self, filepath: str):
        self.feed = CSVFeed(filepath)
        self.exit_engine = ExitEngine()
        self.value_gate = TradeValueGate()
        self.stats = TradeStats(
            path="debug/trade_stats.json",
            csv_path="debug/trade_equity.csv",
            reset=True,
        )

        self.position = None
        self.pending_entry = None
        self.processed = 0
        self.current_timestamp = None

        snapshot = get_active_order_snapshot()

        if snapshot:
            print("RESTART RECOVERY → ACTIVE ORDER FOUND")

            entry = float(snapshot["entry"])
            sl = float(snapshot["sl"])
            risk = abs(entry - sl)

            self.position = {
                "side": snapshot["side"],
                "entry": entry,
                "tp": float(snapshot["tp"]),
                "sl": sl,
                "mfe": 0.0,
                "mae": 0.0,
                "risk": risk,
                "order_id": snapshot.get("id"),
                "entry_ts": snapshot.get("entry_ts"),
                "entry_index": None,
                "last_checked_ts": snapshot.get("entry_ts"),
                "meta": {},
            }

    # ==================================================
    # INTERNE PIPELINE (NUR WINDOW → LOGIK)
    # ==================================================
    def _process_window(self, window):

        # --------------------------------------------------
        # Restart Recovery → Timestamp initialisieren
        # --------------------------------------------------
        if self.position and self.position.get("entry_ts") is None:
            ts = window[-1].get("timestamp")
            self.position["entry_ts"] = ts
            self.position["last_checked_ts"] = ts

        # ------------------------
        # LIVE / BACKTEST Modus prüfen
        # ------------------------
        live_mode = str(getattr(Config, "MODE", "LIVE")).upper() == "LIVE"
        if live_mode and self.position is None:
            if is_order_active():
                if DEBUG:
                    dbr_debug("EXIT: ORDER_ACTIVE_BLOCK", "live_backtest_debug.txt")
                return

        self.current_timestamp = window[-1].get("timestamp")
        self.stats.data["current_timestamp"] = self.current_timestamp
        self.stats._save()

        last = window[-1]
        prev_close = window[-2].get("close") if len(window) > 1 else None
        candle_state = _build_candle_state(last, prev_close=prev_close)

        # --------------------------------------------------------------------------------------------------------------------------
        # EXIT (immer zuerst)
        # --------------------------------------------------------------------------------------------------------------------------
        if self.position is not None:

            entry_price = float(self.position.get("entry", 0.0) or 0.0)
            side = str(self.position.get("side", "")).upper().strip()

            self.current_timestamp = window[-1]["timestamp"]

            high = float(last["high"])
            low = float(last["low"])

            if side == "LONG":
                favorable = max(0.0, high - entry_price)
                adverse = max(0.0, entry_price - low)
            else:
                favorable = max(0.0, entry_price - low)
                adverse = max(0.0, high - entry_price)

            self.position["mfe"] = max(float(self.position.get("mfe", 0.0) or 0.0), favorable)
            self.position["mae"] = max(float(self.position.get("mae", 0.0) or 0.0), adverse)

            exit_signal = self.exit_engine.process(
                window,
                self.position,
                "trading_debug.txt",
            )
            if exit_signal is None:
                return

            reason = exit_signal.get("reason")
            if reason is None:
                return

            if live_mode and Config.AKTIV_ORDER:
                oid = self.position.get("order_id")
                if oid is not None and consume_cancelled(oid):
                    self.stats.on_cancel(
                        order_id=oid,
                        cause="exchange_cancel",
                        exploration_trade=False,
                    )
                    self.position = None
                    return

            self.stats.on_exit(
                entry=self.position.get("entry"),
                tp=self.position.get("tp"),
                sl=self.position.get("sl"),
                reason=reason,
                side=self.position.get("side"),
                amount=Config.ORDER_SIZE if live_mode else 1.0,
                exploration_trade=False,
            )

            self.position = None
            return

        # --------------------------------------------------------------------------------------------------------------------------
        # Pending Entry Fill prüfen (BACKTEST)
        # --------------------------------------------------------------------------------------------------------------------------
        if (not live_mode) and self.pending_entry is not None and self.position is None:

            side = self.pending_entry["side"]
            entry_price = self.pending_entry["entry"]
            tp_price = self.pending_entry["tp"]
            sl_price = self.pending_entry["sl"]

            created = self.pending_entry["created_index"]
            max_wait = self.pending_entry["max_wait_bars"]

            last = window[-1]
            high = float(last["high"])
            low = float(last["low"])

            # --------------------------------------------------
            # REALISTISCHER ENTRY FILL
            # --------------------------------------------------
            open_price = float(last["open"])

            if side == "LONG" and open_price >= entry_price and low <= entry_price:

                risk = abs(entry_price - sl_price)

                self.position = {
                    "side": side,
                    "entry": entry_price,
                    "tp": tp_price,
                    "sl": sl_price,
                    "mfe": 0.0,
                    "mae": 0.0,
                    "risk": float(risk),
                    "order_id": None,
                    "entry_ts": last.get("timestamp"),
                    "entry_index": self.processed,
                    "last_checked_ts": last.get("timestamp"),
                    "meta": {},
                }

                self.pending_entry = None
                return

            if side == "SHORT" and open_price <= entry_price and high >= entry_price:

                risk = abs(entry_price - sl_price)

                self.position = {
                    "side": side,
                    "entry": entry_price,
                    "tp": tp_price,
                    "sl": sl_price,
                    "mfe": 0.0,
                    "mae": 0.0,
                    "risk": float(risk),
                    "order_id": None,
                    "entry_ts": last.get("timestamp"),
                    "entry_index": self.processed,
                    "last_checked_ts": last.get("timestamp"),
                    "meta": {},
                }

                self.pending_entry = None
                return

            # --------------------------------------------------
            # Timeout Cancel
            # --------------------------------------------------
            if (self.processed - created) > max_wait:

                self.stats.on_cancel(
                    order_id=None,
                    cause="backtest_timeout",
                    exploration_trade=False,
                )

                self.pending_entry = None
                return

        # ------------------------------------------------------------------------------------------------------------------------------------------------
        if self.position is None and self.pending_entry is None:

            # --------------------------------------------------
            # DUMMY ENTRY-SLOT
            # --------------------------------------------------
            entry_result = evaluate_entry_decision(
                self,
                window,
                candle_state,
            )


            print(entry_result)


            if entry_result is None:
                return            


            # --------------------------------------------------
            # Ökonomische Prüfung (RR / Mindestabstand)
            # --------------------------------------------------
            value_check = self.value_gate.evaluate(entry_result)

            if DEBUG:
                dbr_debug(f"VALUE_GATE: {value_check}", "value_check_debug.txt")

            if not value_check.get("trade_allowed", False):
                return

            order_side = "sell" if side == "SHORT" else "buy"

            # --------------------------------------------------
            # RR Execution Filter (LIVE)
            # --------------------------------------------------
            order_id = None
            is_memory_trade = False
            rr_exec_min = float(getattr(Config, "RR_EXECUTION_MIN", 1.2) or 1.2)

            if live_mode and Config.AKTIV_ORDER and entry_result("rr_value") < rr_exec_min:
                is_memory_trade = True

            # --------------------------------------------------
            # Exchange Order (LIVE)
            # --------------------------------------------------
            if live_mode and Config.AKTIV_ORDER and not is_memory_trade:
                order_id = place_order(
                    order_type=order_side,
                    price=entry_price,
                    amount=Config.ORDER_SIZE,
                    open_orders=None,
                    tp=tp_price,
                    sl=sl_price,
                    params={},
                )

                if order_id is None:
                    return

            self.pending_entry = {
                "side": side,
                "entry": entry_price,
                "tp": tp_price,
                "sl": sl_price,
                "risk": float(risk),
                "created_index": self.processed,
                "max_wait_bars": int(getattr(Config, "PENDING_ENTRY_MAX_WAIT_BARS", 20) or 20),
                "meta": {},
            }

            return

    # ==================================================
    # MODUS 1: ROW-MODUS (internes Rolling)
    # ==================================================
    def run_rows(self, window_size: int = 2, delay_seconds: float = 0.0):
        buffer = []
        self.processed = 0

        for row in self.feed.rows(delay_seconds=delay_seconds):
            buffer.append(row)

            if len(buffer) < window_size:
                continue

            if len(buffer) > window_size:
                buffer.pop(0)

            self._process_window(buffer)
            self.processed += 1

    # ==================================================
    # MODUS 2: WINDOW-MODUS (direkt vom Feed)
    # ==================================================
    def run_window(self, size: int, delay_seconds: float = 0.0):
        if not hasattr(self, "processed"):
            self.processed = 0

        processed = 0

        for window in self.feed.window(size, delay_seconds=delay_seconds):
            self._process_window(window)
            processed += 1
            self.processed += 1

        return processed
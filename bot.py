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
from MCM_Brain_Modell import apply_outcome_stimulus
from memory_state import apply_memory_state, read_memory_state, save_memory_state


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

        self.mcm_brain = None
        self.mcm_last_state = None
        self.mcm_last_action = None
        self.mcm_last_attractor = None
        self.mcm_snapshot = None
        self.mcm_pause_left = 0

        self.focus_point = None
        self.focus_confidence = 0.0
        self.target_lock = 0.0
        self.target_drift = 0.0

        self.entry_expectation = 0.0
        self.target_expectation = 0.0
        self.approach_pressure = 0.0
        self.pressure_release = 0.0
        self.experience_regulation = 0.0
        self.reflection_maturity = 0.0
        self.load_bearing_capacity = 0.0
        self.protective_width_regulation = 0.0
        self.protective_courage = 0.0

        self.signature_memory = {}
        self.last_signature_key = None
        self.last_signature_outcome = None
        self.last_signature_context = None

        self.context_clusters = {}
        self.context_cluster_seq = 0
        self.last_context_cluster_id = None
        self.last_context_cluster_key = None

        self.inhibition_level = 0.0
        self.habituation_level = 0.0
        self.competition_bias = 0.0
        self.observation_mode = False
        self.last_signal_relevance = 0.0

        self.perception_state = {}
        self.outer_visual_perception_state = {}
        self.inner_field_perception_state = {}
        self.processing_state = {}
        self.felt_state = {}
        self.thought_state = {}
        self.meta_regulation_state = {}
        self.last_outcome_decomposition = {}

        self._memory_state_payload = read_memory_state()
        self._memory_state_mcm_loaded = False
        apply_memory_state(self, self._memory_state_payload)
        self._memory_state_mcm_loaded = isinstance(self.mcm_brain, dict)
        
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
    # MEMORY STATE
    # ==================================================
    def _ensure_memory_state_loaded(self):

        if self._memory_state_mcm_loaded:
            return

        if not isinstance(self.mcm_brain, dict):
            return

        apply_memory_state(self, self._memory_state_payload)
        self._memory_state_mcm_loaded = True

    def _save_memory_state(self):

        payload = save_memory_state(self)

        if payload is None:
            return None

        self._memory_state_payload = payload
        self._memory_state_mcm_loaded = isinstance(self.mcm_brain, dict)
        return payload
            
    # ==================================================
    # INTERNE PIPELINE (NUR WINDOW → LOGIK)
    # ==================================================
    def _process_window(self, window):

        self._ensure_memory_state_loaded()

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
                    dbr_debug("EXIT: ORDER_ACTIVE_BLOCK", "live_backtest_debug.csv")
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
                "exit_trading_debug.csv",
            )
            if exit_signal is None:
                return

            reason = exit_signal.get("reason")
            if reason is None:
                return

            if live_mode and Config.AKTIV_ORDER:
                oid = self.position.get("order_id")
                if oid is not None and consume_cancelled(oid):
                    apply_outcome_stimulus(self, "cancel", self.position)
                    self._save_memory_state()
                    self.stats.on_cancel(
                        order_id=oid,
                        cause="exchange_cancel",
                        exploration_trade=False,
                        outcome_decomposition=dict(getattr(self, "last_outcome_decomposition", {}) or {}),
                    )
                    self.position = None
                    return

            apply_outcome_stimulus(self, reason, self.position)
            self._save_memory_state()
            if str(reason).lower() == "sl_hit":
                self.mcm_pause_left = int(getattr(Config, "MCM_SL_PAUSE_STEPS", 3) or 3)

            self.stats.on_exit(
                entry=self.position.get("entry"),
                tp=self.position.get("tp"),
                sl=self.position.get("sl"),
                reason=reason,
                side=self.position.get("side"),
                amount=Config.ORDER_SIZE if live_mode else 1.0,
                exploration_trade=False,
                outcome_decomposition=dict(getattr(self, "last_outcome_decomposition", {}) or {}),
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
            meta = dict(self.pending_entry.get("meta", {}) or {})
            trade_plan = dict(meta.get("trade_plan", {}) or {})
            entry_validity_band = dict(trade_plan.get("entry_validity_band", {}) or {})

            validity_lower = entry_validity_band.get("lower")
            validity_upper = entry_validity_band.get("upper")

            try:
                validity_lower = float(validity_lower) if validity_lower is not None else None
            except Exception:
                validity_lower = None

            try:
                validity_upper = float(validity_upper) if validity_upper is not None else None
            except Exception:
                validity_upper = None

            # --------------------------------------------------
            # REALISTISCHER ENTRY FILL
            # --------------------------------------------------
            entry_touched = low <= entry_price <= high
            validity_touched = False

            if validity_lower is not None and validity_upper is not None:
                validity_touched = high >= validity_lower and low <= validity_upper

            fill_price = float(entry_price)

            if (not entry_touched) and validity_touched:
                fill_price = float(min(max(entry_price, low), high))

            if side == "LONG" and (entry_touched or validity_touched):

                risk = abs(fill_price - sl_price)

                self.position = {
                    "side": side,
                    "entry": float(fill_price),
                    "tp": tp_price,
                    "sl": sl_price,
                    "mfe": 0.0,
                    "mae": 0.0,
                    "risk": float(risk),
                    "order_id": None,
                    "entry_ts": last.get("timestamp"),
                    "entry_index": self.processed,
                    "last_checked_ts": last.get("timestamp"),
                    "meta": meta,
                }

                self.pending_entry = None
                return

            if side == "SHORT" and (entry_touched or validity_touched):

                risk = abs(fill_price - sl_price)

                self.position = {
                    "side": side,
                    "entry": float(fill_price),
                    "tp": tp_price,
                    "sl": sl_price,
                    "mfe": 0.0,
                    "mae": 0.0,
                    "risk": float(risk),
                    "order_id": None,
                    "entry_ts": last.get("timestamp"),
                    "entry_index": self.processed,
                    "last_checked_ts": last.get("timestamp"),
                    "meta": meta,
                }

                self.pending_entry = None
                return

            # --------------------------------------------------
            # Timeout Cancel
            # --------------------------------------------------
            if (self.processed - created) > max_wait:

                apply_outcome_stimulus(self, "timeout", self.pending_entry)
                self._save_memory_state()
                self.stats.on_cancel(
                    order_id=None,
                    cause="backtest_timeout",
                    exploration_trade=False,
                )

                self.pending_entry = None
                return

        # ------------------------------------------------------------------------------------------------------------------------------------------------
        if self.position is None and self.pending_entry is None:

            if int(getattr(self, "mcm_pause_left", 0) or 0) > 0:
                self.mcm_pause_left -= 1

            # --------------------------------------------------
            # DUMMY ENTRY-SLOT
            # --------------------------------------------------
            entry_result = evaluate_entry_decision(
                self,
                window,
                candle_state,
            )

            if entry_result is None:
                return

            # --------------------------------------------------
            # Ökonomische Prüfung (RR / Mindestabstand)
            # --------------------------------------------------
            value_check = self.value_gate.evaluate(entry_result)

            if DEBUG:
                dbr_debug(f"VALUE_GATE: {value_check}", "value_check_debug.csv")

            if not value_check.get("trade_allowed", False):
                apply_outcome_stimulus(
                    self,
                    value_check.get("reason"),
                    entry_result,
                )
                self._save_memory_state()
                return

            side = str(entry_result.get("decision", "")).upper().strip()
            entry_price = float(entry_result.get("entry_price", 0.0) or 0.0)
            tp_price = float(entry_result.get("tp_price", 0.0) or 0.0)
            sl_price = float(entry_result.get("sl_price", 0.0) or 0.0)
            risk = abs(entry_price - sl_price)

            if side not in ("LONG", "SHORT"):
                return

            if entry_price <= 0.0 or tp_price <= 0.0 or sl_price <= 0.0 or risk <= 0.0:
                return

            order_side = "sell" if side == "SHORT" else "buy"

            # --------------------------------------------------
            # RR Execution Filter (LIVE)
            # --------------------------------------------------
            order_id = None
            is_memory_trade = False
            rr_exec_min = float(getattr(Config, "RR_EXECUTION_MIN", 1.2) or 1.2)

            if live_mode and Config.AKTIV_ORDER and float(entry_result.get("rr_value", 0.0) or 0.0) < rr_exec_min:
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
                    params={
                        "_entry_reference": entry_price,
                        "_entry_distance": abs(entry_price - float(last.get("close", entry_price) or entry_price)),
                        "_risk_reference": risk,
                        "_entry_validity_band": dict(entry_result.get("entry_validity_band", {}) or {}),
                    },
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
                "meta": {
                    "state": {
                        "energy": float(entry_result.get("energy", 0.0) or 0.0),
                        "coherence": float(entry_result.get("coherence", 0.0) or 0.0),
                        "asymmetry": int(entry_result.get("asymmetry", 0) or 0),
                        "coh_zone": float(entry_result.get("coh_zone", 0.0) or 0.0),
                        "self_state": str(entry_result.get("self_state", "stable") or "stable"),
                        "attractor": str(entry_result.get("attractor", "neutral") or "neutral"),
                        "memory_center": float(entry_result.get("memory_center", 0.0) or 0.0),
                        "memory_strength": int(entry_result.get("memory_strength", 0) or 0),
                    },
                    "focus": {
                        "focus_point": float(self.focus_point or 0.0),
                        "focus_confidence": float(self.focus_confidence or 0.0),
                        "target_lock": float(self.target_lock or 0.0),
                        "target_drift": float(self.target_drift or 0.0),
                    },
                    "experience": {
                        "entry_expectation": float(entry_result.get("entry_expectation", 0.0) or 0.0),
                        "target_expectation": float(entry_result.get("target_expectation", 0.0) or 0.0),
                        "approach_pressure": float(entry_result.get("approach_pressure", 0.0) or 0.0),
                        "pressure_release": float(entry_result.get("pressure_release", 0.0) or 0.0),
                        "experience_regulation": float(entry_result.get("experience_regulation", 0.0) or 0.0),
                        "reflection_maturity": float(entry_result.get("reflection_maturity", 0.0) or 0.0),
                    },
                    "vision": dict(entry_result.get("vision", {}) or {}),
                    "filtered_vision": dict(entry_result.get("filtered_vision", {}) or {}),
                    "world_state": dict(entry_result.get("world_state", {}) or {}),
                    "outer_visual_perception_state": dict(entry_result.get("outer_visual_perception_state", {}) or {}),
                    "inner_field_perception_state": dict(entry_result.get("inner_field_perception_state", {}) or {}),
                    "processing_state": dict(entry_result.get("processing_state", {}) or {}),
                    "state_signature": dict(entry_result.get("state_signature", {}) or {}),
                    "trade_plan": {
                        "entry_validity_band": dict(entry_result.get("entry_validity_band", {}) or {}),
                        "target_conviction": float(entry_result.get("target_conviction", 0.0) or 0.0),
                        "risk_model_score": float(entry_result.get("risk_model_score", 0.0) or 0.0),
                        "reward_model_score": float(entry_result.get("reward_model_score", 0.0) or 0.0),
                    },
                    "signal": {
                        "signature_bias": float(entry_result.get("signature_bias", 0.0) or 0.0),
                        "signature_block": bool(entry_result.get("signature_block", False)),
                        "signature_quality": float(entry_result.get("signature_quality", 0.0) or 0.0),
                        "signature_distance": float(entry_result.get("signature_distance", 0.0) or 0.0),
                        "context_cluster_id": str(entry_result.get("context_cluster_id", "-") or "-"),
                        "context_cluster_bias": float(entry_result.get("context_cluster_bias", 0.0) or 0.0),
                        "context_cluster_quality": float(entry_result.get("context_cluster_quality", 0.0) or 0.0),
                        "context_cluster_distance": float(entry_result.get("context_cluster_distance", 0.0) or 0.0),
                        "context_cluster_block": bool(entry_result.get("context_cluster_block", False)),
                        "inhibition_level": float(entry_result.get("inhibition_level", 0.0) or 0.0),
                        "habituation_level": float(entry_result.get("habituation_level", 0.0) or 0.0),
                        "competition_bias": float(entry_result.get("competition_bias", 0.0) or 0.0),
                        "observation_mode": bool(entry_result.get("observation_mode", False)),
                        "long_score": float(entry_result.get("long_score", 0.0) or 0.0),
                        "short_score": float(entry_result.get("short_score", 0.0) or 0.0),
                    },
                },
            }

            self._save_memory_state()
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
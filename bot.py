# ==================================================
# bot.py
# Pipeline:
# OHLC
# -> Exit / Pending Handling
# -> Dummy Entry Slot
# -> TradeValueGate
# -> Order / Pending Entry
# ==================================================
import queue
import threading

from config import Config
from csv_feed import CSVFeed
from trade_stats import TradeStats
from bot_engine.exit_engine import ExitEngine
from bot_engine.mcm_core_engine import build_tension_state_from_window
from bot_engine.strukture_engine import StructureEngine
from bot_gates.trade_value_gate import TradeValueGate

from place_orders import place_order, consume_cancelled, get_active_order_snapshot, is_order_active
from debug_reader import dbr_debug
from ph_ohlcv import _build_candle_state
from bot_gate_funktions import evaluate_entry_decision
from MCM_Brain_Modell import apply_outcome_stimulus, create_mcm_brain, create_mcm_runtime, mark_runtime_episode_event, step_mcm_runtime, step_mcm_runtime_idle
from memory_state import apply_memory_state, read_memory_state, save_memory_state


DEBUG = True
STRUCTURE_ENGINE = StructureEngine()
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

        self.mcm_brain = create_mcm_brain() if bool(getattr(Config, "MCM_ENABLED", True)) else None
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

        self.structure_perception_state = {}
        self.perception_state = {}
        self.outer_visual_perception_state = {}
        self.inner_field_perception_state = {}
        self.processing_state = {}
        self.expectation_state = {}
        self.felt_state = {}
        self.thought_state = {}
        self.meta_regulation_state = {}
        self.last_outcome_decomposition = {}

        self.mcm_runtime_snapshot = {}
        self.mcm_runtime_decision_state = {}
        self.mcm_runtime_brain_snapshot = {}
        self.mcm_runtime_market_ticks = 0
        self.mcm_episode_seq = 0
        self.mcm_decision_episode = {}
        self.mcm_decision_episode_internal = {}
        self.mcm_experience_space = {}
        self.mcm_last_observe_timestamp = None
        self.mcm_runtime = None

        self._memory_state_payload = read_memory_state()
        self._memory_state_mcm_loaded = False
        apply_memory_state(self, self._memory_state_payload)
        self._memory_state_mcm_loaded = isinstance(self.mcm_brain, dict)
        self.mcm_runtime = create_mcm_runtime(self)

        self._runtime_thread = None
        self._runtime_thread_lock = threading.Lock()
        self._runtime_stop_event = threading.Event()
        self._market_packet_queue = queue.Queue()
        self._runtime_idle_sleep = 0.25
        self._runtime_seeded = bool(self.mcm_runtime is not None and self.mcm_runtime.has_impulse())

        live_mode = str(getattr(Config, "MODE", "LIVE")).upper() == "LIVE"
        snapshot = None

        if live_mode and bool(getattr(Config, "AKTIV_ORDER", False)):
            snapshot = get_active_order_snapshot()

        if snapshot:
            entry_raw = snapshot.get("entry")
            tp_raw = snapshot.get("tp")
            sl_raw = snapshot.get("sl")

            try:
                entry = float(entry_raw)
            except Exception:
                entry = None

            try:
                tp_value = float(tp_raw) if tp_raw is not None else None
            except Exception:
                tp_value = None

            try:
                sl_value = float(sl_raw) if sl_raw is not None else None
            except Exception:
                sl_value = None

            if entry is not None and tp_value is not None and sl_value is not None:
                print("RESTART RECOVERY → ACTIVE ORDER FOUND")

                risk = abs(entry - sl_value)

                self.position = {
                    "side": snapshot.get("side"),
                    "entry": entry,
                    "tp": tp_value,
                    "sl": sl_value,
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
    # ENTSCHEIDUNGSBAHN
    # ==================================================
    def _handle_decision_tendency(self, entry_result: dict):

        result = dict(entry_result or {})
        decision_tendency = str(result.get("decision_tendency", "") or "").strip().lower()

        if decision_tendency == "act":
            return False

        if decision_tendency == "observe":
            event_name = "observed_only"
        elif decision_tendency == "replan":
            event_name = "replanned"
        else:
            event_name = "withheld"

        mark_runtime_episode_event(
            self,
            event_name,
            {
                "decision_tendency": str(decision_tendency or "hold"),
                "proposed_decision": str(result.get("proposed_decision", "WAIT") or "WAIT"),
                "reason": str(result.get("rejection_reason", "runtime_non_action") or "runtime_non_action"),
                "meta_regulation_state": dict(result.get("meta_regulation_state", {}) or {}),
                "expectation_state": dict(result.get("expectation_state", {}) or {}),
            },
        )
        return True
                    
    # ==================================================
    # HANDLUNGSBAHN
    # ==================================================
    def _handle_active_position(self, window, last, live_mode: bool):

        if self.position is None:
            return False

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

        mark_runtime_episode_event(
            self,
            "in_trade_updates",
            {
                "position": dict(self.position or {}),
                "mfe": float(self.position.get("mfe", 0.0) or 0.0),
                "mae": float(self.position.get("mae", 0.0) or 0.0),
            },
        )

        exit_signal = self.exit_engine.process(
            window,
            self.position,
            "exit_trading_debug.csv",
        )
        if exit_signal is None:
            return True

        reason = exit_signal.get("reason")
        if reason is None:
            return True

        position_context = dict(self.position.get("meta", {}) or {})
        resolved_position = dict(self.position or {})

        if live_mode and Config.AKTIV_ORDER:
            oid = self.position.get("order_id")
            if oid is not None and consume_cancelled(oid):
                apply_outcome_stimulus(self, "cancel", self.position)
                self.stats.on_attempt(
                    status="cancelled",
                    context=position_context,
                )
                mark_runtime_episode_event(
                    self,
                    "cancelled",
                    {
                        "position": dict(resolved_position or {}),
                        "reason": "exchange_cancel",
                    },
                )
                self.stats.on_cancel(
                    order_id=oid,
                    cause="exchange_cancel",
                    exploration_trade=False,
                    outcome_decomposition=dict(getattr(self, "last_outcome_decomposition", {}) or {}),
                    context=position_context,
                )
                self._save_memory_state()
                self.position = None
                return True

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
            context=position_context,
        )
        mark_runtime_episode_event(
            self,
            "resolved",
            {
                "position": dict(resolved_position or {}),
                "reason": str(reason or "-"),
            },
        )

        self.position = None
        return True

    # ==================================================
    def _handle_pending_entry(self, window, last, live_mode: bool):

        if self.pending_entry is None or self.position is not None:
            return False

        pending_meta = dict(self.pending_entry.get("meta", {}) or {})
        mark_runtime_episode_event(
            self,
            "in_trade_updates",
            {
                "pending_entry": dict(self.pending_entry or {}),
                "reason": "pending_watch",
            },
        )

        if live_mode:
            return True

        side = self.pending_entry["side"]
        entry_price = self.pending_entry["entry"]
        tp_price = self.pending_entry["tp"]
        sl_price = self.pending_entry["sl"]

        created = self.pending_entry["created_index"]
        max_wait = self.pending_entry["max_wait_bars"]

        high = float(last["high"])
        low = float(last["low"])
        trade_plan = dict(pending_meta.get("trade_plan", {}) or {})
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
                "meta": pending_meta,
            }

            self.pending_entry = None
            self.stats.on_attempt(
                status="filled",
                context=pending_meta,
            )
            mark_runtime_episode_event(
                self,
                "filled",
                {
                    "position": dict(self.position or {}),
                    "reason": "backtest_fill",
                },
            )
            self._save_memory_state()
            return True

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
                "meta": pending_meta,
            }

            self.pending_entry = None
            self.stats.on_attempt(
                status="filled",
                context=pending_meta,
            )
            mark_runtime_episode_event(
                self,
                "filled",
                {
                    "position": dict(self.position or {}),
                    "reason": "backtest_fill",
                },
            )
            self._save_memory_state()
            return True

        if (self.processed - created) > max_wait:

            pending_snapshot = dict(self.pending_entry or {})
            apply_outcome_stimulus(self, "timeout", self.pending_entry)
            self.stats.on_attempt(
                status="timeout",
                context=pending_meta,
            )
            mark_runtime_episode_event(
                self,
                "timeout",
                {
                    "pending_entry": dict(pending_snapshot or {}),
                    "reason": "backtest_timeout",
                },
            )
            self.stats.on_cancel(
                order_id=None,
                cause="backtest_timeout",
                exploration_trade=False,
                outcome_decomposition=dict(getattr(self, "last_outcome_decomposition", {}) or {}),
                context=pending_meta,
            )

            self._save_memory_state()
            self.pending_entry = None
            return True

        return True

    # ==================================================
    def _handle_entry_attempt(self, window, candle_state, last, live_mode: bool, external_order_active: bool):

        if self.position is not None or self.pending_entry is not None:
            return False

        if external_order_active:
            return True

        if int(getattr(self, "mcm_pause_left", 0) or 0) > 0:
            self.mcm_pause_left -= 1

        entry_result = evaluate_entry_decision(
            self,
            window,
            candle_state,
        )

        if entry_result is None:
            return True

        if self._handle_decision_tendency(entry_result):
            return True

        value_check = self.value_gate.evaluate(entry_result)

        if DEBUG:
            dbr_debug(f"VALUE_GATE: {value_check}", "value_check_debug.csv")

        if not value_check.get("trade_allowed", False):
            blocked_context = _build_entry_attempt_context(
                self,
                entry_result,
            )

            self.stats.on_attempt(
                status="blocked_value_gate",
                context=blocked_context,
            )
            mark_runtime_episode_event(
                self,
                "blocked_value_gate",
                {
                    "trade_plan": dict((blocked_context.get("trade_plan", {}) or {})),
                    "reason": str(value_check.get("reason") or "blocked_value_gate"),
                },
            )
            apply_outcome_stimulus(
                self,
                value_check.get("reason"),
                entry_result,
            )
            self._save_memory_state()
            return True

        side = str(entry_result.get("decision", "")).upper().strip()
        entry_price = float(entry_result.get("entry_price", 0.0) or 0.0)
        tp_price = float(entry_result.get("tp_price", 0.0) or 0.0)
        sl_price = float(entry_result.get("sl_price", 0.0) or 0.0)
        risk = abs(entry_price - sl_price)

        if side not in ("LONG", "SHORT"):
            return True

        if entry_price <= 0.0 or tp_price <= 0.0 or sl_price <= 0.0 or risk <= 0.0:
            return True

        order_side = "sell" if side == "SHORT" else "buy"

        order_id = None
        is_memory_trade = False
        rr_exec_min = float(getattr(Config, "RR_EXECUTION_MIN", 1.2) or 1.2)

        if live_mode and Config.AKTIV_ORDER and float(entry_result.get("rr_value", 0.0) or 0.0) < rr_exec_min:
            is_memory_trade = True

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
                return True

        attempt_meta = _build_entry_attempt_context(
            self,
            entry_result,
        )

        self.pending_entry = {
            "side": side,
            "entry": entry_price,
            "tp": tp_price,
            "sl": sl_price,
            "risk": float(risk),
            "order_id": order_id,
            "created_index": self.processed,
            "max_wait_bars": int(getattr(Config, "PENDING_ENTRY_MAX_WAIT_BARS", 20) or 20),
            "meta": attempt_meta,
        }
        self.stats.on_attempt(
            status="submitted",
            context=attempt_meta,
        )
        mark_runtime_episode_event(
            self,
            "submitted",
            {
                "trade_plan": dict((attempt_meta.get("trade_plan", {}) or {})),
                "reason": str(side or "-").lower(),
            },
        )

        self._save_memory_state()
        return True
                    
    # ==================================================
    # MCM RUNTIME
    # ==================================================
    def start_runtime_thread(self):

        if self._runtime_thread is not None and self._runtime_thread.is_alive():
            return self._runtime_thread

        with self._runtime_thread_lock:
            if self._runtime_thread is not None and self._runtime_thread.is_alive():
                return self._runtime_thread

            self._runtime_stop_event.clear()
            self._runtime_thread = threading.Thread(
                target=self._runtime_loop,
                daemon=True,
            )
            self._runtime_thread.start()

        return self._runtime_thread

    def stop_runtime_thread(self):

        self._runtime_stop_event.set()

        thread = self._runtime_thread
        if thread is not None and thread.is_alive():
            thread.join()

        return thread

    def wait_until_runtime_idle(self):

        self._market_packet_queue.join()

    def publish_market_window(self, window):

        packet = self._build_market_packet(window)
        if packet is None:
            return None

        self._market_packet_queue.put(dict(packet))
        return dict(packet)

    def _runtime_loop(self):

        while True:
            if self._runtime_stop_event.is_set() and self._market_packet_queue.empty():
                break

            try:
                packet = self._market_packet_queue.get(timeout=self._runtime_idle_sleep)
            except queue.Empty:
                if self._runtime_seeded:
                    self._step_runtime_idle()
                continue

            try:
                self._process_market_packet(packet)
            finally:
                self._market_packet_queue.task_done()

    def _build_market_packet(self, window):

        if not window:
            return None

        local_window = [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
        if not local_window:
            return None

        last = local_window[-1]
        prev_close = local_window[-2].get("close") if len(local_window) > 1 else None
        candle_state = _build_candle_state(last, prev_close=prev_close)
        tension_state = build_tension_state_from_window(local_window)
        structure_perception_state = STRUCTURE_ENGINE.build_structure_perception_state(local_window)

        return {
            "timestamp": last.get("timestamp"),
            "window": local_window,
            "candle_state": dict(candle_state or {}),
            "tension_state": dict(tension_state or {}),
            "structure_perception_state": dict(structure_perception_state or {}),
        }

    def _seed_runtime_window(self, window, candle_state=None):

        self._ensure_memory_state_loaded()

        if not window:
            return None

        local_window = [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
        if not local_window:
            return None

        if candle_state is None:
            last = local_window[-1]
            prev_close = local_window[-2].get("close") if len(local_window) > 1 else None
            candle_state = _build_candle_state(last, prev_close=prev_close)

        self.current_timestamp = local_window[-1].get("timestamp")
        result = step_mcm_runtime(
            local_window,
            dict(candle_state or {}),
            bot=self,
        )
        self._runtime_seeded = True
        return result

    def _step_runtime_idle(self):

        self._ensure_memory_state_loaded()

        return step_mcm_runtime_idle(
            bot=self,
            cycles=int(getattr(Config, "MCM_RUNTIME_IDLE_TICKS", 1) or 1),
        )

    # ==================================================
    # MEMORY STATE
    # ==================================================
    def _ensure_memory_state_loaded(self):

        if self._memory_state_mcm_loaded:
            return

        if not isinstance(self.mcm_brain, dict):
            return

        apply_memory_state(self, self._memory_state_payload)

        if getattr(self, "mcm_runtime", None) is not None:
            self.mcm_runtime.restore_from_bot()

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
    def _process_market_packet(self, packet):

        item = dict(packet or {})
        window = [dict(entry or {}) for entry in list(item.get("window", []) or []) if isinstance(entry, dict)]

        if not window:
            return None

        candle_state = dict(item.get("candle_state", {}) or {})
        if not candle_state:
            last = window[-1]
            prev_close = window[-2].get("close") if len(window) > 1 else None
            candle_state = _build_candle_state(last, prev_close=prev_close)

        if not self._runtime_seeded:
            return self._seed_runtime_window(window, candle_state=candle_state)

        result = self._process_runtime_packet(
            window,
            candle_state,
        )
        self.processed += 1
        return result

    def _process_runtime_packet(self, window, candle_state):

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
        external_order_active = False

        if live_mode and self.position is None and is_order_active():
            external_order_active = True
            if DEBUG:
                dbr_debug("RUNTIME: ORDER_ACTIVE_WATCH", "live_backtest_debug.csv")

        self.current_timestamp = window[-1].get("timestamp")
        self.stats.data["current_timestamp"] = self.current_timestamp

        last = window[-1]

        step_mcm_runtime(
            window,
            candle_state,
            bot=self,
        )

        if self._handle_active_position(window, last, live_mode):
            return True

        if self._handle_pending_entry(window, last, live_mode):
            return True

        if self._handle_entry_attempt(window, candle_state, last, live_mode, external_order_active):
            return True

        return True

    def _process_window(self, window):

        packet = self._build_market_packet(window)
        if packet is None:
            return None

        return self._process_market_packet(packet)

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

        return processed
    
# --------------------------------------------------
# ATTEMPT CONTEXT
# --------------------------------------------------
def _build_entry_attempt_context(bot, entry_result: dict) -> dict:

    result = dict(entry_result or {})

    return {
        "state": {
            "energy": float(result.get("energy", 0.0) or 0.0),
            "coherence": float(result.get("coherence", 0.0) or 0.0),
            "asymmetry": int(result.get("asymmetry", 0) or 0),
            "coh_zone": float(result.get("coh_zone", 0.0) or 0.0),
            "self_state": str(result.get("self_state", "stable") or "stable"),
            "attractor": str(result.get("attractor", "neutral") or "neutral"),
            "memory_center": float(result.get("memory_center", 0.0) or 0.0),
            "memory_strength": int(result.get("memory_strength", 0) or 0),
        },
        "focus": {
            "focus_point": float(getattr(bot, "focus_point", 0.0) or 0.0),
            "focus_confidence": float(getattr(bot, "focus_confidence", 0.0) or 0.0),
            "target_lock": float(getattr(bot, "target_lock", 0.0) or 0.0),
            "target_drift": float(getattr(bot, "target_drift", 0.0) or 0.0),
        },
        "experience": {
            "entry_expectation": float(result.get("entry_expectation", 0.0) or 0.0),
            "target_expectation": float(result.get("target_expectation", 0.0) or 0.0),
            "approach_pressure": float(result.get("approach_pressure", 0.0) or 0.0),
            "pressure_release": float(result.get("pressure_release", 0.0) or 0.0),
            "experience_regulation": float(result.get("experience_regulation", 0.0) or 0.0),
            "reflection_maturity": float(result.get("reflection_maturity", 0.0) or 0.0),
        },
        "vision": dict(result.get("vision", {}) or {}),
        "filtered_vision": dict(result.get("filtered_vision", {}) or {}),
        "world_state": dict(result.get("world_state", {}) or {}),
        "structure_perception_state": dict(result.get("structure_perception_state", {}) or {}),
        "outer_visual_perception_state": dict(result.get("outer_visual_perception_state", {}) or {}),
        "inner_field_perception_state": dict(result.get("inner_field_perception_state", {}) or {}),
        "processing_state": dict(result.get("processing_state", {}) or {}),
        "perception_state": dict(result.get("perception_state", {}) or {}),
        "felt_state": dict(result.get("felt_state", {}) or {}),
        "thought_state": dict(result.get("thought_state", {}) or {}),
        "meta_regulation_state": dict(result.get("meta_regulation_state", {}) or {}),
        "expectation_state": dict(result.get("expectation_state", {}) or {}),
        "state_signature": dict(result.get("state_signature", {}) or {}),
        "trade_plan": {
            "entry_price": float(result.get("entry_price", 0.0) or 0.0),
            "tp_price": float(result.get("tp_price", 0.0) or 0.0),
            "sl_price": float(result.get("sl_price", 0.0) or 0.0),
            "rr_value": float(result.get("rr_value", 0.0) or 0.0),
            "entry_validity_band": dict(result.get("entry_validity_band", {}) or {}),
            "target_conviction": float(result.get("target_conviction", 0.0) or 0.0),
            "risk_model_score": float(result.get("risk_model_score", 0.0) or 0.0),
            "reward_model_score": float(result.get("reward_model_score", 0.0) or 0.0),
        },
        "signal": {
            "signature_bias": float(result.get("signature_bias", 0.0) or 0.0),
            "signature_block": bool(result.get("signature_block", False)),
            "signature_quality": float(result.get("signature_quality", 0.0) or 0.0),
            "signature_distance": float(result.get("signature_distance", 0.0) or 0.0),
            "context_cluster_id": str(result.get("context_cluster_id", "-") or "-"),
            "context_cluster_bias": float(result.get("context_cluster_bias", 0.0) or 0.0),
            "context_cluster_quality": float(result.get("context_cluster_quality", 0.0) or 0.0),
            "context_cluster_distance": float(result.get("context_cluster_distance", 0.0) or 0.0),
            "context_cluster_block": bool(result.get("context_cluster_block", False)),
            "inhibition_level": float(result.get("inhibition_level", 0.0) or 0.0),
            "habituation_level": float(result.get("habituation_level", 0.0) or 0.0),
            "competition_bias": float(result.get("competition_bias", 0.0) or 0.0),
            "observation_mode": bool(result.get("observation_mode", False)),
            "long_score": float(result.get("long_score", 0.0) or 0.0),
            "short_score": float(result.get("short_score", 0.0) or 0.0),
        },
    }
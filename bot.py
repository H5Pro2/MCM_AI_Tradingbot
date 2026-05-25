# ==================================================
# bot.py
# Pipeline:
# OHLC
# -> Exit / Pending Handling
# -> Dummy Entry Slot
# -> TradeValueGate
# -> Order / Pending Entry
# ==================================================
import json
import os
import queue
import threading
import time

from config import Config
from csv_feed import CSVFeed
from trade_stats import TradeStats
from bot_engine.exit_engine import ExitEngine
from bot_engine.mcm_core_engine import build_tension_state_from_window, build_visual_market_state
from bot_engine.strukture_engine import StructureEngine
from bot_gates.trade_value_gate import TradeValueGate

from place_orders import place_order, cancel_order_by_id, consume_cancelled_cause, get_active_order_snapshot, is_order_active
from debug_reader import dbr_append_text, dbr_debug, dbr_path
from ph_ohlcv import _build_candle_state
from bot_gate_funktions import evaluate_entry_decision
from MCM_Brain_Modell import _flush_form_symbol_memory_if_due, _flush_thought_memory_if_due, apply_outcome_stimulus, build_runtime_pipeline_snapshot, build_visualization_snapshot_bundle, capture_runtime_regulation_transition, commit_runtime_regulation_snapshot, create_mcm_brain, create_mcm_runtime, mark_runtime_episode_event, prepare_visualization_snapshot_state, step_mcm_runtime, step_mcm_runtime_idle, write_visualization_snapshot_bundle
from memory_state import capture_memory_state, ensure_memory_state_loaded, finalize_memory_state_save, flush_memory_state_if_due, initialize_memory_state_bootstrap, mark_memory_state_dirty, write_memory_state_payload


DEBUG = True
STRUCTURE_ENGINE = StructureEngine()
# --------------------------------------------------


class Bot:
    # ==================================================
    # INITIALISIERUNG / BOT-LIFECYCLE
    # ==================================================
    def __init__(self, filepath: str):

        self._initialize_bot_state(filepath)
        initialize_memory_state_bootstrap(self)
        self.mcm_runtime = create_mcm_runtime(self)
        self._initialize_runtime_thread_state()
        self._recover_live_state_on_boot()
    # --------------------------------------------------    
    def _recover_live_state_on_boot(self):

        live_mode = str(getattr(Config, "MODE", "LIVE")).upper() == "LIVE"
        snapshot = None

        if live_mode and bool(getattr(Config, "AKTIV_ORDER", False)):
            snapshot = get_active_order_snapshot()

        if snapshot:
            recovered = self._apply_restart_recovery_snapshot(
                snapshot,
            )

            if recovered:
                self._save_memory_state(force=True)

            return bool(recovered)

        return False
    # --------------------------------------------------    
    def start_runtime_thread(self):

        return self._start_runtime_thread()
    # --------------------------------------------------
    def stop_runtime_thread(self):

        return self._stop_runtime_thread()
    # --------------------------------------------------
    def wait_until_runtime_idle(self):

        return self._wait_until_runtime_idle()
    # --------------------------------------------------
    def _initialize_bot_state(self, filepath: str):

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
        self.field_density = 0.0
        self.field_stability = 0.0
        self.regulatory_load = 0.0
        self.action_capacity = 0.0
        self.recovery_need = 0.0
        self.survival_pressure = 0.0

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

        self.inner_context_clusters = {}
        self.inner_context_cluster_seq = 0
        self.last_inner_context_cluster_id = None
        self.last_inner_context_cluster_key = None

        self.inhibition_level = 0.0
        self.habituation_level = 0.0
        self.competition_bias = 0.0
        self.observation_mode = False
        self.last_signal_relevance = 0.0

        self.tension_state = {}
        self.visual_market_state = {}
        self.structure_perception_state = {}
        self.temporal_perception_state = {}
        self.outer_market_state = {}
        self.perception_state = {}
        self.outer_visual_perception_state = {}
        self.inner_field_perception_state = {}
        self.processing_state = {}
        self.expectation_state = {}
        self.felt_state = {}
        self.thought_state = {}
        self.meta_regulation_state = {}
        self.action_intent_state = {}
        self.execution_state = {}
        self.last_outcome_decomposition = {}
        self.mcm_thought_memory = {}
        self.mcm_thought_family_memory = {}
        self.mcm_thought_memory_summary = {}
        self._thought_memory_loaded = False
        self._thought_memory_dirty = False
        self._thought_memory_updates = 0
        self._thought_memory_last_save_ts = 0.0

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
        return True    
    # ==================================================
    # RUNTIME THREAD / IDLE
    # ==================================================
    def _build_runtime_execution_payload(self, action_context, candle_state=None):

        payload_state = self._build_runtime_action_payload_state(
            action_context,
            candle_state=candle_state,
            allow_empty=True,
        )

        return {
            "window": list(payload_state.get("window", []) or []),
            "last": dict(payload_state.get("last", {}) or {}),
            "live_mode": bool(payload_state.get("live_mode", False)),
            "external_order_active": bool(payload_state.get("external_order_active", False)),
            "candle_state": dict(payload_state.get("candle_state", {}) or {}),
        }
    # --------------------------------------------------
    def _sync_last_outcome_decomposition_from_stats(self):
        try:
            stats_data = getattr(self.stats, "data", {}) or {}
            payload = dict(stats_data.get("last_outcome_decomposition", {}) or {})
            if payload:
                self.last_outcome_decomposition = payload
        except Exception:
            pass
    # --------------------------------------------------
    def _resolve_runtime_action_window_state(self, action_context):

        context = dict(action_context or {})
        window = [dict(item or {}) for item in list(context.get("window", []) or []) if isinstance(item, dict)]

        if not window:
            return None

        timestamp = context.get("timestamp", window[-1].get("timestamp"))
        last = dict(context.get("last", window[-1]) or window[-1])

        return {
            "context": dict(context or {}),
            "window": list(window or []),
            "timestamp": timestamp,
            "last": dict(last or {}),
        }
    # --------------------------------------------------
    def _start_runtime_thread(self):

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
    # --------------------------------------------------
    def _run_runtime_packet_action_cycle(self, resolved_packet, seed_runtime: bool = False):

        item = dict(resolved_packet or {})
        local_window = [dict(entry or {}) for entry in list(item.get("window", []) or []) if isinstance(entry, dict)]
        if not local_window:
            return None

        resolved_candle_state = dict(item.get("candle_state", {}) or {})

        if seed_runtime:
            self._ensure_memory_state_loaded()

        self._apply_market_perception_state(item)

        runtime_result = self._advance_runtime_from_resolved_packet(
            item,
        )

        if seed_runtime:
            self._runtime_seeded = True

        action_result = self._run_runtime_action_cycle(
            local_window,
            dict(resolved_candle_state or {}),
        )
        if action_result is None:
            return runtime_result

        return action_result   
    # --------------------------------------------------
    def _build_current_runtime_packet(self, window, candle_state, visual_market_state=None, structure_perception_state=None):

        local_window = [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
        if not local_window:
            return None

        return self._build_runtime_market_packet(
            {
                "timestamp": local_window[-1].get("timestamp", None),
                "window": [dict(item or {}) for item in list(local_window or []) if isinstance(item, dict)],
                "candle_state": dict(candle_state or {}),
                "tension_state": dict(getattr(self, "tension_state", {}) or {}),
                "visual_market_state": dict(visual_market_state or {}),
                "structure_perception_state": dict(structure_perception_state or {}),
                "temporal_perception_state": dict(getattr(self, "temporal_perception_state", {}) or {}),
                "outer_market_state": dict(getattr(self, "outer_market_state", {}) or {}),
            }
        )
    # --------------------------------------------------
    def _build_runtime_market_packet(
        self,
        packet,
        candle_state=None,
        visual_market_state=None,
        structure_perception_state=None,
        tension_state=None,
        temporal_perception_state=None,
    ):

        item = dict(packet or {})
        if not item:
            return None

        resolved_window = [dict(entry or {}) for entry in list(item.get("window", []) or []) if isinstance(entry, dict)]
        if not resolved_window:
            return None

        resolved_timestamp = item.get("timestamp", None)
        resolved_candle_state = dict(item.get("candle_state", {}) or {})
        resolved_tension_state = dict(item.get("tension_state", {}) or {})
        resolved_visual_market_state = dict(item.get("visual_market_state", {}) or {})
        resolved_structure_perception_state = dict(item.get("structure_perception_state", {}) or {})
        resolved_temporal_perception_state = dict(item.get("temporal_perception_state", {}) or {})

        if candle_state is not None:
            resolved_candle_state = dict(candle_state or {})

        if tension_state is not None:
            resolved_tension_state = dict(tension_state or {})

        if visual_market_state is not None:
            resolved_visual_market_state = dict(visual_market_state or {})

        if structure_perception_state is not None:
            resolved_structure_perception_state = dict(structure_perception_state or {})

        if temporal_perception_state is not None:
            resolved_temporal_perception_state = dict(temporal_perception_state or {})

        resolved_outer_market_state = self._build_outer_market_state_packet(
            resolved_timestamp,
            candle_state=resolved_candle_state,
            tension_state=resolved_tension_state,
            visual_market_state=resolved_visual_market_state,
            structure_perception_state=resolved_structure_perception_state,
            temporal_perception_state=resolved_temporal_perception_state,
            base_state=dict(item.get("outer_market_state", {}) or {}),
        )

        return {
            "timestamp": resolved_timestamp,
            "window": [dict(entry or {}) for entry in list(resolved_window or []) if isinstance(entry, dict)],
            "candle_state": dict(resolved_candle_state or {}),
            "tension_state": dict(resolved_tension_state or {}),
            "visual_market_state": dict(resolved_visual_market_state or {}),
            "structure_perception_state": dict(resolved_structure_perception_state or {}),
            "temporal_perception_state": dict(resolved_temporal_perception_state or {}),
            "outer_market_state": dict(resolved_outer_market_state or {}),
        }    
    # --------------------------------------------------
    def _stop_runtime_thread(self):

        self._runtime_stop_event.set()

        thread = self._runtime_thread
        if thread is not None and thread.is_alive():
            thread.join()

        self._save_memory_state(force=True)
        return thread
    # --------------------------------------------------
    def _wait_until_runtime_idle(self):

        self._market_packet_queue.join()
        return True
    # --------------------------------------------------
    def _initialize_runtime_thread_state(self):

        self._runtime_thread = None
        self._runtime_thread_lock = threading.Lock()
        self._runtime_stop_event = threading.Event()
        self._market_packet_queue = queue.Queue()
        self._runtime_seeded = bool(self.mcm_runtime is not None and self.mcm_runtime.has_impulse())
        self._last_regulation_state_snapshot = self._build_regulation_state_snapshot()
        self._memory_state_dirty = False
        self._memory_state_last_save_ts = 0.0
        self._snapshot_bundle = {}
        self._snapshot_dirty = False
        self._snapshot_write_seq = 0
        self._snapshot_last_write_ts = 0.0
        self._snapshot_last_state_key = None
        self._last_live_market_packet_key = None
        self._live_duplicate_market_packet_skips = 0
        self._idle_thinking_protocol_seq = 0
        self._idle_thinking_last_state_key = None
        self._idle_thinking_last_depth = 0.0
        return True
    # -------------------------------------------------
    def _runtime_loop(self):

        while True:
            if self._runtime_stop_event.is_set() and self._market_packet_queue.empty():
                break

            idle_sleep = self._runtime_idle_sleep_seconds()

            try:
                packet = self._market_packet_queue.get(timeout=idle_sleep)
            except queue.Empty:
                self._run_runtime_idle_followup()
                continue

            try:
                self._process_market_packet_and_followup(packet)
            finally:
                self._market_packet_queue.task_done()
    # --------------------------------------------------
    def _run_runtime_execution_paths(self, prepared_context, candle_state):

        if self._run_existing_trade_execution_paths(prepared_context):
            return True

        if self._run_entry_execution_path(prepared_context, candle_state):
            return True

        return True        
    # --------------------------------------------------    
    def _runtime_dynamic_load(self):

        dynamic_load = max(
            float(getattr(self, "focus_confidence", 0.0) or 0.0),
            float(getattr(self, "target_lock", 0.0) or 0.0),
            float(getattr(self, "last_signal_relevance", 0.0) or 0.0),
            abs(float(getattr(self, "competition_bias", 0.0) or 0.0)),
        )

        if self.position is not None:
            dynamic_load = max(dynamic_load, 1.0)
        elif self.pending_entry is not None:
            dynamic_load = max(dynamic_load, 0.82)
        elif bool(getattr(self, "observation_mode", False)):
            dynamic_load = max(dynamic_load, 0.68)

        return float(max(0.0, min(1.0, float(dynamic_load))))
    # --------------------------------------------------
    def _runtime_idle_sleep_seconds(self):

        min_sleep = max(
            0.01,
            float(
                getattr(
                    Config,
                    "MCM_INNER_IDLE_SLEEP_MIN_SECONDS",
                    getattr(Config, "MCM_RUNTIME_IDLE_SLEEP_MIN_SECONDS", 0.05),
                ) or 0.05
            ),
        )
        max_sleep = max(
            min_sleep,
            float(
                getattr(
                    Config,
                    "MCM_INNER_IDLE_SLEEP_MAX_SECONDS",
                    getattr(Config, "MCM_RUNTIME_IDLE_SLEEP_MAX_SECONDS", 0.35),
                ) or 0.35
            ),
        )

        queue_depth = int(self._market_packet_queue.qsize() or 0)
        if queue_depth > 0:
            return float(min_sleep)

        dynamic_load = self._runtime_dynamic_load()
        sleep_span = max_sleep - min_sleep
        return float(max_sleep - (sleep_span * dynamic_load))
    # --------------------------------------------------
    def _runtime_idle_cycles(self):

        base_cycles = max(
            1,
            int(
                getattr(
                    Config,
                    "MCM_INNER_IDLE_BASE_TICKS",
                    getattr(Config, "MCM_RUNTIME_IDLE_TICKS", 1),
                ) or 1
            ),
        )
        max_cycles = max(
            base_cycles,
            int(
                getattr(
                    Config,
                    "MCM_INNER_IDLE_MAX_TICKS",
                    getattr(Config, "MCM_RUNTIME_IDLE_TICKS_MAX", base_cycles),
                ) or base_cycles
            ),
        )

        dynamic_load = self._runtime_dynamic_load()

        cycle_boost = 0

        if self.position is not None:
            cycle_boost += 2
        elif self.pending_entry is not None:
            cycle_boost += 1

        if bool(getattr(self, "observation_mode", False)):
            cycle_boost += 1

        cycle_boost += int(round(dynamic_load * max(0, max_cycles - base_cycles)))
        return int(min(max_cycles, base_cycles + cycle_boost))
    # --------------------------------------------------
    def _step_runtime_idle(self, cycles=None):

        self._ensure_memory_state_loaded()

        idle_cycles = cycles
        if idle_cycles is None:
            idle_cycles = self._runtime_idle_cycles()

        return step_mcm_runtime_idle(
            bot=self,
            cycles=max(1, int(idle_cycles or 1)),
        )
    # --------------------------------------------------
    def _flush_runtime_followup(self):

        self._flush_visualization_snapshots()
        self._flush_memory_state_if_due()
        return True
    # --------------------------------------------------
    def _run_runtime_idle_followup(self):

        idle_result = None
        if self._runtime_seeded:
            idle_result = self._step_runtime_idle(
                cycles=self._runtime_idle_cycles(),
            )
            self._write_idle_thinking_protocol(idle_result)

        return self._flush_runtime_followup()
    # --------------------------------------------------
    @staticmethod
    def _clip01(value):

        try:
            return float(max(0.0, min(1.0, float(value or 0.0))))
        except Exception:
            return 0.0
    # --------------------------------------------------
    @staticmethod
    def _idle_phase_from_state(reflection_need, replay_need, hypothesis_need, pause_maturity, depth_efficiency, decision_tendency, pre_action_phase="hold", plan_pressure=0.0, act_watch_readiness=0.0):

        phase = str(pre_action_phase or "").strip().lower()
        pressure = Bot._clip01(plan_pressure)
        readiness = Bot._clip01(act_watch_readiness)
        if phase == "act_watch" or (str(decision_tendency or "").lower() == "act" and pressure >= 0.44 and readiness >= 0.38):
            return "act_watch"
        if str(decision_tendency or "").lower() == "act" and pressure >= 0.38:
            return "plan_pressure"
        if pause_maturity >= 0.62 and pause_maturity >= max(reflection_need, replay_need, hypothesis_need):
            return "pause"
        if replay_need >= 0.58 and replay_need >= max(reflection_need, hypothesis_need):
            return "replay"
        if hypothesis_need >= 0.56 and hypothesis_need >= reflection_need:
            return "hypothesize"
        if reflection_need >= 0.54:
            return "reflect"
        if depth_efficiency >= 0.58 and str(decision_tendency or "").lower() in ("hold", "observe"):
            return "stabilize"
        return "hold"
    # --------------------------------------------------
    def _write_idle_thinking_protocol(self, runtime_result):

        if not bool(getattr(Config, "MCM_IDLE_THINKING_PROTOCOL_DEBUG", False)):
            return False

        result = dict(runtime_result or {})
        if not result:
            return False

        def _num(source, key, default=0.0):
            try:
                return float((source or {}).get(key, default) or default)
            except Exception:
                return float(default)

        runtime_snapshot = dict(getattr(self, "mcm_runtime_snapshot", {}) or {})
        timestamp = result.get("timestamp", runtime_snapshot.get("timestamp", getattr(self, "current_timestamp", None)))
        runtime_tick_seq = int(result.get("runtime_tick_seq", runtime_snapshot.get("runtime_tick_seq", 0)) or 0)
        market_ticks = int(result.get("market_ticks", runtime_snapshot.get("market_ticks", getattr(self, "mcm_runtime_market_ticks", 0))) or 0)
        decision_tendency = str(result.get("decision_tendency", runtime_snapshot.get("decision_tendency", "hold")) or "hold").lower()
        proposed_decision = str(result.get("proposed_decision", runtime_snapshot.get("proposed_decision", "WAIT")) or "WAIT").upper()

        thought_state = dict(result.get("thought_state", getattr(self, "thought_state", {}) or {}) or {})
        meta_state = dict(result.get("meta_regulation_state", {}) or {})
        perception_state = dict(result.get("perception_state", {}) or {})
        form_symbol_state = dict(result.get("form_symbol_state", getattr(self, "form_symbol_state", {}) or {}) or {})
        memory_state = dict(result.get("memory_complexity_state", {}) or {})
        if not memory_state:
            memory_state = dict((meta_state.get("memory_complexity_state", {}) or {}) or {})
        if not memory_state:
            memory_state = dict(getattr(self, "last_memory_complexity_state", {}) or {})

        regulatory_load = self._clip01(result.get("regulatory_load", getattr(self, "regulatory_load", 0.0)))
        action_capacity = self._clip01(result.get("action_capacity", getattr(self, "action_capacity", 0.0)))
        recovery_need = self._clip01(result.get("recovery_need", getattr(self, "recovery_need", 0.0)))
        survival_pressure = self._clip01(result.get("survival_pressure", getattr(self, "survival_pressure", 0.0)))
        rumination_depth = self._clip01(_num(thought_state, "rumination_depth", 0.0))
        decision_conflict = self._clip01(_num(thought_state, "decision_conflict", 0.0))
        state_maturity = self._clip01(_num(thought_state, "state_maturity", 0.0))
        decision_readiness = self._clip01(_num(thought_state, "decision_readiness", 0.0))
        observe_priority = self._clip01(_num(perception_state, "observe_priority", 0.0))
        uncertainty_score = self._clip01(_num(perception_state, "uncertainty_score", 0.0))
        signal_quality = self._clip01(_num(perception_state, "signal_quality", 0.0))

        memory_compare_load = self._clip01(_num(memory_state, "memory_compare_load", 0.0))
        memory_support = self._clip01(_num(memory_state, "memory_support", 0.0))
        memory_inhibition = self._clip01(_num(memory_state, "memory_inhibition", 0.0))
        memory_conflict = self._clip01(_num(memory_state, "memory_conflict", 0.0))
        thinking_complexity = self._clip01(_num(memory_state, "thinking_complexity", 0.0))
        cognitive_load = self._clip01(_num(memory_state, "cognitive_load", 0.0))
        decision_energy_cost = self._clip01(_num(memory_state, "decision_energy_cost", 0.0))

        form_symbol_maturity = self._clip01(_num(form_symbol_state, "form_symbol_maturity", 0.0))
        form_symbol_zoom_need = self._clip01(_num(form_symbol_state, "form_symbol_zoom_need", 0.0))
        form_symbol_detail_pressure = self._clip01(_num(form_symbol_state, "form_symbol_detail_pressure", 0.0))
        form_symbol_containment = self._clip01(_num(form_symbol_state, "form_symbol_containment", 0.0))
        form_symbol_field_decoupling = self._clip01(_num(form_symbol_state, "form_symbol_field_decoupling", 0.0))
        pre_action_phase = str(meta_state.get("pre_action_phase", "hold") or "hold").strip().lower()
        plan_pressure = self._clip01(_num(meta_state, "plan_pressure", 0.0))
        act_watch_readiness = self._clip01(_num(meta_state, "act_watch_readiness", 0.0))
        structure_carrying_need = self._clip01(_num(meta_state, "structure_carrying_need", 0.0))

        load_gap = self._clip01(regulatory_load - action_capacity)
        reflection_need = self._clip01((decision_conflict * 0.30) + (cognitive_load * 0.24) + (load_gap * 0.22) + (rumination_depth * 0.16) + (uncertainty_score * 0.08))
        replay_need = self._clip01((memory_compare_load * 0.28) + (memory_conflict * 0.24) + (memory_support * 0.18) + (thinking_complexity * 0.16) + (max(0.0, 1.0 - form_symbol_maturity) * 0.08))
        hypothesis_need = self._clip01((form_symbol_zoom_need * 0.30) + (form_symbol_detail_pressure * 0.22) + (uncertainty_score * 0.18) + (observe_priority * 0.14) + (max(0.0, 1.0 - signal_quality) * 0.10))
        pause_maturity = self._clip01((load_gap * 0.34) + (observe_priority * 0.24) + (recovery_need * 0.18) + (survival_pressure * 0.14) + (decision_conflict * 0.10) - (decision_readiness * 0.10))
        action_load_capacity = self._clip01(action_capacity - (regulatory_load * 0.48) - (decision_energy_cost * 0.22) + (state_maturity * 0.18))
        regulatory_self_control = self._clip01((pause_maturity * 0.32) + (reflection_need * 0.24) + (form_symbol_containment * 0.18) + (form_symbol_field_decoupling * 0.16) + (max(0.0, memory_inhibition - memory_support) * 0.10))
        parameter_dependency = self._clip01((max(0.0, 1.0 - form_symbol_maturity) * 0.26) + (decision_energy_cost * 0.20) + (cognitive_load * 0.18) + (uncertainty_score * 0.16) + (memory_inhibition * 0.12) - (form_symbol_containment * 0.10))
        self_regulation_maturity = self._clip01((state_maturity * 0.24) + (action_load_capacity * 0.22) + (form_symbol_containment * 0.18) + (form_symbol_field_decoupling * 0.14) + (memory_support * 0.12) - (load_gap * 0.14))
        depth_efficiency = self._clip01((state_maturity * 0.24) + (memory_support * 0.18) + (form_symbol_containment * 0.16) + (form_symbol_field_decoupling * 0.16) + (signal_quality * 0.14) - (cognitive_load * 0.18) - (memory_conflict * 0.10))
        cognitive_overcontrol = self._clip01((cognitive_load * 0.30) + (rumination_depth * 0.24) + (decision_energy_cost * 0.20) + (memory_compare_load * 0.14) - (depth_efficiency * 0.18))
        thinking_depth = self._clip01(max(rumination_depth, thinking_complexity, reflection_need, replay_need, hypothesis_need))
        action_depth = self._clip01((decision_energy_cost * 0.26) + (regulatory_load * 0.24) + (decision_conflict * 0.18) + ((1.0 if proposed_decision in ("LONG", "SHORT") else 0.0) * 0.16) + (max(0.0, 1.0 - action_capacity) * 0.16))
        adaptive_depth_shift = self._clip01(abs(thinking_depth - float(getattr(self, "_idle_thinking_last_depth", 0.0) or 0.0)))
        self._idle_thinking_last_depth = float(thinking_depth)

        idle_phase = self._idle_phase_from_state(
            reflection_need,
            replay_need,
            hypothesis_need,
            pause_maturity,
            depth_efficiency,
            decision_tendency,
            pre_action_phase=pre_action_phase,
            plan_pressure=plan_pressure,
            act_watch_readiness=act_watch_readiness,
        )
        state_key = (
            timestamp,
            idle_phase,
            round(thinking_depth, 2),
            round(regulatory_self_control, 2),
            round(parameter_dependency, 2),
            round(depth_efficiency, 2),
            round(plan_pressure, 2),
            round(act_watch_readiness, 2),
            pre_action_phase,
            decision_tendency,
            proposed_decision,
        )
        state_changed = state_key != self._idle_thinking_last_state_key
        self._idle_thinking_protocol_seq = int(getattr(self, "_idle_thinking_protocol_seq", 0) or 0) + 1
        every_n = max(1, int(getattr(Config, "MCM_IDLE_THINKING_PROTOCOL_EVERY_N", 5) or 5))
        if not state_changed and (self._idle_thinking_protocol_seq % every_n) != 0:
            return False
        self._idle_thinking_last_state_key = state_key

        path = dbr_path("mcm_idle_thinking_protocol.csv")
        try:
            header_key = "_idle_thinking_protocol_header_written"
            write_header = (not os.path.exists(path)) and not bool(getattr(self, header_key, False))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            payload = ""
            if write_header:
                payload += (
                    "timestamp;market_ticks;runtime_tick_sequence;idle_phase;state_changed;"
                    "decision_tendency;proposed_decision;pre_action_phase;thinking_depth;action_depth;"
                    "reflection_need;replay_need;hypothesis_need;pause_maturity;"
                    "regulatory_self_control;parameter_dependency;self_regulation_maturity;"
                    "cognitive_overcontrol;adaptive_depth_shift;action_load_capacity;"
                    "depth_efficiency;plan_pressure;act_watch_readiness;structure_carrying_need;"
                    "thinking_complexity;memory_compare_load;memory_support;"
                    "memory_inhibition;memory_conflict;cognitive_load;decision_energy_cost;"
                    "regulatory_load;action_capacity;recovery_need;survival_pressure;"
                    "rumination_depth;decision_conflict;state_maturity;decision_readiness;"
                    "observe_priority;uncertainty_score;signal_quality;form_symbol_id;"
                    "form_symbol_maturity;form_symbol_zoom_need;form_symbol_containment;"
                    "form_symbol_field_decoupling\n"
                )
                setattr(self, header_key, True)

            form_symbol_id = str(form_symbol_state.get("form_symbol_id", "-") or "-").replace(";", "|")
            values = [
                timestamp,
                market_ticks,
                runtime_tick_seq,
                idle_phase,
                int(bool(state_changed)),
                decision_tendency,
                proposed_decision,
                pre_action_phase,
                thinking_depth,
                action_depth,
                reflection_need,
                replay_need,
                hypothesis_need,
                pause_maturity,
                regulatory_self_control,
                parameter_dependency,
                self_regulation_maturity,
                cognitive_overcontrol,
                adaptive_depth_shift,
                action_load_capacity,
                depth_efficiency,
                plan_pressure,
                act_watch_readiness,
                structure_carrying_need,
                thinking_complexity,
                memory_compare_load,
                memory_support,
                memory_inhibition,
                memory_conflict,
                cognitive_load,
                decision_energy_cost,
                regulatory_load,
                action_capacity,
                recovery_need,
                survival_pressure,
                rumination_depth,
                decision_conflict,
                state_maturity,
                decision_readiness,
                observe_priority,
                uncertainty_score,
                signal_quality,
                form_symbol_id,
                form_symbol_maturity,
                form_symbol_zoom_need,
                form_symbol_containment,
                form_symbol_field_decoupling,
            ]
            line = ";".join(
                f"{item:.4f}" if isinstance(item, float) else str(item)
                for item in values
            )
            payload += line + "\n"
            dbr_append_text(path, payload, operation="idle_thinking_protocol_append")
            return True
        except Exception as exc:
            if DEBUG:
                dbr_debug(
                    f"IDLE_THINKING_PROTOCOL_ERROR | {type(exc).__name__}:{str(exc).replace(';', '|')}",
                    "mcm_idle_thinking_protocol_error.csv",
                )
            return False
    # --------------------------------------------------
    def _run_runtime_market_followup(self):

        market_cycles = self._runtime_market_followup_cycles()
        if self._runtime_seeded and market_cycles > 0:
            self._step_runtime_idle(
                cycles=market_cycles,
            )

        return self._flush_runtime_followup()
    # -------------------------------------------------- 
    def _build_runtime_action_context_flags(self):

        live_mode = str(getattr(Config, "MODE", "LIVE")).upper() == "LIVE"
        external_order_active = False

        if live_mode and self.position is None and is_order_active():
            external_order_active = True
            if DEBUG:
                dbr_debug("RUNTIME: ORDER_ACTIVE_WATCH", "live_backtest_debug.csv")

        return {
            "live_mode": bool(live_mode),
            "external_order_active": bool(external_order_active),
            "outer_market_state": dict(getattr(self, "outer_market_state", {}) or {}),
        }
    # --------------------------------------------------
    def _resolve_runtime_action_context_state(self, action_context):

        resolved_state = self._resolve_runtime_action_window_state(
            action_context,
        )
        if resolved_state is None:
            return None

        context = dict(resolved_state.get("context", {}) or {})
        return {
            "context": dict(context or {}),
            "window": list(resolved_state.get("window", []) or []),
            "last": dict(resolved_state.get("last", {}) or {}),
            "timestamp": resolved_state.get("timestamp", None),
            "live_mode": bool(context.get("live_mode", False)),
            "external_order_active": bool(context.get("external_order_active", False)),
            "outer_market_state": dict(context.get("outer_market_state", {}) or {}),
        }   
    # ==================================================
    # WINDOW EINGANG / FEED
    # ==================================================  
    def _build_market_packet_from_window(self, window):

        packet = self._build_market_perception_packet(window)
        if packet is None:
            return None

        return dict(packet or {}) 
    # --------------------------------------------------    
    def _consume_feed_windows(self, windows):

        processed = 0

        for window in windows:
            self._process_market_window_and_followup(window)
            processed += 1

        return processed
    # --------------------------------------------------
    def _iter_row_windows(self, window_size: int = 2, delay_seconds: float = 0.0):

        buffer = []

        for row in self.feed.rows(delay_seconds=delay_seconds):
            buffer.append(row)

            if len(buffer) < window_size:
                continue

            if len(buffer) > window_size:
                buffer.pop(0)

            yield list(buffer)
    # --------------------------------------------------
    def _process_market_packet_and_followup(self, packet):

        result = self._process_market_packet(packet)
        self._run_runtime_market_followup()
        return result
    # --------------------------------------------------  
    def publish_market_window(self, window):

        packet = self._build_market_packet_from_window(window)
        if packet is None:
            return None

        return self._publish_market_packet(packet)
    # --------------------------------------------------
    def _process_market_window_and_followup(self, window):

        packet = self._build_market_packet_from_window(window)
        if packet is None:
            return None

        return self._process_market_packet_and_followup(packet)
    # --------------------------------------------------   
    def _run_rows_buffer_loop(self, window_size: int = 2, delay_seconds: float = 0.0):

        self.processed = 0

        return self._consume_feed_windows(
            self._iter_row_windows(
                window_size=window_size,
                delay_seconds=delay_seconds,
            )
        )
    # --------------------------------------------------
    def _run_window_feed_loop(self, size: int, delay_seconds: float = 0.0):

        if not hasattr(self, "processed"):
            self.processed = 0

        return self._consume_feed_windows(
            self.feed.window(size, delay_seconds=delay_seconds)
        )
    # --------------------------------------------------
    def run_rows(self, window_size: int = 2, delay_seconds: float = 0.0):

        return self._run_rows_buffer_loop(
            window_size=window_size,
            delay_seconds=delay_seconds,
        )
    # -------------------------------------------------- 
    def run_window(self, size: int, delay_seconds: float = 0.0):

        return self._run_window_feed_loop(
            size=size,
            delay_seconds=delay_seconds,
        )
    # --------------------------------------------------     
    def _run_existing_trade_execution_paths(self, prepared_context):

        if self._run_position_execution_path(prepared_context):
            return True

        if self._run_pending_execution_path(prepared_context):
            return True

        return False  
    # --------------------------------------------------       
    def _run_entry_execution_path(self, prepared_context, candle_state):

        return self._run_decision_execution_path(
            prepared_context,
            candle_state,
        )    
    # ==================================================
    # MARKET WINDOW NORMALISIERUNG / AUSSENWAHRNEHMUNG
    # ==================================================
    def _build_outer_market_state_packet(
        self,
        timestamp,
        candle_state=None,
        tension_state=None,
        visual_market_state=None,
        structure_perception_state=None,
        temporal_perception_state=None,
        base_state=None,
    ):

        return {
            **dict(base_state or {}),
            "timestamp": timestamp,
            "candle_state": dict(candle_state or {}),
            "tension_state": dict(tension_state or {}),
            "visual_market_state": dict(visual_market_state or {}),
            "structure_perception_state": dict(structure_perception_state or {}),
            "temporal_perception_state": dict(temporal_perception_state or {}),
        }
    # --------------------------------------------------
    def _build_market_component_bundle(self, window, base_packet=None):

        local_window = self._normalize_market_window(window)
        if not local_window:
            return None

        item = dict(base_packet or {})
        timestamp = local_window[-1].get("timestamp")

        candle_state = dict(item.get("candle_state", {}) or {})
        tension_state = dict(item.get("tension_state", {}) or {})
        visual_market_state = dict(item.get("visual_market_state", {}) or {})
        structure_perception_state = dict(item.get("structure_perception_state", {}) or {})
        temporal_perception_state = dict(item.get("temporal_perception_state", {}) or {})

        if not candle_state:
            candle_state = self._build_candle_state_packet(local_window)

        if not tension_state:
            tension_state = self._build_tension_state_packet(local_window)

        if not visual_market_state:
            visual_market_state = self._build_visual_market_state_packet(local_window)

        if not structure_perception_state:
            structure_perception_state = self._build_structure_perception_packet(local_window)

        if not temporal_perception_state:
            temporal_perception_state = dict(self._build_temporal_perception_state(local_window) or {})

        outer_market_state = self._build_outer_market_state_packet(
            timestamp,
            candle_state=candle_state,
            tension_state=tension_state,
            visual_market_state=visual_market_state,
            structure_perception_state=structure_perception_state,
            temporal_perception_state=temporal_perception_state,
            base_state=dict(item.get("outer_market_state", {}) or {}),
        )

        return {
            "timestamp": timestamp,
            "window": list(local_window or []),
            "candle_state": dict(candle_state or {}),
            "tension_state": dict(tension_state or {}),
            "visual_market_state": dict(visual_market_state or {}),
            "structure_perception_state": dict(structure_perception_state or {}),
            "temporal_perception_state": dict(temporal_perception_state or {}),
            "outer_market_state": dict(outer_market_state or {}),
        }      
    # --------------------------------------------------        
    def _publish_market_packet(self, packet):

        payload = dict(packet or {})
        if not payload:
            return None

        if self._is_duplicate_live_market_packet(payload):
            return None

        self._market_packet_queue.put(dict(payload))
        return dict(payload)
    # --------------------------------------------------
    def _is_duplicate_live_market_packet(self, packet):

        if str(getattr(Config, "MODE", "LIVE")).upper() != "LIVE":
            return False

        if not bool(getattr(Config, "LIVE_MARKET_PACKET_DEDUPE_ENABLED", True)):
            return False

        key = self._build_live_market_packet_key(packet)
        if key is None:
            return False

        if key != self._last_live_market_packet_key:
            self._last_live_market_packet_key = key
            self._live_duplicate_market_packet_skips = 0
            return False

        self._live_duplicate_market_packet_skips = int(getattr(self, "_live_duplicate_market_packet_skips", 0) or 0) + 1
        every_n = max(1, int(getattr(Config, "LIVE_MARKET_PACKET_DEDUPE_LOG_EVERY_N", 25) or 25))
        if self._live_duplicate_market_packet_skips == 1 or (self._live_duplicate_market_packet_skips % every_n) == 0:
            dbr_debug(
                f"LIVE_MARKET_PACKET_DEDUPE | skipped={self._live_duplicate_market_packet_skips} timestamp={key[0]} tail={key[1]}",
                "mcm_live_market_dedupe.csv",
            )
        return True
    # --------------------------------------------------
    def _build_live_market_packet_key(self, packet):

        window = [dict(item or {}) for item in list((packet or {}).get("window", []) or []) if isinstance(item, dict)]
        if not window:
            return None

        first = dict(window[0] or {})
        last = dict(window[-1] or {})
        tail = []

        for item in window[-3:]:
            row = dict(item or {})
            tail.append(
                (
                    int(float(row.get("timestamp", 0) or 0)),
                    round(float(row.get("open", 0.0) or 0.0), 8),
                    round(float(row.get("high", 0.0) or 0.0), 8),
                    round(float(row.get("low", 0.0) or 0.0), 8),
                    round(float(row.get("close", 0.0) or 0.0), 8),
                    round(float(row.get("volume", 0.0) or 0.0), 8),
                )
            )

        return (
            int(float(last.get("timestamp", (packet or {}).get("timestamp", 0)) or 0)),
            int(float(first.get("timestamp", 0) or 0)),
            len(window),
            tuple(tail),
        )
    # --------------------------------------------------
    def _normalize_market_window(self, window):

        if not window:
            return []

        return [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
    # --------------------------------------------------
    def _build_market_perception_packet(self, window):

        return self._build_market_component_bundle(window)
    # --------------------------------------------------
    def _resolve_market_packet_payload(self, packet):

        item = dict(packet or {})
        window = [dict(entry or {}) for entry in list(item.get("window", []) or []) if isinstance(entry, dict)]

        return self._build_market_component_bundle(
            window,
            base_packet=item,
        )    
    # --------------------------------------------------
    def _build_candle_state_packet(self, window):

        local_window = self._normalize_market_window(window)
        if not local_window:
            return {}

        last = local_window[-1]
        prev_close = local_window[-2].get("close") if len(local_window) > 1 else None
        return dict(_build_candle_state(last, prev_close=prev_close) or {})
    # --------------------------------------------------
    def _build_tension_state_packet(self, window):

        local_window = self._normalize_market_window(window)
        if not local_window:
            return {}

        return dict(build_tension_state_from_window(local_window) or {})
    # --------------------------------------------------
    def _build_structure_perception_packet(self, window):

        local_window = self._normalize_market_window(window)
        if not local_window:
            return {}

        return dict(STRUCTURE_ENGINE.build_structure_perception_state(local_window) or {})
    # -------------------------------------------------- 
    def _build_visual_market_state_packet(self, window):

        local_window = self._normalize_market_window(window)
        if not local_window:
            return {}

        visual_state = dict(build_visual_market_state(local_window) or {})
        self._record_visual_cortex_protocol(local_window, visual_state)
        return dict(visual_state or {})
    # --------------------------------------------------
    def _record_visual_cortex_protocol(self, window, visual_market_state):

        if not bool(getattr(Config, "MCM_VISUAL_CORTEX_PROTOCOL_DEBUG", True)):
            return False

        visual = dict(visual_market_state or {})
        form_state = dict(visual.get("visual_form_state", {}) or {})
        axes = dict(form_state.get("axes", {}) or {})
        if not visual:
            return False

        local_window = self._normalize_market_window(window)
        timestamp = local_window[-1].get("timestamp") if local_window else getattr(self, "current_timestamp", None)
        visual_form_id = str(form_state.get("visual_form_id", "-") or "-")
        clarity_bucket = int(round(float(visual.get("visual_clarity", 0.0) or 0.0) * 10.0))
        blindness_bucket = int(round(float(visual.get("visual_blindness", 0.0) or 0.0) * 10.0))
        pressure_bucket = int(round(float(visual.get("visual_form_pressure", 0.0) or 0.0) * 10.0))

        protocol = dict(getattr(self, "mcm_visual_cortex_protocol", {}) or {})
        sequence = int(protocol.get("sequence", 0) or 0) + 1
        key = f"{visual_form_id}|c{clarity_bucket}|b{blindness_bucket}|p{pressure_bucket}"
        changed = bool(str(protocol.get("last_key", "") or "") != key)
        every_n = max(1, int(getattr(Config, "MCM_VISUAL_CORTEX_PROTOCOL_EVERY_N", 5) or 5))

        protocol.update({
            "sequence": int(sequence),
            "last_key": str(key),
            "last_visual_form_id": str(visual_form_id),
            "last_timestamp": timestamp,
        })
        setattr(self, "mcm_visual_cortex_protocol", dict(protocol))

        if not changed and (sequence % every_n) != 0:
            return False

        path = dbr_path("mcm_visual_cortex_protocol.csv")
        header_key = "_visual_cortex_protocol_header_written"
        write_header = (not os.path.exists(path)) and not bool(getattr(self, header_key, False))

        def _clean(value):
            return str(value).replace("\n", " ").replace(";", "|")

        def _num(source, key_name, default=0.0):
            try:
                return float((source or {}).get(key_name, default) or default)
            except Exception:
                return float(default)

        payload = ""
        if write_header:
            payload += (
                "timestamp;sequence;visual_form_id;visual_clarity;visual_object_stability;"
                "visual_form_novelty;visual_blindness;visual_form_pressure;visual_shape_resonance;"
                "visual_shape_fragility;edge_strength;curvature;density;fracture;flow;void;"
                "range_rhythm;direction_consistency;spatial_bias;directional_bias;range_position;"
                "short_impulse;mid_impulse;compression;expansion;body_pressure;wick_pressure;"
                "volume_bias;market_balance;breakout_tension;visual_coherence;"
                "sensory_reality_pressure;sensory_load;sensory_redundancy;sensory_habituation;"
                "sensory_gate;sensory_active_axis_count;sensory_primary_pressure;sensory_reality_label\n"
            )
            setattr(self, header_key, True)

        row = [
            _clean(timestamp),
            int(sequence),
            _clean(visual_form_id),
            f"{_num(visual, 'visual_clarity'):.4f}",
            f"{_num(visual, 'visual_object_stability'):.4f}",
            f"{_num(visual, 'visual_form_novelty'):.4f}",
            f"{_num(visual, 'visual_blindness'):.4f}",
            f"{_num(visual, 'visual_form_pressure'):.4f}",
            f"{_num(visual, 'visual_shape_resonance'):.4f}",
            f"{_num(visual, 'visual_shape_fragility'):.4f}",
            f"{_num(axes, 'edge_strength'):.4f}",
            f"{_num(axes, 'curvature'):.4f}",
            f"{_num(axes, 'density'):.4f}",
            f"{_num(axes, 'fracture'):.4f}",
            f"{_num(axes, 'flow'):.4f}",
            f"{_num(axes, 'void'):.4f}",
            f"{_num(axes, 'range_rhythm'):.4f}",
            f"{_num(axes, 'direction_consistency'):.4f}",
            f"{_num(visual, 'spatial_bias'):.4f}",
            f"{_num(visual, 'directional_bias'):.4f}",
            f"{_num(visual, 'range_position'):.4f}",
            f"{_num(visual, 'short_impulse'):.4f}",
            f"{_num(visual, 'mid_impulse'):.4f}",
            f"{_num(visual, 'compression'):.4f}",
            f"{_num(visual, 'expansion'):.4f}",
            f"{_num(visual, 'body_pressure'):.4f}",
            f"{_num(visual, 'wick_pressure'):.4f}",
            f"{_num(visual, 'volume_bias'):.4f}",
            f"{_num(visual, 'market_balance'):.4f}",
            f"{_num(visual, 'breakout_tension'):.4f}",
            f"{_num(visual, 'visual_coherence'):.4f}",
            f"{_num(visual, 'sensory_reality_pressure'):.4f}",
            f"{_num(visual, 'sensory_load'):.4f}",
            f"{_num(visual, 'sensory_redundancy'):.4f}",
            f"{_num(visual, 'sensory_habituation'):.4f}",
            f"{_num(visual, 'sensory_gate', 1.0):.4f}",
            int(_num(visual, 'sensory_active_axis_count')),
            f"{_num(visual, 'sensory_primary_pressure'):.4f}",
            _clean(visual.get("sensory_reality_label", "quiet_outer_reality")),
        ]
        payload += ";".join(str(item) for item in row) + "\n"
        dbr_append_text(path, payload, operation="visual_cortex_protocol_append")
        return True
    # --------------------------------------------------     
    def _build_temporal_perception_state(self, window):

        previous_state = dict(getattr(self, "temporal_perception_state", {}) or {})
        candles = [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
        if len(candles) < 3:
            return {
                "flow_direction": float(previous_state.get("flow_direction", 0.0) or 0.0),
                "flow_strength": float(previous_state.get("flow_strength", 0.0) or 0.0),
                "flow_stability": float(previous_state.get("flow_stability", 0.0) or 0.0),
                "acceleration": 0.0,
                "swing_pressure": float(previous_state.get("swing_pressure", 0.0) or 0.0),
                "sequence_bias": str(previous_state.get("sequence_bias", "neutral") or "neutral"),
                "flow_memory": float(previous_state.get("flow_memory", 0.0) or 0.0),
                "transition_pressure": float(previous_state.get("transition_pressure", 0.0) or 0.0),
                "continuation_readiness": float(previous_state.get("continuation_readiness", 0.0) or 0.0),
                "temporal_exhaustion": float(previous_state.get("temporal_exhaustion", 0.0) or 0.0),
                "temporal_coherence": float(previous_state.get("temporal_coherence", 0.0) or 0.0),
                "state_drift": 0.0,
            }

        tail = candles[-12:]
        closes = [float(item.get("close", 0.0) or 0.0) for item in tail]
        highs = [float(item.get("high", 0.0) or 0.0) for item in tail]
        lows = [float(item.get("low", 0.0) or 0.0) for item in tail]

        deltas = []
        for index in range(1, len(closes)):
            deltas.append(float(closes[index] - closes[index - 1]))

        move_sum = sum(deltas)
        abs_sum = sum(abs(value) for value in deltas)
        raw_flow_direction = float(move_sum / max(abs_sum, 1e-9))
        raw_flow_strength = float(min(1.0, abs_sum / max(abs(closes[-1]) * 0.02, 1e-9)))

        direction_hits = 0
        for value in deltas:
            if move_sum >= 0.0 and value >= 0.0:
                direction_hits += 1
            elif move_sum < 0.0 and value <= 0.0:
                direction_hits += 1

        raw_flow_stability = float(direction_hits / max(1, len(deltas)))

        raw_acceleration = 0.0
        if len(deltas) >= 2:
            raw_acceleration = float(deltas[-1] - deltas[-2])

        range_span = max(max(highs) - min(lows), 1e-9)
        raw_swing_pressure = float(min(1.0, abs(raw_acceleration) / range_span))

        previous_direction = float(previous_state.get("flow_direction", 0.0) or 0.0)
        previous_strength = float(previous_state.get("flow_strength", 0.0) or 0.0)
        previous_stability = float(previous_state.get("flow_stability", 0.0) or 0.0)
        previous_swing_pressure = float(previous_state.get("swing_pressure", 0.0) or 0.0)
        previous_flow_memory = float(previous_state.get("flow_memory", 0.0) or 0.0)
        previous_transition_pressure = float(previous_state.get("transition_pressure", 0.0) or 0.0)
        previous_continuation_readiness = float(previous_state.get("continuation_readiness", 0.0) or 0.0)
        previous_temporal_exhaustion = float(previous_state.get("temporal_exhaustion", 0.0) or 0.0)
        previous_temporal_coherence = float(previous_state.get("temporal_coherence", 0.0) or 0.0)

        flow_direction = float((previous_direction * 0.34) + (raw_flow_direction * 0.66))
        flow_strength = float(min(1.0, max(0.0, (previous_strength * 0.26) + (raw_flow_strength * 0.74))))
        flow_stability = float(min(1.0, max(0.0, (previous_stability * 0.30) + (raw_flow_stability * 0.70))))
        swing_pressure = float(min(1.0, max(0.0, (previous_swing_pressure * 0.28) + (raw_swing_pressure * 0.72))))
        acceleration = float(raw_acceleration)

        state_drift = float(abs(flow_direction - previous_direction))
        direction_alignment = 1.0 - min(1.0, abs(flow_direction - previous_direction) / 2.0)
        flow_memory = float(max(-1.0, min(1.0, (previous_flow_memory * 0.58) + (flow_direction * 0.42))))
        transition_pressure = float(min(1.0, max(0.0, (previous_transition_pressure * 0.52) + (state_drift * 0.34) + (swing_pressure * 0.24) + (max(0.0, 1.0 - flow_stability) * 0.12))))
        continuation_readiness = float(min(1.0, max(0.0, (previous_continuation_readiness * 0.48) + (flow_strength * 0.24) + (flow_stability * 0.24) + (max(0.0, direction_alignment) * 0.16) - (transition_pressure * 0.18))))
        temporal_exhaustion = float(min(1.0, max(0.0, (previous_temporal_exhaustion * 0.62) + (swing_pressure * 0.20) + (max(0.0, abs(acceleration) / range_span) * 0.18) - (flow_stability * 0.10))))
        temporal_coherence = float(min(1.0, max(0.0, (previous_temporal_coherence * 0.34) + (flow_stability * 0.30) + (max(0.0, 1.0 - transition_pressure) * 0.22) + (max(0.0, 1.0 - temporal_exhaustion) * 0.14))))

        sequence_bias = "neutral"
        if flow_direction >= 0.18:
            sequence_bias = "up"
        elif flow_direction <= -0.18:
            sequence_bias = "down"

        return {
            "flow_direction": float(flow_direction),
            "flow_strength": float(flow_strength),
            "flow_stability": float(flow_stability),
            "acceleration": float(acceleration),
            "swing_pressure": float(swing_pressure),
            "sequence_bias": str(sequence_bias),
            "flow_memory": float(flow_memory),
            "transition_pressure": float(transition_pressure),
            "continuation_readiness": float(continuation_readiness),
            "temporal_exhaustion": float(temporal_exhaustion),
            "temporal_coherence": float(temporal_coherence),
            "state_drift": float(state_drift),
        }    
    # --------------------------------------------------
    def _apply_market_perception_state(self, resolved_packet):

        item = dict(resolved_packet or {})
        if not item:
            return None

        self.current_timestamp = item.get("timestamp", None)
        self.tension_state = dict(item.get("tension_state", {}) or {})
        self.visual_market_state = dict(item.get("visual_market_state", {}) or {})
        self.structure_perception_state = dict(item.get("structure_perception_state", {}) or {})
        self.temporal_perception_state = dict(item.get("temporal_perception_state", {}) or {})
        self.outer_market_state = dict(item.get("outer_market_state", {}) or {})
        return dict(item)
    # ==================================================
    # RUNTIME ADVANCE / INNENVERARBEITUNG
    # ==================================================
    def _compose_runtime_perception_packet(self, perception_packet, candle_state=None, visual_market_state=None, structure_perception_state=None):

        return self._build_runtime_market_packet(
            perception_packet,
            candle_state=candle_state,
            visual_market_state=visual_market_state,
            structure_perception_state=structure_perception_state,
        )
    # --------------------------------------------------
    def _advance_runtime_from_resolved_packet(self, resolved_packet):

        item = dict(resolved_packet or {})
        local_window = [dict(entry or {}) for entry in list(item.get("window", []) or []) if isinstance(entry, dict)]
        if not local_window:
            return None

        resolved_candle_state = dict(item.get("candle_state", {}) or {})
        resolved_tension_state = dict(item.get("tension_state", {}) or {})
        resolved_visual_market_state = dict(item.get("visual_market_state", {}) or {})
        resolved_structure_perception_state = dict(item.get("structure_perception_state", {}) or {})
        resolved_temporal_perception_state = dict(item.get("temporal_perception_state", {}) or {})

        return step_mcm_runtime(
            local_window,
            dict(resolved_candle_state or {}),
            bot=self,
            tension_state=dict(resolved_tension_state or {}),
            visual_market_state=dict(resolved_visual_market_state or {}),
            structure_perception_state=dict(resolved_structure_perception_state or {}),
            temporal_perception_state=dict(resolved_temporal_perception_state or {}),
        )    
    # --------------------------------------------------
    def _seed_runtime_window(self, resolved_packet):

        return self._run_runtime_packet_action_cycle(
            resolved_packet,
            seed_runtime=True,
        )
    # --------------------------------------------------
    def _build_prepared_runtime_action_context(self, window):

        action_context = self._build_runtime_action_context(window)
        if action_context is None:
            return None

        return self._prepare_runtime_action_context(
            action_context,
        )    
    # --------------------------------------------------
    def _process_market_packet(self, packet):

        resolved_packet = self._resolve_market_packet_payload(packet)
        if resolved_packet is None:
            return None

        window = [dict(entry or {}) for entry in list(resolved_packet.get("window", []) or []) if isinstance(entry, dict)]
        candle_state = dict(resolved_packet.get("candle_state", {}) or {})
        visual_market_state = dict(resolved_packet.get("visual_market_state", {}) or {})
        structure_perception_state = dict(resolved_packet.get("structure_perception_state", {}) or {})

        if not self._runtime_seeded:
            result = self._seed_runtime_window(
                resolved_packet,
            )
        else:
            result = self._process_runtime_packet(
                window,
                candle_state,
                visual_market_state=visual_market_state,
                structure_perception_state=structure_perception_state,
            )

        self._finalize_market_packet_processing(resolved_packet)
        return result
    # --------------------------------------------------
    def _process_runtime_packet(self, window, candle_state, visual_market_state=None, structure_perception_state=None):

        runtime_packet = self._build_current_runtime_packet(
            window,
            candle_state,
            visual_market_state=visual_market_state,
            structure_perception_state=structure_perception_state,
        )
        if runtime_packet is None:
            return None

        return self._run_runtime_packet_action_cycle(
            runtime_packet,
            seed_runtime=False,
        )
    # --------------------------------------------------
    def _runtime_market_followup_cycles(self):

        configured_cycles = max(
            1,
            int(
                getattr(
                    Config,
                    "MCM_RUNTIME_TICKS_PER_WINDOW",
                    getattr(Config, "MCM_INNER_TICKS_PER_WORLD_TICK", 1),
                ) or 1
            ),
        )

        followup_cycles = max(0, configured_cycles - 1)
        if followup_cycles <= 0:
            return 0

        dynamic_load = self._runtime_dynamic_load()
        scaled_cycles = int(round(dynamic_load * followup_cycles))
        return int(max(0, min(followup_cycles, scaled_cycles if followup_cycles > 1 else followup_cycles)))
    # --------------------------------------------------
    def _finalize_market_packet_processing(self, resolved_packet):

        item = dict(resolved_packet or {})
        window = [dict(entry or {}) for entry in list(item.get("window", []) or []) if isinstance(entry, dict)]
        if not window:
            return None

        candle_state = dict(item.get("candle_state", {}) or {})

        self._write_visualization_snapshots(
            window,
            candle_state,
        )

        self.processed += 1
        return True   
    # ==================================================
    # ACTION CONTEXT / RUNTIME HANDLUNGSVORBEREITUNG
    # ==================================================
    def _build_runtime_action_payload_state(self, action_context, candle_state=None, allow_empty: bool = False):

        resolved_context = self._resolve_runtime_action_context_state(
            action_context,
        )
        if resolved_context is None:
            if not bool(allow_empty):
                return None

            return {
                "window": [],
                "last": {},
                "timestamp": None,
                "live_mode": False,
                "external_order_active": False,
                "outer_market_state": {},
                "candle_state": dict(candle_state or {}),
            }

        return {
            "window": list(resolved_context.get("window", []) or []),
            "last": dict(resolved_context.get("last", {}) or {}),
            "timestamp": resolved_context.get("timestamp", None),
            "live_mode": bool(resolved_context.get("live_mode", False)),
            "external_order_active": bool(resolved_context.get("external_order_active", False)),
            "outer_market_state": dict(resolved_context.get("outer_market_state", {}) or {}),
            "candle_state": dict(candle_state or {}),
        }   
    # --------------------------------------------------  
    def _build_runtime_action_context(self, window):

        if not window:
            return None

        local_window = [dict(item or {}) for item in list(window or []) if isinstance(item, dict)]
        if not local_window:
            return None

        last = local_window[-1]
        timestamp = last.get("timestamp")
        context_flags = self._build_runtime_action_context_flags()

        return {
            "window": local_window,
            "last": last,
            "timestamp": timestamp,
            "live_mode": bool(context_flags.get("live_mode", False)),
            "external_order_active": bool(context_flags.get("external_order_active", False)),
            "outer_market_state": dict(context_flags.get("outer_market_state", {}) or {}),
        }
    # --------------------------------------------------
    def _normalize_runtime_action_context(self, action_context):

        payload_state = self._build_runtime_action_payload_state(
            action_context,
            allow_empty=False,
        )
        if payload_state is None:
            return None

        return {
            "window": list(payload_state.get("window", []) or []),
            "last": dict(payload_state.get("last", {}) or {}),
            "timestamp": payload_state.get("timestamp", None),
            "live_mode": bool(payload_state.get("live_mode", False)),
            "external_order_active": bool(payload_state.get("external_order_active", False)),
            "outer_market_state": dict(payload_state.get("outer_market_state", {}) or {}),
        }    
    # --------------------------------------------------
    def _apply_runtime_action_state(self, action_context):

        resolved_state = self._resolve_runtime_action_window_state(
            action_context,
        )
        if resolved_state is None:
            return None

        context = dict(resolved_state.get("context", {}) or {})
        timestamp = resolved_state.get("timestamp", None)

        if self.position and self.position.get("entry_ts") is None:
            self.position["entry_ts"] = timestamp
            self.position["last_checked_ts"] = timestamp

        self.current_timestamp = timestamp
        self.stats.data["current_timestamp"] = self.current_timestamp
        return dict(context or {})
    # --------------------------------------------------
    def _prepare_runtime_action_context(self, action_context):

        normalized_context = self._normalize_runtime_action_context(
            action_context,
        )
        if normalized_context is None:
            return None

        return self._apply_runtime_action_state(
            normalized_context,
        ) 
    # --------------------------------------------------
    def _run_runtime_action_cycle(self, window, candle_state):

        self._ensure_memory_state_loaded()

        prepared_context = self._build_prepared_runtime_action_context(window)
        if prepared_context is None:
            return None

        return self._run_runtime_execution_paths(
            prepared_context,
            candle_state,
        )   
    # --------------------------------------------------
    def _run_position_execution_path(self, action_context):

        payload = self._build_runtime_execution_payload(
            action_context,
        )
        return self._handle_active_position(
            payload.get("window", []),
            payload.get("last", {}),
            bool(payload.get("live_mode", False)),
        )
    # --------------------------------------------------
    def _run_pending_execution_path(self, action_context):

        payload = self._build_runtime_execution_payload(
            action_context,
        )
        return self._handle_pending_entry(
            payload.get("window", []),
            payload.get("last", {}),
            bool(payload.get("live_mode", False)),
        )
    # --------------------------------------------------
    def _run_decision_execution_path(self, action_context, candle_state):

        payload = self._build_runtime_execution_payload(
            action_context,
            candle_state=candle_state,
        )
        return self._handle_entry_attempt(
            payload.get("window", []),
            dict(payload.get("candle_state", {}) or {}),
            payload.get("last", {}),
            bool(payload.get("live_mode", False)),
            bool(payload.get("external_order_active", False)),
        )
    # ==================================================
    # ENTSCHEIDUNGSBAHN / HANDLUNGSBAHN
    # ==================================================
    def _finalize_pending_fill_handoff(self, side, entry_price, tp_price, sl_price, entry_ts, order_id, position_meta, reason: str):

        fill_state_before = self._build_regulation_state_snapshot()
        fill_risk = abs(float(entry_price) - float(sl_price))

        position_context = dict(position_meta or {})
        position_context["handoff_reason"] = str(reason or "pending_fill_handoff")
        position_context["felt_bearing_score"] = float(position_context.get("felt_bearing_score", 0.0) or 0.0)
        position_context["felt_profile_label"] = str(position_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear")
        position_context["bearing_context"] = dict(position_context.get("bearing_context", {}) or {})

        self.execution_state = {
            **dict(self.execution_state or {}),
            "execution_phase": "position_active",
            "execution_ready": True,
            "execution_blocked": False,
        }

        self.position = {
            "side": str(side),
            "entry": float(entry_price),
            "tp": float(tp_price),
            "sl": float(sl_price),
            "mfe": 0.0,
            "mae": 0.0,
            "risk": float(fill_risk),
            "order_id": order_id,
            "entry_ts": entry_ts,
            "entry_index": self.processed,
            "last_checked_ts": entry_ts,
            "meta": dict(position_context or {}),
        }

        fill_state_after = self._build_regulation_state_snapshot()
        fill_state_delta = self._build_regulation_state_delta(
            fill_state_before,
            fill_state_after,
        )

        self.pending_entry = None
        self.stats.on_attempt(
            status="filled",
            context=position_context,
        )
        mark_runtime_episode_event(
            self,
            "filled",
            {
                "position": dict(self.position or {}),
                "reason": str(reason or "pending_fill_handoff"),
                "bearing_context": dict((position_context.get("bearing_context", {}) or {})),
                "felt_bearing_score": float(position_context.get("felt_bearing_score", 0.0) or 0.0),
                "felt_profile_label": str(position_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                "state_before": dict(fill_state_before or {}),
                "state_after": dict(fill_state_after or {}),
                "state_delta": dict(fill_state_delta or {}),
            },
        )
        self._mark_memory_state_dirty()
        self._commit_regulation_state_snapshot(fill_state_after)
        return True
    # --------------------------------------------------   
    def _handle_decision_tendency(self, entry_result: dict):

        result = dict(entry_result or {})
        decision_tendency = str(result.get("decision_tendency", "") or "").strip().lower()

        self.action_intent_state = dict(result.get("action_intent_state", {}) or {})
        self.execution_state = dict(result.get("execution_state", {}) or {})

        if decision_tendency == "act":
            return False

        if decision_tendency == "observe":
            event_name = "observed_only"
        elif decision_tendency == "replan":
            event_name = "replanned"
        else:
            event_name = "withheld"

        state_before, state_after, state_delta = self._capture_regulation_transition()

        non_action_context = self._build_entry_attempt_context(
            result,
            state_before=state_before,
            state_after=state_after,
            state_delta=state_delta,
        )
        self.stats.on_attempt(
            status=event_name,
            context=non_action_context,
        )

        mark_runtime_episode_event(
            self,
            event_name,
            {
                "decision_tendency": str(decision_tendency or "hold"),
                "proposed_decision": str(result.get("proposed_decision", "WAIT") or "WAIT"),
                "reason": str(result.get("rejection_reason", "runtime_non_action") or "runtime_non_action"),
                "meta_regulation_state": dict(result.get("meta_regulation_state", {}) or {}),
                "expectation_state": dict(result.get("expectation_state", {}) or {}),
                "bearing_context": dict((non_action_context.get("bearing_context", {}) or {})),
                "felt_bearing_score": float(non_action_context.get("felt_bearing_score", 0.0) or 0.0),
                "felt_profile_label": str(non_action_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                "state_before": dict(state_before or {}),
                "state_after": dict(state_after or {}),
                "state_delta": dict(state_delta or {}),
            },
        )
        self._commit_regulation_state_snapshot(state_after)
        return True               
    # --------------------------------------------------   
    def _finalize_active_position_cancel(self, resolved_position, exit_context, order_id, cancel_cause):

        cancel_state_before = self._build_regulation_state_snapshot()
        position_for_outcome = dict(self.position or {})
        position_for_outcome["meta"] = {
            **dict(position_for_outcome.get("meta", {}) or {}),
            **dict(exit_context or {}),
        }
        apply_outcome_stimulus(self, "cancel", position_for_outcome)
        cancel_state_after = self._build_regulation_state_snapshot()
        cancel_state_delta = self._build_regulation_state_delta(
            cancel_state_before,
            cancel_state_after,
        )
        self.stats.on_attempt(
            status="cancelled",
            context=exit_context,
        )
        mark_runtime_episode_event(
            self,
            "cancelled",
            {
                "position": dict(resolved_position or {}),
                "reason": str(cancel_cause or "exchange_cancel"),
                "bearing_context": dict((exit_context.get("bearing_context", {}) or {})),
                "felt_bearing_score": float(exit_context.get("felt_bearing_score", 0.0) or 0.0),
                "felt_profile_label": str(exit_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                "state_before": dict(cancel_state_before or {}),
                "state_after": dict(cancel_state_after or {}),
                "state_delta": dict(cancel_state_delta or {}),
            },
        )
        self.stats.on_cancel(
            order_id=order_id,
            cause=str(cancel_cause or "exchange_cancel"),
            exploration_trade=False,
            outcome_decomposition=dict(getattr(self, "last_outcome_decomposition", {}) or {}),
            context=exit_context,
        )
        self._sync_last_outcome_decomposition_from_stats()
        self._mark_memory_state_dirty()
        self._commit_regulation_state_snapshot(cancel_state_after)
        self.position = None
        return True    
    # --------------------------------------------------   
    def _finalize_active_position_resolution(self, resolved_position, exit_context, reason, live_mode: bool):

        state_before = self._build_regulation_state_snapshot()
        position_for_outcome = dict(self.position or {})
        position_for_outcome["meta"] = {
            **dict(position_for_outcome.get("meta", {}) or {}),
            **dict(exit_context or {}),
        }
        apply_outcome_stimulus(self, reason, position_for_outcome)
        state_after = self._build_regulation_state_snapshot()
        state_delta = self._build_regulation_state_delta(
            state_before,
            state_after,
        )
        self._mark_memory_state_dirty()

        if str(reason).lower() == "sl_hit":
            self.mcm_pause_left = int(getattr(Config, "MCM_SL_PAUSE_STEPS", 3) or 3)

        self.stats.on_exit(
            entry=self.position.get("entry"),
            tp=self.position.get("tp"),
            sl=self.position.get("sl"),
            reason=reason,
            side=self.position.get("side"),
            amount=Config.ORDER_SIZE if live_mode else 1.0,
            exit_price=float(resolved_position.get("matured_exit_price", 0.0) or 0.0) if str(reason).lower() == "matured_exit" else None,
            exploration_trade=False,
            outcome_decomposition=dict(getattr(self, "last_outcome_decomposition", {}) or {}),
            context=exit_context,
        )
        self._sync_last_outcome_decomposition_from_stats()
        mark_runtime_episode_event(
            self,
            "resolved",
            {
                "position": dict(resolved_position or {}),
                "reason": str(reason or "-"),
                "bearing_context": dict((exit_context.get("bearing_context", {}) or {})),
                "felt_bearing_score": float(exit_context.get("felt_bearing_score", 0.0) or 0.0),
                "felt_profile_label": str(exit_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                "state_before": dict(state_before or {}),
                "state_after": dict(state_after or {}),
                "state_delta": dict(state_delta or {}),
            },
        )

        self._commit_regulation_state_snapshot(state_after)
        self.position = None
        return True    
    # --------------------------------------------------   
    def _build_position_intervention_state(
        self,
        *,
        close_price: float,
        entry_price: float,
        side: str,
        risk_value: float,
        mfe_r: float,
        mae_r: float,
        fill_ratio: float,
        pressure_to_capacity: float,
        bars_open: int,
    ) -> dict:

        def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
            try:
                return max(lo, min(hi, float(value)))
            except Exception:
                return lo

        if risk_value <= 0.0:
            return {}

        side = str(side or "").upper().strip()
        if side == "LONG":
            current_r = (float(close_price) - float(entry_price)) / max(risk_value, 1e-9)
        elif side == "SHORT":
            current_r = (float(entry_price) - float(close_price)) / max(risk_value, 1e-9)
        else:
            current_r = 0.0

        giveback_r = max(0.0, float(mfe_r) - float(current_r))
        structure_quality = float((self.structure_perception_state or {}).get("structure_quality", 0.0) or 0.0)
        structure_stability = float((self.structure_perception_state or {}).get("structure_stability", structure_quality) or 0.0)
        context_confidence = float((self.structure_perception_state or {}).get("context_confidence", structure_quality) or 0.0)
        regulatory_load = float(getattr(self, "regulatory_load", 0.0) or 0.0)
        action_capacity = float(getattr(self, "action_capacity", 0.0) or 0.0)
        recovery_need = float(getattr(self, "recovery_need", 0.0) or 0.0)
        recovery_balance = float(getattr(self, "recovery_balance", 0.0) or 0.0)
        survival_pressure = float(getattr(self, "survival_pressure", 0.0) or 0.0)
        if pressure_to_capacity <= 0.0 and action_capacity > 0.0:
            pressure_to_capacity = regulatory_load / max(0.05, action_capacity)

        pressure_load = _clamp(float(pressure_to_capacity) / 2.25)
        giveback_load = _clamp(giveback_r / 2.50)
        adverse_load = _clamp(float(mae_r) / 1.20)
        recovery_load = _clamp(float(recovery_need) + max(0.0, -float(recovery_balance)))
        structure_loss = _clamp((0.62 - structure_quality) / 0.35)
        confidence_loss = _clamp((0.58 - context_confidence) / 0.35)
        negative_current_load = _clamp((-current_r) / 0.90)

        exit_decision_pressure = _clamp(
            (giveback_load * 0.30)
            + (structure_loss * 0.24)
            + (pressure_load * 0.20)
            + (negative_current_load * 0.16)
            + (adverse_load * 0.10)
        )
        position_cognitive_load = _clamp(
            (pressure_load * 0.24)
            + (regulatory_load * 0.20)
            + (recovery_load * 0.18)
            + (exit_decision_pressure * 0.18)
            + (survival_pressure * 0.10)
            + (_clamp(float(bars_open) / 64.0) * 0.10)
        )
        plan_trust = _clamp(
            (structure_quality * 0.26)
            + (structure_stability * 0.18)
            + (context_confidence * 0.16)
            + (_clamp(current_r / 1.40) * 0.14)
            + ((1.0 - pressure_load) * 0.12)
            + ((1.0 - giveback_load) * 0.10)
            + ((1.0 - recovery_load) * 0.04)
        )
        holding_stability = _clamp(
            (plan_trust * 0.46)
            + ((1.0 - exit_decision_pressure) * 0.24)
            + (_clamp(current_r / 1.75) * 0.16)
            + ((1.0 - position_cognitive_load) * 0.14)
        )
        inner_noise = _clamp(
            (position_cognitive_load * 0.32)
            + (exit_decision_pressure * 0.28)
            + (abs(plan_trust - exit_decision_pressure) * 0.14)
            + (confidence_loss * 0.14)
            + (_clamp(giveback_r / max(float(mfe_r), 0.25)) * 0.12)
        )

        contact_state = dict(getattr(self, "active_mcm_contact_state", {}) or {})
        temporal_state = dict(getattr(self, "temporal_perception_state", {}) or {})
        meta_state = dict(getattr(self, "meta_regulation_state", {}) or {})
        contact_reality_check = _clamp(contact_state.get("contact_reality_check", 0.0))
        contact_temporal_bearing = _clamp(contact_state.get("contact_temporal_bearing", 0.0))
        contact_bearing_gap = _clamp(contact_state.get("contact_bearing_gap", 0.0))
        contact_action_maturity = _clamp(contact_state.get("contact_action_maturity", 0.0))
        contact_learning_need = _clamp(contact_state.get("contact_learning_need", 0.0))
        contact_overcoupling_risk = _clamp(contact_state.get("contact_overcoupling_risk", 0.0))
        temporal_self_location = _clamp(temporal_state.get("temporal_self_location", 0.0))
        spacetime_reflection_need = _clamp(meta_state.get("spacetime_reflection_need", 0.0))
        structure_action_uncertainty = _clamp(meta_state.get("structure_action_uncertainty", 0.0))

        position_self_trust_gap = _clamp(
            ((1.0 - plan_trust) * 0.22)
            + (contact_bearing_gap * 0.18)
            + ((1.0 - contact_reality_check) * 0.14)
            + ((1.0 - contact_temporal_bearing) * 0.12)
            + (structure_action_uncertainty * 0.12)
            + (negative_current_load * 0.10)
            + (giveback_load * 0.08)
            + ((1.0 - temporal_self_location) * 0.04)
        )
        position_inconsistency_stress = _clamp(
            (position_self_trust_gap * 0.26)
            + (position_cognitive_load * 0.20)
            + (exit_decision_pressure * 0.16)
            + (inner_noise * 0.14)
            + (adverse_load * 0.10)
            + (contact_learning_need * 0.08)
            + (spacetime_reflection_need * 0.06)
        )
        position_noradrenaline_arousal = _clamp(
            (exit_decision_pressure * 0.28)
            + (negative_current_load * 0.20)
            + (giveback_load * 0.18)
            + (contact_overcoupling_risk * 0.14)
            + (structure_action_uncertainty * 0.12)
            + (_clamp(float(bars_open) / 40.0) * 0.08)
        )
        prior_count = int(self.position.get("intervention_pressure_count", 0) or 0) if self.position else 0
        prior_sum = float(self.position.get("intervention_pressure_sum", 0.0) or 0.0) if self.position else 0.0
        pressure_count = prior_count + 1
        pressure_sum = prior_sum + float(exit_decision_pressure)
        sustained_exit_pressure = _clamp(pressure_sum / max(1, pressure_count))

        position_cortisol_load = _clamp(
            (position_inconsistency_stress * 0.32)
            + (position_cognitive_load * 0.22)
            + (sustained_exit_pressure * 0.18)
            + (recovery_load * 0.12)
            + (adverse_load * 0.08)
            + (spacetime_reflection_need * 0.08)
        )
        position_mcm_field_strain = _clamp(
            (position_cortisol_load * 0.26)
            + (position_noradrenaline_arousal * 0.22)
            + (contact_overcoupling_risk * 0.18)
            + (position_self_trust_gap * 0.16)
            + ((1.0 - holding_stability) * 0.10)
            + ((1.0 - temporal_self_location) * 0.08)
        )
        position_protective_distance = _clamp(
            (position_mcm_field_strain * 0.28)
            + (position_self_trust_gap * 0.22)
            + (position_cortisol_load * 0.18)
            + (spacetime_reflection_need * 0.14)
            + ((1.0 - contact_action_maturity) * 0.10)
            + ((1.0 - holding_stability) * 0.08)
        )
        position_held_risk_discomfort = _clamp(
            (adverse_load * 0.22)
            + (negative_current_load * 0.20)
            + (position_self_trust_gap * 0.18)
            + (position_noradrenaline_arousal * 0.16)
            + (position_cortisol_load * 0.14)
            + (giveback_load * 0.10)
        )
        position_process_quality = _clamp(
            (plan_trust * 0.22)
            + (holding_stability * 0.18)
            + (contact_reality_check * 0.14)
            + (contact_temporal_bearing * 0.12)
            + (contact_action_maturity * 0.10)
            + ((1.0 - position_inconsistency_stress) * 0.10)
            + ((1.0 - position_mcm_field_strain) * 0.08)
            + ((1.0 - position_held_risk_discomfort) * 0.06)
        )

        intervention_fatigue = _clamp(
            (sustained_exit_pressure * 0.48)
            + (_clamp(pressure_count / 48.0) * 0.20)
            + (position_cognitive_load * 0.20)
            + (inner_noise * 0.12)
        )
        intervention_unfit_state = _clamp(
            (position_cognitive_load * 0.34)
            + (inner_noise * 0.24)
            + ((1.0 - plan_trust) * 0.20)
            + (intervention_fatigue * 0.14)
            + ((1.0 - holding_stability) * 0.08)
        )
        exit_evidence = _clamp(
            (structure_loss * 0.30)
            + (giveback_load * 0.26)
            + (negative_current_load * 0.20)
            + (pressure_load * 0.16)
            + (adverse_load * 0.08)
        )
        intervention_fitness = _clamp(exit_evidence * (1.0 - (intervention_unfit_state * 0.65)))

        if self.position is not None:
            self.position["intervention_pressure_count"] = int(pressure_count)
            self.position["intervention_pressure_sum"] = float(pressure_sum)

        if intervention_fitness >= 0.62 and exit_decision_pressure >= 0.55:
            intervention_label = "confirmed_exit_candidate"
        elif intervention_unfit_state >= 0.58 and exit_decision_pressure >= 0.45:
            intervention_label = "intervention_unfit_state"
        elif plan_trust >= 0.58 and holding_stability >= 0.52:
            intervention_label = "plan_holding_trust"
        elif exit_decision_pressure >= 0.46:
            intervention_label = "exit_nervousness_observe"
        else:
            intervention_label = "quiet_position_watch"

        if position_process_quality >= 0.58 and position_mcm_field_strain <= 0.36:
            position_experience_label = "carried_position_contact"
        elif current_r > 0.0 and position_process_quality < 0.42:
            position_experience_label = "unearned_relief_watch"
        elif position_cortisol_load >= 0.56 or position_held_risk_discomfort >= 0.58:
            position_experience_label = "protective_stress_contact"
        elif position_self_trust_gap >= 0.50:
            position_experience_label = "self_trust_gap_contact"
        elif position_protective_distance >= 0.48:
            position_experience_label = "protective_distance_watch"
        else:
            position_experience_label = "open_position_feel"

        position_experience_state = {
            "position_inconsistency_stress": float(position_inconsistency_stress),
            "position_mcm_field_strain": float(position_mcm_field_strain),
            "position_self_trust_gap": float(position_self_trust_gap),
            "position_cortisol_load": float(position_cortisol_load),
            "position_noradrenaline_arousal": float(position_noradrenaline_arousal),
            "position_protective_distance": float(position_protective_distance),
            "position_held_risk_discomfort": float(position_held_risk_discomfort),
            "position_process_quality": float(position_process_quality),
            "position_experience_label": str(position_experience_label),
        }

        state = {
            "position_cognitive_load": float(position_cognitive_load),
            "exit_decision_pressure": float(exit_decision_pressure),
            "holding_stability": float(holding_stability),
            "plan_trust": float(plan_trust),
            "intervention_fatigue": float(intervention_fatigue),
            "inner_noise": float(inner_noise),
            "intervention_fitness": float(intervention_fitness),
            "intervention_unfit_state": float(intervention_unfit_state),
            "exit_evidence": float(exit_evidence),
            "sustained_exit_pressure": float(sustained_exit_pressure),
            "current_r": float(current_r),
            "giveback_r": float(giveback_r),
            "mfe_r": float(mfe_r),
            "mae_r": float(mae_r),
            "pressure_to_capacity": float(pressure_to_capacity),
            "structure_quality": float(structure_quality),
            "structure_stability": float(structure_stability),
            "context_confidence": float(context_confidence),
            "bars_open": int(bars_open),
            "intervention_label": str(intervention_label),
            "position_inconsistency_stress": float(position_inconsistency_stress),
            "position_mcm_field_strain": float(position_mcm_field_strain),
            "position_self_trust_gap": float(position_self_trust_gap),
            "position_cortisol_load": float(position_cortisol_load),
            "position_noradrenaline_arousal": float(position_noradrenaline_arousal),
            "position_protective_distance": float(position_protective_distance),
            "position_held_risk_discomfort": float(position_held_risk_discomfort),
            "position_process_quality": float(position_process_quality),
            "position_experience_label": str(position_experience_label),
            "position_experience_state": dict(position_experience_state),
        }

        if bool(getattr(Config, "MCM_POSITION_INTERVENTION_PROTOCOL_DEBUG", True)):
            every_n = max(1, int(getattr(Config, "MCM_POSITION_INTERVENTION_PROTOCOL_EVERY_N", 5) or 5))
            should_write = (int(getattr(self, "processed", 0) or 0) % every_n == 0) or exit_decision_pressure >= 0.46
            if should_write:
                dbr_debug(
                    "POSITION_INTERVENTION "
                    f"ts={int(getattr(self, 'current_timestamp', 0) or 0)} side={side} "
                    f"entry={float(entry_price):.4f} close={float(close_price):.4f} "
                    f"current_r={current_r:.4f} mfe_r={float(mfe_r):.4f} mae_r={float(mae_r):.4f} "
                    f"giveback_r={giveback_r:.4f} position_cognitive_load={position_cognitive_load:.4f} "
                    f"exit_decision_pressure={exit_decision_pressure:.4f} plan_trust={plan_trust:.4f} "
                    f"holding_stability={holding_stability:.4f} intervention_fatigue={intervention_fatigue:.4f} "
                    f"inner_noise={inner_noise:.4f} intervention_unfit_state={intervention_unfit_state:.4f} "
                    f"intervention_fitness={intervention_fitness:.4f} label={intervention_label} "
                    f"position_inconsistency_stress={position_inconsistency_stress:.4f} "
                    f"position_mcm_field_strain={position_mcm_field_strain:.4f} "
                    f"position_self_trust_gap={position_self_trust_gap:.4f} "
                    f"position_cortisol_load={position_cortisol_load:.4f} "
                    f"position_noradrenaline_arousal={position_noradrenaline_arousal:.4f} "
                    f"position_protective_distance={position_protective_distance:.4f} "
                    f"position_held_risk_discomfort={position_held_risk_discomfort:.4f} "
                    f"position_process_quality={position_process_quality:.4f} "
                    f"position_experience_label={position_experience_label}",
                    "mcm_position_intervention_protocol.csv",
                )

        return state
    # --------------------------------------------------   
    def _build_target_expectation_state(
        self,
        *,
        position_intervention_state: dict,
        side: str,
        entry_price: float,
        close_price: float,
        tp_price: float,
        risk_value: float,
        bars_open: int,
    ) -> dict:

        state = dict(position_intervention_state or {})
        if not state or risk_value <= 0.0:
            return {}

        def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
            try:
                return max(lo, min(hi, float(value)))
            except Exception:
                return lo

        def _val(key: str) -> float:
            try:
                return float(state.get(key, 0.0) or 0.0)
            except Exception:
                return 0.0

        side = str(side or "").upper().strip()
        if side == "LONG":
            current_r = (float(close_price) - float(entry_price)) / max(float(risk_value), 1e-9)
            target_total_r = max(0.0, (float(tp_price) - float(entry_price)) / max(float(risk_value), 1e-9))
        elif side == "SHORT":
            current_r = (float(entry_price) - float(close_price)) / max(float(risk_value), 1e-9)
            target_total_r = max(0.0, (float(entry_price) - float(tp_price)) / max(float(risk_value), 1e-9))
        else:
            current_r = _val("current_r")
            target_total_r = 0.0

        target_total_r = max(float(target_total_r), 0.01)
        target_progress = _clamp(float(current_r) / target_total_r)
        target_remaining_r = max(0.0, target_total_r - float(current_r))
        target_remaining_pressure = _clamp(target_remaining_r / max(target_total_r, 0.01))

        plan_trust = _val("plan_trust")
        holding_stability = _val("holding_stability")
        exit_decision_pressure = _val("exit_decision_pressure")
        exit_evidence = _val("exit_evidence")
        structure_quality = _val("structure_quality")
        structure_stability = _val("structure_stability")
        context_confidence = _val("context_confidence")
        giveback_r = _val("giveback_r")
        mfe_r = _val("mfe_r")
        mae_r = _val("mae_r")
        position_cognitive_load = _val("position_cognitive_load")
        intervention_unfit_state = _val("intervention_unfit_state")

        position_meta = dict((self.position or {}).get("meta", {}) or {})
        expectation_state = dict(position_meta.get("expectation_state", {}) or {})
        experience_state = dict(position_meta.get("experience", {}) or {})
        entry_meta_regulation_state = dict(position_meta.get("meta_regulation_state", {}) or {})
        current_meta_regulation_state = dict(getattr(self, "meta_regulation_state", {}) or {})
        base_entry_expectation = float(
            expectation_state.get(
                "entry_expectation",
                experience_state.get("entry_expectation", 0.0),
            ) or 0.0
        )
        base_target_expectation = float(
            expectation_state.get(
                "target_expectation",
                experience_state.get("target_expectation", 0.0),
            ) or 0.0
        )
        base_expectation_support = _clamp((base_entry_expectation * 0.62) + (base_target_expectation * 0.38))

        giveback_load = _clamp(giveback_r / 2.50)
        adverse_load = _clamp(mae_r / 1.20)
        negative_current_load = _clamp((-float(current_r)) / 0.90)
        path_pullback_load = _clamp(giveback_r / max(float(mfe_r), 0.25))
        time_pressure = _clamp(float(bars_open) / 96.0)

        tp_reachability = _clamp(
            (plan_trust * 0.26)
            + (holding_stability * 0.20)
            + (structure_quality * 0.16)
            + (context_confidence * 0.12)
            + (target_progress * 0.10)
            + ((1.0 - giveback_load) * 0.07)
            + ((1.0 - negative_current_load) * 0.05)
            + (base_expectation_support * 0.04)
        )
        target_path_integrity = _clamp(
            (structure_stability * 0.24)
            + (plan_trust * 0.22)
            + (holding_stability * 0.18)
            + (context_confidence * 0.12)
            + ((1.0 - path_pullback_load) * 0.10)
            + ((1.0 - adverse_load) * 0.08)
            + (base_expectation_support * 0.06)
        )
        expectation_deviation = _clamp(
            ((1.0 - target_path_integrity) * 0.28)
            + (exit_decision_pressure * 0.22)
            + (negative_current_load * 0.18)
            + (giveback_load * 0.14)
            + ((1.0 - plan_trust) * 0.10)
            + (position_cognitive_load * 0.08)
        )
        expectation_break_pressure = _clamp(
            (expectation_deviation * 0.38)
            + (exit_evidence * 0.22)
            + ((1.0 - tp_reachability) * 0.18)
            + (negative_current_load * 0.12)
            + (intervention_unfit_state * 0.10)
        )
        expectation_hold_support = _clamp(
            (tp_reachability * 0.38)
            + (target_path_integrity * 0.28)
            + (plan_trust * 0.16)
            + (holding_stability * 0.12)
            + ((1.0 - expectation_break_pressure) * 0.06)
        )
        target_room_pressure = _clamp(
            (target_remaining_pressure * 0.34)
            + (exit_decision_pressure * 0.22)
            + (time_pressure * 0.14)
            + (path_pullback_load * 0.14)
            + (position_cognitive_load * 0.10)
            + ((1.0 - base_expectation_support) * 0.06)
        )
        target_semantic_confidence = _clamp(
            (context_confidence * 0.30)
            + (structure_quality * 0.22)
            + (structure_stability * 0.18)
            + (base_expectation_support * 0.16)
            + ((1.0 - position_cognitive_load) * 0.08)
            + ((1.0 - target_room_pressure) * 0.06)
        )
        entry_route_familiarity = _clamp(entry_meta_regulation_state.get("route_familiarity", 0.0))
        entry_transfer_bearing = _clamp(entry_meta_regulation_state.get("transfer_bearing", 0.0))
        current_route_familiarity = _clamp(current_meta_regulation_state.get("route_familiarity", entry_route_familiarity))
        current_semantic_shift_pressure = _clamp(current_meta_regulation_state.get("semantic_shift_pressure", 0.0))
        current_transfer_bearing = _clamp(current_meta_regulation_state.get("transfer_bearing", entry_transfer_bearing))
        current_interpretation_quality = _clamp(current_meta_regulation_state.get("interpretation_quality", 0.0))
        current_adaptation_phase = str(current_meta_regulation_state.get("adaptation_phase", "-") or "-")
        route_familiarity_delta = max(-1.0, min(1.0, current_route_familiarity - entry_route_familiarity))
        transfer_bearing_delta = max(-1.0, min(1.0, current_transfer_bearing - entry_transfer_bearing))
        semantic_transfer_stress = _clamp(
            (current_semantic_shift_pressure * 0.42)
            + ((1.0 - current_transfer_bearing) * 0.24)
            + ((1.0 - current_route_familiarity) * 0.16)
            + (max(0.0, -route_familiarity_delta) * 0.10)
            + (max(0.0, -transfer_bearing_delta) * 0.08)
        )

        prior_target_hold_support = 0.0
        prior_tp_reachability = 0.0
        prior_target_path_integrity = 0.0
        previous_tp_reachability = tp_reachability
        previous_target_path_integrity = target_path_integrity
        previous_expectation_hold_support = expectation_hold_support
        previous_expectation_break_pressure = expectation_break_pressure
        previous_current_r = current_r
        previous_target_progress = target_progress
        prior_break_count = 0
        if self.position is not None:
            prior_target_hold_support = float(self.position.get("target_hold_support_peak", 0.0) or 0.0)
            prior_tp_reachability = float(self.position.get("tp_reachability_peak", 0.0) or 0.0)
            prior_target_path_integrity = float(self.position.get("target_path_integrity_peak", 0.0) or 0.0)
            previous_tp_reachability = float(self.position.get("last_tp_reachability", tp_reachability) or 0.0)
            previous_target_path_integrity = float(self.position.get("last_target_path_integrity", target_path_integrity) or 0.0)
            previous_expectation_hold_support = float(self.position.get("last_expectation_hold_support", expectation_hold_support) or 0.0)
            previous_expectation_break_pressure = float(self.position.get("last_expectation_break_pressure", expectation_break_pressure) or 0.0)
            previous_current_r = float(self.position.get("last_current_r", current_r) or 0.0)
            previous_target_progress = float(self.position.get("last_target_progress", target_progress) or 0.0)
            prior_break_count = int(self.position.get("expectation_break_count", 0) or 0)

        break_active = bool(expectation_break_pressure >= 0.58 and expectation_hold_support <= 0.52)
        if break_active:
            expectation_break_count = prior_break_count + 1
        else:
            expectation_break_count = max(0, prior_break_count - 1)

        expectation_break_persistence = _clamp(
            (_clamp(expectation_break_count / 4.0) * 0.42)
            + (expectation_break_pressure * 0.24)
            + ((1.0 - expectation_hold_support) * 0.16)
            + (expectation_deviation * 0.12)
            + (target_room_pressure * 0.06)
        )
        target_recovery_potential = _clamp(
            (prior_target_hold_support * 0.24)
            + (prior_tp_reachability * 0.18)
            + (prior_target_path_integrity * 0.12)
            + (structure_stability * 0.14)
            + (context_confidence * 0.10)
            + (_clamp(mfe_r / 2.0) * 0.10)
            + ((1.0 - negative_current_load) * 0.06)
            + ((1.0 - path_pullback_load) * 0.04)
            + (base_expectation_support * 0.02)
        )
        target_recovery_momentum = _clamp(
            (_clamp((tp_reachability - previous_tp_reachability) / 0.18) * 0.24)
            + (_clamp((target_path_integrity - previous_target_path_integrity) / 0.18) * 0.20)
            + (_clamp((expectation_hold_support - previous_expectation_hold_support) / 0.18) * 0.20)
            + (_clamp((previous_expectation_break_pressure - expectation_break_pressure) / 0.20) * 0.16)
            + (_clamp((current_r - previous_current_r) / 0.45) * 0.12)
            + (_clamp((target_progress - previous_target_progress) / 0.20) * 0.08)
        )
        break_to_recovery_delta = _clamp(
            (target_recovery_momentum * 0.40)
            + (expectation_hold_support * 0.20)
            + (target_path_integrity * 0.18)
            + ((1.0 - expectation_break_pressure) * 0.14)
            + (target_semantic_confidence * 0.08)
        )
        target_recovery_confirmation = _clamp(
            (target_recovery_momentum * 0.34)
            + (break_to_recovery_delta * 0.26)
            + (target_recovery_potential * 0.18)
            + ((1.0 - expectation_break_persistence) * 0.12)
            + (target_semantic_confidence * 0.10)
        )
        recovery_after_break_watch = bool(
            prior_break_count > 0
            and not break_active
            and target_recovery_momentum >= 0.30
            and target_recovery_confirmation >= 0.56
            and expectation_break_pressure < 0.54
        )
        deep_pullback_recovery_watch = bool(
            break_active
            and target_recovery_potential >= 0.60
            and target_recovery_momentum >= 0.28
            and target_recovery_confirmation >= 0.52
            and expectation_break_persistence <= 0.68
        )

        if self.position is not None:
            self.position["target_hold_support_peak"] = float(max(prior_target_hold_support * 0.92, expectation_hold_support))
            self.position["tp_reachability_peak"] = float(max(prior_tp_reachability * 0.92, tp_reachability))
            self.position["target_path_integrity_peak"] = float(max(prior_target_path_integrity * 0.92, target_path_integrity))
            self.position["expectation_break_count"] = int(expectation_break_count)
            self.position["last_tp_reachability"] = float(tp_reachability)
            self.position["last_target_path_integrity"] = float(target_path_integrity)
            self.position["last_expectation_hold_support"] = float(expectation_hold_support)
            self.position["last_expectation_break_pressure"] = float(expectation_break_pressure)
            self.position["last_current_r"] = float(current_r)
            self.position["last_target_progress"] = float(target_progress)

        if recovery_after_break_watch:
            expectation_label = "recovery_after_break_watch"
        elif deep_pullback_recovery_watch:
            expectation_label = "deep_pullback_recovery_watch"
        elif break_active:
            expectation_label = "expectation_break_observe"
        elif expectation_hold_support >= 0.58 and expectation_break_pressure < 0.48:
            expectation_label = "target_expectation_holds"
        elif path_pullback_load >= 0.55 and tp_reachability >= 0.50:
            expectation_label = "target_pullback_observe"
        elif target_semantic_confidence <= 0.42 or expectation_deviation >= 0.52:
            expectation_label = "target_unclear_observe"
        else:
            expectation_label = "target_watch"

        result = {
            "target_expectation_context": str(expectation_label),
            "tp_reachability": float(tp_reachability),
            "target_path_integrity": float(target_path_integrity),
            "expectation_deviation": float(expectation_deviation),
            "expectation_break_pressure": float(expectation_break_pressure),
            "expectation_hold_support": float(expectation_hold_support),
            "target_room_pressure": float(target_room_pressure),
            "target_semantic_confidence": float(target_semantic_confidence),
            "target_progress": float(target_progress),
            "target_remaining_r": float(target_remaining_r),
            "target_total_r": float(target_total_r),
            "target_recovery_potential": float(target_recovery_potential),
            "target_recovery_momentum": float(target_recovery_momentum),
            "target_recovery_confirmation": float(target_recovery_confirmation),
            "break_to_recovery_delta": float(break_to_recovery_delta),
            "recovery_after_break_watch": bool(recovery_after_break_watch),
            "prior_target_hold_support": float(prior_target_hold_support),
            "prior_tp_reachability": float(prior_tp_reachability),
            "prior_target_path_integrity": float(prior_target_path_integrity),
            "expectation_break_persistence": float(expectation_break_persistence),
            "expectation_break_count": int(expectation_break_count),
            "deep_pullback_recovery_watch": bool(deep_pullback_recovery_watch),
            "base_entry_expectation": float(base_entry_expectation),
            "base_target_expectation": float(base_target_expectation),
            "entry_route_familiarity": float(entry_route_familiarity),
            "entry_transfer_bearing": float(entry_transfer_bearing),
            "current_route_familiarity": float(current_route_familiarity),
            "current_semantic_shift_pressure": float(current_semantic_shift_pressure),
            "current_transfer_bearing": float(current_transfer_bearing),
            "current_interpretation_quality": float(current_interpretation_quality),
            "current_adaptation_phase": str(current_adaptation_phase),
            "route_familiarity_delta": float(route_familiarity_delta),
            "transfer_bearing_delta": float(transfer_bearing_delta),
            "semantic_transfer_stress": float(semantic_transfer_stress),
        }

        if bool(getattr(Config, "MCM_TARGET_EXPECTATION_PROTOCOL_DEBUG", True)):
            every_n = max(1, int(getattr(Config, "MCM_TARGET_EXPECTATION_PROTOCOL_EVERY_N", 5) or 5))
            should_write = (
                (int(getattr(self, "processed", 0) or 0) % every_n == 0)
                or expectation_break_pressure >= 0.52
                or expectation_label != "target_watch"
            )
            if should_write:
                dbr_debug(
                    "TARGET_EXPECTATION "
                    f"ts={int(getattr(self, 'current_timestamp', 0) or 0)} "
                    f"label={expectation_label} side={side} "
                    f"entry={float(entry_price):.4f} close={float(close_price):.4f} tp={float(tp_price):.4f} "
                    f"tp_reachability={tp_reachability:.4f} target_path_integrity={target_path_integrity:.4f} "
                    f"expectation_deviation={expectation_deviation:.4f} "
                    f"expectation_break_pressure={expectation_break_pressure:.4f} "
                    f"expectation_hold_support={expectation_hold_support:.4f} "
                    f"target_room_pressure={target_room_pressure:.4f} "
                    f"target_semantic_confidence={target_semantic_confidence:.4f} "
                    f"target_progress={target_progress:.4f} target_remaining_r={target_remaining_r:.4f} "
                    f"target_recovery_potential={target_recovery_potential:.4f} "
                    f"target_recovery_momentum={target_recovery_momentum:.4f} "
                    f"target_recovery_confirmation={target_recovery_confirmation:.4f} "
                    f"break_to_recovery_delta={break_to_recovery_delta:.4f} "
                    f"current_route_familiarity={current_route_familiarity:.4f} "
                    f"current_semantic_shift_pressure={current_semantic_shift_pressure:.4f} "
                    f"current_transfer_bearing={current_transfer_bearing:.4f} "
                    f"semantic_transfer_stress={semantic_transfer_stress:.4f} "
                    f"current_adaptation_phase={current_adaptation_phase} "
                    f"prior_target_hold_support={prior_target_hold_support:.4f} "
                    f"expectation_break_persistence={expectation_break_persistence:.4f} "
                    f"deep_pullback_recovery_watch={int(deep_pullback_recovery_watch)} "
                    f"recovery_after_break_watch={int(recovery_after_break_watch)}",
                    "mcm_target_expectation_protocol.csv",
                )

        return result
    # --------------------------------------------------   
    def _build_exit_candidate_observe_state(self, position_intervention_state: dict, side: str, entry_price: float, close_price: float, target_expectation_state: dict = None) -> dict:

        state = dict(position_intervention_state or {})
        if not state:
            return {}

        def _val(key: str) -> float:
            try:
                return float(state.get(key, 0.0) or 0.0)
            except Exception:
                return 0.0

        min_pressure = float(getattr(Config, "MCM_EXIT_CANDIDATE_MIN_PRESSURE", 0.58) or 0.58)
        max_plan_trust = float(getattr(Config, "MCM_EXIT_CANDIDATE_MAX_PLAN_TRUST", 0.52) or 0.52)
        max_holding_stability = float(getattr(Config, "MCM_EXIT_CANDIDATE_MAX_HOLDING_STABILITY", 0.50) or 0.50)
        min_fitness = float(getattr(Config, "MCM_EXIT_CANDIDATE_MIN_FITNESS", 0.40) or 0.40)
        min_evidence = float(getattr(Config, "MCM_EXIT_CANDIDATE_MIN_EVIDENCE", 0.54) or 0.54)
        max_current_r = float(getattr(Config, "MCM_EXIT_CANDIDATE_MAX_CURRENT_R", -0.45) or -0.45)

        exit_decision_pressure = _val("exit_decision_pressure")
        plan_trust = _val("plan_trust")
        holding_stability = _val("holding_stability")
        intervention_fitness = _val("intervention_fitness")
        intervention_unfit_state = _val("intervention_unfit_state")
        exit_evidence = _val("exit_evidence")
        current_r = _val("current_r")
        sustained_exit_pressure = _val("sustained_exit_pressure")

        pressure_ok = exit_decision_pressure >= min_pressure
        trust_ok = plan_trust <= max_plan_trust
        stability_ok = holding_stability <= max_holding_stability
        fitness_ok = intervention_fitness >= min_fitness
        evidence_ok = exit_evidence >= min_evidence
        adverse_depth_ok = current_r <= max_current_r
        unfit_not_dominant = intervention_unfit_state <= 0.58

        confirmation_score = max(
            0.0,
            min(
                1.0,
                (exit_decision_pressure * 0.24)
                + ((1.0 - plan_trust) * 0.20)
                + ((1.0 - holding_stability) * 0.16)
                + (intervention_fitness * 0.18)
                + (exit_evidence * 0.14)
                + (sustained_exit_pressure * 0.08),
            ),
        )

        is_candidate = bool(
            pressure_ok
            and trust_ok
            and stability_ok
            and fitness_ok
            and evidence_ok
            and adverse_depth_ok
            and unfit_not_dominant
        )

        candidate_label = "exit_candidate_observe" if is_candidate else "no_exit_candidate"
        if not is_candidate and exit_decision_pressure >= min_pressure and not fitness_ok:
            candidate_label = "exit_pressure_unfit_observe"
        elif not is_candidate and exit_decision_pressure >= min_pressure and not adverse_depth_ok:
            candidate_label = "exit_pullback_observe"
        elif not is_candidate and plan_trust > max_plan_trust:
            candidate_label = "plan_trust_holds"

        candidate = {
            "exit_candidate": bool(is_candidate),
            "candidate_label": str(candidate_label),
            "confirmation_score": float(confirmation_score),
            "exit_decision_pressure": float(exit_decision_pressure),
            "plan_trust": float(plan_trust),
            "holding_stability": float(holding_stability),
            "intervention_fitness": float(intervention_fitness),
            "intervention_unfit_state": float(intervention_unfit_state),
            "exit_evidence": float(exit_evidence),
            "current_r": float(current_r),
            "adverse_depth_ok": bool(adverse_depth_ok),
            "sustained_exit_pressure": float(sustained_exit_pressure),
            "side": str(side or "").upper().strip(),
            "entry": float(entry_price),
            "close": float(close_price),
            **dict(target_expectation_state or {}),
        }

        if bool(getattr(Config, "MCM_EXIT_CANDIDATE_OBSERVE_DEBUG", True)) and candidate_label != "no_exit_candidate":
            dbr_debug(
                "EXIT_CANDIDATE "
                f"ts={int(getattr(self, 'current_timestamp', 0) or 0)} "
                f"label={candidate_label} candidate={int(is_candidate)} side={candidate['side']} "
                f"entry={float(entry_price):.4f} close={float(close_price):.4f} "
                f"confirmation_score={confirmation_score:.4f} "
                f"exit_decision_pressure={exit_decision_pressure:.4f} plan_trust={plan_trust:.4f} "
                f"holding_stability={holding_stability:.4f} intervention_fitness={intervention_fitness:.4f} "
                f"intervention_unfit_state={intervention_unfit_state:.4f} exit_evidence={exit_evidence:.4f} "
                f"current_r={current_r:.4f} "
                f"target_expectation_context={str((target_expectation_state or {}).get('target_expectation_context', '-'))} "
                f"tp_reachability={float((target_expectation_state or {}).get('tp_reachability', 0.0) or 0.0):.4f} "
                f"expectation_break_pressure={float((target_expectation_state or {}).get('expectation_break_pressure', 0.0) or 0.0):.4f} "
                f"expectation_hold_support={float((target_expectation_state or {}).get('expectation_hold_support', 0.0) or 0.0):.4f} "
                f"target_recovery_potential={float((target_expectation_state or {}).get('target_recovery_potential', 0.0) or 0.0):.4f} "
                f"target_recovery_momentum={float((target_expectation_state or {}).get('target_recovery_momentum', 0.0) or 0.0):.4f} "
                f"target_recovery_confirmation={float((target_expectation_state or {}).get('target_recovery_confirmation', 0.0) or 0.0):.4f} "
                f"break_to_recovery_delta={float((target_expectation_state or {}).get('break_to_recovery_delta', 0.0) or 0.0):.4f} "
                f"expectation_break_persistence={float((target_expectation_state or {}).get('expectation_break_persistence', 0.0) or 0.0):.4f} "
                f"deep_pullback_recovery_watch={int(bool((target_expectation_state or {}).get('deep_pullback_recovery_watch', False)))} "
                f"recovery_after_break_watch={int(bool((target_expectation_state or {}).get('recovery_after_break_watch', False)))}",
                "mcm_exit_candidate_observe.csv",
            )

        if is_candidate:
            mark_runtime_episode_event(
                self,
                "exit_candidate_observe",
                dict(candidate),
            )

        return candidate
    # --------------------------------------------------   
    def _resolve_matured_exit_signal(self, last: dict, exit_context: dict, fill_ratio: float, pressure_to_capacity: float, risk_value: float, bars_open: int, live_mode: bool = False):

        mode = str(getattr(Config, "MCM_MATURED_EXIT_MODE", "fixed") or "fixed").strip().lower()
        if mode not in ("observe", "active"):
            return None

        if not self.position or risk_value <= 0.0:
            return None

        side = str(self.position.get("side", "") or "").upper().strip()
        if side not in ("LONG", "SHORT"):
            return None

        try:
            close_price = float(last.get("close", 0.0) or 0.0)
        except Exception:
            close_price = 0.0
        if close_price <= 0.0:
            return None

        mfe_r = float(self.position.get("mfe", 0.0) or 0.0) / max(risk_value, 1e-9)
        mae_r = float(self.position.get("mae", 0.0) or 0.0) / max(risk_value, 1e-9)
        if side == "LONG":
            current_r = (close_price - float(self.position.get("entry", 0.0) or 0.0)) / max(risk_value, 1e-9)
        else:
            current_r = (float(self.position.get("entry", 0.0) or 0.0) - close_price) / max(risk_value, 1e-9)

        giveback_r = max(0.0, mfe_r - current_r)
        structure_quality = float((self.structure_perception_state or {}).get("structure_quality", 0.0) or 0.0)
        recovery_balance = float(getattr(self, "recovery_balance", 0.0) or 0.0)
        action_capacity = float(getattr(self, "action_capacity", 0.0) or 0.0)
        regulatory_load = float(getattr(self, "regulatory_load", 0.0) or 0.0)
        if pressure_to_capacity <= 0.0 and action_capacity > 0.0:
            pressure_to_capacity = regulatory_load / max(0.05, action_capacity)

        min_mfe = float(getattr(Config, "MCM_MATURED_EXIT_MIN_MFE_R", 1.0) or 1.0)
        min_giveback = float(getattr(Config, "MCM_MATURED_EXIT_GIVEBACK_R", 0.35) or 0.35)
        max_structure = float(getattr(Config, "MCM_MATURED_EXIT_STRUCTURE_MAX", 0.50) or 0.50)
        min_pressure = float(getattr(Config, "MCM_MATURED_EXIT_PRESSURE_MIN", 1.15) or 1.15)

        structure_loss = max(0.0, min(1.0, (max_structure - structure_quality) / 0.18))
        pressure_load = max(0.0, min(1.0, (pressure_to_capacity - min_pressure) / 0.70))
        giveback_load = max(0.0, min(1.0, (giveback_r - min_giveback) / 0.80))
        recovery_loss = max(0.0, min(1.0, (-recovery_balance - 0.20) / 0.55))
        maturity_pressure = (
            (structure_loss * 0.34)
            + (giveback_load * 0.30)
            + (pressure_load * 0.22)
            + (recovery_loss * 0.14)
        )

        if mfe_r < min_mfe or giveback_r < min_giveback or maturity_pressure < 0.46:
            return None

        signal = {
            "reason": "matured_exit",
            "mode": str(mode),
            "timestamp": int(getattr(self, "current_timestamp", 0) or 0),
            "entry": float(self.position.get("entry", 0.0) or 0.0),
            "tp": float(self.position.get("tp", 0.0) or 0.0),
            "sl": float(self.position.get("sl", 0.0) or 0.0),
            "risk": float(risk_value),
            "exit_price": float(close_price),
            "maturity_pressure": float(maturity_pressure),
            "mfe_r": float(mfe_r),
            "mae_r": float(mae_r),
            "current_r": float(current_r),
            "giveback_r": float(giveback_r),
            "structure_quality": float(structure_quality),
            "pressure_to_capacity": float(pressure_to_capacity),
            "recovery_balance": float(recovery_balance),
            "bars_open": int(bars_open),
        }
        position_intervention_state = dict((exit_context or {}).get("position_intervention_state", {}) or {})
        if position_intervention_state:
            signal["position_intervention_state"] = dict(position_intervention_state)
        exit_candidate_observe_state = dict((exit_context or {}).get("exit_candidate_observe_state", {}) or {})
        if exit_candidate_observe_state:
            signal["exit_candidate_observe_state"] = dict(exit_candidate_observe_state)

        if DEBUG:
            dbr_debug(
                "MATURED_EXIT "
                f"mode={mode} ts={int(getattr(self, 'current_timestamp', 0) or 0)} "
                f"side={side} entry={float(self.position.get('entry', 0.0) or 0.0):.4f} "
                f"tp={float(self.position.get('tp', 0.0) or 0.0):.4f} "
                f"sl={float(self.position.get('sl', 0.0) or 0.0):.4f} "
                f"risk={risk_value:.4f} exit_price={close_price:.4f} "
                f"maturity_pressure={maturity_pressure:.4f} "
                f"mfe_r={mfe_r:.4f} mae_r={mae_r:.4f} current_r={current_r:.4f} "
                f"giveback_r={giveback_r:.4f} structure_quality={structure_quality:.4f} "
                f"pressure_to_capacity={pressure_to_capacity:.4f} recovery_balance={recovery_balance:.4f} "
                f"bars_open={int(bars_open)} "
                f"position_cognitive_load={float(position_intervention_state.get('position_cognitive_load', 0.0) or 0.0):.4f} "
                f"exit_decision_pressure={float(position_intervention_state.get('exit_decision_pressure', 0.0) or 0.0):.4f} "
                f"plan_trust={float(position_intervention_state.get('plan_trust', 0.0) or 0.0):.4f} "
                f"intervention_fitness={float(position_intervention_state.get('intervention_fitness', 0.0) or 0.0):.4f} "
                f"intervention_label={str(position_intervention_state.get('intervention_label', '-') or '-')} "
                f"exit_candidate={int(bool(exit_candidate_observe_state.get('exit_candidate', False)))} "
                f"candidate_label={str(exit_candidate_observe_state.get('candidate_label', '-') or '-')}",
                "matured_exit_debug.csv",
            )

        mark_runtime_episode_event(
            self,
            "matured_exit_observe" if mode == "observe" else "matured_exit_active",
            {
                **dict(signal),
                "position": dict(self.position or {}),
                "bearing_context": dict((exit_context or {}).get("bearing_context", {}) or {}),
                "position_intervention_state": dict(position_intervention_state),
                "exit_candidate_observe_state": dict(exit_candidate_observe_state),
            },
        )

        if mode == "observe" or bool(live_mode):
            return None
        return dict(signal)

    # --------------------------------------------------   
    def _handle_active_position(self, window, last, live_mode: bool):

        if self.position is None:
            return False

        entry_price = float(self.position.get("entry", 0.0) or 0.0)
        side = str(self.position.get("side", "")).upper().strip()
        risk_value = abs(float(self.position.get("risk", 0.0) or 0.0))

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

        bars_open = 0
        entry_index = self.position.get("entry_index")
        if isinstance(entry_index, int):
            bars_open = max(0, int(self.processed) - int(entry_index))

        rr_value = 0.0
        if risk_value > 0.0:
            if side == "LONG":
                rr_value = max(
                    0.0,
                    float(self.position.get("tp", 0.0) or 0.0) - entry_price,
                ) / risk_value
            else:
                rr_value = max(
                    0.0,
                    entry_price - float(self.position.get("tp", 0.0) or 0.0),
                ) / risk_value

        fill_ratio = 0.0
        if risk_value > 0.0:
            fill_ratio = max(0.0, min(2.0, favorable / risk_value))

        try:
            close_price = float(last.get("close", 0.0) or 0.0)
        except Exception:
            close_price = 0.0
        mfe_r = float((float(self.position.get("mfe", 0.0) or 0.0) / max(risk_value, 1e-9)) if risk_value > 0.0 else 0.0)
        mae_r = float((float(self.position.get("mae", 0.0) or 0.0) / max(risk_value, 1e-9)) if risk_value > 0.0 else 0.0)

        meta_regulation_state = dict(getattr(self, "meta_regulation_state", {}) or {})
        runtime_state = dict(getattr(self, "mcm_runtime_decision_state", {}) or {})
        position_state_before, position_state_after, position_state_delta = self._capture_regulation_transition()

        pressure_to_capacity = 0.0
        if float(getattr(self, "action_capacity", 0.0) or 0.0) > 0.0:
            pressure_to_capacity = float(getattr(self, "regulatory_load", 0.0) or 0.0) / max(0.05, float(getattr(self, "action_capacity", 0.0) or 0.0))

        position_intervention_state = self._build_position_intervention_state(
            close_price=float(close_price),
            entry_price=float(entry_price),
            side=str(side),
            risk_value=float(risk_value),
            mfe_r=float(mfe_r),
            mae_r=float(mae_r),
            fill_ratio=float(fill_ratio),
            pressure_to_capacity=float(pressure_to_capacity),
            bars_open=int(bars_open),
        )
        target_expectation_state = self._build_target_expectation_state(
            position_intervention_state=dict(position_intervention_state or {}),
            side=str(side),
            entry_price=float(entry_price),
            close_price=float(close_price),
            tp_price=float(self.position.get("tp", 0.0) or 0.0),
            risk_value=float(risk_value),
            bars_open=int(bars_open),
        )
        exit_candidate_observe_state = self._build_exit_candidate_observe_state(
            dict(position_intervention_state or {}),
            side=str(side),
            entry_price=float(entry_price),
            close_price=float(close_price),
            target_expectation_state=dict(target_expectation_state or {}),
        )
        exit_candidate_replay_state = dict(self.position.get("exit_candidate_replay_state", {}) or {})

        position_context = dict(self.position.get("meta", {}) or {})
        exit_bearing_context = {
            **dict((position_context.get("bearing_context", {}) or {})),
            "structure_quality": float((self.structure_perception_state or {}).get("structure_quality", 0.0) or 0.0),
            "stress_relief_potential": float((self.structure_perception_state or {}).get("stress_relief_potential", 0.0) or 0.0),
            "context_confidence": float((self.structure_perception_state or {}).get("context_confidence", 0.0) or 0.0),
            "pressure_to_capacity": float(pressure_to_capacity),
            "regulatory_load": float(getattr(self, "regulatory_load", 0.0) or 0.0),
            "action_capacity": float(getattr(self, "action_capacity", 0.0) or 0.0),
            "recovery_need": float(getattr(self, "recovery_need", 0.0) or 0.0),
            "survival_pressure": float(getattr(self, "survival_pressure", 0.0) or 0.0),
        }
        exit_context = {
            **dict(position_context or {}),
            "bearing_context": dict(exit_bearing_context or {}),
            "structure_perception_state": dict(self.structure_perception_state or {}),
            "outer_visual_perception_state": dict(self.outer_visual_perception_state or {}),
            "position_watch_state": {
                "mfe": float(self.position.get("mfe", 0.0) or 0.0),
                "mae": float(self.position.get("mae", 0.0) or 0.0),
                "risk": float(risk_value),
                "mfe_r": float(mfe_r),
                "mae_r": float(mae_r),
                "fill_ratio": float(fill_ratio),
                "bars_open": int(bars_open),
            },
            "position_intervention_state": dict(position_intervention_state or {}),
            "target_expectation_state": dict(target_expectation_state or {}),
            "exit_candidate_observe_state": dict(exit_candidate_observe_state or {}),
            "exit_candidate_replay_state": dict(exit_candidate_replay_state or {}),
            "world_state": {
                **dict((position_context.get("world_state", {}) or {})),
                "structure_perception_state": dict(self.structure_perception_state or {}),
                "visual_market_state": dict(self.visual_market_state or {}),
                "tension_state": dict(self.tension_state or {}),
                "temporal_perception_state": dict(self.temporal_perception_state or {}),
            },
        }

        mark_runtime_episode_event(
            self,
            "position_update",
            {
                "position": dict(self.position or {}),
                "entry": float(self.position.get("entry", 0.0) or 0.0),
                "tp": float(self.position.get("tp", 0.0) or 0.0),
                "sl": float(self.position.get("sl", 0.0) or 0.0),
                "risk": float(risk_value),
                "rr": float(rr_value),
                "mfe": float(self.position.get("mfe", 0.0) or 0.0),
                "mae": float(self.position.get("mae", 0.0) or 0.0),
                "bars_open": int(bars_open),
                "fill_ratio": float(fill_ratio),
                "regulatory_load": float(getattr(self, "regulatory_load", 0.0) or 0.0),
                "action_capacity": float(getattr(self, "action_capacity", 0.0) or 0.0),
                "recovery_need": float(getattr(self, "recovery_need", 0.0) or 0.0),
                "survival_pressure": float(getattr(self, "survival_pressure", 0.0) or 0.0),
                "pressure_to_capacity": float(pressure_to_capacity),
                "regulated_courage": float(meta_regulation_state.get("regulated_courage", 0.0) or 0.0),
                "courage_gap": float(meta_regulation_state.get("courage_gap", 0.0) or 0.0),
                "decision_tendency": str(runtime_state.get("decision_tendency", "hold") or "hold"),
                "proposed_decision": str(runtime_state.get("proposed_decision", "WAIT") or "WAIT"),
                "pre_action_phase": str(meta_regulation_state.get("pre_action_phase", "hold") or "hold"),
                "dominant_tension_cause": str(meta_regulation_state.get("dominant_tension_cause", "-") or "-"),
                "bearing_context": dict((exit_context.get("bearing_context", {}) or {})),
                "felt_bearing_score": float(exit_context.get("felt_bearing_score", 0.0) or 0.0),
                "felt_profile_label": str(exit_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                "position_intervention_state": dict(position_intervention_state or {}),
                "target_expectation_state": dict(target_expectation_state or {}),
                "exit_candidate_observe_state": dict(exit_candidate_observe_state or {}),
                "exit_candidate_replay_state": dict(exit_candidate_replay_state or {}),
                "reason": "position_watch",
                "state_before": dict(position_state_before or {}),
                "state_after": dict(position_state_after or {}),
                "state_delta": dict(position_state_delta or {}),
            },
        )
        self._commit_regulation_state_snapshot(position_state_after)

        exit_signal = self.exit_engine.process(
            window,
            self.position,
            "exit_trading_debug.csv",
        )

        reason = None
        if exit_signal is not None:
            reason = exit_signal.get("reason")

        if reason is not None:
            resolved_position = dict(self.position or {})

            if live_mode and Config.AKTIV_ORDER:
                oid = self.position.get("order_id")
                cancel_cause = consume_cancelled_cause(oid)
                if oid is not None and cancel_cause is not None:
                    return self._finalize_active_position_cancel(
                        resolved_position=dict(resolved_position or {}),
                        exit_context=dict(exit_context or {}),
                        order_id=oid,
                        cancel_cause=cancel_cause,
                    )

                live_snapshot = get_active_order_snapshot()
                if isinstance(live_snapshot, dict):
                    exit_context = {
                        **dict(exit_context or {}),
                        "live_exit_confirmation": {
                            "confirmed_closed": False,
                            "reason": "exchange_position_or_order_still_active",
                            "snapshot": dict(live_snapshot or {}),
                            "local_exit_reason": str(reason or "-"),
                        },
                    }
                    dbr_debug(
                        "LIVE_EXIT_WAIT "
                        f"local_reason={str(reason or '-')} "
                        f"source={str(live_snapshot.get('source', '-') or '-')} "
                        f"id={str(live_snapshot.get('id', '-') or '-')}",
                        "live_backtest_debug.csv",
                    )
                    return True

                exit_context = {
                    **dict(exit_context or {}),
                    "live_exit_confirmation": {
                        "confirmed_closed": True,
                        "reason": "exchange_no_active_position_snapshot",
                        "local_exit_reason": str(reason or "-"),
                    },
                }

            return self._finalize_active_position_resolution(
                resolved_position=dict(resolved_position or {}),
                exit_context=dict(exit_context or {}),
                reason=reason,
                live_mode=bool(live_mode),
            )

        if bool((exit_candidate_observe_state or {}).get("exit_candidate", False)) and not self.position.get("exit_candidate_replay_state"):
            self.position["exit_candidate_replay_state"] = {
                **dict(exit_candidate_observe_state or {}),
                "candidate_timestamp": int(getattr(self, "current_timestamp", 0) or 0),
                "candidate_bars_open": int(bars_open),
                "candidate_price": float(close_price),
                "candidate_mfe_r": float(mfe_r),
                "candidate_mae_r": float(mae_r),
                "target_expectation_state": dict(target_expectation_state or {}),
            }
            exit_context["exit_candidate_replay_state"] = dict(self.position.get("exit_candidate_replay_state", {}) or {})

        matured_signal = self._resolve_matured_exit_signal(
            last=last,
            exit_context=dict(exit_context or {}),
            fill_ratio=float(fill_ratio),
            pressure_to_capacity=float(pressure_to_capacity),
            risk_value=float(risk_value),
            bars_open=int(bars_open),
            live_mode=bool(live_mode),
        )
        if matured_signal is not None:
            exit_context = {
                **dict(exit_context or {}),
                "matured_exit_state": dict(matured_signal or {}),
            }
            self.position["matured_exit_price"] = float(matured_signal.get("exit_price", 0.0) or 0.0)
            return self._finalize_active_position_resolution(
                resolved_position=dict(self.position or {}),
                exit_context=dict(exit_context or {}),
                reason="matured_exit",
                live_mode=bool(live_mode),
            )
        return True
    # --------------------------------------------------
    def _handle_pending_entry(self, window, last, live_mode: bool):

        if self.pending_entry is None or self.position is not None:
            return False

        pending_meta = dict(self.pending_entry.get("meta", {}) or {})
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

        bars_open = max(0, int(self.processed) - int(created))
        pending_risk = abs(float(entry_price) - float(sl_price))
        rr_value = 0.0
        if pending_risk > 0.0:
            if side == "LONG":
                rr_value = max(
                    0.0,
                    float(tp_price) - float(entry_price),
                ) / pending_risk
            else:
                rr_value = max(
                    0.0,
                    float(entry_price) - float(tp_price),
                ) / pending_risk

        distance_to_entry = 0.0
        if low <= entry_price <= high:
            distance_to_entry = 0.0
        elif entry_price < low:
            distance_to_entry = low - entry_price
        elif entry_price > high:
            distance_to_entry = entry_price - high

        fill_ratio = 0.0
        if pending_risk > 0.0:
            fill_ratio = max(0.0, min(2.0, 1.0 - (distance_to_entry / max(pending_risk, 1e-9))))

        meta_regulation_state = dict(getattr(self, "meta_regulation_state", {}) or {})
        runtime_state = dict(getattr(self, "mcm_runtime_decision_state", {}) or {})
        pending_state_before, pending_state_after, pending_state_delta = self._capture_regulation_transition()

        pressure_to_capacity = 0.0
        if float(getattr(self, "action_capacity", 0.0) or 0.0) > 0.0:
            pressure_to_capacity = float(getattr(self, "regulatory_load", 0.0) or 0.0) / max(0.05, float(getattr(self, "action_capacity", 0.0) or 0.0))

        mark_runtime_episode_event(
            self,
            "pending_update",
            {
                "pending_entry": dict(self.pending_entry or {}),
                "entry": float(entry_price),
                "tp": float(tp_price),
                "sl": float(sl_price),
                "risk": float(pending_risk),
                "rr": float(rr_value),
                "mfe": 0.0,
                "mae": 0.0,
                "bars_open": int(bars_open),
                "fill_ratio": float(fill_ratio),
                "regulatory_load": float(getattr(self, "regulatory_load", 0.0) or 0.0),
                "action_capacity": float(getattr(self, "action_capacity", 0.0) or 0.0),
                "recovery_need": float(getattr(self, "recovery_need", 0.0) or 0.0),
                "survival_pressure": float(getattr(self, "survival_pressure", 0.0) or 0.0),
                "pressure_to_capacity": float(pressure_to_capacity),
                "regulated_courage": float(meta_regulation_state.get("regulated_courage", 0.0) or 0.0),
                "courage_gap": float(meta_regulation_state.get("courage_gap", 0.0) or 0.0),
                "decision_tendency": str(runtime_state.get("decision_tendency", "hold") or "hold"),
                "proposed_decision": str(runtime_state.get("proposed_decision", "WAIT") or "WAIT"),
                "pre_action_phase": str(meta_regulation_state.get("pre_action_phase", "hold") or "hold"),
                "dominant_tension_cause": str(meta_regulation_state.get("dominant_tension_cause", "-") or "-"),
                "bearing_context": dict((pending_meta.get("bearing_context", {}) or {})),
                "felt_bearing_score": float(pending_meta.get("felt_bearing_score", 0.0) or 0.0),
                "felt_profile_label": str(pending_meta.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                "reason": "pending_watch",
                "state_before": dict(pending_state_before or {}),
                "state_after": dict(pending_state_after or {}),
                "state_delta": dict(pending_state_delta or {}),
            },
        )
        self._commit_regulation_state_snapshot(pending_state_after)

        pending_order_id = self.pending_entry.get("order_id")

        if live_mode and pending_order_id is not None:
            cancel_cause = consume_cancelled_cause(pending_order_id)
            if cancel_cause is not None:
                cancel_snapshot = dict(self.pending_entry or {})
                cancel_state_before = self._build_regulation_state_snapshot()
                apply_outcome_stimulus(self, "cancel", self.pending_entry)
                cancel_state_after = self._build_regulation_state_snapshot()
                cancel_state_delta = self._build_regulation_state_delta(
                    cancel_state_before,
                    cancel_state_after,
                )
                self.stats.on_attempt(
                    status="cancelled",
                    context=pending_meta,
                )
                mark_runtime_episode_event(
                    self,
                    "cancelled",
                    {
                        "pending_entry": dict(cancel_snapshot or {}),
                        "reason": str(cancel_cause or "exchange_cancel"),
                        "bearing_context": dict((pending_meta.get("bearing_context", {}) or {})),
                        "felt_bearing_score": float(pending_meta.get("felt_bearing_score", 0.0) or 0.0),
                        "felt_profile_label": str(pending_meta.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                        "state_before": dict(cancel_state_before or {}),
                        "state_after": dict(cancel_state_after or {}),
                        "state_delta": dict(cancel_state_delta or {}),
                    },
                )
                self.stats.on_cancel(
                    order_id=pending_order_id,
                    cause=str(cancel_cause or "exchange_cancel"),
                    exploration_trade=False,
                    outcome_decomposition=dict(getattr(self, "last_outcome_decomposition", {}) or {}),
                    context=pending_meta,
                )
                self._sync_last_outcome_decomposition_from_stats()
                self._mark_memory_state_dirty()
                self._commit_regulation_state_snapshot(cancel_state_after)
                self.pending_entry = None
                return True

            live_snapshot = get_active_order_snapshot()
            live_source = ""

            if isinstance(live_snapshot, dict):
                live_source = str(live_snapshot.get("source", "") or "").strip().lower()

            if live_source == "position_context":
                live_entry_price = float(live_snapshot.get("entry", entry_price) or entry_price)
                live_tp_price = float(live_snapshot.get("tp", tp_price) or tp_price)
                live_sl_price = float(live_snapshot.get("sl", sl_price) or sl_price)
                live_entry_ts = live_snapshot.get("entry_ts")

                if live_entry_ts is None:
                    live_entry_ts = last.get("timestamp")

                live_position_meta = dict(pending_meta or {})
                live_position_meta["live_handoff"] = {
                    "source": str(live_source or "position_context"),
                    "order_id": self.pending_entry.get("order_id"),
                    "pending_order_id": self.pending_entry.get("order_id"),
                    "snapshot_id": live_snapshot.get("id"),
                    "pending_side": str(side),
                    "snapshot_side": str(live_snapshot.get("side", side) or side),
                    "entry": float(live_entry_price),
                    "tp": float(live_tp_price),
                    "sl": float(live_sl_price),
                    "entry_ts": live_entry_ts,
                }
                live_position_meta["execution_source"] = "live_position_context"

                return self._finalize_pending_fill_handoff(
                    side=str(live_snapshot.get("side", side) or side),
                    entry_price=float(live_entry_price),
                    tp_price=float(live_tp_price),
                    sl_price=float(live_sl_price),
                    entry_ts=live_entry_ts,
                    order_id=self.pending_entry.get("order_id"),
                    position_meta=dict(live_position_meta or {}),
                    reason="live_fill_handoff",
                )

            if (self.processed - created) > max_wait:
                timeout_snapshot = dict(self.pending_entry or {})
                cancel_sent = cancel_order_by_id(pending_order_id, cause="pending_timeout")

                if not cancel_sent:
                    return True

                consume_cancelled_cause(pending_order_id)

                timeout_state_before = self._build_regulation_state_snapshot()
                apply_outcome_stimulus(self, "timeout", self.pending_entry)
                timeout_state_after = self._build_regulation_state_snapshot()
                timeout_state_delta = self._build_regulation_state_delta(
                    timeout_state_before,
                    timeout_state_after,
                )
                self.stats.on_attempt(
                    status="timeout",
                    context=pending_meta,
                )
                mark_runtime_episode_event(
                    self,
                    "timeout",
                    {
                        "pending_entry": dict(timeout_snapshot or {}),
                        "reason": "live_timeout",
                        "bearing_context": dict((pending_meta.get("bearing_context", {}) or {})),
                        "felt_bearing_score": float(pending_meta.get("felt_bearing_score", 0.0) or 0.0),
                        "felt_profile_label": str(pending_meta.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                        "state_before": dict(timeout_state_before or {}),
                        "state_after": dict(timeout_state_after or {}),
                        "state_delta": dict(timeout_state_delta or {}),
                    },
                )
                self.stats.on_cancel(
                    order_id=pending_order_id,
                    cause="pending_timeout",
                    exploration_trade=False,
                    outcome_decomposition=dict(getattr(self, "last_outcome_decomposition", {}) or {}),
                    context=pending_meta,
                )
                self._sync_last_outcome_decomposition_from_stats()
                self._mark_memory_state_dirty()
                self._commit_regulation_state_snapshot(timeout_state_after)
                self.pending_entry = None
                return True

            return True

        fill_price = float(entry_price)

        if (not entry_touched) and validity_touched:
            fill_price = float(min(max(entry_price, low), high))

        if side in ("LONG", "SHORT") and (entry_touched or validity_touched):
            return self._finalize_pending_fill_handoff(
                side=str(side),
                entry_price=float(fill_price),
                tp_price=float(tp_price),
                sl_price=float(sl_price),
                entry_ts=last.get("timestamp"),
                order_id=None,
                position_meta=dict(pending_meta or {}),
                reason="backtest_fill",
            )

        if (self.processed - created) > max_wait:

            pending_snapshot = dict(self.pending_entry or {})
            timeout_state_before = self._build_regulation_state_snapshot()
            apply_outcome_stimulus(self, "timeout", self.pending_entry)
            timeout_state_after = self._build_regulation_state_snapshot()
            timeout_state_delta = self._build_regulation_state_delta(
                timeout_state_before,
                timeout_state_after,
            )
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
                    "bearing_context": dict((pending_meta.get("bearing_context", {}) or {})),
                    "felt_bearing_score": float(pending_meta.get("felt_bearing_score", 0.0) or 0.0),
                    "felt_profile_label": str(pending_meta.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                    "state_before": dict(timeout_state_before or {}),
                    "state_after": dict(timeout_state_after or {}),
                    "state_delta": dict(timeout_state_delta or {}),
                },
            )
            self.stats.on_cancel(
                order_id=None,
                cause="backtest_timeout",
                exploration_trade=False,
                outcome_decomposition=dict(getattr(self, "last_outcome_decomposition", {}) or {}),
                context=pending_meta,
            )
            self._sync_last_outcome_decomposition_from_stats()

            self._mark_memory_state_dirty()
            self._commit_regulation_state_snapshot(timeout_state_after)
            self.pending_entry = None
            return True

        return True
    # --------------------------------------------------
    def _finalize_entry_attempt_abandoned(self, entry_result: dict, reason: str, state_before, state_after, state_delta):

        abandoned_context = self._build_entry_attempt_context(
            entry_result,
            state_before=state_before,
            state_after=state_after,
            state_delta=state_delta,
        )
        self.stats.on_attempt(
            status="skipped",
            context=abandoned_context,
        )
        mark_runtime_episode_event(
            self,
            "abandoned",
            {
                "trade_plan": dict((abandoned_context.get("trade_plan", {}) or {})),
                "reason": str(reason or "entry_abandoned"),
                "bearing_context": dict((abandoned_context.get("bearing_context", {}) or {})),
                "felt_bearing_score": float(abandoned_context.get("felt_bearing_score", 0.0) or 0.0),
                "felt_profile_label": str(abandoned_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                "state_before": dict((abandoned_context.get("state_before", {}) or {})),
                "state_after": dict((abandoned_context.get("state_after", {}) or {})),
                "state_delta": dict((abandoned_context.get("state_delta", {}) or {})),
            },
        )
        self._commit_regulation_state_snapshot(state_after)
        return True    
    # --------------------------------------------------
    def _finalize_entry_attempt_submission(self, entry_result: dict, side, entry_price, tp_price, sl_price, risk, order_id, state_before, state_after, state_delta):

        attempt_meta = self._build_entry_attempt_context(
            entry_result,
            state_before=state_before,
            state_after=state_after,
            state_delta=state_delta,
        )

        self.execution_state = {
            **dict(self.execution_state or {}),
            "execution_phase": "pending_submitted",
            "execution_ready": True,
            "execution_blocked": False,
        }

        self.pending_entry = {
            "side": side,
            "entry": entry_price,
            "tp": tp_price,
            "sl": sl_price,
            "risk": float(risk),
            "order_id": order_id,
            "created_index": self.processed,
            "max_wait_bars": int(getattr(Config, "PENDING_ENTRY_MAX_WAIT_BARS", 20) or 20),
            "meta": {
                **dict(attempt_meta or {}),
                "felt_bearing_score": float(entry_result.get("felt_bearing_score", 0.0) or 0.0),
                "felt_profile_label": str(entry_result.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                "episode_felt_summary": dict(entry_result.get("episode_felt_summary", {}) or {}),
                "bearing_context": dict((attempt_meta.get("bearing_context", {}) or {})),
            },
        }
        self.stats.on_attempt(
            status="submitted",
            context=dict(self.pending_entry.get("meta", {}) or {}),
        )
        mark_runtime_episode_event(
            self,
            "submitted",
            {
                "trade_plan": dict((attempt_meta.get("trade_plan", {}) or {})),
                "reason": str(side or "-").lower(),
                "bearing_context": dict((attempt_meta.get("bearing_context", {}) or {})),
                "felt_bearing_score": float(attempt_meta.get("felt_bearing_score", 0.0) or 0.0),
                "felt_profile_label": str(attempt_meta.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            },
        )

        self._mark_memory_state_dirty()
        self._commit_regulation_state_snapshot(state_after)
        return True    
    # --------------------------------------------------
    def _handle_entry_attempt(self, window, candle_state, last, live_mode: bool, external_order_active: bool):

        if self.position is not None or self.pending_entry is not None:
            return False

        if external_order_active:
            skip_state_before, skip_state_after, skip_state_delta = self._capture_regulation_transition()
            return self._finalize_entry_attempt_abandoned(
                {
                    "decision_tendency": "hold",
                    "proposed_decision": "WAIT",
                    "rejection_reason": "external_order_active",
                },
                reason="external_order_active",
                state_before=skip_state_before,
                state_after=skip_state_after,
                state_delta=skip_state_delta,
            )

        if int(getattr(self, "mcm_pause_left", 0) or 0) > 0:
            self.mcm_pause_left -= 1

        entry_result = evaluate_entry_decision(
            self,
            window,
            candle_state,
        )

        if entry_result is None:
            skip_state_before, skip_state_after, skip_state_delta = self._capture_regulation_transition()
            return self._finalize_entry_attempt_abandoned(
                {
                    "decision_tendency": "hold",
                    "proposed_decision": "WAIT",
                    "rejection_reason": "entry_result_missing",
                },
                reason="entry_result_missing",
                state_before=skip_state_before,
                state_after=skip_state_after,
                state_delta=skip_state_delta,
            )

        entry_world_state = dict(entry_result.get("world_state", {}) or {})
        entry_world_state["candle_state"] = dict(candle_state or {})
        try:
            entry_world_state["current_price"] = float(candle_state.get("close", last.get("close", 0.0)) or 0.0)
        except Exception:
            entry_world_state["current_price"] = 0.0
        entry_result["world_state"] = dict(entry_world_state)

        self.action_intent_state = dict(entry_result.get("action_intent_state", {}) or {})
        self.execution_state = dict(entry_result.get("execution_state", {}) or {})

        if self._handle_decision_tendency(entry_result):
            return True

        self.execution_state = {
            **dict(self.execution_state or {}),
            "execution_phase": "value_check",
            "execution_ready": True,
            "execution_blocked": False,
        }

        value_check = self.value_gate.evaluate(entry_result)

        if DEBUG:
            dbr_debug(f"VALUE_GATE: {value_check}", "value_check_debug.csv")

        if not value_check.get("trade_allowed", False):
            self.execution_state = {
                **dict(self.execution_state or {}),
                "execution_phase": "blocked_value_gate",
                "execution_ready": False,
                "execution_blocked": True,
            }
            blocked_state_before = self._build_regulation_state_snapshot()
            apply_outcome_stimulus(
                self,
                value_check.get("reason"),
                entry_result,
            )
            blocked_state_after = self._build_regulation_state_snapshot()
            blocked_state_delta = self._build_regulation_state_delta(
                blocked_state_before,
                blocked_state_after,
            )
            blocked_context = self._build_entry_attempt_context(
                entry_result,
                state_before=blocked_state_before,
                state_after=blocked_state_after,
                state_delta=blocked_state_delta,
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
                    "bearing_context": dict((blocked_context.get("bearing_context", {}) or {})),
                    "felt_bearing_score": float(blocked_context.get("felt_bearing_score", 0.0) or 0.0),
                    "felt_profile_label": str(blocked_context.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                    "state_before": dict(blocked_state_before or {}),
                    "state_after": dict(blocked_state_after or {}),
                    "state_delta": dict(blocked_state_delta or {}),
                },
            )
            self._mark_memory_state_dirty()
            self._commit_regulation_state_snapshot(blocked_state_after)
            return True

        side = str(entry_result.get("decision", "")).upper().strip()
        entry_price = float(entry_result.get("entry_price", 0.0) or 0.0)
        tp_price = float(entry_result.get("tp_price", 0.0) or 0.0)
        sl_price = float(entry_result.get("sl_price", 0.0) or 0.0)
        risk = abs(entry_price - sl_price)

        if side not in ("LONG", "SHORT"):
            invalid_state_before, invalid_state_after, invalid_state_delta = self._capture_regulation_transition()
            return self._finalize_entry_attempt_abandoned(
                {
                    **dict(entry_result or {}),
                    "rejection_reason": "invalid_trade_direction",
                },
                reason="invalid_trade_direction",
                state_before=invalid_state_before,
                state_after=invalid_state_after,
                state_delta=invalid_state_delta,
            )

        if entry_price <= 0.0 or tp_price <= 0.0 or sl_price <= 0.0 or risk <= 0.0:
            invalid_state_before, invalid_state_after, invalid_state_delta = self._capture_regulation_transition()
            return self._finalize_entry_attempt_abandoned(
                {
                    **dict(entry_result or {}),
                    "rejection_reason": "invalid_trade_geometry",
                },
                reason="invalid_trade_geometry",
                state_before=invalid_state_before,
                state_after=invalid_state_after,
                state_delta=invalid_state_delta,
            )

        order_side = "sell" if side == "SHORT" else "buy"

        order_id = None
        is_memory_trade = False
        rr_exec_min = float(getattr(Config, "RR_EXECUTION_MIN", 1.2) or 1.2)

        self.execution_state = {
            **dict(self.execution_state or {}),
            "execution_phase": "execution_prepare",
            "execution_ready": True,
            "execution_blocked": False,
        }

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
                failed_state_before, failed_state_after, failed_state_delta = self._capture_regulation_transition()
                return self._finalize_entry_attempt_abandoned(
                    {
                        **dict(entry_result or {}),
                        "rejection_reason": "order_submit_failed",
                    },
                    reason="order_submit_failed",
                    state_before=failed_state_before,
                    state_after=failed_state_after,
                    state_delta=failed_state_delta,
                )

        submitted_state_before, submitted_state_after, submitted_state_delta = self._capture_regulation_transition()
        return self._finalize_entry_attempt_submission(
            entry_result=dict(entry_result or {}),
            side=side,
            entry_price=entry_price,
            tp_price=tp_price,
            sl_price=sl_price,
            risk=float(risk),
            order_id=order_id,
            state_before=submitted_state_before,
            state_after=submitted_state_after,
            state_delta=submitted_state_delta,
        )
    # --------------------------------------------------    
    def _build_entry_attempt_context(self, entry_result: dict, state_before: dict | None = None, state_after: dict | None = None, state_delta: dict | None = None) -> dict:

        result = dict(entry_result or {})
        action_capacity = float(result.get("action_capacity", 0.0) or 0.0)
        pressure_to_capacity = 0.0

        regulation_snapshot = dict(state_after or {}) if state_after is not None else (self._build_regulation_state_snapshot() if self is not None else {
            "tension": {
                "energy": 0.0,
                "coherence": 0.0,
                "stability": 0.0,
                "momentum": 0.0,
                "perceived_pressure": 0.0,
                "volume_pressure": 0.0,
            },
            "field": {
                "regulatory_load": 0.0,
                "action_capacity": 0.0,
                "recovery_need": 0.0,
                "survival_pressure": 0.0,
                "pressure_to_capacity": 0.0,
                "capacity_reserve": 0.0,
                "recovery_balance": 0.0,
            },
            "experience": {
                "approach_pressure": 0.0,
                "pressure_release": 0.0,
                "experience_regulation": 0.0,
                "reflection_maturity": 0.0,
                "load_bearing_capacity": 0.0,
                "protective_width_regulation": 0.0,
                "protective_courage": 0.0,
                "carrying_balance": 0.0,
                "bearing_pressure_gap": 0.0,
            },
        })

        if state_before is not None:
            previous_snapshot = dict(state_before or {})
        else:
            previous_snapshot = dict(getattr(self, "_last_regulation_state_snapshot", {}) or {})

        if not previous_snapshot:
            previous_snapshot = dict(regulation_snapshot or {})

        state_before = dict(previous_snapshot or {})
        state_after = dict(regulation_snapshot or {})

        if state_delta is None:
            state_delta = self._build_regulation_state_delta(
                state_before,
                state_after,
            )
        else:
            state_delta = dict(state_delta or {})

        if action_capacity > 0.0:
            pressure_to_capacity = float(result.get("regulatory_load", 0.0) or 0.0) / max(0.05, action_capacity)

        structure_perception_state = dict(result.get("structure_perception_state", {}) or {})

        field_state = {
            "field_density": float(result.get("field_density", 0.0) or 0.0),
            "field_stability": float(result.get("field_stability", 0.0) or 0.0),
            "regulatory_load": float(result.get("regulatory_load", 0.0) or 0.0),
            "action_capacity": float(action_capacity),
            "recovery_need": float(result.get("recovery_need", 0.0) or 0.0),
            "survival_pressure": float(result.get("survival_pressure", 0.0) or 0.0),
            "pressure_to_capacity": float(pressure_to_capacity),
            "capacity_reserve": float((regulation_snapshot.get("field", {}) or {}).get("capacity_reserve", 0.0) or 0.0),
            "recovery_balance": float((regulation_snapshot.get("field", {}) or {}).get("recovery_balance", 0.0) or 0.0),
        }

        experience_state = {
            "entry_expectation": float(getattr(self, "entry_expectation", 0.0) or 0.0) if self is not None else 0.0,
            "target_expectation": float(getattr(self, "target_expectation", 0.0) or 0.0) if self is not None else 0.0,
            "approach_pressure": float(getattr(self, "approach_pressure", 0.0) or 0.0) if self is not None else 0.0,
            "pressure_release": float(getattr(self, "pressure_release", 0.0) or 0.0) if self is not None else 0.0,
            "experience_regulation": float(getattr(self, "experience_regulation", 0.0) or 0.0) if self is not None else 0.0,
            "reflection_maturity": float(getattr(self, "reflection_maturity", 0.0) or 0.0) if self is not None else 0.0,
            "load_bearing_capacity": float(getattr(self, "load_bearing_capacity", 0.0) or 0.0) if self is not None else 0.0,
            "protective_width_regulation": float(getattr(self, "protective_width_regulation", 0.0) or 0.0) if self is not None else 0.0,
            "protective_courage": float(getattr(self, "protective_courage", 0.0) or 0.0) if self is not None else 0.0,
            "carrying_balance": float((regulation_snapshot.get("experience", {}) or {}).get("carrying_balance", 0.0) or 0.0),
            "bearing_pressure_gap": float((regulation_snapshot.get("experience", {}) or {}).get("bearing_pressure_gap", 0.0) or 0.0),
        }

        return {
            "state": {
                "energy": float(result.get("energy", 0.0) or 0.0),
                "coherence": float(result.get("coherence", 0.0) or 0.0),
                "asymmetry": int(result.get("asymmetry", 0) or 0),
                "coh_zone": float(result.get("coh_zone", 0.0) or 0.0),
                "self_state": str(result.get("self_state", "stable") or "stable"),
                "attractor": str(result.get("attractor", "neutral") or "neutral"),
            },
            "focus": {
                "focus_point": float(getattr(self, "focus_point", 0.0) or 0.0) if self is not None else 0.0,
                "focus_confidence": float(result.get("focus", {}).get("focus_confidence", getattr(self, "focus_confidence", 0.0) if self is not None else 0.0) or 0.0),
                "target_lock": float(getattr(self, "target_lock", 0.0) or 0.0) if self is not None else 0.0,
                "target_drift": float(getattr(self, "target_drift", 0.0) or 0.0) if self is not None else 0.0,
            },
            "experience": dict(experience_state or {}),
            "field_state": dict(field_state or {}),
            "bearing_context": {
                "felt_bearing_score": float(result.get("felt_bearing_score", 0.0) or 0.0),
                "felt_profile_label": str(result.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
                "structure_quality": float(structure_perception_state.get("structure_quality", 0.0) or 0.0),
                "stress_relief_potential": float(structure_perception_state.get("stress_relief_potential", 0.0) or 0.0),
                "context_confidence": float(structure_perception_state.get("context_confidence", 0.0) or 0.0),
                "pressure_to_capacity": float(field_state.get("pressure_to_capacity", 0.0) or 0.0),
                "regulatory_load": float(field_state.get("regulatory_load", 0.0) or 0.0),
                "action_capacity": float(field_state.get("action_capacity", 0.0) or 0.0),
                "recovery_need": float(field_state.get("recovery_need", 0.0) or 0.0),
                "survival_pressure": float(field_state.get("survival_pressure", 0.0) or 0.0),
                "pressure_release": float(experience_state.get("pressure_release", 0.0) or 0.0),
                "experience_regulation": float(experience_state.get("experience_regulation", 0.0) or 0.0),
                "reflection_maturity": float(experience_state.get("reflection_maturity", 0.0) or 0.0),
                "load_bearing_capacity": float(experience_state.get("load_bearing_capacity", 0.0) or 0.0),
                "protective_width_regulation": float(experience_state.get("protective_width_regulation", 0.0) or 0.0),
                "protective_courage": float(experience_state.get("protective_courage", 0.0) or 0.0),
                "capacity_reserve": float(field_state.get("capacity_reserve", 0.0) or 0.0),
                "recovery_balance": float(field_state.get("recovery_balance", 0.0) or 0.0),
                "carrying_balance": float(experience_state.get("carrying_balance", 0.0) or 0.0),
                "bearing_pressure_gap": float(experience_state.get("bearing_pressure_gap", 0.0) or 0.0),
                "state_stability": float((regulation_snapshot.get("tension", {}) or {}).get("stability", 0.0) or 0.0),
            },
            "regulation_snapshot": dict(regulation_snapshot or {}),
            "state_before": dict(state_before or {}),
            "state_after": dict(state_after or {}),
            "state_delta": dict(state_delta or {}),
            "vision": dict(result.get("vision", {}) or {}),
            "filtered_vision": dict(result.get("filtered_vision", {}) or {}),
            "world_state": dict(result.get("world_state", {}) or {}),
            "structure_perception_state": dict(structure_perception_state or {}),
            "outer_visual_perception_state": dict(result.get("outer_visual_perception_state", {}) or {}),
            "inner_field_perception_state": dict(result.get("inner_field_perception_state", {}) or {}),
            "perception_state": dict(result.get("perception_state", {}) or {}),
            "processing_state": dict(result.get("processing_state", {}) or {}),
            "felt_state": dict(result.get("felt_state", {}) or {}),
            "thought_state": dict(result.get("thought_state", {}) or {}),
            "meta_regulation_state": dict(result.get("meta_regulation_state", {}) or {}),
            "expectation_state": dict(result.get("expectation_state", {}) or {}),
            "form_symbol_state": dict(result.get("form_symbol_state", getattr(self, "form_symbol_state", {}) if self is not None else {}) or {}),
            "thought_seed_state": dict(result.get("thought_seed_state", getattr(self, "mcm_thought_seed_state", {}) if self is not None else {}) or {}),
            "state_signature": dict(result.get("state_signature", {}) or {}),
            "trade_plan": {
                "decision": str(result.get("proposed_decision", "WAIT") if str(result.get("decision", "WAIT") or "WAIT").upper().strip() == "WAIT" else result.get("decision", "WAIT")),
                "entry_price": float(result.get("entry_price", 0.0) or 0.0),
                "sl_price": float(result.get("sl_price", 0.0) or 0.0),
                "tp_price": float(result.get("tp_price", 0.0) or 0.0),
                "rr_value": float(result.get("rr_value", 0.0) or 0.0),
                "risk_model_score": float(result.get("risk_model_score", 0.0) or 0.0),
                "reward_model_score": float(result.get("reward_model_score", 0.0) or 0.0),
                "entry_mode": str(result.get("entry_mode", "impulse_contact") or "impulse_contact"),
                "impulse_entry_price": float(result.get("impulse_entry_price", result.get("entry_price", 0.0)) or 0.0),
                "strategic_entry_price": float(result.get("strategic_entry_price", result.get("entry_price", 0.0)) or 0.0),
                "strategic_entry_weight": float(result.get("strategic_entry_weight", 0.0) or 0.0),
                "strategic_entry_fit": float(result.get("strategic_entry_fit", 0.0) or 0.0),
                "area_motor_intention": float(result.get("area_motor_intention", 0.0) or 0.0),
                "area_motor_distance_fit": float(result.get("area_motor_distance_fit", 0.0) or 0.0),
                "impulse_entry_intention": float(result.get("impulse_entry_intention", 0.0) or 0.0),
                "area_entry_intention": float(result.get("area_entry_intention", 0.0) or 0.0),
                "entry_choice_conflict": float(result.get("entry_choice_conflict", 0.0) or 0.0),
                "entry_choice_bearing": float(result.get("entry_choice_bearing", 0.0) or 0.0),
                "area_direct_readiness": float(result.get("area_direct_readiness", 0.0) or 0.0),
                "area_motor_restraint": float(result.get("area_motor_restraint", 0.0) or 0.0),
                "entry_choice_state": str(result.get("entry_choice_state", "impulse_only") or "impulse_only"),
                "entry_choice_sync": str(result.get("entry_choice_sync", "-") or "-"),
                "strategic_area_focus_id": str(result.get("strategic_area_focus_id", "-") or "-"),
                "strategic_area_price_low": float(result.get("strategic_area_price_low", 0.0) or 0.0),
                "strategic_area_price_high": float(result.get("strategic_area_price_high", 0.0) or 0.0),
                "entry_validity_band": dict(result.get("entry_validity_band", {}) or {}),
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
            "felt_bearing_score": float(result.get("felt_bearing_score", 0.0) or 0.0),
            "felt_profile_label": str(result.get("felt_profile_label", "mixed_unclear") or "mixed_unclear"),
            "episode_felt_summary": dict(result.get("episode_felt_summary", {}) or {}),
        }    
    # ==================================================
    # REGULATIONSZUSTAND / ZUSTANDSÜBERGANG
    # ==================================================   
    def _build_regulation_state_snapshot(self) -> dict:

        if self is None:
            return {
                "tension": {
                    "energy": 0.0,
                    "coherence": 0.0,
                    "stability": 0.0,
                    "momentum": 0.0,
                    "perceived_pressure": 0.0,
                    "volume_pressure": 0.0,
                },
                "field": {
                    "regulatory_load": 0.0,
                    "action_capacity": 0.0,
                    "recovery_need": 0.0,
                    "survival_pressure": 0.0,
                    "pressure_to_capacity": 0.0,
                    "capacity_reserve": 0.0,
                    "recovery_balance": 0.0,
                    "field_areal_count": 0.0,
                    "field_areal_activation_mean": 0.0,
                    "field_areal_stability_mean": 0.0,
                    "field_areal_pressure_mean": 0.0,
                    "field_areal_drift": 0.0,
                    "field_areal_dominance": 0.0,
                    "field_areal_fragmentation": 0.0,
                    "field_areal_coherence_mean": 0.0,
                    "field_areal_conflict_mean": 0.0,
                },
                "experience": {
                    "approach_pressure": 0.0,
                    "pressure_release": 0.0,
                    "experience_regulation": 0.0,
                    "reflection_maturity": 0.0,
                    "load_bearing_capacity": 0.0,
                    "protective_width_regulation": 0.0,
                    "protective_courage": 0.0,
                    "carrying_balance": 0.0,
                    "bearing_pressure_gap": 0.0,
                },
            }

        tension_state = dict(getattr(self, "tension_state", {}) or {})
        inner_field_state = dict(getattr(self, "inner_field_perception_state", {}) or {})
        regulatory_load = float(getattr(self, "regulatory_load", 0.0) or 0.0)
        action_capacity = float(getattr(self, "action_capacity", 0.0) or 0.0)
        recovery_need = float(getattr(self, "recovery_need", 0.0) or 0.0)
        survival_pressure = float(getattr(self, "survival_pressure", 0.0) or 0.0)
        pressure_release = float(getattr(self, "pressure_release", 0.0) or 0.0)
        experience_regulation = float(getattr(self, "experience_regulation", 0.0) or 0.0)
        reflection_maturity = float(getattr(self, "reflection_maturity", 0.0) or 0.0)
        load_bearing_capacity = float(getattr(self, "load_bearing_capacity", 0.0) or 0.0)
        protective_width_regulation = float(getattr(self, "protective_width_regulation", 0.0) or 0.0)
        protective_courage = float(getattr(self, "protective_courage", 0.0) or 0.0)

        pressure_to_capacity = 0.0
        if action_capacity > 0.0:
            pressure_to_capacity = regulatory_load / max(0.05, action_capacity)

        capacity_reserve = float(max(0.0, action_capacity - regulatory_load))
        recovery_balance = float(max(-1.0, min(1.0, pressure_release - recovery_need)))
        carrying_balance = float(
            max(
                -1.0,
                min(
                    1.0,
                    (load_bearing_capacity + action_capacity + protective_courage)
                    - (regulatory_load + recovery_need + survival_pressure),
                ),
            )
        )
        bearing_pressure_gap = float(
            max(
                -1.0,
                min(
                    1.0,
                    (load_bearing_capacity + protective_width_regulation + protective_courage)
                    - (pressure_to_capacity + survival_pressure),
                ),
            )
        )

        return {
            "tension": {
                "energy": float(tension_state.get("energy", 0.0) or 0.0),
                "coherence": float(tension_state.get("coherence", 0.0) or 0.0),
                "stability": float(tension_state.get("stability", 0.0) or 0.0),
                "momentum": float(tension_state.get("momentum", 0.0) or 0.0),
                "perceived_pressure": float(tension_state.get("perceived_pressure", 0.0) or 0.0),
                "volume_pressure": float(tension_state.get("volume_pressure", 0.0) or 0.0),
            },
            "field": {
                "regulatory_load": float(regulatory_load),
                "action_capacity": float(action_capacity),
                "recovery_need": float(recovery_need),
                "survival_pressure": float(survival_pressure),
                "pressure_to_capacity": float(pressure_to_capacity),
                "capacity_reserve": float(capacity_reserve),
                "recovery_balance": float(recovery_balance),
                "field_areal_count": float(inner_field_state.get("field_areal_count", 0.0) or 0.0),
                "field_areal_activation_mean": float(inner_field_state.get("field_areal_activation_mean", 0.0) or 0.0),
                "field_areal_stability_mean": float(inner_field_state.get("field_areal_stability_mean", 0.0) or 0.0),
                "field_areal_pressure_mean": float(inner_field_state.get("field_areal_pressure_mean", 0.0) or 0.0),
                "field_areal_drift": float(inner_field_state.get("field_areal_drift", 0.0) or 0.0),
                "field_areal_dominance": float(inner_field_state.get("field_areal_dominance", 0.0) or 0.0),
                "field_areal_fragmentation": float(inner_field_state.get("field_areal_fragmentation", 0.0) or 0.0),
                "field_areal_coherence_mean": float(inner_field_state.get("field_areal_coherence_mean", 0.0) or 0.0),
                "field_areal_conflict_mean": float(inner_field_state.get("field_areal_conflict_mean", 0.0) or 0.0),
            },
            "experience": {
                "approach_pressure": float(getattr(self, "approach_pressure", 0.0) or 0.0),
                "pressure_release": float(pressure_release),
                "experience_regulation": float(experience_regulation),
                "reflection_maturity": float(reflection_maturity),
                "load_bearing_capacity": float(load_bearing_capacity),
                "protective_width_regulation": float(protective_width_regulation),
                "protective_courage": float(protective_courage),
                "carrying_balance": float(carrying_balance),
                "bearing_pressure_gap": float(bearing_pressure_gap),
            },
        }    
    # --------------------------------------------------    
    def _build_regulation_state_delta(self, state_before: dict, state_after: dict) -> dict:

        before = dict(state_before or {})
        after = dict(state_after or {})

        return {
            "tension": {
                "energy": float(after.get("tension", {}).get("energy", 0.0) - before.get("tension", {}).get("energy", 0.0)),
                "coherence": float(after.get("tension", {}).get("coherence", 0.0) - before.get("tension", {}).get("coherence", 0.0)),
                "stability": float(after.get("tension", {}).get("stability", 0.0) - before.get("tension", {}).get("stability", 0.0)),
                "momentum": float(after.get("tension", {}).get("momentum", 0.0) - before.get("tension", {}).get("momentum", 0.0)),
                "perceived_pressure": float(after.get("tension", {}).get("perceived_pressure", 0.0) - before.get("tension", {}).get("perceived_pressure", 0.0)),
                "volume_pressure": float(after.get("tension", {}).get("volume_pressure", 0.0) - before.get("tension", {}).get("volume_pressure", 0.0)),
            },
            "field": {
                "regulatory_load": float(after.get("field", {}).get("regulatory_load", 0.0) - before.get("field", {}).get("regulatory_load", 0.0)),
                "action_capacity": float(after.get("field", {}).get("action_capacity", 0.0) - before.get("field", {}).get("action_capacity", 0.0)),
                "recovery_need": float(after.get("field", {}).get("recovery_need", 0.0) - before.get("field", {}).get("recovery_need", 0.0)),
                "survival_pressure": float(after.get("field", {}).get("survival_pressure", 0.0) - before.get("field", {}).get("survival_pressure", 0.0)),
                "pressure_to_capacity": float(after.get("field", {}).get("pressure_to_capacity", 0.0) - before.get("field", {}).get("pressure_to_capacity", 0.0)),
                "capacity_reserve": float(after.get("field", {}).get("capacity_reserve", 0.0) - before.get("field", {}).get("capacity_reserve", 0.0)),
                "recovery_balance": float(after.get("field", {}).get("recovery_balance", 0.0) - before.get("field", {}).get("recovery_balance", 0.0)),
                "field_areal_count": float(after.get("field", {}).get("field_areal_count", 0.0) - before.get("field", {}).get("field_areal_count", 0.0)),
                "field_areal_activation_mean": float(after.get("field", {}).get("field_areal_activation_mean", 0.0) - before.get("field", {}).get("field_areal_activation_mean", 0.0)),
                "field_areal_stability_mean": float(after.get("field", {}).get("field_areal_stability_mean", 0.0) - before.get("field", {}).get("field_areal_stability_mean", 0.0)),
                "field_areal_pressure_mean": float(after.get("field", {}).get("field_areal_pressure_mean", 0.0) - before.get("field", {}).get("field_areal_pressure_mean", 0.0)),
                "field_areal_drift": float(after.get("field", {}).get("field_areal_drift", 0.0) - before.get("field", {}).get("field_areal_drift", 0.0)),
                "field_areal_dominance": float(after.get("field", {}).get("field_areal_dominance", 0.0) - before.get("field", {}).get("field_areal_dominance", 0.0)),
                "field_areal_fragmentation": float(after.get("field", {}).get("field_areal_fragmentation", 0.0) - before.get("field", {}).get("field_areal_fragmentation", 0.0)),
                "field_areal_coherence_mean": float(after.get("field", {}).get("field_areal_coherence_mean", 0.0) - before.get("field", {}).get("field_areal_coherence_mean", 0.0)),
                "field_areal_conflict_mean": float(after.get("field", {}).get("field_areal_conflict_mean", 0.0) - before.get("field", {}).get("field_areal_conflict_mean", 0.0)),
            },
            "experience": {
                "approach_pressure": float(after.get("experience", {}).get("approach_pressure", 0.0) - before.get("experience", {}).get("approach_pressure", 0.0)),
                "pressure_release": float(after.get("experience", {}).get("pressure_release", 0.0) - before.get("experience", {}).get("pressure_release", 0.0)),
                "experience_regulation": float(after.get("experience", {}).get("experience_regulation", 0.0) - before.get("experience", {}).get("experience_regulation", 0.0)),
                "reflection_maturity": float(after.get("experience", {}).get("reflection_maturity", 0.0) - before.get("experience", {}).get("reflection_maturity", 0.0)),
                "load_bearing_capacity": float(after.get("experience", {}).get("load_bearing_capacity", 0.0) - before.get("experience", {}).get("load_bearing_capacity", 0.0)),
                "protective_width_regulation": float(after.get("experience", {}).get("protective_width_regulation", 0.0) - before.get("experience", {}).get("protective_width_regulation", 0.0)),
                "protective_courage": float(after.get("experience", {}).get("protective_courage", 0.0) - before.get("experience", {}).get("protective_courage", 0.0)),
                "carrying_balance": float(after.get("experience", {}).get("carrying_balance", 0.0) - before.get("experience", {}).get("carrying_balance", 0.0)),
                "bearing_pressure_gap": float(after.get("experience", {}).get("bearing_pressure_gap", 0.0) - before.get("experience", {}).get("bearing_pressure_gap", 0.0)),
            },
        }
    # --------------------------------------------------
    def _capture_regulation_transition(self, state_before: dict | None = None, state_after: dict | None = None) -> tuple[dict, dict, dict]:

        return capture_runtime_regulation_transition(
            self,
            state_before=state_before,
            state_after=state_after,
        )
    # --------------------------------------------------    
    def _commit_regulation_state_snapshot(self, state_after: dict | None = None) -> dict:

        return commit_runtime_regulation_snapshot(
            self,
            state_after=state_after,
        )
    # ==================================================
    # SNAPSHOT / VISUALISIERUNG
    # ==================================================
    def _resolve_visualization_snapshot_write_due(self, window=None, candle_state=None):

        self._snapshot_write_seq = int(getattr(self, "_snapshot_write_seq", 0) or 0) + 1

        every_n = max(
            1,
            int(getattr(Config, "MCM_VISUAL_SNAPSHOT_WRITE_EVERY_N", 1) or 1),
        )
        min_interval = max(
            0.0,
            float(getattr(Config, "MCM_VISUAL_SNAPSHOT_MIN_INTERVAL_SECONDS", 0.0) or 0.0),
        )
        force_on_state_change = bool(getattr(Config, "MCM_VISUAL_SNAPSHOT_FORCE_ON_STATE_CHANGE", True))

        pending_state = dict(getattr(self, "pending_entry", {}) or {})
        position_state = dict(getattr(self, "position", {}) or {})

        state_key = (
            bool(position_state),
            str(position_state.get("side", "-") or "-"),
            str(position_state.get("entry_ts", position_state.get("entry", "-")) or "-"),
            bool(pending_state),
            str(pending_state.get("order_id", pending_state.get("id", "-")) or "-"),
        )

        if force_on_state_change and state_key != getattr(self, "_snapshot_last_state_key", None):
            self._snapshot_last_state_key = tuple(state_key)
            self._snapshot_last_write_ts = float(time.time())
            return True

        if every_n <= 1:
            self._snapshot_last_write_ts = float(time.time())
            return True

        if (int(self._snapshot_write_seq) % every_n) == 0:
            self._snapshot_last_write_ts = float(time.time())
            return True

        if min_interval > 0.0:
            now_ts = float(time.time())
            last_ts = float(getattr(self, "_snapshot_last_write_ts", 0.0) or 0.0)
            if (now_ts - last_ts) >= min_interval:
                self._snapshot_last_write_ts = float(now_ts)
                return True

        return False
    # --------------------------------------------------
    def _apply_restart_recovery_snapshot(bot, snapshot):

        if bot is None or not isinstance(snapshot, dict):
            return False

        snapshot_source = str(snapshot.get("source", "") or "").strip().lower()
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

        if entry is None or tp_value is None or sl_value is None:
            return False

        restart_state_before = bot._build_regulation_state_snapshot()
        risk = abs(entry - sl_value)
        restart_entry_ts = snapshot.get("entry_ts")

        if restart_entry_ts is None:
            restart_entry_ts = getattr(bot, "current_timestamp", None)

        if restart_entry_ts is None:
            restart_entry_ts = int(time.time() * 1000)

        restart_meta = {
            "felt_bearing_score": 0.0,
            "felt_profile_label": "mixed_unclear",
            "episode_felt_summary": {},
            "bearing_context": {},
            "restart_recovery": True,
            "recovery_source": str(snapshot_source or "unknown"),
            "recovery_snapshot": dict(snapshot or {}),
        }

        if snapshot_source == "open_order":
            print("RESTART RECOVERY → PENDING ORDER FOUND")

            bot.execution_state = {
                **dict(getattr(bot, "execution_state", {}) or {}),
                "execution_phase": "pending_recovered",
                "execution_ready": True,
                "execution_blocked": False,
            }
            bot.pending_entry = {
                "side": snapshot.get("side"),
                "entry": entry,
                "tp": tp_value,
                "sl": sl_value,
                "risk": risk,
                "order_id": snapshot.get("id"),
                "created_index": 0,
                "max_wait_bars": int(getattr(Config, "PENDING_ENTRY_MAX_WAIT_BARS", 20) or 20),
                "meta": dict(restart_meta or {}),
            }
            restart_state_after = bot._build_regulation_state_snapshot()
            restart_state_delta = bot._build_regulation_state_delta(
                restart_state_before,
                restart_state_after,
            )
            mark_runtime_episode_event(
                bot,
                "pending_update",
                {
                    "pending_entry": dict(bot.pending_entry or {}),
                    "reason": "restart_pending_recovery",
                    "recovery_source": str(snapshot_source or "open_order"),
                    "recovery_snapshot": dict(snapshot or {}),
                    "state_before": dict(restart_state_before or {}),
                    "state_after": dict(restart_state_after or {}),
                    "state_delta": dict(restart_state_delta or {}),
                },
            )
        else:
            print("RESTART RECOVERY → ACTIVE POSITION FOUND")

            bot.execution_state = {
                **dict(getattr(bot, "execution_state", {}) or {}),
                "execution_phase": "position_recovered",
                "execution_ready": True,
                "execution_blocked": False,
            }
            bot.position = {
                "side": snapshot.get("side"),
                "entry": entry,
                "tp": tp_value,
                "sl": sl_value,
                "mfe": 0.0,
                "mae": 0.0,
                "risk": risk,
                "order_id": snapshot.get("id"),
                "entry_ts": restart_entry_ts,
                "entry_index": None,
                "last_checked_ts": restart_entry_ts,
                "meta": dict(restart_meta or {}),
            }
            restart_state_after = bot._build_regulation_state_snapshot()
            restart_state_delta = bot._build_regulation_state_delta(
                restart_state_before,
                restart_state_after,
            )
            mark_runtime_episode_event(
                bot,
                "position_update",
                {
                    "position": dict(bot.position or {}),
                    "reason": "restart_position_recovery",
                    "recovery_source": str(snapshot_source or "position_context"),
                    "recovery_snapshot": dict(snapshot or {}),
                    "state_before": dict(restart_state_before or {}),
                    "state_after": dict(restart_state_after or {}),
                    "state_delta": dict(restart_state_delta or {}),
                },
            )

        bot._mark_memory_state_dirty()
        bot._commit_regulation_state_snapshot(restart_state_after)
        return True
    # --------------------------------------------------  
    def _build_inner_pipeline_snapshot(self):

        return build_runtime_pipeline_snapshot(self)
    # --------------------------------------------------  
    def _build_visualization_snapshot_bundle(self, window, candle_state):

        return build_visualization_snapshot_bundle(
            bot=self,
            window=window,
            candle_state=candle_state,
        )
    # --------------------------------------------------
    def _write_visualization_snapshots(self, window, candle_state):

        if not self._resolve_visualization_snapshot_write_due(
            window=window,
            candle_state=candle_state,
        ):
            return None

        snapshot_state = prepare_visualization_snapshot_state(
            bot=self,
            window=window,
            candle_state=candle_state,
        )

        snapshot_bundle = dict(snapshot_state.get("snapshot_bundle", {}) or {})
        if not snapshot_bundle:
            return None

        self._snapshot_bundle = dict(snapshot_bundle or {})
        self._snapshot_dirty = bool(snapshot_state.get("snapshot_dirty", False))
        return dict(snapshot_bundle or {})
    # --------------------------------------------------  
    def _flush_visualization_snapshots(self, force: bool = False):

        if not bool(getattr(self, "_snapshot_dirty", False)) and not bool(force):
            return None

        snapshot_bundle = dict(getattr(self, "_snapshot_bundle", {}) or {})
        if not snapshot_bundle:
            return None

        written_bundle = write_visualization_snapshot_bundle(snapshot_bundle)
        if written_bundle is None:
            return None

        self._snapshot_dirty = False
        return dict(written_bundle or {}) 
    # ==================================================
    # MEMORY STATE / PERSISTENZ
    # ==================================================   
    def _ensure_memory_state_loaded(self):

        return ensure_memory_state_loaded(
            self,
            payload=self._memory_state_payload,
        )
    # --------------------------------------------------
    def _mark_memory_state_dirty(self):

        return mark_memory_state_dirty(self)
    # --------------------------------------------------
    def _flush_memory_state_if_due(self, force: bool = False):

        return flush_memory_state_if_due(
            self,
            force=force,
        )
    # --------------------------------------------------
    def _save_memory_state(self, force: bool = False):

        if not bool(force) and not bool(getattr(self, "_memory_state_dirty", False)):
            return None

        _flush_form_symbol_memory_if_due(self, force=bool(force))
        _flush_thought_memory_if_due(self, force=bool(force))

        payload = capture_memory_state(
            self,
            include_runtime_state=bool(getattr(Config, "MCM_SAVE_RUNTIME_STATE", False)),
        )

        if payload is None:
            return None

        saved_payload = write_memory_state_payload(payload)

        if saved_payload is None:
            return None

        return finalize_memory_state_save(
            self,
            payload=saved_payload,
        )

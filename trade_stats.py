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
import time
from config import Config
from debug_reader import dbr_append_text, dbr_debug, dbr_file_write_profile, dbr_resolve_path

class TradeStats:

    @staticmethod
    def _is_live_mode():
        return str(getattr(Config, "MODE", "LIVE")).upper() == "LIVE"

    @staticmethod
    def _live_equity_sync_enabled():
        return bool(getattr(Config, "LIVE_EQUITY_SYNC_ENABLED", True))

    @staticmethod
    def _fetch_live_account_equity():
        from ph_ohlcv import create_exchange, get_account_value

        exchange = create_exchange()
        return float(get_account_value(exchange, Config.USDT))

    def _resolve_start_equity(self):
        fallback_equity = float(getattr(Config, "START_EQUITY", 0.0) or 0.0)
        if not self._is_live_mode():
            return fallback_equity

        try:
            live_equity = self._fetch_live_account_equity()
            if live_equity > 0.0:
                dbr_debug(
                    f"LIVE_EQUITY_INIT | source=phemex_futures equity={live_equity:.8f}",
                    "mcm_live_equity_sync.csv",
                )
                return float(live_equity)
            dbr_debug(
                f"LIVE_EQUITY_INIT_FALLBACK | reason=non_positive_exchange_equity exchange_equity={live_equity:.8f} fallback={fallback_equity:.8f}",
                "mcm_live_equity_sync.csv",
            )
        except Exception as exc:
            dbr_debug(
                f"LIVE_EQUITY_INIT_FALLBACK | reason=exchange_error error={type(exc).__name__}:{str(exc).replace(';', '|')} fallback={fallback_equity:.8f}",
                "mcm_live_equity_sync.csv",
            )

        return fallback_equity

    def _sync_live_account_equity(self, reason="sync"):
        if not self._is_live_mode() or not self._live_equity_sync_enabled():
            return False

        try:
            live_equity = self._fetch_live_account_equity()
            if live_equity <= 0.0:
                dbr_debug(
                    f"LIVE_EQUITY_SYNC_SKIPPED | reason=non_positive_exchange_equity exchange_equity={live_equity:.8f}",
                    "mcm_live_equity_sync.csv",
                )
                return False

            start_equity = float(self.data.get("start_equity", 0.0) or 0.0)
            local_equity = float(self.data.get("current_equity", start_equity) or start_equity)
            self.data["current_equity"] = float(live_equity)
            self.data["pnl_netto"] = float(live_equity - start_equity)
            dbr_debug(
                f"LIVE_EQUITY_SYNC | reason={str(reason or 'sync')} start_equity={start_equity:.8f} live_equity={live_equity:.8f} local_equity_before={local_equity:.8f} pnl_netto={float(self.data.get('pnl_netto', 0.0) or 0.0):.8f}",
                "mcm_live_equity_sync.csv",
            )
            return True
        except Exception as exc:
            dbr_debug(
                f"LIVE_EQUITY_SYNC_FAILED | reason={str(reason or 'sync')} error={type(exc).__name__}:{str(exc).replace(';', '|')}",
                "mcm_live_equity_sync.csv",
            )
            return False

    def __init__(
        self,
        path="debug/trade_stats.json",
        csv_path="debug/trade_equity.csv",
        attempt_path="debug/attempt_records.jsonl",
        outcome_path="debug/outcome_records.jsonl",
        reset=True,
    ):
        self.path = dbr_resolve_path(path)
        self.csv_path = dbr_resolve_path(csv_path)
        self.attempt_path = dbr_resolve_path(attempt_path)
        self.outcome_path = dbr_resolve_path(outcome_path)
        self.exit_candidate_replay_path = dbr_resolve_path("debug/mcm_exit_candidate_replay.csv")
        self._outcome_records_cache = []

        start_equity = self._resolve_start_equity()

        self.data = {
            "trades": 0,
            "tp": 0,
            "sl": 0,
            "start_equity": float(start_equity),
            "current_equity": float(start_equity),
            "pnl_netto": 0.0,
            "pnl_tp": 0.0,
            "pnl_sl": 0.0,
            "cancels": 0,
            "attempts": 0,
            "attempts_submitted": 0,
            "attempts_filled": 0,
            "attempts_cancelled": 0,
            "attempts_timeout": 0,
            "attempts_blocked": 0,
            "attempts_skipped": 0,
            "attempts_observed": 0,
            "attempts_replanned": 0,
            "attempts_withheld": 0,
            "attempts_long": 0,
            "attempts_short": 0,
            "attempts_submitted_long": 0,
            "attempts_submitted_short": 0,
            "attempts_filled_long": 0,
            "attempts_filled_short": 0,
            "attempt_structure_zone": 0,
            "attempt_non_structure_zone": 0,
            "long_trades": 0,
            "short_trades": 0,
            "long_tp": 0,
            "long_sl": 0,
            "short_tp": 0,
            "short_sl": 0,
            "long_pnl": 0.0,
            "short_pnl": 0.0,
            "current_timestamp": None,
            "last_outcome_decomposition": {},
            "recent_attempts": [],
            "pending_observations": [],
            "observation_learning": {
                "open": 0,
                "resolved": 0,
                "saved_loss": 0,
                "missed_gain": 0,
                "neutral": 0,
                "low_observations": 0,
                "zone_observations": 0,
                "maturity_trust": 0.0,
                "action_pressure": 0.0,
                "last_result": "-",
            },
            "recent_observation_learning": [],
            "exploration_trades": 0,
            "exploration_tp": 0,
            "exploration_sl": 0,
            "exploration_cancels": 0,
            "exploration_pnl": 0.0,
            "matured_exits": 0,
            "matured_exit_pnl": 0.0,
            "exit_candidate_replay_count": 0,
            "exit_candidate_replay_actual_pnl": 0.0,
            "exit_candidate_replay_hypothetical_pnl": 0.0,
            "exit_candidate_replay_delta_pnl": 0.0,
            "exit_candidate_replay_saved_loss_count": 0,
            "exit_candidate_replay_saved_giveback_count": 0,
            "exit_candidate_replay_harmed_count": 0,
            "exit_candidate_replay_tp_cut_count": 0,
            "equity_peak": float(start_equity),
            "max_drawdown_abs": 0.0,
            "max_drawdown_pct": 0.0,
            "kpi_summary": {},
        }
        self._json_save_seq = 0

        if reset:
            # JSON zurücksetzen
            self._save(force=True)

            # CSV bei Neustart überschreiben
            if os.path.exists(self.csv_path):
                try:
                    os.remove(self.csv_path)
                except Exception:
                    pass

            if os.path.exists(self.attempt_path):
                try:
                    os.remove(self.attempt_path)
                except Exception:
                    pass

            if os.path.exists(self.outcome_path):
                try:
                    os.remove(self.outcome_path)
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
                self.data.pop("attempt_records", None)
                self.data.pop("outcome_records", None)
        except Exception:
            pass
    # ─────────────────────────────────────────────
    def _normalize_record_value(self, value):
        if isinstance(value, dict):
            normalized = {}
            for key, item in value.items():
                if key is None:
                    continue
                normalized[str(key)] = self._normalize_record_value(item)
            return normalized

        if isinstance(value, list):
            return [self._normalize_record_value(item) for item in list(value or [])[:128]]

        if value is None or isinstance(value, (str, int, float, bool)):
            return value

        return str(value)

    # ─────────────────────────────────────────────
    def _append_record_file(self, path: str, record: dict):
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            resolved_path = dbr_resolve_path(path)
            if resolved_path == self.outcome_path:
                cache = list(getattr(self, "_outcome_records_cache", []) or [])
                cache.append(dict(record or {}))
                self._outcome_records_cache = cache[-2000:]
            line = json.dumps(dict(record or {}), ensure_ascii=False) + "\n"
            dbr_append_text(
                path,
                line,
                operation="trade_stats_jsonl_append",
                extra=f"event={str((record or {}).get('event', '-'))}|status={str((record or {}).get('status', '-'))}",
            )
        except Exception:
            pass

    # ─────────────────────────────────────────────
    def _read_record_file(self, path: str, limit: int | None = None) -> list[dict]:
        records = []

        try:
            resolved_path = dbr_resolve_path(path)
            cache = list(getattr(self, "_outcome_records_cache", []) or [])
            if resolved_path == self.outcome_path and cache:
                records = [dict(item or {}) for item in cache if isinstance(item, dict)]
                if limit is not None:
                    return records[-max(1, int(limit or 1)):]
                return records

            if not os.path.exists(resolved_path):
                return records

            with open(resolved_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = str(line or "").strip()
                    if not line:
                        continue

                    try:
                        item = json.loads(line)
                    except Exception:
                        continue

                    if isinstance(item, dict):
                        records.append(item)
        except Exception:
            return []

        if limit is not None:
            return records[-max(1, int(limit or 1)):]

        return records

    # ─────────────────────────────────────────────
    def _structure_band(self, structure_quality: float) -> str:
        quality = float(structure_quality or 0.0)

        if quality >= 0.70:
            return "high"

        if quality >= 0.55:
            return "mid"

        return "low"

    # ─────────────────────────────────────────────
    def _derive_open_hypothesis_learning(self, record: dict, emergent_state: str | None = None) -> dict:
        source = dict(record or {})
        state = str(emergent_state or source.get("emergent_structure_state", "") or "").strip()
        reason = str(source.get("reason", "") or "").strip().lower()

        def _f(value, default=0.0):
            try:
                if value is None:
                    return float(default)
                return float(value)
            except Exception:
                return float(default)

        def _clip(value):
            value = _f(value)
            if value != value:
                value = 0.0
            return max(0.0, min(1.0, float(value)))

        if state != "open_structural_hypothesis":
            return {
                "open_hypothesis_learning_state": "-",
                "open_hypothesis_consequence_score": 0.0,
                "open_hypothesis_burden_score": 0.0,
                "open_hypothesis_reorganization_score": 0.0,
                "open_hypothesis_replay_need": 0.0,
                "open_hypothesis_distance_need": 0.0,
                "open_hypothesis_reinterpretation_need": 0.0,
                "open_hypothesis_reorganization_posture": "-",
            }

        pnl = _f(source.get("pnl", 0.0))
        rr_value = _f(source.get("rr_value", 0.0))
        reading = _clip(source.get("emergent_structure_reading", 0.0))
        confirmation = _clip(source.get("emergent_structure_confirmation", 0.0))
        grounding = _clip(source.get("thought_seed_structural_grounding", 0.0))
        open_pressure = _clip(source.get("thought_seed_open_hypothesis_pressure", 0.0))
        lag = _clip(source.get("thought_seed_reality_lag", 0.0))
        balance = max(-1.0, min(1.0, _f(source.get("thought_seed_consequence_balance", 0.0))))

        positive = reason == "tp_hit" or pnl > 0.0
        negative = reason == "sl_hit" or pnl < 0.0
        pnl_magnitude = _clip(abs(pnl) / max(0.5, abs(pnl) + 1.0))
        consequence_score = _clip(
            (0.42 if positive else 0.0)
            + (confirmation * 0.18)
            + (grounding * 0.14)
            + (max(0.0, balance) * 0.12)
            + (_clip(rr_value / 4.0) * 0.08)
            + (pnl_magnitude * 0.06)
        )
        burden_score = _clip(
            (0.42 if negative else 0.0)
            + (open_pressure * 0.18)
            + (lag * 0.16)
            + (max(0.0, -balance) * 0.12)
            + ((1.0 - grounding) * 0.08)
            + (pnl_magnitude * 0.04)
        )
        reorganization_score = _clip(
            (open_pressure * 0.26)
            + (lag * 0.22)
            + ((1.0 - confirmation) * 0.16)
            + ((1.0 - grounding) * 0.14)
            + (reading * 0.12)
            + (burden_score * 0.10)
            - (consequence_score * 0.12)
        )
        replay_need = _clip(
            (reorganization_score * 0.38)
            + (lag * 0.24)
            + (open_pressure * 0.16)
            + ((1.0 - grounding) * 0.12)
            + ((1.0 - confirmation) * 0.10)
        )
        distance_need = _clip(
            (burden_score * 0.34)
            + (max(0.0, -balance) * 0.20)
            + (open_pressure * 0.16)
            + (lag * 0.14)
            + ((1.0 - grounding) * 0.10)
            + (0.06 if negative else 0.0)
        )
        reinterpretation_need = _clip(
            (reorganization_score * 0.34)
            + (max(0.0, burden_score - consequence_score) * 0.20)
            + ((1.0 - confirmation) * 0.16)
            + (reading * 0.12)
            + (lag * 0.10)
            + ((1.0 - grounding) * 0.08)
        )
        if max(replay_need, distance_need, reinterpretation_need) < 0.28:
            reorganization_posture = "low_reorganization_need"
        elif reinterpretation_need >= max(replay_need, distance_need):
            reorganization_posture = "reinterpretation_dominant"
        elif distance_need >= replay_need:
            reorganization_posture = "distance_dominant"
        else:
            reorganization_posture = "replay_dominant"

        if positive and consequence_score >= max(0.34, burden_score):
            learning_state = "open_hypothesis_carried"
        elif reorganization_score >= 0.46 and (burden_score - reorganization_score) < 0.18:
            learning_state = "open_hypothesis_reorganizing"
        elif negative and burden_score >= 0.42:
            learning_state = "open_hypothesis_burdened"
        elif reorganization_score >= 0.34:
            learning_state = "open_hypothesis_reorganizing"
        else:
            learning_state = "open_hypothesis_reorganizing"

        return {
            "open_hypothesis_learning_state": str(learning_state),
            "open_hypothesis_consequence_score": float(consequence_score),
            "open_hypothesis_burden_score": float(burden_score),
            "open_hypothesis_reorganization_score": float(reorganization_score),
            "open_hypothesis_replay_need": float(replay_need),
            "open_hypothesis_distance_need": float(distance_need),
            "open_hypothesis_reinterpretation_need": float(reinterpretation_need),
            "open_hypothesis_reorganization_posture": str(reorganization_posture),
        }

    # ─────────────────────────────────────────────
    def _rebuild_kpi_summary(self):
        trades = int(self.data.get("trades", 0) or 0)
        tp = int(self.data.get("tp", 0) or 0)
        sl = int(self.data.get("sl", 0) or 0)
        cancels = int(self.data.get("cancels", 0) or 0)
        attempts = int(self.data.get("attempts", 0) or 0)

        pnl_netto = float(self.data.get("pnl_netto", 0.0) or 0.0)
        pnl_tp = float(self.data.get("pnl_tp", 0.0) or 0.0)
        pnl_sl = float(self.data.get("pnl_sl", 0.0) or 0.0)

        avg_win = (pnl_tp / tp) if tp > 0 else 0.0
        avg_loss = (pnl_sl / sl) if sl > 0 else 0.0
        profit_factor = abs(pnl_tp / pnl_sl) if pnl_sl != 0 else 0.0
        expectancy = (pnl_netto / trades) if trades > 0 else 0.0
        winrate = (tp / trades) if trades > 0 else 0.0
        long_trades = int(self.data.get("long_trades", 0) or 0)
        short_trades = int(self.data.get("short_trades", 0) or 0)
        long_tp = int(self.data.get("long_tp", 0) or 0)
        long_sl = int(self.data.get("long_sl", 0) or 0)
        short_tp = int(self.data.get("short_tp", 0) or 0)
        short_sl = int(self.data.get("short_sl", 0) or 0)
        long_pnl = float(self.data.get("long_pnl", 0.0) or 0.0)
        short_pnl = float(self.data.get("short_pnl", 0.0) or 0.0)

        attempt_feedback = self.get_attempt_feedback()

        outcomes = self._read_record_file(self.outcome_path)

        band_stats = {
            "high": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0},
            "mid": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0},
            "low": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0},
        }
        emergent_structure_stats = {
            "confirmed_structural_interpretation": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "reading_sum": 0.0, "confirmation_sum": 0.0, "rr_sum": 0.0},
            "open_structural_hypothesis": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "reading_sum": 0.0, "confirmation_sum": 0.0, "rr_sum": 0.0},
            "wide_target_without_structure": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "reading_sum": 0.0, "confirmation_sum": 0.0, "rr_sum": 0.0},
            "ordinary_structure_reading": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "reading_sum": 0.0, "confirmation_sum": 0.0, "rr_sum": 0.0},
        }
        open_hypothesis_learning_stats = {
            "open_hypothesis_carried": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "consequence_sum": 0.0, "burden_sum": 0.0, "reorganization_sum": 0.0, "replay_sum": 0.0, "distance_sum": 0.0, "reinterpretation_sum": 0.0, "grounding_sum": 0.0, "pressure_sum": 0.0, "lag_sum": 0.0},
            "open_hypothesis_burdened": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "consequence_sum": 0.0, "burden_sum": 0.0, "reorganization_sum": 0.0, "replay_sum": 0.0, "distance_sum": 0.0, "reinterpretation_sum": 0.0, "grounding_sum": 0.0, "pressure_sum": 0.0, "lag_sum": 0.0},
            "open_hypothesis_reorganizing": {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "consequence_sum": 0.0, "burden_sum": 0.0, "reorganization_sum": 0.0, "replay_sum": 0.0, "distance_sum": 0.0, "reinterpretation_sum": 0.0, "grounding_sum": 0.0, "pressure_sum": 0.0, "lag_sum": 0.0},
        }
        open_hypothesis_reorganization_posture_stats = {
            "reinterpretation_dominant": {"count": 0, "pnl": 0.0},
            "distance_dominant": {"count": 0, "pnl": 0.0},
            "replay_dominant": {"count": 0, "pnl": 0.0},
            "low_reorganization_need": {"count": 0, "pnl": 0.0},
        }

        def _summary_f(*values, default=0.0):
            for value in values:
                try:
                    if value is None:
                        continue
                    return float(value)
                except Exception:
                    continue
            if default is None:
                return None
            return float(default)

        def _summary_clip(value):
            value = _summary_f(value)
            if value != value:
                value = 0.0
            return max(0.0, min(1.0, float(value)))

        def _summary_section(record: dict, name: str) -> dict:
            context = dict(record.get("context", {}) or {})
            value = record.get(name, context.get(name, {}))
            return dict(value or {}) if isinstance(value, dict) else {}

        def _derive_emergent_structure(record: dict) -> dict:
            plan = _summary_section(record, "trade_plan")
            meta = _summary_section(record, "meta_regulation_state")
            contact = _summary_section(record, "active_mcm_contact_state")
            target = _summary_section(record, "target_expectation_state")
            decomposition = dict(record.get("outcome_decomposition", {}) or {})
            if not contact:
                contact = dict(meta.get("active_mcm_contact", {}) or {})

            rr_value = _summary_f(record.get("rr_value"), plan.get("rr_value"), default=0.0)
            structural_run_room = _summary_f(record.get("structural_run_room"), _summary_clip((rr_value - 1.6) / 3.2))
            target_expectation_value = _summary_f(
                record.get("target_expectation_value"),
                target.get(
                    "tp_reachability",
                    target.get(
                        "base_target_expectation",
                        (_summary_section(record, "experience") or {}).get("target_expectation", 0.0),
                    ),
                ),
            )
            reading = _summary_f(record.get("emergent_structure_reading"), default=None)
            if reading is None:
                reading = _summary_clip(
                    (_summary_clip(structural_run_room) * 0.24)
                    + (_summary_clip(meta.get("future_projection_depth", record.get("future_projection_depth", 0.0))) * 0.16)
                    + (_summary_clip(meta.get("mcm_spacetime_depth", record.get("mcm_spacetime_depth", 0.0))) * 0.14)
                    + (_summary_clip(meta.get("area_bearing_quality", record.get("area_bearing_quality", 0.0))) * 0.14)
                    + (_summary_clip(plan.get("entry_choice_bearing", record.get("entry_choice_bearing", 0.0))) * 0.12)
                    + (_summary_clip(contact.get("contact_action_maturity", meta.get("contact_action_maturity", 0.0))) * 0.10)
                    + (_summary_clip(target_expectation_value) * 0.10)
                    - (_summary_clip(meta.get("spacetime_unlocated_pressure", record.get("spacetime_unlocated_pressure", 0.0))) * 0.10)
                    - (_summary_clip(meta.get("contact_regime_mismatch", record.get("contact_regime_mismatch", 0.0))) * 0.08)
                )
            confirmation = _summary_f(record.get("emergent_structure_confirmation"), default=None)
            reason = str(record.get("reason", "") or "").strip().lower()
            if confirmation is None:
                confirmation = _summary_clip(
                    (_summary_clip(reading) * 0.42)
                    + (_summary_clip(decomposition.get("plan_quality", 0.0)) * 0.16)
                    + (_summary_clip(decomposition.get("execution_quality", 0.0)) * 0.14)
                    + (_summary_clip(decomposition.get("risk_fit_quality", 0.0)) * 0.12)
                    + (_summary_clip(decomposition.get("position_constructive_bearing", 0.0)) * 0.10)
                    + (0.12 if reason == "tp_hit" and rr_value >= 2.4 else 0.0)
                    - (0.10 if reason == "sl_hit" and rr_value >= 2.4 else 0.0)
                )
            state = str(record.get("emergent_structure_state", "") or "").strip()
            if not state:
                if reading >= 0.52 and confirmation >= 0.50:
                    state = "confirmed_structural_interpretation"
                elif reading >= 0.44 and rr_value >= 2.4:
                    state = "open_structural_hypothesis"
                elif rr_value >= 2.4 and reading < 0.34:
                    state = "wide_target_without_structure"
                else:
                    state = "ordinary_structure_reading"
            return {
                "state": state,
                "rr_value": float(rr_value),
                "structural_run_room": float(structural_run_room),
                "target_expectation_value": float(target_expectation_value),
                "reading": float(reading),
                "confirmation": float(confirmation),
            }

        for item in outcomes:
            record = dict(item or {})
            band = self._structure_band(record.get("structure_quality", 0.0))
            reason = str(record.get("reason", "") or "").strip().lower()
            emergent = _derive_emergent_structure(record)
            emergent_state = str(emergent.get("state", "ordinary_structure_reading") or "ordinary_structure_reading")
            if emergent_state not in emergent_structure_stats:
                emergent_structure_stats[emergent_state] = {"count": 0, "tp": 0, "sl": 0, "cancel": 0, "pnl": 0.0, "reading_sum": 0.0, "confirmation_sum": 0.0, "rr_sum": 0.0}

            band_stats[band]["count"] += 1
            band_stats[band]["pnl"] += float(record.get("pnl", 0.0) or 0.0)
            emergent_structure_stats[emergent_state]["count"] += 1
            emergent_structure_stats[emergent_state]["pnl"] += float(record.get("pnl", 0.0) or 0.0)
            emergent_structure_stats[emergent_state]["reading_sum"] += float(emergent.get("reading", 0.0) or 0.0)
            emergent_structure_stats[emergent_state]["confirmation_sum"] += float(emergent.get("confirmation", 0.0) or 0.0)
            emergent_structure_stats[emergent_state]["rr_sum"] += float(emergent.get("rr_value", 0.0) or 0.0)
            open_learning = self._derive_open_hypothesis_learning(record, emergent_state=emergent_state)
            open_learning_state = str(open_learning.get("open_hypothesis_learning_state", "-") or "-")
            if open_learning_state in open_hypothesis_learning_stats:
                open_hypothesis_learning_stats[open_learning_state]["count"] += 1
                open_hypothesis_learning_stats[open_learning_state]["pnl"] += float(record.get("pnl", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["consequence_sum"] += float(open_learning.get("open_hypothesis_consequence_score", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["burden_sum"] += float(open_learning.get("open_hypothesis_burden_score", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["reorganization_sum"] += float(open_learning.get("open_hypothesis_reorganization_score", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["replay_sum"] += float(open_learning.get("open_hypothesis_replay_need", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["distance_sum"] += float(open_learning.get("open_hypothesis_distance_need", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["reinterpretation_sum"] += float(open_learning.get("open_hypothesis_reinterpretation_need", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["grounding_sum"] += float(record.get("thought_seed_structural_grounding", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["pressure_sum"] += float(record.get("thought_seed_open_hypothesis_pressure", 0.0) or 0.0)
                open_hypothesis_learning_stats[open_learning_state]["lag_sum"] += float(record.get("thought_seed_reality_lag", 0.0) or 0.0)
                posture = str(open_learning.get("open_hypothesis_reorganization_posture", "-") or "-")
                if posture in open_hypothesis_reorganization_posture_stats:
                    open_hypothesis_reorganization_posture_stats[posture]["count"] += 1
                    open_hypothesis_reorganization_posture_stats[posture]["pnl"] += float(record.get("pnl", 0.0) or 0.0)

            if reason == "tp_hit":
                band_stats[band]["tp"] += 1
                emergent_structure_stats[emergent_state]["tp"] += 1
                if open_learning_state in open_hypothesis_learning_stats:
                    open_hypothesis_learning_stats[open_learning_state]["tp"] += 1
            elif reason == "sl_hit":
                band_stats[band]["sl"] += 1
                emergent_structure_stats[emergent_state]["sl"] += 1
                if open_learning_state in open_hypothesis_learning_stats:
                    open_hypothesis_learning_stats[open_learning_state]["sl"] += 1
            else:
                band_stats[band]["cancel"] += 1
                emergent_structure_stats[emergent_state]["cancel"] += 1
                if open_learning_state in open_hypothesis_learning_stats:
                    open_hypothesis_learning_stats[open_learning_state]["cancel"] += 1

        for band_name, payload in band_stats.items():
            count = int(payload.get("count", 0) or 0)
            tp_count = int(payload.get("tp", 0) or 0)
            payload["winrate"] = float(tp_count / count) if count > 0 else 0.0
            payload["avg_pnl"] = float(payload.get("pnl", 0.0) or 0.0) / count if count > 0 else 0.0

        for state_name, payload in emergent_structure_stats.items():
            count = int(payload.get("count", 0) or 0)
            tp_count = int(payload.get("tp", 0) or 0)
            payload["winrate"] = float(tp_count / count) if count > 0 else 0.0
            payload["avg_pnl"] = float(payload.get("pnl", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_reading"] = float(payload.get("reading_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_confirmation"] = float(payload.get("confirmation_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_rr"] = float(payload.get("rr_sum", 0.0) or 0.0) / count if count > 0 else 0.0

        for state_name, payload in open_hypothesis_learning_stats.items():
            count = int(payload.get("count", 0) or 0)
            tp_count = int(payload.get("tp", 0) or 0)
            payload["winrate"] = float(tp_count / count) if count > 0 else 0.0
            payload["avg_pnl"] = float(payload.get("pnl", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_consequence_score"] = float(payload.get("consequence_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_burden_score"] = float(payload.get("burden_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_reorganization_score"] = float(payload.get("reorganization_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_replay_need"] = float(payload.get("replay_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_distance_need"] = float(payload.get("distance_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_reinterpretation_need"] = float(payload.get("reinterpretation_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_structural_grounding"] = float(payload.get("grounding_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_open_hypothesis_pressure"] = float(payload.get("pressure_sum", 0.0) or 0.0) / count if count > 0 else 0.0
            payload["avg_reality_lag"] = float(payload.get("lag_sum", 0.0) or 0.0) / count if count > 0 else 0.0

        proof = {
            "attempt_density": float(attempt_feedback.get("attempt_density", 0.0) or 0.0),
            "context_quality": float(attempt_feedback.get("context_quality", 0.0) or 0.0),
            "overtrade_pressure": float(attempt_feedback.get("overtrade_pressure", 0.0) or 0.0),
            "observe_share": float(attempt_feedback.get("observe_share", 0.0) or 0.0),
            "replan_share": float(attempt_feedback.get("replan_share", 0.0) or 0.0),
            "withheld_share": float(attempt_feedback.get("withheld_share", 0.0) or 0.0),
            "pressure_to_capacity": float(attempt_feedback.get("pressure_to_capacity", 0.0) or 0.0),
            "regulatory_load": float(attempt_feedback.get("regulatory_load", 0.0) or 0.0),
            "action_capacity": float(attempt_feedback.get("action_capacity", 0.0) or 0.0),
            "recovery_need": float(attempt_feedback.get("recovery_need", 0.0) or 0.0),
            "survival_pressure": float(attempt_feedback.get("survival_pressure", 0.0) or 0.0),
            "pressure_release": float(attempt_feedback.get("pressure_release", 0.0) or 0.0),
            "load_bearing_capacity": float(attempt_feedback.get("load_bearing_capacity", 0.0) or 0.0),
            "state_stability": float(attempt_feedback.get("state_stability", 0.0) or 0.0),
            "capacity_reserve": float(attempt_feedback.get("capacity_reserve", 0.0) or 0.0),
            "recovery_balance": float(attempt_feedback.get("recovery_balance", 0.0) or 0.0),
            "regulated_courage": float(attempt_feedback.get("regulated_courage", 0.0) or 0.0),
            "courage_gap": float(attempt_feedback.get("courage_gap", 0.0) or 0.0),
            "action_inhibition": float(attempt_feedback.get("action_inhibition", 0.0) or 0.0),
            "action_clearance": float(attempt_feedback.get("action_clearance", 0.0) or 0.0),
            "regulation_before_action": float(attempt_feedback.get("regulation_before_action", 0.0) or 0.0),
            "observation_learning_open": int(attempt_feedback.get("observation_learning_open", 0) or 0),
            "observation_learning_resolved": int(attempt_feedback.get("observation_learning_resolved", 0) or 0),
            "observation_saved_loss": int(attempt_feedback.get("observation_saved_loss", 0) or 0),
            "observation_missed_gain": int(attempt_feedback.get("observation_missed_gain", 0) or 0),
            "observation_neutral": int(attempt_feedback.get("observation_neutral", 0) or 0),
            "observation_low_count": int(attempt_feedback.get("observation_low_count", 0) or 0),
            "observation_maturity_trust": float(attempt_feedback.get("observation_maturity_trust", 0.0) or 0.0),
            "observation_action_pressure": float(attempt_feedback.get("observation_action_pressure", 0.0) or 0.0),
            "attempt_fill_rate": float(self.data.get("attempts_filled", 0) or 0) / max(1, attempts),
            "attempt_zone_share": float(self.data.get("attempt_structure_zone", 0) or 0) / max(1, attempts),
            "attempts_per_trade": float(attempts / max(1, trades)),
            "long_trade_share": float(long_trades / max(1, trades)),
            "short_trade_share": float(short_trades / max(1, trades)),
            "long_attempt_share": float(self.data.get("attempts_long", 0) or 0) / max(1, attempts),
            "short_attempt_share": float(self.data.get("attempts_short", 0) or 0) / max(1, attempts),
            "max_drawdown_abs": float(self.data.get("max_drawdown_abs", 0.0) or 0.0),
            "max_drawdown_pct": float(self.data.get("max_drawdown_pct", 0.0) or 0.0),
            "winrate": float(winrate),
            "profit_factor": float(profit_factor),
            "expectancy": float(expectancy),
            "avg_win": float(avg_win),
            "avg_loss": float(avg_loss),
        }

        self.data["kpi_summary"] = {
            "proof": dict(proof),
            "state_core": {
                "state_stability": float(proof.get("state_stability", 0.0) or 0.0),
                "capacity_reserve": float(proof.get("capacity_reserve", 0.0) or 0.0),
                "recovery_balance": float(proof.get("recovery_balance", 0.0) or 0.0),
                "context_quality": float(proof.get("context_quality", 0.0) or 0.0),
                "overtrade_pressure": float(proof.get("overtrade_pressure", 0.0) or 0.0),
            },
            "regulation_core": {
                "regulatory_load": float(proof.get("regulatory_load", 0.0) or 0.0),
                "action_capacity": float(proof.get("action_capacity", 0.0) or 0.0),
                "recovery_need": float(proof.get("recovery_need", 0.0) or 0.0),
                "survival_pressure": float(proof.get("survival_pressure", 0.0) or 0.0),
                "pressure_release": float(proof.get("pressure_release", 0.0) or 0.0),
                "load_bearing_capacity": float(proof.get("load_bearing_capacity", 0.0) or 0.0),
                "pressure_to_capacity": float(proof.get("pressure_to_capacity", 0.0) or 0.0),
                "regulated_courage": float(proof.get("regulated_courage", 0.0) or 0.0),
                "courage_gap": float(proof.get("courage_gap", 0.0) or 0.0),
                "action_inhibition": float(proof.get("action_inhibition", 0.0) or 0.0),
                "action_clearance": float(proof.get("action_clearance", 0.0) or 0.0),
                "regulation_before_action": float(proof.get("regulation_before_action", 0.0) or 0.0),
            },
            "flow": {
                "attempt_density": float(proof.get("attempt_density", 0.0) or 0.0),
                "attempt_fill_rate": float(proof.get("attempt_fill_rate", 0.0) or 0.0),
                "attempt_zone_share": float(proof.get("attempt_zone_share", 0.0) or 0.0),
                "attempts_per_trade": float(proof.get("attempts_per_trade", 0.0) or 0.0),
                "observe_share": float(proof.get("observe_share", 0.0) or 0.0),
                "replan_share": float(proof.get("replan_share", 0.0) or 0.0),
                "withheld_share": float(proof.get("withheld_share", 0.0) or 0.0),
            },
            "observation_learning": {
                "open": int(proof.get("observation_learning_open", 0) or 0),
                "resolved": int(proof.get("observation_learning_resolved", 0) or 0),
                "saved_loss": int(proof.get("observation_saved_loss", 0) or 0),
                "missed_gain": int(proof.get("observation_missed_gain", 0) or 0),
                "neutral": int(proof.get("observation_neutral", 0) or 0),
                "low_observations": int(proof.get("observation_low_count", 0) or 0),
                "maturity_trust": float(proof.get("observation_maturity_trust", 0.0) or 0.0),
                "action_pressure": float(proof.get("observation_action_pressure", 0.0) or 0.0),
            },
            "economics": {
                "winrate": float(proof.get("winrate", 0.0) or 0.0),
                "profit_factor": float(proof.get("profit_factor", 0.0) or 0.0),
                "expectancy": float(proof.get("expectancy", 0.0) or 0.0),
                "avg_win": float(proof.get("avg_win", 0.0) or 0.0),
                "avg_loss": float(proof.get("avg_loss", 0.0) or 0.0),
                "max_drawdown_abs": float(proof.get("max_drawdown_abs", 0.0) or 0.0),
                "max_drawdown_pct": float(proof.get("max_drawdown_pct", 0.0) or 0.0),
            },
            "direction_profile": {
                "long_trades": int(long_trades),
                "short_trades": int(short_trades),
                "long_tp": int(long_tp),
                "long_sl": int(long_sl),
                "short_tp": int(short_tp),
                "short_sl": int(short_sl),
                "long_pnl": float(long_pnl),
                "short_pnl": float(short_pnl),
                "long_winrate": float(long_tp / max(1, long_trades)),
                "short_winrate": float(short_tp / max(1, short_trades)),
                "long_trade_share": float(proof.get("long_trade_share", 0.0) or 0.0),
                "short_trade_share": float(proof.get("short_trade_share", 0.0) or 0.0),
                "attempts_long": int(self.data.get("attempts_long", 0) or 0),
                "attempts_short": int(self.data.get("attempts_short", 0) or 0),
                "attempts_submitted_long": int(self.data.get("attempts_submitted_long", 0) or 0),
                "attempts_submitted_short": int(self.data.get("attempts_submitted_short", 0) or 0),
                "attempts_filled_long": int(self.data.get("attempts_filled_long", 0) or 0),
                "attempts_filled_short": int(self.data.get("attempts_filled_short", 0) or 0),
                "long_attempt_share": float(proof.get("long_attempt_share", 0.0) or 0.0),
                "short_attempt_share": float(proof.get("short_attempt_share", 0.0) or 0.0),
            },
            "structure_bands": {
                "high": dict(band_stats["high"]),
                "mid": dict(band_stats["mid"]),
                "low": dict(band_stats["low"]),
            },
            "emergent_structure": {
                key: dict(value) for key, value in emergent_structure_stats.items()
            },
            "open_hypothesis_learning": {
                key: dict(value) for key, value in open_hypothesis_learning_stats.items()
            },
            "open_hypothesis_reorganization_posture": {
                key: dict(value) for key, value in open_hypothesis_reorganization_posture_stats.items()
            },
            "totals": {
                "trades": int(trades),
                "tp": int(tp),
                "sl": int(sl),
                "cancels": int(cancels),
                "attempts": int(attempts),
                "attempts_observed": int(self.data.get("attempts_observed", 0) or 0),
                "attempts_replanned": int(self.data.get("attempts_replanned", 0) or 0),
                "attempts_withheld": int(self.data.get("attempts_withheld", 0) or 0),
                "long_trades": int(long_trades),
                "short_trades": int(short_trades),
                "pnl_netto": float(pnl_netto),
            },
        }

    # ─────────────────────────────────────────────
    def _pick_fields(self, payload: dict, keys: list[str]) -> dict:
        source = dict(payload or {})
        result = {}

        for key in list(keys or []):
            if key not in source:
                continue

            value = source.get(key)
            if value is None:
                continue

            result[str(key)] = value

        return result

    # ─────────────────────────────────────────────
    def _net_pnl_at_price(self, *, side: str, entry: float, exit_price: float, amount: float) -> float:
        side_key = str(side or "").upper().strip()
        if side_key == "LONG":
            gross = (float(exit_price) - float(entry)) * float(amount)
        elif side_key == "SHORT":
            gross = (float(entry) - float(exit_price)) * float(amount)
        else:
            return 0.0

        fee_rate = getattr(Config, "FEE_RATE", 0.0) or 0.0
        fees = (
            (float(entry) * float(amount) * fee_rate) +
            (float(exit_price) * float(amount) * fee_rate) +
            (Config.FEE_PER_TRADE or 0.0)
        )
        return float(gross - fees)

    # ─────────────────────────────────────────────
    def _record_exit_candidate_replay(self, *, entry: float, side: str, amount: float, actual_reason: str, actual_exit_price: float, actual_pnl: float, context: dict):
        replay_state = dict((context or {}).get("exit_candidate_replay_state", {}) or {})
        if not bool(replay_state.get("exit_candidate", False)):
            return None

        try:
            candidate_price = float(replay_state.get("candidate_price", replay_state.get("close", 0.0)) or 0.0)
        except Exception:
            candidate_price = 0.0
        if candidate_price <= 0.0:
            return None

        hypothetical_pnl = self._net_pnl_at_price(
            side=str(side),
            entry=float(entry),
            exit_price=float(candidate_price),
            amount=float(amount),
        )
        delta_pnl = float(hypothetical_pnl) - float(actual_pnl)
        actual_reason_key = str(actual_reason or "").strip().lower()

        self.data["exit_candidate_replay_count"] = int(self.data.get("exit_candidate_replay_count", 0) or 0) + 1
        self.data["exit_candidate_replay_actual_pnl"] = float(self.data.get("exit_candidate_replay_actual_pnl", 0.0) or 0.0) + float(actual_pnl)
        self.data["exit_candidate_replay_hypothetical_pnl"] = float(self.data.get("exit_candidate_replay_hypothetical_pnl", 0.0) or 0.0) + float(hypothetical_pnl)
        self.data["exit_candidate_replay_delta_pnl"] = float(self.data.get("exit_candidate_replay_delta_pnl", 0.0) or 0.0) + float(delta_pnl)

        if delta_pnl > 0.0 and actual_pnl < 0.0:
            self.data["exit_candidate_replay_saved_loss_count"] = int(self.data.get("exit_candidate_replay_saved_loss_count", 0) or 0) + 1
        elif delta_pnl > 0.0:
            self.data["exit_candidate_replay_saved_giveback_count"] = int(self.data.get("exit_candidate_replay_saved_giveback_count", 0) or 0) + 1
        elif delta_pnl < 0.0:
            self.data["exit_candidate_replay_harmed_count"] = int(self.data.get("exit_candidate_replay_harmed_count", 0) or 0) + 1

        if actual_reason_key == "tp_hit" and delta_pnl < 0.0:
            self.data["exit_candidate_replay_tp_cut_count"] = int(self.data.get("exit_candidate_replay_tp_cut_count", 0) or 0) + 1

        replay_csv = {
            "timestamp": self.data.get("current_timestamp"),
            "candidate_timestamp": replay_state.get("candidate_timestamp"),
            "candidate_bars_open": replay_state.get("candidate_bars_open"),
            "side": str(side or "").upper().strip(),
            "entry": float(entry),
            "candidate_price": float(candidate_price),
            "actual_exit_price": float(actual_exit_price),
            "actual_reason": str(actual_reason_key),
            "actual_pnl": float(actual_pnl),
            "hypothetical_pnl": float(hypothetical_pnl),
            "delta_pnl": float(delta_pnl),
            "confirmation_score": float(replay_state.get("confirmation_score", 0.0) or 0.0),
            "exit_decision_pressure": float(replay_state.get("exit_decision_pressure", 0.0) or 0.0),
            "plan_trust": float(replay_state.get("plan_trust", 0.0) or 0.0),
            "holding_stability": float(replay_state.get("holding_stability", 0.0) or 0.0),
            "intervention_fitness": float(replay_state.get("intervention_fitness", 0.0) or 0.0),
            "intervention_unfit_state": float(replay_state.get("intervention_unfit_state", 0.0) or 0.0),
            "exit_evidence": float(replay_state.get("exit_evidence", 0.0) or 0.0),
            "current_r": float(replay_state.get("current_r", 0.0) or 0.0),
            "candidate_mfe_r": float(replay_state.get("candidate_mfe_r", 0.0) or 0.0),
            "candidate_mae_r": float(replay_state.get("candidate_mae_r", 0.0) or 0.0),
            "target_expectation_context": str(replay_state.get("target_expectation_context", "") or ""),
            "tp_reachability": float(replay_state.get("tp_reachability", 0.0) or 0.0),
            "target_path_integrity": float(replay_state.get("target_path_integrity", 0.0) or 0.0),
            "expectation_deviation": float(replay_state.get("expectation_deviation", 0.0) or 0.0),
            "expectation_break_pressure": float(replay_state.get("expectation_break_pressure", 0.0) or 0.0),
            "expectation_hold_support": float(replay_state.get("expectation_hold_support", 0.0) or 0.0),
            "target_recovery_potential": float(replay_state.get("target_recovery_potential", 0.0) or 0.0),
            "target_recovery_momentum": float(replay_state.get("target_recovery_momentum", 0.0) or 0.0),
            "target_recovery_confirmation": float(replay_state.get("target_recovery_confirmation", 0.0) or 0.0),
            "break_to_recovery_delta": float(replay_state.get("break_to_recovery_delta", 0.0) or 0.0),
            "prior_target_hold_support": float(replay_state.get("prior_target_hold_support", 0.0) or 0.0),
            "prior_tp_reachability": float(replay_state.get("prior_tp_reachability", 0.0) or 0.0),
            "expectation_break_persistence": float(replay_state.get("expectation_break_persistence", 0.0) or 0.0),
            "deep_pullback_recovery_watch": int(bool(replay_state.get("deep_pullback_recovery_watch", False))),
            "recovery_after_break_watch": int(bool(replay_state.get("recovery_after_break_watch", False))),
            "entry_route_familiarity": float(replay_state.get("entry_route_familiarity", 0.0) or 0.0),
            "entry_transfer_bearing": float(replay_state.get("entry_transfer_bearing", 0.0) or 0.0),
            "current_route_familiarity": float(replay_state.get("current_route_familiarity", 0.0) or 0.0),
            "current_semantic_shift_pressure": float(replay_state.get("current_semantic_shift_pressure", 0.0) or 0.0),
            "current_transfer_bearing": float(replay_state.get("current_transfer_bearing", 0.0) or 0.0),
            "current_interpretation_quality": float(replay_state.get("current_interpretation_quality", 0.0) or 0.0),
            "current_adaptation_phase": str(replay_state.get("current_adaptation_phase", "") or ""),
            "route_familiarity_delta": float(replay_state.get("route_familiarity_delta", 0.0) or 0.0),
            "transfer_bearing_delta": float(replay_state.get("transfer_bearing_delta", 0.0) or 0.0),
            "semantic_transfer_stress": float(replay_state.get("semantic_transfer_stress", 0.0) or 0.0),
        }
        self._append_exit_candidate_replay_csv(replay_csv)

        dbr_debug(
            "EXIT_CANDIDATE_REPLAY "
            f"ts={self.data.get('current_timestamp')} "
            f"candidate_ts={replay_state.get('candidate_timestamp')} "
            f"side={str(side or '').upper().strip()} "
            f"entry={float(entry):.4f} candidate_price={candidate_price:.4f} "
            f"actual_exit_price={float(actual_exit_price):.4f} actual_reason={actual_reason_key} "
            f"actual_pnl={float(actual_pnl):.6f} hypothetical_pnl={float(hypothetical_pnl):.6f} "
            f"delta_pnl={float(delta_pnl):.6f} "
            f"score={float(replay_state.get('confirmation_score', 0.0) or 0.0):.4f} "
            f"pressure={float(replay_state.get('exit_decision_pressure', 0.0) or 0.0):.4f} "
            f"plan_trust={float(replay_state.get('plan_trust', 0.0) or 0.0):.4f} "
            f"fitness={float(replay_state.get('intervention_fitness', 0.0) or 0.0):.4f}",
            "mcm_exit_candidate_replay_debug.log",
        )

        return {
            "candidate_price": float(candidate_price),
            "hypothetical_pnl": float(hypothetical_pnl),
            "delta_pnl": float(delta_pnl),
        }

    # ─────────────────────────────────────────────
    def _append_exit_candidate_replay_csv(self, record: dict):
        try:
            path = str(self.exit_candidate_replay_path)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            keys = [
                "timestamp",
                "candidate_timestamp",
                "candidate_bars_open",
                "side",
                "entry",
                "candidate_price",
                "actual_exit_price",
                "actual_reason",
                "actual_pnl",
                "hypothetical_pnl",
                "delta_pnl",
                "confirmation_score",
                "exit_decision_pressure",
                "plan_trust",
                "holding_stability",
                "intervention_fitness",
                "intervention_unfit_state",
                "exit_evidence",
                "current_r",
                "candidate_mfe_r",
                "candidate_mae_r",
                "target_expectation_context",
                "tp_reachability",
                "target_path_integrity",
                "expectation_deviation",
                "expectation_break_pressure",
                "expectation_hold_support",
                "target_recovery_potential",
                "target_recovery_momentum",
                "target_recovery_confirmation",
                "break_to_recovery_delta",
                "prior_target_hold_support",
                "prior_tp_reachability",
                "expectation_break_persistence",
                "deep_pullback_recovery_watch",
                "recovery_after_break_watch",
                "entry_route_familiarity",
                "entry_transfer_bearing",
                "current_route_familiarity",
                "current_semantic_shift_pressure",
                "current_transfer_bearing",
                "current_interpretation_quality",
                "current_adaptation_phase",
                "route_familiarity_delta",
                "transfer_bearing_delta",
                "semantic_transfer_stress",
            ]
            header_key = f"_csv_header_written::{path}"
            write_header = (not os.path.exists(path)) and not bool(getattr(self, header_key, False))
            payload = ""
            if write_header:
                payload += ",".join(keys) + "\n"
                setattr(self, header_key, True)
            payload += ",".join(str((record or {}).get(key, "")) for key in keys) + "\n"
            dbr_append_text(
                path,
                payload,
                operation="exit_candidate_replay_csv_append",
            )
        except Exception:
            pass

    # ─────────────────────────────────────────────
    def _compact_context(self, context: dict) -> dict:
        normalized_context = self._normalize_record_value(context or {})
        compact_attempt = bool(getattr(Config, "TRADE_STATS_ATTEMPT_RECORD_COMPACT", True))

        def _compact_snapshot(value):
            item = self._normalize_record_value(value or {})
            if not isinstance(item, dict):
                return {}
            return {
                "tension": self._pick_fields(item.get("tension", {}), [
                    "stability",
                    "clarity",
                    "pressure",
                    "conflict",
                    "recovery_balance",
                ]),
                "field": self._pick_fields(item.get("field", {}), [
                    "pressure_to_capacity",
                    "regulatory_load",
                    "action_capacity",
                    "recovery_need",
                    "survival_pressure",
                    "capacity_reserve",
                    "recovery_balance",
                    "field_perception_label",
                    "field_perception_clarity",
                    "field_perception_fragmentation",
                    "field_perception_strain",
                ]),
                "experience": self._pick_fields(item.get("experience", {}), [
                    "pressure_release",
                    "load_bearing_capacity",
                    "process_quality",
                    "carrying_capacity_delta",
                    "self_confidence_delta",
                ]),
            }

        compact = {
            "state": self._pick_fields(normalized_context.get("state", {}), [
                "energy",
                "coherence",
                "asymmetry",
                "coh_zone",
                "self_state",
                "attractor",
            ]),
            "focus": self._pick_fields(normalized_context.get("focus", {}), [
                "focus_point",
                "focus_confidence",
                "target_lock",
                "target_drift",
            ]),
            "experience": self._pick_fields(normalized_context.get("experience", {}), [
                "entry_expectation",
                "target_expectation",
                "approach_pressure",
                "pressure_release",
                "experience_regulation",
                "reflection_maturity",
                "load_bearing_capacity",
                "protective_width_regulation",
                "protective_courage",
                "carrying_balance",
                "bearing_pressure_gap",
            ]),
            "field_state": self._pick_fields(normalized_context.get("field_state", {}), [
                "field_density",
                "field_stability",
                "regulatory_load",
                "action_capacity",
                "recovery_need",
                "survival_pressure",
                "pressure_to_capacity",
                "capacity_reserve",
                "recovery_balance",
            ]),
            "bearing_context": self._pick_fields(normalized_context.get("bearing_context", {}), [
                "structure_quality",
                "bearing_pressure",
                "load_bearing_capacity",
                "regulation_cost",
                "relief_quality",
            ]),
            "position_watch_state": self._pick_fields(normalized_context.get("position_watch_state", {}), [
                "mfe",
                "mae",
                "risk",
                "mfe_r",
                "mae_r",
                "fill_ratio",
                "bars_open",
            ]),
            "position_intervention_state": self._pick_fields(normalized_context.get("position_intervention_state", {}), [
                "position_cognitive_load",
                "exit_decision_pressure",
                "holding_stability",
                "plan_trust",
                "intervention_fatigue",
                "inner_noise",
                "intervention_fitness",
                "intervention_unfit_state",
                "exit_evidence",
                "sustained_exit_pressure",
                "current_r",
                "giveback_r",
                "mfe_r",
                "mae_r",
                "pressure_to_capacity",
                "structure_quality",
                "structure_stability",
                "context_confidence",
                "bars_open",
                "intervention_label",
                "position_inconsistency_stress",
                "position_mcm_field_strain",
                "position_self_trust_gap",
                "position_cortisol_load",
                "position_noradrenaline_arousal",
                "position_protective_distance",
                "position_held_risk_discomfort",
                "position_process_quality",
                "position_experience_label",
            ]),
            "target_expectation_state": self._pick_fields(normalized_context.get("target_expectation_state", {}), [
                "target_expectation_context",
                "tp_reachability",
                "target_path_integrity",
                "expectation_deviation",
                "expectation_break_pressure",
                "expectation_hold_support",
                "target_room_pressure",
                "target_semantic_confidence",
                "target_progress",
                "target_remaining_r",
                "target_total_r",
                "target_recovery_potential",
                "target_recovery_momentum",
                "target_recovery_confirmation",
                "break_to_recovery_delta",
                "recovery_after_break_watch",
                "prior_target_hold_support",
                "prior_tp_reachability",
                "prior_target_path_integrity",
                "expectation_break_persistence",
                "expectation_break_count",
                "deep_pullback_recovery_watch",
                "base_entry_expectation",
                "base_target_expectation",
                "entry_route_familiarity",
                "entry_transfer_bearing",
                "current_route_familiarity",
                "current_semantic_shift_pressure",
                "current_transfer_bearing",
                "current_interpretation_quality",
                "current_adaptation_phase",
                "route_familiarity_delta",
                "transfer_bearing_delta",
                "semantic_transfer_stress",
            ]),
            "matured_exit_state": self._pick_fields(normalized_context.get("matured_exit_state", {}), [
                "mode",
                "exit_price",
                "maturity_pressure",
                "mfe_r",
                "mae_r",
                "current_r",
                "giveback_r",
                "structure_quality",
                "pressure_to_capacity",
                "recovery_balance",
                "bars_open",
            ]),
            "exit_candidate_observe_state": self._pick_fields(normalized_context.get("exit_candidate_observe_state", {}), [
                "exit_candidate",
                "candidate_label",
                "confirmation_score",
                "exit_decision_pressure",
                "plan_trust",
                "holding_stability",
                "intervention_fitness",
                "intervention_unfit_state",
                "exit_evidence",
                "current_r",
                "adverse_depth_ok",
                "sustained_exit_pressure",
                "target_expectation_context",
                "tp_reachability",
                "target_path_integrity",
                "expectation_deviation",
                "expectation_break_pressure",
                "expectation_hold_support",
                "target_recovery_potential",
                "target_recovery_momentum",
                "target_recovery_confirmation",
                "break_to_recovery_delta",
                "prior_target_hold_support",
                "prior_tp_reachability",
                "expectation_break_persistence",
                "deep_pullback_recovery_watch",
                "recovery_after_break_watch",
                "entry_route_familiarity",
                "entry_transfer_bearing",
                "current_route_familiarity",
                "current_semantic_shift_pressure",
                "current_transfer_bearing",
                "current_interpretation_quality",
                "current_adaptation_phase",
                "route_familiarity_delta",
                "transfer_bearing_delta",
                "semantic_transfer_stress",
            ]),
            "exit_candidate_replay_state": self._pick_fields(normalized_context.get("exit_candidate_replay_state", {}), [
                "exit_candidate",
                "candidate_label",
                "confirmation_score",
                "exit_decision_pressure",
                "plan_trust",
                "holding_stability",
                "intervention_fitness",
                "intervention_unfit_state",
                "exit_evidence",
                "current_r",
                "adverse_depth_ok",
                "sustained_exit_pressure",
                "candidate_timestamp",
                "candidate_bars_open",
                "candidate_price",
                "candidate_mfe_r",
                "candidate_mae_r",
                "target_expectation_context",
                "tp_reachability",
                "target_path_integrity",
                "expectation_deviation",
                "expectation_break_pressure",
                "expectation_hold_support",
                "target_recovery_potential",
                "target_recovery_momentum",
                "target_recovery_confirmation",
                "break_to_recovery_delta",
                "prior_target_hold_support",
                "prior_tp_reachability",
                "expectation_break_persistence",
                "deep_pullback_recovery_watch",
                "recovery_after_break_watch",
                "entry_route_familiarity",
                "entry_transfer_bearing",
                "current_route_familiarity",
                "current_semantic_shift_pressure",
                "current_transfer_bearing",
                "current_interpretation_quality",
                "current_adaptation_phase",
                "route_familiarity_delta",
                "transfer_bearing_delta",
                "semantic_transfer_stress",
            ]),
            "thought_seed_state": self._pick_fields(normalized_context.get("thought_seed_state", {}), [
                "thought_seed_id",
                "thought_seed_label",
                "thought_trace_strength",
                "thought_recall_potential",
                "thought_maturity",
                "reality_binding_score",
                "thought_confirmation_score",
                "consequence_echo",
                "reorganization_echo",
                "thought_consequence_alignment",
                "thought_consequence_balance",
                "thought_reality_lag",
                "thought_structural_grounding",
                "thought_open_hypothesis_pressure",
                "thought_replay_maturation_pull",
                "thought_distance_maturation_pull",
                "thought_reinterpretation_pull",
                "thought_digestive_replay_pull",
                "thought_digestive_distance_pull",
                "thought_digestive_integration_pull",
                "thought_digestive_returned_trust",
                "trust_return_readiness",
                "thought_digest_state",
                "thought_reifung_direction",
                "semantic_origin_state",
                "borrowed_open_hypothesis_pressure",
                "own_field_binding_pull",
                "own_vs_foreign_margin",
                "borrowed_vs_own_margin",
                "boundary_support_margin",
                "previous_open_hypothesis_learning_state",
                "previous_open_hypothesis_reorganization_posture",
                "hallucination_drift_risk",
                "overthinking_risk",
                "seed_metaregulator_state",
                "emergent_memory_trace",
                "emergent_structure_state",
                "emergent_structure_reading",
                "form_symbol_anchor",
                "mcm_field_anchor",
                "experience_memory_anchor",
                "outcome_anchor",
                "decision",
                "phase",
                "reason",
                "rr_value",
            ]),
            "regulation_snapshot": _compact_snapshot(normalized_context.get("regulation_snapshot", {})) if compact_attempt else self._normalize_record_value(normalized_context.get("regulation_snapshot", {})),
            "state_before": _compact_snapshot(normalized_context.get("state_before", {})) if compact_attempt else self._normalize_record_value(normalized_context.get("state_before", {})),
            "state_after": _compact_snapshot(normalized_context.get("state_after", {})) if compact_attempt else self._normalize_record_value(normalized_context.get("state_after", {})),
            "state_delta": _compact_snapshot(normalized_context.get("state_delta", {})) if compact_attempt else self._normalize_record_value(normalized_context.get("state_delta", {})),
            "world_state": self._pick_fields(normalized_context.get("world_state", {}), [
                "current_price",
                "close",
                "last_price",
                "price",
                "candle_state",
            ]),
            "felt_state": self._pick_fields(normalized_context.get("felt_state", {}), [
                "confidence",
                "urgency",
                "pressure",
                "hesitation",
                "protective_tension",
                "courage_tension",
                "relief_need",
                "regulated_confidence",
            ]),
            "meta_regulation_state": self._pick_fields(normalized_context.get("meta_regulation_state", {}), [
                "decision",
                "observation_priority",
                "uncertainty_load",
                "regulatory_balance",
                "neurochemical_state_label",
                "neurochemical_dominant_tone",
                "dopamine_tone",
                "gaba_inhibition",
                "noradrenaline_arousal",
                "acetylcholine_focus",
                "serotonin_stability",
                "cortisol_load",
                "endorphin_relief",
                "glutamate_activation",
                "neurochemical_load",
                "neurochemical_support",
                "neurochemical_balance",
                "reward_stability_echo",
                "world_shift_evidence",
                "serotonin_carryover_risk",
                "emotional_decoupling",
                "reactive_nervous_drive",
                "nervous_system_overload",
                "escape_action_drive",
                "shock_response_risk",
                "nervous_overload_reflection_need",
                "previous_digest_state",
                "previous_trust_return_readiness",
                "previous_digestive_returned_trust",
                "previous_emergent_structure_state",
                "previous_confirmed_structure_protection",
                "trust_return_open_hypothesis_load",
                "trust_return_context_instability",
                "trust_return_motor_contact_strength",
                "trust_return_act_bridge",
                "trust_return_motor_heat",
                "trust_return_stabilization_need",
                "trust_return_focus_pull",
                "trust_return_motor_mode",
                "active_context_self_certainty",
                "nervous_context_overcoupling",
                "own_field_identity_strength",
                "foreign_semantic_pressure",
                "adopted_language_pressure",
                "self_foreign_boundary_clarity",
                "semantic_origin_conflict",
                "own_vs_foreign_margin",
                "borrowed_vs_own_margin",
                "boundary_support_margin",
                "semantic_origin_state",
                "conscious_perception_state",
                "inner_posture_state",
                "arousal_load",
                "curiosity_tone",
                "fatigue_tone",
                "calm_tone",
                "stimulus_field_effect",
                "inner_impact_trace",
                "perceived_field_change",
                "felt_afterimage",
                "object_release_state",
                "inner_outer_reflection",
                "perceptual_distance",
                "object_contact_depth",
                "field_attachment",
                "release_capacity",
                "selective_attention",
                "background_containment",
                "reflective_distance",
                "inner_outer_alignment",
                "engaged_effort",
                "effort_state",
                "effort_learning_pull",
                "effort_reorganization_pressure",
                "pre_action_reorganization_pressure",
                "pre_action_context_selectivity",
                "strategic_window_state",
                "strategic_pressure_interpretation",
                "strategic_patience",
                "lookback_bearing_capacity",
                "area_bearing_quality",
                "area_order_intention",
                "active_mcm_contact_state",
                "contact_posture",
                "contact_interest",
                "contact_focus_pull",
                "contact_resonance_probe",
                "outer_inner_resonance",
                "outer_inner_coherence",
                "inner_change_from_contact",
                "contact_carrying_quality",
                "contact_overcoupling_risk",
                "contact_release_readiness",
                "contact_deepen_pull",
                "contact_replay_pull",
                "contact_curiosity",
                "contact_felt_shift",
                "contact_selected_depth",
                "contact_salience",
                "overcoupled_touch_score",
                "release_contact_score",
                "deepening_contact_score",
                "resonant_contact_score",
                "reflective_contact_score",
                "curious_touch_score",
                "contact_action_maturity",
                "contact_bearing_gap",
                "contact_impulse_vs_bearing",
                "contact_learning_need",
                "contact_reality_check",
                "contact_regime_mismatch",
                "contact_stability_carryover",
                "contact_context_maturity",
                "contact_context_reframe_need",
                "previous_packet_label",
                "previous_packet_process_reward",
                "previous_packet_reorganization_need",
                "diffuse_open_development_pressure",
                "posture_development_hint",
                "regulated_courage",
                "courage_gap",
                "action_inhibition",
                "action_clearance",
                "pre_action_phase",
                "dominant_tension_cause",
                "known_form_support",
                "route_familiarity",
                "semantic_shift_pressure",
                "transfer_bearing",
                "interpretation_quality",
                "adaptation_phase",
                "trust_transfer_base",
                "trust_transfer_support",
                "transfer_maturity_gap",
                "trust_transfer_mode",
                "transfer_break_fatigue",
                "transfer_recovery_need",
                "transfer_break_trigger",
                "transfer_break_ready",
                "visual_blind_action_load",
                "visual_action_uncertainty",
                "visual_object_binding",
                "visual_grounding_strength",
                "visual_resonance_unbound",
                "visual_grounding_gap",
                "visual_grounding_need",
                "visual_rational_observation_support",
                "visual_grounding_state",
                "uncertain_form_family_state",
                "uncertain_form_exposure",
                "uncertainty_familiarity",
                "variant_similarity",
                "variant_spread",
                "variant_learning_pressure",
                "variant_bearing_memory",
                "form_symbol_semantic_density",
                "form_symbol_semantic_compression",
                "form_symbol_semantic_coherence",
                "form_symbol_semantic_learning_need",
                "form_symbol_semantic_action_nearness",
                "form_symbol_semantic_primary_layer",
                "form_symbol_semantic_layer_count",
                "form_symbol_semantic_packet_state",
                "form_symbol_semantic_profile",
            ]),            
            "strategic_window_state": self._pick_fields(normalized_context.get("strategic_window_state", {}), [
                "strategic_window_state",
                "lookback_window_size",
                "lookback_load",
                "lookback_relevance",
                "lookback_bearing_capacity",
                "replay_budget",
                "zoom_budget",
                "old_structure_carryover_risk",
                "strategic_pressure_interpretation",
                "strategic_patience",
                "area_candidate_count",
                "area_focus_id",
                "area_price_low",
                "area_price_high",
                "area_distance_from_price",
                "area_structural_density",
                "area_energy_compression",
                "area_mcm_resonance",
                "area_memory_pull",
                "area_bearing_quality",
                "area_zoom_need",
                "area_zoom_clarity",
                "area_replay_fit",
                "area_patience_quality",
                "area_order_intention",
                "area_invalidity_pressure",
            ]),
            "active_mcm_contact_state": self._pick_fields(
                normalized_context.get("active_mcm_contact_state", normalized_context.get("meta_regulation_state", {}).get("active_mcm_contact", {})),
                [
                    "active_mcm_contact_state",
                    "contact_posture",
                    "contact_interest",
                    "contact_focus_pull",
                    "contact_resonance_probe",
                    "outer_inner_resonance",
                    "outer_inner_coherence",
                    "inner_change_from_contact",
                    "contact_carrying_quality",
                    "contact_overcoupling_risk",
                    "contact_release_readiness",
                    "contact_deepen_pull",
                    "contact_replay_pull",
                    "contact_curiosity",
                    "contact_felt_shift",
                    "contact_selected_depth",
                    "contact_salience",
                    "overcoupled_touch_score",
                    "release_contact_score",
                    "deepening_contact_score",
                    "resonant_contact_score",
                    "reflective_contact_score",
                    "curious_touch_score",
                    "contact_action_maturity",
                    "contact_bearing_gap",
                    "contact_impulse_vs_bearing",
                    "contact_learning_need",
                    "contact_reality_check",
                    "contact_regime_mismatch",
                    "contact_stability_carryover",
                    "contact_context_maturity",
                    "contact_context_reframe_need",
                ],
            ),
            "expectation_state": self._pick_fields(normalized_context.get("expectation_state", {}), [
                "entry_expectation",
                "target_expectation",
                "approach_pressure",
                "pressure_release",
                "experience_regulation",
                "reflection_maturity",
                "load_bearing_capacity",
            ]),
            "neurochemical_state": self._pick_fields(
                normalized_context.get("neurochemical_state", normalized_context.get("meta_regulation_state", {}).get("neurochemical_state", {})),
                [
                    "neurochemical_state_label",
                    "neurochemical_dominant_tone",
                    "dopamine_tone",
                    "gaba_inhibition",
                    "noradrenaline_arousal",
                    "acetylcholine_focus",
                    "serotonin_stability",
                    "cortisol_load",
                    "endorphin_relief",
                    "glutamate_activation",
                    "neurochemical_load",
                    "neurochemical_support",
                    "neurochemical_balance",
                    "reward_stability_echo",
                    "world_shift_evidence",
                    "serotonin_carryover_risk",
                    "emotional_decoupling",
                    "reactive_nervous_drive",
                ],
            ),
            "form_symbol_state": self._pick_fields(normalized_context.get("form_symbol_state", {}), [
                "form_symbol_id",
                "form_symbol_scope",
                "form_symbol_development_quality",
                "form_symbol_action_affinity",
                "form_symbol_action_binding",
                "form_symbol_observation_affinity",
                "form_symbol_observation_binding",
                "form_symbol_reframe_binding",
                "form_symbol_learning_trust",
                "form_symbol_action_trust",
                "form_symbol_caution_trust",
                "form_symbol_contact_maturity",
                "form_symbol_contact_utility",
                "form_symbol_contact_pain_memory",
                "form_symbol_contact_carefulness",
                "form_symbol_contact_burden_evidence",
                "form_symbol_contact_utility_evidence",
                "form_symbol_contact_learning_state",
                "form_symbol_compound_id",
                "form_symbol_compound_development_quality",
                "form_symbol_compound_action_affinity",
                "form_symbol_compound_observation_affinity",
                "form_symbol_compound_reframe_potential",
                "form_symbol_compound_learning_trust",
                "form_symbol_compound_action_trust",
                "form_symbol_compound_caution_trust",
                "uncertain_form_family_state",
                "uncertain_form_exposure",
                "uncertainty_familiarity",
                "variant_similarity",
                "variant_spread",
                "variant_learning_pressure",
                "variant_bearing_memory",
                "form_symbol_semantic_density",
                "form_symbol_semantic_compression",
                "form_symbol_semantic_coherence",
                "form_symbol_semantic_learning_need",
                "form_symbol_semantic_action_nearness",
                "form_symbol_semantic_primary_layer",
                "form_symbol_semantic_layer_count",
                "form_symbol_semantic_packet_state",
                "form_symbol_semantic_profile",
            ]),
            "trade_plan": self._pick_fields(normalized_context.get("trade_plan", {}), [
                "decision",
                "entry_price",
                "sl_price",
                "tp_price",
                "rr_value",
                "risk_model_score",
                "reward_model_score",
                "entry_mode",
                "impulse_entry_price",
                "strategic_entry_price",
                "strategic_entry_weight",
                "strategic_entry_fit",
                "area_motor_intention",
                "area_motor_distance_fit",
                "impulse_entry_intention",
                "area_entry_intention",
                "entry_choice_conflict",
                "entry_choice_bearing",
                "area_direct_readiness",
                "area_motor_restraint",
                "entry_choice_state",
                "entry_choice_sync",
                "strategic_area_focus_id",
                "strategic_area_price_low",
                "strategic_area_price_high",
                "entry_validity_band",
            ]),
            "structure_perception_state": self._pick_fields(normalized_context.get("structure_perception_state", {}), [
                "structure_seen",
                "swing_high_strength",
                "swing_low_strength",
                "zone_proximity",
                "structure_stability",
                "structure_quality",
                "stress_relief_potential",
                "context_confidence",
            ]),
            "signal": self._pick_fields(normalized_context.get("signal", {}), [
                "signature_bias",
                "signature_block",
                "signature_quality",
                "signature_distance",
                "context_cluster_id",
                "context_cluster_bias",
                "context_cluster_quality",
                "context_cluster_distance",
                "context_cluster_block",
                "inhibition_level",
                "habituation_level",
                "competition_bias",
                "observation_mode",
                "long_score",
                "short_score",
            ]),
        }
        return {key: value for key, value in compact.items() if value}
    # ─────────────────────────────────────────────
    def _save(self, force: bool = False):
        try:
            if not bool(force):
                every_n = max(1, int(getattr(Config, "TRADE_STATS_JSON_SAVE_EVERY_N", 1) or 1))
                self._json_save_seq = int(getattr(self, "_json_save_seq", 0) or 0) + 1
                if every_n > 1 and (self._json_save_seq % every_n) != 0:
                    return

            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            write_start = time.perf_counter()
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
            elapsed_ms = (time.perf_counter() - write_start) * 1000.0
            try:
                bytes_written = int(os.path.getsize(self.path))
            except Exception:
                bytes_written = 0
            dbr_file_write_profile(
                self.path,
                elapsed_ms,
                bytes_written=bytes_written,
                operation="trade_stats_json_dump",
                extra=f"force={bool(force)}|trades={int(self.data.get('trades', 0) or 0)}|attempts={int(self.data.get('attempts', 0) or 0)}",
            )
        except Exception:
            pass

    # ─────────────────────────────────────────────
    def _extract_structure_quality(self, context: dict) -> float:
        ctx = dict(context or {})
        world_state = dict(ctx.get("world_state", {}) or {})
        structure = dict(ctx.get("structure_perception_state", {}) or {})
        bearing_context = dict(ctx.get("bearing_context", {}) or {})

        if not structure and isinstance(world_state.get("structure_perception_state"), dict):
            structure = dict(world_state.get("structure_perception_state", {}) or {})

        if not structure and isinstance(ctx.get("outer_visual_perception_state"), dict):
            structure = dict(ctx.get("outer_visual_perception_state", {}) or {})

        if not structure and isinstance(ctx.get("context"), dict):
            nested_context = dict(ctx.get("context", {}) or {})
            structure = dict(nested_context.get("structure_perception_state", {}) or {})
            if not structure:
                bearing_context = dict(nested_context.get("bearing_context", {}) or {})

        try:
            if "structure_quality" in structure:
                return float(structure.get("structure_quality", 0.0) or 0.0)
        except Exception:
            pass

        try:
            return float(bearing_context.get("structure_quality", 0.0) or 0.0)
        except Exception:
            return 0.0

    # ─────────────────────────────────────────────
    def _extract_observation_price(self, context: dict) -> float:
        ctx = dict(context or {})
        trade_plan = dict(ctx.get("trade_plan", {}) or {})
        nested = dict(ctx.get("context", {}) or {}) if isinstance(ctx.get("context", {}), dict) else {}
        compact_trade_plan = dict(nested.get("trade_plan", {}) or {})

        for source in (trade_plan, compact_trade_plan):
            try:
                price = float(source.get("entry_price", 0.0) or 0.0)
                if price > 0.0:
                    return float(price)
            except Exception:
                pass
        for source in (ctx.get("world_state", {}), nested.get("world_state", {})):
            world = dict(source or {}) if isinstance(source, dict) else {}
            candle = dict(world.get("candle_state", {}) or {}) if isinstance(world.get("candle_state", {}), dict) else {}
            for key in ("current_price", "close", "last_price", "price"):
                try:
                    price = float(world.get(key, 0.0) or candle.get(key, 0.0) or 0.0)
                    if price > 0.0:
                        return float(price)
                except Exception:
                    pass
        return 0.0

    def _infer_observation_trade_plan(self, context: dict, current_price: float) -> dict:
        ctx = dict(context or {})
        price = float(current_price or 0.0)
        if price <= 0.0:
            return {}

        meta = dict(ctx.get("meta_regulation_state", {}) or {})
        signal = dict(ctx.get("signal", {}) or {})

        side = str(meta.get("decision", "") or "").strip().upper()
        if side not in ("LONG", "SHORT"):
            try:
                long_score = float(signal.get("long_score", 0.0) or 0.0)
                short_score = float(signal.get("short_score", 0.0) or 0.0)
            except Exception:
                long_score = 0.0
                short_score = 0.0
            if max(abs(long_score), abs(short_score)) < 0.08 and abs(long_score - short_score) < 0.04:
                return {}
            side = "LONG" if long_score >= short_score else "SHORT"

        risk_pct = max(0.0015, min(0.012, float(getattr(Config, "BASE_RISK_PCT", 0.0045) or 0.0045)))
        min_rr_floor = max(0.0, float(getattr(Config, "MIN_RR", 1.0) or 1.0))
        target_expectation = float((ctx.get("experience", {}) or {}).get("target_expectation", 0.0) or 0.0)
        load_bearing_capacity = float((ctx.get("experience", {}) or {}).get("load_bearing_capacity", 0.0) or 0.0)
        focus_confidence = float((ctx.get("focus", {}) or {}).get("focus_confidence", 0.0) or 0.0)
        target_lock = float((ctx.get("focus", {}) or {}).get("target_lock", 0.0) or 0.0)
        rr_value = min_rr_floor + max(
            0.0,
            (target_expectation * 0.22)
            + (load_bearing_capacity * 0.16)
            + (focus_confidence * 0.14)
            + (target_lock * 0.12),
        )
        risk_distance = max(price * risk_pct, price * 0.0015)
        reward_distance = risk_distance * rr_value

        if side == "LONG":
            sl_price = price - risk_distance
            tp_price = price + reward_distance
        else:
            sl_price = price + risk_distance
            tp_price = price - reward_distance

        return {
            "decision": str(side),
            "entry_price": float(price),
            "sl_price": float(sl_price),
            "tp_price": float(tp_price),
            "rr_value": float(rr_value),
            "inferred_observation_plan": True,
        }

    def _refresh_observation_learning_summary(self):
        learning = dict(self.data.get("observation_learning", {}) or {})
        resolved = int(learning.get("resolved", 0) or 0)
        saved = int(learning.get("saved_loss", 0) or 0)
        missed = int(learning.get("missed_gain", 0) or 0)
        neutral = int(learning.get("neutral", 0) or 0)

        if resolved > 0:
            learning["maturity_trust"] = float(max(0.0, min(1.0, (saved + neutral * 0.35) / float(resolved))))
            learning["action_pressure"] = float(max(0.0, min(1.0, missed / float(resolved))))
        else:
            learning["maturity_trust"] = 0.0
            learning["action_pressure"] = 0.0

        learning["open"] = int(len(self.data.get("pending_observations", []) or []))
        self.data["observation_learning"] = dict(learning)
        return dict(learning)

    def _resolve_pending_observations(self, current_price: float):
        price = float(current_price or 0.0)
        if price <= 0.0:
            return

        pending = list(self.data.get("pending_observations", []) or [])
        if not pending:
            self._refresh_observation_learning_summary()
            return

        horizon = max(3, int(getattr(Config, "OBSERVATION_LEARNING_HORIZON_ATTEMPTS", 24) or 24))
        now_attempt = int(self.data.get("attempts", 0) or 0)
        learning = dict(self.data.get("observation_learning", {}) or {})
        recent = list(self.data.get("recent_observation_learning", []) or [])
        still_open = []

        for item in pending:
            obs = dict(item or {})
            side = str(obs.get("side", "") or "").strip().upper()
            entry_price = float(obs.get("entry_price", 0.0) or 0.0)
            tp_price = float(obs.get("tp_price", 0.0) or 0.0)
            sl_price = float(obs.get("sl_price", 0.0) or 0.0)
            age = int(now_attempt - int(obs.get("attempt_index", now_attempt) or now_attempt))
            result = None

            if side == "LONG":
                if tp_price > 0.0 and price >= tp_price:
                    result = "missed_gain"
                elif sl_price > 0.0 and price <= sl_price:
                    result = "saved_loss"
            elif side == "SHORT":
                if tp_price > 0.0 and price <= tp_price:
                    result = "missed_gain"
                elif sl_price > 0.0 and price >= sl_price:
                    result = "saved_loss"

            if result is None and age >= horizon:
                virtual_move = 0.0
                if entry_price > 0.0:
                    if side == "LONG":
                        virtual_move = price - entry_price
                    elif side == "SHORT":
                        virtual_move = entry_price - price
                if virtual_move > 0.0:
                    result = "missed_gain"
                elif virtual_move < 0.0:
                    result = "saved_loss"
                else:
                    result = "neutral"

            if result is None:
                still_open.append(obs)
                continue

            learning["resolved"] = int(learning.get("resolved", 0) or 0) + 1
            learning[result] = int(learning.get(result, 0) or 0) + 1
            learning["last_result"] = str(result)
            recent.append({
                "result": str(result),
                "age": int(age),
                "side": str(side or "-"),
                "structure_quality": float(obs.get("structure_quality", 0.0) or 0.0),
                "structure_bucket": str(obs.get("structure_bucket", "") or ""),
                "entry_price": float(entry_price),
                "current_price": float(price),
                "form_symbol_id": str(obs.get("form_symbol_id", "") or ""),
            })

        self.data["pending_observations"] = still_open[-120:]
        self.data["recent_observation_learning"] = recent[-80:]
        self.data["observation_learning"] = dict(learning)
        self._refresh_observation_learning_summary()

    def _register_observation_learning(self, status_key: str, context: dict, structure_quality: float, structure_bucket: str):
        compact_context = self._compact_context(context or {})
        current_price = self._extract_observation_price(compact_context)
        self._resolve_pending_observations(current_price)

        status = str(status_key or "").strip().lower()
        if status not in ("observed_only", "replanned", "withheld", "skipped"):
            return

        learning = dict(self.data.get("observation_learning", {}) or {})
        if str(structure_bucket or "").strip().lower() != "non_zone":
            learning["zone_observations"] = int(learning.get("zone_observations", 0) or 0) + 1
            self.data["observation_learning"] = dict(learning)
            self._refresh_observation_learning_summary()
            return

        trade_plan = dict(compact_context.get("trade_plan", {}) or {})
        side = str(trade_plan.get("decision", "") or "").strip().upper()
        entry_price = float(trade_plan.get("entry_price", 0.0) or 0.0)
        tp_price = float(trade_plan.get("tp_price", 0.0) or 0.0)
        sl_price = float(trade_plan.get("sl_price", 0.0) or 0.0)
        if side not in ("LONG", "SHORT") or entry_price <= 0.0 or tp_price <= 0.0 or sl_price <= 0.0:
            trade_plan = self._infer_observation_trade_plan(compact_context, current_price)
            side = str(trade_plan.get("decision", "") or "").strip().upper()
            entry_price = float(trade_plan.get("entry_price", 0.0) or 0.0)
            tp_price = float(trade_plan.get("tp_price", 0.0) or 0.0)
            sl_price = float(trade_plan.get("sl_price", 0.0) or 0.0)
            if side not in ("LONG", "SHORT") or entry_price <= 0.0 or tp_price <= 0.0 or sl_price <= 0.0:
                return

        form_state = dict(compact_context.get("form_symbol_state", {}) or {})
        pending = list(self.data.get("pending_observations", []) or [])
        pending.append({
            "attempt_index": int(self.data.get("attempts", 0) or 0),
            "timestamp": self.data.get("current_timestamp"),
            "status": str(status),
            "side": str(side),
            "entry_price": float(entry_price),
            "tp_price": float(tp_price),
            "sl_price": float(sl_price),
            "structure_quality": float(structure_quality),
            "structure_bucket": str(structure_bucket),
            "form_symbol_id": str(form_state.get("form_symbol_id", "") or ""),
        })
        self.data["pending_observations"] = pending[-120:]
        learning["low_observations"] = int(learning.get("low_observations", 0) or 0) + 1
        self.data["observation_learning"] = dict(learning)
        self._refresh_observation_learning_summary()

    def _build_attempt_record(self, status_key: str, context: dict, structure_quality: float, structure_bucket: str) -> dict:
        compact_context = self._compact_context(context or {})
        trade_plan = dict(compact_context.get("trade_plan", {}) or {})
        side = str(trade_plan.get("decision", "") or "").strip().upper()
        if side not in ("LONG", "SHORT"):
            side = "-"

        return {
            "event": "attempt",
            "status": str(status_key or "unknown"),
            "timestamp": self.data.get("current_timestamp"),
            "side": str(side),
            "structure_quality": float(structure_quality),
            "structure_bucket": str(structure_bucket),
            "context": compact_context,
        }

    # ─────────────────────────────────────────────
    def _should_write_attempt_record(self, status_key: str) -> bool:
        if not bool(getattr(Config, "TRADE_STATS_ATTEMPT_RECORD_DEBUG", True)):
            return False

        status = str(status_key or "").strip().lower()
        if status in ("submitted", "filled", "cancelled", "timeout", "blocked_value_gate"):
            return True

        every_n = max(1, int(getattr(Config, "TRADE_STATS_ATTEMPT_RECORD_EVERY_N", 1) or 1))
        if every_n <= 1:
            return True

        return (int(self.data.get("attempts", 0) or 0) % every_n) == 0

    # ─────────────────────────────────────────────
    def get_attempt_feedback(self, window: int = 24) -> dict:
        recent_attempts = list(self.data.get("recent_attempts", []) or [])
        items = recent_attempts[-max(1, int(window or 1)):]

        if not items:
            return {
                "recent_attempt_count": 0,
                "attempt_density": 0.0,
                "fill_ratio": 0.0,
                "blocked_ratio": 0.0,
                "cancel_ratio": 0.0,
                "timeout_ratio": 0.0,
                "zone_ratio": 0.0,
                "mean_structure_quality": 0.0,
                "context_quality": 0.0,
                "overtrade_pressure": 0.0,
                "observe_share": 0.0,
                "replan_share": 0.0,
                "withheld_share": 0.0,
                "pressure_to_capacity": 0.0,
                "regulatory_load": 0.0,
                "action_capacity": 0.0,
                "recovery_need": 0.0,
                "survival_pressure": 0.0,
                "pressure_release": 0.0,
                "load_bearing_capacity": 0.0,
                "state_stability": 0.0,
                "capacity_reserve": 0.0,
                "recovery_balance": 0.0,
                "regulated_courage": 0.0,
                "courage_gap": 0.0,
                "action_inhibition": 0.0,
                "action_clearance": 0.0,
                "regulation_before_action": 0.0,
                "observation_learning_open": 0,
                "observation_learning_resolved": 0,
                "observation_saved_loss": 0,
                "observation_missed_gain": 0,
                "observation_neutral": 0,
                "observation_low_count": 0,
                "observation_maturity_trust": 0.0,
                "observation_action_pressure": 0.0,
            }

        total = float(len(items))
        filled = 0.0
        blocked = 0.0
        cancelled = 0.0
        timeout = 0.0
        observed = 0.0
        replanned = 0.0
        withheld = 0.0
        zone = 0.0
        structure_sum = 0.0
        pressure_sum = 0.0
        regulatory_load_sum = 0.0
        action_capacity_sum = 0.0
        recovery_sum = 0.0
        survival_pressure_sum = 0.0
        pressure_release_sum = 0.0
        load_bearing_sum = 0.0
        state_stability_sum = 0.0
        capacity_reserve_sum = 0.0
        recovery_balance_sum = 0.0
        regulated_courage_sum = 0.0
        courage_gap_sum = 0.0
        action_inhibition_sum = 0.0
        action_clearance_sum = 0.0
        regulation_before_action_sum = 0.0

        for item in items:
            status = str((item or {}).get("status", "") or "").strip().lower()
            structure_quality = float((item or {}).get("structure_quality", 0.0) or 0.0)
            structure_bucket = str((item or {}).get("structure_bucket", "") or "").strip().lower()
            pressure_to_capacity = float((item or {}).get("pressure_to_capacity", 0.0) or 0.0)
            regulatory_load = float((item or {}).get("regulatory_load", 0.0) or 0.0)
            action_capacity = float((item or {}).get("action_capacity", 0.0) or 0.0)
            recovery_need = float((item or {}).get("recovery_need", 0.0) or 0.0)
            survival_pressure = float((item or {}).get("survival_pressure", 0.0) or 0.0)
            pressure_release = float((item or {}).get("pressure_release", 0.0) or 0.0)
            load_bearing_capacity = float((item or {}).get("load_bearing_capacity", 0.0) or 0.0)
            state_stability = float((item or {}).get("state_stability", 0.0) or 0.0)
            capacity_reserve = float((item or {}).get("capacity_reserve", 0.0) or 0.0)
            recovery_balance = float((item or {}).get("recovery_balance", 0.0) or 0.0)
            regulated_courage = float((item or {}).get("regulated_courage", 0.0) or 0.0)
            courage_gap = float((item or {}).get("courage_gap", 0.0) or 0.0)
            action_inhibition = float((item or {}).get("action_inhibition", 0.0) or 0.0)
            action_clearance = float((item or {}).get("action_clearance", 0.0) or 0.0)
            pre_action_phase = str((item or {}).get("pre_action_phase", "") or "").strip().lower()

            structure_sum += structure_quality
            pressure_sum += pressure_to_capacity
            regulatory_load_sum += regulatory_load
            action_capacity_sum += action_capacity
            recovery_sum += recovery_need
            survival_pressure_sum += survival_pressure
            pressure_release_sum += pressure_release
            load_bearing_sum += load_bearing_capacity
            state_stability_sum += state_stability
            capacity_reserve_sum += capacity_reserve
            recovery_balance_sum += recovery_balance
            regulated_courage_sum += regulated_courage
            courage_gap_sum += courage_gap
            action_inhibition_sum += action_inhibition
            action_clearance_sum += action_clearance

            if status == "filled":
                filled += 1.0
            elif status in ("blocked", "blocked_value_gate"):
                blocked += 1.0
            elif status == "cancelled":
                cancelled += 1.0
            elif status == "timeout":
                timeout += 1.0
            elif status == "observed_only":
                observed += 1.0
            elif status == "replanned":
                replanned += 1.0
            elif status == "withheld":
                withheld += 1.0

            if structure_bucket == "zone":
                zone += 1.0

            if pre_action_phase in ("regulated", "ready", "stable", "aligned"):
                regulation_before_action_sum += 1.0

        attempt_density = max(0.0, min(1.0, total / max(8.0, float(window) * 0.50)))
        fill_ratio = filled / total
        blocked_ratio = blocked / total
        cancel_ratio = cancelled / total
        timeout_ratio = timeout / total
        observe_share = observed / total
        replan_share = replanned / total
        withheld_share = withheld / total
        zone_ratio = zone / total
        mean_structure_quality = structure_sum / total
        avg_pressure_to_capacity = pressure_sum / total
        avg_regulatory_load = regulatory_load_sum / total
        avg_action_capacity = action_capacity_sum / total
        avg_recovery_need = recovery_sum / total
        avg_survival_pressure = survival_pressure_sum / total
        avg_pressure_release = pressure_release_sum / total
        avg_load_bearing_capacity = load_bearing_sum / total
        avg_state_stability = state_stability_sum / total
        avg_capacity_reserve = capacity_reserve_sum / total
        avg_recovery_balance = recovery_balance_sum / total
        avg_regulated_courage = regulated_courage_sum / total
        avg_courage_gap = courage_gap_sum / total
        avg_action_inhibition = action_inhibition_sum / total
        avg_action_clearance = action_clearance_sum / total
        regulation_before_action = regulation_before_action_sum / total
        observation_learning = self._refresh_observation_learning_summary()
        observation_open = int(observation_learning.get("open", 0) or 0)
        observation_resolved = int(observation_learning.get("resolved", 0) or 0)
        observation_saved_loss = int(observation_learning.get("saved_loss", 0) or 0)
        observation_missed_gain = int(observation_learning.get("missed_gain", 0) or 0)
        observation_neutral = int(observation_learning.get("neutral", 0) or 0)
        observation_low_count = int(observation_learning.get("low_observations", 0) or 0)
        observation_maturity_trust = float(observation_learning.get("maturity_trust", 0.0) or 0.0)
        observation_action_pressure = float(observation_learning.get("action_pressure", 0.0) or 0.0)

        context_quality = max(
            0.0,
            min(
                1.0,
                (mean_structure_quality * 0.28)
                + (zone_ratio * 0.12)
                + (fill_ratio * 0.08)
                + (avg_regulated_courage * 0.08)
                + (avg_action_clearance * 0.08)
                + (regulation_before_action * 0.08)
                + (observe_share * 0.03)
                + (replan_share * 0.03)
                + (avg_load_bearing_capacity * 0.08)
                + (avg_pressure_release * 0.05)
                + (avg_state_stability * 0.04)
                + (avg_capacity_reserve * 0.03)
                + (avg_recovery_balance * 0.03)
                - (min(1.0, avg_pressure_to_capacity / 2.0) * 0.06)
                - (avg_regulatory_load * 0.05)
                - (avg_recovery_need * 0.04)
                - (avg_survival_pressure * 0.04)
                - (avg_courage_gap * 0.04)
                - (avg_action_inhibition * 0.04)
                - (cancel_ratio * 0.03)
                - (timeout_ratio * 0.04)
            ),
        )

        overtrade_pressure = max(
            0.0,
            min(
                1.0,
                (attempt_density * 0.26)
                + ((1.0 - context_quality) * 0.18)
                + (blocked_ratio * 0.08)
                + (cancel_ratio * 0.06)
                + (timeout_ratio * 0.08)
                + (min(1.0, avg_pressure_to_capacity / 2.0) * 0.08)
                + (avg_regulatory_load * 0.08)
                + (avg_recovery_need * 0.05)
                + (avg_survival_pressure * 0.05)
                + (avg_action_inhibition * 0.04)
            ),
        )

        return {
            "recent_attempt_count": int(total),
            "attempt_density": float(attempt_density),
            "fill_ratio": float(fill_ratio),
            "blocked_ratio": float(blocked_ratio),
            "cancel_ratio": float(cancel_ratio),
            "timeout_ratio": float(timeout_ratio),
            "zone_ratio": float(zone_ratio),
            "mean_structure_quality": float(mean_structure_quality),
            "context_quality": float(context_quality),
            "overtrade_pressure": float(overtrade_pressure),
            "observe_share": float(observe_share),
            "replan_share": float(replan_share),
            "withheld_share": float(withheld_share),
            "pressure_to_capacity": float(avg_pressure_to_capacity),
            "regulatory_load": float(avg_regulatory_load),
            "action_capacity": float(avg_action_capacity),
            "recovery_need": float(avg_recovery_need),
            "survival_pressure": float(avg_survival_pressure),
            "pressure_release": float(avg_pressure_release),
            "load_bearing_capacity": float(avg_load_bearing_capacity),
            "state_stability": float(avg_state_stability),
            "capacity_reserve": float(avg_capacity_reserve),
            "recovery_balance": float(avg_recovery_balance),
            "regulated_courage": float(avg_regulated_courage),
            "courage_gap": float(avg_courage_gap),
            "action_inhibition": float(avg_action_inhibition),
            "action_clearance": float(avg_action_clearance),
            "regulation_before_action": float(regulation_before_action),
            "observation_learning_open": int(observation_open),
            "observation_learning_resolved": int(observation_resolved),
            "observation_saved_loss": int(observation_saved_loss),
            "observation_missed_gain": int(observation_missed_gain),
            "observation_neutral": int(observation_neutral),
            "observation_low_count": int(observation_low_count),
            "observation_maturity_trust": float(observation_maturity_trust),
            "observation_action_pressure": float(observation_action_pressure),
        }

    # ─────────────────────────────────────────────
    def on_attempt(self, *, status: str, context: dict = None):
        status_key = str(status or "").strip().lower()
        normalized_context = self._normalize_record_value(context or {})
        compact_context = self._compact_context(normalized_context)
        trade_plan = dict(compact_context.get("trade_plan", {}) or {})
        side = str(trade_plan.get("decision", "") or "").strip().upper()
        if side not in ("LONG", "SHORT"):
            side = "-"

        self.data["attempts"] = int(self.data.get("attempts", 0) or 0) + 1
        if side == "LONG":
            self.data["attempts_long"] = int(self.data.get("attempts_long", 0) or 0) + 1
        elif side == "SHORT":
            self.data["attempts_short"] = int(self.data.get("attempts_short", 0) or 0) + 1

        if status_key == "submitted":
            self.data["attempts_submitted"] = int(self.data.get("attempts_submitted", 0) or 0) + 1
            if side == "LONG":
                self.data["attempts_submitted_long"] = int(self.data.get("attempts_submitted_long", 0) or 0) + 1
            elif side == "SHORT":
                self.data["attempts_submitted_short"] = int(self.data.get("attempts_submitted_short", 0) or 0) + 1
        elif status_key == "filled":
            self.data["attempts_filled"] = int(self.data.get("attempts_filled", 0) or 0) + 1
            if side == "LONG":
                self.data["attempts_filled_long"] = int(self.data.get("attempts_filled_long", 0) or 0) + 1
            elif side == "SHORT":
                self.data["attempts_filled_short"] = int(self.data.get("attempts_filled_short", 0) or 0) + 1
        elif status_key == "cancelled":
            self.data["attempts_cancelled"] = int(self.data.get("attempts_cancelled", 0) or 0) + 1
        elif status_key == "timeout":
            self.data["attempts_timeout"] = int(self.data.get("attempts_timeout", 0) or 0) + 1
        elif status_key in ("blocked", "blocked_value_gate"):
            self.data["attempts_blocked"] = int(self.data.get("attempts_blocked", 0) or 0) + 1
        elif status_key == "skipped":
            self.data["attempts_skipped"] = int(self.data.get("attempts_skipped", 0) or 0) + 1
        elif status_key == "observed_only":
            self.data["attempts_observed"] = int(self.data.get("attempts_observed", 0) or 0) + 1
        elif status_key == "replanned":
            self.data["attempts_replanned"] = int(self.data.get("attempts_replanned", 0) or 0) + 1
        elif status_key == "withheld":
            self.data["attempts_withheld"] = int(self.data.get("attempts_withheld", 0) or 0) + 1

        structure_quality = self._extract_structure_quality(normalized_context)
        if structure_quality >= 0.55:
            self.data["attempt_structure_zone"] = int(self.data.get("attempt_structure_zone", 0) or 0) + 1
            structure_bucket = "zone"
        else:
            self.data["attempt_non_structure_zone"] = int(self.data.get("attempt_non_structure_zone", 0) or 0) + 1
            structure_bucket = "non_zone"

        self._register_observation_learning(
            status_key,
            normalized_context,
            structure_quality,
            structure_bucket,
        )

        attempt_record = self._build_attempt_record(
            status_key,
            normalized_context,
            structure_quality,
            structure_bucket,
        )

        field_state = dict(compact_context.get("field_state", {}) or {})
        experience_state = dict(compact_context.get("experience", {}) or {})
        meta_regulation_state = dict(compact_context.get("meta_regulation_state", {}) or {})
        regulation_snapshot = dict(compact_context.get("regulation_snapshot", {}) or {})
        state_after = dict(compact_context.get("state_after", {}) or {})

        snapshot_tension = dict(regulation_snapshot.get("tension", {}) or state_after.get("tension", {}) or {})
        snapshot_field = dict(regulation_snapshot.get("field", {}) or state_after.get("field", {}) or {})
        snapshot_experience = dict(regulation_snapshot.get("experience", {}) or state_after.get("experience", {}) or {})

        recent = list(self.data.get("recent_attempts", []) or [])
        recent.append(
            {
                "status": status_key or "unknown",
                "side": str(side),
                "structure_quality": float(structure_quality),
                "structure_bucket": structure_bucket,
                "pressure_to_capacity": float(field_state.get("pressure_to_capacity", snapshot_field.get("pressure_to_capacity", 0.0)) or 0.0),
                "regulatory_load": float(field_state.get("regulatory_load", snapshot_field.get("regulatory_load", 0.0)) or 0.0),
                "action_capacity": float(field_state.get("action_capacity", snapshot_field.get("action_capacity", 0.0)) or 0.0),
                "recovery_need": float(field_state.get("recovery_need", snapshot_field.get("recovery_need", 0.0)) or 0.0),
                "survival_pressure": float(field_state.get("survival_pressure", snapshot_field.get("survival_pressure", 0.0)) or 0.0),
                "pressure_release": float(experience_state.get("pressure_release", snapshot_experience.get("pressure_release", 0.0)) or 0.0),
                "load_bearing_capacity": float(experience_state.get("load_bearing_capacity", snapshot_experience.get("load_bearing_capacity", 0.0)) or 0.0),
                "state_stability": float(snapshot_tension.get("stability", 0.0) or 0.0),
                "capacity_reserve": float(field_state.get("capacity_reserve", snapshot_field.get("capacity_reserve", 0.0)) or 0.0),
                "recovery_balance": float(field_state.get("recovery_balance", snapshot_field.get("recovery_balance", 0.0)) or 0.0),
                "regulated_courage": float(meta_regulation_state.get("regulated_courage", 0.0) or 0.0),
                "courage_gap": float(meta_regulation_state.get("courage_gap", 0.0) or 0.0),
                "action_inhibition": float(meta_regulation_state.get("action_inhibition", 0.0) or 0.0),
                "action_clearance": float(meta_regulation_state.get("action_clearance", 0.0) or 0.0),
                "pre_action_phase": str(meta_regulation_state.get("pre_action_phase", "") or ""),
            }
        )
        self.data["recent_attempts"] = recent[-80:]
        if self._should_write_attempt_record(status_key):
            self._append_record_file(self.attempt_path, attempt_record)
        self._rebuild_kpi_summary()
        self._save()

    # ─────────────────────────────────────────────
    def on_exit(
        self,
        *,
        entry: float,
        tp: float,
        sl: float,
        reason: str,
        side: str = None,
        amount: float = 1.0,
        exit_price: float = None,
        exploration_trade: bool = False,
        outcome_decomposition: dict = None,
        context: dict = None,
    ):
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

        elif reason == "matured_exit":
            try:
                resolved_exit_price = float(exit_price)
            except Exception:
                return
            if resolved_exit_price <= 0.0:
                return
            if side == "LONG":
                pnl = (resolved_exit_price - entry) * float(amount)
            elif side == "SHORT":
                pnl = (entry - resolved_exit_price) * float(amount)
            else:
                return
            self.data["matured_exits"] = int(self.data.get("matured_exits", 0) or 0) + 1
            if pnl >= 0:
                self.data["tp"] += 1
                if exploration_trade:
                    self.data["exploration_tp"] = int(self.data.get("exploration_tp", 0) or 0) + 1
            else:
                self.data["sl"] += 1
                if exploration_trade:
                    self.data["exploration_sl"] = int(self.data.get("exploration_sl", 0) or 0) + 1

        else:
            return

        exit_price = float(exit_price) if reason == "matured_exit" else (tp if reason == "tp_hit" else sl)
        fee_rate = getattr(Config, "FEE_RATE", 0.0) or 0.0
        fees = (
            (entry * float(amount) * fee_rate) +
            (exit_price * float(amount) * fee_rate) +
            (Config.FEE_PER_TRADE or 0.0)
        )
        pnl = pnl - fees

        normalized_context = self._normalize_record_value(context or {})
        compact_context = self._compact_context(normalized_context)
        normalized_decomposition = self._normalize_record_value(outcome_decomposition or {})

        def _context_section(name: str) -> dict:
            for source in (
                normalized_context,
                compact_context,
                dict(normalized_context.get("context", {}) or {}),
                dict(compact_context.get("context", {}) or {}),
            ):
                value = source.get(name, {}) if isinstance(source, dict) else {}
                if isinstance(value, dict) and value:
                    return dict(value)
            return {}

        exit_candidate_replay = self._record_exit_candidate_replay(
            entry=float(entry),
            side=str(side),
            amount=float(amount),
            actual_reason=str(reason or ""),
            actual_exit_price=float(exit_price),
            actual_pnl=float(pnl),
            context=normalized_context,
        )

        self.data["trades"] += 1
        self.data["last_outcome_decomposition"] = dict(normalized_decomposition or {})
        if side == "LONG":
            self.data["long_trades"] = int(self.data.get("long_trades", 0) or 0) + 1
            self.data["long_pnl"] = float(self.data.get("long_pnl", 0.0) or 0.0) + float(pnl)
            if reason == "tp_hit" or (reason == "matured_exit" and pnl >= 0.0):
                self.data["long_tp"] = int(self.data.get("long_tp", 0) or 0) + 1
            elif reason == "sl_hit" or (reason == "matured_exit" and pnl < 0.0):
                self.data["long_sl"] = int(self.data.get("long_sl", 0) or 0) + 1
        elif side == "SHORT":
            self.data["short_trades"] = int(self.data.get("short_trades", 0) or 0) + 1
            self.data["short_pnl"] = float(self.data.get("short_pnl", 0.0) or 0.0) + float(pnl)
            if reason == "tp_hit" or (reason == "matured_exit" and pnl >= 0.0):
                self.data["short_tp"] = int(self.data.get("short_tp", 0) or 0) + 1
            elif reason == "sl_hit" or (reason == "matured_exit" and pnl < 0.0):
                self.data["short_sl"] = int(self.data.get("short_sl", 0) or 0) + 1

        if exploration_trade:
            self.data["exploration_trades"] = int(self.data.get("exploration_trades", 0) or 0) + 1
            self.data["exploration_pnl"] = float(self.data.get("exploration_pnl", 0.0) or 0.0) + float(pnl)

        self.data["pnl_netto"] = float(self.data.get("pnl_netto", 0.0) or 0.0) + float(pnl)
        self.data["current_equity"] = float(self.data.get("start_equity", 0.0) or 0.0) + float(self.data.get("pnl_netto", 0.0) or 0.0)
        self._sync_live_account_equity(reason="trade_exit")

        if pnl > 0:
            self.data["pnl_tp"] += pnl

        if pnl < 0:
            self.data["pnl_sl"] += pnl

        if reason == "matured_exit":
            self.data["matured_exit_pnl"] = float(self.data.get("matured_exit_pnl", 0.0) or 0.0) + float(pnl)

        structure_quality = self._extract_structure_quality(normalized_context)
        structure_bucket = "zone" if structure_quality >= 0.55 else "non_zone"
        form_symbol_state = _context_section("form_symbol_state")
        meta_regulation_state = _context_section("meta_regulation_state")
        neurochemical_state = _context_section("neurochemical_state") or dict(meta_regulation_state.get("neurochemical_state", {}) or {})
        active_mcm_contact_state = _context_section("active_mcm_contact_state") or dict(meta_regulation_state.get("active_mcm_contact", {}) or {})
        strategic_window_state = _context_section("strategic_window_state")
        trade_plan_state = _context_section("trade_plan")
        target_expectation_state = _context_section("target_expectation_state")
        thought_seed_state = _context_section("thought_seed_state")
        experience_state = _context_section("experience")
        experience_packet_feedback = dict(normalized_decomposition.get("experience_packet_feedback", {}) or {})

        def _f(*values, default=0.0):
            for value in values:
                try:
                    if value is None:
                        continue
                    return float(value)
                except Exception:
                    continue
            return float(default)

        def _clip(value):
            value = _f(value)
            if value != value:
                value = 0.0
            return max(0.0, min(1.0, float(value)))

        rr_value = _f(trade_plan_state.get("rr_value"), default=0.0)
        structural_run_room = _clip((rr_value - 1.6) / 3.2)
        target_expectation_value = _clip(
            target_expectation_state.get(
                "tp_reachability",
                target_expectation_state.get(
                    "base_target_expectation",
                    experience_state.get("target_expectation", 0.0),
                ),
            )
        )
        emergent_structure_reading = _clip(
            (structural_run_room * 0.24)
            + (_clip(meta_regulation_state.get("future_projection_depth", 0.0)) * 0.16)
            + (_clip(meta_regulation_state.get("mcm_spacetime_depth", 0.0)) * 0.14)
            + (_clip(strategic_window_state.get("area_bearing_quality", meta_regulation_state.get("area_bearing_quality", 0.0))) * 0.14)
            + (_clip(trade_plan_state.get("entry_choice_bearing", 0.0)) * 0.12)
            + (_clip(active_mcm_contact_state.get("contact_action_maturity", meta_regulation_state.get("contact_action_maturity", 0.0))) * 0.10)
            + (target_expectation_value * 0.10)
            - (_clip(meta_regulation_state.get("spacetime_unlocated_pressure", 0.0)) * 0.10)
            - (_clip(meta_regulation_state.get("contact_regime_mismatch", 0.0)) * 0.08)
        )
        emergent_structure_confirmation = _clip(
            (emergent_structure_reading * 0.42)
            + (_clip(normalized_decomposition.get("plan_quality", 0.0)) * 0.16)
            + (_clip(normalized_decomposition.get("execution_quality", 0.0)) * 0.14)
            + (_clip(normalized_decomposition.get("risk_fit_quality", 0.0)) * 0.12)
            + (_clip(normalized_decomposition.get("position_constructive_bearing", 0.0)) * 0.10)
            + (0.12 if reason == "tp_hit" and rr_value >= 2.4 else 0.0)
            - (0.10 if reason == "sl_hit" and rr_value >= 2.4 else 0.0)
        )
        if emergent_structure_reading >= 0.52 and emergent_structure_confirmation >= 0.50:
            emergent_structure_state = "confirmed_structural_interpretation"
        elif emergent_structure_reading >= 0.44 and rr_value >= 2.4:
            emergent_structure_state = "open_structural_hypothesis"
        elif rr_value >= 2.4 and emergent_structure_reading < 0.34:
            emergent_structure_state = "wide_target_without_structure"
        else:
            emergent_structure_state = "ordinary_structure_reading"
        open_hypothesis_learning = self._derive_open_hypothesis_learning(
            {
                "reason": str(reason or "").strip().lower(),
                "pnl": float(pnl),
                "rr_value": float(rr_value),
                "emergent_structure_reading": float(emergent_structure_reading),
                "emergent_structure_confirmation": float(emergent_structure_confirmation),
                "emergent_structure_state": str(emergent_structure_state),
                "thought_seed_structural_grounding": float(thought_seed_state.get("thought_structural_grounding", 0.0) or 0.0),
                "thought_seed_open_hypothesis_pressure": float(thought_seed_state.get("thought_open_hypothesis_pressure", 0.0) or 0.0),
                "thought_seed_reality_lag": float(thought_seed_state.get("thought_reality_lag", 0.0) or 0.0),
                "thought_seed_consequence_balance": float(thought_seed_state.get("thought_consequence_balance", 0.0) or 0.0),
            },
            emergent_state=str(emergent_structure_state),
        )
        normalized_decomposition.update({
            "emergent_structure_reading": float(emergent_structure_reading),
            "emergent_structure_confirmation": float(emergent_structure_confirmation),
            "emergent_structure_state": str(emergent_structure_state),
            "open_hypothesis_learning_state": str(open_hypothesis_learning.get("open_hypothesis_learning_state", "-") or "-"),
            "open_hypothesis_consequence_score": float(open_hypothesis_learning.get("open_hypothesis_consequence_score", 0.0) or 0.0),
            "open_hypothesis_burden_score": float(open_hypothesis_learning.get("open_hypothesis_burden_score", 0.0) or 0.0),
            "open_hypothesis_reorganization_score": float(open_hypothesis_learning.get("open_hypothesis_reorganization_score", 0.0) or 0.0),
            "open_hypothesis_replay_need": float(open_hypothesis_learning.get("open_hypothesis_replay_need", 0.0) or 0.0),
            "open_hypothesis_distance_need": float(open_hypothesis_learning.get("open_hypothesis_distance_need", 0.0) or 0.0),
            "open_hypothesis_reinterpretation_need": float(open_hypothesis_learning.get("open_hypothesis_reinterpretation_need", 0.0) or 0.0),
            "open_hypothesis_reorganization_posture": str(open_hypothesis_learning.get("open_hypothesis_reorganization_posture", "-") or "-"),
        })
        self.data["last_outcome_decomposition"] = dict(normalized_decomposition or {})

        outcome_record = {
            "event": "trade_exit",
            "reason": str(reason or "").strip().lower(),
            "timestamp": self.data.get("current_timestamp"),
            "side": side,
            "entry": float(entry),
            "tp": float(tp),
            "sl": float(sl),
            "exit_price": float(exit_price),
            "amount": float(amount),
            "pnl": float(pnl),
            "rr_value": float(rr_value),
            "structural_run_room": float(structural_run_room),
            "emergent_structure_reading": float(emergent_structure_reading),
            "emergent_structure_confirmation": float(emergent_structure_confirmation),
            "emergent_structure_state": str(emergent_structure_state),
            "open_hypothesis_learning_state": str(open_hypothesis_learning.get("open_hypothesis_learning_state", "-") or "-"),
            "open_hypothesis_consequence_score": float(open_hypothesis_learning.get("open_hypothesis_consequence_score", 0.0) or 0.0),
            "open_hypothesis_burden_score": float(open_hypothesis_learning.get("open_hypothesis_burden_score", 0.0) or 0.0),
            "open_hypothesis_reorganization_score": float(open_hypothesis_learning.get("open_hypothesis_reorganization_score", 0.0) or 0.0),
            "open_hypothesis_replay_need": float(open_hypothesis_learning.get("open_hypothesis_replay_need", 0.0) or 0.0),
            "open_hypothesis_distance_need": float(open_hypothesis_learning.get("open_hypothesis_distance_need", 0.0) or 0.0),
            "open_hypothesis_reinterpretation_need": float(open_hypothesis_learning.get("open_hypothesis_reinterpretation_need", 0.0) or 0.0),
            "open_hypothesis_reorganization_posture": str(open_hypothesis_learning.get("open_hypothesis_reorganization_posture", "-") or "-"),
            "thought_seed_id": str(thought_seed_state.get("thought_seed_id", "") or ""),
            "thought_seed_label": str(thought_seed_state.get("thought_seed_label", "") or ""),
            "thought_seed_metaregulator_state": str(thought_seed_state.get("seed_metaregulator_state", "") or ""),
            "thought_seed_emergent_state": str(thought_seed_state.get("emergent_structure_state", "") or ""),
            "thought_seed_trace_strength": float(thought_seed_state.get("thought_trace_strength", 0.0) or 0.0),
            "thought_seed_maturity": float(thought_seed_state.get("thought_maturity", 0.0) or 0.0),
            "thought_seed_reality_binding": float(thought_seed_state.get("reality_binding_score", 0.0) or 0.0),
            "thought_seed_confirmation": float(thought_seed_state.get("thought_confirmation_score", 0.0) or 0.0),
            "thought_seed_consequence_echo": float(thought_seed_state.get("consequence_echo", 0.0) or 0.0),
            "thought_seed_reorganization_echo": float(thought_seed_state.get("reorganization_echo", 0.0) or 0.0),
            "thought_seed_consequence_alignment": float(thought_seed_state.get("thought_consequence_alignment", 0.0) or 0.0),
            "thought_seed_consequence_balance": float(thought_seed_state.get("thought_consequence_balance", 0.0) or 0.0),
            "thought_seed_reality_lag": float(thought_seed_state.get("thought_reality_lag", 0.0) or 0.0),
            "thought_seed_structural_grounding": float(thought_seed_state.get("thought_structural_grounding", 0.0) or 0.0),
            "thought_seed_open_hypothesis_pressure": float(thought_seed_state.get("thought_open_hypothesis_pressure", 0.0) or 0.0),
            "thought_seed_replay_maturation_pull": float(thought_seed_state.get("thought_replay_maturation_pull", 0.0) or 0.0),
            "thought_seed_distance_maturation_pull": float(thought_seed_state.get("thought_distance_maturation_pull", 0.0) or 0.0),
            "thought_seed_reinterpretation_pull": float(thought_seed_state.get("thought_reinterpretation_pull", 0.0) or 0.0),
            "thought_seed_digestive_replay_pull": float(thought_seed_state.get("thought_digestive_replay_pull", 0.0) or 0.0),
            "thought_seed_digestive_distance_pull": float(thought_seed_state.get("thought_digestive_distance_pull", 0.0) or 0.0),
            "thought_seed_digestive_integration_pull": float(thought_seed_state.get("thought_digestive_integration_pull", 0.0) or 0.0),
            "thought_seed_digestive_returned_trust": float(thought_seed_state.get("thought_digestive_returned_trust", 0.0) or 0.0),
            "thought_seed_trust_return_readiness": float(thought_seed_state.get("trust_return_readiness", 0.0) or 0.0),
            "thought_seed_digest_state": str(thought_seed_state.get("thought_digest_state", "") or ""),
            "thought_seed_reifung_direction": str(thought_seed_state.get("thought_reifung_direction", "") or ""),
            "thought_seed_semantic_origin_state": str(thought_seed_state.get("semantic_origin_state", "") or ""),
            "thought_seed_borrowed_open_hypothesis_pressure": float(thought_seed_state.get("borrowed_open_hypothesis_pressure", 0.0) or 0.0),
            "thought_seed_own_field_binding_pull": float(thought_seed_state.get("own_field_binding_pull", 0.0) or 0.0),
            "semantic_origin_state": str(meta_regulation_state.get("semantic_origin_state", "") or ""),
            "own_field_identity_strength": float(meta_regulation_state.get("own_field_identity_strength", 0.0) or 0.0),
            "foreign_semantic_pressure": float(meta_regulation_state.get("foreign_semantic_pressure", 0.0) or 0.0),
            "adopted_language_pressure": float(meta_regulation_state.get("adopted_language_pressure", 0.0) or 0.0),
            "self_foreign_boundary_clarity": float(meta_regulation_state.get("self_foreign_boundary_clarity", 0.0) or 0.0),
            "semantic_origin_conflict": float(meta_regulation_state.get("semantic_origin_conflict", 0.0) or 0.0),
            "own_vs_foreign_margin": float(meta_regulation_state.get("own_vs_foreign_margin", 0.0) or 0.0),
            "borrowed_vs_own_margin": float(meta_regulation_state.get("borrowed_vs_own_margin", 0.0) or 0.0),
            "boundary_support_margin": float(meta_regulation_state.get("boundary_support_margin", 0.0) or 0.0),
            "thought_seed_drift_risk": float(thought_seed_state.get("hallucination_drift_risk", 0.0) or 0.0),
            "thought_seed_overthinking_risk": float(thought_seed_state.get("overthinking_risk", 0.0) or 0.0),
            "target_expectation_value": float(target_expectation_value),
            "structure_quality": float(structure_quality),
            "structure_bucket": structure_bucket,
            "form_symbol_id": str(form_symbol_state.get("form_symbol_id", "") or ""),
            "form_symbol_development_quality": float(form_symbol_state.get("form_symbol_development_quality", 0.0) or 0.0),
            "form_symbol_action_binding": float(form_symbol_state.get("form_symbol_action_binding", 0.0) or 0.0),
            "form_symbol_observation_binding": float(form_symbol_state.get("form_symbol_observation_binding", 0.0) or 0.0),
            "form_symbol_reframe_binding": float(form_symbol_state.get("form_symbol_reframe_binding", 0.0) or 0.0),
            "form_symbol_learning_trust": float(form_symbol_state.get("form_symbol_learning_trust", 0.0) or 0.0),
            "form_symbol_action_trust": float(form_symbol_state.get("form_symbol_action_trust", 0.0) or 0.0),
            "form_symbol_caution_trust": float(form_symbol_state.get("form_symbol_caution_trust", 0.0) or 0.0),
            "form_symbol_contact_maturity": float(form_symbol_state.get("form_symbol_contact_maturity", meta_regulation_state.get("form_symbol_contact_maturity", 0.0)) or 0.0),
            "form_symbol_contact_utility": float(form_symbol_state.get("form_symbol_contact_utility", meta_regulation_state.get("form_symbol_contact_utility", 0.0)) or 0.0),
            "form_symbol_contact_pain_memory": float(form_symbol_state.get("form_symbol_contact_pain_memory", meta_regulation_state.get("form_symbol_contact_pain_memory", 0.0)) or 0.0),
            "form_symbol_contact_carefulness": float(form_symbol_state.get("form_symbol_contact_carefulness", meta_regulation_state.get("form_symbol_contact_carefulness", 0.0)) or 0.0),
            "form_symbol_contact_burden_evidence": float(form_symbol_state.get("form_symbol_contact_burden_evidence", meta_regulation_state.get("form_symbol_contact_burden_evidence", 0.0)) or 0.0),
            "form_symbol_contact_utility_evidence": float(form_symbol_state.get("form_symbol_contact_utility_evidence", meta_regulation_state.get("form_symbol_contact_utility_evidence", 0.0)) or 0.0),
            "form_symbol_contact_learning_state": str(form_symbol_state.get("form_symbol_contact_learning_state", meta_regulation_state.get("form_symbol_contact_learning_state", "")) or ""),
            "form_contact_maturity_sample": float(normalized_decomposition.get("contact_maturity_sample", 0.0) or 0.0),
            "form_contact_utility_sample": float(normalized_decomposition.get("contact_utility_sample", 0.0) or 0.0),
            "form_contact_pain_sample": float(normalized_decomposition.get("contact_pain_sample", 0.0) or 0.0),
            "form_contact_carefulness_sample": float(normalized_decomposition.get("contact_carefulness_sample", 0.0) or 0.0),
            "form_contact_learning_state": str(normalized_decomposition.get("contact_learning_state", "") or ""),
            "position_consequence_burden": float(normalized_decomposition.get("position_consequence_burden", 0.0) or 0.0),
            "position_consequence_residual_for_care": float(normalized_decomposition.get("position_consequence_residual_for_care", 0.0) or 0.0),
            "position_consequence_residual_for_memory": float(normalized_decomposition.get("position_consequence_residual_for_memory", 0.0) or 0.0),
            "position_constructive_bearing": float(normalized_decomposition.get("position_constructive_bearing", 0.0) or 0.0),
            "transitional_contact_band": float(normalized_decomposition.get("transitional_contact_band", 0.0) or 0.0),
            "transitional_contact_maturation": float(normalized_decomposition.get("transitional_contact_maturation", 0.0) or 0.0),
            "position_feedback_label": str(normalized_decomposition.get("position_feedback_label", "") or ""),
            "position_process_quality_feedback": float(normalized_decomposition.get("position_process_quality", 0.0) or 0.0),
            "position_held_risk_discomfort_feedback": float(normalized_decomposition.get("position_held_risk_discomfort", 0.0) or 0.0),
            "position_cortisol_load_feedback": float(normalized_decomposition.get("position_cortisol_load", 0.0) or 0.0),
            "position_noradrenaline_arousal_feedback": float(normalized_decomposition.get("position_noradrenaline_arousal", 0.0) or 0.0),
            "form_symbol_compound_id": str(form_symbol_state.get("form_symbol_compound_id", "") or ""),
            "form_symbol_compound_development_quality": float(form_symbol_state.get("form_symbol_compound_development_quality", 0.0) or 0.0),
            "uncertain_form_family_state": str(form_symbol_state.get("uncertain_form_family_state", meta_regulation_state.get("uncertain_form_family_state", "")) or ""),
            "uncertain_form_exposure": float(form_symbol_state.get("uncertain_form_exposure", meta_regulation_state.get("uncertain_form_exposure", 0.0)) or 0.0),
            "uncertainty_familiarity": float(form_symbol_state.get("uncertainty_familiarity", meta_regulation_state.get("uncertainty_familiarity", 0.0)) or 0.0),
            "variant_similarity": float(form_symbol_state.get("variant_similarity", meta_regulation_state.get("variant_similarity", 0.0)) or 0.0),
            "variant_spread": float(form_symbol_state.get("variant_spread", meta_regulation_state.get("variant_spread", 0.0)) or 0.0),
            "variant_learning_pressure": float(form_symbol_state.get("variant_learning_pressure", meta_regulation_state.get("variant_learning_pressure", 0.0)) or 0.0),
            "variant_bearing_memory": float(form_symbol_state.get("variant_bearing_memory", meta_regulation_state.get("variant_bearing_memory", 0.0)) or 0.0),
            "form_symbol_semantic_density": float(form_symbol_state.get("form_symbol_semantic_density", 0.0) or 0.0),
            "form_symbol_semantic_compression": float(form_symbol_state.get("form_symbol_semantic_compression", 0.0) or 0.0),
            "form_symbol_semantic_coherence": float(form_symbol_state.get("form_symbol_semantic_coherence", 0.0) or 0.0),
            "form_symbol_semantic_learning_need": float(form_symbol_state.get("form_symbol_semantic_learning_need", 0.0) or 0.0),
            "form_symbol_semantic_action_nearness": float(form_symbol_state.get("form_symbol_semantic_action_nearness", 0.0) or 0.0),
            "form_symbol_semantic_primary_layer": str(form_symbol_state.get("form_symbol_semantic_primary_layer", "") or ""),
            "form_symbol_semantic_layer_count": int(form_symbol_state.get("form_symbol_semantic_layer_count", 0) or 0),
            "form_symbol_semantic_packet_state": str(form_symbol_state.get("form_symbol_semantic_packet_state", "") or ""),
            "form_symbol_semantic_profile": str(form_symbol_state.get("form_symbol_semantic_profile", "") or ""),
            "visual_blind_action_load": float(meta_regulation_state.get("visual_blind_action_load", 0.0) or 0.0),
            "visual_action_uncertainty": float(meta_regulation_state.get("visual_action_uncertainty", 0.0) or 0.0),
            "visual_object_binding": float(meta_regulation_state.get("visual_object_binding", 0.0) or 0.0),
            "visual_grounding_strength": float(meta_regulation_state.get("visual_grounding_strength", 0.0) or 0.0),
            "visual_resonance_unbound": float(meta_regulation_state.get("visual_resonance_unbound", 0.0) or 0.0),
            "visual_grounding_gap": float(meta_regulation_state.get("visual_grounding_gap", 0.0) or 0.0),
            "visual_grounding_need": float(meta_regulation_state.get("visual_grounding_need", 0.0) or 0.0),
            "visual_rational_observation_support": float(meta_regulation_state.get("visual_rational_observation_support", 0.0) or 0.0),
            "visual_grounding_state": str(meta_regulation_state.get("visual_grounding_state", "") or ""),
            "neurochemical_state_label": str(neurochemical_state.get("neurochemical_state_label", meta_regulation_state.get("neurochemical_state_label", "")) or ""),
            "neurochemical_dominant_tone": str(neurochemical_state.get("neurochemical_dominant_tone", meta_regulation_state.get("neurochemical_dominant_tone", "")) or ""),
            "dopamine_tone": float(neurochemical_state.get("dopamine_tone", meta_regulation_state.get("dopamine_tone", 0.0)) or 0.0),
            "gaba_inhibition": float(neurochemical_state.get("gaba_inhibition", meta_regulation_state.get("gaba_inhibition", 0.0)) or 0.0),
            "noradrenaline_arousal": float(neurochemical_state.get("noradrenaline_arousal", meta_regulation_state.get("noradrenaline_arousal", 0.0)) or 0.0),
            "acetylcholine_focus": float(neurochemical_state.get("acetylcholine_focus", meta_regulation_state.get("acetylcholine_focus", 0.0)) or 0.0),
            "serotonin_stability": float(neurochemical_state.get("serotonin_stability", meta_regulation_state.get("serotonin_stability", 0.0)) or 0.0),
            "cortisol_load": float(neurochemical_state.get("cortisol_load", meta_regulation_state.get("cortisol_load", 0.0)) or 0.0),
            "endorphin_relief": float(neurochemical_state.get("endorphin_relief", meta_regulation_state.get("endorphin_relief", 0.0)) or 0.0),
            "glutamate_activation": float(neurochemical_state.get("glutamate_activation", meta_regulation_state.get("glutamate_activation", 0.0)) or 0.0),
            "neurochemical_load": float(neurochemical_state.get("neurochemical_load", meta_regulation_state.get("neurochemical_load", 0.0)) or 0.0),
            "neurochemical_support": float(neurochemical_state.get("neurochemical_support", meta_regulation_state.get("neurochemical_support", 0.0)) or 0.0),
            "neurochemical_balance": float(neurochemical_state.get("neurochemical_balance", meta_regulation_state.get("neurochemical_balance", 0.0)) or 0.0),
            "reward_stability_echo": float(neurochemical_state.get("reward_stability_echo", meta_regulation_state.get("reward_stability_echo", 0.0)) or 0.0),
            "world_shift_evidence": float(neurochemical_state.get("world_shift_evidence", meta_regulation_state.get("world_shift_evidence", 0.0)) or 0.0),
            "serotonin_carryover_risk": float(neurochemical_state.get("serotonin_carryover_risk", meta_regulation_state.get("serotonin_carryover_risk", 0.0)) or 0.0),
            "emotional_decoupling": float(neurochemical_state.get("emotional_decoupling", meta_regulation_state.get("emotional_decoupling", 0.0)) or 0.0),
            "reactive_nervous_drive": float(neurochemical_state.get("reactive_nervous_drive", meta_regulation_state.get("reactive_nervous_drive", 0.0)) or 0.0),
            "active_mcm_contact_state": str(active_mcm_contact_state.get("active_mcm_contact_state", meta_regulation_state.get("active_mcm_contact_state", "")) or ""),
            "contact_posture": str(active_mcm_contact_state.get("contact_posture", meta_regulation_state.get("contact_posture", "")) or ""),
            "contact_interest": float(active_mcm_contact_state.get("contact_interest", meta_regulation_state.get("contact_interest", 0.0)) or 0.0),
            "contact_focus_pull": float(active_mcm_contact_state.get("contact_focus_pull", meta_regulation_state.get("contact_focus_pull", 0.0)) or 0.0),
            "contact_resonance_probe": float(active_mcm_contact_state.get("contact_resonance_probe", meta_regulation_state.get("contact_resonance_probe", 0.0)) or 0.0),
            "outer_inner_resonance": float(active_mcm_contact_state.get("outer_inner_resonance", meta_regulation_state.get("outer_inner_resonance", 0.0)) or 0.0),
            "outer_inner_coherence": float(active_mcm_contact_state.get("outer_inner_coherence", meta_regulation_state.get("outer_inner_coherence", 0.0)) or 0.0),
            "inner_change_from_contact": float(active_mcm_contact_state.get("inner_change_from_contact", meta_regulation_state.get("inner_change_from_contact", 0.0)) or 0.0),
            "contact_carrying_quality": float(active_mcm_contact_state.get("contact_carrying_quality", meta_regulation_state.get("contact_carrying_quality", 0.0)) or 0.0),
            "contact_overcoupling_risk": float(active_mcm_contact_state.get("contact_overcoupling_risk", meta_regulation_state.get("contact_overcoupling_risk", 0.0)) or 0.0),
            "contact_release_readiness": float(active_mcm_contact_state.get("contact_release_readiness", meta_regulation_state.get("contact_release_readiness", 0.0)) or 0.0),
            "contact_deepen_pull": float(active_mcm_contact_state.get("contact_deepen_pull", meta_regulation_state.get("contact_deepen_pull", 0.0)) or 0.0),
            "contact_replay_pull": float(active_mcm_contact_state.get("contact_replay_pull", meta_regulation_state.get("contact_replay_pull", 0.0)) or 0.0),
            "contact_curiosity": float(active_mcm_contact_state.get("contact_curiosity", meta_regulation_state.get("contact_curiosity", 0.0)) or 0.0),
            "contact_felt_shift": float(active_mcm_contact_state.get("contact_felt_shift", meta_regulation_state.get("contact_felt_shift", 0.0)) or 0.0),
            "contact_selected_depth": float(active_mcm_contact_state.get("contact_selected_depth", meta_regulation_state.get("contact_selected_depth", 0.0)) or 0.0),
            "contact_salience": float(active_mcm_contact_state.get("contact_salience", meta_regulation_state.get("contact_salience", 0.0)) or 0.0),
            "overcoupled_touch_score": float(active_mcm_contact_state.get("overcoupled_touch_score", meta_regulation_state.get("overcoupled_touch_score", 0.0)) or 0.0),
            "release_contact_score": float(active_mcm_contact_state.get("release_contact_score", meta_regulation_state.get("release_contact_score", 0.0)) or 0.0),
            "deepening_contact_score": float(active_mcm_contact_state.get("deepening_contact_score", meta_regulation_state.get("deepening_contact_score", 0.0)) or 0.0),
            "resonant_contact_score": float(active_mcm_contact_state.get("resonant_contact_score", meta_regulation_state.get("resonant_contact_score", 0.0)) or 0.0),
            "reflective_contact_score": float(active_mcm_contact_state.get("reflective_contact_score", meta_regulation_state.get("reflective_contact_score", 0.0)) or 0.0),
            "curious_touch_score": float(active_mcm_contact_state.get("curious_touch_score", meta_regulation_state.get("curious_touch_score", 0.0)) or 0.0),
            "contact_action_maturity": float(active_mcm_contact_state.get("contact_action_maturity", meta_regulation_state.get("contact_action_maturity", 0.0)) or 0.0),
            "contact_bearing_gap": float(active_mcm_contact_state.get("contact_bearing_gap", meta_regulation_state.get("contact_bearing_gap", 0.0)) or 0.0),
            "contact_impulse_vs_bearing": float(active_mcm_contact_state.get("contact_impulse_vs_bearing", meta_regulation_state.get("contact_impulse_vs_bearing", 0.0)) or 0.0),
            "contact_learning_need": float(active_mcm_contact_state.get("contact_learning_need", meta_regulation_state.get("contact_learning_need", 0.0)) or 0.0),
            "contact_reality_check": float(active_mcm_contact_state.get("contact_reality_check", meta_regulation_state.get("contact_reality_check", 0.0)) or 0.0),
            "contact_regime_mismatch": float(active_mcm_contact_state.get("contact_regime_mismatch", meta_regulation_state.get("contact_regime_mismatch", 0.0)) or 0.0),
            "contact_stability_carryover": float(active_mcm_contact_state.get("contact_stability_carryover", meta_regulation_state.get("contact_stability_carryover", 0.0)) or 0.0),
            "contact_context_maturity": float(active_mcm_contact_state.get("contact_context_maturity", meta_regulation_state.get("contact_context_maturity", 0.0)) or 0.0),
            "contact_context_reframe_need": float(active_mcm_contact_state.get("contact_context_reframe_need", meta_regulation_state.get("contact_context_reframe_need", 0.0)) or 0.0),
            "conscious_perception_state": str(meta_regulation_state.get("conscious_perception_state", "") or ""),
            "inner_posture_state": str(meta_regulation_state.get("inner_posture_state", "") or ""),
            "arousal_load": float(meta_regulation_state.get("arousal_load", 0.0) or 0.0),
            "curiosity_tone": float(meta_regulation_state.get("curiosity_tone", 0.0) or 0.0),
            "fatigue_tone": float(meta_regulation_state.get("fatigue_tone", 0.0) or 0.0),
            "calm_tone": float(meta_regulation_state.get("calm_tone", 0.0) or 0.0),
            "stimulus_field_effect": float(meta_regulation_state.get("stimulus_field_effect", 0.0) or 0.0),
            "inner_impact_trace": float(meta_regulation_state.get("inner_impact_trace", 0.0) or 0.0),
            "perceived_field_change": float(meta_regulation_state.get("perceived_field_change", 0.0) or 0.0),
            "felt_afterimage": float(meta_regulation_state.get("felt_afterimage", 0.0) or 0.0),
            "object_release_state": str(meta_regulation_state.get("object_release_state", "") or ""),
            "inner_outer_reflection": float(meta_regulation_state.get("inner_outer_reflection", 0.0) or 0.0),
            "perceptual_distance": float(meta_regulation_state.get("perceptual_distance", 0.0) or 0.0),
            "object_contact_depth": float(meta_regulation_state.get("object_contact_depth", 0.0) or 0.0),
            "field_attachment": float(meta_regulation_state.get("field_attachment", 0.0) or 0.0),
            "release_capacity": float(meta_regulation_state.get("release_capacity", 0.0) or 0.0),
            "selective_attention": float(meta_regulation_state.get("selective_attention", 0.0) or 0.0),
            "background_containment": float(meta_regulation_state.get("background_containment", 0.0) or 0.0),
            "reflective_distance": float(meta_regulation_state.get("reflective_distance", 0.0) or 0.0),
            "inner_outer_alignment": float(meta_regulation_state.get("inner_outer_alignment", 0.0) or 0.0),
            "engaged_effort": float(meta_regulation_state.get("engaged_effort", 0.0) or 0.0),
            "effort_state": str(meta_regulation_state.get("effort_state", "") or ""),
            "effort_learning_pull": float(meta_regulation_state.get("effort_learning_pull", 0.0) or 0.0),
            "effort_reorganization_pressure": float(meta_regulation_state.get("effort_reorganization_pressure", 0.0) or 0.0),
            "pre_action_reorganization_pressure": float(meta_regulation_state.get("pre_action_reorganization_pressure", 0.0) or 0.0),
            "pre_action_context_selectivity": float(meta_regulation_state.get("pre_action_context_selectivity", 0.0) or 0.0),
            "previous_packet_label": str(meta_regulation_state.get("previous_packet_label", "") or ""),
            "previous_packet_process_reward": float(meta_regulation_state.get("previous_packet_process_reward", 0.0) or 0.0),
            "previous_packet_reorganization_need": float(meta_regulation_state.get("previous_packet_reorganization_need", 0.0) or 0.0),
            "diffuse_open_development_pressure": float(meta_regulation_state.get("diffuse_open_development_pressure", 0.0) or 0.0),
            "posture_development_hint": str(meta_regulation_state.get("posture_development_hint", "") or ""),
            "metaregulator_state": str(meta_regulation_state.get("metaregulator_state", "") or ""),
            "metaregulator_balance": float(meta_regulation_state.get("metaregulator_balance", 0.0) or 0.0),
            "regulatory_second_order_load": float(meta_regulation_state.get("regulatory_second_order_load", 0.0) or 0.0),
            "subconscious_field_pressure": float(meta_regulation_state.get("subconscious_field_pressure", 0.0) or 0.0),
            "subconscious_habituation": float(meta_regulation_state.get("subconscious_habituation", 0.0) or 0.0),
            "subconscious_filter_strength": float(meta_regulation_state.get("subconscious_filter_strength", 0.0) or 0.0),
            "subconscious_buffering": float(meta_regulation_state.get("subconscious_buffering", 0.0) or 0.0),
            "subconscious_leakage": float(meta_regulation_state.get("subconscious_leakage", 0.0) or 0.0),
            "subconscious_afterimage_depth": float(meta_regulation_state.get("subconscious_afterimage_depth", 0.0) or 0.0),
            "subconscious_afterimage_pressure": float(meta_regulation_state.get("subconscious_afterimage_pressure", 0.0) or 0.0),
            "subconscious_afterimage_bearing": float(meta_regulation_state.get("subconscious_afterimage_bearing", 0.0) or 0.0),
            "subconscious_afterimage_clarity": float(meta_regulation_state.get("subconscious_afterimage_clarity", 0.0) or 0.0),
            "subconscious_afterimage_release": float(meta_regulation_state.get("subconscious_afterimage_release", 0.0) or 0.0),
            "subconscious_afterimage_reflection_pull": float(meta_regulation_state.get("subconscious_afterimage_reflection_pull", 0.0) or 0.0),
            "conscious_selection_pressure": float(meta_regulation_state.get("conscious_selection_pressure", 0.0) or 0.0),
            "conscious_workspace_focus": float(meta_regulation_state.get("conscious_workspace_focus", 0.0) or 0.0),
            "conscious_workspace_load": float(meta_regulation_state.get("conscious_workspace_load", 0.0) or 0.0),
            "conscious_gate_balance": float(meta_regulation_state.get("conscious_gate_balance", 0.0) or 0.0),
            "integration_strain_value": float(meta_regulation_state.get("integration_strain_value", 0.0) or 0.0),
            "integration_sorting_need": float(meta_regulation_state.get("integration_sorting_need", 0.0) or 0.0),
            "integration_reframe_pull": float(meta_regulation_state.get("integration_reframe_pull", 0.0) or 0.0),
            "integration_memory_recall": float(meta_regulation_state.get("integration_memory_recall", 0.0) or 0.0),
            "integration_contact_deepening": float(meta_regulation_state.get("integration_contact_deepening", 0.0) or 0.0),
            "integration_response_strength": float(meta_regulation_state.get("integration_response_strength", 0.0) or 0.0),
            "integration_response_state": str(meta_regulation_state.get("integration_response_state", "") or ""),
            "cautious_hypothesis_strength": float(meta_regulation_state.get("cautious_hypothesis_strength", 0.0) or 0.0),
            "cautious_hypothesis_clarity": float(meta_regulation_state.get("cautious_hypothesis_clarity", 0.0) or 0.0),
            "cautious_hypothesis_patience": float(meta_regulation_state.get("cautious_hypothesis_patience", 0.0) or 0.0),
            "cautious_hypothesis_state": str(meta_regulation_state.get("cautious_hypothesis_state", "") or ""),
            "temporal_binding_state": str(meta_regulation_state.get("temporal_binding_state", "") or ""),
            "temporal_continuity": float(meta_regulation_state.get("temporal_continuity", 0.0) or 0.0),
            "temporal_source_binding": float(meta_regulation_state.get("temporal_source_binding", 0.0) or 0.0),
            "temporal_recurrence": float(meta_regulation_state.get("temporal_recurrence", 0.0) or 0.0),
            "temporal_novelty": float(meta_regulation_state.get("temporal_novelty", 0.0) or 0.0),
            "temporal_afterimage": float(meta_regulation_state.get("temporal_afterimage", 0.0) or 0.0),
            "temporal_decay": float(meta_regulation_state.get("temporal_decay", 0.0) or 0.0),
            "temporal_context_depth": float(meta_regulation_state.get("temporal_context_depth", 0.0) or 0.0),
            "mcm_spacetime_depth": float(meta_regulation_state.get("mcm_spacetime_depth", 0.0) or 0.0),
            "memory_experience_depth": float(meta_regulation_state.get("memory_experience_depth", 0.0) or 0.0),
            "future_projection_depth": float(meta_regulation_state.get("future_projection_depth", 0.0) or 0.0),
            "temporal_self_location": float(meta_regulation_state.get("temporal_self_location", 0.0) or 0.0),
            "temporal_self_location_state": str(meta_regulation_state.get("temporal_self_location_state", "") or ""),
            "spacetime_unlocated_pressure": float(meta_regulation_state.get("spacetime_unlocated_pressure", 0.0) or 0.0),
            "spacetime_memory_bearing": float(meta_regulation_state.get("spacetime_memory_bearing", 0.0) or 0.0),
            "spacetime_future_bearing": float(meta_regulation_state.get("spacetime_future_bearing", 0.0) or 0.0),
            "spacetime_reflection_need": float(meta_regulation_state.get("spacetime_reflection_need", 0.0) or 0.0),
            "spacetime_regulation_support": float(meta_regulation_state.get("spacetime_regulation_support", 0.0) or 0.0),
            "spacetime_regulation_state": str(meta_regulation_state.get("spacetime_regulation_state", "") or ""),
            "temporal_self_consistency": float(meta_regulation_state.get("temporal_self_consistency", 0.0) or 0.0),
            "perception_sequence_coherence": float(meta_regulation_state.get("perception_sequence_coherence", 0.0) or 0.0),
            "memory_time_distance": float(meta_regulation_state.get("memory_time_distance", 1.0) or 1.0),
            "return_strength": float(meta_regulation_state.get("return_strength", 0.0) or 0.0),
            "integration_capacity": float(meta_regulation_state.get("integration_capacity", 0.0) or 0.0),
            "variance_regulation": float(meta_regulation_state.get("variance_regulation", 0.0) or 0.0),
            "load_tolerance": float(meta_regulation_state.get("load_tolerance", 0.0) or 0.0),
            "impulse_control": float(meta_regulation_state.get("impulse_control", 0.0) or 0.0),
            "frustration_tolerance": float(meta_regulation_state.get("frustration_tolerance", 0.0) or 0.0),
            "protective_distance_regulation": float(meta_regulation_state.get("protective_distance_regulation", 0.0) or 0.0),
            "self_reflection_regulator": float(meta_regulation_state.get("self_reflection_regulator", 0.0) or 0.0),
            "distance_regulation": float(meta_regulation_state.get("distance_regulation", 0.0) or 0.0),
            "experience_packet_label": str(experience_packet_feedback.get("experience_packet_label", normalized_decomposition.get("experience_packet_label", "")) or ""),
            "packet_bearing_quality": float(experience_packet_feedback.get("packet_bearing_quality", normalized_decomposition.get("packet_bearing_quality", 0.0)) or 0.0),
            "packet_inner_outer_fit": float(experience_packet_feedback.get("packet_inner_outer_fit", normalized_decomposition.get("packet_inner_outer_fit", 0.0)) or 0.0),
            "packet_confidence_integrity": float(experience_packet_feedback.get("packet_confidence_integrity", normalized_decomposition.get("packet_confidence_integrity", 0.0)) or 0.0),
            "packet_repetition_potential": float(experience_packet_feedback.get("packet_repetition_potential", normalized_decomposition.get("packet_repetition_potential", 0.0)) or 0.0),
            "packet_curiosity_pull": float(experience_packet_feedback.get("packet_curiosity_pull", normalized_decomposition.get("packet_curiosity_pull", 0.0)) or 0.0),
            "packet_process_reward": float(experience_packet_feedback.get("packet_process_reward", normalized_decomposition.get("packet_process_reward", 0.0)) or 0.0),
            "packet_reorganization_need": float(experience_packet_feedback.get("packet_reorganization_need", normalized_decomposition.get("packet_reorganization_need", 0.0)) or 0.0),
            "constructive_stimulation": float(experience_packet_feedback.get("constructive_stimulation", normalized_decomposition.get("constructive_stimulation", 0.0)) or 0.0),
            "constructive_dopamine": float(experience_packet_feedback.get("constructive_dopamine", normalized_decomposition.get("constructive_dopamine", 0.0)) or 0.0),
            "stabilizing_serotonin": float(experience_packet_feedback.get("stabilizing_serotonin", normalized_decomposition.get("stabilizing_serotonin", 0.0)) or 0.0),
            "relief_endorphin": float(experience_packet_feedback.get("relief_endorphin", normalized_decomposition.get("relief_endorphin", 0.0)) or 0.0),
            "focused_acetylcholine": float(experience_packet_feedback.get("focused_acetylcholine", normalized_decomposition.get("focused_acetylcholine", 0.0)) or 0.0),
            "exit_candidate_replay": self._normalize_record_value(exit_candidate_replay or {}),
            "outcome_decomposition": normalized_decomposition,
            "context": compact_context,
        }

        self._append_record_file(self.outcome_path, outcome_record)

        current_equity = float(self.data.get("current_equity", self.data.get("start_equity", 0.0)) or 0.0)
        equity_peak = max(
            float(self.data.get("equity_peak", self.data.get("start_equity", 0.0)) or self.data.get("start_equity", 0.0)),
            float(current_equity),
        )
        self.data["equity_peak"] = float(equity_peak)

        drawdown_abs = max(0.0, equity_peak - float(current_equity))
        drawdown_pct = (drawdown_abs / equity_peak) if equity_peak > 0.0 else 0.0

        self.data["max_drawdown_abs"] = float(max(float(self.data.get("max_drawdown_abs", 0.0) or 0.0), drawdown_abs))
        self.data["max_drawdown_pct"] = float(max(float(self.data.get("max_drawdown_pct", 0.0) or 0.0), drawdown_pct))

        self._rebuild_kpi_summary()
        self._save(force=True)

        try:
            os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)

            header_key = f"_csv_header_written::{self.csv_path}"
            write_header = (not os.path.exists(self.csv_path)) and not bool(getattr(self, header_key, False))
            payload = ""
            if write_header:
                payload += "trade,current_equity,pnl_netto,pnl_tp,pnl_sl\n"
                setattr(self, header_key, True)
            payload += (
                f"{self.data['trades']},"
                f"{self.data.get('current_equity', self.data.get('start_equity', 0.0))},"
                f"{self.data['pnl_netto']},"
                f"{self.data['pnl_tp']},"
                f"{self.data['pnl_sl']}\n"
            )
            dbr_append_text(self.csv_path, payload, operation="trade_equity_csv_append")
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

        self._rebuild_kpi_summary()
        kpi_summary = dict(self.data.get("kpi_summary", {}) or {})
        proof = dict(kpi_summary.get("proof", {}) or {})

        data.pop("attempt_records", None)
        data.pop("outcome_records", None)

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
            "attempt_density": float(proof.get("attempt_density", 0.0) or 0.0),
            "context_quality": float(proof.get("context_quality", 0.0) or 0.0),
            "overtrade_pressure": float(proof.get("overtrade_pressure", 0.0) or 0.0),
            "observe_share": float(proof.get("observe_share", 0.0) or 0.0),
            "replan_share": float(proof.get("replan_share", 0.0) or 0.0),
            "withheld_share": float(proof.get("withheld_share", 0.0) or 0.0),
            "pressure_to_capacity": float(proof.get("pressure_to_capacity", 0.0) or 0.0),
            "recovery_need": float(proof.get("recovery_need", 0.0) or 0.0),
            "regulated_courage": float(proof.get("regulated_courage", 0.0) or 0.0),
            "courage_gap": float(proof.get("courage_gap", 0.0) or 0.0),
            "action_inhibition": float(proof.get("action_inhibition", 0.0) or 0.0),
            "action_clearance": float(proof.get("action_clearance", 0.0) or 0.0),
            "regulation_before_action": float(proof.get("regulation_before_action", 0.0) or 0.0),
            "max_drawdown_abs": float(proof.get("max_drawdown_abs", 0.0) or 0.0),
            "max_drawdown_pct": float(proof.get("max_drawdown_pct", 0.0) or 0.0),
            "kpi_summary": kpi_summary,
        })

        return data
    
    # ───────────────────────────────────────────── 
    def on_cancel(self, *, order_id=None, cause: str = None, exploration_trade: bool = False, outcome_decomposition: dict = None, context: dict = None):
        """
        Order wurde gecancelt bevor ein Trade/Exit stattgefunden hat.
        Keine PnL-Änderung – nur Zählung.
        """
        try:
            normalized_context = self._normalize_record_value(context or {})
            normalized_decomposition = self._normalize_record_value(outcome_decomposition or {})
            structure_quality = self._extract_structure_quality(normalized_context)
            structure_bucket = "zone" if structure_quality >= 0.55 else "non_zone"

            self.data["cancels"] = int(self.data.get("cancels", 0) or 0) + 1
            self.data["last_outcome_decomposition"] = dict(normalized_decomposition or {})
            if exploration_trade:
                self.data["exploration_cancels"] = int(self.data.get("exploration_cancels", 0) or 0) + 1

            compact_context = self._compact_context(normalized_context)
            trade_plan_state = dict(compact_context.get("trade_plan", {}) or {})
            meta_regulation_state = dict(compact_context.get("meta_regulation_state", {}) or {})
            active_mcm_contact_state = dict(compact_context.get("active_mcm_contact_state", meta_regulation_state.get("active_mcm_contact", {}) or {}) or {})
            target_expectation_state = dict(compact_context.get("target_expectation_state", {}) or {})
            thought_seed_state = dict(compact_context.get("thought_seed_state", {}) or {})

            def _f(*values, default=0.0):
                for value in values:
                    try:
                        if value is None:
                            continue
                        return float(value)
                    except Exception:
                        continue
                return float(default)

            def _clip(value):
                value = _f(value)
                if value != value:
                    value = 0.0
                return max(0.0, min(1.0, float(value)))

            rr_value = _f(trade_plan_state.get("rr_value"), default=0.0)
            structural_run_room = _clip((rr_value - 1.6) / 3.2)
            target_expectation_value = _clip(
                target_expectation_state.get(
                    "tp_reachability",
                    target_expectation_state.get("base_target_expectation", 0.0),
                )
            )
            emergent_structure_reading = _clip(
                (structural_run_room * 0.24)
                + (_clip(meta_regulation_state.get("future_projection_depth", 0.0)) * 0.16)
                + (_clip(meta_regulation_state.get("mcm_spacetime_depth", 0.0)) * 0.14)
                + (_clip(meta_regulation_state.get("area_bearing_quality", 0.0)) * 0.14)
                + (_clip(trade_plan_state.get("entry_choice_bearing", 0.0)) * 0.12)
                + (_clip(active_mcm_contact_state.get("contact_action_maturity", meta_regulation_state.get("contact_action_maturity", 0.0))) * 0.10)
                + (target_expectation_value * 0.10)
                - (_clip(meta_regulation_state.get("spacetime_unlocated_pressure", 0.0)) * 0.10)
                - (_clip(meta_regulation_state.get("contact_regime_mismatch", 0.0)) * 0.08)
            )
            emergent_structure_confirmation = _clip(
                (emergent_structure_reading * 0.42)
                + (_clip(normalized_decomposition.get("plan_quality", 0.0)) * 0.16)
                + (_clip(normalized_decomposition.get("execution_quality", 0.0)) * 0.14)
                + (_clip(normalized_decomposition.get("risk_fit_quality", 0.0)) * 0.12)
                + (_clip(normalized_decomposition.get("position_constructive_bearing", 0.0)) * 0.10)
            )
            if emergent_structure_reading >= 0.52 and emergent_structure_confirmation >= 0.50:
                emergent_structure_state = "confirmed_structural_interpretation"
            elif emergent_structure_reading >= 0.44 and rr_value >= 2.4:
                emergent_structure_state = "open_structural_hypothesis"
            elif rr_value >= 2.4 and emergent_structure_reading < 0.34:
                emergent_structure_state = "wide_target_without_structure"
            else:
                emergent_structure_state = "ordinary_structure_reading"
            open_hypothesis_learning = self._derive_open_hypothesis_learning(
                {
                    "reason": "cancel",
                    "pnl": 0.0,
                    "rr_value": float(rr_value),
                    "emergent_structure_reading": float(emergent_structure_reading),
                    "emergent_structure_confirmation": float(emergent_structure_confirmation),
                    "emergent_structure_state": str(emergent_structure_state),
                    "thought_seed_structural_grounding": float(thought_seed_state.get("thought_structural_grounding", 0.0) or 0.0),
                    "thought_seed_open_hypothesis_pressure": float(thought_seed_state.get("thought_open_hypothesis_pressure", 0.0) or 0.0),
                    "thought_seed_reality_lag": float(thought_seed_state.get("thought_reality_lag", 0.0) or 0.0),
                    "thought_seed_consequence_balance": float(thought_seed_state.get("thought_consequence_balance", 0.0) or 0.0),
                },
                emergent_state=str(emergent_structure_state),
            )
            normalized_decomposition.update({
                "emergent_structure_reading": float(emergent_structure_reading),
                "emergent_structure_confirmation": float(emergent_structure_confirmation),
                "emergent_structure_state": str(emergent_structure_state),
                "open_hypothesis_learning_state": str(open_hypothesis_learning.get("open_hypothesis_learning_state", "-") or "-"),
                "open_hypothesis_consequence_score": float(open_hypothesis_learning.get("open_hypothesis_consequence_score", 0.0) or 0.0),
                "open_hypothesis_burden_score": float(open_hypothesis_learning.get("open_hypothesis_burden_score", 0.0) or 0.0),
                "open_hypothesis_reorganization_score": float(open_hypothesis_learning.get("open_hypothesis_reorganization_score", 0.0) or 0.0),
                "open_hypothesis_replay_need": float(open_hypothesis_learning.get("open_hypothesis_replay_need", 0.0) or 0.0),
                "open_hypothesis_distance_need": float(open_hypothesis_learning.get("open_hypothesis_distance_need", 0.0) or 0.0),
                "open_hypothesis_reinterpretation_need": float(open_hypothesis_learning.get("open_hypothesis_reinterpretation_need", 0.0) or 0.0),
                "open_hypothesis_reorganization_posture": str(open_hypothesis_learning.get("open_hypothesis_reorganization_posture", "-") or "-"),
            })
            self.data["last_outcome_decomposition"] = dict(normalized_decomposition or {})

            outcome_record = {
                    "event": "cancel",
                    "reason": "cancel",
                    "timestamp": self.data.get("current_timestamp"),
                    "order_id": None if order_id is None else str(order_id),
                    "cause": None if cause is None else str(cause),
                    "rr_value": float(rr_value),
                    "structural_run_room": float(structural_run_room),
                    "emergent_structure_reading": float(emergent_structure_reading),
                    "emergent_structure_confirmation": float(emergent_structure_confirmation),
                    "emergent_structure_state": str(emergent_structure_state),
                    "open_hypothesis_learning_state": str(open_hypothesis_learning.get("open_hypothesis_learning_state", "-") or "-"),
                    "open_hypothesis_consequence_score": float(open_hypothesis_learning.get("open_hypothesis_consequence_score", 0.0) or 0.0),
                    "open_hypothesis_burden_score": float(open_hypothesis_learning.get("open_hypothesis_burden_score", 0.0) or 0.0),
                    "open_hypothesis_reorganization_score": float(open_hypothesis_learning.get("open_hypothesis_reorganization_score", 0.0) or 0.0),
                    "open_hypothesis_replay_need": float(open_hypothesis_learning.get("open_hypothesis_replay_need", 0.0) or 0.0),
                    "open_hypothesis_distance_need": float(open_hypothesis_learning.get("open_hypothesis_distance_need", 0.0) or 0.0),
                    "open_hypothesis_reinterpretation_need": float(open_hypothesis_learning.get("open_hypothesis_reinterpretation_need", 0.0) or 0.0),
                    "open_hypothesis_reorganization_posture": str(open_hypothesis_learning.get("open_hypothesis_reorganization_posture", "-") or "-"),
                    "thought_seed_id": str(thought_seed_state.get("thought_seed_id", "") or ""),
                    "thought_seed_label": str(thought_seed_state.get("thought_seed_label", "") or ""),
                    "thought_seed_metaregulator_state": str(thought_seed_state.get("seed_metaregulator_state", "") or ""),
                    "thought_seed_emergent_state": str(thought_seed_state.get("emergent_structure_state", "") or ""),
                    "thought_seed_trace_strength": float(thought_seed_state.get("thought_trace_strength", 0.0) or 0.0),
                    "thought_seed_maturity": float(thought_seed_state.get("thought_maturity", 0.0) or 0.0),
                    "thought_seed_reality_binding": float(thought_seed_state.get("reality_binding_score", 0.0) or 0.0),
                    "thought_seed_confirmation": float(thought_seed_state.get("thought_confirmation_score", 0.0) or 0.0),
                    "thought_seed_consequence_echo": float(thought_seed_state.get("consequence_echo", 0.0) or 0.0),
                    "thought_seed_reorganization_echo": float(thought_seed_state.get("reorganization_echo", 0.0) or 0.0),
                    "thought_seed_consequence_alignment": float(thought_seed_state.get("thought_consequence_alignment", 0.0) or 0.0),
                    "thought_seed_consequence_balance": float(thought_seed_state.get("thought_consequence_balance", 0.0) or 0.0),
                    "thought_seed_reality_lag": float(thought_seed_state.get("thought_reality_lag", 0.0) or 0.0),
                    "thought_seed_structural_grounding": float(thought_seed_state.get("thought_structural_grounding", 0.0) or 0.0),
                    "thought_seed_open_hypothesis_pressure": float(thought_seed_state.get("thought_open_hypothesis_pressure", 0.0) or 0.0),
                    "thought_seed_replay_maturation_pull": float(thought_seed_state.get("thought_replay_maturation_pull", 0.0) or 0.0),
                    "thought_seed_distance_maturation_pull": float(thought_seed_state.get("thought_distance_maturation_pull", 0.0) or 0.0),
                    "thought_seed_reinterpretation_pull": float(thought_seed_state.get("thought_reinterpretation_pull", 0.0) or 0.0),
                    "thought_seed_digestive_replay_pull": float(thought_seed_state.get("thought_digestive_replay_pull", 0.0) or 0.0),
                    "thought_seed_digestive_distance_pull": float(thought_seed_state.get("thought_digestive_distance_pull", 0.0) or 0.0),
                    "thought_seed_digestive_integration_pull": float(thought_seed_state.get("thought_digestive_integration_pull", 0.0) or 0.0),
                    "thought_seed_digestive_returned_trust": float(thought_seed_state.get("thought_digestive_returned_trust", 0.0) or 0.0),
                    "thought_seed_trust_return_readiness": float(thought_seed_state.get("trust_return_readiness", 0.0) or 0.0),
                    "thought_seed_digest_state": str(thought_seed_state.get("thought_digest_state", "") or ""),
                    "thought_seed_reifung_direction": str(thought_seed_state.get("thought_reifung_direction", "") or ""),
                    "thought_seed_semantic_origin_state": str(thought_seed_state.get("semantic_origin_state", "") or ""),
                    "thought_seed_borrowed_open_hypothesis_pressure": float(thought_seed_state.get("borrowed_open_hypothesis_pressure", 0.0) or 0.0),
                    "thought_seed_own_field_binding_pull": float(thought_seed_state.get("own_field_binding_pull", 0.0) or 0.0),
                    "semantic_origin_state": str(meta_regulation_state.get("semantic_origin_state", "") or ""),
                    "own_field_identity_strength": float(meta_regulation_state.get("own_field_identity_strength", 0.0) or 0.0),
                    "foreign_semantic_pressure": float(meta_regulation_state.get("foreign_semantic_pressure", 0.0) or 0.0),
                    "adopted_language_pressure": float(meta_regulation_state.get("adopted_language_pressure", 0.0) or 0.0),
                    "self_foreign_boundary_clarity": float(meta_regulation_state.get("self_foreign_boundary_clarity", 0.0) or 0.0),
                    "semantic_origin_conflict": float(meta_regulation_state.get("semantic_origin_conflict", 0.0) or 0.0),
                    "own_vs_foreign_margin": float(meta_regulation_state.get("own_vs_foreign_margin", 0.0) or 0.0),
                    "borrowed_vs_own_margin": float(meta_regulation_state.get("borrowed_vs_own_margin", 0.0) or 0.0),
                    "boundary_support_margin": float(meta_regulation_state.get("boundary_support_margin", 0.0) or 0.0),
                    "thought_seed_drift_risk": float(thought_seed_state.get("hallucination_drift_risk", 0.0) or 0.0),
                    "thought_seed_overthinking_risk": float(thought_seed_state.get("overthinking_risk", 0.0) or 0.0),
                    "target_expectation_value": float(target_expectation_value),
                    "structure_quality": float(structure_quality),
                    "structure_bucket": structure_bucket,
                    "outcome_decomposition": normalized_decomposition,
                    "context": compact_context,
                }

            self._append_record_file(self.outcome_path, outcome_record)
            self._rebuild_kpi_summary()
            self._save(force=True)
        except Exception:
            pass

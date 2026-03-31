# ==================================================
# MCM_Brain_Modell.py
# Brain + MCM Bridge
# ==================================================
from config import Config
from debug_reader import dbr_debug
from bot_engine.mcm_core_engine import compute_tension_from_ohlc
from MCM_KI_Modell import MCMField, ClusterDetector, Memory, SelfModel, AttractorSystem, RegulationLayer
from bot_engine.strukture_engine import StructureEngine
import numpy as np


# --------------------------------------------------
# DEBUG
# --------------------------------------------------
def _mcm_state_debug(msg):
    if bool(getattr(Config, "MCM_DEBUG", False)):
        dbr_debug(msg, "mcm_state_debug.csv")


def _mcm_decision_debug(msg):
    if bool(getattr(Config, "MCM_DEBUG", False)):
        dbr_debug(msg, "mcm_decision_debug.csv")


def _mcm_outcome_debug(msg):
    if bool(getattr(Config, "MCM_OUTCOME_DEBUG", False)):
        dbr_debug(msg, "mcm_outcome_debug.txt")


STRUCTURE_ENGINE = StructureEngine()

# --------------------------------------------------
# BRAIN FACTORY
# --------------------------------------------------
def create_mcm_brain():
    field = MCMField(
        n_agents=int(getattr(Config, "MCM_FIELD_AGENTS", 80) or 80),
        dims=int(getattr(Config, "MCM_FIELD_DIMS", 3) or 3),
    )

    field.coupling = float(getattr(Config, "MCM_COUPLING", field.coupling) or field.coupling)
    field.noise = float(getattr(Config, "MCM_NOISE", field.noise) or field.noise)
    field.k_center = float(getattr(Config, "MCM_CENTER_FORCE", field.k_center) or field.k_center)

    return {
        "field": field,
        "cluster": ClusterDetector(),
        "memory": Memory(),
        "self_model": SelfModel(),
        "attractor": AttractorSystem(),
        "regulation": RegulationLayer(),
    }


# --------------------------------------------------
# STIMULUS
# --------------------------------------------------
def build_market_vision(candle_state, tension_state):

    energy = float(tension_state.get("energy", 0.0) or 0.0)
    coherence = float(tension_state.get("coherence", 0.0) or 0.0)
    asymmetry = float(tension_state.get("asymmetry", 0.0) or 0.0)
    coh_zone = float(tension_state.get("coh_zone", 0.0) or 0.0)

    close_position = float(candle_state.get("close_position", 0.0) or 0.0)
    wick_bias = float(candle_state.get("wick_bias", 0.0) or 0.0)
    return_intensity = float(candle_state.get("return_intensity", 0.0) or 0.0)

    left_eye_flow = (coherence * 0.90) + (coh_zone * 0.25)
    right_eye_flow = (close_position * 0.85) + (return_intensity * 0.55)
    optic_flow = (left_eye_flow * 0.55) + (right_eye_flow * 0.45) + (asymmetry * 0.12)
    threat_map = (abs(wick_bias) * 0.55) + max(0.0, energy - 1.15) * 0.35 + abs(min(0.0, coherence)) * 0.30
    target_map = (max(0.0, coherence) * 0.45) + (max(0.0, close_position) * 0.35) + (max(0.0, return_intensity) * 0.20)
    orientation_drive = (energy - 1.0) * 0.45 + optic_flow * 0.75 - threat_map * 0.15
    vision_contrast = abs(coherence - close_position) + abs(wick_bias) * 0.35

    return {
        "left_eye_field": float(max(-2.5, min(2.5, left_eye_flow))),
        "right_eye_field": float(max(-2.5, min(2.5, right_eye_flow))),
        "optic_flow": float(max(-2.5, min(2.5, optic_flow))),
        "threat_map": float(max(0.0, min(2.5, threat_map))),
        "target_map": float(max(0.0, min(2.5, target_map))),
        "orientation_drive": float(max(-2.5, min(2.5, orientation_drive))),
        "vision_contrast": float(max(0.0, min(2.5, vision_contrast))),
    }


def build_focus_projection(candle_state, tension_state, vision, pause_mode=False, bot=None):

    coherence = float(tension_state.get("coherence", 0.0) or 0.0)
    energy = float(tension_state.get("energy", 0.0) or 0.0)
    close_position = float(candle_state.get("close_position", 0.0) or 0.0)
    return_intensity = float(candle_state.get("return_intensity", 0.0) or 0.0)

    optic_flow = float(vision.get("optic_flow", 0.0) or 0.0)
    threat_map = float(vision.get("threat_map", 0.0) or 0.0)
    target_map = float(vision.get("target_map", 0.0) or 0.0)
    orientation_drive = float(vision.get("orientation_drive", 0.0) or 0.0)
    vision_contrast = float(vision.get("vision_contrast", 0.0) or 0.0)

    prev_focus_point = 0.0
    prev_focus_confidence = 0.0
    prev_target_lock = 0.0
    prev_target_drift = 0.0

    if bot is not None:
        prev_focus_point = float(getattr(bot, "focus_point", 0.0) or 0.0)
        prev_focus_confidence = float(getattr(bot, "focus_confidence", 0.0) or 0.0)
        prev_target_lock = float(getattr(bot, "target_lock", 0.0) or 0.0)
        prev_target_drift = float(getattr(bot, "target_drift", 0.0) or 0.0)

    focus_direction = (
        orientation_drive * 0.38
        + coherence * 0.20
        + close_position * 0.18
        + return_intensity * 0.10
        + prev_focus_point * 0.14
    )

    raw_focus_strength = (
        target_map * float(getattr(Config, "MCM_FOCUS_TARGET_WEIGHT", 0.72) or 0.72)
        + max(0.0, optic_flow) * float(getattr(Config, "MCM_FOCUS_FLOW_WEIGHT", 0.18) or 0.18)
        + max(0.0, coherence) * 0.08
        + prev_target_lock * 0.12
    )

    noise_damp = (
        vision_contrast * float(getattr(Config, "MCM_FOCUS_NOISE_WEIGHT", 0.34) or 0.34)
        + threat_map * float(getattr(Config, "MCM_FOCUS_THREAT_NOISE_WEIGHT", 0.18) or 0.18)
        + max(0.0, abs(energy) - 1.25) * 0.10
        + max(0.0, abs(prev_target_drift) - 0.20) * 0.18
    )

    if bool(pause_mode):
        noise_damp += float(getattr(Config, "MCM_FOCUS_PAUSE_NOISE_ADD", 0.22) or 0.22)

    focus_strength = max(0.0, raw_focus_strength - noise_damp)

    target_lock = max(
        0.0,
        min(
            1.0,
            (focus_strength * 0.52)
            + (max(0.0, coherence) * 0.12)
            + (prev_target_lock * 0.20)
            + (prev_focus_confidence * 0.10),
        ),
    )

    focus_confidence = max(
        0.0,
        min(
            1.0,
            (target_map * 0.28)
            + (max(0.0, coherence) * 0.22)
            + (max(0.0, return_intensity) * 0.16)
            + (prev_focus_confidence * 0.18)
            - (vision_contrast * 0.18)
            - (threat_map * 0.12),
        ),
    )

    signal_relevance = max(
        0.0,
        min(
            1.0,
            (target_lock * 0.38)
            + (focus_confidence * 0.32)
            + (max(0.0, abs(focus_direction)) * 0.10)
            - (noise_damp * 0.10),
        ),
    )

    return {
        "focus_direction": float(max(-2.5, min(2.5, focus_direction))),
        "focus_strength": float(max(0.0, min(2.5, focus_strength))),
        "focus_confidence": float(max(0.0, min(1.0, focus_confidence))),
        "target_lock": float(max(0.0, min(1.0, target_lock))),
        "noise_damp": float(max(0.0, min(2.5, noise_damp))),
        "signal_relevance": float(max(0.0, min(1.0, signal_relevance))),
    }


# --------------------------------------------------
def apply_focus_filter(candle_state, tension_state, vision, focus, pause_mode=False):

    left_eye_field = float(vision.get("left_eye_field", 0.0) or 0.0)
    right_eye_field = float(vision.get("right_eye_field", 0.0) or 0.0)
    optic_flow = float(vision.get("optic_flow", 0.0) or 0.0)
    threat_map = float(vision.get("threat_map", 0.0) or 0.0)
    target_map = float(vision.get("target_map", 0.0) or 0.0)
    orientation_drive = float(vision.get("orientation_drive", 0.0) or 0.0)
    vision_contrast = float(vision.get("vision_contrast", 0.0) or 0.0)

    focus_direction = float(focus.get("focus_direction", 0.0) or 0.0)
    focus_strength = float(focus.get("focus_strength", 0.0) or 0.0)
    focus_confidence = float(focus.get("focus_confidence", 0.0) or 0.0)
    target_lock = float(focus.get("target_lock", 0.0) or 0.0)
    noise_damp = float(focus.get("noise_damp", 0.0) or 0.0)
    signal_relevance = float(focus.get("signal_relevance", 0.0) or 0.0)

    focus_gain = 1.0 + (focus_strength * float(getattr(Config, "MCM_FOCUS_GAIN_WEIGHT", 0.30) or 0.30))
    target_gain = 1.0 + (target_lock * float(getattr(Config, "MCM_TARGET_LOCK_GAIN", 0.42) or 0.42))
    threat_gate = 1.0 - (focus_confidence * float(getattr(Config, "MCM_THREAT_FOCUS_DAMP", 0.22) or 0.22))
    noise_gate = max(0.35, 1.0 - (noise_damp * float(getattr(Config, "MCM_NOISE_DAMP_WEIGHT", 0.24) or 0.24)))

    filtered_target_map = target_map * target_gain * noise_gate
    filtered_optic_flow = optic_flow * focus_gain * noise_gate
    filtered_orientation_drive = orientation_drive + (focus_direction * 0.26)
    filtered_threat_map = threat_map * max(0.35, threat_gate)
    filtered_contrast = vision_contrast * max(0.25, 1.0 - (signal_relevance * 0.45))

    impulse = filtered_orientation_drive + (filtered_optic_flow * 0.35) - (filtered_contrast * 0.08)
    motivation_impulse = (filtered_target_map * 0.48) + (right_eye_field * 0.22) - (filtered_threat_map * 0.14)
    risk_impulse = -(filtered_threat_map * 0.28) - (filtered_contrast * 0.06) + min(0.0, left_eye_field) * 0.08
    opportunity_bias = (filtered_target_map * 0.62) + max(0.0, filtered_optic_flow) * 0.22 + (signal_relevance * 0.10)

    if bool(pause_mode):
        impulse *= float(getattr(Config, "MCM_PAUSE_ORIENTATION_GAIN", 1.35) or 1.35)
        motivation_impulse *= float(getattr(Config, "MCM_PAUSE_MOTIVATION_DAMP", 0.55) or 0.55)
        risk_impulse *= float(getattr(Config, "MCM_PAUSE_RISK_GAIN", 1.20) or 1.20)
        opportunity_bias *= 0.50

    return {
        "vision": vision,
        "filtered_vision": {
            "left_eye_field": float(max(-2.5, min(2.5, left_eye_field))),
            "right_eye_field": float(max(-2.5, min(2.5, right_eye_field))),
            "optic_flow": float(max(-2.5, min(2.5, filtered_optic_flow))),
            "threat_map": float(max(0.0, min(2.5, filtered_threat_map))),
            "target_map": float(max(0.0, min(2.5, filtered_target_map))),
            "orientation_drive": float(max(-2.5, min(2.5, filtered_orientation_drive))),
            "vision_contrast": float(max(0.0, min(2.5, filtered_contrast))),
        },
        "focus": {
            "focus_direction": float(max(-2.5, min(2.5, focus_direction))),
            "focus_strength": float(max(0.0, min(2.5, focus_strength))),
            "focus_confidence": float(max(0.0, min(1.0, focus_confidence))),
            "target_lock": float(max(0.0, min(1.0, target_lock))),
            "noise_damp": float(max(0.0, min(2.5, noise_damp))),
            "signal_relevance": float(max(0.0, min(1.0, signal_relevance))),
        },
        "impulse": float(max(-2.5, min(2.5, impulse))),
        "motivation_impulse": float(max(-2.5, min(2.5, motivation_impulse))),
        "risk_impulse": float(max(-2.5, min(2.5, risk_impulse))),
        "opportunity_bias": float(max(-2.5, min(2.5, opportunity_bias))),
    }


# --------------------------------------------------
def build_mcm_stimulus(candle_state, tension_state, pause_mode=False, bot=None):

    vision = build_market_vision(candle_state, tension_state)
    focus = build_focus_projection(
        candle_state,
        tension_state,
        vision,
        pause_mode=pause_mode,
        bot=bot,
    )
    filtered = apply_focus_filter(candle_state, tension_state, vision, focus, pause_mode=pause_mode)

    return {
        "mode": "market",
        "pause_mode": bool(pause_mode),
        "vision": dict(filtered.get("vision", {}) or {}),
        "filtered_vision": dict(filtered.get("filtered_vision", {}) or {}),
        "focus": dict(filtered.get("focus", {}) or {}),
        "impulse": float(filtered.get("impulse", 0.0) or 0.0),
        "motivation_impulse": float(filtered.get("motivation_impulse", 0.0) or 0.0),
        "risk_impulse": float(filtered.get("risk_impulse", 0.0) or 0.0),
        "opportunity_bias": float(filtered.get("opportunity_bias", 0.0) or 0.0),
    }


# --------------------------------------------------
def build_neural_modulation(bot, stimulus):

    if bot is None:
        return {
            "inhibition_level": 0.0,
            "habituation_level": 0.0,
            "competition_bias": 0.0,
            "observation_mode": False,
            "signal_relevance": 0.0,
        }

    focus = dict((stimulus or {}).get("focus", {}) or {})
    filtered_vision = dict((stimulus or {}).get("filtered_vision", {}) or {})

    focus_direction = float(focus.get("focus_direction", 0.0) or 0.0)
    focus_confidence = float(focus.get("focus_confidence", 0.0) or 0.0)
    signal_relevance = float(focus.get("signal_relevance", 0.0) or 0.0)
    noise_damp = float(focus.get("noise_damp", 0.0) or 0.0)
    target_lock = float(focus.get("target_lock", 0.0) or 0.0)
    target_map = float(filtered_vision.get("target_map", 0.0) or 0.0)
    threat_map = float(filtered_vision.get("threat_map", 0.0) or 0.0)
    optic_flow = float(filtered_vision.get("optic_flow", 0.0) or 0.0)

    prev_inhibition = float(getattr(bot, "inhibition_level", 0.0) or 0.0)
    prev_habituation = float(getattr(bot, "habituation_level", 0.0) or 0.0)
    prev_competition = float(getattr(bot, "competition_bias", 0.0) or 0.0)
    prev_signal_relevance = float(getattr(bot, "last_signal_relevance", 0.0) or 0.0)

    repeated_signal = max(0.0, min(1.0, min(signal_relevance, prev_signal_relevance)))
    settling_bias = max(
        0.0,
        min(
            1.0,
            (focus_confidence * 0.26)
            + (signal_relevance * 0.24)
            + (target_lock * 0.14),
        ),
    )

    inhibition_raw = (noise_damp * 0.48) + (threat_map * 0.26) + max(0.0, abs(focus_direction) - focus_confidence) * 0.14
    habituation_raw = (repeated_signal * 0.58) + (target_lock * 0.16) + (max(0.0, target_map - abs(optic_flow)) * 0.10)
    competition_raw = (focus_direction * 0.62) + ((target_map - threat_map) * 0.18) + (optic_flow * 0.10)

    inhibition_level = max(0.0, min(1.0, (prev_inhibition * 0.68) + (inhibition_raw * float(getattr(Config, "MCM_INHIBITION_GAIN", 0.26) or 0.26))))
    habituation_level = max(0.0, min(1.0, (prev_habituation * 0.72) + (habituation_raw * float(getattr(Config, "MCM_HABITUATION_GAIN", 0.18) or 0.18))))
    competition_bias = max(-1.0, min(1.0, (prev_competition * 0.44) + (competition_raw * float(getattr(Config, "MCM_COMPETITION_GAIN", 0.22) or 0.22))))

    observation_pressure = max(
        0.0,
        (inhibition_level * 0.56)
        + (habituation_level * 0.44)
        - (settling_bias * 0.42),
    )
    observation_mode = bool(
        observation_pressure >= float(getattr(Config, "MCM_OBSERVE_THRESHOLD", 0.66) or 0.66)
        and focus_confidence < 0.70
        and signal_relevance < 0.76
    )

    bot.inhibition_level = float(inhibition_level)
    bot.habituation_level = float(habituation_level)
    bot.competition_bias = float(competition_bias)
    bot.observation_mode = bool(observation_mode)
    bot.last_signal_relevance = float(signal_relevance)

    return {
        "inhibition_level": float(inhibition_level),
        "habituation_level": float(habituation_level),
        "competition_bias": float(competition_bias),
        "observation_mode": bool(observation_mode),
        "signal_relevance": float(signal_relevance),
    }


def build_outcome_stimulus(outcome_reason, position=None):

    reason = str(outcome_reason or "").strip().lower()

    reward = 0.0
    motivation_impulse = 0.0
    risk_impulse = 0.0
    memory_boost = 0.0
    outcome_label = "neutral"

    if reason == "tp_hit":
        reward = float(getattr(Config, "MCM_TP_REWARD", 0.75) or 0.75)
        motivation_impulse = reward * 0.40
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.18) or 0.18)
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 1.0) or 1.0)
        outcome_label = "reward"
    elif reason == "sl_hit":
        reward = -float(getattr(Config, "MCM_SL_PENALTY", 0.85) or 0.85)
        motivation_impulse = reward * 0.28
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.18) or 0.18)
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 1.0) or 1.0)
        outcome_label = "aversive"
    elif reason == "cancel":
        reward = -float(getattr(Config, "MCM_CANCEL_PENALTY", 0.35) or 0.35)
        motivation_impulse = reward * 0.30
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.30) or 0.30) * 0.45
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 2.0) or 2.0) * 0.50
        outcome_label = "cancel"
    elif reason == "timeout":
        reward = -float(getattr(Config, "MCM_TIMEOUT_PENALTY", 0.45) or 0.45)
        motivation_impulse = reward * 0.35
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.30) or 0.30) * 0.60
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 2.0) or 2.0) * 0.60
        outcome_label = "timeout"
    elif reason == "reward_too_small":
        reward = -float(getattr(Config, "MCM_CANCEL_PENALTY", 0.35) or 0.35) * 0.85
        motivation_impulse = reward * 0.32
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.30) or 0.30) * 0.42
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 2.0) or 2.0) * 0.45
        outcome_label = "gate_reward"
    elif reason == "sl_distance_too_high":
        reward = -float(getattr(Config, "MCM_SL_PENALTY", 0.85) or 0.85) * 0.72
        motivation_impulse = reward * 0.26
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.30) or 0.30) * 0.70
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 2.0) or 2.0) * 0.55
        outcome_label = "gate_risk"
    elif reason == "rr_too_low":
        reward = -float(getattr(Config, "MCM_CANCEL_PENALTY", 0.35) or 0.35) * 1.05
        motivation_impulse = reward * 0.34
        risk_impulse = -float(getattr(Config, "MCM_OUTCOME_RISK_SHIFT", 0.30) or 0.30) * 0.58
        memory_boost = float(getattr(Config, "MCM_OUTCOME_MEMORY_BOOST", 2.0) or 2.0) * 0.50
        outcome_label = "gate_rr"

    return {
        "mode": "outcome",
        "impulse": float(max(-2.5, min(2.5, reward))),
        "motivation_impulse": float(max(-2.5, min(2.5, motivation_impulse))),
        "risk_impulse": float(max(-2.5, min(2.5, risk_impulse))),
        "memory_boost": float(max(0.0, min(8.0, memory_boost))),
        "outcome_label": outcome_label,
    }

# --------------------------------------------------
# MCM STEP
# --------------------------------------------------
def step_mcm_brain(brain, stimulus, mode="market"):

    field = brain["field"]
    memory = brain["memory"]
    cluster = brain["cluster"]
    self_model = brain["self_model"]
    attractor = brain["attractor"]
    regulation = brain["regulation"]

    replay_scale = float(getattr(Config, "MCM_REPLAY_SCALE", 0.05) or 0.05)
    internal_cycles = int(getattr(Config, "MCM_INTERNAL_CYCLES", 3) or 3)

    replay_impulse = float(memory.replay_impulse(replay_scale=replay_scale) or 0.0)

    mode_value = str(mode or stimulus.get("mode", "market") or "market").strip().lower()

    raw_impulse = float(stimulus.get("impulse", 0.0) or 0.0)
    motivation_impulse = float(stimulus.get("motivation_impulse", 0.0) or 0.0)
    risk_impulse = float(stimulus.get("risk_impulse", 0.0) or 0.0)
    opportunity_bias = float(stimulus.get("opportunity_bias", 0.0) or 0.0)
    memory_boost = float(stimulus.get("memory_boost", 0.0) or 0.0)
    outcome_label = str(stimulus.get("outcome_label", "-") or "-")

    if mode_value == "outcome":
        total_energy_impulse = (raw_impulse * 1.10) + (replay_impulse * 0.18)
        motivation_impulse = (motivation_impulse * 0.95)
        risk_impulse = (risk_impulse * 0.95) - (max(0.0, abs(raw_impulse) - 0.5) * 0.15)
    else:
        total_energy_impulse = (raw_impulse * 0.72) + (replay_impulse * 0.45)
        motivation_impulse = (motivation_impulse * 0.55) - (abs(replay_impulse) * 0.08)
        risk_impulse = (risk_impulse * 0.85) - (max(0.0, abs(raw_impulse) - 1.0) * 0.10)

    for _ in range(max(1, internal_cycles)):
        field.step(replay_impulse * 0.35)

    field.energy *= 0.94
    field.velocity *= 0.88

    field.energy[:, 0] += total_energy_impulse
    if mode_value == "outcome":
        field.energy[:, 1] += motivation_impulse
        field.energy[:, 2] += risk_impulse
    else:
        field.energy[:, 1] += motivation_impulse - (opportunity_bias * 0.06)
        field.energy[:, 2] += risk_impulse - (opportunity_bias * 0.08)

    field.energy = np.clip(field.energy, -2.2, 2.2)
    field.step(total_energy_impulse * 0.55)
    field.energy = np.clip(field.energy, -2.2, 2.2)

    clusters = cluster.detect(field.energy)

    memory_store_clusters = []
    for item in clusters:
        strength = int(len(item))
        if mode_value == "outcome":
            strength += int(round(memory_boost))
        if strength >= 3:
            memory_store_clusters.append(item[:12])

    memory.store(memory_store_clusters)

    # ---------------
    self_state = self_model.evaluate(field.energy)
    regulation.regulate(field)

    mean_energy = float(np.mean(field.energy[:, 0]))
    mean_motivation = float(np.mean(field.energy[:, 1]))
    mean_risk = float(np.mean(field.energy[:, 2]))

    if self_state == "excited" and mean_energy > 1.35:
        field.energy[:, 0] *= 0.90
        field.energy[:, 1] *= 0.92

    if self_state == "stressed" and mean_risk < -0.85:
        field.energy[:, 0] *= 0.88
        field.energy[:, 1] *= 0.84

    strongest_memory = memory.strongest()
    selected_attractor = attractor.choose(strongest_memory, self_state)

    mean_energy = float(np.mean(field.energy[:, 0]))
    mean_motivation = float(np.mean(field.energy[:, 1]))
    mean_risk = float(np.mean(field.energy[:, 2]))
    mean_velocity = float(np.mean(np.linalg.norm(field.velocity, axis=1)))

    snapshot = {
        "mode": mode_value,
        "outcome_label": outcome_label,
        "replay_impulse": float(replay_impulse),
        "self_state": str(self_state),
        "attractor": str(selected_attractor),
        "strongest_memory": strongest_memory,
        "mean_energy": float(mean_energy),
        "mean_motivation": float(mean_motivation),
        "mean_risk": float(mean_risk),
        "mean_velocity": float(mean_velocity),
        "cluster_count": int(len(clusters)),
        "regulation_pressure": float(abs(mean_energy) * 0.85 + abs(mean_risk) * 0.95 + mean_velocity * 0.35),
    }

    _mcm_state_debug(
        "MCM_STATE | "
        f"mode={mode_value} "
        f"impulse={total_energy_impulse:.4f} "
        f"motivation={motivation_impulse:.4f} "
        f"risk={risk_impulse:.4f} "
        f"replay={replay_impulse:.4f} "
        f"self_state={self_state} "
        f"attractor={selected_attractor} "
        f"mean_energy={mean_energy:.4f} "
        f"mean_motivation={mean_motivation:.4f} "
        f"mean_risk={mean_risk:.4f} "
        f"mean_velocity={mean_velocity:.4f} "
        f"clusters={len(clusters)} "
        f"memory_center={float(strongest_memory.get('center', 0.0)) if strongest_memory else 0.0:.4f} "
        f"memory_strength={int(strongest_memory.get('strength', 0)) if strongest_memory else 0}"
    )

    return snapshot

# --------------------------------------------------
# OUTCOME API
# --------------------------------------------------
def apply_outcome_stimulus(bot, outcome_reason, position=None):

    if bot is None:
        return None

    if not bool(getattr(Config, "MCM_ENABLED", True)):
        return None

    if getattr(bot, "mcm_brain", None) is None:
        bot.mcm_brain = create_mcm_brain()

    before_snapshot = dict(getattr(bot, "mcm_snapshot", {}) or {})
    before_memory = before_snapshot.get("strongest_memory") or {}

    stimulus = build_outcome_stimulus(outcome_reason, position)
    snapshot = step_mcm_brain(bot.mcm_brain, stimulus, mode="outcome")

    bot.mcm_last_state = dict(snapshot)
    bot.mcm_last_action = str(snapshot.get("self_state", "stable"))
    bot.mcm_last_attractor = str(snapshot.get("attractor", "neutral"))
    bot.mcm_snapshot = dict(snapshot)

    reason = str(outcome_reason or "").strip().lower()

    if reason == "tp_hit":
        bot.focus_confidence = float(min(1.0, (float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.55) + 0.35))
        bot.target_lock = float(min(1.0, (float(getattr(bot, "target_lock", 0.0) or 0.0) * 0.60) + 0.30))
        bot.target_drift = float((float(getattr(bot, "target_drift", 0.0) or 0.0)) * 0.45)

    elif reason == "sl_hit":
        bot.focus_confidence = float(max(0.0, float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.55))
        bot.target_lock = float(max(0.0, float(getattr(bot, "target_lock", 0.0) or 0.0) * 0.45))
        bot.target_drift = float((float(getattr(bot, "target_drift", 0.0) or 0.0)) * 1.15)

    elif reason in ("cancel", "timeout"):
        bot.focus_confidence = float(max(0.0, float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.72))
        bot.target_lock = float(max(0.0, float(getattr(bot, "target_lock", 0.0) or 0.0) * 0.68))

    elif reason in ("reward_too_small", "rr_too_low", "sl_distance_too_high"):
        bot.focus_confidence = float(max(0.0, float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.64))
        bot.target_lock = float(max(0.0, float(getattr(bot, "target_lock", 0.0) or 0.0) * 0.58))
        bot.target_drift = float((float(getattr(bot, "target_drift", 0.0) or 0.0)) * 1.08)

    experience_state = update_experience_state(bot, reason)
    outcome_decomposition = build_outcome_decomposition(bot, reason, position, experience_state)
    bot.last_outcome_decomposition = dict(outcome_decomposition or {})

    signature_key = str(getattr(bot, "last_signature_key", "") or "").strip()
    if signature_key:
        update_signature_memory(
            bot,
            {"signature_key": signature_key},
            outcome=reason,
        )

    context_cluster_id = str(getattr(bot, "last_context_cluster_id", "") or "").strip()
    if context_cluster_id:
        update_context_cluster_outcome(
            bot,
            context_cluster_id,
            outcome=reason,
        )

    after_memory = snapshot.get("strongest_memory") or {}

    signature_score = 0.0
    if signature_key and isinstance(getattr(bot, "signature_memory", None), dict):
        signature_score = float((bot.signature_memory.get(signature_key) or {}).get("score", 0.0) or 0.0)

    _mcm_outcome_debug(
        "MCM_OUTCOME | "
        f"reason={str(outcome_reason or '-')} "
        f"reward_impulse={float(stimulus.get('impulse', 0.0) or 0.0):.4f} "
        f"motivation_impulse={float(stimulus.get('motivation_impulse', 0.0) or 0.0):.4f} "
        f"risk_impulse={float(stimulus.get('risk_impulse', 0.0) or 0.0):.4f} "
        f"self_state_before={str(before_snapshot.get('self_state', '-'))} "
        f"self_state_after={str(snapshot.get('self_state', '-'))} "
        f"attractor_before={str(before_snapshot.get('attractor', '-'))} "
        f"attractor_after={str(snapshot.get('attractor', '-'))} "
        f"memory_center_before={float(before_memory.get('center', 0.0) or 0.0):.4f} "
        f"memory_center_after={float(after_memory.get('center', 0.0) or 0.0):.4f} "
        f"memory_strength_before={int(before_memory.get('strength', 0) or 0)} "
        f"memory_strength_after={int(after_memory.get('strength', 0) or 0)} "
        f"focus_confidence={float(getattr(bot, 'focus_confidence', 0.0) or 0.0):.4f} "
        f"target_lock={float(getattr(bot, 'target_lock', 0.0) or 0.0):.4f} "
        f"target_drift={float(getattr(bot, 'target_drift', 0.0) or 0.0):.4f} "
        f"entry_expectation={float((experience_state or {}).get('entry_expectation', 0.0) or 0.0):.4f} "
        f"target_expectation={float((experience_state or {}).get('target_expectation', 0.0) or 0.0):.4f} "
        f"approach_pressure={float((experience_state or {}).get('approach_pressure', 0.0) or 0.0):.4f} "
        f"pressure_release={float((experience_state or {}).get('pressure_release', 0.0) or 0.0):.4f} "
        f"experience_regulation={float((experience_state or {}).get('experience_regulation', 0.0) or 0.0):.4f} "
        f"reflection_maturity={float((experience_state or {}).get('reflection_maturity', 0.0) or 0.0):.4f} "
        f"signature_key={signature_key or '-'} "
        f"signature_score={signature_score:.4f} "
        f"outcome_decomposition={dict(outcome_decomposition or {})}"
    )

    return snapshot


def build_world_state(candle_state, tension_state, stimulus, structure_perception_state=None):
    return {
        "candle_state": dict(candle_state or {}),
        "tension_state": dict(tension_state or {}),
        "vision": dict((stimulus or {}).get("vision", {}) or {}),
        "filtered_vision": dict((stimulus or {}).get("filtered_vision", {}) or {}),
        "focus": dict((stimulus or {}).get("focus", {}) or {}),
        "structure_perception_state": dict(structure_perception_state or {}),
    }


def build_outer_visual_perception_state(world_state):
    world = dict(world_state or {})
    focus = dict(world.get("focus", {}) or {})
    filtered_vision = dict(world.get("filtered_vision", {}) or {})
    vision = dict(world.get("vision", {}) or {})

    return {
        "focus_direction": float(focus.get("focus_direction", 0.0) or 0.0),
        "focus_strength": float(focus.get("focus_strength", 0.0) or 0.0),
        "focus_confidence": float(focus.get("focus_confidence", 0.0) or 0.0),
        "target_lock": float(focus.get("target_lock", 0.0) or 0.0),
        "noise_damp": float(focus.get("noise_damp", 0.0) or 0.0),
        "signal_relevance": float(focus.get("signal_relevance", 0.0) or 0.0),
        "visual_target_map": float(filtered_vision.get("target_map", 0.0) or 0.0),
        "visual_threat_map": float(filtered_vision.get("threat_map", 0.0) or 0.0),
        "visual_optic_flow": float(filtered_vision.get("optic_flow", 0.0) or 0.0),
        "visual_contrast": float(vision.get("vision_contrast", 0.0) or 0.0),
    }


def build_inner_field_perception_state(snapshot, bot=None):
    snap = dict(snapshot or {})
    prior_regulation = float(getattr(bot, "experience_regulation", 0.0) or 0.0) if bot is not None else 0.0
    return {
        "field_mean_energy": float(snap.get("mean_energy", 0.0) or 0.0),
        "field_mean_motivation": float(snap.get("mean_motivation", 0.0) or 0.0),
        "field_mean_risk": float(snap.get("mean_risk", 0.0) or 0.0),
        "field_mean_velocity": float(snap.get("mean_velocity", 0.0) or 0.0),
        "field_cluster_count": int(snap.get("cluster_count", 0) or 0),
        "field_regulation_pressure": float(snap.get("regulation_pressure", 0.0) or 0.0),
        "self_state": str(snap.get("self_state", "stable") or "stable"),
        "attractor": str(snap.get("attractor", "neutral") or "neutral"),
        "prior_experience_regulation": float(prior_regulation),
    }


def build_processing_state(outer_visual_perception_state, inner_field_perception_state, perception_state):
    outer = dict(outer_visual_perception_state or {})
    inner = dict(inner_field_perception_state or {})
    perception = dict(perception_state or {})

    signal_relevance = float(outer.get("signal_relevance", 0.0) or 0.0)
    visual_contrast = float(outer.get("visual_contrast", 0.0) or 0.0)
    field_risk = abs(float(inner.get("field_mean_risk", 0.0) or 0.0))
    field_pressure = float(inner.get("field_regulation_pressure", 0.0) or 0.0)
    uncertainty = float(perception.get("uncertainty_score", 0.0) or 0.0)
    novelty = float(perception.get("novelty_score", 0.0) or 0.0)
    structure_quality = float(perception.get("structure_quality", 0.0) or 0.0)
    structure_stability = float(perception.get("structure_stability", 0.0) or 0.0)

    processing_load = max(0.0, min(1.0, (uncertainty * 0.35) + (novelty * 0.20) + (field_pressure * 0.20) + (field_risk * 0.15) + (visual_contrast * 0.10) - (structure_stability * 0.08)))
    processing_stability = max(0.0, min(1.0, signal_relevance * 0.40 + max(0.0, 1.0 - uncertainty) * 0.30 + max(0.0, 1.0 - min(1.0, field_risk)) * 0.18 + (structure_quality * 0.12)))
    processing_readiness = max(0.0, min(1.0, (processing_stability * 0.58) + (max(0.0, 1.0 - processing_load) * 0.42)))

    return {
        "processing_load": float(processing_load),
        "processing_stability": float(processing_stability),
        "processing_readiness": float(processing_readiness),
    }


def build_outcome_decomposition(bot, outcome_reason, position=None, experience_state=None):
    reason = str(outcome_reason or "").strip().lower()
    state = dict(experience_state or {})

    perception_quality = float(max(0.0, min(
        1.0,
        0.52
        + (float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.22)
        - (float(getattr(bot, "last_signal_relevance", 0.0) or 0.0) * 0.10),
    )))
    felt_quality = float(max(0.0, min(
        1.0,
        0.50
        + (float(state.get("experience_regulation", 0.0) or 0.0) * 0.20)
        + (float(state.get("reflection_maturity", 0.0) or 0.0) * 0.12),
    )))
    thought_quality = float(max(0.0, min(
        1.0,
        0.50
        + (float(state.get("reflection_maturity", 0.0) or 0.0) * 0.22)
        + (float(state.get("load_bearing_capacity", 0.0) or 0.0) * 0.12),
    )))

    plan_quality = 0.50
    execution_quality = 0.50
    risk_fit_quality = 0.50

    if reason == "tp_hit":
        plan_quality += 0.18
        execution_quality += 0.18
        risk_fit_quality += 0.12
    elif reason == "sl_hit":
        plan_quality -= 0.16
        execution_quality -= 0.12
        risk_fit_quality -= 0.18
    elif reason in ("cancel", "timeout"):
        execution_quality -= 0.15
        plan_quality -= 0.08
    elif reason == "reward_too_small":
        plan_quality -= 0.18
    elif reason == "rr_too_low":
        plan_quality -= 0.16
        risk_fit_quality -= 0.12
    elif reason == "sl_distance_too_high":
        risk_fit_quality -= 0.20
        plan_quality -= 0.10

    if isinstance(position, dict):
        risk = abs(float(position.get("entry", 0.0) or 0.0) - float(position.get("sl", 0.0) or 0.0))
        if risk > 0.0:
            risk_fit_quality = float(max(0.0, min(1.0, risk_fit_quality - min(0.18, risk * 2.5))))

    return {
        "perception_quality": float(max(0.0, min(1.0, perception_quality))),
        "felt_quality": float(max(0.0, min(1.0, felt_quality))),
        "thought_quality": float(max(0.0, min(1.0, thought_quality))),
        "plan_quality": float(max(0.0, min(1.0, plan_quality))),
        "execution_quality": float(max(0.0, min(1.0, execution_quality))),
        "risk_fit_quality": float(max(0.0, min(1.0, risk_fit_quality))),
        "reason": str(reason or "-"),
    }

def build_world_state(candle_state, tension_state, stimulus):
    return {
        "candle_state": dict(candle_state or {}),
        "tension_state": dict(tension_state or {}),
        "vision": dict((stimulus or {}).get("vision", {}) or {}),
        "filtered_vision": dict((stimulus or {}).get("filtered_vision", {}) or {}),
        "focus": dict((stimulus or {}).get("focus", {}) or {}),
    }

def build_outer_visual_perception_state(world_state):
    world = dict(world_state or {})
    focus = dict(world.get("focus", {}) or {})
    filtered_vision = dict(world.get("filtered_vision", {}) or {})
    vision = dict(world.get("vision", {}) or {})

    return {
        "focus_direction": float(focus.get("focus_direction", 0.0) or 0.0),
        "focus_strength": float(focus.get("focus_strength", 0.0) or 0.0),
        "focus_confidence": float(focus.get("focus_confidence", 0.0) or 0.0),
        "target_lock": float(focus.get("target_lock", 0.0) or 0.0),
        "noise_damp": float(focus.get("noise_damp", 0.0) or 0.0),
        "signal_relevance": float(focus.get("signal_relevance", 0.0) or 0.0),
        "visual_target_map": float(filtered_vision.get("target_map", 0.0) or 0.0),
        "visual_threat_map": float(filtered_vision.get("threat_map", 0.0) or 0.0),
        "visual_optic_flow": float(filtered_vision.get("optic_flow", 0.0) or 0.0),
        "visual_contrast": float(vision.get("vision_contrast", 0.0) or 0.0),
    }

def build_inner_field_perception_state(snapshot, bot=None):
    snap = dict(snapshot or {})
    prior_regulation = float(getattr(bot, "experience_regulation", 0.0) or 0.0) if bot is not None else 0.0
    return {
        "field_mean_energy": float(snap.get("mean_energy", 0.0) or 0.0),
        "field_mean_motivation": float(snap.get("mean_motivation", 0.0) or 0.0),
        "field_mean_risk": float(snap.get("mean_risk", 0.0) or 0.0),
        "field_mean_velocity": float(snap.get("mean_velocity", 0.0) or 0.0),
        "field_cluster_count": int(snap.get("cluster_count", 0) or 0),
        "field_regulation_pressure": float(snap.get("regulation_pressure", 0.0) or 0.0),
        "self_state": str(snap.get("self_state", "stable") or "stable"),
        "attractor": str(snap.get("attractor", "neutral") or "neutral"),
        "prior_experience_regulation": float(prior_regulation),
    }

def build_processing_state(outer_visual_perception_state, inner_field_perception_state, perception_state):
    outer = dict(outer_visual_perception_state or {})
    inner = dict(inner_field_perception_state or {})
    perception = dict(perception_state or {})

    signal_relevance = float(outer.get("signal_relevance", 0.0) or 0.0)
    visual_contrast = float(outer.get("visual_contrast", 0.0) or 0.0)
    field_risk = abs(float(inner.get("field_mean_risk", 0.0) or 0.0))
    field_pressure = float(inner.get("field_regulation_pressure", 0.0) or 0.0)
    uncertainty = float(perception.get("uncertainty_score", 0.0) or 0.0)
    novelty = float(perception.get("novelty_score", 0.0) or 0.0)   

    processing_load = max(0.0, min(1.0, (uncertainty * 0.35) + (novelty * 0.20) + (field_pressure * 0.20) + (field_risk * 0.15) + (visual_contrast * 0.10)))
    processing_stability = max(0.0, min(1.0, signal_relevance * 0.45 + max(0.0, 1.0 - uncertainty) * 0.35 + max(0.0, 1.0 - min(1.0, field_risk)) * 0.20))
    processing_readiness = max(0.0, min(1.0, (processing_stability * 0.58) + (max(0.0, 1.0 - processing_load) * 0.42)))

    return {
        "processing_load": float(processing_load),
        "processing_stability": float(processing_stability),
        "processing_readiness": float(processing_readiness),
    }

def build_outcome_decomposition(bot, outcome_reason, position=None, experience_state=None):
    reason = str(outcome_reason or "").strip().lower()
    state = dict(experience_state or {})

    perception_quality = float(max(0.0, min(
        1.0,
        0.52
        + (float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.22)
        - (float(getattr(bot, "last_signal_relevance", 0.0) or 0.0) * 0.10),
    )))
    felt_quality = float(max(0.0, min(
        1.0,
        0.50
        + (float(state.get("experience_regulation", 0.0) or 0.0) * 0.20)
        + (float(state.get("reflection_maturity", 0.0) or 0.0) * 0.12),
    )))
    thought_quality = float(max(0.0, min(
        1.0,
        0.50
        + (float(state.get("reflection_maturity", 0.0) or 0.0) * 0.22)
        + (float(state.get("load_bearing_capacity", 0.0) or 0.0) * 0.12),
    )))

    plan_quality = 0.50
    execution_quality = 0.50
    risk_fit_quality = 0.50

    if reason == "tp_hit":
        plan_quality += 0.18
        execution_quality += 0.18
        risk_fit_quality += 0.12
    elif reason == "sl_hit":
        plan_quality -= 0.16
        execution_quality -= 0.12
        risk_fit_quality -= 0.18
    elif reason in ("cancel", "timeout"):
        execution_quality -= 0.15
        plan_quality -= 0.08
    elif reason == "reward_too_small":
        plan_quality -= 0.18
    elif reason == "rr_too_low":
        plan_quality -= 0.16
        risk_fit_quality -= 0.12
    elif reason == "sl_distance_too_high":
        risk_fit_quality -= 0.20
        plan_quality -= 0.10

    if isinstance(position, dict):
        risk = abs(float(position.get("entry", 0.0) or 0.0) - float(position.get("sl", 0.0) or 0.0))
        if risk > 0.0:
            risk_fit_quality = float(max(0.0, min(1.0, risk_fit_quality - min(0.18, risk * 2.5))))

    return {
        "perception_quality": float(max(0.0, min(1.0, perception_quality))),
        "felt_quality": float(max(0.0, min(1.0, felt_quality))),
        "thought_quality": float(max(0.0, min(1.0, thought_quality))),
        "plan_quality": float(max(0.0, min(1.0, plan_quality))),
        "execution_quality": float(max(0.0, min(1.0, execution_quality))),
        "risk_fit_quality": float(max(0.0, min(1.0, risk_fit_quality))),
        "reason": str(reason or "-"),
    }

# --------------------------------------------------
# PRICE BUILD
# --------------------------------------------------
def derive_trade_plan_from_brain(side, candle_state, fused, stimulus, snapshot, bot=None):

    decision = str(side or "").upper().strip()
    if decision not in ("LONG", "SHORT"):
        return None

    candle = dict(candle_state or {})
    fused_state = dict(fused or {})
    stimulus_state = dict(stimulus or {})
    snapshot_state = dict(snapshot or {})

    open_price = float(candle.get("open", 0.0) or 0.0)
    high_price = float(candle.get("high", open_price) or open_price)
    low_price = float(candle.get("low", open_price) or open_price)
    close_price = float(candle.get("close", open_price) or open_price)

    if close_price <= 0.0:
        return None

    candle_span = max(high_price - low_price, close_price * 0.0005, 1e-9)
    base_move = max(candle_span, close_price * 0.0012)

    focus = dict(stimulus_state.get("focus", {}) or {})
    filtered_vision = dict(stimulus_state.get("filtered_vision", {}) or {})

    focus_direction = float(focus.get("focus_direction", 0.0) or 0.0)
    focus_confidence = float(focus.get("focus_confidence", 0.0) or 0.0)
    target_lock = float(focus.get("target_lock", 0.0) or 0.0)
    signal_relevance = float(focus.get("signal_relevance", 0.0) or 0.0)
    noise_damp = float(focus.get("noise_damp", 0.0) or 0.0)

    filtered_target_map = float(filtered_vision.get("target_map", 0.0) or 0.0)
    filtered_threat_map = float(filtered_vision.get("threat_map", 0.0) or 0.0)
    filtered_optic_flow = float(filtered_vision.get("optic_flow", 0.0) or 0.0)

    target_drift = float(getattr(bot, "target_drift", 0.0) or 0.0) if bot is not None else 0.0
    load_bearing_capacity = float(getattr(bot, "load_bearing_capacity", 0.0) or 0.0) if bot is not None else 0.0
    protective_width_regulation = float(getattr(bot, "protective_width_regulation", 0.0) or 0.0) if bot is not None else 0.0
    protective_courage = float(getattr(bot, "protective_courage", 0.0) or 0.0) if bot is not None else 0.0
    inhibition_level = float(fused_state.get("inhibition_level", 0.0) or 0.0)
    habituation_level = float(fused_state.get("habituation_level", 0.0) or 0.0)
    competition_bias = float(fused_state.get("competition_bias", 0.0) or 0.0)
    context_cluster_bias = float(fused_state.get("context_cluster_bias", 0.0) or 0.0)
    context_cluster_quality = float(fused_state.get("context_cluster_quality", 0.0) or 0.0)
    signature_bias = float(fused_state.get("signature_bias", 0.0) or 0.0)
    signature_quality = float(fused_state.get("signature_quality", 0.0) or 0.0)
    long_score = float(fused_state.get("long_score", 0.0) or 0.0)
    short_score = float(fused_state.get("short_score", 0.0) or 0.0)
    self_state = str(snapshot_state.get("self_state", "stable") or "stable")

    directional_score = long_score if decision == "LONG" else short_score
    directional_competition = max(0.0, competition_bias) if decision == "LONG" else max(0.0, -competition_bias)
    entry_pull = max(0.0, abs(target_drift)) * 0.35 + max(0.0, abs(focus_direction)) * 0.18 + max(0.0, filtered_optic_flow) * 0.08
    entry_shift = min(base_move * 0.55, base_move * entry_pull)

    if decision == "LONG":
        entry_price = close_price - entry_shift
        validity_center = entry_price + min(entry_shift * 0.35, base_move * 0.15)
    else:
        entry_price = close_price + entry_shift
        validity_center = entry_price - min(entry_shift * 0.35, base_move * 0.15)

    validity_halfwidth = max(
        base_move * 0.20,
        base_move * (
            0.22
            + (1.0 - focus_confidence) * 0.20
            + noise_damp * 0.08
            + inhibition_level * 0.10
        ),
    )

    risk_model_score = max(
        0.0,
        min(
            1.0,
            (filtered_threat_map * 0.28)
            + (noise_damp * 0.18)
            + (inhibition_level * 0.18)
            + (habituation_level * 0.10)
            + max(0.0, -context_cluster_bias) * 0.10
            + max(0.0, -signature_bias) * 0.08
            + max(0.0, abs(target_drift)) * 0.10,
        ),
    )

    reward_model_score = max(
        0.0,
        min(
            1.0,
            (signal_relevance * 0.24)
            + (target_lock * 0.22)
            + (focus_confidence * 0.18)
            + (filtered_target_map * 0.14)
            + directional_competition * 0.08
            + max(0.0, context_cluster_bias) * 0.08
            + max(0.0, signature_bias) * 0.06
            + max(0.0, directional_score) * 0.06,
        ),
    )

    target_conviction = max(
        0.0,
        min(
            1.0,
            (target_lock * 0.28)
            + (focus_confidence * 0.22)
            + (signal_relevance * 0.18)
            + (context_cluster_quality * 0.10)
            + (signature_quality * 0.08)
            + max(0.0, directional_score) * 0.08,
        ),
    )

    stress_pressure = max(
        0.0,
        min(
            1.0,
            max(0.0, float(snapshot_state.get("regulation_pressure", 0.0) or 0.0) / 2.2),
        ),
    )

    risk_distance = max(
        base_move * (
            0.42
            + (risk_model_score * 0.58)
            + (1.0 - target_conviction) * 0.12
            + (1.0 - reward_model_score) * 0.06
        ),
        close_price * float(getattr(Config, "MCM_MIN_SL_DISTANCE", 0.0022) or 0.0022),
        candle_span * 0.42,
    )

    protective_width_factor = max(
        0.82,
        min(
            1.12,
            1.0
            + (protective_width_regulation * 0.14)
            + (load_bearing_capacity * 0.04)
            + (stress_pressure * 0.10)
            + max(0.0, risk_model_score - reward_model_score) * 0.08
            - (protective_courage * 0.10)
            - (target_conviction * 0.12)
            - (inhibition_level * 0.04),
        ),
    )
    risk_distance *= protective_width_factor

    max_sl_pct = float(getattr(Config, "MAX_SL_DISTANCE", 0.0) or 0.0)
    if max_sl_pct > 0.0:
        gate_aligned_sl = close_price * max_sl_pct * float(getattr(Config, "MCM_PLAN_GATE_ALIGN", 0.92) or 0.92)
        risk_distance = min(
            risk_distance,
            max(
                gate_aligned_sl,
                close_price * float(getattr(Config, "MCM_MIN_SL_DISTANCE", 0.0022) or 0.0022),
            ),
        )

    min_reward_distance = close_price * float(getattr(Config, "MIN_TP_DISTANCE", 0.008) or 0.008)
    min_rr_target = max(
        float(getattr(Config, "MIN_RR", 1.0) or 1.0),
        1.15 + (target_conviction * 0.18) + (reward_model_score * 0.12) - (risk_model_score * 0.08),
    )
    reward_distance = max(
        base_move * (
            0.82
            + (reward_model_score * 1.18)
            + (target_conviction * 0.42)
            - (risk_model_score * 0.12)
        ),
        min_reward_distance * (
            1.0
            + (reward_model_score * 0.22)
            + (target_conviction * 0.12)
            - (risk_model_score * 0.06)
        ),
        risk_distance * min_rr_target,
        min_reward_distance,
    )

    if self_state == "stressed":
        reward_distance *= 0.94
        risk_distance *= 1.0 + (stress_pressure * 0.06)
    elif self_state == "excited":
        reward_distance *= 1.06

    if decision == "LONG":
        sl_price = entry_price - risk_distance
        tp_price = entry_price + reward_distance
    else:
        sl_price = entry_price + risk_distance
        tp_price = entry_price - reward_distance

    reward = abs(tp_price - entry_price)
    risk = abs(entry_price - sl_price)
    rr_value = reward / max(risk, 1e-9)

    return {
        "entry_price": float(entry_price),
        "sl_price": float(sl_price),
        "tp_price": float(tp_price),
        "rr_value": float(rr_value),
        "entry_validity_band": {
            "center": float(validity_center),
            "lower": float(validity_center - validity_halfwidth),
            "upper": float(validity_center + validity_halfwidth),
            "halfwidth": float(validity_halfwidth),
        },
        "target_conviction": float(target_conviction),
        "risk_model_score": float(risk_model_score),
        "reward_model_score": float(reward_model_score),
    }


# --------------------------------------------------
# FUSION
# --------------------------------------------------
def resolve_fused_decision(candle_state, tension_state, mcm_snapshot, bot=None):

    coherence = float(tension_state.get("coherence", 0.0) or 0.0)
    close_position = float(candle_state.get("close_position", 0.0) or 0.0)
    wick_bias = float(candle_state.get("wick_bias", 0.0) or 0.0)
    return_intensity = float(candle_state.get("return_intensity", 0.0) or 0.0)

    long_score = (coherence * 0.95) + (close_position * 0.75) + (wick_bias * 0.35) + (return_intensity * 0.45)
    short_score = (-coherence * 0.95) + (-close_position * 0.75) + (-wick_bias * 0.35) + (-return_intensity * 0.45)

    memory = mcm_snapshot.get("strongest_memory") or {}
    memory_center = float(memory.get("center", 0.0) or 0.0)
    memory_strength = float(memory.get("strength", 0.0) or 0.0)

    focus_point = 0.0
    focus_confidence = 0.0
    target_lock = 0.0
    target_drift = 0.0
    inhibition_level = 0.0
    habituation_level = 0.0
    competition_bias = 0.0
    observation_mode = False

    if bot is not None:
        focus_point = float(getattr(bot, "focus_point", 0.0) or 0.0)
        focus_confidence = float(getattr(bot, "focus_confidence", 0.0) or 0.0)
        target_lock = float(getattr(bot, "target_lock", 0.0) or 0.0)
        target_drift = float(getattr(bot, "target_drift", 0.0) or 0.0)
        inhibition_level = float(getattr(bot, "inhibition_level", 0.0) or 0.0)
        habituation_level = float(getattr(bot, "habituation_level", 0.0) or 0.0)
        competition_bias = float(getattr(bot, "competition_bias", 0.0) or 0.0)
        observation_mode = bool(getattr(bot, "observation_mode", False))

    pressure_weight = float(getattr(Config, "MCM_PRESSURE_WEIGHT", 0.35) or 0.35)
    memory_weight = float(getattr(Config, "MCM_MEMORY_WEIGHT", 0.20) or 0.20)
    regulation_weight = float(getattr(Config, "MCM_REGULATION_WEIGHT", 0.25) or 0.25)

    mcm_direction = (
        float(mcm_snapshot.get("mean_energy", 0.0) or 0.0) * pressure_weight
        + float(mcm_snapshot.get("mean_motivation", 0.0) or 0.0) * 0.10
        + memory_center * memory_weight
    )

    regulation_pressure = float(mcm_snapshot.get("regulation_pressure", 0.0) or 0.0)
    memory_penalty = min(0.42, max(0.0, memory_strength - 12.0) * 0.012)
    regulation_penalty = min(
        0.52,
        max(0.0, regulation_pressure - 0.85) * (regulation_weight * 0.34),
    )

    focus_long_bias = max(0.0, focus_point) * (0.20 + target_lock * 0.14 + focus_confidence * 0.10)
    focus_short_bias = max(0.0, -focus_point) * (0.20 + target_lock * 0.14 + focus_confidence * 0.10)
    drift_penalty = max(0.0, abs(target_drift) - 0.28) * 0.12
    inhibition_penalty = inhibition_level * 0.18
    habituation_penalty = habituation_level * 0.12
    competition_long_bias = max(0.0, competition_bias) * 0.28
    competition_short_bias = max(0.0, -competition_bias) * 0.28

    long_score = long_score + mcm_direction - regulation_penalty - memory_penalty + focus_long_bias + competition_long_bias - drift_penalty - inhibition_penalty - habituation_penalty
    short_score = short_score - mcm_direction - regulation_penalty - memory_penalty + focus_short_bias + competition_short_bias - drift_penalty - inhibition_penalty - habituation_penalty

    selected_attractor = str(mcm_snapshot.get("attractor", "neutral") or "neutral")
    self_state = str(mcm_snapshot.get("self_state", "stable") or "stable")

    long_allowed = True
    short_allowed = True
    reject_reason = None

    if selected_attractor == "defense":
        long_score -= 0.10
        short_score -= 0.10
        if abs(coherence) < 0.10 and abs(return_intensity) < 0.06:
            long_allowed = False
            short_allowed = False
            reject_reason = "defense_block"
    elif selected_attractor == "explore":
        long_score -= 0.03
        short_score -= 0.03
    elif selected_attractor == "analysis":
        long_score -= 0.08
        short_score -= 0.08
    elif selected_attractor == "cooperate":
        if abs(coherence) < 0.10:
            long_score -= 0.04
            short_score -= 0.04

    if self_state == "stressed":
        long_score -= 0.14
        short_score -= 0.14
        if abs(coherence) < 0.12 and abs(return_intensity) < 0.08:
            long_allowed = False
            short_allowed = False
            reject_reason = "stressed_block"

    elif self_state == "excited":
        long_score -= 0.03
        short_score -= 0.03

    if abs(return_intensity) < 0.05:
        long_score -= 0.03
        short_score -= 0.03

    if observation_mode:
        long_score -= 0.10
        short_score -= 0.10
        if reject_reason is None and max(long_score, short_score) < 0.34:
            long_allowed = False
            short_allowed = False
            reject_reason = "observation_mode"

    if bool(getattr(Config, "MCM_ATTRACTOR_LONG_ALLOW", True)) is False:
        long_allowed = False

    if bool(getattr(Config, "MCM_ATTRACTOR_SHORT_ALLOW", True)) is False:
        short_allowed = False

    min_score = 0.18
    min_edge = 0.08

    side = "WAIT"
    best_score = 0.0

    if long_allowed and long_score > min_score and (long_score - short_score) > min_edge:
        side = "LONG"
        best_score = long_score
    elif short_allowed and short_score > min_score and (short_score - long_score) > min_edge:
        side = "SHORT"
        best_score = short_score
    elif reject_reason is None:
        reject_reason = "fused_score_too_low"

    rr_value = float(getattr(Config, "RR", 2.0) or 2.0)
    risk_pct = float(getattr(Config, "BASE_RISK_PCT", 0.01) or 0.01)

    if self_state == "stressed":
        risk_pct *= float(getattr(Config, "MCM_STRESS_RISK_FACTOR", 0.75) or 0.75)
        rr_value = max(float(getattr(Config, "MIN_RR", rr_value) or rr_value), rr_value * 0.92)
    elif self_state == "excited":
        rr_value *= float(getattr(Config, "MCM_EXCITED_RR_FACTOR", 1.15) or 1.15)
        rr_value = min(rr_value, float(getattr(Config, "MAX_RR", rr_value) or rr_value))

    _mcm_decision_debug(
        "MCM_DECISION | "
        f"long_score={long_score:.4f} "
        f"short_score={short_score:.4f} "
        f"memory_center={memory_center:.4f} "
        f"memory_strength={memory_strength:.0f} "
        f"self_state={self_state} "
        f"attractor={selected_attractor} "
        f"best_score={best_score:.4f} "
        f"reject_reason={reject_reason or '-'}"
    )

    return {
        "decision": side,
        "rr_value": float(rr_value),
        "risk_pct": float(risk_pct),
        "long_score": float(long_score),
        "short_score": float(short_score),
        "self_state": self_state,
        "attractor": selected_attractor,
        "reject_reason": reject_reason,
        "inhibition_level": float(inhibition_level),
        "habituation_level": float(habituation_level),
        "competition_bias": float(competition_bias),
        "observation_mode": bool(observation_mode),
    }

# --------------------------------------------------
# update target model
# --------------------------------------------------
def update_target_model(bot, candle_state, focus):

    if bot is None:
        return None

    focus_point = float(focus.get("focus_direction", 0.0) or 0.0)
    focus_confidence = float(focus.get("focus_confidence", 0.0) or 0.0)
    target_lock = float(focus.get("target_lock", 0.0) or 0.0)
    return_intensity = float(candle_state.get("return_intensity", 0.0) or 0.0)

    previous_focus_point = float(getattr(bot, "focus_point", 0.0) or 0.0)

    bot.focus_point = float((previous_focus_point * 0.55) + (focus_point * 0.45))
    bot.focus_confidence = float((float(getattr(bot, "focus_confidence", 0.0) or 0.0) * 0.45) + (focus_confidence * 0.55))
    bot.target_lock = float((float(getattr(bot, "target_lock", 0.0) or 0.0) * 0.40) + (target_lock * 0.60))
    bot.target_drift = float(return_intensity - bot.focus_point)

    return {
        "focus_point": float(bot.focus_point),
        "focus_confidence": float(bot.focus_confidence),
        "target_lock": float(bot.target_lock),
        "target_drift": float(bot.target_drift),
    }


# --------------------------------------------------
def update_expectation_pressure_state(bot, candle_state, stimulus, snapshot, decision="WAIT"):

    if bot is None:
        return None

    focus = dict((stimulus or {}).get("focus", {}) or {})
    filtered_vision = dict((stimulus or {}).get("filtered_vision", {}) or {})
    snapshot_state = dict(snapshot or {})
    candle = dict(candle_state or {})

    focus_confidence = float(focus.get("focus_confidence", 0.0) or 0.0)
    target_lock = float(focus.get("target_lock", 0.0) or 0.0)
    signal_relevance = float(focus.get("signal_relevance", 0.0) or 0.0)
    noise_damp = float(focus.get("noise_damp", 0.0) or 0.0)
    filtered_target_map = float(filtered_vision.get("target_map", 0.0) or 0.0)
    filtered_threat_map = float(filtered_vision.get("threat_map", 0.0) or 0.0)
    filtered_optic_flow = float(filtered_vision.get("optic_flow", 0.0) or 0.0)
    return_intensity = float(candle.get("return_intensity", 0.0) or 0.0)
    close_position = float(candle.get("close_position", 0.0) or 0.0)

    prior_entry_expectation = float(getattr(bot, "entry_expectation", 0.0) or 0.0)
    prior_target_expectation = float(getattr(bot, "target_expectation", 0.0) or 0.0)
    prior_approach_pressure = float(getattr(bot, "approach_pressure", 0.0) or 0.0)
    prior_pressure_release = float(getattr(bot, "pressure_release", 0.0) or 0.0)
    experience_regulation = float(getattr(bot, "experience_regulation", 0.0) or 0.0)
    reflection_maturity = float(getattr(bot, "reflection_maturity", 0.0) or 0.0)
    load_bearing_capacity = float(getattr(bot, "load_bearing_capacity", 0.0) or 0.0)
    protective_width_regulation = float(getattr(bot, "protective_width_regulation", 0.0) or 0.0)
    protective_courage = float(getattr(bot, "protective_courage", 0.0) or 0.0)
    inhibition_level = float(getattr(bot, "inhibition_level", 0.0) or 0.0)
    observation_mode = bool(getattr(bot, "observation_mode", False))
    stress_pressure = max(
        0.0,
        min(
            1.0,
            max(0.0, float(snapshot_state.get("regulation_pressure", 0.0) or 0.0) / 2.2),
        ),
    )

    decision_value = str(decision or "WAIT").upper().strip()
    has_position = isinstance(getattr(bot, "position", None), dict)
    has_pending_entry = isinstance(getattr(bot, "pending_entry", None), dict)

    entry_anchor = max(
        0.0,
        min(
            1.0,
            (target_lock * 0.34)
            + (focus_confidence * 0.28)
            + (signal_relevance * 0.20)
            + (max(0.0, filtered_target_map) * 0.10)
            + (max(0.0, filtered_optic_flow) * 0.05)
            - (noise_damp * 0.08)
            - (filtered_threat_map * 0.06),
        ),
    )

    target_anchor = max(
        0.0,
        min(
            1.0,
            (target_lock * 0.38)
            + (focus_confidence * 0.18)
            + (signal_relevance * 0.16)
            + (max(0.0, filtered_target_map) * 0.16)
            + (max(0.0, abs(close_position)) * 0.06)
            - (noise_damp * 0.06),
        ),
    )

    if has_position:
        entry_expectation_target = 0.0
        target_expectation_target = min(1.0, target_anchor + 0.18)
    elif has_pending_entry or decision_value in ("LONG", "SHORT"):
        entry_expectation_target = min(1.0, entry_anchor + 0.16)
        target_expectation_target = target_anchor * 0.35
    else:
        entry_expectation_target = entry_anchor
        target_expectation_target = 0.0

    if observation_mode:
        entry_expectation_target *= 0.82
        target_expectation_target *= 0.86

    expectation_bias = max(entry_expectation_target, target_expectation_target)
    approach_gain = max(
        0.0,
        (expectation_bias * 0.32)
        + (max(0.0, 0.45 - abs(float(getattr(bot, "target_drift", 0.0) or 0.0))) * 0.40)
        + (max(0.0, abs(return_intensity)) * 0.10)
        - (inhibition_level * 0.12)
        - (experience_regulation * 0.08),
    )

    missed_release = 0.0
    if decision_value == "WAIT" and prior_entry_expectation > 0.34 and prior_approach_pressure > 0.24:
        missed_release = min(1.0, (prior_entry_expectation * 0.42) + (prior_approach_pressure * 0.58))
    elif has_position is False and has_pending_entry is False and prior_target_expectation > 0.30 and prior_approach_pressure > 0.20:
        missed_release = min(1.0, (prior_target_expectation * 0.36) + (prior_approach_pressure * 0.52))

    release_decay = max(0.0, prior_pressure_release * 0.62)
    bot.entry_expectation = float(max(0.0, min(1.0, (prior_entry_expectation * 0.52) + (entry_expectation_target * 0.48))))
    bot.target_expectation = float(max(0.0, min(1.0, (prior_target_expectation * 0.54) + (target_expectation_target * 0.46))))
    bot.approach_pressure = float(max(0.0, min(1.0, (prior_approach_pressure * 0.58) + approach_gain - (missed_release * 0.44))))
    bot.pressure_release = float(max(0.0, min(1.0, release_decay + missed_release)))
    bot.experience_regulation = float(max(0.0, min(1.0, (experience_regulation * 0.985) + (reflection_maturity * 0.010))))
    bot.reflection_maturity = float(max(0.0, min(1.0, (reflection_maturity * 0.996) + (abs(snapshot_state.get("mean_velocity", 0.0) or 0.0) * 0.002))))
    bot.load_bearing_capacity = float(max(0.0, min(1.0, (load_bearing_capacity * 0.82) + (bot.experience_regulation * 0.11) + (bot.reflection_maturity * 0.08) - (bot.pressure_release * 0.03))))
    bot.protective_width_regulation = float(max(0.0, min(
        1.0,
        (protective_width_regulation * 0.68)
        + (bot.approach_pressure * 0.24)
        + (bot.pressure_release * 0.34)
        + (bot.experience_regulation * 0.26)
        + (bot.reflection_maturity * 0.14)
        + (stress_pressure * 0.10)
        - (inhibition_level * 0.08),
    )))
    bot.protective_courage = float(max(0.0, min(
        0.86,
        (protective_courage * 0.72)
        + (bot.load_bearing_capacity * 0.20)
        + (bot.reflection_maturity * 0.12)
        + (max(0.0, 1.0 - noise_damp) * 0.06)
        - (bot.pressure_release * 0.14)
        - (filtered_threat_map * 0.10),
    )))

    return {
        "entry_expectation": float(bot.entry_expectation),
        "target_expectation": float(bot.target_expectation),
        "approach_pressure": float(bot.approach_pressure),
        "pressure_release": float(bot.pressure_release),
        "experience_regulation": float(bot.experience_regulation),
        "reflection_maturity": float(bot.reflection_maturity),
        "load_bearing_capacity": float(bot.load_bearing_capacity),
        "protective_width_regulation": float(bot.protective_width_regulation),
        "protective_courage": float(bot.protective_courage),
    }


# --------------------------------------------------
def update_experience_state(bot, outcome_reason):

    if bot is None:
        return None

    reason = str(outcome_reason or "").strip().lower()

    prior_release = float(getattr(bot, "pressure_release", 0.0) or 0.0)
    prior_regulation = float(getattr(bot, "experience_regulation", 0.0) or 0.0)
    prior_maturity = float(getattr(bot, "reflection_maturity", 0.0) or 0.0)
    prior_entry_expectation = float(getattr(bot, "entry_expectation", 0.0) or 0.0)
    prior_target_expectation = float(getattr(bot, "target_expectation", 0.0) or 0.0)
    prior_pressure = float(getattr(bot, "approach_pressure", 0.0) or 0.0)
    prior_load_bearing_capacity = float(getattr(bot, "load_bearing_capacity", 0.0) or 0.0)
    prior_protective_width_regulation = float(getattr(bot, "protective_width_regulation", 0.0) or 0.0)
    prior_protective_courage = float(getattr(bot, "protective_courage", 0.0) or 0.0)

    release_gain = 0.0
    regulation_gain = 0.0
    maturity_gain = 0.0

    if reason == "tp_hit":
        release_gain = 0.72 + (prior_pressure * 0.18)
        regulation_gain = 0.08 + (prior_target_expectation * 0.06)
        maturity_gain = 0.04
    elif reason == "sl_hit":
        release_gain = 0.82 + (prior_pressure * 0.22)
        regulation_gain = 0.05 + (prior_regulation * 0.02)
        maturity_gain = 0.06
    elif reason in ("cancel", "timeout"):
        release_gain = 0.58 + (prior_entry_expectation * 0.18)
        regulation_gain = 0.04
        maturity_gain = 0.05
    elif reason in ("reward_too_small", "rr_too_low", "sl_distance_too_high"):
        release_gain = 0.46 + (prior_entry_expectation * 0.16)
        regulation_gain = 0.03
        maturity_gain = 0.04

    bot.pressure_release = float(max(0.0, min(1.0, (prior_release * 0.30) + release_gain)))
    bot.approach_pressure = float(max(0.0, min(1.0, prior_pressure * 0.36)))
    bot.entry_expectation = float(max(0.0, min(1.0, prior_entry_expectation * 0.42)))
    bot.target_expectation = float(max(0.0, min(1.0, prior_target_expectation * 0.34)))
    bot.experience_regulation = float(max(0.0, min(1.0, (prior_regulation * 0.82) + regulation_gain + (prior_maturity * 0.04))))
    bot.reflection_maturity = float(max(0.0, min(1.0, (prior_maturity * 0.96) + maturity_gain + (abs(release_gain - regulation_gain) * 0.04))))
    bot.load_bearing_capacity = float(max(0.0, min(
        1.0,
        (prior_load_bearing_capacity * 0.76)
        + (bot.experience_regulation * 0.22)
        + (bot.reflection_maturity * 0.16)
        - (bot.pressure_release * 0.10),
    )))
    bot.protective_width_regulation = float(max(0.0, min(
        1.0,
        (prior_protective_width_regulation * 0.58)
        + (bot.pressure_release * 0.36)
        + (bot.experience_regulation * 0.28)
        + (bot.reflection_maturity * 0.18)
        + (prior_pressure * 0.14),
    )))
    bot.protective_courage = float(max(0.0, min(
        0.86,
        (prior_protective_courage * 0.62)
        + (bot.load_bearing_capacity * 0.16)
        + (bot.reflection_maturity * 0.10)
        - (bot.pressure_release * 0.16),
    )))

    return {
        "entry_expectation": float(bot.entry_expectation),
        "target_expectation": float(bot.target_expectation),
        "approach_pressure": float(bot.approach_pressure),
        "pressure_release": float(bot.pressure_release),
        "experience_regulation": float(bot.experience_regulation),
        "reflection_maturity": float(bot.reflection_maturity),
        "load_bearing_capacity": float(bot.load_bearing_capacity),
        "protective_width_regulation": float(bot.protective_width_regulation),
        "protective_courage": float(bot.protective_courage),
    }


# --------------------------------------------------
def build_state_signature(candle_state, tension_state, snapshot, stimulus, bot=None):

    focus = dict(stimulus.get("focus", {}) or {})
    filtered_vision = dict(stimulus.get("filtered_vision", {}) or {})
    strongest_memory = dict((snapshot.get("strongest_memory") or {}) or {})

    focus_point = float(getattr(bot, "focus_point", 0.0) or 0.0) if bot is not None else 0.0
    focus_confidence = float(getattr(bot, "focus_confidence", 0.0) or 0.0) if bot is not None else 0.0
    target_lock = float(getattr(bot, "target_lock", 0.0) or 0.0) if bot is not None else 0.0
    target_drift = float(getattr(bot, "target_drift", 0.0) or 0.0) if bot is not None else 0.0
    entry_expectation = float(getattr(bot, "entry_expectation", 0.0) or 0.0) if bot is not None else 0.0
    target_expectation = float(getattr(bot, "target_expectation", 0.0) or 0.0) if bot is not None else 0.0
    approach_pressure = float(getattr(bot, "approach_pressure", 0.0) or 0.0) if bot is not None else 0.0
    pressure_release = float(getattr(bot, "pressure_release", 0.0) or 0.0) if bot is not None else 0.0
    experience_regulation = float(getattr(bot, "experience_regulation", 0.0) or 0.0) if bot is not None else 0.0
    reflection_maturity = float(getattr(bot, "reflection_maturity", 0.0) or 0.0) if bot is not None else 0.0
    load_bearing_capacity = float(getattr(bot, "load_bearing_capacity", 0.0) or 0.0) if bot is not None else 0.0
    protective_width_regulation = float(getattr(bot, "protective_width_regulation", 0.0) or 0.0) if bot is not None else 0.0
    protective_courage = float(getattr(bot, "protective_courage", 0.0) or 0.0) if bot is not None else 0.0

    coherence = float(tension_state.get("coherence", 0.0) or 0.0)
    energy = float(tension_state.get("energy", 0.0) or 0.0)
    asymmetry = int(tension_state.get("asymmetry", 0) or 0)
    return_intensity = float(candle_state.get("return_intensity", 0.0) or 0.0)
    close_position = float(candle_state.get("close_position", 0.0) or 0.0)

    signal_relevance = float(focus.get("signal_relevance", 0.0) or 0.0)
    noise_damp = float(focus.get("noise_damp", 0.0) or 0.0)
    filtered_target_map = float(filtered_vision.get("target_map", 0.0) or 0.0)
    filtered_threat_map = float(filtered_vision.get("threat_map", 0.0) or 0.0)

    memory_center = float(strongest_memory.get("center", 0.0) or 0.0)
    memory_strength = int(strongest_memory.get("strength", 0) or 0)

    attractor = str(snapshot.get("attractor", "neutral") or "neutral")
    self_state = str(snapshot.get("self_state", "stable") or "stable")

    attractor_code = {
        "defense": -2,
        "analysis": -1,
        "neutral": 0,
        "cooperate": 1,
        "explore": 2,
    }.get(attractor, 0)

    self_state_code = {
        "stressed": -1,
        "stable": 0,
        "active": 1,
        "excited": 2,
    }.get(self_state, 0)

    signature_vector = [
        round(float(energy), 2),
        round(float(coherence), 2),
        int(asymmetry),
        round(float(close_position), 2),
        round(float(return_intensity), 2),
        round(float(focus_point), 2),
        round(float(focus_confidence), 2),
        round(float(target_lock), 2),
        round(float(target_drift), 2),
        round(float(entry_expectation), 2),
        round(float(target_expectation), 2),
        round(float(approach_pressure), 2),
        round(float(pressure_release), 2),
        round(float(experience_regulation), 2),
        round(float(reflection_maturity), 2),
        round(float(load_bearing_capacity), 2),
        round(float(protective_width_regulation), 2),
        round(float(protective_courage), 2),
        round(float(signal_relevance), 2),
        round(float(noise_damp), 2),
        round(float(filtered_target_map), 2),
        round(float(filtered_threat_map), 2),
        round(float(memory_center), 2),
        int(memory_strength),
        int(attractor_code),
        int(self_state_code),
    ]

    signature_key = "|".join(
        [
            f"e:{round(float(energy) / 0.25) * 0.25:.2f}",
            f"c:{round(float(coherence) / 0.20) * 0.20:.2f}",
            f"a:{int(asymmetry)}",
            f"cp:{round(float(close_position) / 0.25) * 0.25:.2f}",
            f"ri:{round(float(return_intensity) / 0.20) * 0.20:.2f}",
            f"fp:{round(float(focus_point) / 0.20) * 0.20:.2f}",
            f"fc:{round(float(focus_confidence) / 0.20) * 0.20:.2f}",
            f"tl:{round(float(target_lock) / 0.20) * 0.20:.2f}",
            f"td:{round(float(target_drift) / 0.20) * 0.20:.2f}",
            f"ee:{round(float(entry_expectation) / 0.20) * 0.20:.2f}",
            f"te:{round(float(target_expectation) / 0.20) * 0.20:.2f}",
            f"ap:{round(float(approach_pressure) / 0.20) * 0.20:.2f}",
            f"pr:{round(float(pressure_release) / 0.20) * 0.20:.2f}",
            f"er:{round(float(experience_regulation) / 0.20) * 0.20:.2f}",
            f"rm:{round(float(reflection_maturity) / 0.20) * 0.20:.2f}",
            f"lb:{round(float(load_bearing_capacity) / 0.20) * 0.20:.2f}",
            f"pw:{round(float(protective_width_regulation) / 0.20) * 0.20:.2f}",
            f"pc:{round(float(protective_courage) / 0.20) * 0.20:.2f}",
            f"sr:{round(float(signal_relevance) / 0.20) * 0.20:.2f}",
            f"nd:{round(float(noise_damp) / 0.20) * 0.20:.2f}",
            f"tm:{round(float(filtered_target_map) / 0.25) * 0.25:.2f}",
            f"th:{round(float(filtered_threat_map) / 0.25) * 0.25:.2f}",
            f"mc:{round(float(memory_center) / 0.25) * 0.25:.2f}",
            f"ms:{int(min(12, max(0, memory_strength)))}",
            f"at:{int(attractor_code)}",
            f"ss:{int(self_state_code)}",
        ]
    )

    return {
        "signature_key": str(signature_key),
        "signature_vector": list(signature_vector),
        "attractor_code": int(attractor_code),
        "self_state_code": int(self_state_code),
    }

# --------------------------------------------------
# context cluster
# --------------------------------------------------
def decay_weak_cluster(bot):

    if bot is None:
        return None

    cluster_map = getattr(bot, "context_clusters", None)
    if not isinstance(cluster_map, dict):
        bot.context_clusters = {}
        return None

    decay_score = float(getattr(Config, "MCM_CONTEXT_DECAY", 0.992) or 0.992)
    max_age = int(getattr(Config, "MCM_CONTEXT_MAX_AGE", 320) or 320)
    min_trust = float(getattr(Config, "MCM_CONTEXT_MIN_TRUST", 0.06) or 0.06)

    updated_clusters = {}

    for cluster_id, item in cluster_map.items():
        if not isinstance(item, dict):
            continue

        aged_item = dict(item)
        aged_item["age"] = int(aged_item.get("age", 0) or 0) + 1
        aged_item["score"] = float(aged_item.get("score", 0.0) or 0.0) * decay_score
        aged_item["trust"] = float(aged_item.get("trust", 0.0) or 0.0) * 0.998

        if int(aged_item["age"]) > max_age and abs(float(aged_item["score"])) < 0.18 and float(aged_item["trust"]) < min_trust:
            continue

        updated_clusters[str(cluster_id)] = aged_item

    bot.context_clusters = updated_clusters
    return updated_clusters


# --------------------------------------------------
def classify_state_cluster(bot, state_signature):

    if bot is None:
        return None

    signature = dict(state_signature or {})
    signature_key = str(signature.get("signature_key", "") or "").strip()
    signature_vector = list(signature.get("signature_vector", []) or [])

    if not signature_key or not signature_vector:
        return None

    if not isinstance(getattr(bot, "context_clusters", None), dict):
        bot.context_clusters = {}

    decay_weak_cluster(bot)

    cluster_threshold = float(getattr(Config, "MCM_CONTEXT_MATCH_THRESHOLD", 0.28) or 0.28)
    current_vector = np.asarray(signature_vector, dtype=float)

    nearest_cluster_id = None
    nearest_cluster = None
    nearest_distance = None

    for cluster_id, item in bot.context_clusters.items():
        if not isinstance(item, dict):
            continue

        center_vector = list(item.get("center_vector", []) or [])
        if len(center_vector) != len(signature_vector):
            continue

        center_array = np.asarray(center_vector, dtype=float)
        distance = float(np.mean(np.abs(current_vector - center_array)))

        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest_cluster_id = str(cluster_id)
            nearest_cluster = item

    if nearest_cluster is None or nearest_distance is None or nearest_distance > cluster_threshold:
        bot.context_cluster_seq = int(getattr(bot, "context_cluster_seq", 0) or 0) + 1
        nearest_cluster_id = f"ctx_{int(bot.context_cluster_seq)}"
        nearest_cluster = {
            "cluster_id": str(nearest_cluster_id),
            "center_vector": list(signature_vector),
            "variance": 0.0,
            "radius": 0.0,
            "seen": 0,
            "tp": 0,
            "sl": 0,
            "cancel": 0,
            "timeout": 0,
            "score": 0.0,
            "trust": 0.12,
            "age": 0,
            "signature_keys": [str(signature_key)],
            "last_signature_key": str(signature_key),
            "last_outcome": None,
            "last_distance": 0.0,
        }
        bot.context_clusters[str(nearest_cluster_id)] = nearest_cluster
        nearest_distance = 0.0

    seen_before = int(nearest_cluster.get("seen", 0) or 0)
    learn_rate = 1.0 / float(max(1, min(24, seen_before + 1)))
    center_array = np.asarray(list(nearest_cluster.get("center_vector", []) or signature_vector), dtype=float)
    new_center = center_array + ((current_vector - center_array) * learn_rate)
    distance_now = float(np.mean(np.abs(current_vector - new_center)))

    nearest_cluster["center_vector"] = [float(round(value, 4)) for value in new_center.tolist()]
    nearest_cluster["seen"] = seen_before + 1
    nearest_cluster["age"] = 0
    nearest_cluster["radius"] = float((float(nearest_cluster.get("radius", 0.0) or 0.0) * 0.72) + (distance_now * 0.28))
    nearest_cluster["variance"] = float((float(nearest_cluster.get("variance", 0.0) or 0.0) * 0.70) + ((distance_now ** 2) * 0.30))
    nearest_cluster["trust"] = float(min(1.0, (float(nearest_cluster.get("trust", 0.0) or 0.0) * 0.82) + 0.10))
    nearest_cluster["last_signature_key"] = str(signature_key)
    nearest_cluster["last_distance"] = float(nearest_distance)

    signature_keys = list(nearest_cluster.get("signature_keys", []) or [])
    if signature_key not in signature_keys:
        signature_keys.append(str(signature_key))
    nearest_cluster["signature_keys"] = signature_keys[-24:]

    bot.context_clusters[str(nearest_cluster_id)] = nearest_cluster
    bot.last_context_cluster_id = str(nearest_cluster_id)
    bot.last_context_cluster_key = str(signature_key)

    return {
        "cluster_id": str(nearest_cluster_id),
        "distance": float(nearest_distance),
        "seen": int(nearest_cluster.get("seen", 0) or 0),
        "score": float(nearest_cluster.get("score", 0.0) or 0.0),
        "trust": float(nearest_cluster.get("trust", 0.0) or 0.0),
        "variance": float(nearest_cluster.get("variance", 0.0) or 0.0),
        "radius": float(nearest_cluster.get("radius", 0.0) or 0.0),
        "tp": int(nearest_cluster.get("tp", 0) or 0),
        "sl": int(nearest_cluster.get("sl", 0) or 0),
        "cancel": int(nearest_cluster.get("cancel", 0) or 0),
        "timeout": int(nearest_cluster.get("timeout", 0) or 0),
        "last_outcome": nearest_cluster.get("last_outcome"),
    }


# --------------------------------------------------
# --------------------------------------------------
def merge_similar_signatures(bot):

    if bot is None:
        return None

    cluster_map = getattr(bot, "context_clusters", None)
    if not isinstance(cluster_map, dict) or len(cluster_map) < 2:
        return cluster_map

    merge_threshold = float(getattr(Config, "MCM_CONTEXT_MERGE_THRESHOLD", 0.16) or 0.16)
    cluster_ids = list(cluster_map.keys())
    consumed_ids = set()
    merged_clusters = {}

    for idx, cluster_id in enumerate(cluster_ids):
        if cluster_id in consumed_ids:
            continue

        base_item = dict(cluster_map.get(cluster_id) or {})
        base_vector = list(base_item.get("center_vector", []) or [])
        if not base_vector:
            merged_clusters[str(cluster_id)] = base_item
            continue

        base_array = np.asarray(base_vector, dtype=float)

        for other_id in cluster_ids[idx + 1:]:
            if other_id in consumed_ids:
                continue

            other_item = dict(cluster_map.get(other_id) or {})
            other_vector = list(other_item.get("center_vector", []) or [])
            if len(other_vector) != len(base_vector):
                continue

            other_array = np.asarray(other_vector, dtype=float)
            distance = float(np.mean(np.abs(base_array - other_array)))

            if distance > merge_threshold:
                continue

            base_seen = int(base_item.get("seen", 0) or 0)
            other_seen = int(other_item.get("seen", 0) or 0)
            total_seen = max(1, base_seen + other_seen)

            merged_center = ((base_array * base_seen) + (other_array * other_seen)) / float(total_seen)
            base_item["center_vector"] = [float(round(value, 4)) for value in merged_center.tolist()]
            base_array = np.asarray(base_item["center_vector"], dtype=float)
            base_item["seen"] = int(total_seen)
            base_item["tp"] = int(base_item.get("tp", 0) or 0) + int(other_item.get("tp", 0) or 0)
            base_item["sl"] = int(base_item.get("sl", 0) or 0) + int(other_item.get("sl", 0) or 0)
            base_item["cancel"] = int(base_item.get("cancel", 0) or 0) + int(other_item.get("cancel", 0) or 0)
            base_item["timeout"] = int(base_item.get("timeout", 0) or 0) + int(other_item.get("timeout", 0) or 0)
            base_item["score"] = float(base_item.get("score", 0.0) or 0.0) + float(other_item.get("score", 0.0) or 0.0)
            base_item["trust"] = float(min(1.0, max(float(base_item.get("trust", 0.0) or 0.0), float(other_item.get("trust", 0.0) or 0.0)) + 0.06))
            base_item["variance"] = float((float(base_item.get("variance", 0.0) or 0.0) + float(other_item.get("variance", 0.0) or 0.0) + (distance ** 2)) / 3.0)
            base_item["radius"] = float(max(float(base_item.get("radius", 0.0) or 0.0), float(other_item.get("radius", 0.0) or 0.0), distance))
            base_item["age"] = int(min(int(base_item.get("age", 0) or 0), int(other_item.get("age", 0) or 0)))

            merged_keys = list(base_item.get("signature_keys", []) or [])
            merged_keys.extend(list(other_item.get("signature_keys", []) or []))
            unique_keys = []
            for key in merged_keys:
                key_value = str(key)
                if key_value not in unique_keys:
                    unique_keys.append(key_value)
            base_item["signature_keys"] = unique_keys[-32:]
            base_item["last_signature_key"] = str(base_item.get("last_signature_key") or other_item.get("last_signature_key") or "")
            base_item["last_outcome"] = other_item.get("last_outcome") or base_item.get("last_outcome")
            base_item["last_distance"] = float(min(float(base_item.get("last_distance", 0.0) or 0.0), float(other_item.get("last_distance", 0.0) or 0.0), distance))

            consumed_ids.add(str(other_id))

            if str(getattr(bot, "last_context_cluster_id", "") or "") == str(other_id):
                bot.last_context_cluster_id = str(cluster_id)

        merged_clusters[str(cluster_id)] = base_item

    bot.context_clusters = merged_clusters
    return merged_clusters

# --------------------------------------------------
# --------------------------------------------------
def split_unstable_cluster(bot):

    if bot is None:
        return None

    cluster_map = getattr(bot, "context_clusters", None)
    if not isinstance(cluster_map, dict) or not cluster_map:
        return cluster_map

    split_variance = float(getattr(Config, "MCM_CONTEXT_SPLIT_VARIANCE", 0.085) or 0.085)
    split_radius = float(getattr(Config, "MCM_CONTEXT_SPLIT_RADIUS", 0.24) or 0.24)
    updated_clusters = {}

    for cluster_id, item in cluster_map.items():
        cluster_item = dict(item or {})
        seen = int(cluster_item.get("seen", 0) or 0)
        variance = float(cluster_item.get("variance", 0.0) or 0.0)
        radius = float(cluster_item.get("radius", 0.0) or 0.0)
        center_vector = list(cluster_item.get("center_vector", []) or [])

        if seen < 8 or not center_vector or (variance <= split_variance and radius <= split_radius):
            updated_clusters[str(cluster_id)] = cluster_item
            continue

        bot.context_cluster_seq = int(getattr(bot, "context_cluster_seq", 0) or 0) + 1
        child_cluster_id = f"ctx_{int(bot.context_cluster_seq)}"

        split_axis = int(np.argmax(np.abs(np.asarray(center_vector, dtype=float)))) if center_vector else 0
        offset_size = max(0.04, min(0.18, radius * 0.50 + (variance * 0.35)))

        parent_center = list(center_vector)
        child_center = list(center_vector)

        parent_center[split_axis] = float(round(parent_center[split_axis] - offset_size, 4))
        child_center[split_axis] = float(round(child_center[split_axis] + offset_size, 4))

        parent_tp = int(cluster_item.get("tp", 0) or 0)
        parent_sl = int(cluster_item.get("sl", 0) or 0)
        parent_cancel = int(cluster_item.get("cancel", 0) or 0)
        parent_timeout = int(cluster_item.get("timeout", 0) or 0)

        child_item = dict(cluster_item)
        child_item["cluster_id"] = str(child_cluster_id)
        child_item["center_vector"] = child_center
        child_item["seen"] = max(1, seen // 2)
        child_item["tp"] = max(0, parent_tp // 2)
        child_item["sl"] = max(0, parent_sl // 2)
        child_item["cancel"] = max(0, parent_cancel // 2)
        child_item["timeout"] = max(0, parent_timeout // 2)
        child_item["score"] = float(float(cluster_item.get("score", 0.0) or 0.0) * 0.46)
        child_item["trust"] = float(max(0.08, float(cluster_item.get("trust", 0.0) or 0.0) * 0.72))
        child_item["variance"] = float(max(0.0, variance * 0.58))
        child_item["radius"] = float(max(0.0, radius * 0.62))
        child_item["age"] = 0
        child_item["signature_keys"] = list((list(cluster_item.get("signature_keys", []) or []))[-12:])
        child_item["last_distance"] = float(radius * 0.50)

        cluster_item["center_vector"] = parent_center
        cluster_item["seen"] = max(1, seen - int(child_item["seen"]))
        cluster_item["tp"] = max(0, parent_tp - int(child_item["tp"]))
        cluster_item["sl"] = max(0, parent_sl - int(child_item["sl"]))
        cluster_item["cancel"] = max(0, parent_cancel - int(child_item["cancel"]))
        cluster_item["timeout"] = max(0, parent_timeout - int(child_item["timeout"]))
        cluster_item["score"] = float(float(cluster_item.get("score", 0.0) or 0.0) * 0.54)
        cluster_item["trust"] = float(max(0.08, float(cluster_item.get("trust", 0.0) or 0.0) * 0.76))
        cluster_item["variance"] = float(max(0.0, variance * 0.54))
        cluster_item["radius"] = float(max(0.0, radius * 0.58))
        cluster_item["age"] = 0
        cluster_item["last_distance"] = float(radius * 0.50)

        updated_clusters[str(cluster_id)] = cluster_item
        updated_clusters[str(child_cluster_id)] = child_item

    bot.context_clusters = updated_clusters
    return updated_clusters
# --------------------------------------------------
# --------------------------------------------------
def update_context_cluster_outcome(bot, cluster_id, outcome=None):

    if bot is None:
        return None

    cluster_map = getattr(bot, "context_clusters", None)
    if not isinstance(cluster_map, dict):
        return None

    cluster_key = str(cluster_id or "").strip()
    if not cluster_key:
        return None

    cluster = cluster_map.get(cluster_key)
    if not isinstance(cluster, dict):
        return None

    reason = str(outcome or "").strip().lower()

    if reason == "tp_hit":
        cluster["tp"] = int(cluster.get("tp", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) + 1.00
        cluster["trust"] = float(min(1.0, float(cluster.get("trust", 0.0) or 0.0) + 0.08))
        cluster["last_outcome"] = "tp_hit"
    elif reason == "sl_hit":
        cluster["sl"] = int(cluster.get("sl", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) - 1.10
        cluster["trust"] = float(max(0.0, float(cluster.get("trust", 0.0) or 0.0) - 0.10))
        cluster["last_outcome"] = "sl_hit"
    elif reason == "cancel":
        cluster["cancel"] = int(cluster.get("cancel", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) - 0.35
        cluster["trust"] = float(max(0.0, float(cluster.get("trust", 0.0) or 0.0) - 0.04))
        cluster["last_outcome"] = "cancel"
    elif reason == "timeout":
        cluster["timeout"] = int(cluster.get("timeout", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) - 0.28
        cluster["trust"] = float(max(0.0, float(cluster.get("trust", 0.0) or 0.0) - 0.03))
        cluster["last_outcome"] = "timeout"
    elif reason == "reward_too_small":
        cluster["cancel"] = int(cluster.get("cancel", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) - 0.40
        cluster["trust"] = float(max(0.0, float(cluster.get("trust", 0.0) or 0.0) - 0.05))
        cluster["last_outcome"] = "reward_too_small"
    elif reason == "sl_distance_too_high":
        cluster["sl"] = int(cluster.get("sl", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) - 0.62
        cluster["trust"] = float(max(0.0, float(cluster.get("trust", 0.0) or 0.0) - 0.07))
        cluster["last_outcome"] = "sl_distance_too_high"
    elif reason == "rr_too_low":
        cluster["timeout"] = int(cluster.get("timeout", 0) or 0) + 1
        cluster["score"] = float(cluster.get("score", 0.0) or 0.0) - 0.48
        cluster["trust"] = float(max(0.0, float(cluster.get("trust", 0.0) or 0.0) - 0.05))
        cluster["last_outcome"] = "rr_too_low"

    cluster["score"] = float(max(-8.0, min(8.0, float(cluster.get("score", 0.0) or 0.0))))
    cluster["age"] = 0
    cluster_map[cluster_key] = cluster
    bot.context_clusters = cluster_map

    return {
        "cluster_id": str(cluster_key),
        "seen": int(cluster.get("seen", 0) or 0),
        "tp": int(cluster.get("tp", 0) or 0),
        "sl": int(cluster.get("sl", 0) or 0),
        "cancel": int(cluster.get("cancel", 0) or 0),
        "timeout": int(cluster.get("timeout", 0) or 0),
        "score": float(cluster.get("score", 0.0) or 0.0),
        "trust": float(cluster.get("trust", 0.0) or 0.0),
        "variance": float(cluster.get("variance", 0.0) or 0.0),
        "radius": float(cluster.get("radius", 0.0) or 0.0),
        "last_outcome": cluster.get("last_outcome"),
    }
# --------------------------------------------------
# --------------------------------------------------
def lookup_context_cluster(bot, state_signature):

    if bot is None:
        return None

    cluster_map = getattr(bot, "context_clusters", None)
    if not isinstance(cluster_map, dict) or not cluster_map:
        return None

    signature_vector = list((state_signature or {}).get("signature_vector", []) or [])
    if not signature_vector:
        return None

    current_vector = np.asarray(signature_vector, dtype=float)
    lookup_threshold = float(getattr(Config, "MCM_CONTEXT_LOOKUP_THRESHOLD", 0.30) or 0.30)

    nearest_cluster_id = None
    nearest_cluster = None
    nearest_distance = None

    for cluster_id, item in cluster_map.items():
        if not isinstance(item, dict):
            continue

        center_vector = list(item.get("center_vector", []) or [])
        if len(center_vector) != len(signature_vector):
            continue

        center_array = np.asarray(center_vector, dtype=float)
        distance = float(np.mean(np.abs(current_vector - center_array)))

        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest_cluster_id = str(cluster_id)
            nearest_cluster = item

    if nearest_cluster is None or nearest_distance is None or nearest_distance > lookup_threshold:
        return None

    return {
        "cluster_id": str(nearest_cluster_id),
        "distance": float(nearest_distance),
        "seen": int(nearest_cluster.get("seen", 0) or 0),
        "tp": int(nearest_cluster.get("tp", 0) or 0),
        "sl": int(nearest_cluster.get("sl", 0) or 0),
        "cancel": int(nearest_cluster.get("cancel", 0) or 0),
        "timeout": int(nearest_cluster.get("timeout", 0) or 0),
        "score": float(nearest_cluster.get("score", 0.0) or 0.0),
        "trust": float(nearest_cluster.get("trust", 0.0) or 0.0),
        "variance": float(nearest_cluster.get("variance", 0.0) or 0.0),
        "radius": float(nearest_cluster.get("radius", 0.0) or 0.0),
        "age": int(nearest_cluster.get("age", 0) or 0),
        "last_outcome": nearest_cluster.get("last_outcome"),
    }

# --------------------------------------------------
# update signature memory
# --------------------------------------------------
def update_signature_memory(bot, state_signature, outcome=None):

    if bot is None:
        return None

    signature = dict(state_signature or {})
    signature_key = str(signature.get("signature_key", "") or "").strip()
    signature_vector = list(signature.get("signature_vector", []) or [])

    if not signature_key:
        return None

    if not isinstance(getattr(bot, "signature_memory", None), dict):
        bot.signature_memory = {}

    updated_memory = {}

    for key, item in dict(getattr(bot, "signature_memory", {}) or {}).items():
        if not isinstance(item, dict):
            continue

        aged_item = {
            "seen": int(item.get("seen", 0) or 0),
            "tp": int(item.get("tp", 0) or 0),
            "sl": int(item.get("sl", 0) or 0),
            "cancel": int(item.get("cancel", 0) or 0),
            "timeout": int(item.get("timeout", 0) or 0),
            "score": float(item.get("score", 0.0) or 0.0) * 0.995,
            "last_outcome": item.get("last_outcome"),
            "age": int(item.get("age", 0) or 0) + 1,
            "signature_vector": list(item.get("signature_vector", []) or []),
        }

        if aged_item["age"] <= 250 or abs(float(aged_item["score"])) >= 0.18:
            updated_memory[str(key)] = aged_item

    bot.signature_memory = updated_memory

    memory = bot.signature_memory.get(signature_key)
    if not isinstance(memory, dict):
        memory = {
            "seen": 0,
            "tp": 0,
            "sl": 0,
            "cancel": 0,
            "timeout": 0,
            "score": 0.0,
            "last_outcome": None,
            "age": 0,
            "signature_vector": list(signature_vector),
        }

    memory["seen"] = int(memory.get("seen", 0) or 0) + 1
    memory["age"] = 0

    if signature_vector:
        memory["signature_vector"] = list(signature_vector)

    reason = str(outcome or "").strip().lower()

    if reason == "tp_hit":
        memory["tp"] = int(memory.get("tp", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) + 1.00
        memory["last_outcome"] = "tp_hit"

    elif reason == "sl_hit":
        memory["sl"] = int(memory.get("sl", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) - 1.10
        memory["last_outcome"] = "sl_hit"

    elif reason == "cancel":
        memory["cancel"] = int(memory.get("cancel", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) - 0.35
        memory["last_outcome"] = "cancel"

    elif reason == "timeout":
        memory["timeout"] = int(memory.get("timeout", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) - 0.28
        memory["last_outcome"] = "timeout"

    elif reason == "reward_too_small":
        memory["cancel"] = int(memory.get("cancel", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) - 0.40
        memory["last_outcome"] = "reward_too_small"

    elif reason == "sl_distance_too_high":
        memory["sl"] = int(memory.get("sl", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) - 0.62
        memory["last_outcome"] = "sl_distance_too_high"

    elif reason == "rr_too_low":
        memory["timeout"] = int(memory.get("timeout", 0) or 0) + 1
        memory["score"] = float(memory.get("score", 0.0) or 0.0) - 0.48
        memory["last_outcome"] = "rr_too_low"

    memory["score"] = float(max(-6.0, min(6.0, memory["score"])))

    bot.signature_memory[signature_key] = memory
    bot.last_signature_key = signature_key

    if reason:
        bot.last_signature_outcome = reason

    if len(bot.signature_memory) > 180:
        sorted_items = sorted(
            bot.signature_memory.items(),
            key=lambda item: (
                abs(float((item[1] or {}).get("score", 0.0) or 0.0)),
                -int((item[1] or {}).get("age", 0) or 0),
                int((item[1] or {}).get("seen", 0) or 0),
            ),
            reverse=True,
        )[:180]
        bot.signature_memory = dict(sorted_items)

    return {
        "signature_key": signature_key,
        "seen": int(memory.get("seen", 0) or 0),
        "tp": int(memory.get("tp", 0) or 0),
        "sl": int(memory.get("sl", 0) or 0),
        "cancel": int(memory.get("cancel", 0) or 0),
        "timeout": int(memory.get("timeout", 0) or 0),
        "score": float(memory.get("score", 0.0) or 0.0),
        "age": int(memory.get("age", 0) or 0),
        "last_outcome": memory.get("last_outcome"),
        "signature_vector": list(memory.get("signature_vector", []) or []),
    }

# --------------------------------------------------
# lookup signature context
# --------------------------------------------------
def lookup_signature_context(bot, state_signature):

    if bot is None:
        return None

    signature_key = str((state_signature or {}).get("signature_key", "") or "").strip()
    signature_vector = list((state_signature or {}).get("signature_vector", []) or [])

    if not signature_key or not signature_vector:
        return None

    signature_memory = getattr(bot, "signature_memory", None)
    if not isinstance(signature_memory, dict) or not signature_memory:
        return None

    nearest_key = None
    nearest_item = None
    nearest_distance = None

    current_vector = np.asarray(signature_vector, dtype=float)

    for key, item in signature_memory.items():
        if not isinstance(item, dict):
            continue

        candidate_vector = list(item.get("signature_vector", []) or [])
        if not candidate_vector:
            continue

        if len(candidate_vector) != len(signature_vector):
            continue

        candidate_array = np.asarray(candidate_vector, dtype=float)
        distance = float(np.mean(np.abs(current_vector - candidate_array)))

        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest_key = str(key)
            nearest_item = item

    if nearest_item is None or nearest_distance is None:
        return None

    if nearest_distance > 0.34:
        return None

    return {
        "signature_key": str(nearest_key),
        "distance": float(nearest_distance),
        "seen": int(nearest_item.get("seen", 0) or 0),
        "tp": int(nearest_item.get("tp", 0) or 0),
        "sl": int(nearest_item.get("sl", 0) or 0),
        "cancel": int(nearest_item.get("cancel", 0) or 0),
        "timeout": int(nearest_item.get("timeout", 0) or 0),
        "score": float(nearest_item.get("score", 0.0) or 0.0),
        "age": int(nearest_item.get("age", 0) or 0),
        "last_outcome": nearest_item.get("last_outcome"),
    }

# --------------------------------------------------
# ENTRY API
# --------------------------------------------------
def reinterpret_focus_by_signature(bot, fused, state_signature):

    if bot is None:
        return dict(fused or {})

    result = dict(fused or {})
    signature_context = lookup_signature_context(bot, state_signature)
    cluster_context = lookup_context_cluster(bot, state_signature)

    result["signature_bias"] = 0.0
    result["signature_block"] = False
    result["signature_key"] = "-"
    result["signature_quality"] = 0.0
    result["signature_distance"] = 0.0
    result["context_cluster_id"] = "-"
    result["context_cluster_bias"] = 0.0
    result["context_cluster_quality"] = 0.0
    result["context_cluster_distance"] = 0.0
    result["context_cluster_block"] = False

    long_score = float(result.get("long_score", 0.0) or 0.0)
    short_score = float(result.get("short_score", 0.0) or 0.0)

    if isinstance(signature_context, dict):
        score = float(signature_context.get("score", 0.0) or 0.0)
        seen = int(signature_context.get("seen", 0) or 0)
        tp_hits = int(signature_context.get("tp", 0) or 0)
        sl_hits = int(signature_context.get("sl", 0) or 0)
        cancel_hits = int(signature_context.get("cancel", 0) or 0)
        timeout_hits = int(signature_context.get("timeout", 0) or 0)
        distance = float(signature_context.get("distance", 0.0) or 0.0)
        resolved = max(1, tp_hits + sl_hits + cancel_hits + timeout_hits)
        hit_ratio = tp_hits / float(resolved)

        if seen >= 3:
            quality = (
                score * 0.10
                + (hit_ratio - 0.50) * 0.35
                - (max(0, sl_hits - tp_hits) * 0.04)
                - (distance * 0.30)
            )
            bias = max(-0.28, min(0.28, quality))

            if float(getattr(bot, "focus_point", 0.0) or 0.0) >= 0.0:
                long_score += bias
                short_score -= max(0.0, bias * 0.45)
            else:
                short_score += bias
                long_score -= max(0.0, bias * 0.45)

            result["signature_bias"] = float(bias)
            result["signature_quality"] = float(quality)

            if score <= -2.20 or (seen >= 5 and hit_ratio <= 0.18):
                result["decision"] = "WAIT"
                result["reject_reason"] = "signature_negative"
                result["signature_block"] = True

            bot.last_signature_context = {
                "signature_key": str(signature_context.get("signature_key", "-") or "-"),
                "distance": float(distance),
                "quality": float(quality),
                "score": float(score),
            }

        result["signature_key"] = str(signature_context.get("signature_key", "-") or "-")
        result["signature_distance"] = float(distance)

    if isinstance(cluster_context, dict):
        cluster_score = float(cluster_context.get("score", 0.0) or 0.0)
        cluster_seen = int(cluster_context.get("seen", 0) or 0)
        cluster_tp = int(cluster_context.get("tp", 0) or 0)
        cluster_sl = int(cluster_context.get("sl", 0) or 0)
        cluster_cancel = int(cluster_context.get("cancel", 0) or 0)
        cluster_timeout = int(cluster_context.get("timeout", 0) or 0)
        cluster_distance = float(cluster_context.get("distance", 0.0) or 0.0)
        cluster_trust = float(cluster_context.get("trust", 0.0) or 0.0)
        cluster_variance = float(cluster_context.get("variance", 0.0) or 0.0)

        cluster_resolved = max(1, cluster_tp + cluster_sl + cluster_cancel + cluster_timeout)
        cluster_hit_ratio = cluster_tp / float(cluster_resolved)

        if cluster_seen >= 3:
            cluster_quality = (
                cluster_score * 0.08
                + (cluster_hit_ratio - 0.50) * 0.42
                + (cluster_trust * 0.18)
                - (cluster_distance * 0.34)
                - (cluster_variance * 0.08)
            )
            cluster_bias = max(-0.24, min(0.24, cluster_quality))

            if float(getattr(bot, "focus_point", 0.0) or 0.0) >= 0.0:
                long_score += cluster_bias
                short_score -= max(0.0, cluster_bias * 0.40)
            else:
                short_score += cluster_bias
                long_score -= max(0.0, cluster_bias * 0.40)

            result["context_cluster_bias"] = float(cluster_bias)
            result["context_cluster_quality"] = float(cluster_quality)

            if cluster_score <= -2.60 or (cluster_seen >= 6 and cluster_hit_ratio <= 0.16):
                result["decision"] = "WAIT"
                result["reject_reason"] = "context_cluster_negative"
                result["context_cluster_block"] = True

        result["context_cluster_id"] = str(cluster_context.get("cluster_id", "-") or "-")
        result["context_cluster_distance"] = float(cluster_distance)

    result["long_score"] = float(long_score)
    result["short_score"] = float(short_score)
    return result

# --------------------------------------------------
# felt_state
# --------------------------------------------------
def build_felt_state(bot, candle_state, stimulus, snapshot, perception_state, decision="WAIT"):

    expectation_state = update_expectation_pressure_state(bot, candle_state, stimulus, snapshot, decision=decision)
    filtered_vision = dict((stimulus or {}).get("filtered_vision", {}) or {})
    perception = dict(perception_state or {})
    competition_abs = abs(float(getattr(bot, "competition_bias", 0.0) or 0.0)) if bot is not None else 0.0

    structure_quality = float(perception.get("structure_quality", 0.0) or 0.0)
    stress_relief_potential = float(perception.get("stress_relief_potential", 0.0) or 0.0)
    context_confidence = float(perception.get("context_confidence", 0.0) or 0.0)

    felt_risk = max(0.0, min(1.0, (float(filtered_vision.get("threat_map", 0.0) or 0.0) * 0.34) + (float(perception.get("uncertainty_score", 0.0) or 0.0) * 0.24) + (float(perception.get("noise_damp", 0.0) or 0.0) * 0.16) - (stress_relief_potential * 0.14)))
    felt_opportunity = max(0.0, min(1.0, (float(filtered_vision.get("target_map", 0.0) or 0.0) * 0.34) + (float(perception.get("signal_quality", 0.0) or 0.0) * 0.26) + (float(perception.get("target_lock", 0.0) or 0.0) * 0.18) + (structure_quality * 0.14)))
    felt_conflict = max(0.0, min(1.0, abs(felt_opportunity - felt_risk) * 0.18 + min(felt_opportunity, felt_risk) * 0.64 + (competition_abs * 0.10)))
    felt_pressure = max(0.0, min(1.0, (float((expectation_state or {}).get("approach_pressure", 0.0) or 0.0) * 0.44) + (float((expectation_state or {}).get("entry_expectation", 0.0) or 0.0) * 0.18) + (felt_opportunity * 0.12) + (felt_risk * 0.10) - (stress_relief_potential * 0.16)))
    felt_stability = max(0.0, min(1.0, 1.0 - (float(perception.get("uncertainty_score", 0.0) or 0.0) * 0.38) - (felt_conflict * 0.24) - (float((expectation_state or {}).get("pressure_release", 0.0) or 0.0) * 0.12) + (float((expectation_state or {}).get("experience_regulation", 0.0) or 0.0) * 0.18) + (context_confidence * 0.14)))

    market_feel_state = "balanced"
    if felt_risk > felt_opportunity and felt_risk >= 0.58:
        market_feel_state = "threatened"
    elif felt_opportunity > felt_risk and felt_opportunity >= 0.58:
        market_feel_state = "drawn"
    elif felt_conflict >= 0.52:
        market_feel_state = "conflicted"
    elif felt_stability < 0.34:
        market_feel_state = "unstable"

    return {
        "market_feel_state": str(market_feel_state),
        "felt_risk": float(felt_risk),
        "felt_opportunity": float(felt_opportunity),
        "felt_conflict": float(felt_conflict),
        "felt_pressure": float(felt_pressure),
        "felt_stability": float(felt_stability),
        "structure_quality": float(structure_quality),
        "stress_relief_potential": float(stress_relief_potential),
        "context_confidence": float(context_confidence),
        "entry_expectation": float((expectation_state or {}).get("entry_expectation", 0.0) or 0.0),
        "target_expectation": float((expectation_state or {}).get("target_expectation", 0.0) or 0.0),
        "approach_pressure": float((expectation_state or {}).get("approach_pressure", 0.0) or 0.0),
        "pressure_release": float((expectation_state or {}).get("pressure_release", 0.0) or 0.0),
        "experience_regulation": float((expectation_state or {}).get("experience_regulation", 0.0) or 0.0),
        "reflection_maturity": float((expectation_state or {}).get("reflection_maturity", 0.0) or 0.0),
        "load_bearing_capacity": float((expectation_state or {}).get("load_bearing_capacity", 0.0) or 0.0),
        "protective_width_regulation": float((expectation_state or {}).get("protective_width_regulation", 0.0) or 0.0),
        "protective_courage": float((expectation_state or {}).get("protective_courage", 0.0) or 0.0),
    }

# --------------------------------------------------
# meta_regulation_state
# --------------------------------------------------
def build_meta_regulation_state(perception_state, felt_state, thought_state, fused, pause_mode=False):

    perception = dict(perception_state or {})
    felt = dict(felt_state or {})
    thought = dict(thought_state or {})
    fused_state = dict(fused or {})

    uncertainty_score = float(perception.get("uncertainty_score", 0.0) or 0.0)
    observe_priority = float(perception.get("observe_priority", 0.0) or 0.0)
    signal_quality = float(perception.get("signal_quality", 0.0) or 0.0)
    felt_conflict = float(felt.get("felt_conflict", 0.0) or 0.0)
    felt_pressure = float(felt.get("felt_pressure", 0.0) or 0.0)
    state_maturity = float(thought.get("state_maturity", 0.0) or 0.0)
    decision_conflict = float(thought.get("decision_conflict", 0.0) or 0.0)
    rumination_depth = float(thought.get("rumination_depth", 0.0) or 0.0)
    decision_readiness = float(thought.get("decision_readiness", 0.0) or 0.0)
    long_hypothesis = float(thought.get("long_hypothesis", 0.0) or 0.0)
    short_hypothesis = float(thought.get("short_hypothesis", 0.0) or 0.0)
    decision_strength = max(long_hypothesis, short_hypothesis)
    observation_mode = bool(fused_state.get("observation_mode", False))
    decision = str(thought.get("decision", fused_state.get("decision", "WAIT")) or "WAIT")

    observe_priority_threshold = float(getattr(Config, "MCM_META_OBSERVE_PRIORITY_ALLOW", 0.66) or 0.66)
    uncertainty_threshold = float(getattr(Config, "MCM_META_UNCERTAINTY_ALLOW", 0.72) or 0.72)
    conflict_threshold = float(getattr(Config, "MCM_META_CONFLICT_ALLOW", 0.60) or 0.60)
    rumination_threshold = float(getattr(Config, "MCM_META_RUMINATION_ALLOW", 0.64) or 0.64)
    maturity_min = float(getattr(Config, "MCM_META_MATURITY_MIN", 0.34) or 0.34)
    readiness_min = float(getattr(Config, "MCM_META_READINESS_MIN", 0.38) or 0.38)
    signal_quality_min = float(getattr(Config, "MCM_META_SIGNAL_QUALITY_MIN", 0.24) or 0.24)

    allow_observe = False
    allow_ruminate = False
    allow_plan = False
    allow_block = False
    rejection_reason = None

    if bool(pause_mode):
        allow_block = True
        rejection_reason = "pause_mode"
    elif decision not in ("LONG", "SHORT"):
        allow_block = True
        rejection_reason = str(fused_state.get("reject_reason", "decision_wait") or "decision_wait")
    elif observation_mode and decision_strength < 1.10:
        allow_observe = True
        rejection_reason = "observe_state"
    elif observe_priority >= observe_priority_threshold and decision_strength < 1.06:
        allow_observe = True
        rejection_reason = "observe_state"
    elif uncertainty_score >= uncertainty_threshold and decision_strength < 1.12:
        allow_observe = True
        rejection_reason = "observe_state"
    elif decision_conflict >= conflict_threshold or rumination_depth >= rumination_threshold or felt_conflict >= 0.58:
        allow_ruminate = True
        rejection_reason = "ruminate_state"
    elif ((state_maturity < maturity_min) and decision_strength < 1.10) or ((decision_readiness < readiness_min) and decision_strength < 1.02) or ((signal_quality < signal_quality_min) and decision_strength < 1.08):
        allow_block = True
        rejection_reason = "maturity_block"
    elif felt_pressure > 0.94 and state_maturity < 0.50 and decision_strength < 1.18:
        allow_block = True
        rejection_reason = "pressure_block"
    else:
        allow_plan = True
        rejection_reason = "plan_allowed"

    return {
        "allow_observe": bool(allow_observe),
        "allow_ruminate": bool(allow_ruminate),
        "allow_plan": bool(allow_plan),
        "allow_block": bool(allow_block),
        "rejection_reason": str(rejection_reason or "-"),
        "decision": str(decision),
        "uncertainty_score": float(uncertainty_score),
        "observe_priority": float(observe_priority),
        "felt_conflict": float(felt_conflict),
        "felt_pressure": float(felt_pressure),
        "decision_conflict": float(decision_conflict),
        "state_maturity": float(state_maturity),
        "rumination_depth": float(rumination_depth),
        "decision_readiness": float(decision_readiness),
        "signal_quality": float(signal_quality),
        "decision_strength": float(decision_strength),
    }

# --------------------------------------------------
# pthought_state
# --------------------------------------------------
def build_thought_state(candle_state, tension_state, fused, perception_state, felt_state, snapshot, bot=None):

    fused_state = dict(fused or {})
    perception = dict(perception_state or {})
    felt = dict(felt_state or {})

    long_score = float(fused_state.get("long_score", 0.0) or 0.0)
    short_score = float(fused_state.get("short_score", 0.0) or 0.0)
    decision = str(fused_state.get("decision", "WAIT") or "WAIT")

    decision_conflict = max(0.0, min(1.0, 1.0 - min(1.0, abs(long_score - short_score) / 1.2) + (float(felt.get("felt_conflict", 0.0) or 0.0) * 0.24)))
    state_maturity = max(0.0, min(1.0, (float(felt.get("reflection_maturity", 0.0) or 0.0) * 0.28) + (float(felt.get("experience_regulation", 0.0) or 0.0) * 0.20) + (float(felt.get("felt_stability", 0.0) or 0.0) * 0.18) + (float(perception.get("signal_quality", 0.0) or 0.0) * 0.18) + (max(0.0, 1.0 - float(perception.get("uncertainty_score", 0.0) or 0.0)) * 0.16) - (decision_conflict * 0.16)))
    rumination_depth = max(0.0, min(1.0, (decision_conflict * 0.42) + (float(perception.get("observe_priority", 0.0) or 0.0) * 0.22) + (float(felt.get("felt_pressure", 0.0) or 0.0) * 0.14) + (0.14 if bool(fused_state.get("observation_mode", False)) else 0.0)))
    inner_time_scale = max(0.0, min(1.0, (state_maturity * 0.36) + (float(felt.get("load_bearing_capacity", 0.0) or 0.0) * 0.18) + (max(0.0, 1.0 - float(perception.get("novelty_score", 0.0) or 0.0)) * 0.14) + max(0.0, 1.0 - (abs(float((tension_state or {}).get("coherence", 0.0) or 0.0)) * 0.25))))
    decision_readiness = max(0.0, min(1.0, (state_maturity * 0.40) + (max(0.0, 1.0 - decision_conflict) * 0.24) + (float(perception.get("signal_quality", 0.0) or 0.0) * 0.16) + (float(felt.get("felt_stability", 0.0) or 0.0) * 0.12) - (rumination_depth * 0.14)))

    return {
        "long_hypothesis": float(long_score),
        "short_hypothesis": float(short_score),
        "wait_hypothesis": float(max(0.0, 1.0 - max(long_score, short_score))),
        "decision": str(decision),
        "decision_conflict": float(decision_conflict),
        "state_maturity": float(state_maturity),
        "rumination_depth": float(rumination_depth),
        "inner_time_scale": float(inner_time_scale),
        "decision_readiness": float(decision_readiness),
    }

# --------------------------------------------------
# perception_stat
# --------------------------------------------------
def build_perception_state(world_state, bot=None):

    world = dict(world_state or {})
    candle_state = dict(world.get("candle_state", {}) or {})
    tension_state = dict(world.get("tension_state", {}) or {})
    focus = dict(world.get("focus", {}) or {})
    filtered_vision = dict(world.get("filtered_vision", {}) or {})
    structure_perception_state = dict(world.get("structure_perception_state", {}) or {})

    focus_direction = float(focus.get("focus_direction", 0.0) or 0.0)
    focus_strength = float(focus.get("focus_strength", 0.0) or 0.0)
    focus_confidence = float(focus.get("focus_confidence", 0.0) or 0.0)
    target_lock = float(focus.get("target_lock", 0.0) or 0.0)
    noise_damp = float(focus.get("noise_damp", 0.0) or 0.0)
    signal_relevance = float(focus.get("signal_relevance", 0.0) or 0.0)
    filtered_target_map = float(filtered_vision.get("target_map", 0.0) or 0.0)
    filtered_threat_map = float(filtered_vision.get("threat_map", 0.0) or 0.0)
    filtered_optic_flow = float(filtered_vision.get("optic_flow", 0.0) or 0.0)

    coherence = float((tension_state or {}).get("coherence", 0.0) or 0.0)
    energy = float((tension_state or {}).get("energy", 0.0) or 0.0)
    return_intensity = float((candle_state or {}).get("return_intensity", 0.0) or 0.0)
    close_position = float((candle_state or {}).get("close_position", 0.0) or 0.0)

    prev_signal_relevance = float(getattr(bot, "last_signal_relevance", 0.0) or 0.0) if bot is not None else 0.0
    prev_focus_confidence = float(getattr(bot, "focus_confidence", 0.0) or 0.0) if bot is not None else 0.0
    observation_mode = bool(getattr(bot, "observation_mode", False)) if bot is not None else False

    perception_settle = max(
        0.0,
        min(
            1.0,
            (prev_signal_relevance * 0.22)
            + (prev_focus_confidence * 0.20)
            + (focus_confidence * 0.14),
        ),
    )

    uncertainty_score = max(0.0, min(1.0, (noise_damp * 0.24) + (filtered_threat_map * 0.18) + max(0.0, abs(focus_direction) - focus_confidence) * 0.18 + max(0.0, 1.0 - signal_relevance) * 0.20 + max(0.0, abs(coherence - close_position)) * 0.10 - (perception_settle * 0.18)))
    novelty_score = max(0.0, min(1.0, abs(signal_relevance - prev_signal_relevance) * 0.46 + abs(return_intensity) * 0.22 + abs(filtered_optic_flow) * 0.14 + abs(energy - coherence) * 0.10 + abs(close_position) * 0.08 - (perception_settle * 0.16)))
    signal_quality = max(0.0, min(1.0, (signal_relevance * 0.34) + (focus_confidence * 0.24) + (target_lock * 0.18) + (focus_strength * 0.10) + (max(0.0, filtered_target_map) * 0.10) + (perception_settle * 0.16) - (uncertainty_score * 0.18)))
    observe_priority = max(0.0, min(1.0, (uncertainty_score * 0.46) + (novelty_score * 0.18) + (max(0.0, 1.0 - signal_quality) * 0.24) + (0.12 if observation_mode else 0.0) - (perception_settle * 0.24)))

    return {
        "focus_direction": float(focus_direction),
        "focus_strength": float(focus_strength),
        "focus_confidence": float(focus_confidence),
        "target_lock": float(target_lock),
        "noise_damp": float(noise_damp),
        "signal_relevance": float(signal_relevance),
        "uncertainty_score": float(uncertainty_score),
        "novelty_score": float(novelty_score),
        "signal_quality": float(signal_quality),
        "observe_priority": float(observe_priority),
        "structure_seen": float(structure_perception_state.get("structure_seen", 0.0) or 0.0),
        "structure_high": float(structure_perception_state.get("structure_high", 0.0) or 0.0),
        "structure_low": float(structure_perception_state.get("structure_low", 0.0) or 0.0),
        "structure_range": float(structure_perception_state.get("structure_range", 0.0) or 0.0),
        "swing_high_strength": float(structure_perception_state.get("swing_high_strength", 0.0) or 0.0),
        "swing_low_strength": float(structure_perception_state.get("swing_low_strength", 0.0) or 0.0),
        "zone_proximity": float(structure_perception_state.get("zone_proximity", 0.0) or 0.0),
        "structure_stability": float(structure_perception_state.get("structure_stability", 0.0) or 0.0),
        "structure_quality": float(structure_perception_state.get("structure_quality", 0.0) or 0.0),
        "stress_relief_potential": float(structure_perception_state.get("stress_relief_potential", 0.0) or 0.0),
        "context_confidence": float(structure_perception_state.get("context_confidence", 0.0) or 0.0),
    }

# --------------------------------------------------
# ENTRY API
# --------------------------------------------------
def decide_mcm_brain_entry(window, candle_state, bot=None):

    if not window:
        return None

    last = window[-1]

    energy, coherence, asymmetry, coh_zone = compute_tension_from_ohlc(
        float(last.get("open", 0.0) or 0.0),
        float(last.get("high", 0.0) or 0.0),
        float(last.get("low", 0.0) or 0.0),
        float(last.get("close", 0.0) or 0.0),
        float(last.get("volume", 0.0) or 0.0),
    )

    tension_state = {
        "energy": float(energy),
        "coherence": float(coherence),
        "asymmetry": int(asymmetry),
        "coh_zone": float(coh_zone),
    }

    if not bool(getattr(Config, "MCM_ENABLED", True)):
        return None

    if bot is None:
        return None

    if getattr(bot, "mcm_brain", None) is None:
        bot.mcm_brain = create_mcm_brain()

    pause_left = int(getattr(bot, "mcm_pause_left", 0) or 0)
    pause_mode = pause_left > 0

    stimulus = build_mcm_stimulus(
        candle_state,
        tension_state,
        pause_mode=pause_mode,
        bot=bot,
    )
    snapshot = step_mcm_brain(bot.mcm_brain, stimulus, mode="market")

    bot.mcm_last_state = dict(snapshot)
    bot.mcm_last_action = str(snapshot.get("self_state", "stable"))
    bot.mcm_last_attractor = str(snapshot.get("attractor", "neutral"))
    bot.mcm_snapshot = dict(snapshot)

    update_target_model(
        bot,
        candle_state,
        dict(stimulus.get("focus", {}) or {}),
    )

    neural_state = build_neural_modulation(
        bot,
        stimulus,
    )

    fused_preview = resolve_fused_decision(candle_state, tension_state, snapshot, bot=bot)

    structure_perception_state = STRUCTURE_ENGINE.build_structure_perception_state(window)
    world_state = build_world_state(
        candle_state,
        tension_state,
        stimulus,
        structure_perception_state=structure_perception_state,
    )
    outer_visual_perception_state = build_outer_visual_perception_state(world_state)
    inner_field_perception_state = build_inner_field_perception_state(snapshot, bot=bot)
    perception_state = build_perception_state(world_state, bot=bot)
    processing_state = build_processing_state(
        outer_visual_perception_state,
        inner_field_perception_state,
        perception_state,
    )
    felt_state = build_felt_state(bot, candle_state, stimulus, snapshot, perception_state, decision=str(fused_preview.get("decision", "WAIT") or "WAIT"))
    state_signature = build_state_signature(candle_state, tension_state, snapshot, stimulus, bot=bot)

    update_signature_memory(bot, state_signature, outcome=None)
    classify_state_cluster(bot, state_signature)
    merge_similar_signatures(bot)
    split_unstable_cluster(bot)

    fused = dict(fused_preview or {})
    fused = reinterpret_focus_by_signature(bot, fused, state_signature)

    thought_state = build_thought_state(candle_state, tension_state, fused, perception_state, felt_state, snapshot, bot=bot)
    meta_regulation_state = build_meta_regulation_state(perception_state, felt_state, thought_state, fused, pause_mode=pause_mode)

    bot.perception_state = dict(perception_state)
    bot.outer_visual_perception_state = dict(outer_visual_perception_state)
    bot.inner_field_perception_state = dict(inner_field_perception_state)
    bot.structure_perception_state = dict(structure_perception_state)
    bot.processing_state = dict(processing_state)
    bot.felt_state = dict(felt_state)
    bot.thought_state = dict(thought_state)
    bot.meta_regulation_state = dict(meta_regulation_state)

    decision = str(meta_regulation_state.get("decision", fused.get("decision", "WAIT")) or "WAIT")

    if not bool(meta_regulation_state.get("allow_plan", False)):
        return {
            "decision": "WAIT",
            "energy": float(energy),
            "coherence": float(coherence),
            "asymmetry": int(asymmetry),
            "coh_zone": float(coh_zone),
            "self_state": str(snapshot.get("self_state", "stable")),
            "attractor": str(snapshot.get("attractor", "neutral")),
            "memory_center": float((snapshot.get("strongest_memory") or {}).get("center", 0.0) or 0.0),
            "memory_strength": int((snapshot.get("strongest_memory") or {}).get("strength", 0) or 0),
            "vision": dict(stimulus.get("vision", {}) or {}),
            "filtered_vision": dict(stimulus.get("filtered_vision", {}) or {}),
            "focus": dict(stimulus.get("focus", {}) or {}),
            "world_state": dict(world_state or {}),
            "structure_perception_state": dict(structure_perception_state or {}),
            "outer_visual_perception_state": dict(outer_visual_perception_state or {}),
            "inner_field_perception_state": dict(inner_field_perception_state or {}),
            "processing_state": dict(processing_state or {}),
            "perception_state": dict(perception_state or {}),
            "felt_state": dict(felt_state or {}),
            "thought_state": dict(thought_state or {}),
            "meta_regulation_state": dict(meta_regulation_state or {}),
            "expectation_state": dict(felt_state or {}),
            "state_signature": dict(state_signature or {}),
            "signature_bias": float(fused.get("signature_bias", 0.0) or 0.0),
            "signature_block": bool(fused.get("signature_block", False)),
            "signature_quality": float(fused.get("signature_quality", 0.0) or 0.0),
            "signature_distance": float(fused.get("signature_distance", 0.0) or 0.0),
            "context_cluster_id": str(fused.get("context_cluster_id", "-") or "-"),
            "context_cluster_bias": float(fused.get("context_cluster_bias", 0.0) or 0.0),
            "context_cluster_quality": float(fused.get("context_cluster_quality", 0.0) or 0.0),
            "context_cluster_distance": float(fused.get("context_cluster_distance", 0.0) or 0.0),
            "context_cluster_block": bool(fused.get("context_cluster_block", False)),
            "inhibition_level": float(neural_state.get("inhibition_level", 0.0) or 0.0),
            "habituation_level": float(neural_state.get("habituation_level", 0.0) or 0.0),
            "competition_bias": float(neural_state.get("competition_bias", 0.0) or 0.0),
            "observation_mode": bool(neural_state.get("observation_mode", False)),
            "long_score": float(fused.get("long_score", 0.0) or 0.0),
            "short_score": float(fused.get("short_score", 0.0) or 0.0),
            "rejection_reason": str(meta_regulation_state.get("rejection_reason", fused.get("reject_reason", "meta_block")) or "meta_block"),
        }

    if decision not in ("LONG", "SHORT"):
        return None

    prices = derive_trade_plan_from_brain(decision, candle_state, fused, stimulus, snapshot, bot=bot)

    if prices is None:
        return None

    return {
        "decision": decision,
        "entry_price": float(prices["entry_price"]),
        "sl_price": float(prices["sl_price"]),
        "tp_price": float(prices["tp_price"]),
        "rr_value": float(prices["rr_value"]),
        "entry_validity_band": dict(prices.get("entry_validity_band", {}) or {}),
        "target_conviction": float(prices.get("target_conviction", 0.0) or 0.0),
        "risk_model_score": float(prices.get("risk_model_score", 0.0) or 0.0),
        "reward_model_score": float(prices.get("reward_model_score", 0.0) or 0.0),
        "energy": float(energy),
        "coherence": float(coherence),
        "asymmetry": int(asymmetry),
        "coh_zone": float(coh_zone),
        "self_state": str(snapshot.get("self_state", "stable")),
        "attractor": str(snapshot.get("attractor", "neutral")),
        "memory_center": float((snapshot.get("strongest_memory") or {}).get("center", 0.0) or 0.0),
        "memory_strength": int((snapshot.get("strongest_memory") or {}).get("strength", 0) or 0),
        "vision": dict(stimulus.get("vision", {}) or {}),
        "filtered_vision": dict(stimulus.get("filtered_vision", {}) or {}),
        "focus": dict(stimulus.get("focus", {}) or {}),
        "world_state": dict(world_state or {}),
        "structure_perception_state": dict(structure_perception_state or {}),
        "outer_visual_perception_state": dict(outer_visual_perception_state or {}),
        "inner_field_perception_state": dict(inner_field_perception_state or {}),
        "processing_state": dict(processing_state or {}),
        "perception_state": dict(perception_state or {}),        
        "felt_state": dict(felt_state or {}),
        "thought_state": dict(thought_state or {}),
        "meta_regulation_state": dict(meta_regulation_state or {}),
        "expectation_state": dict(felt_state or {}),
        "state_signature": dict(state_signature or {}),
        "signature_bias": float(fused.get("signature_bias", 0.0) or 0.0),
        "signature_block": bool(fused.get("signature_block", False)),
        "signature_quality": float(fused.get("signature_quality", 0.0) or 0.0),
        "signature_distance": float(fused.get("signature_distance", 0.0) or 0.0),
        "context_cluster_id": str(fused.get("context_cluster_id", "-") or "-"),
        "context_cluster_bias": float(fused.get("context_cluster_bias", 0.0) or 0.0),
        "context_cluster_quality": float(fused.get("context_cluster_quality", 0.0) or 0.0),
        "context_cluster_distance": float(fused.get("context_cluster_distance", 0.0) or 0.0),
        "context_cluster_block": bool(fused.get("context_cluster_block", False)),
        "inhibition_level": float(neural_state.get("inhibition_level", 0.0) or 0.0),
        "habituation_level": float(neural_state.get("habituation_level", 0.0) or 0.0),
        "competition_bias": float(neural_state.get("competition_bias", 0.0) or 0.0),
        "observation_mode": bool(neural_state.get("observation_mode", False)),
        "long_score": float(fused.get("long_score", 0.0) or 0.0),
        "short_score": float(fused.get("short_score", 0.0) or 0.0),
    }
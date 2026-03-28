# ==================================================
# ZENTRALE BOT KONFIGURATION
# Nur aktiv verwendete Variablen
# ==================================================

class Config:

    # ==================================================
    # SYSTEM
    # ==================================================
    MODE = "BACKTEST"            # "BACKTEST" | "LIVE"
    AKTIV_ORDER = True           # Nur relevant im LIVE-Modus

    # ==================================================
    # DATENQUELLE
    # ==================================================
    BACKTEST_FILEPATH = "data/1-12_2025_5m_SOLUSDT.csv" 
    # workspace | 1-12_2023_5m_SOLUSDT | 1-12_2024_5m_SOLUSDT | 1-12_2025_5m_SOLUSDT | 1-2_2026_5m_SOLUSDT 
    
    CSV_OHLCV_PATH = "workspace.csv"   # Live Mode OHLCV Daten Börse
    # ==================================================
    # MARKT
    # ==================================================
    COIN = "SOL"
    USDT = "USDT"
    SYMBOL = f"{COIN}/{USDT}"
    TIMEFRAME = "5m"
    MECHANIK = "swap"
    ORDER_SIZE = 0.5

    # ==================================================
    # WORKSPACE
    # ==================================================
    WINDOW_SIZE = 500

    # ==================================================
    # RISK MANAGEMENT
    # ==================================================
    RR = 2
    MIN_RR = 1
    MAX_RR = 6
    # trade_value_gate.py Ökonomische Absicherung
    BASE_RISK_PCT = 0.0045
    MAX_SL_DISTANCE = 0.006
    MIN_TP_DISTANCE = 0.015

    RR_EXECUTION_MIN = 1.8
    PENDING_ENTRY_MAX_WAIT_BARS = 4

    # ==================================================
    # MCM BRAIN
    # ==================================================
    MCM_DEBUG = True
    MCM_OUTCOME_DEBUG = True

    MCM_ENABLED = True
    MCM_INTERNAL_CYCLES = 1
    MCM_REPLAY_SCALE = 0.012
    MCM_FIELD_AGENTS = 48
    MCM_FIELD_DIMS = 3
    MCM_COUPLING = 0.045
    MCM_NOISE = 0.08
    MCM_CENTER_FORCE = 0.0100
    MCM_ATTRACTOR_LONG_ALLOW = True
    MCM_ATTRACTOR_SHORT_ALLOW = True
    MCM_PRESSURE_WEIGHT = 0.16
    MCM_MEMORY_WEIGHT = 0.08
    MCM_REGULATION_WEIGHT = 0.42
    MCM_STRESS_RISK_FACTOR = 0.70
    MCM_EXCITED_RR_FACTOR = 1.06
    MCM_TP_REWARD = 0.75
    MCM_SL_PENALTY = 0.85
    MCM_CANCEL_PENALTY = 0.20
    MCM_TIMEOUT_PENALTY = 0.25
    MCM_OUTCOME_MEMORY_BOOST = 1.0
    MCM_OUTCOME_RISK_SHIFT = 0.18
    MCM_SL_PAUSE_STEPS = 5
    MCM_PAUSE_ORIENTATION_GAIN = 1.35
    MCM_PAUSE_MOTIVATION_DAMP = 0.55
    MCM_PAUSE_RISK_GAIN = 1.20
    MCM_CONTEXT_DECAY = 0.992
    MCM_CONTEXT_MAX_AGE = 320
    MCM_CONTEXT_MIN_TRUST = 0.06
    MCM_CONTEXT_MATCH_THRESHOLD = 0.28
    MCM_CONTEXT_LOOKUP_THRESHOLD = 0.30
    MCM_CONTEXT_MERGE_THRESHOLD = 0.16
    MCM_CONTEXT_SPLIT_VARIANCE = 0.085
    MCM_CONTEXT_SPLIT_RADIUS = 0.24
    MCM_INHIBITION_GAIN = 0.26
    MCM_HABITUATION_GAIN = 0.18
    MCM_COMPETITION_GAIN = 0.22
    MCM_OBSERVE_THRESHOLD = 0.66
    MCM_META_OBSERVE_PRIORITY_ALLOW = 0.66
    MCM_META_UNCERTAINTY_ALLOW = 0.72
    MCM_META_CONFLICT_ALLOW = 0.60
    MCM_META_RUMINATION_ALLOW = 0.64
    MCM_META_MATURITY_MIN = 0.34
    MCM_META_READINESS_MIN = 0.38
    MCM_META_SIGNAL_QUALITY_MIN = 0.24
    MCM_MIN_SL_DISTANCE = 0.0022
    MCM_PLAN_GATE_ALIGN = 0.92
    MCM_PROTECTIVE_WIDTH_GAIN = 0.95
    MCM_STRESS_WIDTH_GAIN = 0.34

    # ==================================================
    # KOSTEN
    # ==================================================
    FEE_RATE = 0.0006
    FEE_PER_TRADE = 0.0

    # ==================================================
    # EQUITY
    # ==================================================
    START_EQUITY = 100.0
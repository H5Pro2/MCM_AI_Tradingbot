# ==================================================
# ZENTRALE BOT KONFIGURATION
# Nur aktiv verwendete Variablen
# ==================================================

class Config:

    # ==================================================
    # SYSTEM
    # ==================================================
    MODE = "BACKTEST"            # "BACKTEST" | "LIVE"
    AKTIV_ORDER = False           # Nur relevant im LIVE-Modus

    # ==================================================
    # DATENQUELLE
    # ==================================================
    BACKTEST_FILEPATH = "data/3-4_2026_5m_SOLUSDT.csv" 
    # workspace | 1-12_2023_5m_SOLUSDT | 1-12_2024_5m_SOLUSDT | 1-12_2025_5m_SOLUSDT | 1-2_2026_5m_SOLUSDT | test_5m_SOLUSDT
    
    CSV_OHLCV_PATH = "data/workspace.csv"   # Live Mode OHLCV Daten BÃ¶rse
    # ==================================================
    # MARKT
    # ==================================================
    COIN = "SOL"
    USDT = "USDT"
    SYMBOL = f"{COIN}/{USDT}"
    TIMEFRAME = "5m"
    MECHANIK = "swap"
    ORDER_SIZE = 0.5
    WORLD_TIME_LOOP_SECONDS = 1.0 # Live-Loop-Wartezeit fÃ¼r den Ã¤uÃŸeren Welt-/Chart-Loop.
    # WORLD_TIME_LOOP_SECONDS sollte fachlich  eher Polling-Intervall heiÃŸen, nicht Weltzeit. !!!!!
    WORLD_REPLAY_LOOP_SECONDS = 0.001 # Replay-VerzÃ¶gerung im Backtest/CSV-Feed.
    # ==================================================
    # WORKSPACE
    # ==================================================
    WINDOW_SIZE = 500

    # ==================================================
    # RISK MANAGEMENT
    # ==================================================
    MIN_RR = 1
    # trade_value_gate.py Ã–konomische Absicherung
    BASE_RISK_PCT = 0.0045
    MAX_SL_DISTANCE = 0.01
    MIN_TP_DISTANCE = 0.01

    RR_EXECUTION_MIN = 1.8
    PENDING_ENTRY_MAX_WAIT_BARS = 4
    MCM_MATURED_EXIT_MODE = "observe" # "fixed" = nur TP/SL, "observe" = Exit-Reife nur protokollieren, "active" = gereifte Exit-Entscheidung darf schliessen.
    MCM_MATURED_EXIT_MIN_MFE_R = 0.70 # Mindest-Gewinnlauf in R, bevor gereifte Exit-Reife ueberhaupt relevant wird.
    MCM_MATURED_EXIT_GIVEBACK_R = 0.25 # Rueckgabe vom Peak in R, ab der Schutz-/Exit-Reife entstehen darf.
    MCM_MATURED_EXIT_STRUCTURE_MAX = 0.50 # Unterhalb dieser Strukturqualitaet gilt Halten als weniger tragfaehig.
    MCM_MATURED_EXIT_PRESSURE_MIN = 1.15 # Druck/Kapazitaets-Verhaeltnis, ab dem Halten als belastet gilt.

    # ==================================================
    # MCM BRAIN
    # ==================================================
    MCM_DEBUG = True
    MCM_OUTCOME_DEBUG = True
    DEBUG_OUTPUT_PROFILE = "DIO_CORE_DEBUG" # DIO_CORE_DEBUG, RESEARCH_DEBUG, LEAN_BACKTEST, GUI_DEBUG, PERFORMANCE_DEBUG, LIVE_DEBUG oder CUSTOM.
    DEBUG_WRITE_MODE = "buffered_safe" # immediate, buffered oder buffered_safe. Buffered haelt Debug-Zeilen bis Ende/Flush im RAM.
    DEBUG_BUFFER_FLUSH_EVERY_N = 1000 # Bei buffered_safe nach N gepufferten Zeilen je Datei schreiben.
    DEBUG_BUFFER_FLUSH_SECONDS = 10.0 # Bei buffered_safe spaetestens nach N Sekunden je Datei schreiben.
    DEBUG_BUFFER_MAX_LINES_PER_FILE = 50000 # Sicherheitsgrenze je Datei; danach wird automatisch geflusht.
    DEBUG_GROUPED_DIRS = True # Schreibt Debug-Dateien pro Lauf in Unterordner wie gui/core/research/performance.
    MCM_RUNTIME_PROFILE_DEBUG = True # Schreibt Laufzeitprofile nach debug/mcm_profile.csv, um Rechenzeit, Snapshot- und Schreibkosten sichtbar zu machen.
    MCM_RUNTIME_PROFILE_MIN_MS = 0.05 # Mindestdauer in Millisekunden, ab der Profiling-Zeilen geschrieben werden.
    MCM_RUNTIME_PROFILE_EVERY_N = 10 # Schreibt jede n-te Profiling-Zeile. HÃ¶her setzen, wenn der Profiling-Output zu groÃŸ wird.
    MCM_FILE_WRITE_PROFILE_DEBUG = True # Schreibt kompakte Dateischreibprofile nach debug/mcm_file_write_profile.csv.
    MCM_FILE_WRITE_PROFILE_MIN_MS = 0.05 # Mindestdauer in Millisekunden, ab der Dateischreibprofile geschrieben werden.
    MCM_FILE_WRITE_PROFILE_EVERY_N = 5 # Schreibt jede n-te Dateischreib-Profilzeile, damit die Messung selbst leicht bleibt.
    TRADE_STATS_ATTEMPT_RECORD_DEBUG = True # Schreibt Attempt-Replay-Zeilen; In-Memory-Zaehler bleiben auch bei Sampling aktiv.
    TRADE_STATS_ATTEMPT_RECORD_EVERY_N = 10 # Schreibt nur jede n-te Attempt-Zeile; echte Submitted/Filled/Cancel/Timeout-Events bleiben sichtbar.
    TRADE_STATS_ATTEMPT_RECORD_COMPACT = True # Entfernt schwere Snapshot-Nester aus Attempt-JSONL und behaelt nur Diagnoseachsen.
    TRADE_STATS_JSON_SAVE_EVERY_N = 25 # Schreibt trade_stats.json auf Attempt-Pfaden nur periodisch; Exits/Cancels schreiben weiterhin sofort.
    MCM_STRATEGIC_WINDOW_PROTOCOL_DEBUG = True # Schreibt Rueckblick-/Bereichsfenster-Diagnose; sehr datenintensiv, nur bei gezielter Strukturpruefung aktiv lassen.
    MCM_ACTIVE_CONTACT_PROTOCOL_DEBUG = True # Schreibt Kontaktbereichs-Diagnose; fuer Kernlaeufe standardmaessig abschaltbar.
    MCM_FIELD_DECISION_PROTOCOL_DEBUG = True # Schreibt ein kompaktes Feldentscheidungs-Protokoll nach debug/mcm_field_decision_protocol.csv.
    MCM_FIELD_DECISION_PROTOCOL_EVERY_N = 5 # Schreibt jede n-te Feldentscheidung; Phasenwechsel werden trotzdem sofort geschrieben.
    MCM_NEURO_TRANSITION_PROTOCOL_DEBUG = True # Schreibt neurochemische Zustandswechsel mit -2/+2 Kerzenumfeld nach debug/mcm_neuro_transition_protocol.csv.
    MCM_NEURO_TRANSITION_PROTOCOL_CONTEXT = 2 # Anzahl Kerzen vor/nach einem neurochemischen Wechsel fuer das Analyseprotokoll.
    MCM_MEMORY_THINKING_PROTOCOL_DEBUG = True # Schreibt Memory-/Denkkomplexitaets-Diagnose nach debug/mcm_memory_thinking_protocol.csv.
    MCM_MEMORY_THINKING_PROTOCOL_EVERY_N = 5 # Schreibt jede n-te Memory-Diagnose; Phasen-/Grundwechsel werden trotzdem sofort geschrieben.
    MCM_POSITION_INTERVENTION_PROTOCOL_DEBUG = True # Schreibt Positionslast-/Exit-Nervositaets-Diagnose nach debug/mcm_position_intervention_protocol.csv.
    MCM_POSITION_INTERVENTION_PROTOCOL_EVERY_N = 5 # Schreibt jede n-te offene Positionslesung; hohe Exit-Spannung wird trotzdem sichtbar.
    MCM_TARGET_EXPECTATION_PROTOCOL_DEBUG = True # Schreibt observe-only Zielerwartungs-/TP-Erreichbarkeitsdiagnose.
    MCM_TARGET_EXPECTATION_PROTOCOL_EVERY_N = 5 # Schreibt jede n-te Zielerwartung; Erwartungsbruch wird trotzdem sofort sichtbar.
    MCM_EXIT_CANDIDATE_OBSERVE_DEBUG = True # Schreibt gekoppelte Exit-Kandidaten nur als Beobachtung, nicht als aktive Schliessung.
    MCM_IDLE_THINKING_PROTOCOL_DEBUG = True # Schreibt Live-/Idle-Denktiefe, Replaybedarf und regulatorische Selbstkontrolle nach debug/mcm_idle_thinking_protocol.csv.
    MCM_IDLE_THINKING_PROTOCOL_EVERY_N = 5 # Schreibt jede n-te Idle-Denkzeile; echte Zustandswechsel werden trotzdem sofort protokolliert.
    MCM_EXIT_CANDIDATE_MIN_PRESSURE = 0.58 # Mindest-Exit-Druck fuer einen reifen Kandidaten.
    MCM_EXIT_CANDIDATE_MAX_PLAN_TRUST = 0.52 # Obergrenze Planvertrauen; hohes Vertrauen soll Halten schuetzen.
    MCM_EXIT_CANDIDATE_MAX_HOLDING_STABILITY = 0.50 # Haltestabilitaet muss sichtbar kippen.
    MCM_EXIT_CANDIDATE_MIN_FITNESS = 0.40 # Intervention muss trotz Last ausreichend tragfaehig sein.
    MCM_EXIT_CANDIDATE_MIN_EVIDENCE = 0.54 # Struktur-/Rueckgabe-/Druck-Evidenz muss gekoppelt tragen.
    MCM_EXIT_CANDIDATE_MAX_CURRENT_R = -0.45 # Kandidat braucht echte adverse Tiefe; leichte Rueckatmung nach Gewinnlauf reicht nicht.
    MCM_FORM_SYMBOL_PROTOCOL_DEBUG = True # Schreibt interne Eigenzeichen-/Formsymbol-Diagnose nach debug/mcm_form_symbol_protocol.csv.
    MCM_FORM_SYMBOL_PROTOCOL_EVERY_N = 5 # Schreibt jede n-te Formsymbol-Diagnose; Symbol-/Zoomwechsel werden trotzdem sofort geschrieben.
    MCM_THOUGHT_SEED_PROTOCOL_DEBUG = True # Schreibt Gedankenkeim-/Gedankenfamilien-Diagnose; JSON-Memory bleibt unabhaengig davon aktiv.
    MCM_THOUGHT_SEED_PROTOCOL_EVERY_N = 5 # Schreibt jede n-te Gedankenkeim-Zeile.
    MCM_THOUGHT_DIGEST_PROTOCOL_DEBUG = True # Schlanke Diagnose fuer Gedanken-Verdauung, Replay, Abstand, Integration und Trust-Return.
    MCM_THOUGHT_DIGEST_PROTOCOL_EVERY_N = 5 # Schreibt jede n-te Verdauungszeile; Zustandswechsel werden sofort sichtbar.
    MCM_VISUAL_CORTEX_PROTOCOL_DEBUG = True # Schreibt beobachtende Formsehen-Diagnose nach debug/mcm_visual_cortex_protocol.csv.
    MCM_VISUAL_CORTEX_PROTOCOL_EVERY_N = 5 # Schreibt jede n-te visuelle Kortex-Zeile; Formwechsel werden trotzdem sofort geschrieben.
    MCM_FORM_SYMBOL_MEMORY_ENABLED = True # Persistenter, separater Speicher fuer eigene Form-Sprache.
    MCM_FORM_SYMBOL_MEMORY_PATH = "bot_memory/form_symbol_memory.json" # Getrennt vom Trade-/State-Memory.
    MCM_FORM_SYMBOL_MEMORY_SAVE_EVERY_N = 64 # Speichert periodisch nach N Symbol-Aktualisierungen.
    MCM_FORM_SYMBOL_MEMORY_MAX_SYMBOLS = 1024 # Begrenzung gegen Speicherwachstum.
    MCM_FORM_SYMBOL_MEMORY_MAX_VARIANTS = 12 # Pro Form-Familie nur haeufige Varianten behalten.
    MCM_FORM_SYMBOL_MEMORY_MAX_COMPOUNDS = 768 # Begrenzung fuer zusammengesetzte Formzeichen.
    MCM_THOUGHT_MEMORY_ENABLED = True # Persistenter, separater Speicher fuer innere Gedankenkeime.
    MCM_THOUGHT_MEMORY_PATH = "bot_memory/mcm_thought_memory.json" # Getrennt von weltlicher Erfahrung und Form-Sprache.
    MCM_THOUGHT_MEMORY_SAVE_EVERY_N = 64 # Speichert periodisch nach N Gedanken-Aktualisierungen.
    MCM_THOUGHT_MEMORY_MAX_SEEDS = 2048 # Begrenzung gegen Speicherwachstum.
    MCM_THOUGHT_MEMORY_MAX_FAMILIES = 768 # Begrenzung fuer verdichtete Gedankenfamilien.
    MCM_STRUCTURE_ACTION_MIN_QUALITY = 0.70 # Unterhalb davon braucht Handlung zusaetzliche Tragfaehigkeit statt nur Wiedererkennung.
    MCM_STRUCTURE_ACTION_MID_SUPPORT_MIN = 0.045 # Minimaler Memory-/Feldsupport fuer mittlere Struktur.
    MCM_STRUCTURE_ACTION_MID_STRENGTH_MIN = 1.36 # Starke Entscheidung darf mittlere Struktur kontrolliert passieren.
    MCM_STRUCTURE_ACTION_LOW_STRENGTH_MIN = 1.52 # Niedrige Struktur braucht ausserordentlich starke Evidenz.
    MCM_ACT_WATCH_ENABLED = True # Handlungsdruck ohne ausreichende Tragfaehigkeit als Reifespur beobachten statt hart blockieren.
    MCM_ACT_WATCH_STRUCTURE_MAX = 0.58 # Unterhalb dieser Strukturqualitaet kann Handlungsdruck als act_watch statt act reifen.
    MCM_ACT_WATCH_PLAN_PRESSURE_MIN = 0.44 # Mindestdruck, ab dem eine unreife Handlung als plan_pressure sichtbar wird.
    MCM_ACT_WATCH_MATURITY_MIN = 0.38 # Mindest-Reife, damit act_watch nicht bloss Rauschen ist.
    MCM_VISUAL_SNAPSHOT_WRITE_EVERY_N = 25 # Schreibt Visual-/Inner-Snapshots nur jeden n-ten Runtime-Markt-Tick.
    MCM_VISUAL_SNAPSHOT_MIN_INTERVAL_SECONDS = 0.0 # Optionale Mindestzeit zwischen Visual-/Inner-Snapshot-SchreibvorgÃ¤ngen.
    MCM_VISUAL_SNAPSHOT_FORCE_ON_STATE_CHANGE = False # Schreibt sofort, wenn Pending-/Position-/Execution-Zustand wechselt.
    MCM_INNER_PATTERN_IDENTITY_STABILITY_TICKS = 5 # Anzahl gleicher Innenmuster-Ticks, ab der inner_pattern_identity als wiederkehrend lesbar wird.

    MCM_ENABLED = True # Aktiviert die MCM-Interne Simulation, um die Entscheidungsfindung der Agenten zu beeinflussen. Deaktivieren, um die MCM-Interne Simulation zu Ã¼berspringen und direkt auf Marktinformationen zu reagieren.
    MCM_INTERNAL_CYCLES = 1 # Anzahl der MCM-Interne Zyklen pro Weltzeit-Tick. Je hÃ¶her, desto intensiver die interne Simulation pro Weltzeit-Tick, aber auch rechenintensiver.
    MCM_REPLAY_SCALE = 0.012 # Skalierungsfaktor fÃ¼r die Geschwindigkeit der MCM-Interne Simulation im Vergleich zur Weltzeit. Je kleiner, desto schneller lÃ¤uft die MCM-Interne Simulation im VerhÃ¤ltnis zur Weltzeit.
    MCM_FIELD_NEURON = 230 # Neuronenzahl im MCM-Feld, beeinflusst die Granularitaet der Simulation und die Rechenzeit.
    MCM_FIELD_DIMS = 3 # Anzahl der Dimensionen im MCM-Feld, z.B. 3 fÃ¼r einen 3D-Raum.
    MCM_FIELD_LOCAL_NEIGHBORS = 8 # Anzahl der nÃ¤chsten Nachbarn, die fÃ¼r lokale Interaktionen berÃ¼cksichtigt werden.
    MCM_NEURON_STEP_RETURN_SNAPSHOT = False # Gibt pro Neuron-Step keinen Snapshot zurueck; das Feld liest Snapshots zentral.
    MCM_FIELD_AREAL_REFRESH_EVERY_N = 2 # Berechnet schwere Areal-/Topologie-Metriken nur jeden n-ten Feldtick voll.
    MCM_FIELD_COUPLING_SIGMA = 0.5 # Standardabweichung fÃ¼r die KopplungsstÃ¤rke in AbhÃ¤ngigkeit von der Entfernung im MCM-Feld. Je kleiner, desto stÃ¤rker die Kopplung bei nahen Agenten und schwÃ¤cher bei entfernten Agenten.
    MCM_COUPLING = 0.045 # Grundlegende KopplungsstÃ¤rke zwischen den Agenten im MCM-Feld. Beeinflusst, wie stark die Agenten sich gegenseitig beeinflussen.
    MCM_NOISE = 0.08 # StÃ¤rke des Rauschens in der MCM-Interne Simulation. Beeinflusst die ZufÃ¤lligkeit der Agentenbewegungen und Entscheidungen.
    MCM_CENTER_FORCE = 0.0100 # StÃ¤rke der Anziehungskraft zum Zentrum des MCM-Feldes. Beeinflusst, wie stark die Agenten dazu neigen, sich in der Mitte des Feldes zu versammeln.
    MCM_CLUSTER_EVERY_N_TICKS = 2 # Anzahl der MCM-Interne Zyklen, nach denen eine Clusteranalyse durchgefÃ¼hrt wird, um Muster und Strukturen im Agentenverhalten zu identifizieren.
    MCM_CLUSTER_EPS = 0.4 # Maximale Entfernung zwischen zwei Agenten, damit sie im selben Cluster liegen (DBSCAN-Parameter). Je kleiner, desto dichter mÃ¼ssen die Agenten beieinander liegen, um als Cluster zu gelten.
    MCM_CLUSTER_MIN_SAMPLES = 4 # Minimale Anzahl von Agenten, die erforderlich ist, um einen Cluster zu bilden (DBSCAN-Parameter). Je hÃ¶her, desto mehr Agenten mÃ¼ssen beieinander liegen, um als Cluster zu gelten.
    MCM_ATTRACTOR_LONG_ALLOW = True # Erlaubt die Bildung von Long-Anziehungspunkten im MCM-Feld, die potenziell auf steigende Marktbewegungen hinweisen.
    MCM_ATTRACTOR_SHORT_ALLOW = True # Erlaubt die Bildung von Short-Anziehungspunkten im MCM-Feld, die potenziell auf fallende Marktbewegungen hinweisen.
    MCM_PRESSURE_WEIGHT = 0.16 # Gewichtung des Drucks (Pressure) in der Entscheidungsfindung der Agenten im MCM-Feld. Beeinflusst, wie stark die Agenten auf den wahrgenommenen Druck reagieren.
    MCM_MEMORY_WEIGHT = 0.08 # Gewichtung der Erinnerung (Memory) in der Entscheidungsfindung der Agenten im MCM-Feld. Beeinflusst, wie stark die Agenten auf vergangene Erfahrungen und Ergebnisse reagieren.
    MCM_REGULATION_WEIGHT = 0.42 # Gewichtung der Regulierung (Regulation) in der Entscheidungsfindung der Agenten im MCM-Feld. Beeinflusst, wie stark die Agenten auf interne und externe Regeln reagieren.
    MCM_STRESS_RISK_FACTOR = 0.70 # Faktor, der das wahrgenommene Risiko (Risk) in Stress umwandelt. Je hÃ¶her, desto stÃ¤rker wird das Risiko in Stress umgewandelt, was zu vorsichtigerem Verhalten der Agenten fÃ¼hren kann.
    MCM_TP_REWARD = 0.75 # Belohnung fÃ¼r das Erreichen des Take-Profits (TP) in der MCM-Interne Simulation. Beeinflusst, wie stark die Agenten das Erreichen von Gewinnzielen anstreben.
    MCM_SL_PENALTY = 0.85 # Bestrafung fÃ¼r das Erreichen des Stop-Loss (SL) in der MCM-Interne Simulation. Beeinflusst, wie stark die Agenten das Erreichen von Verlustzielen vermeiden.
    MCM_CANCEL_PENALTY = 0.20 # Bestrafung fÃ¼r das Abbrechen von Trades in der MCM-Interne Simulation. Beeinflusst, wie stark die Agenten Trades abbrechen.
    MCM_TIMEOUT_PENALTY = 0.25 # Bestrafung fÃ¼r das ZeitÃ¼berschreiten von Trades in der MCM-Interne Simulation. Beeinflusst, wie stark die Agenten auf ZeitÃ¼berschreitungen reagieren.
    MCM_OUTCOME_MEMORY_BOOST = 1.0 # Boost fÃ¼r die Erinnerung (Memory) in der Entscheidungsfindung der Agenten im MCM-Feld. Beeinflusst, wie stark die Agenten auf vergangene Erfahrungen und Ergebnisse reagieren.
    MCM_OUTCOME_RISK_SHIFT = 0.18 # Verschiebung des Risikos (Risk) in der Entscheidungsfindung der Agenten im MCM-Feld. Beeinflusst, wie stark die Agenten auf das wahrgenommene Risiko reagieren.
    MCM_SL_PAUSE_STEPS = 5 # Anzahl der MCM-Interne Zyklen, die nach einem Stop-Loss (SL) pausiert werden, bevor die Agenten wieder aktiv werden. Beeinflusst, wie lange die Agenten nach einem Verlust innehalten, um sich neu zu orientieren.
    MCM_PAUSE_ORIENTATION_GAIN = 1.35 # VerstÃ¤rkung der Orientierung (Orientation) wÃ¤hrend der Pause nach einem Stop-Loss (SL) in der MCM-Interne Simulation. Beeinflusst, wie stark die Agenten ihre Orientierung wÃ¤hrend der Pause anpassen, um zukÃ¼nftige Verluste zu vermeiden.
    MCM_PAUSE_MOTIVATION_DAMP = 0.55 # DÃ¤mpfung der Motivation (Motivation) wÃ¤hrend der Pause nach einem Stop-Loss (SL) in der MCM-Interne Simulation. Beeinflusst, wie stark die Agenten ihre Motivation wÃ¤hrend der Pause reduzieren, um vorsichtigeres Verhalten zu fÃ¶rdern.
    MCM_PAUSE_RISK_GAIN = 1.20 # VerstÃ¤rkung des Risikos (Risk) wÃ¤hrend der Pause nach einem Stop-Loss (SL) in der MCM-Interne Simulation. Beeinflusst, wie stark die Agenten ihr wahrgenommenes Risiko wÃ¤hrend der Pause erhÃ¶hen, um vorsichtigeres Verhalten zu fÃ¶rdern.
    MCM_CONTEXT_DECAY = 0.992 # Rate, mit der die Relevanz von Kontextinformationen im MCM-Feld Ã¼ber die Zeit abnimmt. Je hÃ¶her, desto schneller verlieren Kontextinformationen an Einfluss auf die Entscheidungsfindung der Agenten.  
    MCM_CONTEXT_MAX_AGE = 320 # Maximales Alter von Kontextinformationen im MCM-Feld, bevor sie als irrelevant betrachtet und aus der Entscheidungsfindung entfernt werden. Beeinflusst, wie lange Kontextinformationen die Entscheidungen der Agenten beeinflussen kÃ¶nnen.
    MCM_CONTEXT_MIN_TRUST = 0.06 # Minimales Vertrauen, das erforderlich ist, damit Kontextinformationen im MCM-Feld in die Entscheidungsfindung der Agenten einbezogen werden. Je hÃ¶her, desto mehr Vertrauen ist erforderlich, damit Kontextinformationen berÃ¼cksichtigt werden.
    MCM_CONTEXT_MATCH_THRESHOLD = 0.28 # Schwelle fÃ¼r die Ãœbereinstimmung von Kontextinformationen im MCM-Feld, um als relevant fÃ¼r die Entscheidungsfindung der Agenten zu gelten. Je hÃ¶her, desto strenger die Anforderungen an die Ãœbereinstimmung von Kontextinformationen.
    MCM_CONTEXT_LOOKUP_THRESHOLD = 0.30 # Schwelle fÃ¼r die Suche nach Kontextinformationen im MCM-Feld, um als relevant fÃ¼r die Entscheidungsfindung der Agenten zu gelten. Je hÃ¶her, desto strenger die Anforderungen an die Suche nach Kontextinformationen.
    MCM_CONTEXT_MERGE_THRESHOLD = 0.16 # Schwelle fÃ¼r die ZusammenfÃ¼hrung von Kontextinformationen im MCM-Feld, um als relevant fÃ¼r die Entscheidungsfindung der Agenten zu gelten. Je hÃ¶her, desto strenger die Anforderungen an die ZusammenfÃ¼hrung von Kontextinformationen.
    MCM_CONTEXT_SPLIT_VARIANCE = 0.085 # Schwelle fÃ¼r die Aufteilung von Kontextinformationen im MCM-Feld, um als relevant fÃ¼r die Entscheidungsfindung der Agenten zu gelten. Je hÃ¶her, desto strenger die Anforderungen an die Aufteilung von Kontextinformationen.
    MCM_CONTEXT_SPLIT_RADIUS = 0.24 # Schwelle fÃ¼r die Aufteilung von Kontextinformationen im MCM-Feld basierend auf der rÃ¤umlichen Verteilung, um als relevant fÃ¼r die Entscheidungsfindung der Agenten zu gelten. Je hÃ¶her, desto strenger die Anforderungen an die rÃ¤umliche Verteilung von Kontextinformationen.
    MCM_INHIBITION_GAIN = 0.26 # VerstÃ¤rkung der Hemmung (Inhibition) in der Entscheidungsfindung der Agenten im MCM-Feld. Beeinflusst, wie stark die Agenten hemmende Signale berÃ¼cksichtigen, um Ã¼bermÃ¤ÃŸige AktivitÃ¤t zu vermeiden.
    MCM_HABITUATION_GAIN = 0.18 # VerstÃ¤rkung der GewÃ¶hnung (Habituation) in der Entscheidungsfindung der Agenten im MCM-Feld. Beeinflusst, wie stark die Agenten auf wiederholte Reize mit reduzierter Reaktion reagieren, um sich an hÃ¤ufige Situationen anzupassen.
    MCM_COMPETITION_GAIN = 0.22 # VerstÃ¤rkung der Konkurrenz (Competition) in der Entscheidungsfindung der Agenten im MCM-Feld. Beeinflusst, wie stark die Agenten konkurrierende Signale berÃ¼cksichtigen, um Entscheidungen zu treffen.
    MCM_OBSERVE_THRESHOLD = 0.66 # Schwelle fÃ¼r die Beobachtung von Marktbedingungen und internen ZustÃ¤nden im MCM-Feld, um als relevant fÃ¼r die Entscheidungsfindung der Agenten zu gelten. Je hÃ¶her, desto strenger die Anforderungen an die Beobachtung von Informationen.
    MCM_META_OBSERVE_PRIORITY_ALLOW = 0.66 # Schwelle fÃ¼r die Priorisierung von Beobachtungen im MCM-Feld, um als relevant fÃ¼r die Entscheidungsfindung der Agenten zu gelten. Je hÃ¶her, desto strenger die Anforderungen an die Priorisierung von Beobachtungen.
    MCM_META_UNCERTAINTY_ALLOW = 0.72 # Schwelle fÃ¼r die BerÃ¼cksichtigung von Unsicherheit in der Entscheidungsfindung der Agenten im MCM-Feld. Je hÃ¶her, desto mehr Unsicherheit wird toleriert, bevor sie als relevant fÃ¼r Entscheidungen betrachtet wird.
    MCM_META_CONFLICT_ALLOW = 0.60 # Schwelle fÃ¼r die BerÃ¼cksichtigung von Konflikten in der Entscheidungsfindung der Agenten im MCM-Feld. Je hÃ¶her, desto mehr Konflikte werden toleriert, bevor sie als relevant fÃ¼r Entscheidungen betrachtet werden.
    MCM_META_RUMINATION_ALLOW = 0.64 # Schwelle fÃ¼r die BerÃ¼cksichtigung von GrÃ¼beln (Rumination) in der Entscheidungsfindung der Agenten im MCM-Feld. Je hÃ¶her, desto mehr GrÃ¼beln wird toleriert, bevor es als relevant fÃ¼r Entscheidungen betrachtet wird.
    MCM_META_MATURITY_MIN = 0.34 # Minimale Reife (Maturity), die erforderlich ist, damit die Agenten im MCM-Feld als bereit fÃ¼r komplexe Entscheidungen gelten. Je hÃ¶her, desto reifer mÃ¼ssen die Agenten sein, um komplexe Entscheidungen zu treffen.
    MCM_META_READINESS_MIN = 0.38 # Minimale Bereitschaft (Readiness), die erforderlich ist, damit die Agenten im MCM-Feld als bereit fÃ¼r Entscheidungen gelten. Je hÃ¶her, desto bereiter mÃ¼ssen die Agenten sein, um Entscheidungen zu treffen.
    MCM_META_SIGNAL_QUALITY_MIN = 0.24 # Minimale SignalqualitÃ¤t, die erforderlich ist, damit Informationen im MCM-Feld in die Entscheidungsfindung der Agenten einbezogen werden. Je hÃ¶her, desto mehr QualitÃ¤t ist erforderlich, damit Informationen berÃ¼cksichtigt werden.
    MCM_MIN_SL_DISTANCE = 0.0022 # Minimale Stop-Loss-Distanz, die von den Agenten im MCM-Feld berÃ¼cksichtigt wird. Beeinflusst, wie eng die Agenten ihre Stop-Loss-Positionen setzen, um Verluste zu begrenzen.
    MCM_PLAN_GATE_ALIGN = 0.92 # Schwelle fÃ¼r die Ausrichtung von PlÃ¤nen im MCM-Feld, um als relevant fÃ¼r die Entscheidungsfindung der Agenten zu gelten. Je hÃ¶her, desto strenger die Anforderungen an die Ausrichtung von PlÃ¤nen.
    MCM_PROTECTIVE_WIDTH_GAIN = 0.95 # VerstÃ¤rkung der Schutzbreite (Protective Width) in der Entscheidungsfindung der Agenten im MCM-Feld. Beeinflusst, wie stark die Agenten ihre SchutzmaÃŸnahmen anpassen, um Risiken zu minimieren.
    MCM_STRESS_WIDTH_GAIN = 0.34 # VerstÃ¤rkung der Stressbreite (Stress Width) in der Entscheidungsfindung der Agenten im MCM-Feld. Beeinflusst, wie stark die Agenten ihre Reaktionen auf Stress anpassen, um besser mit herausfordernden Situationen umzugehen.
    MCM_INNER_TICKS_PER_WORLD_TICK = 1 # Anzahl der MCM-Interne Zyklen pro Weltzeit-Tick. Je hÃ¶her, desto intensiver die interne Simulation pro Weltzeit-Tick, aber auch rechenintensiver.
    MCM_INNER_IDLE_BASE_TICKS = 1 # Anzahl der MCM-Interne Zyklen, die als Basis fÃ¼r die Berechnung der Idle-Zeit dienen. Je hÃ¶her, desto lÃ¤nger die Basis-Idle-Zeit, bevor zusÃ¤tzliche Faktoren berÃ¼cksichtigt werden.
    MCM_INNER_IDLE_MAX_TICKS = 2 # Maximale Anzahl der MCM-Interne Zyklen, die als Idle-Zeit verwendet werden kÃ¶nnen. Beeinflusst, wie lange die Agenten inaktiv bleiben kÃ¶nnen, bevor sie wieder aktiv werden.
    MCM_INNER_IDLE_SLEEP_MIN_SECONDS = 0.10 # Minimale Schlafzeit in Sekunden, die die Agenten im MCM-Feld wÃ¤hrend der Idle-Phase verbringen. Beeinflusst, wie kurz die Agenten inaktiv bleiben kÃ¶nnen, bevor sie wieder aktiv werden.
    MCM_INNER_IDLE_SLEEP_MAX_SECONDS = 0.45 # Maximale Schlafzeit in Sekunden, die die Agenten im MCM-Feld wÃ¤hrend der Idle-Phase verbringen. Beeinflusst, wie lange die Agenten inaktiv bleiben kÃ¶nnen, bevor sie wieder aktiv werden.
    MCM_RUNTIME_TICKS_PER_WINDOW = 1 # Anzahl der MCM-Interne Zyklen pro Fensteraktualisierung. Je hÃ¶her, desto intensiver die interne Simulation pro Fensteraktualisierung, aber auch rechenintensiver.
    MCM_RUNTIME_IDLE_TICKS = 1 # Anzahl der MCM-Interne Zyklen, die als Idle-Zeit wÃ¤hrend der Laufzeit dienen. Beeinflusst, wie lange die Agenten inaktiv bleiben kÃ¶nnen, bevor sie wieder aktiv werden.
    MCM_RUNTIME_IDLE_TICKS_MAX = 2 # Maximale Anzahl der MCM-Interne Zyklen, die als Idle-Zeit wÃ¤hrend der Laufzeit verwendet werden kÃ¶nnen. Beeinflusst, wie lange die Agenten inaktiv bleiben kÃ¶nnen, bevor sie wieder aktiv werden.
    MCM_RUNTIME_IDLE_SLEEP_MIN_SECONDS = 0.10 # Minimale Schlafzeit in Sekunden, die die Agenten im MCM-Feld wÃ¤hrend der Idle-Phase der Laufzeit verbringen. Beeinflusst, wie kurz die Agenten inaktiv bleiben kÃ¶nnen, bevor sie wieder aktiv werden.
    MCM_RUNTIME_IDLE_SLEEP_MAX_SECONDS = 0.45 # Maximale Schlafzeit in Sekunden, die die Agenten im MCM-Feld wÃ¤hrend der Idle-Phase der Laufzeit verbringen. Beeinflusst, wie lange die Agenten inaktiv bleiben kÃ¶nnen, bevor sie wieder aktiv werden.
    MCM_MEMORY_STATE_PATH = "bot_memory/memory_state.json" # Dateipfad fÃ¼r das Speichern des Memory-Zustands der MCM-Interne Simulation. Beeinflusst, wo die Memory-Daten gespeichert werden, um Einblicke in die interne Dynamik zu erhalten.
    MCM_MEMORY_SAVE_COOLDOWN_SECONDS = 5.0 # Minimale Zeit in Sekunden zwischen dem Speichern von Memory-ZustÃ¤nden, um die Leistung zu optimieren und Ã¼bermÃ¤ÃŸiges Schreiben zu vermeiden.
    MCM_SAVE_RUNTIME_STATE = False # Aktiviert das Speichern des Runtime-Zustands der MCM-Interne Simulation, um Einblicke in die interne Dynamik zu erhalten, aber auch mit einem gewissen Leistungsaufwand verbunden.
    DEBUG_WRITE_EVERY_N = 8 # Anzahl der MCM-Interne Zyklen, nach denen Debug-Informationen geschrieben werden. Je hÃ¶her, desto seltener werden Debug-Informationen geschrieben, was die Leistung verbessern kann, aber weniger Einblicke in die interne Dynamik bietet.
    DEBUG_AUTO_RUN_DIR = True # Erstellt pro Start automatisch debug/debug_lauf_X und schreibt alle Debug-Dateien dort hinein.
    DEBUG_RUN_PREFIX = "debug_lauf_" # Namenspraefix fuer automatische Debug-Laufordner.
    LIVE_MARKET_PACKET_DEDUPE_ENABLED = True # LIVE: gleiche 5m-Kerze + gleiche Fensterkante nicht erneut als neue Marktwahrnehmung in die Runtime geben.
    LIVE_MARKET_PACKET_DEDUPE_LOG_EVERY_N = 25 # Jede n-te uebersprungene doppelte Live-Marktwahrnehmung protokollieren.

    # ==================================================
    # KOSTEN
    # ==================================================
    FEE_RATE = 0.0006
    FEE_PER_TRADE = 0.0

    # ==================================================
    # EQUITY
    # ==================================================
    START_EQUITY = 100.0
    LIVE_EQUITY_SYNC_ENABLED = True # LIVE: Equity/PnL aus dem Phemex-Futures-Konto synchronisieren statt nur aus START_EQUITY + lokalem PnL ableiten.


def _apply_debug_output_profile():
    profile = str(getattr(Config, "DEBUG_OUTPUT_PROFILE", "CUSTOM") or "CUSTOM").strip().upper()
    if profile in {"CUSTOM", "MANUAL"}:
        Config.DEBUG_OUTPUT_PROFILE_ACTIVE = profile
        return

    profiles = {
        "DIO_CORE_DEBUG": {
            "DEBUG_WRITE_MODE": "buffered",
            "DEBUG_WRITE_EVERY_N": 25,
            "DEBUG_BUFFER_FLUSH_EVERY_N": 2000,
            "DEBUG_BUFFER_FLUSH_SECONDS": 20.0,
            "MCM_DEBUG": False,
            "MCM_OUTCOME_DEBUG": True,
            "MCM_RUNTIME_PROFILE_DEBUG": False,
            "MCM_FILE_WRITE_PROFILE_DEBUG": False,
            "TRADE_STATS_ATTEMPT_RECORD_DEBUG": False,
            "TRADE_STATS_ATTEMPT_RECORD_COMPACT": True,
            "TRADE_STATS_JSON_SAVE_EVERY_N": 25,
            "MCM_STRATEGIC_WINDOW_PROTOCOL_DEBUG": False,
            "MCM_ACTIVE_CONTACT_PROTOCOL_DEBUG": False,
            "MCM_FIELD_DECISION_PROTOCOL_DEBUG": True,
            "MCM_FIELD_DECISION_PROTOCOL_EVERY_N": 25,
            "MCM_NEURO_TRANSITION_PROTOCOL_DEBUG": True,
            "MCM_NEURO_TRANSITION_PROTOCOL_CONTEXT": 2,
            "MCM_MEMORY_THINKING_PROTOCOL_DEBUG": False,
            "MCM_POSITION_INTERVENTION_PROTOCOL_DEBUG": True,
            "MCM_POSITION_INTERVENTION_PROTOCOL_EVERY_N": 25,
            "MCM_TARGET_EXPECTATION_PROTOCOL_DEBUG": False,
            "MCM_EXIT_CANDIDATE_OBSERVE_DEBUG": True,
            "MCM_IDLE_THINKING_PROTOCOL_DEBUG": False,
            "MCM_FORM_SYMBOL_PROTOCOL_DEBUG": False,
            "MCM_THOUGHT_SEED_PROTOCOL_DEBUG": False,
            "MCM_THOUGHT_SEED_PROTOCOL_EVERY_N": 25,
            "MCM_THOUGHT_DIGEST_PROTOCOL_DEBUG": True,
            "MCM_THOUGHT_DIGEST_PROTOCOL_EVERY_N": 10,
            "MCM_VISUAL_CORTEX_PROTOCOL_DEBUG": False,
            "MCM_VISUAL_SNAPSHOT_WRITE_EVERY_N": 100,
        },
        "RESEARCH_DEBUG": {
            "DEBUG_WRITE_MODE": "buffered_safe",
            "DEBUG_WRITE_EVERY_N": 8,
            "MCM_DEBUG": True,
            "MCM_OUTCOME_DEBUG": True,
            "MCM_RUNTIME_PROFILE_DEBUG": True,
            "MCM_RUNTIME_PROFILE_EVERY_N": 10,
            "MCM_FILE_WRITE_PROFILE_DEBUG": True,
            "MCM_FILE_WRITE_PROFILE_EVERY_N": 5,
            "TRADE_STATS_ATTEMPT_RECORD_DEBUG": True,
            "TRADE_STATS_ATTEMPT_RECORD_EVERY_N": 10,
            "TRADE_STATS_ATTEMPT_RECORD_COMPACT": True,
            "MCM_STRATEGIC_WINDOW_PROTOCOL_DEBUG": True,
            "MCM_ACTIVE_CONTACT_PROTOCOL_DEBUG": True,
            "MCM_FIELD_DECISION_PROTOCOL_DEBUG": True,
            "MCM_FIELD_DECISION_PROTOCOL_EVERY_N": 5,
            "MCM_NEURO_TRANSITION_PROTOCOL_DEBUG": True,
            "MCM_NEURO_TRANSITION_PROTOCOL_CONTEXT": 2,
            "MCM_MEMORY_THINKING_PROTOCOL_DEBUG": True,
            "MCM_MEMORY_THINKING_PROTOCOL_EVERY_N": 5,
            "MCM_POSITION_INTERVENTION_PROTOCOL_DEBUG": True,
            "MCM_POSITION_INTERVENTION_PROTOCOL_EVERY_N": 5,
            "MCM_TARGET_EXPECTATION_PROTOCOL_DEBUG": True,
            "MCM_TARGET_EXPECTATION_PROTOCOL_EVERY_N": 5,
            "MCM_EXIT_CANDIDATE_OBSERVE_DEBUG": True,
            "MCM_IDLE_THINKING_PROTOCOL_DEBUG": True,
            "MCM_IDLE_THINKING_PROTOCOL_EVERY_N": 5,
            "MCM_FORM_SYMBOL_PROTOCOL_DEBUG": True,
            "MCM_FORM_SYMBOL_PROTOCOL_EVERY_N": 5,
            "MCM_THOUGHT_SEED_PROTOCOL_DEBUG": True,
            "MCM_THOUGHT_SEED_PROTOCOL_EVERY_N": 5,
            "MCM_THOUGHT_DIGEST_PROTOCOL_DEBUG": True,
            "MCM_THOUGHT_DIGEST_PROTOCOL_EVERY_N": 5,
            "MCM_VISUAL_CORTEX_PROTOCOL_DEBUG": True,
            "MCM_VISUAL_CORTEX_PROTOCOL_EVERY_N": 5,
            "MCM_VISUAL_SNAPSHOT_WRITE_EVERY_N": 25,
        },
        "LEAN_BACKTEST": {
            "DEBUG_WRITE_MODE": "buffered",
            "DEBUG_WRITE_EVERY_N": 20,
            "MCM_DEBUG": False,
            "MCM_OUTCOME_DEBUG": True,
            "MCM_RUNTIME_PROFILE_DEBUG": False,
            "MCM_FILE_WRITE_PROFILE_DEBUG": False,
            "TRADE_STATS_ATTEMPT_RECORD_DEBUG": True,
            "TRADE_STATS_ATTEMPT_RECORD_EVERY_N": 50,
            "TRADE_STATS_ATTEMPT_RECORD_COMPACT": True,
            "MCM_STRATEGIC_WINDOW_PROTOCOL_DEBUG": False,
            "MCM_ACTIVE_CONTACT_PROTOCOL_DEBUG": False,
            "MCM_FIELD_DECISION_PROTOCOL_DEBUG": True,
            "MCM_FIELD_DECISION_PROTOCOL_EVERY_N": 20,
            "MCM_NEURO_TRANSITION_PROTOCOL_DEBUG": True,
            "MCM_NEURO_TRANSITION_PROTOCOL_CONTEXT": 2,
            "MCM_MEMORY_THINKING_PROTOCOL_DEBUG": False,
            "MCM_POSITION_INTERVENTION_PROTOCOL_DEBUG": True,
            "MCM_POSITION_INTERVENTION_PROTOCOL_EVERY_N": 20,
            "MCM_TARGET_EXPECTATION_PROTOCOL_DEBUG": False,
            "MCM_EXIT_CANDIDATE_OBSERVE_DEBUG": True,
            "MCM_IDLE_THINKING_PROTOCOL_DEBUG": False,
            "MCM_FORM_SYMBOL_PROTOCOL_DEBUG": True,
            "MCM_FORM_SYMBOL_PROTOCOL_EVERY_N": 20,
            "MCM_THOUGHT_SEED_PROTOCOL_DEBUG": False,
            "MCM_THOUGHT_SEED_PROTOCOL_EVERY_N": 20,
            "MCM_THOUGHT_DIGEST_PROTOCOL_DEBUG": True,
            "MCM_THOUGHT_DIGEST_PROTOCOL_EVERY_N": 10,
            "MCM_VISUAL_CORTEX_PROTOCOL_DEBUG": True,
            "MCM_VISUAL_CORTEX_PROTOCOL_EVERY_N": 20,
            "MCM_VISUAL_SNAPSHOT_WRITE_EVERY_N": 100,
        },
        "GUI_DEBUG": {
            "DEBUG_WRITE_MODE": "buffered_safe",
            "DEBUG_WRITE_EVERY_N": 10,
            "MCM_DEBUG": True,
            "MCM_OUTCOME_DEBUG": True,
            "MCM_RUNTIME_PROFILE_DEBUG": False,
            "MCM_FILE_WRITE_PROFILE_DEBUG": False,
            "TRADE_STATS_ATTEMPT_RECORD_DEBUG": True,
            "TRADE_STATS_ATTEMPT_RECORD_EVERY_N": 25,
            "TRADE_STATS_ATTEMPT_RECORD_COMPACT": True,
            "MCM_STRATEGIC_WINDOW_PROTOCOL_DEBUG": False,
            "MCM_ACTIVE_CONTACT_PROTOCOL_DEBUG": True,
            "MCM_FIELD_DECISION_PROTOCOL_DEBUG": True,
            "MCM_FIELD_DECISION_PROTOCOL_EVERY_N": 10,
            "MCM_NEURO_TRANSITION_PROTOCOL_DEBUG": True,
            "MCM_NEURO_TRANSITION_PROTOCOL_CONTEXT": 2,
            "MCM_MEMORY_THINKING_PROTOCOL_DEBUG": True,
            "MCM_MEMORY_THINKING_PROTOCOL_EVERY_N": 20,
            "MCM_POSITION_INTERVENTION_PROTOCOL_DEBUG": True,
            "MCM_POSITION_INTERVENTION_PROTOCOL_EVERY_N": 10,
            "MCM_TARGET_EXPECTATION_PROTOCOL_DEBUG": True,
            "MCM_TARGET_EXPECTATION_PROTOCOL_EVERY_N": 10,
            "MCM_EXIT_CANDIDATE_OBSERVE_DEBUG": True,
            "MCM_IDLE_THINKING_PROTOCOL_DEBUG": True,
            "MCM_IDLE_THINKING_PROTOCOL_EVERY_N": 10,
            "MCM_FORM_SYMBOL_PROTOCOL_DEBUG": True,
            "MCM_FORM_SYMBOL_PROTOCOL_EVERY_N": 10,
            "MCM_THOUGHT_SEED_PROTOCOL_DEBUG": True,
            "MCM_THOUGHT_SEED_PROTOCOL_EVERY_N": 10,
            "MCM_THOUGHT_DIGEST_PROTOCOL_DEBUG": True,
            "MCM_THOUGHT_DIGEST_PROTOCOL_EVERY_N": 10,
            "MCM_VISUAL_CORTEX_PROTOCOL_DEBUG": True,
            "MCM_VISUAL_CORTEX_PROTOCOL_EVERY_N": 10,
            "MCM_VISUAL_SNAPSHOT_WRITE_EVERY_N": 10,
        },
        "PERFORMANCE_DEBUG": {
            "DEBUG_WRITE_MODE": "buffered_safe",
            "DEBUG_WRITE_EVERY_N": 50,
            "MCM_DEBUG": False,
            "MCM_OUTCOME_DEBUG": False,
            "MCM_RUNTIME_PROFILE_DEBUG": True,
            "MCM_RUNTIME_PROFILE_EVERY_N": 5,
            "MCM_FILE_WRITE_PROFILE_DEBUG": True,
            "MCM_FILE_WRITE_PROFILE_EVERY_N": 1,
            "TRADE_STATS_ATTEMPT_RECORD_DEBUG": False,
            "MCM_STRATEGIC_WINDOW_PROTOCOL_DEBUG": False,
            "MCM_ACTIVE_CONTACT_PROTOCOL_DEBUG": False,
            "MCM_FIELD_DECISION_PROTOCOL_DEBUG": False,
            "MCM_NEURO_TRANSITION_PROTOCOL_DEBUG": False,
            "MCM_MEMORY_THINKING_PROTOCOL_DEBUG": False,
            "MCM_POSITION_INTERVENTION_PROTOCOL_DEBUG": False,
            "MCM_TARGET_EXPECTATION_PROTOCOL_DEBUG": False,
            "MCM_EXIT_CANDIDATE_OBSERVE_DEBUG": False,
            "MCM_IDLE_THINKING_PROTOCOL_DEBUG": False,
            "MCM_FORM_SYMBOL_PROTOCOL_DEBUG": False,
            "MCM_THOUGHT_SEED_PROTOCOL_DEBUG": False,
            "MCM_THOUGHT_DIGEST_PROTOCOL_DEBUG": False,
            "MCM_VISUAL_CORTEX_PROTOCOL_DEBUG": False,
            "MCM_VISUAL_SNAPSHOT_WRITE_EVERY_N": 250,
        },
        "LIVE_DEBUG": {
            "DEBUG_WRITE_MODE": "buffered_safe",
            "DEBUG_WRITE_EVERY_N": 10,
            "DEBUG_BUFFER_FLUSH_EVERY_N": 250,
            "DEBUG_BUFFER_FLUSH_SECONDS": 5.0,
            "MCM_DEBUG": True,
            "MCM_OUTCOME_DEBUG": True,
            "MCM_RUNTIME_PROFILE_DEBUG": False,
            "MCM_FILE_WRITE_PROFILE_DEBUG": False,
            "TRADE_STATS_ATTEMPT_RECORD_DEBUG": True,
            "TRADE_STATS_ATTEMPT_RECORD_EVERY_N": 10,
            "TRADE_STATS_ATTEMPT_RECORD_COMPACT": True,
            "MCM_STRATEGIC_WINDOW_PROTOCOL_DEBUG": False,
            "MCM_ACTIVE_CONTACT_PROTOCOL_DEBUG": True,
            "MCM_FIELD_DECISION_PROTOCOL_DEBUG": True,
            "MCM_FIELD_DECISION_PROTOCOL_EVERY_N": 10,
            "MCM_NEURO_TRANSITION_PROTOCOL_DEBUG": True,
            "MCM_NEURO_TRANSITION_PROTOCOL_CONTEXT": 2,
            "MCM_MEMORY_THINKING_PROTOCOL_DEBUG": True,
            "MCM_MEMORY_THINKING_PROTOCOL_EVERY_N": 20,
            "MCM_POSITION_INTERVENTION_PROTOCOL_DEBUG": True,
            "MCM_POSITION_INTERVENTION_PROTOCOL_EVERY_N": 5,
            "MCM_TARGET_EXPECTATION_PROTOCOL_DEBUG": True,
            "MCM_TARGET_EXPECTATION_PROTOCOL_EVERY_N": 10,
            "MCM_EXIT_CANDIDATE_OBSERVE_DEBUG": True,
            "MCM_IDLE_THINKING_PROTOCOL_DEBUG": True,
            "MCM_IDLE_THINKING_PROTOCOL_EVERY_N": 5,
            "MCM_FORM_SYMBOL_PROTOCOL_DEBUG": True,
            "MCM_FORM_SYMBOL_PROTOCOL_EVERY_N": 20,
            "MCM_THOUGHT_SEED_PROTOCOL_DEBUG": True,
            "MCM_THOUGHT_SEED_PROTOCOL_EVERY_N": 20,
            "MCM_THOUGHT_DIGEST_PROTOCOL_DEBUG": True,
            "MCM_THOUGHT_DIGEST_PROTOCOL_EVERY_N": 10,
            "MCM_VISUAL_CORTEX_PROTOCOL_DEBUG": True,
            "MCM_VISUAL_CORTEX_PROTOCOL_EVERY_N": 20,
            "MCM_VISUAL_SNAPSHOT_WRITE_EVERY_N": 25,
        },
    }

    selected = dict(profiles.get(profile, profiles["DIO_CORE_DEBUG"]) or {})
    for key, value in selected.items():
        setattr(Config, key, value)
    Config.DEBUG_OUTPUT_PROFILE_ACTIVE = profile if profile in profiles else "DIO_CORE_DEBUG"


_apply_debug_output_profile()

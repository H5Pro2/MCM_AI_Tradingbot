# MCM Trading Brain

MCM Trading Brain ist ein experimentelles Trading-System, das Marktverarbeitung nicht als direkte Reaktion auf OHLC-Daten modelliert, sondern als mehrstufigen inneren Entscheidungsprozess.

Ziel ist eine Architektur, die dem Ablauf eines menschlichen Traders näherkommt:

1. **Außenwelt lesen**
2. **innerlich verarbeiten**
3. **metakognitiv freigeben oder blockieren**
4. **erst danach planen und handeln**
5. **Ergebnisse gezielt zurücklernen**

Der Fokus liegt damit nicht auf klassischen Indikatoren, sondern auf einer MCM-basierten Zustandsverarbeitung aus Wahrnehmung, Erleben, Denken, Regulation, Planung und Outcome-Lernen.

---

## Setup

Für einen lokalen Start müssen zuerst die Python-Abhängigkeiten installiert werden:

```bash
pip install -r requirements.txt
```

Danach kann der Bot über `runner.py` im in `config.py` gesetzten Modus (`BACKTEST` oder `LIVE`) gestartet werden.

---

## Projektidee

Das System behandelt den Markt nicht nur als Preisreihe, sondern als äußeres Reizfeld.

Aus einer Kerze werden zunächst elementare Marktmerkmale abgeleitet, zum Beispiel:

- Kerzenspanne
- Close-Position
- Wick-Bias
- Return-Intensität
- Energie
- Kohärenz
- Asymmetrie
- Kohäsionszone

Darauf aufbauend entsteht ein interner Verarbeitungsweg:

- **Außenbild** des Marktes
- **Wahrnehmung** des Außenbilds
- **Erlebenszustand**
- **Denkzustand**
- **Metaregulation**
- **Trade-Plan**
- **Ausführung / Pending / Exit**
- **Lernen aus Outcomes**

Dieser Ansatz folgt der Richtung des Umsetzungsplans: Markt nicht direkt handeln, sondern erst intern verarbeiten und nur freigegebene Zustände ausführen. fileciteturn1file7

---

## Aktueller Architekturstand

Der aktuelle Code bildet die MCM-Architektur bereits in mehrere Ebenen auf:

### 1. Außenbahn

Die Außenbahn liest nur den Markt.

Sie besteht aktuell aus:

- `CSVFeed` für Backtest-Daten in `csv_feed.py` fileciteturn0file3
- Live-/Exchange-Daten in `ph_ohlcv.py` fileciteturn0file6
- Kerzenabbildung über `_build_candle_state(...)` in `ph_ohlcv.py` fileciteturn1file5
- Spannungsberechnung über `compute_tension_from_ohlc(...)` in `mcm_core_engine.py` fileciteturn0file13

Hier entstehen unter anderem:

- `candle_state`
- `tension_state`
- Marktvision / Stimulus

### 2. Innenbahn

Die Innenbahn verarbeitet das Außenbild intern weiter.

Im aktuellen Stand existieren dafür direkt benannte Zustände in `MCM_Brain_Modell.py`:

- `perception_state`
- `felt_state`
- `thought_state`
- `meta_regulation_state` fileciteturn2file17turn2file8turn2file10

Zusätzlich laufen darin:

- Fokusprojektion
- gefilterte Marktvision
- neuronale Modulation
- Signaturspeicher
- Kontext-Cluster
- Zustandsreifung
- Erwartungs- und Druckmodell
- metakognitive Freigabe oder Blockade fileciteturn0file17turn2file4turn2file16

### 3. Exekutivbahn

Die Exekutivbahn plant nur freigegebene Trades und verwaltet deren Ausführung.

Im aktuellen Stand:

- Entry-Entscheidung über `evaluate_entry_decision(...)` in `bot_gate_funktions.py` fileciteturn0file10
- Preisplanung über `derive_trade_plan_from_brain(...)` in `MCM_Brain_Modell.py` fileciteturn2file12turn2file15
- ökonomische Endabsicherung über `TradeValueGate.evaluate(...)` in `trade_value_gate.py` fileciteturn0file15
- Pending-/Positions-/Exit-Verwaltung im `Bot` aus `bot.py` fileciteturn1file6turn2file11
- Live-Order-Handling und Monitor-Thread in `place_orders.py` und `place_orders_funktions.py` fileciteturn0file7turn1file8

### 4. Lernbahn

Das System lernt nicht nur über TP und SL, sondern koppelt Outcomes in mehrere interne Zustände zurück.

Aktuell vorhanden:

- Outcome-Stimuli über `apply_outcome_stimulus(...)` in `MCM_Brain_Modell.py` fileciteturn0file17
- Anpassung von Erwartung, Regulation, Reife, Schutzweite und Mut über `update_experience_state(...)` fileciteturn2file10
- Signaturgedächtnis und Kontextcluster in `MCM_Brain_Modell.py` fileciteturn2file16turn2file4

---

## Reale Pipeline im aktuellen Code

Die operative Pipeline sieht derzeit vereinfacht so aus:

```text
OHLC / Candle
  -> candle_state
  -> tension_state
  -> market vision / stimulus
  -> MCM field step
  -> target model / neural modulation
  -> perception_state
  -> felt_state
  -> thought_state
  -> meta_regulation_state
  -> trade_plan
  -> TradeValueGate
  -> pending entry / order
  -> position / exit
  -> outcome stimulus / learning
```

Das ist näher am aktuellen Code als die alte README, die noch von `resonance_gate.py` und `structure_entry_gate.py` als Kernarchitektur sprach. Die zentrale Entry-Entscheidung läuft jetzt über `decide_mcm_brain_entry(...)` in `MCM_Brain_Modell.py`. fileciteturn2file9turn2file14

---

## Zentrale Dateien

### Kernlogik

- `bot.py`  
  Hauptpipeline für Window-Verarbeitung, Pending, Position, Exit, Outcome-Kopplung. fileciteturn1file6

- `MCM_Brain_Modell.py`  
  Zentrale MCM-Brücke zwischen Marktreiz, innerer Zustandsbildung, Metakontrolle, Preisplanung und Lernen. fileciteturn0file17turn2file14

- `MCM_KI_Modell.py`  
  MCM-Feld, Clusterbildung, Memory, SelfModel, Attraktoren, Regulation. fileciteturn0file9

- `mcm_core_engine.py`  
  Berechnet Energie, Kohärenz, Asymmetrie und Kohäsionszone aus OHLC. fileciteturn0file13

### Markt- und Datenebene

- `csv_feed.py`  
  CSV-Feed mit Sliding-Window für Backtests. fileciteturn0file3

- `ph_ohlcv.py`  
  Exchange-Zugriff, Live-Preis, Candle-State, Balance-Prüfungen, OHLCV-Fetch. fileciteturn0file6turn1file5

- `workspace.py`  
  Schreibt Live-/Snapshot-Workspace-Dateien. fileciteturn0file11

### Ausführung und Absicherung

- `trade_value_gate.py`  
  Ökonomische Endabsicherung für Geometrie, RR, TP-Mindestdistanz und maximale SL-Distanz. fileciteturn0file15

- `place_orders.py`  
  Order-Platzierung, Marktverschiebungs-Check, Missed-TP-Handling, Monitor-Loop. fileciteturn0file7turn1file11

- `place_orders_funktions.py`  
  Exchange-Sync, aktive Order-Snapshots, Cancel-Tracking, Failsafe bei offenen Positionen. fileciteturn1file8turn2file19

- `exit_engine.py`  
  Exit-Verarbeitung für TP/SL inklusive Trade-Debug-Daten. fileciteturn0file14

### Statistik und GUI

- `trade_stats.py`  
  Persistente Trade-Statistik, Equity-CSV, Exit- und Cancel-Zählung. fileciteturn2file16turn1file13

- `_gui.py`  
  Read-only GUI für Statistik, Equity-Verlauf und RL-/Memory-Heatmap. fileciteturn0file2

- `debug_reader.py`  
  Zentrales Debug-Write-Backend. fileciteturn0file12

- `runner.py`  
  Startpunkt für Backtest und Live-Modus. fileciteturn0file4

---

## Wichtige Zustände im aktuellen System

### Außenbezogen

- `candle_state`
- `tension_state`
- `vision`
- `filtered_vision`
- `focus`

### Innenbezogen

- `perception_state`
  - Fokus
  - Unsicherheit
  - Neuheit
  - Signalqualität
  - Beobachtungspriorität

- `felt_state`
  - gefühltes Risiko
  - gefühlte Chance
  - Konflikt
  - Druck
  - Stabilität
  - Erwartung
  - Schutzweitenregulation
  - protective courage

- `thought_state`
  - Long-/Short-/Wait-Hypothese
  - Konfliktgrad
  - Reifegrad
  - Grübeltiefe
  - Entscheidungsbereitschaft

- `meta_regulation_state`
  - beobachten
  - grübeln
  - planen
  - blockieren
  - Ablehnungsgrund fileciteturn2file17turn2file8turn2file10

### Planungsbezogen

- `entry_price`
- `sl_price`
- `tp_price`
- `rr_value`
- `entry_validity_band`
- `target_conviction`
- `risk_model_score`
- `reward_model_score` fileciteturn2file14turn2file12

---

## Was das System aktuell bereits macht

### 1. Markt lesen

Aus jeder Kerze wird ein äußerer Zustand gebaut:

- Kerzenform
- Spannungszustand
- Fokus- und Marktvision

### 2. intern verarbeiten

Das MCM-System überführt den Außenreiz in:

- Feldzustand
- Gedächtnisrückkopplung
- Attraktorwahl
- Wahrnehmung
- Erleben
- Denken
- Metaregulation

### 3. unreife Zustände blockieren

Ein Trade wird nicht nur wegen RR oder SL blockiert, sondern schon vorher durch interne Zustandslogik, zum Beispiel bei:

- Beobachtungsmodus
- hoher Unsicherheit
- hohem Konflikt
- zu geringer Reife
- Pause nach negativen Outcomes fileciteturn2file10

### 4. Preisplanung aus innerem Zustand

Entry, SL und TP werden nicht statisch gesetzt, sondern aus mehreren Zustandsgrößen abgeleitet, darunter:

- Fokus
- Signalqualität
- Bedrohungslage
- target conviction
- regulation pressure
- load bearing capacity
- protective width regulation
- protective courage fileciteturn2file12turn2file15

### 5. externe Absicherung

Vor Ausführung wird der Plan über das `TradeValueGate` final abgesichert:

- Geometrie korrekt
- Reward > 0
- Risk > 0
- Mindest-RR erfüllt
- TP-Abstand groß genug
- SL-Abstand nicht zu groß fileciteturn0file15

### 6. Lernen aus Ergebnis

Outcomes wie

- `tp_hit`
- `sl_hit`
- `cancel`
- `timeout`
- `reward_too_small`
- `rr_too_low`
- `sl_distance_too_high`

wirken zurück auf:

- Fokusvertrauen
- target lock
- target drift
- Erwartungsdruck
- Reifung
- Schutzweitenregulation
- Signatur- und Kontextgedächtnis fileciteturn0file17turn2file10

---

## Modus

Die Konfiguration erfolgt zentral in `config.py`. Standardmäßig ist dort aktuell `BACKTEST` aktiv. fileciteturn0file18

### BACKTEST

- Daten kommen aus CSV
- Verarbeitung läuft sequenziell über Sliding Windows
- Trades werden als Pending/Position simuliert
- Statistik und Equity werden lokal geschrieben fileciteturn0file4turn2file11turn2file16

### LIVE

- Daten kommen über Phemex / ccxt
- Workspace wird fortlaufend aktualisiert
- offene Orders und Positionen werden synchronisiert
- Marktverschiebungen können Pending-Orders ungültig machen fileciteturn0file4turn1file11

---

## Start

### Backtest starten

```bash
python runner.py
```

### GUI starten

```bash
python _gui.py
```

Die GUI liest nur:

- `debug/trade_stats.json`
- `debug/trade_equity.csv`

und startet keinen Bot. fileciteturn0file2

---

## Abhängigkeiten

Je nach genutztem Modus werden unter anderem verwendet:

- `ccxt`
- `numpy`
- `scikit-learn`
- `matplotlib`
- `tkinter`

Das System ist als Forschungs- und Entwicklungsprojekt aufgebaut, nicht als fertiges Produkt.

---

## Stand gegenüber dem Umsetzungsplan

Der aktuelle Code ist deutlich näher am Umsetzungsplan als die alte README, aber noch nicht vollständig am Endzustand.

Bereits klar erkennbar umgesetzt sind:

- Trennung von Außenverarbeitung und Innenverarbeitung
- `perception_state`, `felt_state`, `thought_state`, `meta_regulation_state`
- metakognitive Vorselektion vor Preisplanung
- Schutzweiten- und Zielweitenlogik als Zustandsprodukt
- Signatur- und Kontextlernen
- Outcome-Rückkopplung in mehrere Ebenen fileciteturn1file9turn2file8turn2file10

Noch nicht vollständig als streng getrennte Endarchitektur ausformuliert sind:

- ein explizites persistentes `world_state`
- eine vollständig getrennte `outcome_decomposition`
- vollständig harte Schichttrennung zwischen allen Lernarten

Der aktuelle Stand ist daher am besten als **funktionsfähige Zwischenstufe einer MCM-Zustandsarchitektur** zu verstehen, nicht als final abgeschlossene Endform.

---

## Hinweis

Dieses Projekt ist experimentell.

Es dient der Modellierung und Erforschung eines MCM-basierten Trading-Prozesses.

Es ist **keine Finanzberatung**.

---

## Dateiname

`README.md`

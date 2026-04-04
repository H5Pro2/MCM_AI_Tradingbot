# MCM Trading Brain

MCM Trading Brain ist ein experimentelles Trading-System mit MCM-Architektur (Wahrnehmung → innere Verarbeitung → Regulation → Handlung → Lernen).

## Kernprinzip

**KI/Bot haben keine festen Gates oder starren Handelsregeln als Kernlogik.**

Das Ziel ist, dass sich Regeln durch Erfahrung selbst herausbilden:
- Außenwelt erkennen (Markt, Struktur, Spannung)
- Innenzustand verarbeiten (Druck, Konflikt, Reife, Bereitschaft)
- Trade-Versuche beobachten (auch Cancel/No-Fill)
- Outcomes rückkoppeln und Präferenzen lernen

Dadurch soll der Bot mit der Zeit überwiegend dort handeln, wo der Kontext robust ist (z. B. in stabilen Struktur-Zonen), statt durch harte if/else-Regeln gesteuert zu sein.

---

## Setup

```bash
pip install -r requirements.txt
```

Start über:

```bash
python runner.py
```

Der Modus wird in `config.py` gesetzt (`BACKTEST` oder `LIVE`).

---

## Architektur (vereinfacht)

```text
OHLC/Marktdaten
  -> Außenzustand (candle_state, tension_state, world_state)
  -> Wahrnehmung (u. a. Struktur-Signale)
  -> Innenzustand (felt_state, thought_state)
  -> Meta-Regulation (freigeben / beobachten / zurückhalten)
  -> Trade-Plan und Ausführung
  -> Outcome-Decomposition
  -> Erfahrungsupdate
```

### Außenbahn
- Marktdaten aus CSV oder Exchange
- Candle/Tension/World-State
- Struktur als weicher Wahrnehmungskanal

### Innenbahn
- `perception_state`
- `felt_state`
- `thought_state`
- `meta_regulation_state`

### Lernbahn
- Outcome-Decomposition wird mit Kontext gespeichert
- Erfahrung passt Erwartung, Schutzweite, Reife und Bereitschaft adaptiv an

---

## Struktur-Thematik (wichtig)

`strukture_engine.py` ist als **Soft-Perception** gedacht:
- keine feste LONG/SHORT-Entscheidung
- kein hartes Entry-Gate
- keine statische Trade-Freigabe

Die Signale (z. B. `zone_proximity`, `structure_quality`, `structure_stability`) sind Eingänge für lernende Schichten.

---

## Overtrade & Erfahrung

Overtrade soll **nicht** primär über starre Verbote gelöst werden, sondern über lernbare Selbstregulation:
- Versuchsdichte vs. Outcome-Qualität
- Stress-/Druckanstieg nach Fehlserien
- adaptive Zurückhaltung in schwachen Kontexten

So lernt der Bot, welche Versuchsfrequenz und welche Strukturkontexte langfristig bessere Trades liefern.

---

## Umsetzungsplan

Der detaillierte, aktualisierte Plan liegt in:

- `UMSETZUNGSPLAN.md`

Mit Fokus auf:
1. Struktur-Wahrnehmung (sensorisch, ohne harte Regeln)
2. Kopplung von Außen- und Innenzustand
3. Trade-Versuche als Lernobjekt
4. Overtrade-Reduktion durch adaptive Regulation
5. Erfahrungslernen für bessere Struktur-Trades
6. Messbarkeit über KPIs


# --------------------------------------------------
# Thread 1
# --------------------------------------------------

## Chart-Ablauf / Informationen

### Aufgabe

- OHLCV lesen
- Workspace / Buffer pflegen
- reine Marktinformationen berechnen:
  - Candle-State
  - Energy
  - Coherence
  - Asymmetry
  - HH
  - LL
  - Struktur
- nur Stimulus-/Info-Paket erzeugen
- niemals entscheiden
- niemals Memory ändern
- niemals Order / Pending / Position anfassen

### Gehört dahin

- `runner.py` Feed-/Polling-Ablauf
- `csv_feed.py` / `ph_ohlcv.py` / `workspace.py` Datenpfad
- `mcm_core_engine.py` Spannungs-/Chartinfos wie Energy / Coherence / Asymmetry
- `strukture_engine.py` reine Struktur-Wahrnehmung ohne Handelsfreigabe

### Output von Thread 1

Nur ein neutrales Paket, zum Beispiel:

- `timestamp`
- `window_ref` oder `window_snapshot`
- `candle_state`
- `tension_state`
- `structure_perception_state`

# --------------------------------------------------
# Thread 2
# --------------------------------------------------

## Wahrnehmung / Denken / Memory / Handeln

### Aufgabe

- Stimulus von Thread 1 konsumieren
- Runtime permanent fortschreiben
- Wahrnehmung / Verarbeitung / Gefühl / Denken / Meta / Erwartung bilden
- Experience / Episode / Memory pflegen
- Entscheidungstendenz bilden:
  - `act`
  - `observe`
  - `hold`
  - `replan`
- danach technische Handlung ausführen:
  - Pending
  - Entry
  - Position
  - Exit

### Gehört dahin

- `MCMBrainRuntime` und Runtime-Fortschreibung in `MCM_Brain_Modell.py`
- Entscheidungsbahn `build_runtime_decision_tendency(...)` / `decide_mcm_brain_entry(...)`
- Episoden-/Erfahrungsraum / Review / Memory in `MCM_Brain_Modell.py` und `memory_state.py`
- Handlungsbahn in `bot.py`:
  - `_handle_active_position(...)`
  - `_handle_pending_entry(...)`
  - `_handle_entry_attempt(...)`

# --------------------------------------------------
# Harte Regel der Trennung
# --------------------------------------------------

## Harte Regel der Trennung

### Thread 1 schreibt nie

- `mcm_runtime_snapshot`
- `mcm_runtime_decision_state`
- `mcm_runtime_brain_snapshot`
- `mcm_decision_episode`
- `mcm_decision_episode_internal`
- `mcm_experience_space`
- `position`
- `pending_entry`

### Grundregeln

- Thread 2 liest Chartdaten nur als Input, erzeugt aber selbst keine OHLCV-Beschaffung.
- Handlung darf nur noch aus Thread 2 kommen.
- Thread 1 kennt keine Orderlogik.

# --------------------------------------------------
# Zielbild
# --------------------------------------------------

## Zielbild

### Thread 1

- fetch/read market
- normalize
- build chart-info packet
- publish to thread 2

### Thread 2

- consume packet
- runtime tick
- perception/thinking/memory
- decision tendency
- handle pending/entry/position/exit
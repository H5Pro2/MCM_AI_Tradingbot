# ==================================================
# AKTUELLER STAND – MCM TRADING BRAIN
# ==================================================

Dieses Dokument beschreibt den **aktuellen realen Ist-Zustand** des Systems.

Es ist **nicht** der Bauplan.
Der Bauplan steht in `UMSETZUNGSPLAN.md`.

Hier steht:

- was bereits real im Code umgesetzt ist
- was bereits strukturell angelegt ist
- was nur teilweise verhärtet ist
- was als Architektur-Endausbau noch offen bleibt

---

# --------------------------------------------------
# 1. Gesamtstatus
# --------------------------------------------------

Das Projekt ist nicht mehr in einer frühen Basis- oder Fix-Phase.

Die Kernbasis steht bereits:

- äußere Wahrnehmung ist vorhanden
- innere Runtime ist vorhanden
- Zustandskette ist vorhanden
- Entscheidungstendenz ist vorhanden
- technische Handlungsbahn ist vorhanden
- Episode / Review / Experience sind vorhanden
- Persistenz- und KPI-Basis sind vorhanden

Die Hauptarbeit liegt jetzt **nicht mehr** in der Einführung der Grundmechanik,
sondern im **Architektur-Endausbau**.

---

# --------------------------------------------------
# 2. Bereits umgesetzt
# --------------------------------------------------

# --------------------------------------------------
# 2.1 Ebene 1 – äußeres Wahrnehmen
# --------------------------------------------------

Ebene 1 ist bereits als eigenständige Wahrnehmungsbasis angelegt.

Bereits vorhanden sind:

- OHLCV-Datenpfad
- Workspace-/Fensterlogik
- `candle_state`
- `tension_state`
- `visual_market_state`
- `structure_perception_state`

### Fachliche Bedeutung

Die Außenwelt wird bereits nicht mehr nur als einfache Signalquelle behandelt.

Sie wird im aktuellen Code als mehrschichtige Wahrnehmung erfasst:

- Candle-Zustand
- Spannungszustand
- numerische äußere Marktform
- Struktur-Wahrnehmung

### Wichtiger Status

`visual_market_state` ist bereits produktiv im Wahrnehmungspfad angekommen.

Das heißt:

- die Wahrnehmungsbasis ist nicht mehr nur geplant
- sie ist bereits Teil des Bot-Zustands
- sie wird bereits in Runtime und World-State weitergeführt

---

# --------------------------------------------------
# 2.2 Ebene 2 – inneres Wahrnehmen / Denken / Handeln
# --------------------------------------------------

Ebene 2 ist bereits als laufende innere Verarbeitungsschicht vorhanden.

Bereits vorhanden sind:

- `MCMBrainRuntime`
- Runtime-Thread-Modell
- Marktimpuls-Übergabe an die Runtime
- Runtime-Snapshot
- Decision-State
- Brain-Snapshot

### Vorhandene innere Zustandskette

Die gestufte Innenbahn ist bereits angelegt:

- `outer_visual_perception_state`
- `inner_field_perception_state`
- `perception_state`
- `processing_state`
- `felt_state`
- `thought_state`
- `meta_regulation_state`
- `expectation_state`

Diese Zustandskette ist nicht nur dokumentiert,
sondern bereits im aktuellen Codepfad vertreten.

### Entscheidungstendenz

Die Handlung entsteht bereits nicht mehr direkt aus einem einfachen Signal.

Vorhanden ist eine vorgelagerte Entscheidungstendenz:

- `act`
- `observe`
- `hold`
- `replan`

Erst danach folgt die technische Handelsbahn.

### Technische Handlungsbahn

Weiterhin vorhanden und aktiv:

- Pending
- Entry
- Position
- Exit

Damit ist die Handlungsmechanik bereits an die innere Zustandslogik gekoppelt,
auch wenn die architektonische Trennung noch nicht vollständig zu Ende geführt ist.

---

# --------------------------------------------------
# 2.3 MCM-Zustandsraum
# --------------------------------------------------

Der MCM-Raum ist nicht mehr nur implizit,
sondern bereits teilweise explizit lesbar.

Bereits vorhanden sind Zustandsachsen wie:

- `field_density`
- `field_stability`
- `regulatory_load`
- `action_capacity`
- `recovery_need`
- `survival_pressure`

Diese Größen laufen bereits durch Runtime-/Decision-/Snapshot-Strukturen.

Damit ist die spätere Zielidee,
den MCM-Gesamtzustand explizit lesbar zu machen,
im Code bereits begonnen und nicht mehr nur Theorie.

---

# --------------------------------------------------
# 2.4 Ebene 3 – Entwicklung aus Erfahrung
# --------------------------------------------------

Die Entwicklungsebene ist bereits substanziell angelegt.

Vorhanden sind:

- `mcm_decision_episode`
- `mcm_decision_episode_internal`
- `mcm_experience_space`
- `outcome_decomposition`
- Review-Logik
- Signature-Memory
- Context-Cluster
- persistenter Memory-State
- In-Trade-Update-Auswertung
- Experience-Linking
- Similarity-/Axis-/Drift-/Reinforcement-Ansätze

### Fachliche Bedeutung

Das System speichert bereits nicht nur Ausgangsergebnisse,
sondern ganze Entscheidungsverläufe.

Damit ist Ebene 3 bereits mehr als nur Statistik oder Log.

Sie wirkt schon als Entwicklungsraum für:

- Entscheidungsepisoden
- Nicht-Handlung
- Kontextbewertung
- regulatorische Rückkopplung
- langfristige Veränderung der Innenbahn

---

# --------------------------------------------------
# 2.5 Persistenz / KPI / Nachweis
# --------------------------------------------------

Auch die Nachweis- und Speicherbasis ist bereits aufgebaut.

Vorhanden sind:

- `trade_stats.json` als Aggregat
- `attempt_records.jsonl`
- `outcome_records.jsonl`
- getrennte Attempt-/Outcome-Erfassung
- KPI-Zusammenfassung
- Drawdown-/Equity-/Proof-Kennzahlen
- Persistenz für Memory-State
- GUI-/Debug-Lesepfad als Ausgabeschicht

Die Basis für Messbarkeit ist damit vorhanden,
auch wenn sie für die neue Architektur noch weiter ausgebaut werden muss.

---

# --------------------------------------------------
# 3. Bereits teilweise umgesetzt, aber noch nicht verhärtet
# --------------------------------------------------

Ein Teil des Zielbildes ist bereits sichtbar,
aber noch nicht vollständig architektonisch zu Ende geführt.

Dazu gehören insbesondere:

- harte Ebenen-Trennung
- klare Runtime-Entkopplung
- vollständige Trennung von Wahrnehmung, Innenbahn, Entscheidung und Technik
- permanenter Innenprozess als vollständig eigenständige Laufzeitschicht
- vollständige Unterordnung älterer Mischpfade unter die 3-Ebenen-Architektur

Das bedeutet:

Die Richtung stimmt bereits,
aber die Struktur ist an mehreren Stellen noch nicht final verhärtet.

---

# --------------------------------------------------
# 4. Aktuell noch offen
# --------------------------------------------------

# --------------------------------------------------
# 4.1 Architektur-Endausbau
# --------------------------------------------------

Offen bleibt vor allem:

- Ebenen 1 / 2 / 3 technisch vollständig zu entmischen
- Runtime als echten dauerhaften Innenprozess weiter zu vervollständigen
- ältere Mischstellen weiter abzubauen
- Wahrnehmungsbahn, Innenbahn, Entscheidungsbahn und Handlungsbahn noch klarer zu trennen

---

# --------------------------------------------------
# 4.2 MCM-Zustandsraum weiter vertiefen
# --------------------------------------------------

Die Zustandsachsen sind bereits vorhanden,
aber ihre Lesbarkeit und ihr Einsatz sind noch nicht Endzustand.

Weiter offen bleibt:

- tiefere Ableitung aus dem laufenden MCM-Raum
- konsistentere Snapshot-/Debug-/GUI-Lesbarkeit
- stärkere Nutzung dieser Zustände in Review, Experience und Nicht-Handlung
- weitere Härtung gegen starre Fremdlogik

---

# --------------------------------------------------
# 4.3 Entwicklungsebene weiter vertiefen
# --------------------------------------------------

Offen bleibt außerdem:

- Nicht-Handlung als vollständiges Lernobjekt weiter stärken
- Beobachtung / Sammlung / Pause tiefer als wertvolle Episode bewerten
- In-Trade-Lernen weiter ausbauen
- langfristige Veränderung der Innenbahn noch stärker aus Erfahrung ableiten

---

# --------------------------------------------------
# 4.4 Messbarkeit / Nachweis / Tests
# --------------------------------------------------

Die Nachweisbasis ist vorhanden,
aber für den Zielausbau noch nicht vollständig.

Offen bleiben:

- KPI-/Nachweis für neue MCM-Zustände
- KPI-/Nachweis für Nicht-Handlung und Erholung
- erweiterte Debug-/GUI-Lesbarkeit
- dedizierte Tests für:
  - `bot_gate_funktions.py`
  - `mcm_core_engine.py`
  - neue Zustandsachsen
  - regulatorische Pausen-/Beobachtungsdynamik

---

# --------------------------------------------------
# 5. Einordnung des aktuellen Entwicklungsstands
# --------------------------------------------------

Das Projekt ist aktuell in einer Übergangsphase:

nicht mehr

- Basis-Fix
- Rohumbau
- reine Signalmechanik

sondern bereits

- Wahrnehmungssystem
- Runtime-System
- Innenzustandssystem
- Episoden-/Erfahrungssystem
- MCM-basierte Entwicklungsarchitektur

Der Schritt, der jetzt offen ist,
ist vor allem der Übergang von:

- funktionierender MCM-Basis

hin zu:

- vollständig verhärteter MCM-Zielarchitektur

---

# --------------------------------------------------
# 6. Kurzfazit
# --------------------------------------------------

Der aktuelle Stand ist:

- die Grundarchitektur lebt bereits
- die Wahrnehmungsbasis ist aktiv
- die Innenbahn ist aktiv
- Episode / Review / Experience sind aktiv
- Persistenz / KPI sind aktiv

Nicht fertig ist vor allem:

- die endgültige architektonische Trennung
- der vollständig laufende Innenprozess als echte Dauerstruktur
- der Endausbau der Entwicklungs- und Selbstregulationslogik
- die vollständige Messbarkeit der neuen Architektur
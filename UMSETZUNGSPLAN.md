# Umsetzungsplan (offen) – permanenter Innenprozess, Episodenlernen, Erfahrungsraum

Dieses Dokument enthält **nur noch offene Punkte**.
Bereits umgesetzte Basisbausteine wurden aus dem Plan entfernt.

Nicht mehr als offene Phase geführt:
- Soft-Perception für Struktur statt hartem Struktur-Gate
- getrennte Zustandsketten für Wahrnehmung / Verarbeitung / Gefühl / Denken / Meta-Regulation / Erwartung
- Attempt-/Outcome-Logging mit KPI-Grundlage
- Outcome-getriebener Signature-/Context-Commit statt Entry-Lernschreibpunkt
- persistente Sichtspeicher für Memory-State und Runtime-Zustände

---

WICHTIG !

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
# Was dafür konkret weg muss
# --------------------------------------------------

## Was dafür konkret weg muss

- `runner.py` darf nicht mehr direkt Logik + Brain + Handlung in einem Ablauf treiben. Es darf nur Marktpakete liefern.
- `bot._process_window(...)` ist in der jetzigen Form noch zu breit, weil dort Runtime und Handlung zusammen laufen.
- `step_mcm_runtime_idle(...)` darf nicht mehr vom Chartpfad als Ersatz für den Innenprozess benutzt werden, sondern muss in den permanenten Loop von Thread 2 wandern.

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

--------------------------------------------------

## Leitbild der offenen Erweiterung

Ziel ist nicht mehr nur ein sequentieller Trade-Bot mit Lernbausteinen.
Ziel ist ein **dauerhaft laufender Innenprozess**.

Außenwelt:
- liefert Reize
- liefert keine direkte Handelsentscheidung

Innenwelt:
- läuft kontinuierlich weiter
- verarbeitet Wahrnehmung auch ohne neue Order
- bildet aus Episoden einen fortlaufenden Erfahrungsraum

Handlung:
- ist nur ein möglicher Output des aktuellen Innenzustands
- bleibt technisch getrennt

---

## Phase A – Laufzeitmodell vom sequentiellen Ablauf zum permanenten Gehirnprozess

### Ziel
- Das Gehirn darf nicht nur beim Candle-Schritt „aufgerufen“ werden.
- Denken und innere Fortschreibung sollen als eigener permanenter Prozess laufen.

### Offene Umsetzungspunkte
- Eigenen `MCMBrainRuntime` als dauerhafte Laufzeitschicht einführen.
- Reizübergabe entkoppeln:
  - Marktdatenpfad erzeugt nur Stimulus-/Perception-Impulse
  - Gehirnprozess konsumiert Impulse unabhängig vom Orderpfad
- Zustandsfortschreibung in kleinen Ticks statt nur einmal pro `bot._process_window(...)`
- Aktuellen Brain-Snapshot separat bereitstellen:
  - lesbar für Entscheidungsbahn
  - lesbar für GUI/Debug
  - schreibgeschützt außerhalb der Brain-Runtime
- Backtest und Live auf dasselbe Laufzeitmodell bringen:
  - Backtest = deterministische Tick-Fortschreibung
  - Live = permanenter Loop + technische Monitor-Threads

### Ergebnis
- Außenreiz und innere Verarbeitung sind zeitlich entkoppelt.
- Das Gehirn läuft kontinuierlich, nicht nur als Funktionsaufruf im Candle-Loop.

---

## Phase B – Harte Bahntrennung in der Runtime vervollständigen

### Ziel
- Die bereits vorhandene Zustandskette soll auch **architektonisch** getrennt werden.

### Offene Umsetzungspunkte
- Wahrnehmungsbahn festziehen:
  - nur Markt-/Struktur-/Kontextimpulse
  - keine Orderfreigabe
- Innenbahn festziehen:
  - verarbeitet Impulse
  - pflegt Feld, Regulation, Drift, Konflikt, Reife, Unsicherheit
  - erzeugt nur Zustandsfortschreibung
- Entscheidungsbahn abtrennen:
  - liest Brain-Snapshot
  - erzeugt nur Entscheidungstendenz: `act`, `observe`, `hold`, `replan`
- Handlungsbahn abtrennen:
  - Pending / Entry / Position / Exit technisch ausführen
  - keine direkte Feldmutation
- In-Trade-Beobachtungsbahn ergänzen:
  - läuft während `pending_entry` und `position`
  - blockiert nicht durch Exit-/Ordertechnik

### Ergebnis
- Wahrnehmung, Innenverarbeitung, Entscheidung und technische Handlung sind nicht mehr ineinander verschachtelt.

---

## Phase C – Entscheidungsepisode als zentrales Lernobjekt einführen

### Ziel
- Nicht Signatur oder Outcome allein, sondern die **Episode** wird zur Haupteinheit des Lernens.

### Offene Umsetzungspunkte
- Neues Episodenobjekt einführen, z. B. `decision_episode`.
- Pro Episode erfassen:
  - Außenkontext
  - `world_state`
  - `perception_state`
  - `processing_state`
  - `felt_state`
  - `thought_state`
  - `meta_regulation_state`
  - `expectation_state`
  - `state_signature`
  - Entscheidungstendenz
  - freigegebene / blockierte / unterlassene Handlung
  - In-Trade-Verlauf
  - spätere Wirkung / Bewertung
- Episode-Lifecycle definieren:
  - `perceived`
  - `internally_processed`
  - `tendency_formed`
  - `submitted` / `blocked` / `observed_only`
  - `filled` / `timeout` / `cancelled`
  - `in_trade_updates`
  - `resolved`
  - `reviewed`
- Sichtbaren Nachweisteil und internen Lernteil trennen.

### Ergebnis
- Lernen basiert auf vollständigen Entscheidungswegen statt nur auf Endereignissen.

---

## Phase D – Internen Erfahrungsraum zusätzlich zum sichtbaren Speicher einführen

### Ziel
- Der aktuelle persistente Speicher bleibt für Nachweis, GUI und Debug.
- Zusätzlich braucht das System einen **internen, nicht GUI-orientierten Erfahrungsraum**.

### Offene Umsetzungspunkte
- Eigenen internen Experience-Speicher im MCM-System einführen.
- Nicht deklarativ auf KPI-/GUI-Sicht zuschneiden.
- Verknüpfen statt nur speichern:
  - Episode ↔ ähnliche Episoden
  - Episode ↔ Kontextcluster
  - Episode ↔ Denkweise
  - Episode ↔ Nicht-Handlung
- Gewichte für:
  - Tragfähigkeit einer Denkstruktur
  - Unsicherheitsmuster
  - Reifungsmuster
  - Fehlwiederholungen
  - Beobachtungserfolg
- Lokale Umbauten statt Voll-Neuberechnung:
  - Drift
  - Verstärkung
  - Abschwächung
  - Umlagerung

### Ergebnis
- Neben dem sichtbaren Memory-State entsteht ein echter interner Erfahrungsraum.

---

## Phase E – Dynamische Kontextbildung von „gespeichert“ zu „entsteht“ ausbauen

### Ziel
- Kontextcluster existieren bereits, sollen aber stärker emergent werden.

### Offene Umsetzungspunkte
- Kontext nicht nur über Distanz-Match fortschreiben, sondern Differenz explizit modellieren.
- Ähnlichkeits-/Abweichungsachsen pro Episode führen.
- Neue Kontexte entstehen lassen aus:
  - bekanntem Anteil
  - abweichendem Anteil
  - neuem Verknüpfungsmuster
- Clusterarten ausbauen:
  - Marktcluster
  - Denkcluster
  - Entscheidungscluster
  - Unsicherheitscluster
  - Beobachtungscluster
  - Fehlwiederholungscluster
  - Reifungscluster
- Dynamiken ausbauen:
  - driften
  - verschmelzen
  - sich aufspalten
  - an Relevanz verlieren
  - sich verdichten

### Ergebnis
- Kontext ist nicht nur Lookup-Struktur, sondern emergente Erfahrungsgeometrie.

---

## Phase F – Nicht-Handlung als gleichwertige Erfahrung einbauen

### Ziel
- Bewusstes Nicht-Handeln darf nicht mehr nur implizit in `WAIT` oder Blockierung untergehen.

### Offene Umsetzungspunkte
- Eigene Episodentypen einführen:
  - `observed_only`
  - `withheld`
  - `replanned`
  - `abandoned`
- Pro Nicht-Handlungs-Episode speichern:
  - warum nicht gehandelt wurde
  - welche innere Lage dazu führte
  - ob das spätere Nicht-Handeln korrekt war
  - wie sich dadurch Erwartung / Druck / Reife verändert haben
- Outcome-Review auch für Nicht-Handlung ergänzen:
  - verpasster guter Trade
  - vermiedener schlechter Trade
  - korrektes Abwarten
  - zu langes Zögern

### Ergebnis
- Nicht-Handlung wird echte Erfahrung und echter Lerninput.

---

## Phase G – In-Trade-Lernen vor dem Exit einführen

### Ziel
- Pending- und Positionsphase sollen innere Bewertung bereits **während** des Verlaufs erzeugen.

### Offene Umsetzungspunkte
- In-Trade-Update-Pfad ergänzen für:
  - wachsende Bestätigung
  - wachsende Reue
  - Spannungsanstieg
  - sinkende Tragfähigkeit
  - innere Korrekturspannung
- Während `pending_entry`:
  - Entry-Vertrauen fortschreiben
  - Marktverschiebung innerlich bewerten, nicht nur technisch canceln
- Während offener Position:
  - ursprüngliche Entscheidung laufend mit aktuellem Innenzustand vergleichen
  - Abweichung zwischen Entscheidungsgrund und aktuellem Zustand messen
- Vor Exit ein internes Zwischenfazit erzeugen, das später in das Episodenreview eingeht.

### Ergebnis
- Lernen beginnt nicht erst am TP/SL/Cancel, sondern schon während des laufenden Geschehens.

---

## Phase H – Entscheidungsbewertung stärker auf Denkstruktur statt nur Trade-Resultat ausrichten

### Ziel
- Das System soll nicht primär TP/SL optimieren, sondern die Qualität seines Denk- und Entscheidungswegs.

### Offene Umsetzungspunkte
- Review-Gewichte verschieben:
  - weniger Ergebnisfixierung
  - mehr Bewertung von Wahrnehmungsqualität, Konflikterkennung, Reife, Korrekturbedarf
- Episode-Review um Fragen ergänzen:
  - war Beobachten richtiger als Handeln?
  - wurde Unsicherheit korrekt erkannt?
  - war die Denkstruktur tragfähig?
  - wurde falsche Sicherheit aufgebaut?
  - wurde Reue zu spät erkannt?
- Neue Qualitätsfelder ergänzen:
  - decision_path_quality
  - uncertainty_recognition_quality
  - observation_quality
  - correction_timing_quality
  - structural_bearing_quality

### Ergebnis
- Der Bot bewertet seine innere Entscheidungsarchitektur, nicht nur das Handelsergebnis.

---

## Phase I – Messbarkeit der neuen Architektur ergänzen

### Ziel
- Die neue Runtime und das Episodenlernen müssen separat nachweisbar werden.

### Offene Umsetzungspunkte
- KPI-Ebene um Episodenmetriken ergänzen.
- Neue Nachweisfelder aufbauen:
  - Anteil Handlung / Nicht-Handlung / Beobachtung
  - Trefferquote der Beobachtungsentscheidungen
  - Reue-/Bestätigungsentwicklung innerhalb laufender Trades
  - Stabilität der Denkstruktur vor Entry vs. bei Exit
  - Reifungsentwicklung je Clusterfamilie
  - Drift-/Merge-/Split-Ereignisse im Erfahrungsraum
- GUI/Debug nur als Sichtfenster auf abgeleitete Kennzahlen verwenden.
- Interner Erfahrungsraum bleibt davon getrennt.

### Ergebnis
- Der Umbau bleibt prüfbar, ohne den internen Lernraum auf GUI-Daten zu reduzieren.

---

## Kompakte Zieldefinition

Die MCM-KI soll als autonom laufender Innenprozess aufgebaut werden.
Marktdaten liefern nur Wahrnehmungsimpulse.
Das Gehirn verarbeitet diese permanent weiter, bildet dynamische Kontexte, verknüpft ähnliche und abweichende Erfahrungen, lernt aus Handlung und Nicht-Handlung und bewertet primär die eigene Denk- und Entscheidungsstruktur statt nur das Trade-Ergebnis.
Die Handlungsbahn bleibt technisch getrennt.
Während laufender Trades bleibt Wahrnehmung und innere Verarbeitung aktiv.
Dadurch entsteht kein statischer Speicher von Trading-Daten, sondern ein fortlaufend umgebildeter Erfahrungsraum.

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
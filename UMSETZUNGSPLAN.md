# Umsetzungsplan (neu) – Struktur, Overtrade, Erfahrung

Dieses Projektziel bleibt: **keine festen Gates/Regeln**, sondern ein Bot, der Handelsregeln aus Erfahrung selbst lernt.

Der Fokus ist, dass der Bot überwiegend in guten **Struktur-Zonen** tradet, indem er Struktur erst erkennt, intern verarbeitet und Ergebnisse rücklernt.

## Leitbild

1. **Erkennen/Sehen** (Außen): Marktstruktur, Zonen-Nähe, Spannungs- und Kontextlage wahrnehmen.
2. **Innenzustand** (Innen): Risikoempfinden, Konflikt, Reife, Selbstvertrauen und Stress intern modellieren.
3. **Trade-Versuche**: Jeder Versuch wird als Lernsignal gespeichert (auch Cancel/No-Fill).
4. **Erfahrung**: Gute/schlechte Outcomes werden mit Kontext verknüpft und als Präferenz rückgeführt.
5. **Erkenntnisse**: Bot lernt, wann Struktur-Zonen wirklich funktionieren (statt hardcodierter Entry-Regeln).

---

## Phase 1 – Struktur-Wahrnehmung als Sensorik (ohne Entry-Regel)

### Ziele
- `strukture_engine.py` bleibt ein **reiner Wahrnehmungsbaustein**.
- Keine LONG/SHORT-Entscheidung im Strukturmodul.
- Keine harte Freigabe/Blockade durch Struktur.

### Umsetzungspunkte
- Struktur-Features als kontinuierliche Signale bereitstellen:
  - `structure_seen`, `structure_high`, `structure_low`, `structure_range`
  - `zone_proximity`, `structure_quality`, `structure_stability`
  - `stress_relief_potential`, `context_confidence`
- Struktur nur in World/Perception-State einspeisen, nicht direkt in Gate-Funktionen.

### Ergebnis
- Der Bot „sieht“ Strukturzonen, aber entscheidet noch nicht regelbasiert.

---

## Phase 2 – Außen- und Innenzustand systematisch koppeln

### Ziele
- Außenzustand und Innenzustand getrennt, aber klar verknüpft halten.
- Struktur nicht isoliert betrachten, sondern mit psychischem Bot-Zustand kombinieren.

### Außenzustand (Beispiele)
- Candle-/Tension-/Vision-State
- Struktur-Signale aus `strukture_engine.py`
- Markt-Kontext (Volatilität, Energie, Kohärenz)

### Innenzustand (Beispiele)
- `felt_state`: Druck, Chance, Risiko, Stabilität
- `thought_state`: Hypothesenqualität, Konfliktgrad, Reifegrad
- `meta_regulation_state`: Beobachten, Planen, Zurückhalten

### Ergebnis
- Entscheidungen entstehen aus Außen+Innen-Kombination, nicht aus Einzelindikator.

---

## Phase 3 – Trade-Versuche als eigenes Lernobjekt

### Ziele
- Nicht nur abgeschlossene Trades lernen, sondern auch Versuche.
- Overtrade-Muster früh erkennen.

### Umsetzungspunkte
- Pro Versuch ein Attempt-Log führen mit:
  - Zeitpunkt, Kontextfenster, Strukturwerte, Innenzustände
  - Planqualität (RR, SL/TP-Geometrie), Freigabegrad
  - Status: `submitted`, `filled`, `cancelled`, `skipped`
- Attempt-Serien erfassen:
  - Anzahl Versuche pro Zeitfenster
  - Anzahl Versuche pro Strukturkontext
  - Verhältnis gute/schlechte Versuche

### Ergebnis
- Bot versteht, ob er „zu oft“ oder „am falschen Kontext“ versucht.

---

## Phase 4 – Overtrade ohne starre Verbote reduzieren

### Ziele
- Overtrading nicht per harter Regel abschneiden, sondern über adaptive Selbstregulation dämpfen.

### Umsetzungspunkte
- Lernbare Overtrade-Signale aufbauen:
  - Attempt-Frequenz vs. Outcome-Qualität
  - Verlust-Cluster nach kurzer Versuchsdichte
  - Stress-/Druckanstieg nach Fehlserien
- Diese Signale in `meta_regulation_state` einspeisen:
  - temporär mehr „beobachten“
  - geringere Ausführungsbereitschaft bei schlechter Kontextgüte
- Keine fixe „max trades per hour“-Regel als Kernlogik.

### Ergebnis
- Bot reduziert Overtrade kontextsensitiv und erfahrungsgetrieben.

---

## Phase 5 – Erfahrungslernen: Was sind bessere Trades?

### Ziele
- Explizit lernen, welche Konstellationen zu besseren Trades führen.
- Strukturzonen-Präferenz aus Daten statt Handregel.

### Umsetzungspunkte
- Outcome-Decomposition mit Kontext verbinden:
  - Outcome + Strukturqualität + Innenzustand + Attempt-Dichte
- „Bessere Trades“-Merkmale laufend schätzen:
  - Hohe Strukturqualität + niedriger Innenkonflikt
  - Solide Stabilität + kontrollierter Druck
  - Geringe Attempt-Hektik vor Entry
- Präferenzwerte in Erwartung/Mut/Schutzweite rückkoppeln.

### Ergebnis
- Bot entwickelt eine lernbasierte Priorisierung auf hochwertige Struktur-Setups.

---

## Phase 6 – Messbarkeit und Iteration

### KPI-Felder (fortlaufend)
- Trefferquote und Erwartungswert je Struktur-Qualitätsband
- Performance bei hoher vs. niedriger `zone_proximity`
- Outcome nach Attempt-Dichte (Overtrade-Indikator)
- Drawdown-Verlauf relativ zur Versuchsfrequenz

### Iterative Fragen
- Lernt der Bot tatsächlich, in Strukturzonen selektiver zu handeln?
- Sinkt Overtrade-Verhalten ohne starre Verbote?
- Verbessert sich die Qualität der Trades bei stabileren Innenzuständen?

---

## Kurzfassung des Ziels

Der Bot soll **sehen (außen)**, **fühlen/denken (innen)**, **Versuche bewusst verarbeiten** und aus **Erfahrung** lernen,
sodass sich Handelsregeln als emergentes Verhalten bilden – mit einer klaren Tendenz,
überwiegend in robusten Strukturzonen zu traden.

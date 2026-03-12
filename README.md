# MCM Trading System  
Mental Core Matrix – Energetisches Marktmodell

## Überblick

Dieses Projekt implementiert ein Trading-System, das auf der **von mir entwickelten Mental Core Matrix (MCM)** basiert.

Die Mental Core Matrix ist ein konzeptionelles Modell zur Beschreibung dynamischer Entscheidungsprozesse in komplexen Systemen.  
Sie wurde ursprünglich **nicht speziell für Finanzmärkte entwickelt**.

Das hier vorgestellte Trading-System ist daher eine **konzeptionelle Anwendung der MCM auf Marktstrukturen**.

Finanzmärkte eignen sich besonders gut für diese Anwendung, da sie ein komplexes System darstellen, in dem viele Marktteilnehmer gleichzeitig Entscheidungen treffen und dadurch kollektive Muster entstehen.

---

# Grundidee

In den meisten Trading-Systemen werden Märkte als **Preiszeitreihen** betrachtet.

Aus diesen Preisen werden klassische Indikatoren berechnet, zum Beispiel:

- RSI
- Moving Average
- MACD

Dieses System verfolgt einen anderen Ansatz.

Ein Marktchart wird hier nicht nur als Preisdiagramm betrachtet, sondern als **sichtbares Muster kollektiver Entscheidungen**.

Jede Preisbewegung entsteht durch:

- Erwartungen
- Risikoentscheidungen
- Reaktionen auf Informationen
- Liquiditätsverschiebungen
- Emotionen der Marktteilnehmer

Ein Chart kann daher als **psychodynamisches Muster kollektiver Interaktion** verstanden werden.

---

# Kerzen als Flächenenergie

Eine klassische OHLC-Kerze enthält vier Werte:

- Open
- High
- Low
- Close

In diesem System wird eine Kerze nicht nur als Preisintervall interpretiert.

Stattdessen wird sie als **energetische Fläche im Marktspannungsfeld** betrachtet.

Die energetische Struktur einer Kerze entsteht aus:

- der Spanne zwischen High und Low
- der Position von Open und Close
- der Richtung der Bewegung
- der strukturellen Position innerhalb des Marktverlaufs

Eine Kerze kann damit als **kleine Energieeinheit innerhalb des globalen Marktsystems** verstanden werden.

Starke Bewegungen erzeugen höhere energetische Spannung, während ruhige Marktphasen weniger Energie enthalten.

![alt text](Kerzen_Flächenspannung.png)

---

# Energetische Marktparameter

Die Kerzendaten werden in energetische Zustandsgrößen transformiert.

Diese Berechnung erfolgt in:

```
mcm_core_engine.py
```

:contentReference[oaicite:0]{index=0}

Die wichtigsten Zustandsgrößen sind:

| Parameter | Bedeutung |
|----------|-----------|
Energy | Intensität der Bewegung |
Coherence | Ordnung bzw. Richtungsstabilität |
Asymmetry | Richtungsdominanz |
Cohesion Zone | Marktregime |

Dadurch wird der Markt nicht mehr nur als Preisreihe betrachtet, sondern als **energetischer Zustandsraum**.

---

# Trading Pipeline

Der Bot arbeitet mit einer klar strukturierten Pipeline:

```
OHLC Daten
    ↓
compute_tension_from_ohlc
    ↓
ResonanceGate
    ↓
StructureEntryGate
    ↓
Richtung über Asymmetrie
    ↓
Risk / RR Berechnung
    ↓
MCM_AI Entscheidung
    ↓
TradeValueGate
    ↓
Order Ausführung
```

---

# Resonance Gate

Das **ResonanceGate** filtert Marktphasen und blockiert Rauschen.

Implementiert in:

```
resonance_gate.py
```

:contentReference[oaicite:1]{index=1}

Geprüft werden:

- Resonanzstärke
- Phasenstabilität
- Energiegradient
- Stabilitätsfenster

Nur wenn diese Bedingungen erfüllt sind, wird eine Strukturprüfung zugelassen.

---

# Structure Entry Gate

Das **StructureEntryGate** erkennt Marktstruktur.

Implementiert in:

```
structure_entry_gate.py
```

:contentReference[oaicite:2]{index=2}

Erkannte Strukturen:

- Higher High (HH)
- Higher Low (HL)
- Lower High (LH)
- Lower Low (LL)

Zusätzlich werden berechnet:

- structure_strength
- structure_age
- structure_break (BOS / CHOCH)

---

# Richtungsbestimmung

Die Richtung wird nicht direkt aus einer einzelnen Kerze bestimmt.

Stattdessen wird die **Asymmetrie über mehrere Kerzen gemittelt**.

```
asymmetry > 0 → LONG
asymmetry < 0 → SHORT
```

---

# Risiko-Modell

Das Risiko wird dynamisch aus Entrypreis und Marktenergie berechnet.

```
risk = entry_price * risk_pct * energy_scale
```

Der Stop-Loss ergibt sich direkt aus diesem Risiko.

---

# MCM_AI

Die **MCM_AI** ist die adaptive Komponente des Systems.

Sie erhält den vollständigen Marktzustand:

- Energy
- Coherence
- Asymmetry
- Resonance
- Strukturinformationen
- Risiko-Parameter

Die AI kann:

- Trades blockieren
- das Risk-Reward Verhältnis anpassen
- den Entry verfeinern
- aus TP/SL Ergebnissen lernen

Dabei gilt eine wichtige Regel:

Die AI darf den Entry **verbessern, aber nicht verschlechtern**.

Beispiel:

```
LONG:
entry_ai ≤ entry_structure

SHORT:
entry_ai ≥ entry_structure
```

---

# Trade Value Gate

Vor der Orderausführung wird jeder Trade ökonomisch geprüft.

Implementiert in:

```
trade_value_gate.py
```

Die Prüfung beinhaltet:

- Risiko > 0
- Gewinn > 0
- RR über Mindestwert
- Stop-Loss Abstand innerhalb erlaubter Grenzen

---

# Backtesting

Der Bot unterstützt zwei Modi:

```
BACKTEST
LIVE
```

Die Konfiguration erfolgt in:

```
config.py
```

:contentReference[oaicite:3]{index=3}

Backtests verwenden historische OHLC Daten über:

```
csv_feed.py
```

:contentReference[oaicite:4]{index=4}

---

# Orderausführung

Die Orderverwaltung erfolgt über:

```
place_orders.py
```

:contentReference[oaicite:5]{index=5}

Funktionen:

- Order Monitor Thread
- Missed-TP Erkennung
- Neustart-Synchronisation
- Reconnect Handling
- Failsafe bei offenen Positionen

---

# Systemphilosophie

Das System kombiniert zwei Ansätze:

**Regelbasierte Struktur**

- Marktstruktur
- Resonanzfilter
- Risikomanagement

**Adaptive Komponente**

- MCM_AI Bewertung
- Erfahrungsbasierte Anpassung
- Lernen aus Trade-Ergebnissen

Diese Kombination ermöglicht ein System, das strukturell stabil bleibt und sich gleichzeitig an Marktveränderungen anpassen kann.

---

# Forschungsidee

Dieses Projekt untersucht die Hypothese, dass Finanzmärkte als **energetische Systeme kollektiver Entscheidungsprozesse** modelliert werden können.

Indem Kerzen als Flächenenergie interpretiert werden und Marktbewegungen als Gradienten eines Spannungsfeldes betrachtet werden, entsteht eine neue Perspektive auf Marktanalyse.

Der Trading-Bot stellt somit **eine mögliche Anwendung der Mental Core Matrix auf Finanzmärkte dar**.

---

# Hinweis

Dieses Projekt ist ein experimentelles Forschungsprojekt.

Es stellt **keine Finanzberatung** dar.

Der Handel mit Finanzinstrumenten ist mit erheblichen Risiken verbunden.
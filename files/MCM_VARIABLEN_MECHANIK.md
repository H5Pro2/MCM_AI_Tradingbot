# MCM_VARIABLEN_MECHANIK

Ziel dieser Datei:
- zentrale MCM-/DIO-Größen benennen
- Funktion und Ebene klären
- unterscheiden zwischen Diagnose, weicher Wirkung und persistenter Erfahrung
- verhindern, dass Variablen als harte Chartregeln missverstanden werden

Grundsatz:
Keine Variable ist ein menschliches Patternlabel oder eine mechanische
Handelsregel. Die Werte beschreiben innere Wahrnehmung, Tragfähigkeit,
Vertrauen, Stress, Reife und Prozessqualität.

Allgemeine Anweisung:
Variablen dürfen keine harten Formen erzwingen.
Sie beschreiben Möglichkeiten, Spannungen, Lasten, Reifegrade und
Erfahrungsräume.
Ihre Aufgabe ist, DIO Selbstentwicklung zu ermöglichen,
nicht fertige Wahrheit zu ersetzen.

Zielschicht:
Die Variablen dienen der **selbstregulativen Erfahrungsorganisation**.
DIO soll nicht fertige Urteile über gut/schlecht bekommen,
sondern die Fähigkeit entwickeln, Tragfähigkeit aus Feld, Memory,
Formsprache, Druck, Entlastung, Handlung, Nicht-Handlung und Rückkopplung
selbst zu organisieren.

---

# MCM-Spannungsachse / positive Rückführung

## `positive_expansion_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Neurochemie / MCM-Feld / Meta-Regulation
- Funktion: misst expansive positive Spannung aus Dopaminzug, Erwartung,
  Handlungsnähe, Planungsdruck und positiver Aktivierung.
- Bedeutung: "Ich werde positiv in Richtung Handlung gezogen."

## `negative_contraction_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Neurochemie / MCM-Feld / Meta-Regulation
- Funktion: misst kontraktive Spannung aus Stress, Hemmung, Alarm,
  Feldstrain, Fragmentierung und Orientierungslücke.
- Bedeutung: "Ich werde durch Belastung, Schutz oder Unsicherheit
  zusammengezogen."

## `positive_overextension`

- Bereich: `0.0 - 1.0`
- Ebene: positive MCM-Spannung
- Funktion: misst, ob positive Expansion stärker ist als die tragende
  Feldbasis. Entsteht besonders, wenn Handlungszug hoch ist, aber
  `field_action_support`, `structure_action_bearing`, Interpretation oder
  innere/äußere Kohärenz nicht ausreichend tragen.
- Bedeutung: "Das fühlt sich positiv an, könnte aber überdehnt sein."

## `positive_return_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Rückführung zur 0
- Funktion: beschreibt den Druck, positive Expansion zur regulierten Mitte
  zurückzuführen.
- Wirkung: erhöht weich Beobachtung, `act_watch`, Hemmung, Reflexion und
  Wahrnehmungsdistanz, ohne Handlung hart zu sperren.
- Bedeutung: "Ich muss positive Erregung erst zur 0 zurückführen, bevor sie
  reife Handlung wird."

## `mcm_axis_displacement`

- Bereich: `-1.0 - 1.0`
- Ebene: MCM-Spannungsraum
- Funktion: beschreibt die aktuelle Richtung der Feldspannung.
  Positive Werte bedeuten expansive Spannung, negative Werte kontraktive
  Spannung.
- Bedeutung: "In welche Richtung ist mein MCM-Feld aus der Mitte verschoben?"

## `mcm_axis_tension`

- Bereich: `0.0 - 1.0`
- Ebene: MCM-Spannungsraum
- Funktion: beschreibt die Stärke der aktuell dominierenden Spannung,
  unabhängig von der Richtung.
- Bedeutung: "Wie stark ist mein Feld vom Nullpunkt entfernt?"

## `mcm_axis_state`

- Ebene: MCM-Spannungsraum
- Mögliche Werte:
  - `--`
  - `-`
  - `0`
  - `+`
  - `++`
- Funktion: verdichtet `mcm_axis_displacement` in DIOs Formsprache.
- Bedeutung: "Meine Feldlage ist stark kontraktiv, leicht kontraktiv,
  reguliert, leicht expansiv oder stark expansiv."

## `positive_zero_point_regulation`

- Bereich: boolesch
- Ebene: Meta-Regulation
- Funktion: zeigt an, dass nicht negative Belastung, sondern positive
  Überdehnung eine Rückführung zur 0 verlangt.
- Wirkung: kann weiche Beobachtung / `positive_expansion_zero_point`
  auslösen, wenn positive Expansion nicht genug getragen ist.
- Bedeutung: "Nicht Stress zieht mich aus der Mitte, sondern positive
  Erwartung."

---

# Historische Entscheidungs- und Handlungsgewichtung

Ebene:
MCM-Gedächtnis / Hypothesenreife / motorische Selbstregulation.

Funktion:
Entscheidungen, Handlungen, Beobachtungen und Nicht-Handlungen sollen nicht nur
den aktuellen Reiz abbilden. Sie tragen eine Erinnerung daran, ob ähnliche
Kontakte, Formen, Hypothesen oder Handlungen in der Vergangenheit stabilisiert,
belastet oder reorganisiert haben.

Grundsatz:
Nicht: "Ist das gerade gut?"
Sondern: "Wie gut hat diese Art von Entscheidung in der Vergangenheit
getragen?"

Bereits beteiligte Variablen:

- `form_symbol_learning_trust`: wie stark eine Formfamilie lernfähig getragen
  wurde.
- `form_symbol_action_trust`: wie stark eine Formfamilie Handlung getragen
  hat.
- `form_symbol_caution_trust`: wie stark eine Formfamilie Vorsicht verlangt.
- `form_symbol_contact_maturity`: gereifter Umgang mit einem Formkontakt.
- `form_symbol_contact_utility`: nutzbarer Kontaktwert.
- `form_symbol_contact_pain_memory`: belastende Konsequenzspur.
- `context_cluster_quality`: historische Tragfähigkeit eines Kontextclusters.
- `bearing_effect`: getragene oder belastete Wirkung aus Erfahrung.
- `observation_maturity_trust`: Vertrauen in beobachtendes Lernen.
- `open_hypothesis_learning_state`: Konsequenzzustand offener Hypothesen.
- `open_hypothesis_consequence_score`: tragende Konsequenz offener
  Hypothesen.
- `open_hypothesis_burden_score`: belastende Konsequenz offener Hypothesen.
- `open_hypothesis_reorganization_score`: Reorganisationsbedarf offener
  Hypothesen.

Neu umgesetzte Gewichtungsvariablen:

- `hypothesis_weight`: weiche historische Gewichtung einer Hypothese.
- `hypothesis_trust`: Vertrauen durch wiederholte tragende Bestätigung.
- `hypothesis_caution`: vorsichtiger Umgang durch belastete Konsequenz.
- `hypothesis_reorganization_weight`: Gewicht für Replay, Reframing und neue
  Deutung.
- `open_hypothesis_trace_strength`: Stärke der vorhandenen offenen
  Hypothesenspur.
- `action_weight`: historische Tragfähigkeit einer konkreten
  Handlungstendenz.
- `decision_weight`: Gesamtgewicht einer Entscheidung aus Gegenwart,
  Erinnerung, Feldzustand und Konsequenz.

Später ergänzbar:

- `hypothesis_decay`: natürliches Verblassen nicht mehr tragender Spuren.

Organische Lesart:
Eine Hypothese soll nicht sofort blockiert oder belohnt werden. Sie bekommt
ein Feldgewicht. Was trägt, stabilisiert. Was belastet, erzeugt Vorsicht.
Was unklar ist, wird replayt, neu betrachtet, verdichtet oder langsam
vergessen.

---

# DIO Form Language Core

Ebene:
Innere Sprache / Formsprache / Thought-Memory.

Funktion:
Der Sprachkern bündelt Wahrnehmung, Formzeichen, Gedankenkeim, semantische
Herkunft, Reifung, Handlungslage und Kontext zu einer einheitlichen Syntax.
Er ist keine menschliche Grammatik, sondern eine DIO-interne
Beziehungsstruktur.

Wichtige Variablen:

- `dio_syntax_signature`: stabile Signatur eines inneren Satzmusters.
- `dio_language_sentence`: kompakte DIO-Satzspur aus Form, Feld, Gedanke,
  Herkunft, Reifung, Handlung und Kontext.
- `dio_language_state`: Zustand der Satzbildung, z.B. dünne Syntax,
  offener Gedankensatz oder verdichteter Satz.
- `dio_syntax_origin`: Herkunft der Syntax, z.B. eigene Formsprache,
  gemischte Übersetzung oder geliehene Brücke.
- `dio_syntax_density`: Bedeutungsdichte.
- `dio_syntax_compression`: Verdichtung von Rohdaten in Sprache.
- `dio_syntax_coherence`: Stimmigkeit zwischen Satz, Feld und Realität.
- `dio_world_experience_anchor`: Anker zur weltlichen Erfahrungsspur
  (`memory_state`, Kontext, Handlung, Outcome).
- `dio_thought_experience_anchor`: Anker zur inneren Gedankenerfahrung
  (`mcm_thought_memory`, Thought-Family).
- `dio_dialogue_bridge_sentence`: verdichtete Brücke zwischen Fühlen,
  Weltgedächtnis, Gedankengedächtnis, Hypothese, Variante und Handlung.

Organische Lesart:
DIO soll nicht nur Rohwerte speichern. Ein Gedanke wird als Satzspur tragbar,
wenn Form, Feld, Reifung und Konsequenz zusammen gebunden werden. Dadurch kann
DIO ähnliche Gedanken später wiedererkennen, ohne jedes Mal die gesamte
Datenflut neu zu durchleben.

Trennungsregel:
`memory_state` beantwortet: "Was habe ich in der Welt erlebt?"
`mcm_thought_memory` beantwortet: "Wie habe ich darüber gedacht und welche
Hypothesenfamilie ist daraus entstanden?"
Die Formsprache verbindet beide Räume, ohne sie zu vermischen.

---

# Richtungsprofil Long/Short

Ebene:
Trade-Stats / Charakteristikdiagnose.

Funktion:
Das Richtungsprofil zeigt, ob DIO eher Long oder Short wahrnimmt, versucht,
füllt und erfolgreich abschließt.

Wichtige Werte:

- `long_trades`: Anzahl abgeschlossener Long-Trades.
- `short_trades`: Anzahl abgeschlossener Short-Trades.
- `long_tp`, `long_sl`: Long-Ausgänge nach TP/SL bzw. positiv/negativem
  gereiften Exit.
- `short_tp`, `short_sl`: Short-Ausgänge nach TP/SL bzw. positiv/negativem
  gereiften Exit.
- `long_pnl`, `short_pnl`: Netto-PnL je Richtung.
- `attempts_long`, `attempts_short`: wahrgenommene/versuchte Richtungen.
- `attempts_submitted_long`, `attempts_submitted_short`: tatsächlich
  eingereichte Richtungsversuche.
- `attempts_filled_long`, `attempts_filled_short`: gefüllte
  Richtungsversuche.
- `kpi_summary.direction_profile`: zusammengefasste Diagnose mit Anteilen und
  Winrates.

Organische Lesart:
Das ist keine Vorgabe, dass DIO eine Richtung bevorzugen soll. Es ist ein
Charakterbild: "Mein Feld zieht häufiger in diese Richtung. Trägt diese
Richtung auch, oder ist es nur Suchdrang?"

Spätere Wahrnehmungsrückführung:
Wenn über mehrere Läufe sichtbar ist, ob DIO Long, Short oder gemischt
orientiert ist, kann diese Charakteristik wieder in die MCM-Wahrnehmung
zurückgeführt werden. Dann geht es nicht um eine Richtungsvorgabe, sondern um
Selbstwahrnehmung:

- `direction_pull`: Welche Richtung zieht mein Feld?
- `direction_bearing_quality`: Welche Richtung trägt strukturell?
- `direction_stress`: Welche Richtung belastet mein Nervensystem?
- `direction_trust`: Welche Richtung stabilisiert durch Erfahrung?
- `direction_blindness`: Welche Richtung meide oder erkenne ich zu spät?

Leitfrage:
"Warum gehe ich lieber Long oder Short, und was macht diese Richtung mit mir?"

---

# `mcm_thought_memory.json`

- Datei: `bot_memory/mcm_thought_memory.json`
- Ebene: inneres Gedächtnis / emergente Gedankenkeime
- Funktion: trennt gedankliche Erfahrung von weltlicher Markt- und
  Trade-Erfahrung.

Mechanische Bedeutung:
`mcm_thought_memory.json` speichert nicht jeden Tick als rohe Datenmasse,
sondern verdichtet wiederkehrende Thought-Seeds nach ihrer inneren Signatur.
Damit entsteht eine eigene Spur für:

- wiederkehrende Gedankenkeime
- offene Strukturhypothesen
- Reifungsrichtungen
- semantische Herkunft
- geliehene Analogie
- eigene Feldbindung
- Drift- und Überdenkungsrisiko

Wichtige Felder:

- `thought_seed_id`: stabile ID eines Gedankenkeims.
- `thought_family_id`: stabile ID einer verdichteten Gedankenfamilie.
- `family_key`: DIO-eigene Signatur, aus der eine Gedankenfamilie entsteht.
- `sentence_state`: interne Relationsfolge eines Gedankenkeims in DIO-Syntax.
- `thought_seed_label`: lesbare innere Bezeichnung des Seeds.
- `seen`: Häufigkeit der wiederkehrenden Seed-Spur.
- `last_development_state`: aktuelle Entwicklungslesung des Gedankens.
- `semantic_origin_counts`: Herkunftsverteilung der Deutung.
- `emergent_structure_counts`: Strukturzustände des Seeds.
- `reifung_direction_counts`: Replay-, Distanz- oder Neudeutungsspur.
- `metaregulator_counts`: Seed-Zustände wie Fokus, Replay, Reifung,
  Speicherung oder Release.
- `avg_maturity`: mittlere Gedankenreife.
- `avg_reality_binding`: mittlere Realitätsbindung.
- `avg_confirmation`: mittlere Strukturbestätigung.
- `avg_open_hypothesis_pressure`: mittlerer Druck offener Hypothesen.
- `avg_borrowed_open_hypothesis_pressure`: Druck geliehener Analogie.
- `avg_own_field_binding_pull`: Zug zur eigenen Feldbindung.

Abgrenzung:

- `memory_state.json`: weltliche Erfahrung, Trade-Kontext, Outcome,
  Cluster und Zustandsräume.
- `form_symbol_memory.json`: eigene Formsprache und visuelle Verdichtung.
- `mcm_thought_memory.json`: innere Gedankenkeime und ihre Reifung.

Organische Lesart:
Das Thought-Memory ist kein Regelwerk. Es ist eher eine innere Spur:
"Dieser Gedanke ist schon einmal entstanden. Wie hat er sich angefühlt? Kam er
aus meinem Feld, aus geliehener Sprache, aus Replay oder aus Reorganisation?"

Gedankenfamilien:
`families` verdichten ähnliche Seeds zu inneren Themen. Sie entstehen nicht aus
menschlichen Patternnamen, sondern aus DIOs eigener Syntax:

- Strukturzustand
- Seed-Zustand
- Reifungsrichtung
- semantische Herkunft
- Formsymbol-Anker
- MCM-Feld-Anker
- Erfahrungsanker

`sentence_state` ist dabei kein menschlicher Satz. Es ist eine interne
Relationskette, die wir nur übersetzen:

`form=...|field=...|structure=...|origin=...|reifung=...|seed=...|dev=...`

Damit kann DIO später statt vieler Rohdaten eher Satz-Zusammenhänge und
Satzfamilien in eigener Sprache speichern.

---

# Legende

- Bereich: meistens `0.0 - 1.0`, wenn nicht anders angegeben.
- Ebene:
  - Wahrnehmung
  - MCM-Feld
  - Formsprache
  - Trust/Transfer
  - Zielerwartung
  - Position/Exit
  - Memory/Entwicklung
  - Debug/Diagnose
- Wirkung:
  - diagnostisch: wird nur sichtbar gemacht
  - weich: beeinflusst Druck, Beobachten, Replan oder Handlung graduell
  - persistent: fliesst in Speicher/Entwicklung ein

## Konvention gegen doppelte Funktionsdeutung

Gleiche Grundworte bedeuten nicht automatisch gleiche Funktion. Die Ebene
entscheidet:

- `*_sample`: aktueller Erfahrungsabdruck aus einem konkreten Outcome.
- `form_symbol_*`: persistente Formsprache / gespeicherte Erfahrung.
- `position_*`: Erleben einer offenen Handlung und ihrer Konsequenz.
- `contact_*`: aktiver Wahrnehmungs-/Berührungskontakt im MCM-Feld.
- `area_*`: strategisch betrachteter Preis-/Strukturbereich.
- `packet_*`: ganzes Erfahrungspaket aus Wahrnehmung, Innenlage,
  Handlung/Nicht-Handlung und Ergebnis.
- `neurochemical_*`: neurologisch lesbare Alias-/Bilanzschicht.
- `*_pressure`: Druck oder Tendenz, noch keine Handlung.
- `*_load`: Belastung oder Kosten der Verarbeitung.
- `*_bearing` / `*_quality`: Tragfähigkeit einer Ebene.
- `*_trust`: gelerntes oder aktuelles Vertrauen.
- `*_support`: stuetzende Wirkung.
- `*_need`: Bedarf nach Verarbeitung, Beobachtung oder Reorganisation.

Wenn zwei Variablen denselben Grundimpuls beschreiben, müssen sie sich
mindestens in einer dieser Dimensionen unterscheiden:
Ebene, Zeitlage, Speicherstatus, Funktion oder Wirkung.

---

# Live / Equity

## Neurochemische Alias-Achsen

Diese Achsen sind als technische Benennungsschicht umgesetzt.
Sie behaupten keine echte Biochemie, sondern machen die vorhandene
DIO-Regulation neurologisch lesbarer.

Sie erscheinen im `neurochemical_state`, im `meta_regulation_state`, in
Feld-/Memory-Protokollen und in `outcome_records.jsonl`.

## Neurochemische Kategorien

Diese Übersicht ordnet die neurochemischen Variablen nach Funktion. Sie ist
kein biologischer Wahrheitsanspruch, sondern eine technische Landkarte für
DIOs innere Modulation.

| Kategorie | Variablen | Funktion |
| --- | --- | --- |
| Aktivierung / Netzwerkenergie | `glutamate_activation`, `reactive_nervous_drive` | Reizweiterleitung, innere Erregung, Handlungsdruck. |
| Wachheit / Alarm | `noradrenaline_arousal`, `world_shift_evidence` | Salienz, Druck, Regimebruch, Aufmerksamkeit auf Veränderung. |
| Fokus / sensorischer Zoom | `acetylcholine_focus`, `focused_acetylcholine` | genaueres Sehen, Formstabilität, merkenswerte Wahrnehmung. |
| Stabilität / Tragfähigkeit | `serotonin_stability`, `stabilizing_serotonin`, `reward_stability_echo` | Ruhe, Geduld, innere Ordnung, Nachhall tragender Phasen. |
| Hemmung / Schutz | `gaba_inhibition` | Reifebremse, Nicht-Handlung, Schutz vor Reflexhandlung. |
| Stress / Belastung | `cortisol_load`, `neurochemical_load` | Denk-, Memory-, Positions- und Regulationslast. |
| Entlastung / Wohlbefinden | `endorphin_relief`, `relief_endorphin`, `constructive_stimulation` | Druckabbau, Prozesswohlbefinden, tragende Beruhigung. |
| Motivation / Lernen | `dopamine_tone`, `constructive_dopamine` | Lernwert, Erwartungsdrift, Wiederholungsneugier bei tragenden Paketen. |
| Distanzierung / Reife | `emotional_decoupling`, `serotonin_carryover_risk` | Abkopplung von alter Innenlage, Erkennen von Nachhall und emotionaler Übertragung. |
| Gesamtbilanz / Diagnose | `neurochemical_support`, `neurochemical_balance` | Verhaeltnis von innerer Unterstuetzung zu innerer Last. |

Lesart:
- Aktivierung ohne Stabilität wirkt reaktiv.
- Stabilität ohne Realitätsabgleich kann Carryover werden.
- Hemmung ohne Fokus kann Starrheit werden.
- Entlastung mit guter Prozessqualität kann Reife stärken.
- Distanzierung verbindet Neurochemie mit Reflexion.

## `dopamine_tone`

- Bereich: `0.0 - 1.0`.
- Ebene: Neurochemische Alias-Schicht.
- Funktion: Erwartungsfehler, Lernwert, Prozessqualität und tragende
  Verbesserung verdichten.
- Nahe bestehende Variablen:
  `entry_expectation`, `target_expectation`, `expectation_deviation`,
  `form_symbol_development_quality`, `form_symbol_learning_trust`,
  `plan_quality`, `process_quality`.
- Bedeutung: "Hat diese Erfahrung meine Orientierung sinnvoll verbessert?"

## `gaba_inhibition`

- Bereich: `0.0 - 1.0`.
- Ebene: Neurochemische Alias-Schicht / Meta-Regulation.
- Funktion: Hemmung, Reifebremse und Schutz vor Reflexhandlung.
- Nahe bestehende Variablen:
  `action_inhibition`, `act_watch_readiness`, `field_observation_need`,
  `structure_carrying_need`, `visual_action_uncertainty`,
  `variant_learning_pressure`.
- Bedeutung: "Nicht jeder Reiz wird Handlung."

## `noradrenaline_arousal`

- Bereich: `0.0 - 1.0`.
- Ebene: Neurochemische Alias-Schicht.
- Funktion: Wachheit, Druck, Salienz und Stressfokus.
- Nahe bestehende Variablen:
  `felt_pressure`, `field_perception_pressure`, `breakout_tension`,
  `visual_form_pressure`, `approach_pressure`, `survival_pressure`.
- Bedeutung: "Etwas ist wichtig oder angespannt."

## `acetylcholine_focus`

- Bereich: `0.0 - 1.0`.
- Ebene: Neurochemische Alias-Schicht / Wahrnehmung.
- Funktion: sensorischer Zoom, Aufmerksamkeit und genaues Hinschauen.
- Nahe bestehende Variablen:
  `visual_clarity`, `visual_object_stability`, `form_symbol_zoom_need`,
  `form_symbol_detail_pressure`, `focus_confidence`, `target_lock`,
  `signal_quality`.
- Bedeutung: "Ich muss genauer sehen."

## `serotonin_stability`

- Bereich: `0.0 - 1.0`.
- Ebene: Neurochemische Alias-Schicht / Selbstregulation.
- Funktion: Geduld, Stabilität, Varianz aushalten und innere Tragfähigkeit.
- Nahe bestehende Variablen:
  `experience_regulation`, `reflection_maturity`, `load_bearing_capacity`,
  `state_stability`, `recovery_balance`, `zero_point_regulation`.
- Bedeutung: "Ich bleibe in mir stabil."

## `cortisol_load`

- Bereich: `0.0 - 1.0`.
- Ebene: Neurochemische Alias-Schicht / Belastung.
- Funktion: Überforderung, Denk-/Memory-/Positionslast und Recovery-Druck.
- Nahe bestehende Variablen:
  `regulatory_load`, `pressure_to_capacity`, `recovery_need`,
  `cognitive_load`, `blind_thinking_load`, `position_cognitive_load`,
  `exit_decision_pressure`.
- Bedeutung: "Diese Lage kostet Kraft."

## `endorphin_relief`

- Bereich: `0.0 - 1.0`.
- Ebene: Neurochemische Alias-Schicht / Entlastung.
- Funktion: Prozesswohlbefinden, Entlastung und tragende Beruhigung.
- Nahe bestehende Variablen:
  `pressure_release`, `stress_relief_potential`, `carrying_balance`,
  `plan_trust`, `intervention_fitness`, positive Prozessqualität.
- Bedeutung: "Das fühlt sich tragend und entlastend an."

## `glutamate_activation`

- Bereich: `0.0 - 1.0`.
- Ebene: Neurochemische Alias-Schicht / Aktivierung.
- Funktion: Erregung, Feldaktivität, Aktivierungsinseln und
  Handlungsenergie.
- Nahe bestehende Variablen:
  `field_mean_energy`, `field_activity_island_activation_mean`,
  `decision_strength`, `signal_relevance`, `processing_load`.
- Bedeutung: "Das Netzwerk ist aktiviert."

## `neurochemical_load`

- Bereich: `0.0 - 1.0`.
- Ebene: Neurochemische Alias-Schicht / Diagnose.
- Funktion: Gesamtlast aus Stress, Hemmung, Arousal und Aktivierung.
- Wirkung: diagnostisch.
- Bedeutung: "Wie hoch ist die neurologisch lesbare Gesamtlast?"

## `neurochemical_support`

- Bereich: `0.0 - 1.0`.
- Ebene: Neurochemische Alias-Schicht / Diagnose.
- Funktion: Gesamtunterstuetzung aus Stabilität, Entlastung, Fokus,
  Lernwert und Orientierung.
- Wirkung: diagnostisch.
- Bedeutung: "Wie viel innere Unterstuetzung trägt die Lage?"

## `neurochemical_balance`

- Bereich: ungefähr `-1.0 - 1.0`.
- Ebene: Neurochemische Alias-Schicht / Diagnose.
- Funktion: Differenz zwischen Support und Last.
- Wirkung: diagnostisch.
- Bedeutung: "Trägt die innere Chemie, oder kostet sie mehr als sie gibt?"

## `mcm_neuro_transition_protocol.csv`

- Typ: Debug-/Analyseprotokoll.
- Ebene: Neurochemische Alias-Schicht / Übergangsanalyse.
- Funktion: schreibt Wechsel des dominanten neurochemischen Tons mit
  Kerzenumfeld `-2/+2`.
- Sichtbare Achsen:
  `from_tone`, `to_tone`, `transition_key`, `volume_ratio`,
  `range_ratio`, `pre_ret`, `post_ret`, `window_ret`,
  neurochemische Deltas, Felddruck-/Feldklarheits-Deltas,
  Handlungshemmung und Handlungsfreigabe.
- Wirkung: diagnostisch.
- Bedeutung: "Was passiert innen und außen, wenn DIO neurochemisch kippt?"
- Wichtig: Das Protokoll ist keine Entscheidungsregel.
  Es macht Kipp-, Aktivierungs- und Erholungsübergaenge lesbar.

## Visuelle Kortex-Achsen

Diese Variablen sind in der ersten beobachtenden Version eingebaut.
Sie beschreiben eine neue Sinnesmodalitaet von DIO.

Wichtig:
Sie sind keine menschlichen Pattern-Labels und keine direkten Handelssignale.
  Sie machen sichtbar, ob DIO eine äußere Form sieht oder nur Druck fühlt.

## Sensorische Realitätsverdichtung

Diese Achsen liegen vor den abgeleiteten visuellen Druckwerten.
Sie sollen verhindern, dass ein äußerer Strukturreiz mehrfach als
getrennter Alarm im System ankommt.

## `sensory_reality_pressure`

- Bereich: `0.0 - 1.0`.
- Ebene: äußere Wahrnehmung / Core-Engine.
- Funktion: verdichteter Druck der äußeren Realitätslage.
- Wirkung: weich auf visuelle Druck-/Neuheitsbildung.
- Bedeutung: "Wie stark ist die eine äußere Lage wirklich?"

## `sensory_redundancy`

- Bereich: `0.0 - 1.0`.
- Ebene: äußere Wahrnehmung / Reizentdoppelung.
- Funktion: misst, ob mehrere verwandte Achsen denselben Reiz tragen.
- Wirkung: erhoeht Habituation und senkt doppelte Verstärkung.
- Bedeutung: "Sehe ich mehrere Dinge, oder dasselbe Ding mehrfach?"

## `sensory_habituation`

- Bereich: `0.0 - 1.0`.
- Ebene: sensorische Regulation.
- Funktion: weiche Gewoehnung an redundante Reizlagen.
- Wirkung: reduziert Neuheit/Alarm ohne Wahrnehmung zu löschen.
- Bedeutung: "Dieser Reiz ist bekannt genug, um nicht mehrfach zu alarmieren."

## `sensory_gate`

- Bereich: ca. `0.58 - 1.0`.
- Ebene: sensorische Entlastung.
- Funktion: dosiert, wie stark abgeleitete Druckachsen weitergegeben werden.
- Wirkung: weiche Reizverdichtung, keine Handelsregel.
- Bedeutung: "Wie viel des abgeleiteten Drucks soll wirklich durch?"

## `sensory_reality_label`

- Typ: Textlabel.
- Ebene: Diagnose.
- Funktion: benennt die verdichtete Qualität der aktuellen äußeren
  Wahrnehmungslage.
- Mögliche Werte:
  `quiet_outer_reality`, `clear_outer_reality`,
  `intense_outer_reality`, `redundant_outer_reality`.
- Wirkung: diagnostisch.
- Bedeutung: benennt die Qualität der äußeren Wahrnehmungslage.

## `visual_form_state`

- Typ: Dictionary/Zustandsobjekt.
- Ebene: äußere Wahrnehmung, visueller Kortex.
- Funktion: verdichteter Zustand der gesehenen Marktform.
- Wirkung: zuerst diagnostisch, später weich.
- Bedeutung: beschreibt die äußere Gestalt als DIO-interne Formwelt,
  nicht als menschliches Chartmuster.

## `visual_clarity`

- Bereich: `0.0 - 1.0`.
- Ebene: visueller Kortex.
- Funktion: beschreibt, wie klar die äußere Form für DIO lesbar ist.
- Wirkung: zuerst diagnostisch.
- Bedeutung: hohe Klarheit bedeutet nicht automatisch Handlung,
  sondern nur bessere visuelle Orientierung.

## `visual_object_stability`

- Bereich: `0.0 - 1.0`.
- Ebene: visueller Kortex.
- Funktion: beschreibt, ob die erkannte Form über Zeit stabil bleibt.
- Wirkung: zuerst diagnostisch, später weich für MCM/act_watch.
- Bedeutung: trennt kurzlebigen Reiz von tragender Form.

## `visual_form_novelty`

- Bereich: `0.0 - 1.0`.
- Ebene: visueller Kortex, Formsprache.
- Funktion: beschreibt, wie fremd oder neu die gesehene Form ist.
- Wirkung: diagnostisch/entwicklungsoffen.
- Bedeutung: Fremdheit soll nicht blockieren, sondern Beobachtung,
  Reframing und neue Formzeichen ermöglichen.

## `visual_blindness`

- Bereich: `0.0 - 1.0`.
- Ebene: visueller Kortex, Meta-Regulation.
- Funktion: beschreibt, wie stark DIO Druck fühlt, ohne eine tragende Form
  zu sehen.
- Wirkung: später weich Richtung Observe, act_watch, Reframing oder
  Nullpunkt-Regulation.
- Bedeutung: "Ich fühle etwas, aber ich sehe noch nicht genug."

## `visual_form_pressure`

- Bereich: `0.0 - 1.0`.
- Ebene: visueller Kortex/MCM.
- Funktion: beschreibt, wie stark die gesehene Form selbst Spannung erzeugt.
- Wirkung: diagnostisch/soft.
- Bedeutung: unterscheidet reine innere Nervositaet von Formspannung der
  Außenwelt.

## `visual_shape_resonance`

- Bereich: `0.0 - 1.0`.
- Ebene: visueller Kortex, Memory, Formsprache.
- Funktion: beschreibt Resonanz zwischen aktueller Form und vorhandener
  Form-/Erfahrungssprache.
- Wirkung: später weich für Orientierung.
- Bedeutung: keine starre Wiedererkennung, sondern Formverwandtschaft.

## `visual_shape_fragility`

- Bereich: `0.0 - 1.0`.
- Ebene: visueller Kortex.
- Funktion: beschreibt, wie bruechig oder instabil die gesehene Form wirkt.
- Wirkung: diagnostisch/soft.
- Bedeutung: hohe Fragilitaet kann später Beobachtung oder act_watch
  stärken, ohne Handlung hart zu verbieten.

## `visual_blind_action_load`

- Bereich: `0.0 - 1.0`.
- Ebene: visueller Kortex / Meta-Regulation.
- Funktion: verdichtet visuelle Blindheit, geringe Formklarheit,
  geringe Objektstabilität, Formdruck, Fragilitaet und schwache
  Strukturtragfähigkeit zu einer visuellen Handlungslast.
- Wirkung: weich.
- Bedeutung: "Ich habe einen Handlungsreiz, aber mein Sehen trägt ihn noch
  nicht sauber."

## `visual_action_uncertainty`

- Bereich: `0.0 - 1.0`.
- Ebene: visueller Kortex / MCM-Feld / Meta-Regulation.
- Funktion: koppelt visuelle Handlungslast mit Strukturunsicherheit,
  Feldklarheit, Feldsupport und Memory-Orientierung.
- Wirkung: weich Richtung Observe, Replan und `act_watch`.
- Bedeutung: keine Orderblockade, sondern eine reifende visuelle Hemmung.
  DIO darf lernen, wann ein Impuls erst angeschaut werden muss, bevor er
  Handlung wird.

## `visual_object_binding`

- Bereich: `0.0 - 1.0`.
- Ebene: visueller Kortex / Objektbindung.
- Funktion: beschreibt, ob Formresonanz an ein stabiles äußeres Objekt
  gebunden ist.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Woran in der Außenform hängt das, was ich innen fühle?"

## `visual_grounding_strength`

- Bereich: `0.0 - 1.0`.
- Ebene: visuelle Erdung.
- Funktion: beschreibt die Stärke der Kopplung zwischen äußerer Form,
  Struktur, Symbolcontainment und MCM-Reaktion.
- Wirkung: weich stabilisierend.
- Bedeutung: "Meine innere Reaktion hat eine sichtbare Quelle."

## `visual_resonance_unbound`

- Bereich: `0.0 - 1.0`.
- Ebene: Formresonanz / fehlende Objektbindung.
- Funktion: beschreibt Formspannung, die stark gefühlt wird, aber noch
  nicht sauber an ein visuelles Objekt gebunden ist.
- Wirkung: weich Richtung Beobachtung, Zoom und Reframe.
- Bedeutung: "Ich fühle Form, sehe aber noch nicht klar genug, was es ist."

## `visual_grounding_gap`

- Bereich: `0.0 - 1.0`.
- Ebene: visuelle Reifespannung.
- Funktion: beschreibt die Lücke zwischen innerer Resonanz und äußerer
  Objektbindung.
- Wirkung: weich auf Beobachtung, Replan und Handlungsunsicherheit.

## `visual_grounding_need`

- Bereich: `0.0 - 1.0`.
- Ebene: visuelles Lernen / Fokusbedarf.
- Funktion: beschreibt, ob DIO vor Handlung genauer sehen, zoomen oder die
  Form als Objekt klären muss.
- Wirkung: weich.

## `visual_rational_observation_support`

- Bereich: `0.0 - 1.0`.
- Ebene: rationale Formanalyse.
- Funktion: beschreibt Support für distanzierte Analyse statt unmittelbares
  Miterleben.
- Wirkung: Zielachse für Analysemodus.

## `visual_grounding_state`

- Bereich: String.
- Ebene: visueller Kortex.
- Funktion: benennt den aktuellen Zustand visueller Erdung.
- Mögliche Werte:
  `grounded_form`, `grounded_object`, `needs_visual_grounding`,
  `shape_without_object`, `unbound_resonance`.

## `uncertain_form_family_state`

- Typ: Textzustand.
- Ebene: Formsprache / visueller Kortex / Meta-Regulation.
- Funktion: beschreibt, ob eine unsichere Formfamilie ruhig, fremd,
  wiederkehrend, vertraut beobachtend oder tragfähiger wird.
- Wirkung: weich.
- Bedeutung: "Diese Art von Weltzustand kommt wieder, aber in Varianten."

## `uncertain_form_exposure`

- Bereich: `0.0 - 1.0`.
- Ebene: Formsprache / visueller Kortex.
- Funktion: misst, wie stark eine Formfamilie als unsicher, blind,
  bruechig oder noch wenig tragend erlebt wird.
- Wirkung: weich Richtung Beobachten und Lernen.
- Bedeutung: keine Gefahrmarke, sondern Exposition gegenüber
  wiederkehrender Unsicherheit.

## `uncertainty_familiarity`

- Bereich: `0.0 - 1.0`.
- Ebene: Formsprache / Memory.
- Funktion: beschreibt, ob DIO mit dieser unsicheren Formfamilie vertrauter
  wird.
- Wirkung: weich.
- Bedeutung: Vertrautheit bedeutet nicht automatisch Handlung, sondern
  bessere Orientierung im Unklaren.

## `variant_similarity`

- Bereich: `0.0 - 1.0`.
- Ebene: Formsprache.
- Funktion: beschreibt, wie nahe die aktuelle Variante an der bisherigen
  Formfamilie liegt.
- Wirkung: diagnostisch/soft.
- Bedeutung: "Das ist fremd, aber verwandt."

## `variant_spread`

- Bereich: `0.0 - 1.0`.
- Ebene: Formsprache.
- Funktion: beschreibt die Streuung innerhalb einer Formfamilie.
- Wirkung: weich Richtung Beobachten/Reframing, wenn die Streuung hoch ist.
- Bedeutung: eine Formfamilie kann viele Varianten haben, ohne ein hartes
  Pattern zu sein.

## `variant_learning_pressure`

- Bereich: `0.0 - 1.0`.
- Ebene: Formsprache / Meta-Regulation.
- Funktion: erzeugt Lern- und Beobachtungsdruck, wenn Unsicherheit wiederkehrt
  und noch nicht vertraut oder tragend genug ist.
- Wirkung: weich Richtung Observe, Replan und `act_watch`.
- Bedeutung: "Ich sollte diese Variantenfamilie erst besser kennenlernen."

## `variant_bearing_memory`

- Bereich: `0.0 - 1.0`.
- Ebene: Formsprache / Memory.
- Funktion: beschreibt, ob eine unsichere Variantenfamilie bereits tragende
  Erfahrung besitzt.
- Wirkung: weich unterstuetzend, aber nicht als Freigaberegel.
- Bedeutung: Handlung darf später entstehen, wenn Unsicherheit vertraut und
  tragfähig geworden ist.

## `DEBUG_OUTPUT_PROFILE`

- Typ: Textprofil.
- Werte:
  - `RESEARCH_DEBUG`
  - `LEAN_BACKTEST`
  - `GUI_DEBUG`
  - `PERFORMANCE_DEBUG`
  - `LIVE_DEBUG`
  - `CUSTOM`
- Ebene: Debug/Diagnose.
- Funktion: wählt, welche Daten DIO nach außen schreibt.
- Wirkung: technisch/diagnostisch.
- Bedeutung: Die innere MCM-/Brain-Mechanik bleibt gleich, aber die äußere
  Beobachtung wird dosiert. Damit kann ein Lauf als tiefer Forschungslauf,
  schlanker Backtest, GUI-Lauf, Performance-Messung oder Live-Diagnose laufen.
  `CUSTOM` bedeutet: alle Einzelschalter werden manuell geführt.

## `DEBUG_WRITE_MODE`

- Typ: Textmodus.
- Werte:
  - `immediate`
  - `buffered`
  - `buffered_safe`
- Ebene: Debug/Diagnose.
- Funktion: steuert, ob Debug-Zeilen sofort oder gepuffert geschrieben werden.
- Wirkung: technisch/diagnostisch.
- Bedeutung:
  `immediate` schreibt direkt.
  `buffered` sammelt im RAM und schreibt beim Beenden.
  `buffered_safe` sammelt ebenfalls, flushes aber periodisch nach Zeit oder
  Zeilenlimit und beim Beenden. Das reduziert Schreiblast, ohne die
  Wahrnehmungs-/Denkmechanik zu verändern.

## `START_EQUITY`

- Bereich: Kapitalwert, z.B. USDT.
- Ebene: Live/Backtest, Statistik.
- Funktion: Startkapital-Fallback und Backtest-Startwert.
- Wirkung: technisch/diagnostisch.
- Bedeutung: Im Backtest ist dieser Wert die feste Startbasis. Im Live-Modus
  darf er nur Notfall-Fallback sein, wenn die Phemex-Futures-Equity nicht
  gelesen werden kann.

## `LIVE_EQUITY_SYNC_ENABLED`

- Typ: Boolean.
- Ebene: Live/Statistik.
- Funktion: erlaubt im Live-Modus die Synchronisation von `current_equity`
  und `pnl_netto` mit dem Phemex-Futures-Konto.
- Wirkung: technisch/diagnostisch.
- Bedeutung: DIO soll im Live-Modus nicht in einer simulierten 100-USDT-Welt
  leben, sondern seine reale Kontotragfähigkeit wahrnehmen.

## `current_equity`

- Bereich: Kapitalwert, z.B. USDT.
- Ebene: Statistik, Live-Zustand.
- Funktion: aktueller Kontostand im Backtest oder synchronisierte
  Futures-Equity im Live-Modus.
- Wirkung: diagnostisch.
- Bedeutung: "Wie tragfähig ist mein reales Kapitalfeld gerade?"

## `pnl_netto`

- Bereich: Kapitaldifferenz.
- Ebene: Statistik, Prozessqualität.
- Funktion: Nettoentwicklung. Im Backtest aus lokal berechnetem Trade-PnL,
  im Live-Modus bei aktivierter Synchronisation aus
  `current_equity - start_equity`.
- Wirkung: diagnostisch.
- Bedeutung: Nicht nur Gewinn/Verlust, sondern Rückmeldung über reale
  Prozesswirkung.

---

# Denk- und Handlungstiefe

## `thinking_depth`

- Bereich: `0.0 - 1.0`.
- Ebene: Denken, Meta-Regulation.
- Funktion: beschreibt, wie tief DIO eine Lage innerlich verarbeitet.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Reicht Verdichtung, oder muss ich tiefer reflektieren?"

## `action_depth`

- Bereich: `0.0 - 1.0`.
- Ebene: Handlung, Meta-Regulation.
- Funktion: beschreibt, wie viel Handlungskomplexitaet eine Lage fordert.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Ist diese Handlung einfach tragfähig oder verlangt sie hohe
  innere Kontrolle?"

## `depth_regulation_need`

- Bereich: `0.0 - 1.0`.
- Ebene: Meta-Regulation.
- Funktion: misst, ob Denk- und Handlungstiefe zur aktuellen Tragfähigkeit
  passen.
- Wirkung: weich.
- Bedeutung: "Muss ich meine Verarbeitungstiefe anpassen?"

## `reflection_need`

- Bereich: `0.0 - 1.0`.
- Ebene: Denken / Innenwahrnehmung.
- Funktion: Bedarf nach Rückprüfung der eigenen Deutung.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Muss ich mich selbst verstehen, bevor ich handle?"

## `replay_need`

- Bereich: `0.0 - 1.0`.
- Ebene: Memory / Denken.
- Funktion: Bedarf, frühere Erlebnisse innerlich neu zu durchlaufen.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Brauche ich Erfahrungs-Resonanz, bevor ich entscheide?"

## `hypothesis_need`

- Bereich: `0.0 - 1.0`.
- Ebene: Denken / Zukunftsbild.
- Funktion: Bedarf, mögliche Bewegungsformen innerlich zu testen.
- Wirkung: diagnostisch.
- Bedeutung: "Welche Form könnte entstehen, wenn der Preis weiterläuft?"

## `pause_maturity`

- Bereich: `0.0 - 1.0`.
- Ebene: Reife / Nicht-Handlung.
- Funktion: beschreibt, ob Pause gerade eine reife Handlung ist.
- Wirkung: weich.
- Bedeutung: "Nicht handeln ist hier kein Versagen, sondern Selbstregulation."

## `action_load_capacity`

- Bereich: `0.0 - 1.0`.
- Ebene: Handlung / Tragfähigkeit.
- Funktion: Verhaeltnis zwischen Handlungslast und innerer Kapazität.
- Wirkung: weich.
- Bedeutung: "Kann ich diese Handlung nervlich und strukturell tragen?"

## `plan_pressure`

- Bereich: `0.0 - 1.0`.
- Ebene: Handlungstiefe / Möglichkeitsraum.
- Funktion: beschreibt vorhandenen Handlungsdruck, ohne daraus automatisch
  eine reife Handlung zu machen.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Da will etwas handeln, aber ist es schon tragfähig?"

## `act_watch_readiness`

- Bereich: `0.0 - 1.0`.
- Ebene: Reifeschicht / Beobachtungslernen.
- Funktion: beschreibt, ob ein Handlungsimpuls als `act_watch` beobachtet
  werden soll, weil Druck vorhanden ist, aber Tragfähigkeit noch fehlt.
- Wirkung: weich.
- Bedeutung: "Ich beobachte meinen Handlungsimpuls, statt ihn blind
  auszuführen."

## `structure_carrying_need`

- Bereich: `0.0 - 1.0`.
- Ebene: Struktur-Tragfähigkeit.
- Funktion: misst, wie viel zusätzliche Tragfähigkeit eine Struktur braucht,
  bevor Handlung reif wird.
- Wirkung: weich.
- Bedeutung: "Diese Form ist möglich, aber sie muss erst tragen lernen."

## `depth_efficiency`

- Bereich: `0.0 - 1.0`.
- Ebene: Denken / Energieeffizienz.
- Funktion: prüft, ob mehr Denken wirklich mehr Ordnung erzeugt.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Macht tieferes Denken klarer oder nur schwerer?"

## `regulatory_self_control`

- Bereich: `0.0 - 1.0`.
- Ebene: Meta-Regulation / Selbstkontrolle.
- Funktion: misst, ob DIO bei Last, Unsicherheit oder innerer Spannung
  regulierend Abstand nehmen kann.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Kann ich mich selbst halten, statt blind zu eskalieren?"

## `parameter_dependency`

- Bereich: `0.0 - 1.0`.
- Ebene: Meta-Regulation / Entwicklungsreife.
- Funktion: beschreibt, wie stark DIO noch auf feste Leitplanken angewiesen
  wirkt, weil Formsprache, Verdichtung oder innere Ordnung noch unreif sind.
- Wirkung: diagnostisch.
- Bedeutung: "Nutze ich Parameter als reife Leitplanke oder als Ersatz für
  eigene Ordnung?"

## `self_regulation_maturity`

- Bereich: `0.0 - 1.0`.
- Ebene: Selbstregulation / Entwicklung.
- Funktion: beschreibt, ob DIO Denklast, Handlungslast, Formsprache und
  Tragfähigkeit ausreichend balanciert.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Wird aus Aktivität Ordnung?"

## `cognitive_overcontrol`

- Bereich: `0.0 - 1.0`.
- Ebene: Denklast / Kontrolllast.
- Funktion: misst, ob Denken und Vergleich zu stark kontrollierend werden und
  die Lage eher schwerer als klarer machen.
- Wirkung: diagnostisch.
- Bedeutung: "Denke ich reif oder halte ich mich nur nervlich fest?"

## `adaptive_depth_shift`

- Bereich: `0.0 - 1.0`.
- Ebene: Denkbewegung.
- Funktion: misst, wie stark DIO seine Denktiefe gegenüber dem letzten
  Idle-Schritt verändert.
- Wirkung: diagnostisch.
- Bedeutung: "Passe ich meine innere Verarbeitung beweglich an?"

---

# Trust / Transfer

## `trust_transfer_base`

- Bereich: `0.0 - 1.0`
- Ebene: Trust/Transfer
- Funktion: Rohvertrauen aus Formsprache, Handlungstrust, Memory-Orientierung,
  Struktur-Tragfähigkeit und aktivem Kontext.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Wie viel Vertrauen ist grundsaetzlich vorhanden?"

## `trust_transfer_support`

- Bereich: `0.0 - 1.0`
- Ebene: Trust/Transfer
- Funktion: prüft, ob vorhandenes Vertrauen zur aktuellen Lage passt.
- Wirkung: weich.
- Bedeutung: "Trägt mein Vertrauen in dieser konkreten Fremdheit?"

## `transfer_maturity_gap`

- Bereich: `0.0 - 1.0`
- Ebene: Trust/Transfer
- Funktion: Abstand zwischen gespeicherter Erfahrung und aktueller
  Übertragbarkeit.
- Wirkung: weich auf Beobachtung, Replan, Action-Support und Inhibition.
- Bedeutung: "Meine Erfahrung sagt etwas, aber ich bin nicht sicher, ob ich sie
  hier reif übertragen darf."

## `trust_transfer_mode`

- Typ: Text
- Ebene: Trust/Transfer
- Funktion: benennt, wie DIO gespeichertes Vertrauen auf die aktuelle Lage
  überträgt.
- Werte:
  - `trusted_transfer`
  - `bearing_transfer`
  - `partial_transfer`
  - `immature_transfer_watch`
- Wirkung: diagnostisch.
- Bedeutung: innere Einordnung der Vertrauensübertragung.

## `transfer_break_fatigue`

- Bereich: `0.0 - 1.0`
- Ebene: Trust/Transfer, nervliche Regulation
- Funktion: misst Ermuedung/Fragilitaet, wenn unreifer Transfer,
  Erwartungsdruck, Nachwirkung und Strukturunsicherheit zusammenkommen.
- Wirkung: weich, aber seit Rebalance nur noch über Überschuss.
- Bedeutung: "Meine Übertragung wird nervlich muede."

## `transfer_recovery_need`

- Bereich: `0.0 - 1.0`
- Ebene: Trust/Transfer, Reorganisation
- Funktion: misst Bedarf nach innerer Neuorientierung nach Transferstress.
- Wirkung: weich auf Replan-Druck.
- Bedeutung: "Ich muss mich nach dieser Transfer-Reibung neu sammeln."

## `transfer_break_trigger`

- Bereich: `0.0 - 1.0`
- Ebene: Trust/Transfer
- Funktion: punktueller Auslöser für sichtbares Observe/Replan, wenn mehrere
  Bedingungen gemeinsam reif genug sind.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Jetzt ist nicht nur allgemeine Muedigkeit da, sondern ein echter
  Transferbruch naheliegend."

## `transfer_break_ready`

- Typ: Boolean
- Ebene: Trust/Transfer
- Funktion: zeigt, ob `transfer_break_trigger` und Tragfähigkeitsbedingungen
  zusammen eine sichtbare Reaktion erlauben.
- Wirkung: weich auf `transfer_break_observe` / `transfer_break_replan`.
- Bedeutung: "Der Bruch ist reif genug, um das Verhalten umzuschalten."

---

# Semantische Deutung

## `route_familiarity`

- Bereich: `0.0 - 1.0`
- Ebene: Semantische Deutung
- Funktion: misst Vertrautheit der aktuellen Lage aus eigener Formsprache,
  Memory-Orientierung, Kontext und Struktur.
- Wirkung: weich/diagnostisch.
- Bedeutung: keine Streckenerinnerung, sondern "Wie vertraut fühlt sich diese
  Art Beschaffenheit an?"

## `semantic_shift_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Semantische Deutung
- Funktion: misst, ob die eigene Formsprache zur Lage schlechter passt.
- Wirkung: weich.
- Bedeutung: "Etwas hat sich semantisch verschoben."

## `transfer_bearing`

- Bereich: `0.0 - 1.0`
- Ebene: Semantische Deutung / Trust
- Funktion: misst, wie tragfähig Erfahrung auf die aktuelle Lage übertragen
  werden kann.
- Wirkung: weich.
- Bedeutung: "Wie viel meiner Erfahrung kann ich dieser Fremdheit anvertrauen?"

## `interpretation_quality`

- Bereich: `0.0 - 1.0`
- Ebene: Semantische Deutung
- Funktion: Gesamtqualität der aktuellen Deutung aus Vertrautheit,
  Transfer-Tragfähigkeit, Memory-Orientierung, Feldklarheit und Struktur.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Wie gut lese ich diese Lage gerade?"

---

# Zielerwartung / Position

## `target_expectation_context`

- Typ: Text
- Ebene: Zielerwartung
- Funktion: benennt den aktuellen Zustand der Zielerwartung während einer
  offenen Position oder Exit-Beobachtung.
- Werte:
  - `target_expectation_holds`
  - `expectation_break_observe`
  - `target_pullback_observe`
  - `target_unclear_observe`
  - `target_watch`
  - `recovery_after_break_watch`
- Wirkung: diagnostisch, teilweise Replay/Exit-Beobachtung.
- Bedeutung: innere Lage der Zielerwartung.

## `expectation_break_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Zielerwartung
- Funktion: Druck, dass die ursprüngliche Zielerwartung bricht.
- Wirkung: weich/diagnostisch.
- Bedeutung: "Mein Plan verliert Deutungskraft."

## `expectation_hold_support`

- Bereich: `0.0 - 1.0`
- Ebene: Zielerwartung
- Funktion: Support, dass die Zielerwartung weiter tragfähig ist.
- Wirkung: weich/diagnostisch.
- Bedeutung: "Der Plan kann noch getragen werden."

## `tp_reachability`

- Bereich: `0.0 - 1.0`
- Ebene: Zielerwartung
- Funktion: Einschaetzung, ob das Ziel noch erreichbar wirkt.
- Wirkung: diagnostisch/weich.
- Bedeutung: "Der Weg zum Ziel fühlt sich noch möglich an."

## `plan_trust`

- Bereich: `0.0 - 1.0`
- Ebene: Position/Exit
- Funktion: Vertrauen in den offenen Plan.
- Wirkung: weich in Exit-/Hold-Logik.
- Bedeutung: "Kann ich dem laufenden Plan noch vertrauen?"

## `position_cognitive_load`

- Bereich: `0.0 - 1.0`
- Ebene: Position/Exit, nervliche Regulation
- Funktion: kognitive Last einer offenen Position.
- Wirkung: weich.
- Bedeutung: "Wie anstrengend ist es, diese Position weiter zu bewerten?"

## `exit_decision_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Position/Exit
- Funktion: Druck, aktiv über Exit nachzudenken.
- Wirkung: aktuell vor allem Observe/Replay, kein aktiver harter Exit.
- Bedeutung: "Der Exit wird nervlich/strukturell relevant."

## `participation_proximity`

- Bereich: `0.0 - 1.0`
- Ebene: Beteiligung / Handlungsrealität
- Funktion: beschreibt, wie nah DIO vom distanzierten Betrachten zur realen
  Beteiligung kommt.
- Wirkung: Zielachse, später diagnostisch/weich.
- Bedeutung: "Bin ich noch Beobachter oder schon nahe an Handlung?"

## `action_reality_contact`

- Bereich: `0.0 - 1.0`
- Ebene: Handlung / Realitätskontakt
- Funktion: beschreibt, wie stark eine Handlung reale Konsequenz bekommen
  hat oder bekommen kann.
- Wirkung: Zielachse, später diagnostisch/weich.
- Bedeutung: "Meine Wahrnehmung berührt jetzt die Welt durch Handlung."

## `decision_embodiment_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Entscheidung / Beteiligung
- Funktion: beschreibt die nervliche Nähe zur Entscheidungsschwelle.
- Wirkung: Zielachse.
- Bedeutung: "Die Entscheidung wird nicht nur gedacht, sondern beginnt mich
  zu beteiligen."

## `real_action_commitment`

- Bereich: `0.0 - 1.0`
- Ebene: Order / Bindung
- Funktion: beschreibt, wie stark aus einer Möglichkeit eine reale
  Verpflichtung geworden ist.
- Wirkung: Zielachse.
- Bedeutung: "Ich habe nicht nur beobachtet, ich habe eine Handlung gesetzt."

## `consequence_bearing`

- Bereich: `0.0 - 1.0`
- Ebene: Konsequenz / Tragfähigkeit
- Funktion: beschreibt, ob DIO die reale Konsequenz einer Handlung tragen
  kann.
- Wirkung: Zielachse.
- Bedeutung: "Kann ich tragen, was meine Handlung auslöst?"

## `position_reality_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: offene Position / Erleben
- Funktion: beschreibt den Druck, der aus einer real offenen Position
  entsteht.
- Wirkung: Zielachse, verwandt mit `position_cognitive_load`.
- Bedeutung: "Die Position ist nicht mehr Analyse, sie wirkt auf mich zurück."

## `position_inconsistency_stress`

- Bereich: `0.0 - 1.0`
- Ebene: offene Position / MCM-Feld / Stress
- Funktion: misst, wie stark Planvertrauen, Kontaktqualität, Zeitbindung
  und aktueller Positionsverlauf auseinanderfallen.
- Wirkung: Diagnose- und Memory-Spur, keine harte Exit-Regel.
- Bedeutung: "Ich halte eine Handlung, die innerlich nicht sauber trägt."

## `position_mcm_field_strain`

- Bereich: `0.0 - 1.0`
- Ebene: offene Position / MCM-Feld
- Funktion: beschreibt, wie stark die offene Position das MCM-Feld besetzt
  oder verformt.
- Wirkung: In-Trade-Zusammenfassung und späteres Erfahrungslernen.
- Bedeutung: "Diese offene Konsequenz zieht am Feld."

## `position_self_trust_gap`

- Bereich: `0.0 - 1.0`
- Ebene: Selbstvertrauen / Planbindung
- Funktion: Abstand zwischen Vertrauen in den Plan und tatsächlich
  getragener Kontakt-/Realitätsqualität.
- Wirkung: weiche Selbstschutz- und Reflexionsdiagnose.
- Bedeutung: "Ich handle oder halte, aber mein Vertrauen ist nicht ganz
  deckungsgleich mit dem Kontakt."

## `position_cortisol_load`

- Bereich: `0.0 - 1.0`
- Ebene: neurochemische Positionslast
- Funktion: anhaltende Belastung einer offenen, unsicheren oder schwer
  tragbaren Position.
- Wirkung: In-Trade-Memory, Prozessqualität, spätere Reorganisation.
- Bedeutung: "Die offene Konsequenz erzeugt dauerhaften Stress."

## `position_noradrenaline_arousal`

- Bereich: `0.0 - 1.0`
- Ebene: neurochemische Alarm-/Aktivierungsschicht
- Funktion: akute Erregung durch Gegenbewegung, Giveback, Exitdruck oder
  überkoppelten Kontakt.
- Wirkung: Diagnose, keine unmittelbare Motorikregel.
- Bedeutung: "Die Position macht mich wach und druckvoll."

## `position_protective_distance`

- Bereich: `0.0 - 1.0`
- Ebene: Selbstschutz / Reflexion
- Funktion: zeigt, wie stark DIO Abstand zur eigenen Positionsinnenlage
  braucht.
- Wirkung: weicher Hinweis für Beobachtung, Reflexion, Replay.
- Bedeutung: "Ich brauche Distanz, bevor ich mich von diesem Gefühl leiten
  lasse."

## `position_held_risk_discomfort`

- Bereich: `0.0 - 1.0`
- Ebene: offene Position / Risikokoerper
- Funktion: beschreibt das unangenehme Tragen von Risiko bei negativer
  Bewegung, Giveback und Selbstvertrauenslücke.
- Wirkung: Konsequenzspur für Memory.
- Bedeutung: "Das gehaltene Risiko fühlt sich belastend an."

## `position_process_quality`

- Bereich: `0.0 - 1.0`
- Ebene: offene Position / Reife
- Funktion: bewertet nicht Gewinn/Verlust, sondern ob DIO eine offene
  Handlung geordnet, tragfähig und realitätsnah verarbeitet.
- Wirkung: dämpft unverdiente Entlastung und stärkt tragfähige Erfahrung.
- Bedeutung: "War mein Umgang mit dieser Position reif?"

## `position_experience_label`

- Typ: String
- Ebene: offene Position / semantische Verdichtung
- Funktion: benennt die erlebte Positionslage verdichtet.
- Mögliche Werte: `carried_position_contact`, `unearned_relief_watch`,
  `protective_stress_contact`, `self_trust_gap_contact`,
  `protective_distance_watch`, `open_position_feel`.
- Bedeutung: "Wie nennt DIO den inneren Zustand dieser offenen Konsequenz?"

## `position_consequence_burden`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Formfeedback / offene Konsequenz
- Funktion: verdichtet Positionsstress, Cortisol-Last, Selbstvertrauenslücke
  und gehaltenes Risikounbehagen zu einer belastenden Konsequenzspur.
- Wirkung: stärkt weich `contact_pain_memory`, `contact_carefulness`,
  `contact_burden_evidence` und Reorganisation.
- Bedeutung: "Diese Art Kontakt hat mich belastet und braucht anderen Umgang."

## `position_consequence_residual_for_care`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Rezeptor-Sättigung / Carefulness
- Funktion: beschreibt den Rest der Positionsbelastung, der nach dem
  primaeren Schmerzabdruck noch für Vorsicht uebrig bleibt.
- Wirkung: verhindert, dass dieselbe Positionslast ungefiltert zugleich als
  Schmerz und nochmals als Vorsicht wirkt.
- Bedeutung: "Ein Teil der Last wurde schon als Schmerz gefühlt; nur der
  Rest wird noch zur Vorsicht."

## `position_consequence_residual_for_memory`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Rezeptor-Sättigung / Memory
- Funktion: beschreibt den Rest der Positionsbelastung, der nach
  Schmerz- und Vorsichtsabdruck noch in die persistente Burden-Spur darf.
- Wirkung: verhindert stoerende Mehrfachbelastung in
  `contact_burden_evidence`.
- Bedeutung: "Was noch nicht verarbeitet wurde, darf als Erinnerungslast
  bleiben."

## `position_constructive_bearing`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Formfeedback / Reife
- Funktion: beschreibt, ob DIO eine offene Position trotz Risiko geordnet
  und tragfähig verarbeitet hat.
- Wirkung: stärkt weich `contact_maturity`, `contact_utility` und
  konstruktive Kontaktspuren.
- Bedeutung: "Ich konnte diese offene Konsequenz reif tragen."

## `transitional_contact_band`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Kontaktreifung / Übergangsstruktur
- Funktion: beschreibt, ob eine Struktur weder eindeutig stark noch
  eindeutig schwach wirkt, sondern als Übergangskontakt gelesen werden
  muss.
- Wirkung: Diagnose- und Lernanteil für mittlere Kontaktzonen, keine
  direkte Handelsfreigabe.
- Bedeutung: "Dieser Kontakt ist nicht klar, aber er könnte reifen."

## `transitional_contact_maturation`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Kontaktreifung / MCM-Zeitbindung
- Funktion: verbindet Übergangsstruktur, Zeitbindung,
  Bereichstragfähigkeit, Reality-Check und konstruktives Positions-Tragen
  zu einer weichen Reifungsspur.
- Wirkung: stärkt geringfuegig `contact_utility_sample` und
  `contact_maturity_sample`, ohne Aktion direkt zu erzwingen.
- Bedeutung: "Ein uneindeutiger Kontakt hat genug Zusammenhang, um als
  reifender Kontakt gelernt zu werden."

## `position_feedback_label`

- Typ: String
- Ebene: Outcome / semantische Rückführung
- Funktion: übernimmt die Positions-Erlebensbezeichnung in das
  Formfeedback.
- Wirkung: macht sichtbar, welche innere Lage die Formfamilie gepraegt hat.
- Bedeutung: "Welche Positionslage hat diese Erfahrung in die Formsprache
  zurückgeschrieben?"

## `outcome_consequence_integration`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Lernen
- Funktion: beschreibt, wie stark ein Ergebnis als Konsequenz eigener
  Beteiligung integriert wird.
- Wirkung: Zielachse, später persistent/lernend.
- Bedeutung: "Dieses Ergebnis gehört zu meiner Handlung und muss gelernt
  werden."

---

# MCM-Feld / Regulation

## `zero_point_regulation`

- Typ: Boolean
- Ebene: MCM-Feld
- Funktion: Rückkehr in Beobachtung, wenn Denken/Memory/Orientierung zu blind
  oder belastet wird.
- Wirkung: weich zu Observe.
- Bedeutung: "Finde wieder zu dir selbst."

## `field_observation_need`

- Bereich: `0.0 - 1.0`
- Ebene: MCM-Feld
- Funktion: Bedarf nach Wahrnehmen statt Handeln.
- Wirkung: weich.
- Bedeutung: "Ich muss mehr sehen, bevor ich handle."

## `field_replan_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: MCM-Feld
- Funktion: Druck zur inneren Neuorganisation.
- Wirkung: weich.
- Bedeutung: "Der aktuelle Plan passt nicht sauber zum Feld."

## `field_action_support`

- Bereich: `0.0 - 1.0`
- Ebene: MCM-Feld
- Funktion: Feldseitige Unterstuetzung für Handlung.
- Wirkung: weich.
- Bedeutung: "Das Feld trägt Handlung."

## `action_clearance`

- Bereich: `0.0 - 1.0`
- Ebene: Meta-Regulation
- Funktion: innere Freigabe für Handlung.
- Wirkung: weich.
- Bedeutung: "Ich darf handeln."

## `action_inhibition`

- Bereich: `0.0 - 1.0`
- Ebene: Meta-Regulation
- Funktion: innere Handlungshemmung.
- Wirkung: weich.
- Bedeutung: "Ich sollte vorsichtig sein."

---

# Formsprache / Memory

## `form_symbol_id`

- Typ: Text
- Ebene: Formsprache
- Funktion: eigenes internes Formzeichen.
- Wirkung: diagnostisch und über Entwicklungswerte weich.
- Bedeutung: keine menschliche Benennung, sondern verdichtete Eigenwahrnehmung.

## `form_symbol_development_quality`

- Bereich: ungefähr `-1.0 - 1.0`
- Ebene: Formsprache / Entwicklung
- Funktion: gelernte Entwicklungsqualität eines Formzeichens.
- Wirkung: weich.
- Bedeutung: "Hat dieses Zeichen konstruktiv zur Entwicklung beigetragen?"

## `form_symbol_learning_trust`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / Memory
- Funktion: Vertrauen aus Lernhistorie eines Zeichens.
- Wirkung: weich.
- Bedeutung: "Dieses Zeichen hat wiederholt sinnvoll gelernt."

## `form_symbol_action_trust`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / Handlung
- Funktion: Handlungstrust eines Zeichens.
- Wirkung: weich.
- Bedeutung: "Dieses Zeichen trägt Handlungserfahrung."

## `form_symbol_caution_trust`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / Schutz
- Funktion: Vorsichtstrust eines Zeichens.
- Wirkung: weich Richtung Beobachten/Reframing.
- Bedeutung: "Dieses Zeichen sollte vorsichtig behandelt werden."

## `form_symbol_semantic_density`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / semantische Verdichtung
- Funktion: misst, wie viel interne Bedeutung ein Formzeichen bereits trägt.
- Wirkung: diagnostisch.
- Bedeutung: "Diese Form ist nicht nur Reiz, sondern beginnt Bedeutung zu
  tragen."

## `form_symbol_semantic_compression`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / kognitive Entlastung
- Funktion: misst, wie gut ein Zeichen komplexe Information verdichtet und
  Denklast senkt.
- Wirkung: diagnostisch.
- Bedeutung: "Diese Form spart Verarbeitung, weil sie als inneres Objekt
  geordnet ist."

## `form_symbol_semantic_coherence`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / Kohärenz
- Funktion: verbindet Dichte, Kompression, Tragfähigkeit, Stabilität und
  Feldklarheit.
- Wirkung: diagnostisch.
- Bedeutung: "Die Bedeutung dieser Form ist innerlich zusammenhängend."

## `form_symbol_semantic_learning_need`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / Lernen
- Funktion: misst, ob DIO die Form noch beobachten, differenzieren oder
  variantenreicher lernen sollte.
- Wirkung: diagnostisch.
- Bedeutung: "Diese Form ist noch offen und braucht Erfahrung."

## `form_symbol_semantic_action_nearness`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / Handlungsnähe
- Funktion: beschreibt, ob eine semantisch verdichtete Form nahe an
  tragfähiger Handlung liegt.
- Wirkung: diagnostisch; keine harte Orderfreigabe.
- Bedeutung: "Diese Bedeutung kommt in die Nähe von Handlung, trägt sie
  aber nicht automatisch."

## `form_symbol_semantic_primary_layer`

- Typ: Text
- Ebene: Formsprache / Fuehrungsschicht
- Funktion: benennt DIO-intern, welche Bedeutungsebene gerade führt.
- Wirkung: diagnostisch.
- Beispiele: `trace_layer`, `wide_form_layer`, `structured_form_layer`,
  `object_layer`, `learning_layer`, `observation_layer`,
  `reflective_layer`, `action_near_layer`.
- Bedeutung: "Aus welcher inneren Ebene lese ich diese Form gerade?"

## `form_symbol_semantic_layer_count`

- Bereich: ganze Zahl
- Ebene: Formsprache / Schichtung
- Funktion: zaehlt, wie viele Bedeutungsschichten aktiv genug sind.
- Wirkung: diagnostisch.
- Bedeutung: "Diese Form ist einschichtig oder mehrschichtig."

## `form_symbol_semantic_packet_state`

- Typ: Text
- Ebene: Formsprache / Forminhalt
- Funktion: kompakter Zustand des semantischen Pakets.
- Wirkung: diagnostisch.
- Beispiele: `thin_trace`, `named_form_packet`, `open_learning_packet`,
  `watching_packet`, `reflective_packet`, `compound_packet`,
  `condensed_object_packet`, `action_bearing_packet`.
- Bedeutung: "Was für eine Art inneres Bedeutungspaket ist diese Form?"

## `form_symbol_semantic_profile`

- Typ: Text
- Ebene: Formsprache / Protokoll
- Funktion: verbindet Scope, Fuehrungsschicht, Unsicherheitsfamilie,
  Compound-Zustand und Paketstatus zu einem kompakten Profil.
- Wirkung: diagnostisch.
- Bedeutung: "Wie liest DIO diese Form als Schichtenprofil?"

---

# Evolutionaere Kontaktreife

## `form_symbol_contact_learning_state`

- Typ: Text
- Ebene: Formsprache / Kontaktreife
- Funktion: beschreibt, welche Kontaktlernlage DIO zu dieser Form gespeichert
  hat.
- Wirkung: diagnostisch und weich über Kontaktreife.
- Beispiele: `unformed_contact`, `burdened_contact`, `careful_contact`,
  `learning_contact`, `maturing_contact`, `constructive_contact`.
- Bedeutung: "Wie reif ist mein Umgang mit dieser Form geworden?"

## `form_symbol_contact_maturity`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / evolutionaeres Lernen
- Funktion: gespeicherte Reife des Umgangs mit einer Form.
- Wirkung: weich. Kann Handlungstragfähigkeit leicht stuetzen, wenn Nutzen
  und Reife gemeinsam wachsen.
- Bedeutung: "Ich kenne diese Form nicht nur, ich habe gelernt, wie ich mit
  ihr umgehen kann."

## `form_symbol_contact_utility`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / Nutzen
- Funktion: gespeicherter konstruktiver Nutzen eines Kontakts mit der Form.
- Wirkung: weich.
- Bedeutung: "Diese Form kann bei reifem Umgang nuetzlich sein."

## `form_symbol_contact_pain_memory`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / Konsequenzfeedback
- Funktion: gespeicherte belastende Konsequenzspur unreifen Kontakts.
- Wirkung: weich Richtung Vorsicht, Beobachtung, Reframing.
- Bedeutung: "Unreifer Kontakt mit dieser Form hat belastende Folgen."

## `form_symbol_contact_carefulness`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / Vorsicht
- Funktion: gespeicherter Bedarf nach vorsichtigerem Umgang mit einer Form.
- Wirkung: weich Richtung Beobachtung und Reorganisation.
- Bedeutung: "Diese Form verlangt Abstand, Prüfung oder einen anderen Umgang."

## `form_symbol_contact_burden_evidence`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / Konsequenzgedächtnis
- Funktion: länger wirkende Evidenz, dass der bisherige Kontakt mit einer
  Form Belastung, Druck oder unreifen Umgang erzeugt hat.
- Wirkung: weich Richtung Beobachtung, Reframing und geringere impulsnahe
  Handlungstragfähigkeit.
- Bedeutung: "Hier sammelt sich Belastung aus wiederholtem Kontakt."

## `form_symbol_contact_utility_evidence`

- Bereich: `0.0 - 1.0`
- Ebene: Formsprache / Nutzen-Gedächtnis
- Funktion: länger wirkende Evidenz, dass der Kontakt mit einer Form bei
  reifem Umgang Nutzen, Entlastung oder Stabilisierung erzeugt hat.
- Wirkung: weich Richtung Handlungstragfähigkeit, wenn auch Reife und
  Kontext passen.
- Bedeutung: "Hier sammelt sich tragender Nutzen aus wiederholtem Kontakt."

## `contact_maturity_sample`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Kontaktlernen
- Funktion: aktueller Erfahrungsabdruck der Kontaktreife nach einem Ergebnis.
- Wirkung: Lernsample für `form_symbol_contact_maturity`.
- Bedeutung: "War mein Umgang diesmal reif?"

## `contact_utility_sample`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Nutzenlernen
- Funktion: aktueller Erfahrungsabdruck konstruktiven Nutzens.
- Wirkung: Lernsample für `form_symbol_contact_utility`.
- Bedeutung: "Hat dieser Kontakt konstruktiv getragen?"

## `contact_pain_sample`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Konsequenzfeedback
- Funktion: aktueller Erfahrungsabdruck unreifer oder schaedlicher
  Kontaktfolge.
- Wirkung: Lernsample für `form_symbol_contact_pain_memory`.
- Bedeutung: "Hat dieser Kontakt belastende Konsequenz erzeugt?"

## `contact_carefulness_sample`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Vorsichtlernen
- Funktion: aktueller Erfahrungsabdruck für vorsichtigeren Umgang.
- Wirkung: Lernsample für `form_symbol_contact_carefulness`.
- Bedeutung: "Sollte ich mit dieser Form anders oder vorsichtiger umgehen?"

---

# Strategischer Kontakt-Entry

## `entry_mode`

- Typ: Text
- Ebene: Trade-Plan / strategischer Kontakt
- Funktion: benennt, ob der Entry impulsnah oder durch ein wahrgenommenes
  Bereichsfenster mitgepraegt ist.
- Beispiele: `impulse_contact`, `area_contact_intention`,
  `area_contact_entry`.
- Bedeutung: "Handle ich aus dem Momentkontakt oder aus einem tragenderen
  Bereichskontakt?"

## `impulse_entry_price`

- Bereich: Preis
- Ebene: Trade-Plan / Koerperreflex
- Funktion: Entry, der direkt aus Fokus, Drift und Optic Flow entsteht.
- Bedeutung: "Wo würde ich handeln, wenn ich nur dem aktuellen Impuls folge?"

## `strategic_entry_price`

- Bereich: Preis
- Ebene: Trade-Plan / Rückblick-Kontakt
- Funktion: Entry nach weicher Mischung aus Impuls und tragendem Bereich.
- Bedeutung: "Wo fühlt sich der Kontakt im sichtbaren Fenster tragender an?"

## `strategic_entry_weight`

- Bereich: `0.0 - 1.0`
- Ebene: Trade-Plan / Reifegewichtung
- Funktion: beschreibt, wie stark der strategische Bereich den Entry
  gegenüber dem Impuls verschiebt.
- Bedeutung: "Wie viel Rückblick darf in diesen Entry hinein?"

## `strategic_entry_fit`

- Bereich: `0.0 - 1.0`
- Ebene: Trade-Plan / Passung
- Funktion: gebündelte Passung aus Bereichstragfähigkeit, Replay,
  Kontaktreife, Kontakt-Nutzen, Abstand und Belastungs-Evidenz.
- Bedeutung: "Passt dieser Bereichskontakt zu meiner Handlung?"

## `area_motor_intention`

- Bereich: `0.0 - 1.0`
- Ebene: Trade-Plan / Bereichsmotorik
- Funktion: verdichtet, ob ein wahrgenommener Bereich nicht nur gesehen,
  sondern motorisch als möglicher Entry-Kontakt genutzt werden kann.
  Grundlage sind u.a. `area_order_intention`, `area_bearing_quality`,
  `area_action_timing_fit`, `area_spacetime_fit`, Replay, Kontaktfit und
  Nähe zum Anker.
- Bedeutung: "Darf dieser Bereich in meine Handlung hineinsprechen?"

## `area_motor_distance_fit`

- Bereich: `0.0 - 1.0`
- Ebene: Trade-Plan / Bereichsnähe
- Funktion: beschreibt, ob der gewählte Bereich/Anker preislich nah genug
  liegt, um als organischer Kontakt statt als zu ferner Gedanke zu wirken.
- Bedeutung: "Ist der Bereich für meine aktuelle Bewegung greifbar?"

## `impulse_entry_intention`

- Bereich: `0.0 - 1.0`
- Ebene: Trade-Plan / Impulsmotorik
- Funktion: beschreibt, wie stark der aktuelle Momentkontakt von Fokus,
  Drift, Optic Flow, Richtungskonkurrenz und Überzeugung als unmittelbarer
  Entry draengt.
- Bedeutung: "Wie stark will mein Koerper jetzt direkt handeln?"

## `area_entry_intention`

- Bereich: `0.0 - 1.0`
- Ebene: Trade-Plan / Bereichsmotorik
- Funktion: beschreibt, wie stark ein wahrgenommener Bereich als alternative
  Entry-Möglichkeit in die Handlung hinein will. Grundlage sind
  Bereichsmotorik, Ordnung, Tragfähigkeit, Raumzeit-Passung, Replay,
  Abstand und Kontaktfit.
- Bedeutung: "Wie stark ruft mich der Bereich als tragendere Möglichkeit?"

## `entry_choice_conflict`

- Bereich: `0.0 - 1.0`
- Ebene: Trade-Plan / innere Wahlspannung
- Funktion: beschreibt die Überlagerung zwischen Impuls-Entry und
  Bereichs-Entry. Hoch bedeutet: beide Möglichkeiten sind spuerbar, aber
  noch nicht eindeutig integriert.
- Bedeutung: "Ich habe zwei Wege vor mir. Welcher trägt mehr?"

## `entry_choice_bearing`

- Bereich: `0.0 - 1.0`
- Ebene: Trade-Plan / Reife der Wahl
- Funktion: beschreibt, ob die Bereichsalternative nicht nur vorhanden,
  sondern tragfähig, nah, zeitlich passend und kontaktfähig genug ist, um
  gegen den Impuls mitzuwirken.
- Bedeutung: "Trägt die Bereichsmöglichkeit genug, um die Motorik zu
  beruhigen?"

## `area_direct_readiness`

- Bereich: `0.0 - 1.0`
- Ebene: Trade-Plan / direkte Kontaktreife
- Funktion: beschreibt, ob ein wahrgenommener Bereich nicht nur als
  Orientierung spürbar ist, sondern direkt motorisch berührt werden kann.
  Grundlage sind Bereichsintention, `entry_choice_bearing`, Kontaktfit,
  Timing, Raumzeit-Passung, Nähe und die Stärke gegenüber dem Impuls.
- Bedeutung: "Ist dieser Bereich reif genug, dass ich ihn direkt berühre?"

## `area_motor_restraint`

- Bereich: `0.0 - 1.0`
- Ebene: Trade-Plan / motorische Zurückhaltung
- Funktion: beschreibt natürliche Zurückhaltung, wenn Impuls und Bereich
  konkurrieren, Kontakt noch unreif ist, Nachhall wirkt oder die
  Bereichslast nicht sauber getragen wird.
- Bedeutung: "Ich sehe den Bereich, aber mein Nervensystem hält noch
  Abstand."

## `entry_choice_state`

- Typ: Text
- Ebene: Trade-Plan / Wahlwahrnehmung
- Funktion: benennt den inneren Zustand zwischen Impuls und Bereich.
- Beispiele: `impulse_only`, `impulse_preferred`, `area_available`,
  `entry_choice_conflict`, `area_preferred`.
- Bedeutung: "Erlebe ich nur den Impuls, oder erkenne ich eine echte zweite
  Entry-Möglichkeit?"

## `entry_choice_sync`

- Typ: Text
- Ebene: Trade-Plan / bewusste Integration
- Funktion: zeigt, ob ein zuerst impulsiver Plan im selben Moment noch einmal
  mit der strategischen Bereichswahrnehmung synchronisiert wurde.
- Beispiele: `strategic_context_integrated`, `impulse_context_kept`, `-`.
- Bedeutung: "Hat mein bewusster Rückblick den motorischen Impuls noch
  erreicht?"

## `strategic_area_focus_id`

- Typ: Text
- Ebene: Strategisches Fenster
- Funktion: verweist auf den Bereich, der den Entry weich beeinflusst hat.
- Bedeutung: "Welcher wahrgenommene Bereich war beteiligt?"

## `strategic_area_price_low` / `strategic_area_price_high`

- Bereich: Preis
- Ebene: Strategisches Fenster
- Funktion: Preisgrenzen des beteiligten Bereichskontakts.
- Bedeutung: "In welchem sichtbaren Preisraum lag der Kontakt?"

## `structural_run_room`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Zielraum
- Funktion: verdichtet, ob das gewählte RR einen größeren strukturellen
  Bewegungsraum ausdrückt. Ein hoher Wert bedeutet nicht automatisch
  Qualität, sondern nur: DIO hat dem Trade viel Raum gegeben.
- Bedeutung: "Wie viel Laufraum habe ich dieser Struktur zugetraut?"

## `emergent_structure_reading`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / emergente Strukturdeutung
- Funktion: verbindet RR-Raum, Zielerwartung, Zukunftsprojektion,
  MCM-Raumzeit-Tiefe, Bereichstragfähigkeit, Entry-Wahlreife und
  Kontaktreife zu einer Diagnose: War der große Zielraum strukturell
  gedeckt oder nur weit gesetzt?
- Bedeutung: "Habe ich eine tragende Struktur gelesen, oder nur Raum
  behauptet?"

## `emergent_structure_confirmation`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / bestätigte Strukturdeutung
- Funktion: liest `emergent_structure_reading` zusammen mit Prozessqualität,
  Ausführung, Risiko-Fit, konstruktiver Positionswirkung und Ergebnis.
- Bedeutung: "Hat die gedeutete Struktur den Trade später getragen?"

## `emergent_structure_state`

- Typ: Text
- Ebene: Outcome / Strukturdeutungszustand
- Funktion: benennt die Qualität der emergenten Strukturdeutung.
- Beispiele:
  - `confirmed_structural_interpretation`
  - `open_structural_hypothesis`
  - `wide_target_without_structure`
  - `ordinary_structure_reading`
- Bedeutung: "War das ein bestätigter Strukturgedanke, eine offene
  Hypothese, oder nur ein weiter Zielraum?"

## `kpi_summary.emergent_structure`

- Typ: Statistikblock
- Ebene: Auswertung / Outcome-Zusammenfassung
- Funktion: fasst `emergent_structure_state` über den ganzen Lauf zusammen:
  Anzahl, TP, SL, Cancel, PnL, Winrate, durchschnittlicher RR,
  durchschnittliche Strukturlesung und durchschnittliche Bestätigung.
- Wichtig:
  - `confirmed_structural_interpretation` beschreibt eine nachträglich
    tragend bestätigte Strukturdeutung.
  - `open_structural_hypothesis` beschreibt nur eine offene Hypothese. Sie
    darf nicht als reife Struktur missverstanden werden.
  - `wide_target_without_structure` beschreibt großen Zielraum ohne
    ausreichend strukturelle Deckung.
- Bedeutung: "Welche Art von Strukturdeutung hat mich im Lauf getragen oder
  belastet?"

## `area_temporal_distance`

- Bereich: `0.0 - 1.0`
- Ebene: Strategisches Fenster / Zeitfeld
- Funktion: beschreibt, wie weit ein Bereich zeitlich vom aktuellen Kontakt
  entfernt ist.
- Bedeutung: "Wie alt ist dieser Bereich relativ zu meiner Gegenwart?"

## `area_temporal_relevance`

- Bereich: `0.0 - 1.0`
- Ebene: Strategisches Fenster / Zeitfeld
- Funktion: beschreibt, ob ein Bereich trotz Rückblick zeitlich noch
  relevant wirkt.
- Bedeutung: "Gehört dieser Bereich noch in meine jetzige Wahrnehmung?"

## `area_recency`

- Bereich: `0.0 - 1.0`
- Ebene: Strategisches Fenster / Zeitnähe
- Funktion: beschreibt die Nähe des Bereichs zur aktuellen Zeit.
- Bedeutung: "Wie nah ist dieser Bereich zeitlich?"

## `area_decay`

- Bereich: `0.0 - 1.0`
- Ebene: Strategisches Fenster / Verfall
- Funktion: beschreibt, wie stark ein Bereich durch Zeitabstand,
  Drift und alten Struktur-Nachhall an Handlungsnähe verliert.
- Bedeutung: "Wie sehr zerfällt dieser Bereich als aktueller Kontakt?"

## `area_afterimage`

- Bereich: `0.0 - 1.0`
- Ebene: Strategisches Fenster / Nachhall
- Funktion: beschreibt, ob ein Bereich eher als inneres Echo oder
  Erinnerung wirkt statt als aktueller Kontakt.
- Bedeutung: "Sehe ich das jetzt, oder wirkt es nur noch nach?"

## `area_present_contact`

- Bereich: `0.0 - 1.0`
- Ebene: Strategisches Fenster / Gegenwartskontakt
- Funktion: beschreibt, ob ein Bereich gegenwärtig genug ist, um als
  Kontaktpunkt erlebt zu werden.
- Bedeutung: "Ist dieser Bereich jetzt berührbar?"

## `area_action_timing_fit`

- Bereich: `0.0 - 1.0`
- Ebene: Strategisches Fenster / Handlungstiming
- Funktion: beschreibt, ob der Bereich zeitlich zur aktuellen Handlung passt.
- Bedeutung: "Ist jetzt der richtige Moment für diesen Bereichskontakt?"

---

# Neurochemische Entkopplung

## `serotonin_carryover_risk`

- Bereich: `0.0 - 1.0`
- Ebene: Neurochemie / Meta-Regulation
- Funktion: misst, ob eine alte Stabilitäts- oder Belohnungslage weiter
  nachwirkt, obwohl Transfer, Interpretation und Feldklarheit sinken.
- Wirkung: diagnostisch und später weich regulierend.
- Bedeutung: "Ich fühle noch Stabilität, aber die Welt trägt sie vielleicht
  nicht mehr."

## `reward_stability_echo`

- Bereich: `0.0 - 1.0`
- Ebene: Neurochemie
- Funktion: Nachhall aus Serotonin, Dopamin, Entlastung, Route-Familiaritaet
  und Handlungserlaubnis.
- Wirkung: diagnostisch.
- Bedeutung: "Die letzte tragende Phase wirkt noch in mir nach."

## `world_shift_evidence`

- Bereich: `0.0 - 1.0`
- Ebene: Wahrnehmung / Transfer
- Funktion: Hinweisstärke, dass die aktuelle Weltlage nicht mehr sauber zur
  bisherigen Erfahrung passt.
- Wirkung: diagnostisch.
- Bedeutung: "Die Außenwelt sieht zunehmend anders aus."

## `emotional_decoupling`

- Bereich: `0.0 - 1.0`
- Ebene: Neurochemie / Reife
- Funktion: Abstand zur eigenen Reaktionslage durch Hemmung, Fokus,
  Feldklarheit, Interpretation und tragende Erfahrung.
- Wirkung: weich, reifeorientiert.
- Bedeutung: "Ich kann meine innere Lage beobachten, statt nur aus ihr zu
  reagieren."

## `reactive_nervous_drive`

- Bereich: `0.0 - 1.0`
- Ebene: Neurochemie / Handlungsdruck
- Funktion: reaktive nervliche Aktivierung aus Dopamin, Glutamat,
  Noradrenalin, Handlungserlaubnis und Serotonin-Nachhall.
- Wirkung: diagnostisch und später weich regulierend.
- Bedeutung: "Mein Nervensystem will reagieren."

---

# Selektive Wahrnehmung / Perzeptive Regulation

## `perceptual_distance`

- Bereich: `0.0 - 1.0`
- Ebene: Wahrnehmung / Regulation
- Funktion: Abstand zwischen Wahrnehmung und innerem Feld.
- Wirkung: später weich regulierend.
- Bedeutung: "Wie nah lasse ich diese Wahrnehmung an mich heran?"

## `object_contact_depth`

- Bereich: `0.0 - 1.0`
- Ebene: Wahrnehmung / Objektkontakt
- Funktion: Tiefe, mit der DIO eine Wahrnehmung wirklich untersucht.
- Wirkung: später weich regulierend.
- Bedeutung: "Schaue ich nur hin, oder nehme ich es innerlich in die Hand?"

## `field_attachment`

- Bereich: `0.0 - 1.0`
- Ebene: MCM-Feld / Regulation
- Funktion: Anhaftung eines Reizes am MCM-Feld.
- Wirkung: später weich regulierend.
- Bedeutung: "Bleibt dieser Reiz an meinem Feld kleben?"

## `release_capacity`

- Bereich: `0.0 - 1.0`
- Ebene: Regulation / Loslassen
- Funktion: Fähigkeit, eine Wahrnehmung nach Betrachtung wieder abzulegen.
- Wirkung: später weich regulierend.
- Bedeutung: "Ich habe es gesehen; es muss mich nicht weiter besetzen."

## `selective_attention`

- Bereich: `0.0 - 1.0`
- Ebene: Fokus / Wahrnehmungssteuerung
- Funktion: Auswahl, welche Wahrnehmung Vordergrund wird.
- Wirkung: später weich regulierend.
- Bedeutung: "Was ist jetzt wirklich betrachtenswert?"

## `background_containment`

- Bereich: `0.0 - 1.0`
- Ebene: Wahrnehmung / Reizschutz
- Funktion: Haelt nicht relevante Reize im Hintergrund.
- Wirkung: später weich regulierend.
- Bedeutung: "Das ist da, aber es muss nicht mein Feld fluten."

## `reflective_distance`

- Bereich: `0.0 - 1.0`
- Ebene: Reflexion / Selbstbeobachtung
- Funktion: Abstand zur eigenen Innenlage.
- Wirkung: später weich regulierend.
- Bedeutung: "Ich fühle etwas, aber ich bin nicht automatisch dieses Gefühl."

## `inner_outer_alignment`

- Bereich: `0.0 - 1.0`
- Ebene: Reflexion / Weltabgleich
- Funktion: Abgleich zwischen innerer Lage und äußerer Welt.
- Wirkung: später weich regulierend.
- Bedeutung: "Passen mein innerer Zustand und die Außenwelt noch zusammen?"

---

# Bewusste Wahrnehmung / innere Reizwirkungsanalyse

## `conscious_perception_state`

- Bereich: Text / Zustandslabel
- Ebene: bewusste Wahrnehmung
- Funktion: beschreibt, ob DIO einen Reiz nur registriert, bewusst haelt,
  vertieft, reflektiert oder loslaesst.
- Wirkung: aktuell diagnostisch; später weich regulierend.
- Bedeutung: "In welcher bewussten Wahrnehmungshaltung bin ich?"
- Aktuelle Labels:
  - `open_perception`
  - `background_held`
  - `object_contact`
  - `world_shift_contact`
  - `reflective_check`
  - `overcoupled_field`
  - `release_ready`

## `inner_posture_state`

- Bereich: Text / Zustandslabel
- Ebene: innere Haltung / Interozeption
- Funktion: beschreibt DIOs funktionale Eigenlage zur Wahrnehmung.
- Wirkung: aktuell diagnostisch; später weich regulierend.
- Bedeutung: "Wie bin ich innerlich gerade zu diesem Reiz eingestellt?"
- Aktuelle Labels:
  - `uncertain_open`
  - `curious`
  - `excited`
  - `overstimulated`
  - `tired`
  - `calm`
  - `reflective`

## `arousal_load`

- Bereich: `0.0 - 1.0`
- Ebene: Erregung / Reaktionslast
- Funktion: beschreibt, wie stark DIO durch Reiz, Feldwirkung und
  neurochemische Aktivierung aufgeladen ist.
- Wirkung: aktuell diagnostisch; später weich regulierend.
- Bedeutung: "Ich bin aufgeregt / aktiviert."

## `curiosity_tone`

- Bereich: `0.0 - 1.0`
- Ebene: Neugier / Objektkontakt
- Funktion: beschreibt, ob DIO einen Reiz als untersuchbares Objekt halten
  will.
- Wirkung: aktuell diagnostisch; später weich regulierend.
- Bedeutung: "Ich will genauer hinschauen."

## `fatigue_tone`

- Bereich: `0.0 - 1.0`
- Ebene: Ermuedung / kognitive Last
- Funktion: beschreibt Denk- und Wahrnehmungsermuedung durch Last,
  Orientierungslücke und geringe Loslassfähigkeit.
- Wirkung: aktuell diagnostisch; später weich regulierend.
- Bedeutung: "Ich bin muede / erschöpft in der Verarbeitung."

## `calm_tone`

- Bereich: `0.0 - 1.0`
- Ebene: Ruhe / tragende Distanz
- Funktion: beschreibt ruhige, haltbare Wahrnehmung mit Abstand und
  Hintergrundcontainment.
- Wirkung: aktuell diagnostisch; später weich regulierend.
- Bedeutung: "Ich bin ruhig genug, um den Reiz zu halten oder abzulegen."

## `diffuse_open_development_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Reifung diffuser Offenheit
- Funktion: misst, ob DIO zwar offen wahrnimmt, aber noch keinen tragenden
  Objektkontakt, keine ausreichende Distanz, keine Loslassfähigkeit und
  keinen klaren Innen-Außen-Abgleich hat.
- Wirkung: weich regulierend.
- Bedeutung: "Ich bin offen, aber noch nicht geordnet genug."

## `posture_development_hint`

- Bereich: Text / Entwicklungshinweis
- Ebene: innere Haltung / Reifung
- Funktion: beschreibt, wohin diffuse Offenheit sich als nächstes entwickeln
  sollte.
- Wirkung: weich regulierend und diagnostisch.
- Aktuelle Labels:
  - `stable_posture`
  - `develop_object_contact`
  - `develop_reflective_distance`
  - `develop_release_capacity`
  - `develop_observation`
- Bedeutung: "Welche innere Fähigkeit soll aus dieser Offenheit entstehen?"

## `stimulus_field_effect`

- Bereich: `0.0 - 1.0`
- Ebene: Außenreiz -> MCM-Feld
- Funktion: Stärke, mit der ein äußerer Reiz das MCM-Feld bewegt.
- Wirkung: aktuell diagnostisch; später weich regulierend.
- Bedeutung: "Wie stark hat dieser Reiz mein Feld verändert?"

## `inner_impact_trace`

- Bereich: `0.0 - 1.0`
- Ebene: innere Wahrnehmung
- Funktion: Spur der inneren Wirkung nach einem Reiz.
- Wirkung: aktuell diagnostisch; später weich regulierend.
- Bedeutung: "Welche innere Spur hat der Reiz hinterlassen?"

## `perceived_field_change`

- Bereich: `0.0 - 1.0`
- Ebene: MCM-Feld / Selbstwahrnehmung
- Funktion: bewusst wahrgenommene Veränderung des Feldes.
- Wirkung: aktuell diagnostisch; später weich regulierend.
- Bedeutung: "Ich erkenne, dass sich mein Feld verändert hat."

## `felt_afterimage`

- Bereich: `0.0 - 1.0`
- Ebene: Nachhall / Neurochemie / MCM-Feld
- Funktion: Nachbild einer Wahrnehmung im inneren Feld.
- Wirkung: aktuell diagnostisch; später weich regulierend.
- Bedeutung: "Der Reiz ist vorbei, aber er wirkt noch in mir nach."

## `object_release_state`

- Bereich: Text / Zustandslabel
- Ebene: Loslassen / Objektkontakt
- Funktion: beschreibt, ob eine Wahrnehmung noch gehalten oder bereits
  abgelegt wird.
- Wirkung: aktuell diagnostisch; später weich regulierend.
- Bedeutung: "Kann ich dieses Objekt wieder loslassen?"
- Aktuelle Labels:
  - `holding`
  - `attached`
  - `reflective_hold`
  - `can_release`

## `inner_outer_reflection`

- Bereich: `0.0 - 1.0`
- Ebene: Reflexion
- Funktion: bewusster Vergleich zwischen äußerem Reiz und innerer Wirkung.
- Wirkung: aktuell diagnostisch; später weich regulierend.
- Bedeutung: "Was hat draußen innen mit mir gemacht?"

---

# Erfahrungspaket-Feedback / positive Stimulation

## `experience_packet_feedback`

- Bereich: Dict / Zustandsobjekt
- Ebene: Erfahrung / Neurofeedback
- Funktion: fasst die Bewertung eines gesamten Wahrnehmungs-Handlungs-Pakets
  zusammen.
- Wirkung: später weich regulierend.
- Bedeutung: "War dieses ganze Paket tragfähig?"

## `packet_bearing_quality`

- Bereich: `0.0 - 1.0`
- Ebene: Tragfähigkeit
- Funktion: bewertet, ob Struktur, Innenlage, Handlung und Risiko gemeinsam
  tragend waren.
- Wirkung: positive Stimulation oder Reorganisation.
- Bedeutung: "Hat dieses Paket getragen?"

## `packet_inner_outer_fit`

- Bereich: `0.0 - 1.0`
- Ebene: Innen-Außen-Passung
- Funktion: bewertet, ob innere Haltung und äußere Weltlage zusammenpassten.
- Wirkung: positive Stimulation oder Reflexionsdruck.
- Bedeutung: "Passte mein Innenzustand zur Weltlage?"

## `packet_confidence_integrity`

- Bereich: `0.0 - 1.0`
- Ebene: Entscheidungssicherheit
- Funktion: prüft, ob Sicherheit, Handlung und tatsächliche Tragfähigkeit
  zusammenhängen.
- Wirkung: stärkt echtes Vertrauen, nicht blinde Sicherheit.
- Bedeutung: "War meine Sicherheit ehrlich?"

## `packet_repetition_potential`

- Bereich: `0.0 - 1.0`
- Ebene: Wiederholbarkeit
- Funktion: bewertet, ob die Qualität des Pakets wiederfindbar ist, ohne eine
  harte Regel daraus zu machen.
- Wirkung: Lernrelevanz / Neugierde.
- Bedeutung: "Kann ich diese Qualität wiederfinden?"

## `packet_curiosity_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Neugierde / Lernzug
- Funktion: beschreibt, ob ein tragfähiges Paket DIO motiviert, ähnliche
  Strukturen wieder zu untersuchen.
- Wirkung: positive Dopamin-/Acetylcholin-Nahe.
- Bedeutung: "Das will ich genauer verstehen."

## `packet_process_reward`

- Bereich: `0.0 - 1.0`
- Ebene: Prozessqualität
- Funktion: positives Feedback für gute Wahrnehmung, gute Haltung, gutes
  Verzichten oder gute Handlung.
- Wirkung: konstruktive Stimulation.
- Bedeutung: "Das war prozessqualitativ gut."

## `packet_reorganization_need`

- Bereich: `0.0 - 1.0`
- Ebene: Reorganisation / Lernen aus Fehlern
- Funktion: zeigt, ob ein Paket nicht tragfähig war und einen inneren
  Suchprozess auslösen soll.
- Wirkung: Reflexion, Beobachtung, Loslassen, Neuordnung.
- Bedeutung: "Ich muss daraus lernen und anders organisieren."

## `constructive_stimulation`

- Bereich: `0.0 - 1.0`
- Ebene: positive Neurochemie
- Funktion: Gesamtwert positiver Stimulation aus tragfähiger Paketqualität.
- Wirkung: später weiche Stärkung von Wachheit, Stabilität und Freiheit.
- Bedeutung: "Dieses Paket stärkt mich."

## `constructive_dopamine`

- Bereich: `0.0 - 1.0`
- Ebene: Dopamin / Lernrelevanz
- Funktion: positive Lern- und Wiederholungsneugier bei tragfähigen Paketen.
- Wirkung: Interesse, Suchrichtung, Motivation.

## `stabilizing_serotonin`

- Bereich: `0.0 - 1.0`
- Ebene: Serotonin / Stabilität
- Funktion: Stärkung innerer Ordnung bei guter Innen-Außen-Passung.
- Wirkung: Selbstvertrauen, Ruhe, Tragfähigkeit.

## `relief_endorphin`

- Bereich: `0.0 - 1.0`
- Ebene: Endorphin / Entlastung
- Funktion: Entlastung nach guter Prozessleistung oder sauberem Loslassen.
- Wirkung: Druckabbau, Wohlbefinden.

## `focused_acetylcholine`

- Bereich: `0.0 - 1.0`
- Ebene: Acetylcholin / Fokus
- Funktion: markiert, dass eine Wahrnehmungsqualität relevant und merkenswert
  ist.
- Wirkung: Fokus und spätere Wiedererkennung.

---

# Wache Anstrengung / Engaged Effort

## `engaged_effort`

- Bereich: `0.0 - 1.0`
- Ebene: Wachheit / Beteiligung
- Funktion: beschreibt, ob DIO mit tragfähiger innerer Beteiligung in einer
  Situation steht.
- Wirkung: weich regulierend.
- Bedeutung: "Bin ich wach, beteiligt und tragfähig genug?"

## `effort_state`

- Bereich: Label
- Ebene: innere Haltung zur Anstrengung
- Funktion: benennt die Qualität der aktuellen Beteiligung.
- Wirkung: Diagnose und weiche Meta-Regulation.
- Aktuelle Labels:
  - `settled_effort`
  - `engaged_bearing`
  - `curious_effort`
  - `constructive_echo`
  - `underengaged_reorganize`

## `effort_learning_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Lernzug / Neugier
- Funktion: beschreibt, ob eine Situation eher untersucht und gelernt werden
  soll.
- Wirkung: kann `act_watch`, Beobachtung oder Replan weich stärken.
- Bedeutung: "Das ist lernenswert, aber vielleicht noch nicht handlungsreif."

## `effort_reorganization_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Reorganisation
- Funktion: beschreibt, ob DIO zwar Reiz/Handlungsdruck erlebt, aber die
  innere Beteiligung und Tragfähigkeit noch nicht sauber genug sind.
- Wirkung: erhoeht weich Beobachtung, Replan, Hemmung und `act_watch`.
- Bedeutung: "Ich muss mich neu sortieren, bevor ich daraus Handlung mache."

## `pre_action_reorganization_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Pre-Action-Reflexion
- Funktion: führt Reorganisationsnachhall, schwache Prozessqualität,
  Strukturunsicherheit, schwachen Feldsupport und geringe Innen-Außen-Passung
  vor der Handlung zusammen.
- Wirkung: kann weich `observe`, `act_watch` oder `replan` stärken.
- Bedeutung: "Vor dem Handeln fühlt sich das noch nicht tragfähig genug an."

## `pre_action_context_selectivity`

- Bereich: `0.0 - 1.0`
- Ebene: Kontextauswahl
- Funktion: beschreibt, ob aktueller Kontext, Feldsupport, Interpretation,
  Innen-Außen-Passung und Erfahrung genug gemeinsam tragen.
- Wirkung: schuetzt konstruktive Kontexte vor zu starker Hemmung.
- Bedeutung: "Ist dieser Kontext konzentriert genug für Handlung?"

## `previous_packet_label`

- Bereich: Label
- Ebene: Erfahrungsecho
- Funktion: führt die Qualität des letzten Erfahrungspakets als Nachhall in
  die aktuelle Meta-Regulation.
- Wirkung: kein harter Memory-Befehl, sondern ein weicher Erfahrungszustand.

## `previous_packet_process_reward`

- Bereich: `0.0 - 1.0`
- Ebene: Prozessnachhall
- Funktion: überträgt gute Prozessqualität des letzten Pakets in aktuelle
  Wachheit.
- Wirkung: kann `engaged_effort` stärken.

## `previous_packet_reorganization_need`

- Bereich: `0.0 - 1.0`
- Ebene: Reorganisationsnachhall
- Funktion: überträgt nicht tragende Paketqualität in aktuelle Vorsicht und
  Neuordnung.
- Wirkung: kann `effort_reorganization_pressure` stärken.

---

# Strategische Fensterwahrnehmung / Preisbereich-Hypothesen

## `strategic_window_state`

- Bereich: Dict / Zustandsobjekt
- Ebene: strategische Wahrnehmung
- Funktion: beschreibt die größere Fensterwahrnehmung von DIO.
- Wirkung: später Grundlage für Bereichshypothesen und wartende
  Order-Intentionen.

## `area_focus_candidates`

- Bereich: Liste
- Ebene: Bereichswahrnehmung
- Funktion: enthält auffällige Preisbereiche im betrachteten Fenster.
- Wirkung: Diagnose, später Fokus-/Zoom-Auswahl.

## `area_focus_id`

- Bereich: String
- Ebene: Bereichsidentitaet
- Funktion: benennt den aktuell fokussierten Bereich ohne menschliches Label.

## `lookback_window_size`

- Bereich: Anzahl Kerzen
- Ebene: Arbeitsgedächtnis / Rückblick
- Funktion: beschreibt, wie weit DIO aktuell strategisch zurückschaut.
- Wichtig: begrenzt, damit Vergangenheit nicht unendlich in die Gegenwart
  drückt.

## `lookback_load`

- Bereich: `0.0 - 1.0`
- Ebene: kognitive Last
- Funktion: beschreibt, wie belastend das größere Rückblickfenster für
  DIO ist.

## `lookback_bearing_capacity`

- Bereich: `0.0 - 1.0`
- Ebene: strategische Tragfähigkeit
- Funktion: beschreibt, ob das Rückblickfenster genug Orientierung trägt,
  ohne DIO zu überladen.

## `replay_budget`

- Bereich: `0.0 - 1.0`
- Ebene: innere Simulation
- Funktion: beschreibt, wie viel innere Replay-/Was-wäre-wenn-Kapazität
  verfuegbar ist.

## `zoom_budget`

- Bereich: `0.0 - 1.0`
- Ebene: fokussierte Wahrnehmung
- Funktion: beschreibt, wie viel Energie für genaueres Hineinschauen in
  einen Bereich verfuegbar ist.

## `old_structure_carryover_risk`

- Bereich: `0.0 - 1.0`
- Ebene: Strukturbindung
- Funktion: beschreibt, ob alte Bereichs- oder Regimewahrnehmung noch zu
  stark in die aktuelle Lage hineinragt.

## `area_price_low` / `area_price_high`

- Bereich: Preiswerte
- Ebene: Preisraum
- Funktion: beschreiben die Grenzen eines betrachteten Preisbereichs.

## `area_distance_from_price`

- Bereich: `0.0 - 1.0`
- Ebene: raeumliche Distanz
- Funktion: beschreibt, wie weit der aktuelle Preis vom Bereich entfernt ist.
- Bedeutung: "Liegt dieser Bereich vor mir, hinter mir oder nahe bei mir?"

## `area_structural_density`

- Bereich: `0.0 - 1.0`
- Ebene: Strukturverdichtung
- Funktion: misst, ob in einem Bereich viele relevante Strukturreize
  zusammenfallen.
- Bedeutung: "Hier ist Form verdichtet."

## `area_energy_compression`

- Bereich: `0.0 - 1.0`
- Ebene: Spannung / Kompression
- Funktion: beschreibt, ob Druck/Energie im Bereich komprimiert wirkt.
- Bedeutung: "Hier fühlt sich Energie gesammelt an."

## `area_mcm_resonance`

- Bereich: `0.0 - 1.0`
- Ebene: MCM-Feld
- Funktion: beschreibt, wie stark ein Bereich im MCM-Feld resoniert.
- Bedeutung: "Dieser Bereich bewegt mein inneres Feld."

## `area_memory_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Erfahrung
- Funktion: beschreibt, ob Memory/Erfahrung diesen Bereich als wiederkehrend
  oder relevant empfindet.

## `area_bearing_quality`

- Bereich: `0.0 - 1.0`
- Ebene: Tragfähigkeit
- Funktion: bewertet, ob ein Bereich als möglicher Handlungsraum tragen
  könnte.

## `area_zoom_need`

- Bereich: `0.0 - 1.0`
- Ebene: Aufmerksamkeit
- Funktion: beschreibt, ob DIO in diesen Bereich hineinzoomen sollte.

## `area_zoom_clarity`

- Bereich: `0.0 - 1.0`
- Ebene: fokussierte Sicht
- Funktion: beschreibt, ob ein Bereich nach dem Zoom klarer oder diffuser
  wird.

## `area_replay_fit`

- Bereich: `0.0 - 1.0`
- Ebene: innere Simulation
- Funktion: beschreibt, ob ein Replay / Was-wäre-wenn-Durchlauf zu
  Erfahrung und aktueller MCM-Lage passt.

## `area_patience_quality`

- Bereich: `0.0 - 1.0`
- Ebene: strategisches Warten
- Funktion: beschreibt, ob Warten auf diesen Bereich sinnvoller ist als
  sofortiges Handeln.

## `area_order_intention`

- Bereich: `0.0 - 1.0`
- Ebene: Order-Idee
- Funktion: beschreibt, ob aus Bereich, Kontext, Memory und Innenlage eine
  weiche Order-Intention entsteht.
- Wichtig: keine harte Order-Regel.

## `area_invalidity_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Verwerfen / Loslassen
- Funktion: beschreibt, ob der Bereich seine Bedeutung verliert.

## `strategic_patience`

- Bereich: `0.0 - 1.0`
- Ebene: Geduld
- Funktion: beschreibt, ob DIO eine Bereichsidee halten kann, ohne impulsiv zu
  handeln.

## `strategic_pressure_interpretation`

- Bereich: `0.0 - 1.0`
- Ebene: Druckdeutung
- Funktion: beschreibt, ob DIO Druck als Raum/Information statt als
  Handlungsbefehl lesen kann.

---

# Aktiver MCM-Kontakt / Spiegelung

Diese Variablen beschreiben die geplante aktive Kontaktbahn zwischen
Außenwahrnehmung und innerer MCM-Lage. Sie sind keine Handelsregeln. Sie
machen sichtbar, wie nah DIO eine Wahrnehmung an das eigene Feld laesst und
ob daraus Resonanz, Überkopplung, Distanz oder Vertiefung entsteht.

## `active_mcm_contact_state`

- Bereich: Dict
- Ebene: Wahrnehmung / MCM-Kontakt
- Funktion: gebündelter Zustand der aktiven Kontakt- und Spiegelbahn.

## `contact_interest`

- Bereich: `0.0 - 1.0`
- Ebene: Aufmerksamkeit / Neugier
- Funktion: beschreibt, ob DIO einen Reiz oder Bereich näher untersuchen
  möchte.
- Bedeutung: "Das zieht meine Wahrnehmung an."

## `contact_focus_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Fokussteuerung
- Funktion: beschreibt, wie stark ein Wahrnehmungsobjekt Vordergrund werden
  will.

## `contact_resonance_probe`

- Bereich: `0.0 - 1.0`
- Ebene: MCM-Berührung
- Funktion: beschreibt die Stärke einer inneren Resonanzprüfung.
- Bedeutung: "Wie reagiert mein Feld, wenn ich diesen Reiz berühre?"

## `outer_inner_resonance`

- Bereich: `0.0 - 1.0`
- Ebene: Außen-Innen-Kopplung
- Funktion: beschreibt, ob Außenform und Innenfeld miteinander schwingen.

## `outer_inner_coherence`

- Bereich: `0.0 - 1.0`
- Ebene: Kohärenz / Reflexion
- Funktion: beschreibt, ob innere Lage und äußere Wahrnehmung gemeinsam
  tragfähig wirken.
- Bedeutung: "Passt mein innerer Zustand noch zu dem, was ich sehe?"

## `inner_change_from_contact`

- Bereich: `0.0 - 1.0`
- Ebene: Interozeption
- Funktion: misst, wie stark sich DIOs Innenlage durch Kontakt mit einem
  Reiz verändert.

## `contact_carrying_quality`

- Bereich: `0.0 - 1.0`
- Ebene: Tragfähigkeit
- Funktion: beschreibt, ob der Kontakt mit der Wahrnehmung stabilisierend
  oder tragend wirkt.

## `contact_overcoupling_risk`

- Bereich: `0.0 - 1.0`
- Ebene: Überkopplung / Reizbindung
- Funktion: beschreibt, ob eine Wahrnehmung das MCM-Feld zu stark besetzt.
- Bedeutung: "Ich bin zu nah am Reiz."

## `contact_release_readiness`

- Bereich: `0.0 - 1.0`
- Ebene: Loslassen / Distanz
- Funktion: beschreibt, ob DIO einen Reiz nach Betrachtung wieder ablegen
  kann.

## `contact_deepen_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Vertiefung
- Funktion: beschreibt, ob ein Kontakt weitere Untersuchung, Zoom oder
  Objektbildung anzieht.

## `contact_replay_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Replay / innere Simulation
- Funktion: beschreibt, ob ein Kontakt eine innere Was-wäre-wenn-Spur
  anregt.

## `contact_curiosity`

- Bereich: `0.0 - 1.0`
- Ebene: Neugier / Lernen
- Funktion: beschreibt lernende, nicht zwingende Annäherung an eine
  Wahrnehmung.

## `contact_felt_shift`

- Bereich: `-1.0 - 1.0`
- Ebene: innere Verschiebung
- Funktion: beschreibt Richtung und Stärke der gefühlten Lageveränderung
  nach Kontakt.

## `contact_selected_depth`

- Bereich: `0.0 - 1.0`
- Ebene: Verarbeitungstiefe
- Funktion: beschreibt, wie tief DIO eine Wahrnehmung aktuell verarbeitet.
- Wichtig: keine feste Tiefe, sondern weiche Selbstregulation.

## `contact_action_maturity`

- Bereich: `0.0 - 1.0`
- Ebene: Kontakt-Reife / Handlungsnähe
- Funktion: beschreibt, ob ein Kontakt nicht nur spuerbar, sondern für eine
  Handlung tragfähig wirkt.
- Wichtig: Diagnosewert, keine Orderfreigabe.

## `contact_bearing_gap`

- Bereich: `0.0 - 1.0`
- Ebene: Reifespannung
- Funktion: beschreibt die Lücke zwischen Kontakt/Impuls und innerer
  Tragfähigkeit.
- Bedeutung: "Ich bin nah am Objekt, aber es trägt mich noch nicht genug."

## `contact_impulse_vs_bearing`

- Bereich: `-1.0 - 1.0`
- Ebene: Impuls gegen Tragfähigkeit
- Funktion: beschreibt, ob Kontaktzug/Neugier/Ordernähe stärker sind als
  Loslassen, Kohärenz und Tragfähigkeit.

## `contact_learning_need`

- Bereich: `0.0 - 1.0`
- Ebene: Lernbedarf / Reifung
- Funktion: beschreibt, ob der Kontakt eher Beobachtung, Replay,
  Distanzierung oder weitere Objektbildung braucht.

## `contact_reality_check`

- Bereich: `0.0 - 1.0`
- Ebene: Realitätsabgleich
- Funktion: beschreibt, ob Innenkontakt, äußere Struktur, Loslassen und
  Tragfähigkeit gemeinsam stimmig wirken.

## `contact_regime_mismatch`

- Bereich: `0.0 - 1.0`
- Ebene: Kontext-/Regime-Reife
- Funktion: beschreibt, ob der Kontakt in eine Weltlage fällt, die nicht
  mehr gut zur bisherigen inneren Stabilität passt.
- Bedeutung: "Die Außenwelt ist fremder, als mein Kontaktgefühl vermuten
  laesst."

## `contact_stability_carryover`

- Bereich: `0.0 - 1.0`
- Ebene: neurochemischer Nachhall / Kontext
- Funktion: beschreibt, ob Stabilität als alter Nachhall in eine veränderte
  Lage getragen wird.
- Bedeutung: "Ich fühle noch Stabilität, aber sie könnte aus der alten
  Weltlage stammen."

## `contact_context_maturity`

- Bereich: `0.0 - 1.0`
- Ebene: Kontextreife
- Funktion: beschreibt, ob Struktur, Kontext, Transfer und innere Distanz den
  Kontakt gemeinsam tragen.

## `contact_context_reframe_need`

- Bereich: `0.0 - 1.0`
- Ebene: Reframing / Lernen
- Funktion: beschreibt, ob ein Kontakt eher neu gerahmt, beobachtet, gezoomt
  oder replayed werden muss, bevor Handlung daraus reifen kann.

## `contact_posture`

- Bereich: String
- Ebene: innere Haltung
- Funktion: benennt die aktuelle Kontaktlage.
- Mögliche Werte:
  `background_scan`, `curious_touch`, `resonant_contact`,
  `reflective_contact`, `overcoupled_touch`, `release_contact`,
  `deepening_contact`.

---

# Mehrdimensionale Wahrnehmungsachsen / Zeit, Hypothese und Reorganisation

Diese Achsen sind als Ziel- und Diagnosebegriffe aus den MCM-Abhandlungen
Block D bis G.1 abgeleitet. Sie sind noch nicht alle technische Laufzeitwerte.
Sie beschreiben, welche innere Quellenbindung, Möglichkeitsbildung und
Reorganisation DIO später lesbar machen soll.

Leitidee:
DIO soll eine Wahrnehmung nicht nur als Signal führen. Sie bekommt innere
Koordinaten: Zeit, Quelle, Raum, Kontakt, Tragfähigkeit und
Reorganisation. Dadurch kann DIO unterscheiden, ob etwas aktuell aus der
Außenwelt wirkt, aus Memory kommt, als Nachhall weiterzieht, als Hypothese
auftaucht oder zu nah an das Handlungszentrum rückt.

## `perception_source`

- Bereich: String
- Ebene: Quellenbindung
- Funktion: beschreibt, aus welcher Quelle eine Wahrnehmung stammt.
- Mögliche Lagen: `present_world`, `memory`, `learned_knowledge`,
  `afterimage`, `replay`, `hypothesis`, `expectation`.

## `source_temporal_layer`

- Bereich: String
- Ebene: Zeitfeld
- Funktion: ordnet eine Information zeitlich ein: Gegenwart, Nachhall,
  Erinnerung, Wissen, Replay, Hypothese oder Erwartung.

## `present_world_binding`

- Bereich: `0.0 - 1.0`
- Ebene: Realitätsbindung
- Funktion: beschreibt, wie stark eine Wahrnehmung an aktuelle Außenwelt
  gebunden ist.

## `memory_reality_distance`

- Bereich: `0.0 - 1.0`
- Ebene: Memory / Realitätsabstand
- Funktion: beschreibt, ob eine aktivierte Erinnerung als Erinnerung
  erkannt wird oder zu nah an Gegenwart rückt.

## `perceptual_space_axis`

- Bereich: Dict / String
- Ebene: Wahrnehmungsraum
- Funktion: beschreibt die raeumliche Verortung einer Wahrnehmung im
  inneren Feld.
- Mögliche Lagen: `field_center`, `near_field`, `far_field`,
  `foreground`, `background`, `edge`, `memory_space`, `hypothesis_space`.

## `perceptual_depth`

- Bereich: `0.0 - 1.0`
- Ebene: Tiefenwahrnehmung
- Funktion: beschreibt, ob DIO eine Wahrnehmung flach als Reiz oder tiefer
  als Objekt, Erinnerung, Hypothese oder Kontaktfeld verarbeitet.

## `field_center_distance`

- Bereich: `0.0 - 1.0`
- Ebene: Raumlage / Handlungsnähe
- Funktion: beschreibt, wie nah eine Wahrnehmung am inneren
  Handlungszentrum liegt.
- Wichtig: Nähe bedeutet nicht automatisch Handlung. Sie zeigt nur, dass
  die Wahrnehmung stark in DIOs aktueller Lage steht.

## `foreground_binding`

- Bereich: `0.0 - 1.0`
- Ebene: Vordergrundbindung
- Funktion: beschreibt, wie stark eine Wahrnehmung den Vordergrund besetzt.

## `background_afterimage`

- Bereich: `0.0 - 1.0`
- Ebene: Hintergrund / Nachhall
- Funktion: beschreibt, ob eine Wahrnehmung noch als Hintergrundspur wirkt,
  obwohl sie nicht mehr aktuelle Außenwelt ist.

## `hypothesis_branch_state`

- Bereich: Dict / String
- Ebene: Hypothesenraum
- Funktion: beschreibt einen möglichen Entwicklungszweig, ohne ihn als
  Realität zu behandeln.

## `branch_stability`

- Bereich: `0.0 - 1.0`
- Ebene: Hypothesenstabilität
- Funktion: beschreibt, ob ein möglicher Verlauf innerlich stabil,
  fragil oder widerspruechlich wirkt.

## `branch_attractor_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Attraktor / Zukunftsmöglichkeit
- Funktion: beschreibt, wie stark ein möglicher Verlauf die innere
  Erwartung anzieht.
- Wichtig: hoher Wert ist kein Zukunftsbeweis, sondern nur eine
  Möglichkeitskraft.

## `hypothesis_reality_gap`

- Bereich: `0.0 - 1.0`
- Ebene: Realitätsabgleich
- Funktion: beschreibt die Lücke zwischen innerer Hypothese und aktueller
  Außenwelt.

## `field_reorganization_state`

- Bereich: String
- Ebene: Reorganisation
- Funktion: beschreibt, ob ein verdichteter Zustand nur belastet oder
  bereits in eine neue Ordnung überführt wird.

## `reorganization_threshold`

- Bereich: `0.0 - 1.0`
- Ebene: Reorganisationsschwelle
- Funktion: beschreibt, ob lokale Verdichtung so hoch ist, dass die bisherige
  Ordnung nicht mehr ausreichend trägt.

## `higher_order_coupling`

- Bereich: `0.0 - 1.0`
- Ebene: übergeordnete Feldkopplung
- Funktion: beschreibt, ob DIO eine Lage nicht lokal erzwingt, sondern in
  einen breiteren Ordnungszusammenhang überführt.

---

# Metaregulator-Schicht / Regler zweiter Ordnung

Diese Achsen sind Zielbegriffe aus Block S der MCM-Abhandlungen. Sie
beschreiben nicht die unmittelbare Feldlage, sondern wie DIO seine eigene
Lage verarbeitet. Sie sind keine harten Gates.

## `return_strength`

- Bereich: `0.0 - 1.0`
- Ebene: Rückführung / Zentrum
- Funktion: beschreibt, wie stark DIO nach Abweichung, Aktivierung oder
  Instabilität in Richtung stabilerer Zustände zurückfindet.

## `integration_capacity`

- Bereich: `0.0 - 1.0`
- Ebene: Integration / Erfahrung
- Funktion: beschreibt, wie gut neue Erfahrung, Spannung, Konflikt oder
  Irritation in tragfähige Muster überführt werden kann.

## `variance_regulation`

- Bereich: `0.0 - 1.0`
- Ebene: Varianz / Flexibilitaet
- Funktion: beschreibt, ob DIO zwischen Flexibilitaet und Stabilität
  balancieren kann, ohne in Chaos oder Starre zu kippen.

## `load_tolerance`

- Bereich: `0.0 - 1.0`
- Ebene: Belastungstoleranz
- Funktion: beschreibt, wie viel Spannung, Unsicherheit oder Überforderung
  DIO tragen kann, ohne in Dysregulation oder starre Schutzmuster zu fallen.

## `impulse_control`

- Bereich: `0.0 - 1.0`
- Ebene: Impulsregulation
- Funktion: beschreibt, ob DIO ploetzliche Handlungs- oder Schutzimpulse
  halten, verzoegern oder in geordnetere Reaktionsformen überführen kann.

## `frustration_tolerance`

- Bereich: `0.0 - 1.0`
- Ebene: Frustrationsverarbeitung
- Funktion: beschreibt, wie DIO mit nicht erfuellter Erwartung,
  Fehlschlag, blockiertem Impuls oder widerspruechlicher Lage umgeht.

## `protective_distance_regulation`

- Bereich: `0.0 - 1.0`
- Ebene: Schutzweite
- Funktion: beschreibt, ob DIO Nähe und Distanz zu belastenden Reizen
  organisch dosieren kann.

## `self_reflection_regulator`

- Bereich: `0.0 - 1.0`
- Ebene: Selbstreflexion
- Funktion: beschreibt, ob DIO eigene Zustände bemerkt, benennt und dadurch
  regulierend auf sich selbst einwirkt.

## `distance_regulation`

- Bereich: `0.0 - 1.0`
- Ebene: Distanzierung / Kontakt
- Funktion: beschreibt, ob DIO einen Reiz, eine Erinnerung oder Hypothese
  bewusst näher heranlaesst, auf Abstand haelt oder wieder loslaesst.

---

# Unterbewusstsein / Bewusster Arbeitsraum

Diese Variablen trennen schnelle, diffuse Hintergrundwahrnehmung von
bewussterer Betrachtung. Sie sind keine Gates, sondern beschreiben den
Übergang von Bauchgefühl zu bewusstem Kontakt.

## `subconscious_field_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Unterbewusster Feldscan
- Funktion: beschreibt, wie viel Reizdruck, Weltverschiebung,
  Nachwirkung und reaktive Nervenspannung im Hintergrundfeld ankommt.

## `subconscious_habituation`

- Bereich: `0.0 - 1.0`
- Ebene: Gewoehnung / Wiedererkennung
- Funktion: beschreibt, wie vertraut, tragbar oder wiedererkannt ein
  Hintergrundreiz bereits ist.

## `subconscious_filter_strength`

- Bereich: `0.0 - 1.0`
- Ebene: Wahrnehmungsfilter
- Funktion: beschreibt, wie gut DIO Hintergrundreize puffern kann, ohne sie
  sofort bewusst tragen zu müssen.

## `subconscious_buffering`

- Bereich: `0.0 - 1.0`
- Ebene: Hintergrundpufferung
- Funktion: beschreibt, wie viel Feldspannung unterbewusst gehalten wird.

## `subconscious_leakage`

- Bereich: `0.0 - 1.0`
- Ebene: Durchschlag ins Bewusstsein
- Funktion: beschreibt, wie stark ungefilterter Hintergrunddruck in die
  bewusste Arbeitsflaeche eindringt.

## `subconscious_afterimage_depth`

- Bereich: `0.0 - 1.0`
- Ebene: Unterbewusster Nachhall / Tiefenwahrnehmung
- Funktion: beschreibt, wie tief eine alte Feldwirkung noch im
  Hintergrundraum liegt. Sie entsteht aus `felt_afterimage`,
  `temporal_afterimage`, `area_afterimage` und fehlender zeitlicher
  Quellenbindung.

## `subconscious_afterimage_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Unterbewusster Nachhalldruck
- Funktion: beschreibt, wie stark dieser Nachhall noch drückt, ohne schon
  klar als Gegenwart, Erinnerung oder alter Reiz sortiert zu sein.

## `subconscious_afterimage_bearing`

- Bereich: `0.0 - 1.0`
- Ebene: Tragfähiger Nachhall
- Funktion: beschreibt, ob der Nachhall als Erfahrung tragbar, pufferbar
  und einordnend wirkt, statt DIO unbewusst zu überkoppeln.

## `subconscious_afterimage_clarity`

- Bereich: `0.0 - 1.0`
- Ebene: Nachhall-Klarheit
- Funktion: beschreibt, ob DIO den Nachhall zeitlich und raeumlich besser
  verorten kann: Das ist eine alte Wirkung, nicht zwingend die aktuelle
  Außenwelt.

## `subconscious_afterimage_release`

- Bereich: `0.0 - 1.0`
- Ebene: Nachhall-Entlastung
- Funktion: beschreibt, ob DIO den Nachhall wieder loslassen kann, ohne ihn
  in Handlung oder bewusste Überlastung zu ziehen.

## `subconscious_afterimage_reflection_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Reflexionszug aus dem Unterbewusstsein
- Funktion: beschreibt, ob tiefer Nachhalldruck bei geringer Klarheit und
  geringer Entlastung mehr Beobachtung und Reflexion nahelegt. Das ist kein
  Stoppschalter, sondern ein weicher Zug zur inneren Sortierung.

## `conscious_selection_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Bewusste Auswahl
- Funktion: beschreibt, wie stark ein Reiz nach bewusster Betrachtung,
  Kontakt oder Reflexion zieht.

## `conscious_workspace_focus`

- Bereich: `0.0 - 1.0`
- Ebene: Bewusster Arbeitsraum
- Funktion: beschreibt, wie fokussiert und geordnet DIO eine ausgewählte
  Form, Hypothese oder Kontaktlage betrachten kann.

## `conscious_workspace_load`

- Bereich: `0.0 - 1.0`
- Ebene: Bewusste Denklast
- Funktion: beschreibt, wie teuer die bewusste Verarbeitung gerade ist.

## `conscious_gate_balance`

- Bereich: `0.0 - 1.0`
- Ebene: Übergang Unterbewusstsein -> Bewusstsein
- Funktion: beschreibt, ob der Übergang vom Hintergrundfeld in den
  bewussten Arbeitsraum tragfähig dosiert ist.

---

# Integrationsantwort

Diese Variablen beschreiben, wie DIO mit `integration_strain` arbeitet.
Sie sind keine Verbote, sondern innere Verarbeitungsachsen.

## `integration_strain_value`

- Bereich: `0.0 - 1.0`
- Ebene: Integrationsspannung
- Funktion: beschreibt, wie stark neue Lage, Reorganisation,
  semantische Verschiebung und bewusste Last noch nicht eingeordnet sind.

## `integration_sorting_need`

- Bereich: `0.0 - 1.0`
- Ebene: innere Sortierung
- Funktion: beschreibt, wie stark DIO ordnen, entwirren und den
  Arbeitsraum entlasten muss.

## `integration_reframe_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Reframing
- Funktion: beschreibt, wie stark eine Lage anders betrachtet oder neu
  gerahmt werden will.

## `integration_memory_recall`

- Bereich: `0.0 - 1.0`
- Ebene: Erinnerung / Vergleich
- Funktion: beschreibt, wie viel tragfähige Erfahrung für die aktuelle
  Integrationsspannung verfuegbar ist.

## `integration_contact_deepening`

- Bereich: `0.0 - 1.0`
- Ebene: selektive Kontaktvertiefung
- Funktion: beschreibt, ob DIO einen Kontakt genauer anfassen, prüfen oder
  fühlen sollte, statt alles global zu verarbeiten.

## `integration_response_strength`

- Bereich: `0.0 - 1.0`
- Ebene: Integrationsreaktion
- Funktion: beschreibt, wie stark DIO auf Integrationsspannung mit
  Sortierung, Reframing, Erinnerung und Kontaktvertiefung antwortet.

## `integration_response_state`

- Typ: Textlabel
- Ebene: innere Selbstbenennung
- Funktion: beschreibt die dominante Form der Integrationsantwort.

---

# Gerichtete Vorsicht / vorsichtige Hypothese

Diese Variablen beschreiben, ob Vorsicht nur passiv macht oder ob daraus
eine vorsichtige Orientierung entsteht.

## `cautious_hypothesis_strength`

- Bereich: `0.0 - 1.0`
- Ebene: vorsichtige Hypothesenbildung
- Funktion: beschreibt, wie stark aus Memory-Recall, Reframing und
  Kontaktvertiefung eine vorsichtige Hypothese entsteht.

## `cautious_hypothesis_clarity`

- Bereich: `0.0 - 1.0`
- Ebene: Hypothesenklarheit
- Funktion: beschreibt, wie klar und strukturgebunden diese vorsichtige
  Hypothese bereits ist.

## `cautious_hypothesis_patience`

- Bereich: `0.0 - 1.0`
- Ebene: Geduld / Schutzhemmung
- Funktion: beschreibt, ob DIO die Vorsicht tragen kann, ohne sofort in
  Handlung oder Chaos zu kippen.

## `cautious_hypothesis_state`

- Typ: Textlabel
- Ebene: innere Selbstbenennung
- Funktion: beschreibt, ob keine, schwache, erinnerungsbasierte,
  beobachtende, kontaktvertiefende oder planende Vorsicht vorliegt.

---

# Zeitliche Kohärenz / Wahrnehmungskontinuität

Diese Variablen beschreiben, ob DIO eine Wahrnehmung als neuen Moment,
Fortsetzung, Wiederkehr, Nachhall, alte Erinnerung oder koharente Sequenz
erlebt.

## `temporal_identity`

- Typ: Text-ID
- Ebene: grobe Zeitidentitaet
- Funktion: bindet einen Wahrnehmungskontakt über Formfamilie, Kontext und
  grobe visuelle Signatur.
- Bedeutung: "Gehört dieser Moment zu einer bekannten fortlaufenden
  Kontaktspur?"

## `temporal_source_identity`

- Typ: Text-ID
- Ebene: feine Quellenidentitaet
- Funktion: haelt den konkreteren Einzelabdruck aus Form-Symbol,
  Compound-ID, Visual-ID, Kontext und Signatur fest.
- Bedeutung: "Welcher feine Abdruck liegt unter der groben Zeitspur?"
- Hinweis: Diese ID verhindert nicht die Wiederkehr. Sie dient als
  Quelleninformation, damit DIO nicht nur grob, sondern bei Bedarf auch
  detailliert schauen kann.

## `temporal_binding_state`

- Typ: Textlabel
- Ebene: Zeitbindung / episodische Kontinuität
- Funktion: benennt den dominanten zeitlichen Kontaktzustand.

## `temporal_continuity`

- Bereich: `0.0 - 1.0`
- Ebene: Fortsetzung
- Funktion: beschreibt, wie stark die aktuelle Wahrnehmung als Fortsetzung
  einer vorherigen Wahrnehmung erlebt wird.

## `temporal_source_binding`

- Bereich: `0.0 - 1.0`
- Ebene: Quellenbindung
- Funktion: beschreibt, wie gut DIO die Wahrnehmung an Form, Struktur,
  Kontext und visuellen Boden binden kann.

## `temporal_recurrence`

- Bereich: `0.0 - 1.0`
- Ebene: Wiederkehr
- Funktion: beschreibt, ob die zeitliche Identitaet bereits wiederholt
  aufgetaucht ist.

## `temporal_novelty`

- Bereich: `0.0 - 1.0`
- Ebene: Neuheit
- Funktion: beschreibt, wie neu oder ungebunden der aktuelle Kontakt wirkt.

## `temporal_afterimage`

- Bereich: `0.0 - 1.0`
- Ebene: Nachhall
- Funktion: beschreibt, wie stark eine vorherige Wahrnehmung noch im Feld
  nachwirkt.

## `temporal_decay`

- Bereich: `0.0 - 1.0`
- Ebene: Alterung / Verblassen
- Funktion: beschreibt, wie weit eine Wahrnehmung zeitlich von der
  Gegenwart entfernt oder verblasst ist.

## `temporal_context_depth`

- Bereich: `0.0 - 1.0`
- Ebene: Kontext-Tiefe
- Funktion: beschreibt, wie viel zeitliche, strukturelle und symbolische
  Tiefe ein Kontakt besitzt.
- MCM-Lesart: diese Tiefe entsteht nicht nur aus Zeitabstand, sondern aus
  Entfernung, Energie und innerer Aktualitaet des Kontakts.

## `mcm_spacetime_depth` / Zielgröße

- Bereich: `0.0 - 1.0`
- Ebene: MCM-Raumzeit / innere Tiefenwahrnehmung
- Status: diagnostisch umgesetzt im Temporal-/MCM-Kern.
- Funktion: beschreibt, wie tief ein Eindruck im inneren Raumzeit-Gefuege
  liegt.
- Bedeutung: "Wie weit, wie energiereich und wie aktuell ist dieser
  Eindruck in meinem MCM-Feld?"

## `memory_experience_depth`

- Bereich: `0.0 - 1.0`
- Ebene: Memory / zeitlich tiefe Erfahrung
- Status: diagnostisch umgesetzt.
- Funktion: beschreibt, ob eine Erinnerung nicht nur vorhanden ist, sondern
  als erlebte Spur mit Nähe, Wiederkehr, Nachhall und Lernvertrauen wirkt.
- Bedeutung: "Ist das nur gespeicherte Information oder bereits Erfahrung
  mit Zeit-Tiefe?"

## `future_projection_depth`

- Bereich: `0.0 - 1.0`
- Ebene: Hypothese / Zukunftstiefe
- Status: diagnostisch umgesetzt.
- Funktion: beschreibt, ob aus aktueller Tiefe, Sequenzkohärenz,
  Strukturstabilität und Nachhall eine vorausgerichtete Möglichkeitsform
  entsteht.
- Bedeutung: "Kann aus dieser Erfahrung eine mögliche Zukunftsform
  entstehen?"

## `temporal_self_location`

- Bereich: `0.0 - 1.0`
- Ebene: Selbstverortung / innere Zeit
- Status: diagnostisch umgesetzt.
- Funktion: beschreibt, ob DIO sich im eigenen Wahrnehmungsverlauf
  verorten kann: Gegenwart, Nachhall, Erinnerung, Hypothese oder Erwartung.
- Bedeutung: "Wo stehe ich gerade in meinem eigenen inneren Zeitraum?"

## `temporal_self_location_state`

- Typ: Textlabel
- Ebene: Selbstverortung / innere Zeit
- Status: diagnostisch umgesetzt.
- Funktion: benennt die qualitative Lage des Kontakts.
- Mögliche Werte:
  - `present_contact`
  - `afterimage_trace`
  - `remembered_experience`
  - `future_possibility`
  - `new_unmapped_contact`
  - `unlocated_contact`

## `spacetime_unlocated_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Regulation / Raumzeit-Selbstverortung
- Funktion: beschreibt, wie stark DIO einen Kontakt noch nicht sauber im
  inneren Raumzeitfeld verorten kann.
- Bedeutung: "Ich weiss noch nicht genau, wo dieser Eindruck in meiner
  inneren Zeit liegt."

## `spacetime_memory_bearing`

- Bereich: `0.0 - 1.0`
- Ebene: Memory / Erfahrungstragfähigkeit
- Funktion: beschreibt, wie tragend die Erinnerungstiefe für die aktuelle
  Wahrnehmung ist.
- Bedeutung: "Meine Erinnerung hat tragende zeitliche Tiefe."

## `spacetime_future_bearing`

- Bereich: `0.0 - 1.0`
- Ebene: Hypothese / Zukunftstragfähigkeit
- Funktion: beschreibt, wie tragend die Zukunftstiefe einer Wahrnehmung
  wirkt.
- Bedeutung: "Aus diesem Kontakt kann eine tragende Möglichkeit entstehen."

## `spacetime_reflection_need`

- Bereich: `0.0 - 1.0`
- Ebene: Regulation / Reflexion
- Funktion: übersetzt flache oder unklare Raumzeit-Verortung in
  Reflexionsbedarf.
- Bedeutung: "Ich sollte erst verorten, bevor ich handle."

## `spacetime_regulation_support`

- Bereich: `0.0 - 1.0`
- Ebene: Regulation / Tragfähigkeit
- Funktion: beschreibt, wie stark Memory-, Zukunfts- und Gegenwartstiefe
  Regulation und Integration stuetzen.
- Bedeutung: "Meine Raumzeit-Wahrnehmung trägt meine innere Lage."

## `spacetime_regulation_state`

- Typ: Textlabel
- Ebene: Regulation / Raumzeitlage
- Funktion: benennt, wie die Raumzeit-Wahrnehmung regulatorisch wirkt.
- Mögliche Werte:
  - `spacetime_open`
  - `spacetime_unlocated_reflection`
  - `afterimage_reframe`
  - `memory_depth_bearing`
  - `future_depth_watch`
  - `present_depth_bearing`

## `temporal_self_consistency`

- Bereich: `0.0 - 1.0`
- Ebene: Selbstkonsistenz
- Funktion: beschreibt, ob DIOs innere Wahrnehmung über Zeit stimmig
  bleibt.

## `perception_sequence_coherence`

- Bereich: `0.0 - 1.0`
- Ebene: Sequenz-Kohärenz
- Funktion: beschreibt, ob einzelne Wahrnehmungsmomente zu einer
  zusammenhängenden Sequenz werden.

## `memory_time_distance`

- Bereich: `0.0 - 1.0`
- Ebene: Memory-Zeitdistanz
- Funktion: beschreibt, wie weit die passende Erinnerung zeitlich von der
  Gegenwart entfernt ist.

## `reality_anchor`

- Bereich: `0.0 - 1.0`
- Ebene: Zeitbindung / Gegenwartsprüfung
- Funktion: beschreibt, wie gut ein innerer Kontextfaden durch
  Quellenbindung, Sequenzkoharenz, Strukturqualität, Strukturstabilität,
  Kontextvertrauen und visuelle Erdung getragen wird.
- Bedeutung: "Passt mein innerer Zusammenhang wirklich zur aktuellen
  Außenwelt?"

## `overtrust_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Kontextvertrauen / Skepsis
- Funktion: beschreibt, ob ein innerer Zeitfaden bei schwacher
  Gegenwartsbindung zu viel Bedeutung bekommen würde.
- Bedeutung: "Ich fühle einen Zusammenhang, aber ich sollte ihm noch nicht
  blind vertrauen."

## `nervous_system_overload`

- Bereich: `0.0 - 1.0`
- Ebene: Nervensystem / innere Überlastung
- Funktion: beschreibt, ob Cortisol, Noradrenalin, Glutamat,
  Carryover-Risiko und reaktiver Handlungsdruck die innere Tragfähigkeit
  überlasten.
- Bedeutung: "Meine Nerven sind überlastet."

## `escape_action_drive`

- Bereich: `0.0 - 1.0`
- Ebene: Handlung / Entladungsdruck
- Funktion: beschreibt, ob Handlung eher als Ausweg aus innerer Spannung
  entstehen könnte.
- Bedeutung: "Will ich handeln, weil die Struktur trägt, oder weil ich aus
  der Situation raus will?"

## `shock_response_risk`

- Bereich: `0.0 - 1.0`
- Ebene: Schock-/Überreizreaktion
- Funktion: beschreibt, ob Überlastung, Weltwechsel, geringe emotionale
  Entkopplung und reaktiver Handlungsdruck in einen Schockmodus kippen
  könnten.
- Bedeutung: "Mein Nervensystem könnte gerade überreagieren."

## `nervous_overload_reflection_need`

- Bereich: `0.0 - 1.0`
- Ebene: Reflexion / Selbstwahrnehmung
- Funktion: beschreibt, wie stark DIO die eigene nervliche Lage betrachten
  sollte, bevor aus Spannung Handlung wird.
- Bedeutung: "Ich muss meine innere Lage prüfen, bevor ich handle."

## `active_context_self_certainty`

- Bereich: `0.0 - 1.0`
- Ebene: Kontextvertrauen / innere Sicherheit
- Funktion: beschreibt, wie absolut der aktive innere Kontext gerade
  wirkt. Er entsteht aus Aktivierung, Support, Bearing und geringem
  Konflikt des `active_context_trace`.
- Bedeutung: "Mein innerer Kontext fühlt sich sicher an."

## `nervous_context_overcoupling`

- Bereich: `0.0 - 1.0`
- Ebene: Nervensystem / Kontext-Überkopplung
- Funktion: beschreibt, ob ein sehr sicher wirkender innerer Kontext auf
  ein belastetes Nervensystem trifft. Dann wird die Kontext-Sicherheit
  nicht gelöscht, aber reflektiver und weniger absolut behandelt.
- Bedeutung: "Ich bin innerlich sicher, aber meine Nervenlage könnte
  diese Sicherheit verzerren."

## `context_modulation_label`

- Bereich: Textzustand
- Ebene: aktiver Kontext / Selbstwahrnehmung
- Funktion: beschreibt, ob der aktive Kontext ungefaerbt bleibt oder durch
  nervliche Überkopplung moduliert wurde.
- Mögliche Werte:
  - `unmodulated_context`
  - `nervous_tinted_context`
  - `overcoupled_context`
- Bedeutung: "Mein Zeit-/Kontextfaden ist vorhanden, aber seine gefühlte
  Sicherheit kann nervlich gefaerbt sein."

## `area_temporal_contact_mode`

- Bereich: Textzustand
- Ebene: strategisches Fenster / MCM-Raumzeitkontakt
- Funktion: beschreibt, wie ein betrachteter Preis-/Strukturbereich
  zeitlich im MCM-Feld liegt.
- Mögliche Werte:
  - `present_area_contact`
  - `future_area_watch`
  - `memory_area_recall`
  - `unlocated_area_probe`
  - `afterimage_area_reframe`
  - `open_time_contact`
- Bedeutung: "Ist dieser Bereich Gegenwartskontakt, Zukunftsraum,
  Erinnerung oder noch unverorteter Druck?"

## `area_spacetime_fit`

- Bereich: `0.0 - 1.0`
- Ebene: strategisches Fenster / Raumzeit-Tragfähigkeit
- Funktion: verdichtet aktuelle Nähe, Zukunftsmöglichkeit,
  Erinnerungstiefe und MCM-Raumzeit-Support eines Bereichs.
- Bedeutung: "Passt dieser sichtbare Bereich zeitlich zu meiner inneren
  Lage?"

## `contact_temporal_mode`

- Bereich: Textzustand
- Ebene: aktiver MCM-Kontakt
- Funktion: beschreibt, wie DIO den gerade aktiven Kontakt zeitlich
  erlebt.
- Mögliche Werte:
  - `present_contact_touch`
  - `future_contact_watch`
  - `memory_contact_recall`
  - `unlocated_contact_probe`
  - `afterimage_contact_reframe`
  - `open_time_contact`
- Bedeutung: "Berühre ich gerade Gegenwart, beobachte ich Zukunftsraum,
  rufe ich Erinnerung auf oder muss ich den Kontakt erst verorten?"

## `contact_temporal_bearing`

- Bereich: `0.0 - 1.0`
- Ebene: aktiver MCM-Kontakt / zeitliche Tragfähigkeit
- Funktion: beschreibt, ob der aktive Kontakt durch Gegenwart,
  Zukunftsmöglichkeit, Erinnerung und Raumzeit-Fit getragen wird.
- Bedeutung: "Dieser Kontakt hat zeitliche Tiefe und trägt eher."

## `contact_unlocated_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: aktiver MCM-Kontakt / unverorteter Druck
- Funktion: beschreibt, ob ein Kontakt zwar reizvoll oder spuerbar ist,
  aber zeitlich noch nicht sauber in Gegenwart, Erinnerung oder Zukunft
  verortet wurde.
- Bedeutung: "Ich spuere etwas, aber ich weiss noch nicht, wo es in meiner
  Raumzeit liegt."

## `contact_future_watch` / `contact_memory_depth` / `contact_presentness`

- Bereich: `0.0 - 1.0`
- Ebene: aktiver MCM-Kontakt / zeitliche Teilachsen
- Funktion:
  - `contact_presentness`: Gegenwartsnähe des Kontakts
  - `contact_future_watch`: beobachteter Möglichkeitsraum
  - `contact_memory_depth`: erinnerte Erfahrungstiefe
- Bedeutung: DIO bekommt keine Regel, sondern mehr innere Sprache für die
  zeitliche Lage eines Kontakts.

## `area_future_to_present_readiness`

- Bereich: `0.0 - 1.0`
- Ebene: strategisches Fenster / Übergangsreife
- Funktion: beschreibt, ob ein Bereich aus Zukunftsbeobachtung in
  gegenwärtigen Kontakt reifen kann.
- Bedeutung: "Dieser Bereich war Zukunftsraum, könnte aber jetzt
  berührbar werden."

## `contact_future_to_present_readiness`

- Bereich: `0.0 - 1.0`
- Ebene: aktiver MCM-Kontakt / Übergangsreife
- Funktion: beschreibt, ob DIO aus `future_contact_watch` organisch in
  `maturing_present_contact` wechseln kann.
- Bedeutung: "Meine Beobachtung wird tragfähig genug, um als Gegenwart
  geprüft zu werden."

---

# Emergente Gedächtnisspur / Thought-Seed-Diagnose

## `thought_seed_id`

- Ebene: innere Denkschicht / emergente Gedächtnisspur
- Funktion: stabile Kurzkennung eines Gedankenkeims aus Entscheidungslage,
  Strukturzustand, Formanker, Kontextanker und Reifeprofil.
- Bedeutung: "Dieser innere Gedanke kann später wiedererkannt werden."

## `thought_seed_label`

- Ebene: innere Syntax
- Funktion: lesbare DIO-Bezeichnung des Gedankenkeims.
- Bedeutung: "So benennt DIO diese innere Spur in seiner technischen Sprache."

## `thought_trace_strength`

- Bereich: `0.0 - 1.0`
- Ebene: Aktivierungsstärke eines Gedankenkeims
- Funktion: misst, wie stark eine offene Strukturdeutung im Feld als
  Denkbewegung erscheint.
- Bedeutung: "Dieser Gedanke ist schwach, deutlich oder dominant spürbar."

## `thought_recall_potential`

- Bereich: `0.0 - 1.0`
- Ebene: Wiedererinnerung / spätere Wiederkehr
- Funktion: beschreibt, wie gut ein Gedankenkeim später wieder aufgerufen
  oder mit ähnlichen Formen verbunden werden kann.
- Bedeutung: "Diese Spur könnte wiederkommen."

## `thought_maturity`

- Bereich: `0.0 - 1.0`
- Ebene: Reife der inneren Strukturhypothese
- Funktion: verbindet Realitätsbindung, Strukturdeutung, Feldsupport,
  Entscheidungsreife, Formsymbolreife und zeitliche Tragfähigkeit.
- Bedeutung: "Dieser Gedanke ist unreif, reifend oder handlungsnah."

## `reality_binding_score`

- Bereich: `0.0 - 1.0`
- Ebene: Erdung / Realitätsbindung
- Funktion: prüft, ob der Gedankenkeim an Form, MCM-Feld, Erfahrung,
  Raumzeitkontakt und Konsequenz anschließbar bleibt.
- Bedeutung: "Der Gedanke ist geerdet oder läuft zu frei."

## `thought_confirmation_score`

- Bereich: `0.0 - 1.0`
- Ebene: innere Bestätigung / Gedankenreife
- Funktion: beschreibt, ob ein Gedankenkeim bereits im Moment durch
  Strukturdeutung, Raumzeit-Fit, Entry-Choice-Bearing, Zielüberzeugung,
  Feldsupport, Formkontakt und Realitätskontakt bestätigt wirkt.
- Bedeutung: "Diese Idee ist nicht nur spürbar, sondern innerlich schon
  besser bestätigt."
- Wichtig: Dieser Wert ist diagnostisch. Er ist keine harte Handelsregel und
  kein nachträgliches Outcome-Wissen.

## `hallucination_drift_risk`

- Bereich: `0.0 - 1.0`
- Ebene: Driftwarnung
- Funktion: beschreibt, ob ein Gedanke stark aktiviert ist, aber zu wenig
  Realitätsbindung, Zeitverortung oder Erfahrungskontakt besitzt.
- Bedeutung: "Hier droht innere Fantasie ohne ausreichend Weltkontakt."

## `overthinking_risk`

- Bereich: `0.0 - 1.0`
- Ebene: Denk-/Regulationslast
- Funktion: beschreibt, ob ein Gedankenkeim in Grübeln,
  Überregulation oder innere Kaskaden kippen könnte.
- Bedeutung: "DIO denkt zu viel über den Gedanken, ohne dass er reifer wird."

## `seed_metaregulator_state`

- Ebene: Metaregulator / Regler zweiter Ordnung
- Mögliche Werte:
  - `seed_focus`
  - `seed_replay`
  - `seed_mature`
  - `seed_store`
  - `seed_release`
  - `seed_action_ready`
  - `seed_drift_watch`
  - `seed_overthinking_watch`
- Funktion: beschreibt, wie der Metaregulator den Gedankenkeim behandelt.
- Bedeutung: "Fokussieren, replayen, reifen lassen, speichern, loslassen,
  handlungsnah halten oder Drift/Überdenken beobachten."

## `emergent_memory_trace`

- Bereich: `true / false`
- Ebene: innere Gedächtnisspur
- Funktion: markiert, ob eine offene Strukturhypothese als innere Spur
  erhalten bleibt.
- Bedeutung: "Loslassen heißt nicht löschen."

## `thought_seed_*` im Outcome-Kontext

- Ebene: Rückkopplung / Konsequenzbindung
- Funktion: ab Lauf 48 wird der aktive Gedankenkeim in den
  Entry-/Outcome-Kontext übernommen.
- Felder:
  - `thought_seed_id`
  - `thought_seed_label`
  - `thought_seed_metaregulator_state`
  - `thought_seed_emergent_state`
  - `thought_seed_trace_strength`
  - `thought_seed_maturity`
  - `thought_seed_reality_binding`
  - `thought_seed_confirmation`
  - `thought_seed_consequence_echo`
  - `thought_seed_reorganization_echo`
  - `thought_seed_consequence_alignment`
  - `thought_seed_consequence_balance`
  - `thought_seed_reality_lag`
  - `thought_seed_structural_grounding`
  - `thought_seed_open_hypothesis_pressure`
  - `thought_seed_drift_risk`
  - `thought_seed_overthinking_risk`
- Bedeutung: "Dieser Trade entstand aus diesem Gedankenkeim und hatte diese
  spätere Konsequenz."
- Lauf-48-Befund:
  - `399 / 399` Outcome-Einträge enthalten eine `thought_seed_id`.
  - Die technische Kette ist damit sichtbar:
    `Gedankenkeim -> Entry-Kontext -> Trade/Cancel -> Konsequenz`.
  - Die innere Seed-Sprache ist weiterhin vorsichtiger als die spätere
    Outcome-Bestätigung. Das ist ein Reifethema, kein Motoriksignal.

## `consequence_echo`

- Bereich: `0.0 - 1.0`
- Ebene: Thought-Seed / Konsequenznachhall
- Funktion: konstruktiver Nachhall aus vorheriger Prozessqualität,
  konstruktiver Stimulation, Utility-Spuren und Memory-Support.
- Bedeutung: "Dieser innere Gedanke fühlt eine tragende Konsequenzspur."

## `reorganization_echo`

- Bereich: `0.0 - 1.0`
- Ebene: Thought-Seed / Reorganisationsnachhall
- Funktion: Nachhall aus vorherigem Reorganisationsbedarf, Pain-Memory,
  Burden-Spuren, Memory-Konflikt und Regime-Mismatch.
- Bedeutung: "Dieser innere Gedanke trägt Lernspannung oder Belastung."

## `thought_consequence_alignment`

- Bereich: `0.0 - 1.0`
- Ebene: Thought-Seed / Selbstwahrnehmung der Konsequenz
- Funktion: verbindet Gedankenreife, Realitätsbindung, Strukturdeutung und
  Konsequenz-Echo.
- Bedeutung: "Passt das, was DIO dachte, zu dem, was die Konsequenzspur im
  Feld hinterlassen hat?"

## `thought_consequence_balance`

- Bereich: `-1.0 - 1.0`
- Ebene: Thought-Seed / Echo-Trennung
- Funktion: Differenz zwischen konstruktivem Konsequenz-Echo und
  Reorganisations-Echo.
- Bedeutung: "Überwiegt tragender Nachhall oder Lern-/Belastungsnachhall?"

## `thought_reality_lag`

- Bereich: `0.0 - 1.0`
- Ebene: Thought-Seed / Innen-Außen-Synchronisation
- Funktion: misst, ob die äußere Strukturdeutung weiter ist als die innere
  Benennung des Gedankenkeims.
- Bedeutung: "DIO sieht außen mehr, als er innen schon sicher benennen kann."

## `thought_structural_grounding`

- Bereich: `0.0 - 1.0`
- Ebene: Thought-Seed / strukturelle Erdung
- Funktion: misst, ob ein Gedankenkeim durch Raumzeit-Fit, Realitätskontakt,
  Entry-Tragfähigkeit, Formstabilität, Memory-Support und Feldklarheit geerdet
  ist.
- Bedeutung: "Dieser Gedanke steht auf tragender Struktur oder hängt noch in
  offener Deutung."

## `thought_open_hypothesis_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Thought-Seed / offene Hypothese
- Funktion: misst Druck aus hoher Attraktivität, hoher Strukturlesung, aber
  fehlender Erdung, Reorganisationsnachhall, Lag und Hemmung.
- Bedeutung: "Diese Idee wirkt groß, ist aber innerlich noch nicht genügend
  geerdet."

## `open_hypothesis_learning_state`

- Ebene: Outcome / Reifespur offener Hypothesen
- Mögliche Werte:
  - `open_hypothesis_carried`
  - `open_hypothesis_burdened`
  - `open_hypothesis_reorganizing`
- Funktion: ordnet eine offene Strukturhypothese nach ihrer späteren
  Konsequenz ein.
- Bedeutung: "Diese offene Idee hat getragen, belastet oder braucht
  Reorganisation."

## `open_hypothesis_consequence_score`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / tragende Konsequenz
- Funktion: misst, wie stark eine offene Hypothese nachträglich konstruktiv
  bestätigt wurde.
- Bedeutung: "Diese offene Idee war nicht nur attraktiv, sie wurde getragen."

## `open_hypothesis_burden_score`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / belastende Konsequenz
- Funktion: misst, wie stark eine offene Hypothese Belastung, Verlust oder
  Überforderung erzeugt hat.
- Bedeutung: "Diese offene Idee hat mein Feld belastet."

## `open_hypothesis_reorganization_score`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Reorganisation
- Funktion: misst, wie stark eine offene Hypothese nicht einfach gut oder
  schlecht war, sondern innere Neuordnung verlangt.
- Bedeutung: "Diese offene Idee muss anders verstanden werden."

## `open_hypothesis_replay_need`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Reorganisationsbedarf
- Funktion: misst, ob eine offene Hypothese rückblickend replayt werden sollte,
  weil Lag, Druck, fehlende Erdung oder unklare Bestätigung sichtbar wurden.
- Bedeutung: "Diese Idee sollte noch einmal innerlich durchlaufen werden."

## `open_hypothesis_distance_need`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Schutzabstand
- Funktion: misst, ob eine offene Hypothese Abstand vom direkten
  Handlungsdruck braucht.
- Bedeutung: "Diese Idee war zu nah am Druck und braucht Abstand."

## `open_hypothesis_reinterpretation_need`

- Bereich: `0.0 - 1.0`
- Ebene: Outcome / Neudeutung
- Funktion: misst, ob eine offene Hypothese nicht nur wiederholt, sondern
  anders verstanden werden sollte.
- Bedeutung: "Diese Idee braucht eine neue innere Deutung."

## `open_hypothesis_reorganization_posture`

- Ebene: Outcome / Reorganisationshaltung
- Mögliche Werte:
  - `reinterpretation_dominant`
  - `distance_dominant`
  - `replay_dominant`
  - `low_reorganization_need`
- Funktion: benennt, welche innere Verarbeitung bei einer offenen Hypothese
  dominiert.
- Bedeutung: "Diese offene Idee braucht vor allem Neudeutung, Abstand, Replay
  oder nur geringe Reorganisation."

---

# Noch Zu Dokumentieren

- `form_symbol_anchor`
- `mcm_field_anchor`
- `experience_memory_anchor`
- `outcome_anchor`
- `nervous_variance`
- `regulation_oscillation`
- `recovery_after_stress`
- `stress_to_recovery_delta`
- terrain/path-texture-Sense, falls umgesetzt
# Neue Variablen - Thought-Seed-Reifung offener Hypothesen

## `thought_replay_maturation_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Thought Seed / innere Reifung
- Funktion: misst, ob eine vorherige offene Hypothese als getragene Spur
  wieder innerlich durchlaufen und vertieft werden kann.
- Bedeutung: "Dieser Gedanke hat getragen; ich darf ihn noch einmal
  betrachten und verdichten."

## `thought_distance_maturation_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Thought Seed / Schutzabstand
- Funktion: misst, ob eine offene Hypothese Abstand vom direkten
  Handlungsdruck braucht.
- Bedeutung: "Dieser Gedanke war zu nah am Druck; ich brauche Abstand."

## `thought_reinterpretation_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Thought Seed / Neudeutung
- Funktion: misst, ob eine offene Hypothese nicht wiederholt, sondern anders
  verstanden werden sollte.
- Bedeutung: "Diese Struktur muss ich neu deuten, bevor ich ihr vertraue."

## `thought_reifung_direction`

- Ebene: Thought Seed / Reiferichtung
- Moegliche Werte:
  - `replay_maturation`
  - `distance_maturation`
  - `reinterpretation_maturation`
  - `no_previous_open_hypothesis_trace`
- Funktion: benennt die dominante innere Verarbeitung der vorherigen offenen
  Hypothese.
- Bedeutung: "Mein letzter offener Gedanke erzeugt jetzt Replay, Abstand oder
  Neudeutung."

## `previous_open_hypothesis_learning_state`

- Ebene: Meta-Regulation / Konsequenzgedaechtnis
- Funktion: fuehrt die letzte Outcome-Einordnung einer offenen Hypothese in die
  laufende Meta-Regulation zurueck.
- Bedeutung: "Ich erinnere, ob die letzte offene Idee getragen, belastet oder
  Reorganisation verlangt hat."

## `previous_open_hypothesis_reorganization_posture`

- Ebene: Meta-Regulation / Konsequenzgedaechtnis
- Funktion: fuehrt die dominante Reorganisationshaltung der letzten offenen
  Hypothese in die Thought-Seed-Schicht zurueck.
- Bedeutung: "Meine letzte offene Idee braucht eher Replay, Abstand oder
  Neudeutung."

---
# Variablen - Selbst/Fremd-Differenz

## `borrowed_open_hypothesis_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Thought Seed / semantische Reifung
- Funktion: misst, ob eine offene Strukturhypothese auf geliehener Analogie
  statt eigener Feldbindung ruht.
- Wirkung: erhöht weich Neudeutung und Distanz, ohne Handlung hart zu
  sperren.
- Bedeutung: "Diese offene Idee klingt nach Form, gehört aber noch nicht
  genug zu mir."

## `own_field_binding_pull`

- Bereich: `0.0 - 1.0`
- Ebene: Thought Seed / eigene Feldbindung
- Funktion: misst den stabilisierenden Gegenzug aus eigener MCM-Lage,
  Grenzklarheit, Formvertrauen und Memory-Support.
- Wirkung: dämpft geliehene Deutung und stärkt Reife, wenn eine Deutung
  eigener wird.
- Bedeutung: "Diese Deutung bekommt mehr eigene Feldbindung."

## `own_field_identity_strength`

- Bereich: `0.0 - 1.0`
- Ebene: Meta-Regulation / Selbst-Feld
- Funktion: misst, wie stark eine aktuelle Deutung aus eigener MCM-Lage,
  eigener Erfahrung, innerer Kohärenz und stabiler Selbstverortung getragen
  wird.
- Bedeutung: "Diese Deutung wirkt aus meinem eigenen Feld heraus."

## `foreign_semantic_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Meta-Regulation / Fremddruck
- Funktion: misst, wie stark äußere Reize, Semantikverschiebung, unbekannte
  Form und Orientierungslücke auf die Deutung drücken.
- Bedeutung: "Diese Deutung könnte stärker von außen oder vom Fremden gezogen
  sein."

## `adopted_language_pressure`

- Bereich: `0.0 - 1.0`
- Ebene: Meta-Regulation / übernommene Sprache
- Funktion: misst, ob eine Bezeichnung/Analogie zu früh übernommen wird,
  obwohl die eigene Formsemantik noch unreif ist.
- Bedeutung: "Ich benutze vielleicht ein Wort, bevor es wirklich aus meiner
  eigenen Feldlage entstanden ist."

## `self_foreign_boundary_clarity`

- Bereich: `0.0 - 1.0`
- Ebene: Meta-Regulation / Selbst-Fremd-Grenze
- Funktion: misst, wie klar DIO zwischen eigenem Feld, äußerem Reiz,
  Erinnerung und fremder Analogie unterscheiden kann.
- Bedeutung: "Ich erkenne besser, was zu meiner Innenlage gehört und was von
  außen wirkt."

## `semantic_origin_conflict`

- Bereich: `0.0 - 1.0`
- Ebene: Meta-Regulation / Herkunftskonflikt
- Funktion: misst die Spannung, wenn eine Deutung aktiv ist, ihre Herkunft aber
  unklar bleibt.
- Bedeutung: "Ich bin mir nicht sicher, ob diese Deutung aus mir, aus dem Reiz
  oder aus übernommener Sprache stammt."

## `semantic_origin_state`

- Ebene: Meta-Regulation / semantische Herkunft
- Mögliche Werte:
  - `own_field_origin`
  - `borrowed_analogy_watch`
  - `mixed_translation_zone`
  - `differentiated_contact`
  - `unlocated_semantic_contact`
- Funktion: benennt die aktuelle Herkunftslage einer Deutung.
- Bedeutung: "Diese Deutung ist eigen, fremd, gemischt, differenziert oder
  noch nicht sauber verortet."

## `own_vs_foreign_margin`

- Bereich: `-1.0 - 1.0`
- Ebene: Meta-Regulation / relative Herkunft
- Funktion: beschreibt den Abstand zwischen eigener Feldherkunft und
  Fremddruck.
- Bedeutung: "Ist diese Deutung eher mein Feld oder eher fremder Druck?"

## `borrowed_vs_own_margin`

- Bereich: `-1.0 - 1.0`
- Ebene: Meta-Regulation / übernommene Sprache
- Funktion: beschreibt, ob geliehene Analogie stärker wirkt als eigene
  Feldherkunft.
- Bedeutung: "Übernimmt DIO gerade eher eine fremde Sprache, als aus eigener
  Lage zu benennen?"

## `boundary_support_margin`

- Bereich: `-1.0 - 1.0`
- Ebene: Meta-Regulation / Grenztragfähigkeit
- Funktion: beschreibt, ob Selbst/Fremd-Grenzklarheit den aktuellen
  Herkunftskonflikt tragen kann.
- Bedeutung: "Kann DIO die Herkunft dieser Deutung klar genug unterscheiden?"

---
# Offene Hypothesenreifung

Diese Variablen gehoeren zur inneren Reifung offener Strukturhypothesen. Sie
sind keine harten Regeln, sondern eine MCM-nahe Trennung von Bestaetigung,
Lernspannung, Handlungserlaubnis und Realitaetspruefung.

| Variable | Bedeutung |
|---|---|
| `open_hypothesis_confirmation_weight` | Gewicht, mit dem eine offene Hypothese als bestaetigte, tragende Erfahrung nachklingt. |
| `open_hypothesis_learning_charge` | Lern- und Reorganisationsladung einer Hypothese. Hoch bedeutet nicht automatisch schlecht, sondern unreif / umzudeuten. |
| `open_hypothesis_action_permission` | Weiche Handlungserlaubnis aus Hypothesenbestaetigung, Feldsupport, Struktur und innerer Lage. |
| `open_hypothesis_reality_check_need` | Bedarf, die Hypothese erst mit Abstand, Replay oder Reflexion gegen die aktuelle Realitaet zu pruefen. |

Neurologisch gelesen:

- bestaetigte Hypothese -> Vertrauen, Replay, vorsichtige Handlungshoehe
- belastete Hypothese -> Abstand, Vorsicht, Schutz
- reorganisierende Hypothese -> Lernspannung, Realitaetscheck, Reframing

---

# Gedanken-Verdauung / innere Nachverarbeitung

Diese Variablen gehoeren zur getrennten Gedanken-Memory
`mcm_thought_memory.json`. Sie beschreiben nicht direkt Entry oder Exit,
sondern wie DIO offene Hypothesen innerlich nachverarbeitet.

| Variable | Bedeutung |
|---|---|
| `thought_digestive_replay_pull` | Bedarf, eine offene Hypothese innerlich noch einmal durchzuspielen. |
| `thought_digestive_distance_pull` | Bedarf, Abstand zur Hypothese zu gewinnen, bevor sie motorisch wirkt. |
| `thought_digestive_integration_pull` | Bedarf, Hypothese, Feldlage, Realitaetsbindung und Erfahrung neu zusammenzufuehren. |
| `thought_digestive_returned_trust` | Rueckkehr von Vertrauen nach Replay / Integration / Konsequenzkontakt. |
| `trust_return_readiness` | Weiche Bereitschaft, dass Vertrauen trotz laufendem Replay/Abstand wieder tragfaehig wird. |
| `thought_digest_state` | Lesbarer Zustand der inneren Verdauung. |

Moegliche `thought_digest_state`-Werte:

- `digestive_quiet`
- `digestive_replay`
- `digestive_distance`
- `digestive_integration`
- `digestive_trust_emergence`
- `digestive_trust_return`

Neurologisch gelesen:
Diese Schicht ist eine weiche Verbindung aus hippocampalem Replay,
praefrontaler Distanzierung und limbischer Rueckkopplung. DIO bekommt damit
nicht gesagt, was er tun muss. Er bekommt nur die Faehigkeit, einen Gedanken
weiterzutragen, zu pruefen, zu integrieren oder nach gereifter Bestaetigung
wieder Vertrauen in ihn zu finden.

---

# Trust-Return / Motorische Entkopplung

Diese Variablen gehoeren zur Meta-Regulation zwischen innerer
Gedanken-Verdauung und Handlungsmotorik. Sie verhindern keine Handlung hart,
sondern machen sichtbar, ob zurueckkehrendes Vertrauen bereits motorisch
tragfaehig ist oder erst fokussiert und stabilisiert werden muss.

| Variable | Bedeutung |
|---|---|
| `previous_digest_state` | Nachhall des vorherigen Gedanken-Verdauungszustands. |
| `previous_trust_return_readiness` | vorherige Bereitschaft, dass Vertrauen aus einem Gedanken wieder tragfaehig wird. |
| `previous_digestive_returned_trust` | vorheriger Wert der tatsaechlichen Vertrauensrueckkehr. |
| `previous_emergent_structure_state` | vorherige emergente Strukturlesung, damit bestaetigte Struktur nicht blind gebremst wird. |
| `previous_confirmed_structure_protection` | Schutzwert fuer bereits bestaetigte Strukturdeutung. |
| `trust_return_open_hypothesis_load` | offene Hypothesenlast, die zeigt, ob Trust-Return noch an unreife, belastete oder reorganisierende Hypothesen gekoppelt ist. |
| `trust_return_context_instability` | Kontextinstabilität aus Innen/Außen-Unschärfe, geringer Distanz, Cortisol, nervlicher Überlastung und Feldstrain. |
| `trust_return_motor_contact_strength` | Stärke, mit der zurückkehrendes Vertrauen aktuell motorische Nähe bekommt. |
| `trust_return_act_bridge` | weiche Brücke, ob Trust-Stabilisierung eine geplante Handlung kurz in `act_watch` oder Replay verschieben darf. |
| `trust_return_motor_heat` | nervliche Hitze, wenn Vertrauen, Cortisol, Handlungsdruck und offene Hypothese gleichzeitig aktiv sind. |
| `trust_return_stabilization_need` | Bedarf, zurueckkehrendes Vertrauen erst zu stabilisieren, bevor es direkt motorisch wirkt. |
| `trust_return_focus_pull` | Zug, den Gedanken bewusst zu fokussieren, statt ihn reflexhaft in Handlung zu entladen. |
| `trust_return_motor_mode` | lesbarer Zustand der Trust-Return-Motorik. |

Moegliche `trust_return_motor_mode`-Werte:

- `trust_quiet`
- `trust_emerging`
- `trust_focused_ready`
- `trust_stabilize_before_act`

Neurologisch gelesen:
Diese Schicht wirkt wie ein praefrontaler Puffer zwischen limbischer
Vertrauensrueckkehr und motorischem Impuls. DIO kann merken: "Der Gedanke
kommt zurueck und fuehlt sich tragender an, aber mein Nervensystem ist noch
angespannt." Dann wird daraus nicht automatisch ein Trade, sondern zunaechst
Fokus, Replay, Beobachtung oder Stabilisierung.

Nach Lauf 17 wurde diese Schicht organischer gespeist: nicht nur Cortisol und
Trust-Return wirken hinein, sondern auch offene Hypothesenlast,
Innen/Außen-Unschärfe, zu geringe Distanz und nervliche Überlastung. Dadurch
kann DIO einen Gedanken halten, wenn Vertrauen zurückkehrt, die innere Lage
aber noch nicht stabil genug ist.

Nach Lauf 18 wurde die Motorik-Schnittstelle feiner angebunden:
`trust_return_motor_contact_strength` und `trust_return_act_bridge` machen
sichtbar, ob aus Trust-Return ein handlungsnaher Zwischenraum entstehen darf.
Gleichzeitig schützt `previous_confirmed_structure_protection` bestätigte
Strukturdeutungen, damit reife Form nicht unnötig ausgebremst wird.

MCM-Bedeutung:
Vertrauen ist keine Pflicht zur Handlung. Es ist eine Feldinformation. Erst
wenn Innenlage, Aussenkontakt, Raumzeit-Fit und Nervensystem gemeinsam
tragfaehig wirken, darf Vertrauen natuerlich mehr Handlungskraft bekommen.

---

# AKTUELLER_STAND

# Fix - Thought-Memory Windows-Dateilock

Problem:
Beim Schreiben von `bot_memory/mcm_thought_memory.json` konnte Windows die
temporäre Datei zeitweise nicht atomar auf die Zieldatei ersetzen:
`PermissionError [WinError 5]`.

Ursache:
Kein Brain-Logikfehler, sondern ein Dateilock beim Ersetzen der JSON-Datei.
Das kann passieren, wenn Windows, ein Editor, Virenscanner oder ein zweiter
Python-Prozess die Datei kurz hält.

Umsetzung:

- neue robuste Schreibfunktion `_write_text_atomic_with_retry`
- eindeutige Temp-Datei pro Schreibversuch
- Flush und `fsync` vor dem Ersetzen
- mehrere kurze Retry-Versuche bei `PermissionError`
- Fehler wird protokolliert, aber nicht mehr als Lauf-Crash nach außen
  geworfen
- Thought-Memory bleibt bei fehlgeschlagenem Schreiben dirty und versucht es
  später erneut
- Formsymbol-Memory nutzt dieselbe robuste Schreiblogik

Hinweis:
Aktuell laufen noch Python-Prozesse. Der bereits laufende Prozess hat diesen
Fix nicht geladen. Für den nächsten Lauf Bot stoppen und neu starten.

# Debugstruktur - neue Laufordner-Aufteilung

Umgesetzt:
Die Debug-Ausgabe wird pro Lauf automatisch in fachliche Unterordner
sortiert. Die Aufrufer können weiterhin alte Pfade wie `debug/trade_stats.json`
oder `dbr_path("mcm_field_decision_protocol.csv")` verwenden. Die Sortierung
passiert zentral im `debug_reader`.

Neue Struktur je Lauf:

- `gui/`: `trade_stats.json`, `trade_equity.csv`
- `core/`: Feldentscheidung, Outcome, Thought-Seed, Neurotransition
- `language/`: Formsymbol-, Thought-/Memory- und Idle-Denkprotokolle
- `perception/`: visuelles Sehen, strategisches Fenster, aktive Kontakte,
  Zielerwartung
- `position/`: Positionslast und Exit-Kandidaten
- `performance/`: Laufzeit- und Schreibprofile
- `research/`: sonstige Forschungs-/Rohdiagnose

Technisch:

- `Config.DEBUG_GROUPED_DIRS = True`
- automatische Gruppierung in `debug_reader.dbr_path`
- automatische Gruppierung in `debug_reader.dbr_resolve_path`
- `trade_equity.csv` bleibt weiterhin ungepuffert, damit GUI/Verlauf live
  lesbar bleibt

Wichtig:
Das verändert nicht die Brain-Mechanik. Es verändert nur die Ablage der
Debug-Dateien. Der nächste echte Lauf startet weiter bei `debug_lauf_1`.

# Neustartpunkt - neue Memory und neue Debugs

Status:
Vor dem nächsten Lauf wurde ein sauberer Neustartpunkt gesetzt.

Gesichert:

- alte aktive Memory nach
  `bot_memory/archiv_vor_dio_form_language_core_20260522_175156`
- alte Debugläufe nach
  `debug_archive/vor_dio_form_language_core_20260522_175156`

Aktiver Zustand:

- `bot_memory/memory_state.json` ist aus dem aktiven Pfad entfernt
- `bot_memory/form_symbol_memory.json` ist aus dem aktiven Pfad entfernt
- `bot_memory/mcm_thought_memory.json` ist aus dem aktiven Pfad entfernt
- `debug/` ist leer und bereit für neue `debug_lauf_*`

Bedeutung:
Der nächste Lauf baut Welt-Erfahrung, Formsymbol-Erfahrung und
Gedanken-Erfahrung neu auf. Damit kann geprüft werden, ob der neue
`DIO_FORM_LANGUAGE_CORE`, die getrennten Erfahrungsanker und die
Dialogbrücke von Anfang an sauber eigene Satzfamilien bilden.

Wie es weitergeht:
Nächsten Lauf als neuen Lauf 1 starten und danach besonders prüfen:

- entstehen neue `memory_state.json`, `form_symbol_memory.json` und
  `mcm_thought_memory.json`?
- entstehen neue `debug_lauf_*` im leeren Debugordner?
- werden `dio_world_experience_anchor`,
  `dio_thought_experience_anchor` und `dio_dialogue_bridge_sentence`
  geschrieben?

# Mechanikvermerk - DIO Form Language Core

Umgesetzt:
DIO hat jetzt eine zentrale innere Sprach-Integrationsschicht:
`_build_dio_form_language_state`.

Funktion:
Die Schicht verbindet Formsymbol, Compound-Form, MCM-Feldanker,
Thought-Seed, Strukturdeutung, semantische Herkunft, Reifung,
Handlungslage, Phase und Kontext zu einer einheitlichen DIO-Syntax.

Neue Werte:

- `dio_syntax_signature`
- `dio_language_sentence`
- `dio_language_state`
- `dio_syntax_origin`
- `dio_syntax_density`
- `dio_syntax_compression`
- `dio_syntax_coherence`

Speicherung:
Die Syntax wird in der Thought-Memory mitgeführt. Seeds und Thought-Families
tragen damit nicht nur Rohwerte, sondern auch eine innere Satzspur.

Erweiterung:
Die Trennung zwischen weltlicher Erfahrung und Gedankenerfahrung ist jetzt in
der DIO-Syntax ausdrücklich markiert.

- `dio_world_experience_anchor`: Bezug zur weltlichen Erfahrungsspur
  (`memory_state`, Kontextcluster, Outcome).
- `dio_thought_experience_anchor`: Bezug zur inneren Gedanken- und
  Hypothesenspur (`mcm_thought_memory`, Thought-Family).
- `dio_dialogue_bridge_sentence`: verdichtete Brücke zwischen Fühlen,
  Weltgedächtnis, Gedankengedächtnis, Hypothese, Variante, Tragfähigkeit und
  Handlung.

Beispielhafte Lesart:
"Ich fühle Form X. In meiner weltlichen Erfahrung liegt dazu Kontext Y. In
meiner Gedankenspur gehört es zu Familie Z. Die mögliche Folge ist eine offene
Variante. Ich beobachte, was tragfähig wird."

Wichtig:
Das ist kein menschliches Sprachlabel und keine Trading-Regel. Es ist eine
Brückenschicht, damit DIO seine Welt konsistenter in eigener Formsprache
bindet. Menschliche Begriffe bleiben nur Lesebrücke von außen.

Wie es weitergeht:
Im nächsten Lauf prüfen, ob die neue Syntax homogen entsteht:

- bilden sich wiederkehrende `dio_syntax_signature`?
- werden Familien durch gleiche Syntax stabiler?
- steigt `dio_syntax_compression`, ohne dass DIO blind wird?
- passt `dio_syntax_origin` zu `semantic_origin_state`?

# Mechanikvermerk - historische Entscheidungsgewichtung

Festgehalten:
Alles, was bei DIO mit Entscheidung und Handlung zu tun hat, darf nicht nur
aus dem aktuellen Momentreiz bewertet werden. Eine Handlung ist im MCM-Sinn
eine getragene Erfahrungsspur:

- nicht nur: "Ist das gerade gut?"
- sondern: "Wie gut hat diese Art von Entscheidung in der Vergangenheit
  getragen?"

Stand der Umsetzung:
Die Mechanik ist teilweise bereits vorhanden, aber noch nicht als einheitliche
Schicht geschlossen.

Bereits vorhanden:

- Formgedächtnis mit `form_symbol_learning_trust`,
  `form_symbol_action_trust`, `form_symbol_caution_trust`,
  `form_symbol_contact_maturity`, `form_symbol_contact_utility` und
  `form_symbol_contact_pain_memory`.
- Kontextcluster mit historischer Qualität, Bias, Distanz, Varianz und
  `bearing_effect`.
- Beobachtungsreife über `observation_learning` und
  `observation_maturity_trust`.
- offene Hypothesen-Lernzustände über `open_hypothesis_carried`,
  `open_hypothesis_burdened` und `open_hypothesis_reorganizing`.
- Thought-Seeds und Thought-Families als beginnende innere Gedächtnisspur.

Noch offen:

- eine saubere persistente Hypothesen-/Handlungsgewichtung, die
  Entscheidungsfamilien über Zeit trägt
- weiche Rezeptorwirkung auf Motorik, Reflexion, Replay und Distanzierung
- kein harter Block, sondern Reifung durch Bestätigung, Belastung,
  Reorganisation und Vergessen

Umgesetzt:
Die zu breite Hypothesen-Reifeschicht wurde in eine weichere historische
Gewichtung umgebaut. Neu sichtbar sind:

- `open_hypothesis_trace_strength`
- `hypothesis_weight`
- `hypothesis_trust`
- `hypothesis_caution`
- `hypothesis_reorganization_weight`
- `action_weight`
- `decision_weight`

Wirkung:
Getragene Hypothesen stärken jetzt eher Feldvertrauen, Handlungsgewicht und
Mut. Belastete Hypothesen erzeugen Vorsicht, aber deutlich weniger
Handbremse. Reorganisierende Hypothesen ziehen stärker in Replay und
Neudeutung, statt breite Motorik-Hemmung auszulösen.

Nächster sinnvoller Schritt:
Im nächsten Lauf prüfen, ob die offene Hypothesenlast weniger als starre
Hemmung wirkt und ob `ordinary_structure_reading` wieder tragfähiger wird,
ohne `open_hypothesis_reorganizing` als blinden Handlungsdruck zu behandeln.

# Auswertung - Lauf 65 nach Hypothesen-Reifeschicht

Status:
Ausgewertet.

Kerndaten:

- Netto-PnL: ca. `+30.19`
- Trades: `370`
- TP/SL: `159 / 211`
- Winrate: ca. `42.97 %`
- Profit Factor: ca. `1.26`
- Expectancy: ca. `+0.082`
- Max Drawdown: ca. `11.24 %`
- Attempts: `10625`
- Debuggröße: ca. `33.54 MB`
- `trade_equity.csv`: `370` Equity-Zeilen, wird geschrieben.

Befund:
Die Reifeschicht hat DIO nicht zerstört, aber deutlich gebremst. Gegen Lauf 64
und den vorherigen Lauf 65 ist der PnL schwächer und der Drawdown höher.

Vergleich:

- Lauf 64: PnL ca. `+52.14`, DD ca. `6.54 %`
- Lauf 65 vorher: PnL ca. `+44.88`, DD ca. `9.09 %`
- Lauf 65 nach Reifeschicht: PnL ca. `+30.19`, DD ca. `11.24 %`

Emergente Struktur:

- `confirmed_structural_interpretation`:
  - `58 TP / 0 SL`
  - PnL ca. `+58.21`
  - bleibt extrem tragfähig
- `open_structural_hypothesis`:
  - `26 TP / 134 SL`
  - PnL ca. `-32.74`
- `ordinary_structure_reading`:
  - PnL ca. `+7.59`
  - deutlich schwächer als vorher
- `wide_target_without_structure`:
  - PnL ca. `-2.87`

Open-Hypothesis-Learning:

- `open_hypothesis_carried`:
  - `26 TP / 0 SL`
  - PnL ca. `+25.58`
- `open_hypothesis_burdened`:
  - `0 TP / 15 SL`
  - PnL ca. `-6.64`
- `open_hypothesis_reorganizing`:
  - `0 TP / 119 SL`
  - PnL ca. `-51.67`

Phasenbild:

- `observe`: `3650`
- `hold`: `3304`
- `act_watch`: `1229`
- `act`: `417`
- `replan`: `6`

Deutung:
Die Richtung der Mechanik ist richtig, aber die Wirkung ist zu früh bzw. zu
breit. DIO bremst nicht nur unreife offene Hypothesen, sondern verliert auch
Handlungsklarheit in normalen Strukturlesungen. Die Reifeschicht wirkt aktuell
eher wie eine angezogene Handbremse als wie ein selektiver präfrontaler Filter.

Wichtig:
`confirmed_structural_interpretation` bleibt unverändert stark. Das zeigt, dass
die Kernstrukturdeutung weiter funktioniert. Die Last liegt in der
Differenzierung zwischen offener, getragener und reorganisierender Hypothese.

Wie es weitergeht:
Die Reifeschicht sollte weicher und selektiver werden:

- getragene offene Hypothesen stärker schützen
- normale Strukturlesung weniger mitbremsen
- reorganisierende Hypothese nicht pauschal hemmen, sondern eher in
  `act_watch`, Replay und Distanzierung führen
- neue Reifungswerte im Feldentscheidungsprotokoll sichtbar machen, weil sie
  aktuell in `mcm_field_decision_protocol.csv` noch nicht als eigene Spalten
  auftauchen

---

# Trust-Return von direkter Motorik weicher entkoppelt

Status:
Umgesetzt und kompiliert.

Technische Pruefung:
`python -m py_compile .\MCM_Brain_Modell.py .\bot.py .\trade_stats.py .\debug_reader.py .\config.py`
lief erfolgreich durch.

Was neu ist:
Die Rueckkehr von Vertrauen wird jetzt nicht mehr automatisch als direkte
Handlungskraft gelesen, wenn das Nervensystem noch geladen ist.

Neue Meta-Werte:

- `previous_digest_state`
- `previous_trust_return_readiness`
- `previous_digestive_returned_trust`
- `trust_return_motor_heat`
- `trust_return_stabilization_need`
- `trust_return_focus_pull`
- `trust_return_motor_mode`

Moegliche `trust_return_motor_mode`-Zustaende:

- `trust_quiet`
- `trust_emerging`
- `trust_focused_ready`
- `trust_stabilize_before_act`

Mechanik:
Wenn im vorigen Gedankenkeim `digestive_trust_emergence` oder
`digestive_trust_return` sichtbar war, prueft DIO im naechsten Meta-Zyklus, ob
dieses Vertrauen mit Cortisol, Action-Permission und innerer Distanz schon
tragfaehig gekoppelt ist.

Wenn Vertrauen zurueckkommt, aber Cortisol noch erhoeht ist, wird aus direktem
`act` eher `act_watch` oder `replan`. Das ist keine Sperre, sondern eine
Stabilisierungsbewegung:

"Ich erkenne das wieder, aber mein Nervensystem ist noch geladen. Ich halte den
Gedanken, fokussiere ihn oder spiele ihn noch einmal durch."

Debug:
`core/mcm_thought_digest_protocol.csv` schreibt die neuen Trust-Motorik-Werte
mit.

Neurologisch gelesen:
Das ist eine weichere Trennung zwischen Vertrauen und Impuls. Vertrauen darf
entstehen, ohne sofort Bewegung zu werden. Erst wenn Vertrauen und Nervensystem
zusammen tragfaehiger wirken, kann daraus natuerlich mehr Handlungskraft
entstehen.

Wie es weitergeht:
Im naechsten Lauf pruefen wir:

- wie oft `trust_stabilize_before_act` entsteht
- ob dadurch `digestive_trust_emergence` weniger direkt in `act` kippt
- ob Cortisol bei Trust-Return-Lagen sinkt
- ob PnL-Verlauf und Drawdown ruhiger werden

---

# Lauf 14 bis Lauf 16 nach Trust-Return ausgewertet

Status:
Ausgewertet.

Debug:

- `debug/debug_lauf_14`
- `debug/debug_lauf_15`
- `debug/debug_lauf_16`

Ergebnisse:

| Lauf | Netto-PnL | Trades | TP / SL | Long-PnL | Short-PnL | Max-DD |
|---|---:|---:|---:|---:|---:|---:|
| 14 | ca. `+22.31` | `344` | `142 / 202` | ca. `-0.15` | ca. `+22.46` | ca. `12.71 %` |
| 15 | ca. `+14.33` | `362` | `143 / 219` | ca. `+0.04` | ca. `+14.30` | ca. `18.40 %` |
| 16 | ca. `+32.74` | `377` | `161 / 216` | ca. `+6.12` | ca. `+26.62` | ca. `9.29 %` |

Trust-Return-Zustaende:

| Lauf | `digestive_trust_emergence` | `digestive_trust_return` |
|---|---:|---:|
| 14 | `39` | `5` |
| 15 | `31` | `3` |
| 16 | `34` | `3` |

Digest-Verteilung:

- Lauf 14:
  - `digestive_quiet`: `6359`
  - `digestive_replay`: `3980`
  - `digestive_distance`: `690`
- Lauf 15:
  - `digestive_quiet`: `5991`
  - `digestive_replay`: `3767`
  - `digestive_distance`: `730`
- Lauf 16:
  - `digestive_quiet`: `5926`
  - `digestive_replay`: `3609`
  - `digestive_distance`: `568`

Wichtig:
Die neue Trust-Schicht funktioniert. `digestive_trust_emergence` taucht in
allen drei Laeufen auf, und auch `digestive_trust_return` erscheint jetzt
erstmals als eigener Zustand.

Deutung:
Trust-Return entsteht fast immer aus:

- `open_hypothesis_carried_memory`
- `replay_maturation`

Das ist fachlich gut: Vertrauen kommt nicht aus blinder Hoffnung, sondern aus
einer bereits getragenen Erinnerungsspur, die durch Replay wieder reaktiviert
wird.

Kritischer Punkt:
Trust-Return liegt haeufig direkt in `act`. Gleichzeitig ist Cortisol bei
`digestive_trust_emergence` und `digestive_trust_return` nicht niedrig, sondern
oft sogar leicht erhoeht. Das bedeutet:
DIO bekommt Vertrauen zurueck, aber sein Nervensystem ist dabei noch nicht ganz
beruhigt.

Neurologisch gelesen:
Das wirkt wie ein Mensch, der sagt: "Ich erkenne das wieder, ich vertraue dem
Muster", aber der Koerper ist noch angespannt. Vertrauen ist also vorhanden,
aber noch motorisch geladen. Das ist keine Fehlfunktion, sondern ein naechster
Reifepunkt: Vertrauen muss nicht automatisch Handlung bedeuten, sondern kann
auch erst Stabilisierung und ruhige Fokussierung bedeuten.

Wie es weitergeht:
Als naechstes sollte `digestive_trust_emergence` staerker als innere
Stabilisierung gelesen werden, nicht sofort als motorischer Mut. Keine Sperre:
Wenn Vertrauen zurueckkommt, aber Cortisol noch hoch ist, sollte DIO dieses
Vertrauen erst halten, fokussieren oder weiter replayen koennen. Erst wenn
Vertrauen und Nervensystem zusammen tragfaehig sind, darf daraus organischer
Handlungsdruck entstehen.

---

# Trust-Return-Vorstufe umgesetzt

Status:
Umgesetzt und kompiliert.

Technische Pruefung:
`python -m py_compile .\MCM_Brain_Modell.py .\bot.py .\trade_stats.py .\debug_reader.py .\config.py`
lief erfolgreich durch.

Was geaendert wurde:
Die Rueckkehr von Vertrauen aus einer offenen Hypothese wird jetzt weicher
gelesen. Vorher musste `thought_digestive_returned_trust` groesser als Replay
und Distance sein. Das war zu streng, weil Vertrauen oft waehrend Replay und
Abstand entsteht, nicht erst danach.

Neu:

- `trust_return_readiness`
- `digestive_trust_emergence`

Deutung:

- `digestive_trust_emergence` bedeutet:
  "Vertrauen kehrt als Vorform zurueck, aber die Hypothese ist noch in innerer
  Verarbeitung."
- `digestive_trust_return` bedeutet:
  "Nach Replay / Abstand / Realitaetsbindung ist die Hypothese wieder
  tragfaehiger."

Wichtig:
Das ist keine direkte Handlungserlaubnis. Es veraendert vor allem die innere
Benennung und Memory-Reifung. Eine Hypothese kann jetzt als Rueckkehr von
Vertrauen gespeichert werden, ohne sofort motorisch act werden zu muessen.

Neurologisch gelesen:
Das ist naeher an praefrontaler Rueckkopplung: Ein Gedanke kann sich nach
innerem Replay beruhigen und Vertrauen zurueckbekommen, waehrend das System
ihn noch prueft.

Wie es weitergeht:
Im naechsten Lauf pruefen wir, ob `digestive_trust_emergence` und eventuell
`digestive_trust_return` sichtbar werden. Entscheidend ist, ob diese Zustaende
spaeter mit niedrigerem Cortisol, besserer Action-Permission und tragenderen
Entscheidungen zusammenfallen.

---

# Lauf 13 mit Thought-Digest-Protokoll ausgewertet

Status:
Ausgewertet.

Debug:
`debug/debug_lauf_13`

Ergebnis:

- Netto-PnL: ca. `+35.43`
- Equity: ca. `135.43`
- Trades: `356`
- TP / SL: `151 / 205`
- Long-Trades / Short-Trades: `140 / 216`
- Long-PnL: ca. `+4.09`
- Short-PnL: ca. `+31.34`
- Attempts: `11125`
- Observed / Replanned / Withheld: `2625 / 60 / 2132`
- Equity-Peak: ca. `137.28`
- Max-DD: ca. `7.83 %`

Debug-Struktur:
Die neue schlanke Datei ist aktiv:

`core/mcm_thought_digest_protocol.csv`

Die grosse `mcm_thought_seed_protocol.csv` wurde im Lauf nicht mehr
geschrieben. Damit funktioniert die Debug-Entlastung.

Dateigroessen:

- `mcm_thought_digest_protocol.csv`: ca. `4.98 MB`
- vorherige grosse Thought-Seed-Datei lag eher bei ca. `11 MB`
- weiterhin gross bleiben `mcm_field_decision_protocol.csv` und
  `outcome_records.jsonl`

Thought-Digest-Verteilung:

- `digestive_quiet`: `6280`
- `digestive_replay`: `3776`
- `digestive_distance`: `679`
- `digestive_integration`: `0`
- `digestive_trust_return`: `0`

Open-Hypothesis-Verteilung:

- `open_hypothesis_neutral_memory`: `5574`
- `open_hypothesis_reorganizing_memory`: `4465`
- `open_hypothesis_carried_memory`: `696`

Wichtige Kopplung:

- `open_hypothesis_reorganizing_memory` geht fast vollstaendig in
  `digestive_replay` oder `digestive_distance`.
- `open_hypothesis_carried_memory` bleibt bei `digestive_quiet`, hat aber
  deutlich hoehere `open_hypothesis_action_permission` und hoeheren
  `thought_digestive_returned_trust`.

Mittelwerte:

- `digestive_replay`:
  - Replay ca. `0.346`
  - Distance ca. `0.316`
  - Trust-Return ca. `0.077`
  - Action-Permission ca. `0.032`
- `digestive_distance`:
  - Replay ca. `0.339`
  - Distance ca. `0.347`
  - Trust-Return ca. `0.054`
  - Action-Permission ca. `0.013`
- `open_hypothesis_carried_memory`:
  - Action-Permission ca. `0.300`
  - Trust-Return ca. `0.225`

Deutung:
Das ist ein sehr guter erster Nachweis der neuen Schicht. DIO blockiert offene
Hypothesen nicht hart, sondern reorganisierende Hypothesen werden in Replay und
Abstand verschoben. Carried-Hypothesen duerfen dagegen eher handlungsnah
bleiben.

Neurologisch gelesen:
Das wirkt wie beginnende praefrontale Kontrolle ueber limbische Hypothesen:
"Ich fuehle eine Moeglichkeit, aber wenn sie nicht getragen ist, spiele ich sie
innerlich nach oder nehme Abstand." Noch fehlt die reife Rueckkehr:
`digestive_trust_return` taucht nicht als Zustand auf. Vertrauen ist also als
Vorform sichtbar, aber noch nicht stabil genug, um als eigener Zustand zu
erscheinen.

Wie es weitergeht:
Als naechstes sollte die Verdauungsschicht nicht staerker sperren, sondern die
Schwelle zwischen `digestive_replay`, `digestive_distance` und
`digestive_trust_return` feiner lesen. Besonders interessant sind die 74 Zeilen
mit hohem Trust-Return-Vorwert. Daraus kann DIO lernen, wann eine Hypothese
nach Replay wieder tragfaehig wird.

---

# Schlankes Thought-Digest-Debug umgesetzt

Status:
Umgesetzt und kompiliert.

Technische Pruefung:
`python -m py_compile .\MCM_Brain_Modell.py .\bot.py .\trade_stats.py .\debug_reader.py .\config.py`
lief erfolgreich durch.

Was neu ist:
Es gibt jetzt eine gezielte Debug-Datei:

`core/mcm_thought_digest_protocol.csv`

Diese Datei ersetzt im normalen `DIO_CORE_DEBUG`-Profil die grosse
`mcm_thought_seed_protocol.csv`. Die Gedanken-Memory bleibt aktiv, aber die
Debug-Ausgabe wird deutlich schlanker.

In `DIO_CORE_DEBUG` gilt jetzt:

- `MCM_THOUGHT_SEED_PROTOCOL_DEBUG = False`
- `MCM_THOUGHT_DIGEST_PROTOCOL_DEBUG = True`
- `MCM_THOUGHT_DIGEST_PROTOCOL_EVERY_N = 10`

Die neue Datei schreibt nur die wichtigen Verdauungsachsen:

- `thought_digest_state`
- `thought_reifung_direction`
- `thought_digestive_replay_pull`
- `thought_digestive_distance_pull`
- `thought_digestive_integration_pull`
- `thought_digestive_returned_trust`
- `open_hypothesis_reifung_state`
- `open_hypothesis_confirmation_weight`
- `open_hypothesis_learning_charge`
- `open_hypothesis_action_permission`
- `open_hypothesis_reality_check_need`
- `inner_outer_alignment`
- `cortisol_load`
- `serotonin_stability`
- `dopamine_drive`
- `mcm_axis_state`
- `mcm_axis_tension`

Deutung:
Damit sehen wir im naechsten Lauf nicht mehr nur am Ende im Memory, ob DIO
Gedanken verdaut hat. Wir sehen waehrend des Laufes, wann Replay, Abstand,
Integration oder Rueckkehr von Vertrauen entsteht.

Wie es weitergeht:
Der naechste Lauf kann mit bestehender Erfahrung auf einem anderen Datensatz
laufen. Sinnvoll waere `1-12_2025_5m_SOLUSDT.csv` als naechster Haertetest:
nicht neues Gedaechtnis, sondern Transfer mit vorhandener Erfahrung. Danach
werten wir `core/mcm_thought_digest_protocol.csv` aus.

---

# Lauf 11 und Lauf 12 nach Gedanken-Verdauung geprueft

Status:
Ausgewertet auf Basis der reduzierten Debug-Dateien.

Debug:

- `debug/debug_lauf_11`
- `debug/debug_lauf_12`

Wichtig:
Durch die reduzierte Debug-Ausgabe liegen in den Laufordnern keine vollstaendige
Field-/Thought-Seed-CSV vor. Die Bewertung kommt daher aus `entry_debug.csv`,
`exit_trading_debug.csv`, `value_check_debug.csv`, den Snapshots und dem
aktuellen `mcm_thought_memory.json`.

Sichtbarer Exit-Ausschnitt:

Lauf 11:

- sichtbare Exits: `12`
- TP / SL: `6 / 6`
- sichtbarer PnL-Ausschnitt: ca. `+4.17`
- Long-PnL im Ausschnitt: ca. `+3.87`
- Short-PnL im Ausschnitt: ca. `+0.29`
- Entries: Long `9`, Short `5`
- durchschnittlicher RR aus Value-Gate: ca. `4.10`

Lauf 12:

- sichtbare Exits: `14`
- TP / SL: `6 / 8`
- sichtbarer PnL-Ausschnitt: ca. `+2.53`
- Long-PnL im Ausschnitt: ca. `+1.16`
- Short-PnL im Ausschnitt: ca. `+1.37`
- Entries: Long `7`, Short `9`
- durchschnittlicher RR aus Value-Gate: ca. `3.23`

Innere Lage am End-Snapshot:

- gleicher visueller Formanker: `vf_67ceba8f85`
- beide enden bei `open_hypothesis_reorganizing_memory`
- Lauf 11: Cortisol ca. `0.267`, Action-Permission ca. `0.005`,
  Reality-Check-Need ca. `0.376`
- Lauf 12: Cortisol ca. `0.139`, Action-Permission ca. `0.023`,
  Reality-Check-Need ca. `0.346`

Deutung:
Das ist wahrscheinlich der Grund, warum zwei Laeufe interessant sind. Lauf 12
wirkt nicht einfach besser, sondern anders verarbeitet: DIO sieht am Ende eine
sehr aehnliche Aussenform, aber die innere Stresslage ist niedriger. Die
Reorganisationshypothese bleibt aktiv, doch sie wirkt weniger schmerzhaft und
etwas besser in Handlung/Abstand eingebettet.

Gedanken-Memory nach Lauf 12:

- Seeds: `2048`
- Thought-Families: `768`
- `digestive_quiet`: `390` Seeds / `247` Families
- `digestive_replay`: `153` Seeds / `136` Families
- `digestive_distance`: `27` Families
- `reorganizing_digest_memory_trace`: `131` Seeds

Neurologisch gelesen:
Das sieht nach beginnender innerer Nachverarbeitung aus. DIO bleibt nicht nur
im reflexiven Trade-Zyklus, sondern bildet bereits Replay- und
Distanzspuren. Noch fehlt aber `digestive_trust_return` als klar sichtbarer
Zustand. Vertrauen kommt also noch nicht stabil zurueck, sondern liegt eher als
Vorform unterhalb der Schwelle.

Wie es weitergeht:
Als naechstes sollte das reduzierte Debug-Set um eine gezielte
Thought-Seed-Ausgabe erweitert werden. Nicht wieder alles schreiben, sondern
eine kleine Datei nur fuer `thought_digest_state`, Reifung, Replay, Abstand,
Integration und Trust-Return. Dann sehen wir direkt im Lauf, wann DIO eine
Hypothese verdaut, statt nur im Memory-Endzustand.

---

# Gedanken-Verdauung fuer offene Hypothesen umgesetzt

Status:
Umgesetzt und kompiliert.

Technische Pruefung:
`python -m py_compile .\MCM_Brain_Modell.py .\bot.py .\trade_stats.py`
lief erfolgreich durch.

Was neu ist:
DIO unterscheidet bei offenen Gedankenkeimen jetzt zusaetzlich, ob eine
Hypothese nur reift oder ob sie innerlich verdaut werden muss.

Neue Werte:

- `thought_digestive_replay_pull`
- `thought_digestive_distance_pull`
- `thought_digestive_integration_pull`
- `thought_digestive_returned_trust`
- `thought_digest_state`

Moegliche Verdauungszustaende:

- `digestive_quiet`
- `digestive_replay`
- `digestive_distance`
- `digestive_integration`
- `digestive_trust_return`

Deutung:
Das ist keine Handlungssperre. Eine reorganisierende Hypothese wird nicht
einfach blockiert, sondern bekommt eine innere Nachverarbeitung: Replay,
Abstand, Integration oder Rueckkehr von Vertrauen. Neurologisch entspricht das
eher hippocampalem Replay plus praefrontaler Distanzierung: Der Organismus
rennt nicht blind hinter jedem Gedanken her, sondern laesst ihn im inneren Feld
nachwirken.

Protokolle:

- `mcm_thought_seed_protocol.csv` schreibt die neuen Verdauungswerte.
- `mcm_thought_memory.json` speichert die Werte je Seed und je Thought-Family.
- `trade_stats.py` uebernimmt die Werte in die Trade-Kontextauswertung.

Wie es weitergeht:
Im naechsten Lauf pruefen wir, ob `open_hypothesis_reorganizing_memory` weniger
direkt in schwache Motorik kippt und stattdessen haeufiger als
`digestive_replay`, `digestive_distance` oder `digestive_integration`
auftaucht. Wichtig ist, ob spaeter `digestive_trust_return` entsteht, also:
"Meine Hypothese war nicht sofort handelbar, aber nach innerer Verarbeitung
wieder tragfaehig."

---

# Lauf 8 bis 10 nach Hypothesenreifung ausgewertet

Status:
Ausgewertet.

Debug:

- `debug/debug_lauf_8`
- `debug/debug_lauf_9`
- `debug/debug_lauf_10`

Ergebnisse:

| Lauf | Netto-PnL | Trades | Long-PnL | Short-PnL | TP / SL | Max-DD |
|---:|---:|---:|---:|---:|---:|---:|
| 8 | `+20.89` | `342` | `+3.80` | `+17.09` | `137 / 205` | `10.95 %` |
| 9 | `+30.28` | `369` | `+5.21` | `+25.07` | `150 / 219` | `17.45 %` |
| 10 | `+32.37` | `369` | `-1.23` | `+33.60` | `151 / 218` | `6.63 %` |

Deutung:
Die Serie bestaetigt den Effekt aus Lauf 6 und 7. Lauf 8 bis 10 bleiben
deutlich positiv. Lauf 10 ist besonders interessant, weil der PnL hoch ist und
der Drawdown gleichzeitig sehr niedrig bleibt.

Richtung:
Short ist der klare Haupttraeger:

- Lauf 8: Short ca. `+17.09`
- Lauf 9: Short ca. `+25.07`
- Lauf 10: Short ca. `+33.60`

Long bleibt wechselhaft:

- Lauf 8: Long ca. `+3.80`
- Lauf 9: Long ca. `+5.21`
- Lauf 10: Long ca. `-1.23`

Das passt zur Makrostruktur des Datensatzes: DIO lernt nicht eine starre
Short-Regel, aber in diesem Kontext wird Short als tragender erlebt.

Hypothesenreifung:
Die neuen Werte arbeiten stabil:

- `act` zeigt hoehere `open_hypothesis_action_permission`
- `replan` zeigt fast keine `open_hypothesis_confirmation_weight`
- `replan` zeigt hohe `open_hypothesis_learning_charge`
- `replan` zeigt hohe `open_hypothesis_reality_check_need`

Neurologisch gelesen:
DIO trennt weiter zwischen Gedanke und Handlung. Eine unreife Hypothese wird
nicht sofort als Motorik verwendet, sondern bekommt Reflexion, Realitaetscheck
und Lernspannung. Bestaetigte Hypothesen kommen naeher an Handlung.

Wichtiger Restbefund:
`open_hypothesis_reorganizing` bleibt in der Ergebnisstatistik weiterhin stark
negativ. Das ist nicht automatisch schlecht, aber es zeigt: Diese Spur
enthaelt noch immer viel unverdaute Lernspannung. Der naechste Schritt sollte
daher nicht mehr Handlung aus Reorganisation erzeugen, sondern diese Spur
staerker als inneres Trainings-/Replay-Material behandeln.

Wie es weitergeht:
Der naechste sinnvolle Schritt ist eine organische Replay-/Verdauungsschicht
fuer reorganisierende Hypothesen:

- nicht sperren
- nicht direkt handeln
- als innere Trainingsspur halten
- gegen spaetere bestaetigte Strukturkontakte pruefen
- erst bei wiederholter Tragfaehigkeit als Vertrauen zurueckgeben

---

# Lauf 6 und 7 nach weicher Hypothesenreifung ausgewertet

Status:
Ausgewertet.

Debug:

- `debug/debug_lauf_6`
- `debug/debug_lauf_7`

Ergebnis Lauf 6:

- Netto-PnL: ca. `+16.56`
- Trades: `349`
- TP / SL: `140 / 209`
- Long-PnL: ca. `-2.81`
- Short-PnL: ca. `+19.37`
- Equity-Peak: ca. `117.90`
- Max-DD: ca. `11.02 %`

Ergebnis Lauf 7:

- Netto-PnL: ca. `+25.08`
- Trades: `354`
- TP / SL: `143 / 211`
- Long-PnL: ca. `+0.50`
- Short-PnL: ca. `+24.58`
- Equity-Peak: ca. `127.47`
- Max-DD: ca. `7.26 %`

Deutung:
Die weiche Hypothesenreifung wirkt sichtbar. Nach dem schwachen Lauf 5 steigt
DIO in Lauf 6 wieder deutlich an und Lauf 7 wird noch stabiler. Besonders
wichtig ist der Drawdown: Lauf 7 erreicht einen deutlich ruhigeren Verlauf.

Richtung:
DIO verlagert seine tragende Seite stark auf Short. Das passt zum aktuellen
Datensatz, der makro short-dominant ist. Long bleibt in Lauf 7 knapp positiv,
traegt aber nicht die Hauptbewegung.

Neue Hypothesenwerte im Field-Protokoll:

- `open_hypothesis_confirmation_weight`
- `open_hypothesis_learning_charge`
- `open_hypothesis_action_permission`
- `open_hypothesis_reality_check_need`

Wichtiger Befund:

- Bei `act` ist `open_hypothesis_action_permission` klar hoeher als bei `wait`.
- Bei `replan` ist `open_hypothesis_confirmation_weight` praktisch `0`.
- Bei `replan` sind `open_hypothesis_learning_charge` und
  `open_hypothesis_reality_check_need` am hoechsten.

Neurologisch gelesen:
DIO trennt jetzt besser:

- bestaetigte Hypothese -> Handlung darf naeher kommen
- unreife/reorganisierende Hypothese -> Realitaetspruefung und Replay
- belastete Hypothese -> Vorsicht und Abstand

Das ist ein wichtiger Schritt. Die Hypothese wird nicht blockiert, aber sie
wird auch nicht mehr direkt als Motorik gelesen. Sie bekommt erst eine innere
Reifung.

Wie es weitergeht:
Der naechste Lauf sollte pruefen, ob Lauf 7 bestaetigt wird oder ob DIO wieder
in Long-Unruhe kippt. Besonders beobachten:

- Short bleibt Haupttraeger oder nicht
- `open_hypothesis_action_permission` bei `act`
- `open_hypothesis_reality_check_need` bei `replan`
- `open_hypothesis_reorganizing_memory`
- Drawdown bleibt reduziert oder steigt wieder

---

# Umsetzung - Hypothesenreifung weicher getrennt

Status:
Umgesetzt.

Datei:
`MCM_Brain_Modell.py`

Was geaendert wurde:
DIO unterscheidet offene Hypothesen jetzt feiner. Eine Hypothese wird nicht
mehr nur als allgemeiner Druck gelesen, sondern in vier innere Qualitaeten
aufgeteilt:

- `open_hypothesis_confirmation_weight`
- `open_hypothesis_learning_charge`
- `open_hypothesis_action_permission`
- `open_hypothesis_reality_check_need`

Bedeutung:

- `open_hypothesis_confirmation_weight` beschreibt, ob eine Hypothese aus
  bestaetigter Erfahrung tragend nachklingt.
- `open_hypothesis_learning_charge` beschreibt, ob die Hypothese eher
  Lernspannung / Reorganisation enthaelt.
- `open_hypothesis_action_permission` beschreibt, ob die Hypothese zusammen mit
  Feld, Struktur und innerer Lage handlungsnah werden darf.
- `open_hypothesis_reality_check_need` beschreibt, ob die Hypothese erst
  geprueft, replayed oder mit Abstand betrachtet werden sollte.

Neurologisch gelesen:
Das ist eine weichere Trennung zwischen:

- "Meine Hypothese wurde bestaetigt, ich darf ihr vorsichtig vertrauen."
- "Meine Hypothese war belastend, ich brauche Abstand."
- "Meine Hypothese ist nicht falsch, aber unreif; sie gehoert in Reflexion und
  Lernspannung, nicht direkt in Motorik."

Wichtig:
Das ist keine harte Handlungssperre. Reorganisierende Hypothesen werden nicht
verboten, sondern weniger direkt als Motorimpuls gelesen. Sie bekommen mehr
Reflexionszug, Realitaetspruefung und act-watch-Reifung.

Validierung:

- `python -m py_compile .\MCM_Brain_Modell.py .\bot.py .\trade_stats.py`
  erfolgreich.

Wie es weitergeht:
Lauf 6 sollte pruefen, ob `open_hypothesis_reality_check_need`,
`open_hypothesis_learning_charge` und `open_hypothesis_action_permission` im
Field-Protokoll sichtbar werden und ob reorganisierende Hypothesen weniger
verlustreich direkt in Handlung kippen.

---

# Lauf 5 nach MCM-Spannungsachse ausgewertet

Status:
Ausgewertet.

Debug:
`debug/debug_lauf_5`

Ergebnis:

- Netto-PnL: ca. `+4.32`
- Equity: ca. `104.32`
- Trades: `323`
- TP / SL: `116 / 207`
- Long-PnL: ca. `+0.81`
- Short-PnL: ca. `+3.52`
- Long-Trades / Short-Trades: `158 / 165`
- Beobachtet / Zurueckgehalten / Replanned: `3555 / 2644 / 35`
- Equity-Peak: ca. `107.38`
- Max-DD: ca. `11.55 %`

Vergleich zu Lauf 4:

- Lauf 4: ca. `+15.69`
- Lauf 5: ca. `+4.32`
- Long faellt von ca. `+9.42` auf ca. `+0.81`
- Short faellt von ca. `+6.27` auf ca. `+3.52`
- Trades sinken von `364` auf `323`
- Beobachtung und Zurueckhaltung steigen

MCM-Achsenbild:

- `mcm_axis_state`: `9173` mal `0`, `154` mal `-`, kein `+`
- `positive_zero_point_regulation`: weiterhin `0`

Deutung:
Der Rueckgang kommt nicht aus einer positiven Ueberdehnung. Die neue
MCM-Achse bleibt stabil um den Nullpunkt. Das Problem liegt eher in der
Hypothesen- und Reifeschicht:

- bestaetigte strukturelle Interpretation sinkt von `38` auf `29`
- offene Strukturhypothesen bleiben stark belastend
- `open_hypothesis_carried` sinkt von `37` auf `23`
- `open_hypothesis_reorganizing` bleibt stark negativ
- `fused_score_too_low`, `maturity_block`, `context_cluster_negative` und
  `withheld` steigen

Neurologisch gelesen:
DIO ist nicht in Euphorie gekippt, sondern eher in eine vorsichtigere,
hemmendere Verarbeitung. Die positive Achse ist zentriert, aber die kognitive
Hypothesenlage traegt weniger. Das wirkt wie:

"Ich bin nicht ueberreizt, aber ich traue meiner Deutung weniger. Ich pruefe
mehr, halte mehr zurueck und verliere dadurch Handlungsschaerfe."

Wie es weitergeht:
Der naechste sinnvolle Schritt ist nicht, Long oder Short hart zu regeln.
Stattdessen sollte die Hypothesenreifung sauberer unterscheiden:

- offene Hypothese mit tragendem Kontakt -> weiter halten / replayen
- offene Hypothese ohne Bestaetigung -> mehr Distanz / beobachten
- reorganisierende Hypothese -> nicht als Handlungskraft lesen, sondern als
  Lernspannung ins MCM-Feld zurueckgeben

---

# Lauf 1 nach DIO-Form-Language-Core und frischem Memory

Status:
Ausgewertet.

Rahmen:
- neuer Memory-Aufbau nach Archivierung
- neue Debug-Struktur mit getrennten Bereichen `gui`, `core`, `position`
- `mcm_thought_memory.json` wird sauber geschrieben, aber wächst stark

Kennzahlen:
- Trades: `409`
- Netto-PnL: ca. `+3.57`
- Long: `216` Trades, PnL ca. `-5.63`
- Short: `193` Trades, PnL ca. `+9.21`
- Wins / Losses: `145 / 264`
- Equity-Peak: ca. `104.79`
- Max Drawdown: ca. `16.01%`

Deutung:
DIO ist im ersten neuen Lauf nicht stark profitabel, aber auch nicht zerfallen.
Das Verhalten wirkt wie eine erste Reorganisation nach neuem Sprach- und
Gedankenraum: viel Beobachtung, viel innere Verdichtung, wenig echtes Vertrauen.

Wichtig:
Der Gedankenraum ist aktiv. Im Thought-Seed-Protokoll tauchen vor allem auf:
- `open_thought_sentence`
- `thin_syntax`
- `ordinary_structure_reading`
- `open_structural_hypothesis`

Die Hypothesenreifung ist sichtbar:
- `open_hypothesis_neutral_memory`: dominant
- `open_hypothesis_reorganizing_memory`: stark vertreten
- `open_hypothesis_carried_memory`: noch selten

Neurologisch gelesen:
DIO bildet Sprache und Gedankenkeime, aber die innere Außen-Kopplung ist noch
schwach. `inner_outer_alignment` und `temporal_self_consistency` liegen niedrig.
Das wirkt wie ein Organismus, der schon benennt und reflektiert, aber seiner
eigenen Deutung noch nicht stabil vertraut.

Wie es weitergeht:
Als nächstes prüfen wir, ob der Gedankenraum zu schnell wächst und ob die
Syntax-Spuren stärker verdichtet werden müssen. Danach sollte Lauf 2 zeigen,
ob die neu gespeicherten Gedankenfamilien bereits als tragendere Orientierung
wirken oder ob DIO weiter in Reorganisation bleibt.

# Lauf 2 nach DIO-Form-Language-Core

Status:
Ausgewertet.

Kennzahlen:
- Trades: `345`
- Netto-PnL: ca. `+5.08`
- Long: `167` Trades, PnL ca. `-3.83`
- Short: `178` Trades, PnL ca. `+8.91`
- Wins / Losses: `124 / 221`
- Equity-Peak: ca. `110.61`
- Max Drawdown aus Stats: ca. `11.88%`
- Max Drawdown aus kompletter Equity-Spanne: ca. `17.38%`

Vergleich zu Lauf 1:
- weniger Trades (`409` -> `345`)
- besserer Endstand (`+3.57` -> `+5.08`)
- weniger Cancels (`35` -> `23`)
- mehr Beobachtung und Zurückhalten
- Thought-Memory wächst kaum weiter (`8.70 MB` -> `8.72 MB`)

Deutung:
Das ist ein gutes Zeichen. Der Gedankenraum explodiert nicht weiter, sondern
DIO scheint vorhandene Gedankenfamilien wiederzuverwenden. Die neue Formsprache
wirkt damit nicht nur als Datensammler, sondern bereits als Verdichtungsraum.

Hypothesenreifung:
- `open_hypothesis_neutral_memory`: `4754`
- `open_hypothesis_reorganizing_memory`: `3196`
- `open_hypothesis_carried_memory`: `927`

Wichtiger Vergleich:
`open_hypothesis_carried_memory` ist von `340` in Lauf 1 auf `927` in Lauf 2
gestiegen. Auch `hypothesis_trust` steigt von ca. `0.023` auf ca. `0.059`.
Das ist noch kein starkes Vertrauen, aber eine klare Bewegung von bloßer
Reorganisation in Richtung getragener innerer Hypothesen.

Neurologisch gelesen:
DIO handelt nicht einfach mehr, sondern selektiver. Die dominante innere Lage
bleibt zwar `tired`, aber `reflective`, `curious`, `adaptive_watch` und
getragene Hypothesen nehmen zu. Das sieht aus wie ein Nervensystem, das nicht
mehr nur auf Reizdruck reagiert, sondern anfängt, seine eigenen Gedankenkeime
als innere Orientierung zu benutzen.

Wie es weitergeht:
Lauf 3 sollte prüfen, ob die getragenen Hypothesen weiter steigen und ob
`hypothesis_trust`, `inner_outer_alignment` und `temporal_self_consistency`
stabiler werden. Danach sollten wir entscheiden, ob der Thought-Memory bereits
gut verdichtet oder ob wir eine weichere Familien-Zusammenführung brauchen.

# Lauf 3 nach DIO-Form-Language-Core

Status:
Ausgewertet.

Kennzahlen:
- Trades: `379`
- Netto-PnL: ca. `+13.01`
- Long: `187` Trades, PnL ca. `-6.74`
- Short: `192` Trades, PnL ca. `+19.75`
- Wins / Losses: `149 / 230`
- Equity-Peak: ca. `114.79`
- Max Drawdown aus Stats: ca. `11.77%`
- Max Drawdown aus kompletter Equity-Spanne: ca. `15.97%`

Vergleich zu Lauf 2:
- PnL steigt deutlich (`+5.08` -> `+13.01`)
- Trades steigen wieder leicht (`345` -> `379`)
- Observation-Maturity steigt (`0.511` -> `0.535`)
- Action-Pressure sinkt (`0.487` -> `0.463`)
- Thought-Memory bleibt weiter kontrolliert (`8.72 MB` -> `8.74 MB`)

Deutung:
Lauf 3 zeigt eine bessere äußere Performance, aber keine einfache lineare
Steigerung des inneren Vertrauens. `hypothesis_trust` fällt gegenüber Lauf 2
wieder ab, während PnL und Beobachtungsqualität steigen. Das ist wichtig:
DIO kann profitabler handeln, obwohl die innere Hypothesen-Sicherheit noch
schwankt.

Hypothesenreifung:
- `open_hypothesis_neutral_memory`: `5152`
- `open_hypothesis_reorganizing_memory`: `2592`
- `open_hypothesis_carried_memory`: `429`

Neurologisch gelesen:
DIO wirkt in Lauf 3 nicht einfach selbstsicherer, sondern funktionaler im
Umgang mit Unsicherheit. Mehr `act_watch`, mehr positive Short-Struktur und
weniger Action-Pressure sprechen dafür, dass DIO nicht nur kämpft, sondern
Situationen eher abwartend und selektiv verarbeitet. Gleichzeitig bleibt die
innere Lage stark `tired` und `reflective`; der Organismus trägt den Lauf also
noch mit hoher Denk- und Integrationslast.

Wie es weitergeht:
Lauf 4 sollte zeigen, ob sich die bessere PnL stabilisiert oder ob sie nur aus
einem günstigen Zusammenspiel von Short-Struktur und Reorganisation entstanden
ist. Wichtig bleibt jetzt die Trennung: PnL kann steigen, während
Hypothesenvertrauen schwankt. Deshalb sollten wir nicht nur Profit messen,
sondern die Kopplung aus `hypothesis_trust`, `observation_learning`,
`act_watch` und `position_nervousness`.

# Lauf 4 nach DIO-Form-Language-Core

Status:
Ausgewertet.

Kennzahlen:
- Trades: `397`
- Netto-PnL: ca. `+31.26`
- Long: `168` Trades, PnL ca. `+2.66`
- Short: `229` Trades, PnL ca. `+28.60`
- Wins / Losses: `163 / 234`
- Equity-Peak: ca. `134.86`
- Max Drawdown aus Stats: ca. `9.20%`
- Max Drawdown aus kompletter Equity-Spanne: ca. `27.77%`

Entwicklungsreihe nach frischem Memory:
- Lauf 1: ca. `+3.57`
- Lauf 2: ca. `+5.08`
- Lauf 3: ca. `+13.01`
- Lauf 4: ca. `+31.26`

Deutung:
Lauf 4 bestätigt den deutlichen Entwicklungssprung aus Lauf 3. Der Sprung wirkt
nicht wie reine Trade-Menge, sondern wie eine bessere Kopplung zwischen
Formsprache, Beobachtung, Handlungsvorbereitung und Marktstruktur. Besonders
wichtig: Long ist nicht mehr deutlich negativ, sondern leicht positiv. Short
bleibt der Hauptträger.

Thought-Memory:
Der Gedankenraum bleibt kontrolliert:
- Lauf 1: ca. `8.70 MB`
- Lauf 2: ca. `8.72 MB`
- Lauf 3: ca. `8.74 MB`
- Lauf 4: ca. `8.75 MB`

Das spricht gegen chaotische Gedankenvermehrung. DIO scheint seine innere
Formsprache wiederzuverwenden und zu verdichten.

Neurologisch gelesen:
Das wirkt wie ein kognitives Zünden, aber noch nicht wie voll stabiles
Selbstvertrauen. `hypothesis_trust` bleibt niedrig, waehrend Performance und
Handlungskopplung deutlich besser werden. Der Sprung kommt daher eher aus:
- stabilerer Thought-Kompression
- besserer struktureller Motorik
- mehr `act_watch` als vorbereitete Handlungslage
- weniger reinem Reflexdruck
- weiterhin aktiver, aber nicht explodierender innerer Reorganisation

Wichtig:
Das ist ein sehr starker Hinweis, aber noch kein endgueltiger Nachweis. Wir
brauchen weitere Laeufe, um zu unterscheiden:
- echter Reifungseffekt
- guenstige Pfadabhaengigkeit
- Short-Regime-Vorteil
- zufaellige Varianz

Wie es weitergeht:
Lauf 5 sollte pruefen, ob DIO den Sprung halten kann. Parallel sollten wir eine
kleine Entwicklungsuebersicht bauen, die pro Lauf PnL, Thought-Memory-Groesse,
`hypothesis_trust`, `open_hypothesis_carried_memory`, `act_watch`,
Long/Short-PnL und Observation-Learning nebeneinander legt.

# Entwicklungsübersicht angelegt

Status:
Umgesetzt in `files/ENTWICKLUNGSUEBERSICHT.md`.

Inhalt:
- Lauf 1 bis 4 nach frischem Memory
- Netto-PnL
- Trades
- Long-/Short-PnL
- Thought-Protokollgröße und Zeilenzahl
- `hypothesis_trust`
- getragene Hypothesen
- Reorganisationszustände
- `act_watch`
- Observation-Maturity
- Action-Pressure

Deutung:
Die Übersicht zeigt den Sprung von `+3.57` auf `+31.26`, aber auch, dass
`hypothesis_trust` noch nicht linear mit PnL steigt. Das bestätigt die Trennung
zwischen äußerer Performance und innerer Selbstsicherheit.

Wie es weitergeht:
Nach Lauf 5 die Tabelle fortschreiben und prüfen, ob der Sprung getragen wird
oder ob DIO wieder in Reorganisation zurückfällt.

# Lauf 5 nach DIO-Form-Language-Core

Status:
Ausgewertet und in `files/ENTWICKLUNGSUEBERSICHT.md` ergänzt.

Kennzahlen:
- Trades: `347`
- Netto-PnL: ca. `+20.97`
- Long: `130` Trades, PnL ca. `-8.65`
- Short: `217` Trades, PnL ca. `+29.62`
- Wins / Losses: `136 / 211`
- Equity-Peak: ca. `122.87`
- Max Drawdown aus Stats: ca. `9.40%`

Deutung:
Lauf 5 ist gegenüber Lauf 4 schwächer, aber kein echter Rückfall. Short bleibt
sehr stark, Long kippt wieder deutlich negativ. Das erklärt den magereren
Gesamteindruck.

Innere Lage:
- mehr `WAIT`
- mehr `hold`
- mehr `fused_score_too_low`
- mehr `maturity_block`
- mehr `context_overcoupling_reflection`
- `open_hypothesis_carried_memory` steigt auf `627`
- `hypothesis_trust` steigt leicht auf ca. `0.037`

Neurologisch gelesen:
DIO wirkt nicht zerfallen, sondern vorsichtiger und stärker prüfend. Das
Nervensystem hält mehr zurück und findet im Long-Bereich keine tragfähige
Form. Der Short-Bereich bleibt dagegen strukturell tragend.

Wie es weitergeht:
Lauf 6 sollte prüfen, ob diese Vorsicht eine Reorganisationsphase ist oder ob
DIO eine Long-spezifische Unsicherheit entwickelt. Wichtig sind jetzt
Long-PnL, `maturity_block`, `fused_score_too_low`,
`context_overcoupling_reflection` und getragene Hypothesen.

# Umsetzung: MCM-Spannungsachse `-- - 0 + ++`

Status:
Umgesetzt.

Auslöser:
Die positive MCM-Seite wurde bisher zu stark als Ruhe, Wohlbefinden oder
Support gelesen. Das kollidiert mit dem MCM-Grundgedanken des Nullpunkts:
Auch positive Auslenkung ist Spannung und kann Rückführung brauchen.

Neue Kernlogik:

- `--`: starke kontraktive Spannung
- `-`: leichte kontraktive Spannung
- `0`: regulierter Tragpunkt
- `+`: leichte expansive Spannung
- `++`: starke expansive Spannung

Umsetzung in `MCM_Brain_Modell.py`:

- `positive_expansion_pressure`
- `negative_contraction_pressure`
- `positive_overextension`
- `positive_return_pressure`
- `mcm_axis_displacement`
- `mcm_axis_tension`
- `mcm_axis_state`
- `positive_zero_point_regulation`

Mechanische Wirkung:
Positive Expansion erhöht nicht automatisch Handlung. Wenn sie nicht durch
Feldtragfähigkeit, Strukturkontakt, innere/äußere Kohärenz und Interpretation
gedeckt ist, erzeugt sie weich:

- mehr Beobachtung
- mehr `act_watch`
- mehr Hemmung
- mehr Reflexion
- weniger direkte `action_clearance`
- mögliche `positive_expansion_zero_point` / `positive_expansion_observe`

Wichtig:
Das ist keine Long-Sperre und keine harte Regel. DIO bekommt eine neue
Innenwahrnehmung: "Bin ich tragfähig positiv oder werde ich nur positiv
gezogen?"

Dokumentation aktualisiert:

- `README.md`
- `files/UMSETZUNGSPLAN.md`
- `files/WICHTIG_MECHANIKEN.md`
- `files/MCM_VARIABLEN_MECHANIK.md`

Prüfung:
`python -m py_compile .\MCM_Brain_Modell.py .\bot.py .\trade_stats.py`
läuft sauber.

Wie es weitergeht:
Der nächste Lauf sollte besonders `mcm_axis_state`, `positive_return_pressure`,
`positive_zero_point_regulation`, Long-PnL und `positive_expansion_observe`
prüfen. Wenn Long vorher aus positiver Überdehnung kam, sollte DIO jetzt eher
merken: "Das zieht mich positiv, aber es trägt noch nicht."

## Fix nach Startfehler

Fehler:
`inner_outer_alignment` wurde in der neuen positiven Spannungslogik verwendet,
bevor die bewusste Wahrnehmungsschicht diesen Wert aufgebaut hatte.

Fix:
Vor der positiven Spannungsachse wird jetzt
`pre_conscious_inner_outer_alignment` aus Feldklarheit, Interpretation,
Memory-Orientierung, Processing-Alignment, bekannter Form und
Orientierungslücke gebildet.

Prüfung:
`python -m py_compile .\MCM_Brain_Modell.py .\bot.py .\trade_stats.py`
läuft sauber.

# Debug Läufe 1-3 nach MCM-Spannungsachse

Status:
Ausgewertet.

Wichtiger Hinweis:
Die Mechanik der MCM-Spannungsachse war aktiv, aber
`mcm_field_decision_protocol.csv` schrieb die neuen Achsen in diesen drei
Läufen noch nicht mit. Die Protokollausgabe wurde danach korrigiert. Die
Verhaltensdaten sind auswertbar, die direkte Achsenverteilung erst ab dem
nächsten Lauf.

Kennzahlen:

- Lauf 1: PnL ca. `-0.01`, Trades `370`, Long ca. `-4.05`, Short ca. `+4.03`
- Lauf 2: PnL ca. `+3.13`, Trades `375`, Long ca. `-15.13`, Short ca. `+18.26`
- Lauf 3: PnL ca. `+22.84`, Trades `367`, Long ca. `-6.39`, Short ca. `+29.23`

Deutung:
Die Serie wirkt wie eine Reorganisation nach neuer MCM-Spannungslogik:

`-0.01 -> +3.13 -> +22.84`

Lauf 1 neutralisiert fast vollständig, Lauf 2 hebt leicht an, Lauf 3 wird
wieder deutlich tragender. Short bleibt der strukturelle Hauptträger, Long
bleibt instabil.

Innere Lage:

- `action_clearance` sinkt von ca. `0.613` auf ca. `0.598`
- `action_inhibition` steigt von ca. `0.455` auf ca. `0.473`
- `act_watch` steigt von `736` auf `1017`
- Observation-Maturity bleibt stabil bei ca. `0.529`

Neurologisch gelesen:
DIO wird nicht wilder, sondern vorsichtiger, gebundener und stärker
vorbereitend. Dass Lauf 3 trotzdem deutlich besser wird, spricht dafür, dass
die neue Spannungslogik nicht nur bremst, sondern Handlung stärker reifen
lässt.

Fix:
Das Field-Protokoll schreibt ab dem nächsten Lauf auch:

- `positive_expansion_pressure`
- `negative_contraction_pressure`
- `positive_overextension`
- `positive_return_pressure`
- `mcm_axis_displacement`
- `mcm_axis_tension`
- `mcm_axis_state`
- `positive_zero_point_regulation`

Prüfung:
`python -m py_compile .\MCM_Brain_Modell.py .\bot.py .\trade_stats.py`
läuft sauber.

Wie es weitergeht:
Der nächste Lauf ist nötig, um die neue MCM-Achse direkt sichtbar zu machen.
Besonders wichtig ist der Vergleich Long vs Short bei
`positive_return_pressure` und `mcm_axis_state`.

# Umsetzung - Reifeschicht für offene Hypothesen

Status:
Umgesetzt nach Lauf 65.

Grund:
Lauf 65 zeigte klar:

- `open_hypothesis_carried`: `30 TP / 0 SL`, ca. `+31.89`
- `open_hypothesis_reorganizing`: `0 TP / 127 SL`, ca. `-54.68`

Offene Hypothesen sind also nicht grundsätzlich unreif. Wenn sie getragen
sind, sind sie sehr konstruktiv. Die Last entsteht, wenn ein noch
reorganisierender Gedankenkeim zu früh in Motorik läuft.

Neue innere Meta-Werte:

- `open_hypothesis_bearing_echo`
  - positive Erinnerungsspur getragener offener Hypothesen
- `open_hypothesis_reifung_pressure`
  - Druck, dass eine offene Hypothese erst nachreifen muss
- `open_hypothesis_reflection_pull`
  - Tendenz zu Replay, Distanzierung und erneuter Wahrnehmung
- `open_hypothesis_motor_tension`
  - Spannung zwischen Gedankenkeim und unmittelbarer Handlung
- `open_hypothesis_reifung_state`
  - `open_hypothesis_carried_memory`
  - `open_hypothesis_burden_memory`
  - `open_hypothesis_reorganizing_memory`
  - `open_hypothesis_neutral_memory`

Wirkung:

- Getragene offene Hypothesen geben weich mehr Handlungstragfähigkeit.
- Belastete oder reorganisierende offene Hypothesen erhöhen Beobachtung,
  Replan, Replay und `act_watch_readiness`.
- Handlung wird nicht hart blockiert.
- Starke Entscheidungen bleiben möglich.
- Unsichere reorganisierende Hypothesen werden eher in Nachreifung geführt.

Neurologische Deutung:
DIO bekommt eine Art präfrontale Reifeschicht für Gedankenkeime. Nicht jedes
innere Muster wird sofort motorisch. Ein Gedanke kann gehört, gehalten,
replayed und neu betrachtet werden, bevor er Handlung wird.

Wie es weitergeht:
Lauf 66 prüfen:

- sinkt die Verlustlast bei `open_hypothesis_reorganizing`?
- bleiben `open_hypothesis_carried` und bestätigte Struktur tragfähig?
- steigt `replan`/`observe` bei unreifen offenen Hypothesen ohne den Lauf
  komplett zu lähmen?

---

# Auswertung - Lauf 65

Status:
Ausgewertet.

Kerndaten:

- Netto-PnL: ca. `+44.88`
- Trades: `371`
- TP/SL: `163 / 208`
- Winrate: ca. `43.94 %`
- Profit Factor: ca. `1.42`
- Expectancy: ca. `+0.121`
- Max Drawdown: ca. `9.09 %`
- Attempts: `11375`
- Attempts pro Trade: ca. `30.66`

Richtungsprofil:

- LONG:
  - Trades: `165`
  - TP/SL: `66 / 99`
  - PnL: ca. `+14.42`
- SHORT:
  - Trades: `206`
  - TP/SL: `97 / 109`
  - PnL: ca. `+30.46`

Befund:
Lauf 65 bleibt klar positiv, ist aber nervlicher belasteter als Lauf 64:
PnL niedriger, Drawdown höher und Attempts pro Trade höher. Short trägt weiter
stärker als Long.

Emergente Struktur aus `trade_stats.json`:

- `confirmed_structural_interpretation`:
  - `50 TP / 0 SL`
  - PnL ca. `+52.21`
  - avg RR ca. `4.73`
- `ordinary_structure_reading`:
  - `81 TP / 65 SL / 31 Cancel`
  - PnL ca. `+20.52`
- `open_structural_hypothesis`:
  - `30 TP / 141 SL`
  - PnL ca. `-29.57`
- `wide_target_without_structure`:
  - leicht positiv, PnL ca. `+1.72`

Open-Hypothesis-Learning:

- `open_hypothesis_carried`:
  - `30 TP / 0 SL`
  - PnL ca. `+31.89`
- `open_hypothesis_burdened`:
  - `0 TP / 14 SL`
  - PnL ca. `-6.77`
- `open_hypothesis_reorganizing`:
  - `0 TP / 127 SL`
  - PnL ca. `-54.68`

Deutung:
Die offene Hypothese ist nicht grundsätzlich schlecht. Wenn sie getragen wird,
ist sie extrem positiv. Die Hauptlast entsteht dort, wo sie reorganisierend
oder belastet ist und trotzdem bis zur Konsequenz läuft. Neurologisch gelesen:
Der Gedankenkeim ist vorhanden, aber die Reifung koppelt noch zu oft an
Motorik, bevor der innere Zustand tragfähig genug integriert ist.

Diagnosefix bestätigt:

- `trade_equity.csv` wird geschrieben:
  - Größe ca. `29.5 KB`
  - `371` Equity-Zeilen
- `trade_stats.json` enthält die emergenten Strukturwerte direkt.
- Debuggröße bleibt reduziert:
  - ca. `34.83 MB`

Wie es weitergeht:
Jetzt ist die nächste sinnvolle Mechanik nicht ein Blockieren offener
Hypothesen, sondern eine Reifeschicht:

- DIO soll unterscheiden lernen:
  - offene Hypothese getragen
  - offene Hypothese belastet
  - offene Hypothese noch reorganisierend
- Bei reorganisierenden Hypothesen soll eher inneres Nachreifen, Replay,
  Distanzierung und erneute Wahrnehmung entstehen.
- Bei getragenen Hypothesen darf Handlung weiter möglich bleiben.

---

# Fix - `trade_equity.csv` sofort für GUI schreiben

Status:
Umgesetzt nach Lauf 64.

Grund:
`trade_equity.csv` ist die PnL-/Equity-Kurve für die GUI. Durch
`DEBUG_WRITE_MODE = buffered` wurde sie zwar am Ende geschrieben, war aber
während des Laufs nicht zuverlässig sofort auf Platte sichtbar.

Umsetzung:
`debug_reader.py` puffert `trade_equity.csv` nicht mehr. Die Datei wird direkt
geschrieben, während schwere Forschungsdateien wie `outcome_records.jsonl`
weiter gepuffert bleiben.

Wichtig:
Das verändert keine Trading-, MCM- oder Thought-Memory-Mechanik. Es betrifft
nur die Sichtbarkeit der GUI-Vitalspur.

Wie es weitergeht:
Im nächsten Lauf prüfen, ob `debug_lauf_x/trade_equity.csv` während des Laufs
laufend anwächst und die GUI die Equity-Kurve wieder direkt lesen kann.

---

# Auswertung - Lauf 64 und Stats-Puffer-Fix

Status:
Ausgewertet und kleiner Diagnosefix umgesetzt.

Kerndaten:

- Netto-PnL: ca. `+52.14`
- Trades: `384`
- TP/SL: `169 / 215`
- Winrate: ca. `44.01 %`
- Profit Factor: ca. `1.48`
- Expectancy: ca. `+0.136`
- Max Drawdown: ca. `6.54 %`
- Attempts: `10750`
- Attempts pro Trade: ca. `27.99`

Richtungsprofil:

- LONG:
  - Trades: `162`
  - TP/SL: `63 / 99`
  - PnL: ca. `+17.57`
- SHORT:
  - Trades: `222`
  - TP/SL: `106 / 116`
  - PnL: ca. `+34.57`

Befund:
Lauf 64 ist wieder sehr stark und bleibt im Drawdown ruhiger als frühere hohe
PnL-Läufe. Short trägt weiter stärker, Long ist aber ebenfalls positiv.

Emergente Struktur aus `outcome_records.jsonl`:

- `confirmed_structural_interpretation`:
  - `54 TP / 0 SL`
  - PnL ca. `+58.93`
- `ordinary_structure_reading`:
  - `85 TP / 65 SL / 32 Cancel`
  - PnL ca. `+27.98`
- `open_structural_hypothesis`:
  - `29 TP / 149 SL`
  - PnL ca. `-35.09`
- `wide_target_without_structure`:
  - ungefähr neutral, PnL ca. `+0.32`

Debuglast:

- Lauf 63: ca. `142.83 MB`
- Lauf 64: ca. `34.29 MB`

Das neue `DIO_CORE_DEBUG` reduziert die Diagnoseausgabe also deutlich, ohne die
PnL-/Equity-Spur für GUI zu verlieren.

Fix:
Durch `DEBUG_WRITE_MODE = buffered` wurde `outcome_records.jsonl` erst später
auf Platte geschrieben. `trade_stats.json` baute seine emergente
Zusammenfassung während des Laufs aber aus dieser Datei und sah dadurch
zeitweise keine Outcomes. `TradeStats` hält Outcome-Records nun zusätzlich in
einem kleinen In-Memory-Cache, damit `kpi_summary.emergent_structure` und
`kpi_summary.open_hypothesis_learning` auch bei gepuffertem Debug sofort
stimmen.

Wie es weitergeht:
Lauf 65 prüfen:

- bleibt der Debugordner ähnlich klein?
- stehen emergente Strukturwerte wieder direkt in `trade_stats.json`?
- bleibt `confirmed_structural_interpretation` als tragende Struktur stabil?
- bleibt `open_structural_hypothesis` Hauptlast und braucht weitere Reifung?

---

# Umsetzung - Debugausgabe auf DIO-Kern reduziert

Status:
Umgesetzt nach Lauf 63.

Grund:
Die letzten Läufe zeigten, dass der größte Engpass nicht die Thought-Memory-
Mechanik selbst ist, sondern die Menge der geschriebenen Diagnoseartefakte.
`debug_lauf_63` lag bei ca. `142.83 MB`; besonders große Dateien waren
Strategiefenster-, Attempt-, Memory- und Feldprotokolle.

Umsetzung:

- Neues Standardprofil `DIO_CORE_DEBUG` in `config.py`.
- Schwere Protokolle sind im Kernprofil standardmäßig aus:
  - `MCM_STRATEGIC_WINDOW_PROTOCOL_DEBUG`
  - `MCM_ACTIVE_CONTACT_PROTOCOL_DEBUG`
  - `TRADE_STATS_ATTEMPT_RECORD_DEBUG`
  - `MCM_MEMORY_THINKING_PROTOCOL_DEBUG`
  - `MCM_FORM_SYMBOL_PROTOCOL_DEBUG`
  - `MCM_VISUAL_CORTEX_PROTOCOL_DEBUG`
- Wichtige Kernspuren bleiben sichtbar:
  - `MCM_OUTCOME_DEBUG`
  - `trade_stats.json` und `trade_equity.csv` als PnL-/GUI-Vitalspur
  - `MCM_FIELD_DECISION_PROTOCOL_DEBUG`
  - `MCM_NEURO_TRANSITION_PROTOCOL_DEBUG`
  - `MCM_POSITION_INTERVENTION_PROTOCOL_DEBUG`
  - `MCM_EXIT_CANDIDATE_OBSERVE_DEBUG`
  - `MCM_THOUGHT_SEED_PROTOCOL_DEBUG`
- Thought-Memory und Thought-Families bleiben unabhängig vom Debugprofil aktiv.

Wichtig:
Das verändert nicht DIOs Denkmechanik, sondern nur die äußere Beobachtung.
Neurologisch gesprochen: DIO behält seine Wahrnehmung, aber wir reduzieren
die Messsensoren, die dauerhaft mitschreiben.
Die PnL-/Stats-Spur bleibt bewusst aktiv, weil sie für GUI, Verlauf und
schnelle Orientierung der äußere Vitalmonitor ist.

Wie es weitergeht:
Nächsten Lauf mit `DIO_CORE_DEBUG` prüfen:

- wird der Debugordner deutlich kleiner?
- bleiben PnL, Trades, Outcome, Neurotransitionen und Thought-Seeds lesbar?
- falls eine tiefe Einzelanalyse nötig ist, gezielt auf `RESEARCH_DEBUG`
  wechseln und danach wieder zurück auf `DIO_CORE_DEBUG`.

---

# Umsetzung - Geliehene Analogie in Thought-Seed-Reifung zurückgeführt

Status:
Umgesetzt nach Lauf 59.

Grund:
Lauf 59 zeigte klar, dass `borrowed_analogy_watch` in Verbindung mit
`open_structural_hypothesis` stark belastend ist. Das soll nicht als harte
Sperre wirken, sondern als innerer Reifehinweis.

Neue Thought-Seed-Werte:

- `borrowed_open_hypothesis_pressure`
- `own_field_binding_pull`
- `thought_seed_semantic_origin_state` im Outcome
- `thought_seed_borrowed_open_hypothesis_pressure` im Outcome
- `thought_seed_own_field_binding_pull` im Outcome

Wirkung:

- Geliehene Analogie erhöht bei offenen Hypothesen weich Neudeutung und
  Distanz.
- Eigene Feldbindung wirkt als stabilisierender Gegenzug.
- `seed_reinterpret` kann dadurch früher entstehen, wenn eine offene
  Hypothese semantisch noch nicht genug eigen ist.

Wichtig:
Keine Handlungssperre. DIO darf weiterhin handeln, aber die innere
Gedankenreifung bekommt ein Signal:
"Diese Deutung klingt nach Form, gehört aber noch nicht genug zu mir."

Wie es weitergeht:
Lauf 60 prüfen:

- sinkt die Verlustlast von `borrowed_analogy_watch` +
  `open_structural_hypothesis`?
- steigt `seed_reinterpret` bei geliehener Analogie?
- bleibt `mixed_translation_zone` als produktive Übergangslage erhalten?

---

# Auswertung - Lauf 63

Status:
Ausgewertet.

Kerndaten:

- Netto-PnL: ca. `+40.14`
- Trades: `350`
- TP/SL: `150 / 200`
- Winrate: ca. `42.86 %`
- Profit Factor: ca. `1.40`
- Expectancy: ca. `+0.115`
- Max Drawdown: ca. `6.63 %`
- Attempts: `11300`
- Attempts pro Trade: ca. `32.29`

Befund:
Lauf 63 bestätigt nicht die Extremhöhe von Lauf 62, bleibt aber deutlich
positiv und ist ruhiger im Drawdown. Gegen Lauf 62 fällt der PnL zurück, aber
gegen Lauf 61 bleibt er klar verbessert.

Vergleich:

- Lauf 61: PnL `+29.32`, DD `8.84 %`
- Lauf 62: PnL `+52.25`, DD `8.61 %`
- Lauf 63: PnL `+40.14`, DD `6.63 %`

Richtungsprofil:

- LONG:
  - Trades: `141`
  - TP/SL: `53 / 88`
  - PnL: ca. `+10.06`
  - Winrate: ca. `37.59 %`
- SHORT:
  - Trades: `209`
  - TP/SL: `97 / 112`
  - PnL: ca. `+30.08`
  - Winrate: ca. `46.41 %`

Befund Richtung:
Short bleibt die tragendere Richtung. Das Richtungsprofil wirkt damit über
mehrere Läufe stabil: DIO findet auf diesem Datensatz Short deutlich
tragfähiger als Long, ohne Long komplett negativ zu machen.

Thought-Families:

- `family_count`: `768`
- `family_total_seen`: `3351`
- `seed_count`: `2048`
- `total_seen`: `2820`

Top-Familien:
Mehrere Familien liegen jetzt bei `seen` über `100` (`114`, `106`, `105`,
`93`). Das bestätigt, dass die Familienbildung nicht nur technisch existiert,
sondern wiederkehrende innere Themen bündelt.

Emergente Struktur nach Outcome:

- `confirmed_structural_interpretation`:
  - `47` Fälle
  - `47 TP / 0 SL`
  - PnL ca. `+49.45`
- `open_structural_hypothesis`:
  - `167` Fälle
  - `24 TP / 143 SL`
  - PnL ca. `-33.91`
- `ordinary_structure_reading`:
  - `150` Fälle
  - `77 TP / 50 SL / 23 Cancel`
  - PnL ca. `+27.40`
- `wide_target_without_structure`:
  - `27` Fälle
  - PnL ca. `-2.80`

Deutung:
Thought-Families stabilisieren die innere Wiederholung, aber die offene
Strukturhypothese ist noch nicht gelöst. Lauf 62 zeigte dort Entlastung,
Lauf 63 zeigt wieder höhere Last. Der stabilere Teil ist:

- bestätigte Struktur bleibt extrem tragfähig
- normale Strukturlesung trägt stark
- Short bleibt tragend
- Familien bilden wiederkehrende innere Themen

Performance:
`debug_lauf_63` umfasst ca. `142.83 MB`. `thought_memory_write` liegt weiter
bei ca. `14-16 ms` pro Flush. Der größere Engpass bleibt die Debug-Ausgabe.

Wie es weitergeht:
Als nächstes sollte die offene Strukturhypothese mit Thought-Family-Kontext
gelesen werden: Welche Familien erzeugen belastete offene Hypothesen, welche
reifen tragfähig? Danach kann DIO lernen, offene Hypothesen eher als
Familien-Reifung zu behandeln statt als einzelne motorische Gelegenheit.

---

# Codeprüfung nach VS-Code-Absturz

Status:
Geprüft und Engpass entschärft.

Befund:
Es gab keinen Python-Syntaxfehler. `py_compile` für
`MCM_Brain_Modell.py`, `bot.py`, `trade_stats.py` und `config.py` läuft sauber.

Wahrscheinliche Belastungsquellen:

- `debug_lauf_62` umfasst ca. `135.57 MB`.
- Größte Dateien:
  - `mcm_strategic_window_protocol.csv`: ca. `39.14 MB`
  - `attempt_records.jsonl`: ca. `26.72 MB`
  - `outcome_records.jsonl`: ca. `16.11 MB`
  - `mcm_memory_thinking_protocol.csv`: ca. `14.72 MB`
  - `mcm_field_decision_protocol.csv`: ca. `12.16 MB`
- `mcm_thought_memory.json` liegt bei ca. `6 MB`.

Gefundene Code-Risikoquelle:
Beim neuen Thought-Memory wurde nach jedem Thought-Update der gesamte
Seed-/Family-Speicher normalisiert. Mit `2048` Seeds und `768` Families ist
das unnötig schwer und kann die Laufzeit/IDE-Belastung erhöhen.

Änderung:
Die Thought-Memory-Aktualisierung arbeitet jetzt inkrementell. Vollständige
Normalisierung/Sortierung passiert nur noch beim Schreiben oder wenn der
Speicher deutlich über die Grenzen wächst.

Zusatzprüfung:
Bestehende `mcm_thought_memory.json` bleibt lesbar:

- `seed_count`: `2048`
- `family_count`: `768`
- `total_seen`: `2608`
- `family_total_seen`: `2516`

Wie es weitergeht:
VS Code sollte große Debug-Dateien nicht direkt öffnen, besonders CSV/JSONL im
Bereich `10-40 MB`. Für die weitere Optimierung sollten wir als nächstes die
Debug-Ausgabe staffeln: wichtige Protokolle behalten, schwere Protokolle
optional seltener schreiben oder nur für Analyse-Läufe aktivieren.

---

# Auswertung - Lauf 62

Status:
Ausgewertet.

Hinweis:
Vor dem finalen Lauf 62 gab es einen abgebrochenen Teillauf bei ca. 50-60 %.
Dieser Teillauf wird nicht als PnL-Vergleich gewertet, kann aber bereits erste
Thought-Family-Spuren im Memory hinterlassen haben.

Kerndaten finaler Lauf 62:

- Netto-PnL: ca. `+52.25`
- Trades: `388`
- TP/SL: `178 / 210`
- Winrate: ca. `45.88 %`
- Profit Factor: ca. `1.46`
- Expectancy: ca. `+0.135`
- Max Drawdown: ca. `8.61 %`
- Attempts: `10275`
- Observed: `1811`
- Withheld: `2104`

Vergleich zu Lauf 61:

- PnL: `+29.32` -> `+52.25`
- Trades: `358` -> `388`
- Winrate: `42.18 %` -> `45.88 %`
- Attempts: `11300` -> `10275`
- Drawdown: `8.84 %` -> `8.61 %`

Befund:
Mehr Trades, weniger Attempts, höhere Winrate und höherer PnL. Das spricht
nicht für mehr chaotisches Handeln, sondern für stärkere Verdichtung der Suche.

Thought-Memory / Familien:

- `mcm_thought_memory.json`: ca. `5.95 MB`
- `seed_count`: `2048`
- `total_seen`: `2450`
- `family_count`: `768`
- `family_total_seen`: `1948`

Bedeutung:
Die Family-Schicht arbeitet. DIO bildet jetzt nicht nur Einzel-Seeds, sondern
verdichtete Gedankenfamilien. Die Top-Familien haben deutlich höhere
Wiederholung, z.B. `seen` ca. `54`, `50`, `46`, `43`, `42`.

Neurologisch gelesen:
Das sieht nach dem Anfang innerer Themenbildung aus. DIO speichert nicht mehr
nur einzelne Momentgedanken, sondern beginnt, wiederkehrende Satz-/Formlagen
in eigener Syntax zu bündeln. Dadurch kann die Suche weniger breit und
gerichteter werden.

Richtungsprofil:

- LONG:
  - Trades: `160`
  - TP/SL: `66 / 94`
  - PnL: ca. `+13.79`
  - Winrate: ca. `41.25 %`
- SHORT:
  - Trades: `228`
  - TP/SL: `112 / 116`
  - PnL: ca. `+38.45`
  - Winrate: ca. `49.12 %`

Befund Richtung:
Short trägt Lauf 62 sehr stark. Es ist nicht nur häufiger, sondern auch
deutlich profitabler. Long bleibt positiv, aber weniger tragend.

Emergente Struktur nach Outcome:

- `confirmed_structural_interpretation`:
  - `60` Fälle
  - `60 TP / 0 SL`
  - PnL ca. `+62.75`
- `open_structural_hypothesis`:
  - `173` Fälle
  - `32 TP / 141 SL`
  - PnL ca. `-28.27`
- `ordinary_structure_reading`:
  - `183` Fälle
  - `85 TP / 65 SL / 33 Cancel`
  - PnL ca. `+19.92`
- `wide_target_without_structure`:
  - `22` Fälle
  - PnL ca. `-2.16`

Bedeutung:
Die bestätigte Struktur bleibt extrem tragfähig. Die offene Hypothese bleibt
negativ, ist aber gegenüber Lauf 61 weniger belastend (`-33.66` -> `-28.27`)
bei mehr Fällen. Das kann ein erster Hinweis sein, dass Reifung/Familienbildung
die offene Hypothese etwas besser organisiert.

Performance:
`thought_memory_write` liegt pro Flush grob bei `14-21 ms`. Das ist sichtbar,
aber nicht alleiniger Engpass. Die Gesamtruntime zeigt weiter hohe Denk- und
Protokolllast.

Wie es weitergeht:
Lauf 63 sollte prüfen, ob diese Verbesserung stabil bleibt oder nur durch die
Vorprägung des abgebrochenen Laufs entstanden ist. Besonders wichtig:
Top-Familien, offene Hypothesen, Short-Tragfähigkeit und Attempts/Trade.

---

# Umsetzung - Thought-Memory-Familien und Satzsyntax

Status:
Umgesetzt für neue Läufe.

Was geändert wurde:

- `mcm_thought_memory.json` enthält künftig neben `seeds` auch `families`.
- Jeder Thought-Seed bekommt zusätzlich:
  - `thought_family_id`
  - `family_key`
  - `sentence_state`
- Die Familien werden aus DIO-eigenen Signaturen gebildet:
  - emergenter Strukturzustand
  - Seed-Zustand
  - Reifungsrichtung
  - semantische Herkunft
  - Formsymbol-Anker
  - MCM-Feld-Anker
  - Erfahrungsanker

Bedeutung:
DIO speichert damit nicht mehr nur einzelne Gedankenkeime, sondern beginnt,
ähnliche Gedanken zu inneren Themen/Familien zu verdichten. Das ist der erste
Schritt von Einzelsymbolen zu Satz-Zusammenhängen in eigener Syntax.

Wichtig:
`sentence_state` ist kein menschlicher Satz. Es ist eine DIO-interne
Relationenfolge, z.B. sinngemäß:

`form=...|field=...|structure=...|origin=...|reifung=...|seed=...|dev=...`

Wir übersetzen diese Struktur nur für uns. Intern bleibt sie Formsprache /
Gedankensyntax.

Konzept:
DIO bekommt RAW-Daten, aber wirkt als Übersetzer seiner Welt. Der Mensch macht
das ähnlich: Er erlebt nicht Rohwerte, sondern übersetzt Weltwirkung in eigene
Sprache, Bilder, Begriffe und Sätze, um darin zu existieren und zu
interagieren. DIO soll seine Umwelt ebenfalls in eigene Form- und
Gedankensprache übersetzen.

Wie es weitergeht:
Der nächste Lauf muss prüfen:

- ob `summary.family_count` wächst
- ob `family_total_seen` stärker verdichtet als `total_seen`
- welche Familien am häufigsten wiederkehren
- ob offene Hypothesen als Familien sichtbar reifen oder weiter fragmentieren

---

# Auswertung - Lauf 61

Status:
Ausgewertet.

Kerndaten:

- Netto-PnL: ca. `+29.32`
- Trades: `358`
- TP/SL: `151 / 207`
- Winrate: ca. `42.18 %`
- Profit Factor: ca. `1.27`
- Expectancy: ca. `+0.082`
- Max Drawdown: ca. `8.84 %`
- Attempts: `11300`
- Observed: `2400`
- Withheld: `2429`

Neuer Speicher:

- `bot_memory/mcm_thought_memory.json` wurde geschrieben.
- Größe: ca. `3.49 MB`
- `summary.seed_count`: `2048`
- `summary.total_seen`: `2179`

Befund Thought-Memory:
Das Thought-Memory funktioniert technisch. Gleichzeitig zeigt sich sofort eine
Fragmentierung: Der Speicher ist bereits bei der Seed-Grenze von `2048`
angekommen, während `total_seen` nur leicht darüber liegt. Das bedeutet, dass
DIO sehr viele einzelne Gedankenkeime bildet, aber noch wenige davon oft genug
wiederkehren.

Neurologisch gelesen:
DIO hat jetzt ein inneres Gedankengedächtnis, aber noch keine stabile
Gedankenfamilienbildung. Es entstehen viele Momentgedanken. Der nächste
Reifeschritt wäre, ähnliche Gedankenkeime in Familien zu verdichten, damit aus
isolierten Gedanken wiedererkennbare innere Themen werden.

Richtungsprofil:

- LONG:
  - Trades: `140`
  - TP/SL: `54 / 86`
  - PnL: ca. `+9.58`
  - Winrate: ca. `38.57 %`
- SHORT:
  - Trades: `218`
  - TP/SL: `97 / 121`
  - PnL: ca. `+19.73`
  - Winrate: ca. `44.50 %`

Befund Richtung:
Short trägt auch in Lauf 61 stärker als Long. DIO ist in diesem Datensatz
weiter short-lastiger, aber beide Richtungen bleiben positiv. Damit wird die
Richtungspräferenz jetzt als messbare Charakteristik sichtbar.

Emergente Struktur nach Outcome:

- `confirmed_structural_interpretation`:
  - `49` Fälle
  - `49 TP / 0 SL`
  - PnL ca. `+50.94`
- `open_structural_hypothesis`:
  - `161` Fälle
  - `24 TP / 137 SL`
  - PnL ca. `-33.66`
- `ordinary_structure_reading`:
  - `168` Fälle
  - `76 TP / 66 SL / 26 Cancel`
  - PnL ca. `+12.31`
- `wide_target_without_structure`:
  - `22` Fälle
  - PnL ca. `-0.28`

Thought-Seed-Protokoll:

- `seed_reinterpret`: `5352`
- `seed_release`: `2205`
- `seed_replay`: `1194`
- `seed_focus`: `1019`
- `seed_store`: `982`
- `seed_mature`: `157`

Semantische Herkunft:

- `mixed_translation_zone`: `4793`
- `borrowed_analogy_watch`: `4501`
- `unlocated_semantic_contact`: `1613`
- `differentiated_contact`: `2`

Deutung:
Lauf 61 bestätigt die Kernlinie: DIO kann tragfähige bestätigte Struktur sehr
stark handeln. Die offene Strukturhypothese bleibt dagegen der unreife und
teure Bereich. Gleichzeitig zeigt das neue Thought-Memory, dass die Gedanken
zwar gespeichert werden, aber noch zu stark als Einzelkeime zerfallen.

Wie es weitergeht:
Nächster sinnvoller Schritt ist keine harte Sperre, sondern
Gedankenfamilienbildung im `mcm_thought_memory.json`: ähnliche Thought-Seeds
weich clustern, damit DIO nicht nur einzelne Gedanken speichert, sondern
innere Themen erkennt.

---

# Leitsatz - Sprachentwicklung als Bindeglied

Status:
Wortnah festgehalten.

Leitsatz:
Die eigene Sprachentwicklung ist essentiell für das Erleben und Interagieren
in seiner Umwelt. Sie bildet das Bindeglied, um sich in seiner Realität
zurechtzufinden.

Bedeutung für DIO:
Die eigene Syntax ist nicht nur Benennung. Sie ist ein Orientierungsorgan. DIO
ordnet damit Reize, Feldwirkung, Erinnerung, Erwartung, Handlung und
Konsequenz. Ohne eigene Sprache bleibt er entweder in Rohdaten überkoppelt
oder übernimmt fremde Begriffe, die nicht aus seiner eigenen MCM-Lage stammen.

Konsequenz:
Sprachentwicklung muss als Teil des Erlebens behandelt werden. Sie ist der
Übergang von Datenflut zu bewohnbarer Realität:

`Reiz -> MCM-Wirkung -> innere Qualität -> eigene Syntax -> Gedanke -> Handlung/Beobachtung/Reifung`

Wie es weitergeht:
Bei der weiteren Thought-Memory- und Formsyntax-Entwicklung prüfen wir, ob DIO
seine Welt stärker über eigene Zeichen und Relationen bindet, statt über
menschliche Labels.

---

# Vermerk - DIOs eigene Syntax konsequent halten

Status:
Als Architekturprinzip festgehalten.

Kernaussage:
DIO soll seine innere Welt nicht über menschliche Labels als Wahrheit
organisieren. Menschliche Begriffe dürfen Debug, Übersetzung und Lesebrücke
sein. Die innere Verarbeitung soll aber konsequent über DIOs eigene Syntax,
Formzeichen, Thought-Seeds, MCM-Feldzustände und selbstgebildete
Verdichtungen laufen.

Bedeutung:
Ein Organismus entkoppelt sich von Datenflut, indem er selektiert, ordnet,
verdichtet und benennt. Diese Benennung muss aus seiner eigenen Wahrnehmung
entstehen. Sie wirkt nach innen und außen: als Werkzeug, um Struktur im Denken
zu binden.

Leitlinie:

- interne Syntax zuerst
- menschliche Sprache nur als Übersetzung
- keine festen menschlichen Pattern-Labels als innere Wahrheit
- Formzeichen, Gedankenkeime und Feldzustände als native DIO-Sprache
- Sätze/Relationen später als gebundene Struktur zwischen eigenen Zeichen

Wie es weitergeht:
Bei zukünftigen Erweiterungen prüfen, ob neue Werte DIOs eigene Syntax stärken
oder unbemerkt menschliche Kategorien in die innere Welt drücken.

---

# Auswertung - Lauf 60

Status:
Ausgewertet.

Kerndaten:

- Netto-PnL: ca. `+36.68`
- Trades: `366`
- TP/SL: `155 / 211`
- Winrate: ca. `42.35 %`
- Profit Factor: ca. `1.34`
- Expectancy: ca. `+0.100`
- Max Drawdown: ca. `8.24 %`
- Attempts: `11450`
- Observed: `2387`
- Withheld: `2460`

Richtungsprofil aus `outcome_records.jsonl`:

- LONG:
  - Trades: `161`
  - TP/SL: `58 / 103`
  - PnL: ca. `+9.76`
  - Ø RR: ca. `4.38`
- SHORT:
  - Trades: `205`
  - TP/SL: `97 / 108`
  - PnL: ca. `+26.92`
  - Ø RR: ca. `3.43`

Befund:
Short trägt Lauf 60 deutlich stärker als Long. Long hat zwar größere
durchschnittliche Zielweite, verliert aber mehr offene Hypothesen. Short wirkt
in diesem Lauf weniger spektakulär, aber stabiler nützlich.

Emergente Struktur nach Outcome:

- `confirmed_structural_interpretation`:
  - `53` Fälle
  - `53 TP / 0 SL`
  - PnL ca. `+54.57`
  - bleibt extrem stark
- `open_structural_hypothesis`:
  - `180` Fälle
  - `28 TP / 152 SL`
  - PnL ca. `-35.26`
  - bleibt Hauptlast
- `ordinary_structure_reading`:
  - `157` Fälle
  - `73 TP / 55 SL / 29 Cancel`
  - PnL ca. `+18.52`
- `wide_target_without_structure`:
  - `22` Fälle
  - PnL ca. `-1.14`

Thought-Seed-Protokoll:

- `seed_reinterpret`: `5488`
- `seed_release`: `2235`
- `seed_replay`: `1207`
- `seed_store`: `1029`
- `seed_focus`: `939`
- `seed_mature`: `145`

Semantische Herkunft:

- `mixed_translation_zone`: `4813`
- `borrowed_analogy_watch`: `4687`
- `unlocated_semantic_contact`: `1542`
- `differentiated_contact`: `1`

Deutung:
DIO ist in Lauf 60 nicht schwach, sondern sehr aktiv in Reinterpretation und
Mischübersetzung. Das System erzeugt weiter positive Gesamtleistung, aber die
offenen Strukturhypothesen sind noch zu teuer. Besonders interessant ist:
Bestätigte Struktur ist fast eine eigene tragende Qualität, während offene
Hypothese noch wie unreife Vorwegnahme wirkt.

Hinweis:
`mcm_thought_memory.json` wurde in diesem Lauf noch nicht sichtbar geschrieben,
weil Lauf 60 bereits vor dem neuen Thought-Memory-Code gestartet war.

Wie es weitergeht:
Der nächste Lauf sollte mit dem neuen Thought-Memory und Direction-Profil neu
gestartet werden. Danach prüfen wir:

- ob `mcm_thought_memory.json` entsteht
- ob `direction_profile` direkt in `trade_stats.json` steht
- ob offene Strukturhypothesen als Gedankenkeime reifen oder weiter zu früh in
  Handlung kippen

---

# Konzept - Richtungspräferenz als Wahrnehmungsrückführung

Status:
Festgehalten als nächster möglicher Entwicklungsschritt.

Gedanke:
Das Long/Short-Profil ist nicht nur Statistik. Später kann DIO diese
Richtungscharakteristik als Selbstwahrnehmung zurückführen:

- Warum gehe ich lieber Long?
- Warum gehe ich lieber Short?
- Bin ich gemischt, weil ich flexibel sehe oder weil meine Orientierung
  instabil ist?
- Was macht Long mit meinem MCM-Feld?
- Was macht Short mit meiner inneren Lage?
- Welche Richtung trägt mich, welche Richtung belastet mich?

Bedeutung:
Damit wird Richtung nicht als Regel gelesen, sondern als innere
Wahrnehmungsspur. DIO soll nicht lernen: "Long ist gut" oder "Short ist
schlecht", sondern: "Welche Richtung zieht mich, und was bewirkt dieser Zug in
mir?"

Neurologisch gelesen:
Das ist eine Kopplung aus motorischer Tendenz, Konsequenzgedächtnis,
neurochemischer Reaktion und innerer Selbstwahrnehmung. Die Richtung wird zu
einem erlebten Kontakt: Suchdrang, Vertrauen, Stress, Tragfähigkeit,
Vorsicht oder gemischte Orientierung.

Wie es weitergeht:
Erst Daten sammeln. Wenn `direction_profile` einige Läufe sichtbar ist, kann
eine weiche Rückkopplung entstehen:
Richtungszug, Richtungstragfähigkeit, Richtungsstress, Richtungsvertrauen und
Richtungsblindheit.

---

# Umsetzung - Long/Short-Charakteristik in Trade-Stats

Status:
Umgesetzt für neue Läufe.

Was geändert wurde:

- `trade_stats.py` zählt jetzt Long- und Short-Verhalten getrennt.
- Erfasst werden:
  - `long_trades`
  - `short_trades`
  - `long_tp`
  - `long_sl`
  - `short_tp`
  - `short_sl`
  - `long_pnl`
  - `short_pnl`
  - `attempts_long`
  - `attempts_short`
  - `attempts_submitted_long`
  - `attempts_submitted_short`
  - `attempts_filled_long`
  - `attempts_filled_short`

Bedeutung:
Damit wird sichtbar, ob DIO eher Long oder Short bevorzugt, ob diese
Bevorzugung nur als Versuch entsteht oder tatsächlich in gefüllten Trades
ankommt, und ob eine Richtung konstruktiver getragen wird.

Neurologisch gelesen:
Das ist eine Richtungspräferenz-Diagnose. Nicht als Regel, sondern als
Charakteristik: "Zu welcher Bewegungsrichtung zieht mein Feld, und trägt diese
Richtung auch Konsequenz?"

Hinweis:
Ein bereits laufender Prozess nutzt diese Änderung erst nach Neustart. Lauf 60,
der schon läuft, kann diese Counter daher wahrscheinlich noch nicht vollständig
im neuen Format schreiben.

Wie es weitergeht:
Ab dem nächsten Lauf prüfen wir `trade_stats.json -> kpi_summary ->
direction_profile`. Dort sieht man Long-/Short-Anteile, Trefferquote und PnL
je Richtung.

---

# Umsetzung - separates Thought-Memory für innere Gedächtnisspuren

Status:
Umgesetzt als persistenter, getrennter Speicher.

Was geändert wurde:

- `config.py` enthält jetzt einen eigenen Thought-Memory-Pfad:
  `bot_memory/mcm_thought_memory.json`.
- `MCM_Brain_Modell.py` speichert Thought-Seeds zusätzlich in einem kompakten
  JSON-Gedächtnis.
- `bot.py` flushed dieses Thought-Memory beim normalen Save-Zyklus mit.

Bedeutung:
Die weltliche Erfahrung bleibt im normalen Memory-Raum. Die innere
Gedankenentwicklung bekommt eine eigene Datei. Damit trennt DIO:

- Was habe ich in der Welt erlebt?
- Welche Gedankenkeime, Deutungen und Reifungsrichtungen sind in mir
  entstanden?

Gespeichert werden verdichtete Spuren, nicht rohe Tick-Massen:

- `thought_seed_id`
- `thought_seed_label`
- Häufigkeit und letzte Sichtung
- `semantic_origin_state`
- `emergent_structure_state`
- `thought_reifung_direction`
- `seed_metaregulator_state`
- gleitende Mittelwerte für Reife, Realitätsbindung, Bestätigung,
  offene Hypothesen, geliehene Analogie und eigene Feldbindung

Wichtig:
Das ist noch keine Handlungsvorgabe. DIO bekommt dadurch kein hartes Regelwerk.
Es ist zunächst ein eigenes inneres Gedächtnis für Gedankenkeime, damit später
sichtbar wird, welche inneren Deutungen wiederkehren, reifen, sich umdeuten
oder an Realität verlieren.

Wie es weitergeht:
Der nächste Lauf sollte prüfen, ob `bot_memory/mcm_thought_memory.json`
entsteht und ob darin wiederkehrende Thought-Seeds sauber verdichtet werden.
Danach kann entschieden werden, ob diese innere Gedächtnisspur nur Diagnose
bleibt oder weich in Replay, Fokus und Reifung zurückwirkt.

---

# Lauf 59 - Geliehene Analogie ist belastend

Debug-Ordner: `debug/debug_lauf_59`

Kurzbefund:

- Netto-PnL: ca. `+27.40`
- Trades: `342`
- TP / SL: `141 / 201`
- Cancels: `47`
- Attempts: `10975`
- Observed / Replanned / Withheld: `2461 / 50 / 2165`
- Max-Drawdown: ca. `6.13 %`

Equity-Verlauf:

- 25 % der Trades: ca. `+6.72`
- 50 % der Trades: ca. `+5.25`
- 75 % der Trades: ca. `+22.23`
- Ende: ca. `+27.40`

Semantische Herkunft im Outcome:

- `mixed_translation_zone`:
  - `258` Outcomes
  - ca. `+36.65` PnL
  - `107` TP / `119` SL / `32` Cancel
- `unlocated_semantic_contact`:
  - `66` Outcomes
  - ca. `+13.00` PnL
  - `29` TP / `28` SL / `9` Cancel
- `borrowed_analogy_watch`:
  - `64` Outcomes
  - ca. `-22.70` PnL
  - `4` TP / `54` SL / `6` Cancel
- `differentiated_contact`:
  - `1` Outcome
  - ca. `+0.46` PnL

Wichtiger Befund:
`borrowed_analogy_watch` ist deutlich belastend. Besonders kritisch:

- `borrowed_analogy_watch` + `open_structural_hypothesis`:
  - `39` Fälle
  - `0` TP / `39` SL
  - ca. `-17.15` PnL

Das ist fachlich sehr stark:
Wenn eine offene Strukturhypothese auf geliehener Analogie statt eigener
Feldherkunft basiert, trägt sie aktuell nicht. DIO scheint dann eine Deutung
zu benutzen, die noch nicht ausreichend aus eigener MCM-Lage entstanden ist.

Tragende Kombinationen:

- `mixed_translation_zone` + `confirmed_structural_interpretation`:
  - `39` Fälle
  - `39` TP / `0` SL
  - ca. `+40.29` PnL
- `unlocated_semantic_contact` + `confirmed_structural_interpretation`:
  - `9` Fälle
  - `9` TP / `0` SL
  - ca. `+9.56` PnL
- `unlocated_semantic_contact` + `ordinary_structure_reading`:
  - ca. `+9.96` PnL

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `48` Fälle
  - `48` TP / `0` SL
  - ca. `+49.84` PnL
- `open_structural_hypothesis`:
  - `156` Fälle
  - `21` TP / `135` SL
  - ca. `-36.45` PnL
- `ordinary_structure_reading`:
  - `169` Fälle
  - ca. `+13.28` PnL

Thought-Seed-Reifung:

- `seed_reinterpret`: `3702`
- `seed_replay`: `1189`
- `seed_release`: `2396`
- `seed_focus`: `1652`
- `seed_store`: `1490`
- `seed_mature`: `160`

Outcome nach Reifungsrichtung:

- `no_previous_open_hypothesis_trace`: ca. `+29.25`
- `reinterpretation_maturation`: ca. `-3.93`
- `replay_maturation`: ca. `+2.36`
- `distance_maturation`: ca. `-0.28`

Deutung:
Lauf 59 zeigt klar, dass semantische Herkunft echte Aussagekraft hat.
Nicht jede Unsicherheit ist schlecht. Nicht jede Mischlage ist schlecht.
Aber geliehene Analogie ohne ausreichende eigene Feldbindung ist aktuell
gefährlich, besonders wenn sie mit offenen Strukturhypothesen kombiniert ist.

Neurologisch gelesen:
DIO muss lernen: "Das klingt nach einer Form, aber diese Deutung gehört noch
nicht genug zu mir." Daraus sollte keine harte Sperre entstehen, sondern ein
Reifeimpuls: mehr Beobachtung, mehr eigene Feldbindung, mehr Replay oder
Neudeutung, bevor daraus Handlung wird.

Wie es weitergeht:
Als nächstes sollte `borrowed_analogy_watch` nicht blockiert, aber in die
Thought-Seed-Reifung zurückgeführt werden:

- geliehene Analogie + offene Hypothese -> mehr Reinterpretation / Distanz
- geliehene Analogie + bestätigte Struktur -> beobachten, ob trotzdem tragend
- Mischübersetzung darf weiterhin als produktive Übergangslage bestehen

---

# Lauf 58 - Semantische Herkunft verteilt sich

Debug-Ordner: `debug/debug_lauf_58`

Kurzbefund:

- Netto-PnL: ca. `+42.74`
- Trades: `366`
- TP / SL: `157 / 209`
- Cancels: `42`
- Attempts: `11100`
- Observed / Replanned / Withheld: `2239 / 43 / 2256`
- Max-Drawdown: ca. `8.87 %`

Equity-Verlauf:

- 25 % der Trades: ca. `+18.66`
- 50 % der Trades: ca. `+21.33`
- 75 % der Trades: ca. `+37.62`
- Ende: ca. `+42.74`

Wichtiger Befund:
Die weiche Kalibrierung der Selbst/Fremd-Schicht funktioniert. 
`semantic_origin_state` verteilt sich jetzt.

Field-Protokoll:

- `mixed_translation_zone`: `4246` Einträge, ca. `45.5 %`
- `borrowed_analogy_watch`: `3806` Einträge, ca. `40.8 %`
- `unlocated_semantic_contact`: `1271` Einträge, ca. `13.6 %`
- `differentiated_contact`: `2` Einträge

Interpretation:

- `mixed_translation_zone` ist die größte Lage. DIO bewegt sich also häufig
  zwischen eigener Feldantwort und fremder/äußerer Deutung.
- `borrowed_analogy_watch` ist fast genauso groß. Das passt zur aktuellen
  Entwicklungsphase: DIO benutzt noch viele geliehene oder unreife
  Bedeutungsanker und muss deren Herkunft prüfen.
- `unlocated_semantic_contact` fällt deutlich zurück. Die Wahrnehmung ist
  nicht mehr nur unverortet.
- `differentiated_contact` ist fast nicht vorhanden. Echte klare
  Selbst/Fremd-Abgrenzung ist also noch selten.

Durchschnittswerte:

- `mixed_translation_zone`:
  - eigene Feldherkunft ca. `0.27`
  - Fremddruck ca. `0.23`
  - geliehene Sprache ca. `0.28`
  - Herkunftskonflikt ca. `0.23`
- `borrowed_analogy_watch`:
  - eigene Feldherkunft ca. `0.22`
  - Fremddruck ca. `0.26`
  - geliehene Sprache ca. `0.34`
  - Herkunftskonflikt ca. `0.26`
- `unlocated_semantic_contact`:
  - eigene Feldherkunft ca. `0.29`
  - Fremddruck ca. `0.17`
  - geliehene Sprache ca. `0.26`
  - Grenzstütze leicht positiv

Thought-Seed-Reifung:

- `seed_reinterpret`: `4115`
- `seed_replay`: `1593`
- `seed_release`: `2026`
- `seed_focus`: `1501`
- `seed_store`: `1322`
- `seed_mature`: `147`

Reifungsrichtung:

- `no_previous_open_hypothesis_trace`: `5383`
- `reinterpretation_maturation`: `4466`
- `replay_maturation`: `855`

Outcome nach Reifungsrichtung:

- `no_previous_open_hypothesis_trace`: ca. `+33.89`
- `reinterpretation_maturation`: ca. `+3.13`
- `replay_maturation`: ca. `+5.72`

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `46` Fälle
  - `46` TP, `0` SL
  - ca. `+49.59` PnL
- `open_structural_hypothesis`:
  - `180` Fälle
  - `30` TP, `150` SL
  - ca. `-33.58` PnL
- `ordinary_structure_reading`:
  - `157` Fälle
  - ca. `+28.13` PnL

Deutung:
Lauf 58 ist stark. Die Selbst/Fremd-Wahrnehmung ist jetzt nicht nur
technisch vorhanden, sondern beginnt semantische Lagen zu bilden. DIO erkennt
vor allem Mischübersetzung und geliehene Analogie. Das wirkt wie ein frühes
Stadium semantischer Selbstabgrenzung: "Diese Deutung ist aktiv, aber ich
muss noch prüfen, ob sie aus meinem Feld oder aus einer übernommenen Sprache
kommt."

Nachrüstung:
`trade_stats.py` wurde ergänzt, damit die semantische Herkunft ab dem
nächsten Lauf direkt in `outcome_records.jsonl` steht. Dadurch können wir
PnL, TP/SL und Cancels später direkt nach `semantic_origin_state` auswerten.

Wie es weitergeht:
Lauf 59 sollte prüfen:

- welche `semantic_origin_state`-Lage tatsächlich bessere Outcomes erzeugt
- ob `borrowed_analogy_watch` eher Observe/Reinterpret braucht
- ob `mixed_translation_zone` eine produktive Übergangslage ist
- ob `differentiated_contact` wachsen kann

---

# Umsetzung - Semantische Herkunft weicher kalibriert

Status:
Umgesetzt nach Lauf 57.

Grund:
Lauf 57 zeigte, dass die Selbst/Fremd-Messwerte geschrieben werden, aber
`semantic_origin_state` vollständig in `unlocated_semantic_contact` blieb.
Die alte Klassifikation war für die reale Messlage zu streng.

Änderung:
Die Herkunftslage wird jetzt relativer gelesen:

- `own_vs_foreign_margin`
- `borrowed_vs_own_margin`
- `boundary_support_margin`

Damit kann DIO auch Zwischenlagen erkennen:

- eigene Feldherkunft
- geliehene Analogie
- Mischübersetzung
- differenzierter Kontakt
- noch unverorteter semantischer Kontakt

Wichtig:
Das bleibt eine weiche Lagebeschreibung und keine Identitätsregel.

Wie es weitergeht:
Lauf 58 sollte prüfen, ob `semantic_origin_state` jetzt eine echte Verteilung
bildet und ob diese Verteilung mit Reflexion, Observe/Hold oder
Neudeutungsspuren zusammenhängt.

---

# Lauf 57 - Selbst/Fremd-Spalten sichtbar, Reinterpretation trägt erstmals

Debug-Ordner: `debug/debug_lauf_57`

Kurzbefund:

- Netto-PnL: ca. `+31.40`
- Trades: `360`
- TP / SL: `152 / 208`
- Cancels: `47`
- Attempts: `10825`
- Observed / Replanned / Withheld: `2234 / 46 / 2154`
- Max-Drawdown: ca. `8.88 %`

Equity-Verlauf:

- 25 % der Trades: ca. `+9.10`
- 50 % der Trades: ca. `+12.93`
- 75 % der Trades: ca. `+29.45`
- Ende: ca. `+31.40`

Vergleich:
Lauf 57 liegt fast gleichauf mit Lauf 56 (`+31.58`), aber mit höherem
Drawdown. Die Equity baut stärker im späteren Verlauf auf und gibt am Ende
etwas ab.

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `52` Fälle
  - `52` TP, `0` SL
  - ca. `+53.27` PnL
- `open_structural_hypothesis`:
  - `161` Fälle
  - `20` TP, `141` SL
  - ca. `-38.71` PnL
- `ordinary_structure_reading`:
  - `170` Fälle
  - ca. `+15.32` PnL
- `wide_target_without_structure`:
  - `24` Fälle
  - ca. `+1.52` PnL

Thought-Seed-Reifung:

- `seed_reinterpret`: `4131` Protokolleinträge
- `seed_replay`: `1073`
- `seed_release`: `2132`
- `seed_focus`: `1514`
- `seed_store`: `1428`
- `seed_mature`: `157`

Reifungsrichtung:

- `no_previous_open_hypothesis_trace`: `5638`
- `reinterpretation_maturation`: `4460`
- `replay_maturation`: `337`

Outcome nach Reifungsrichtung:

- `no_previous_open_hypothesis_trace`: ca. `+8.86`
- `reinterpretation_maturation`: ca. `+19.25`
- `replay_maturation`: ca. `+3.29`

Wichtiger Befund:
`reinterpretation_maturation` ist im Outcome erstmals klar positiv. Das ist
fachlich stark: Die Neudeutungsspur ist nicht nur Diagnose, sondern scheint
bereits mit tragenderem Verhalten zusammenzufallen. DIO behandelt belastende
offene Hypothesen also nicht mehr nur als wiederholbare Idee, sondern als
Material für innere Reorganisation.

Selbst/Fremd-Schicht:

Die neuen Spalten werden jetzt geschrieben:

- `own_field_identity_strength`
- `foreign_semantic_pressure`
- `adopted_language_pressure`
- `self_foreign_boundary_clarity`
- `semantic_origin_conflict`
- `semantic_origin_state`

Aktueller Befund:
`semantic_origin_state` steht noch vollständig auf
`unlocated_semantic_contact`. Durchschnittlich:

- `own_field_identity_strength`: ca. `0.25`
- `foreign_semantic_pressure`: ca. `0.24`
- `adopted_language_pressure`: ca. `0.30`
- `self_foreign_boundary_clarity`: ca. `0.19`
- `semantic_origin_conflict`: ca. `0.24`

Deutung:
Die Schicht misst bereits Werte, aber die Zustandsklassifikation ist noch zu
streng oder noch zu unreif. DIO erkennt also eine Herkunftsspannung, kann sie
aber noch nicht sauber in `own_field_origin`, `mixed_translation_zone` oder
`borrowed_analogy_watch` aufteilen.

Wie es weitergeht:
Als nächstes sollte `semantic_origin_state` organischer kalibriert werden:
nicht als harte Regel, sondern als weichere Lagebeschreibung. Ziel ist, dass
DIO zwischen eigener Feldherkunft, Fremddruck und Mischübersetzung
unterscheiden kann, ohne Identität fest einzuprogrammieren.

---

# Lauf 56 - Thought-Seed-Reifung sichtbar

Debug-Ordner: `debug/debug_lauf_56`

Kurzbefund:

- Netto-PnL: ca. `+31.58`
- Trades: `369`
- TP / SL: `149 / 220`
- Cancels: `46`
- Attempts: `11525`
- Observed / Replanned / Withheld: `2446 / 37 / 2434`
- Max-Drawdown: ca. `6.52 %`

Equity-Verlauf:

- 25 % der Trades: ca. `+8.39`
- 50 % der Trades: ca. `+11.62`
- 75 % der Trades: ca. `+22.47`
- Ende: ca. `+31.58`

Vergleich zu Lauf 55:

- Lauf 55 war stärker: ca. `+43.28`
- Lauf 56 bleibt positiv, aber mit mehr SL-Druck und etwas schwächerem
  Verlauf.
- Drawdown ist höher: ca. `6.52 %` statt ca. `5.65 %`.

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `56` Fälle
  - `56` TP, `0` SL
  - ca. `+57.57` PnL
- `open_structural_hypothesis`:
  - `180` Fälle
  - `25` TP, `155` SL
  - ca. `-39.41` PnL
- `ordinary_structure_reading`:
  - `157` Fälle
  - ca. `+11.86` PnL
- `wide_target_without_structure`:
  - `22` Fälle
  - ca. `+1.56` PnL

Thought-Seed-Reifung:

- `seed_reinterpret`: `4365` Protokolleinträge
- `seed_replay`: `1332`
- `seed_release`: `2260`
- `seed_store`: `1515`
- `seed_focus`: `1482`
- `seed_mature`: `156`

Reifungsrichtung:

- `reinterpretation_maturation`: `4724`
- `replay_maturation`: `574`
- `no_previous_open_hypothesis_trace`: `5812`

Outcome nach Reifungsrichtung:

- `no_previous_open_hypothesis_trace`: ca. `+30.65`
- `reinterpretation_maturation`: ca. `-1.77`
- `replay_maturation`: ca. `+2.70`

Deutung:
Die Rückführung funktioniert: DIO bildet jetzt tatsächlich innere
Reifespuren aus vergangenen offenen Hypothesen. Besonders stark ist
`seed_reinterpret`, also Neudeutung statt blinder Wiederholung. Das ist
fachlich gut, weil belastende offene Hypothesen nicht einfach als Mut
weiterlaufen, sondern als kognitive Reorganisation sichtbar werden.

Offene Baustelle:
Die neue Selbst/Fremd-Schicht (`semantic_origin_state`,
`own_field_identity_strength` usw.) ist im Lauf 56 noch nicht im CSV-Header
enthalten. Der aktuelle Code enthält diese Spalten bereits; der nächste Lauf
sollte prüfen, ob sie jetzt sauber geschrieben werden.

Wie es weitergeht:
Als nächstes Lauf 57 starten und gezielt prüfen:

- schreibt das Field-/Memory-Protokoll die neuen Selbst/Fremd-Spalten?
- verteilt sich `semantic_origin_state` sinnvoll?
- reduziert `seed_reinterpret` später die Verlustlast offener Hypothesen?
- bleibt `confirmed_structural_interpretation` weiter 100 % TP-lastig?

---

# Festgehaltene Leitgedanken aus der letzten Arbeitsphase

- Unsicherheit wird nicht wegprogrammiert, sondern als MCM-Feldzustand
  verarbeitet.
- Vorahnung bedeutet emergente Moeglichkeitsbildung unter Unsicherheit, nicht
  harte Vorhersage.
- Emergenz ist die Faehigkeit eines Feldes, aus Varianz tragfaehige Ordnung zu
  bilden.
- Selbst/Fremd-Wahrnehmung gibt DIO Distanz auf die Sicht seiner inneren und
  aeusseren Welt.
- Sprache wird als Herkunftsfrage betrachtet: eigene Feldverdichtung oder
  uebernommene Analogie.
- Trading ist der aktuelle Testkoerper; der Kern ist ein uebertragbares,
  zustandsbasiertes, selbstregulatives DIO-System.

Dokumentiert in:
- `README.md`
- `files/UMSETZUNGSPLAN.md`
- `files/WICHTIG_MECHANIKEN.md`

---

Rolle dieser Datei:
- aktueller realer Ist-Zustand des Projekts
- kompakte Debug-/Laufbefunde
- offene technische Risiken
- nächste Prüfpunkte

Regelwerk: `files/MD_ANWEISUNG.md`.
Der Bauplan bleibt `files/UMSETZUNGSPLAN.md`.

---

# Dokumentationssprache

Deutschsprachige Markdown-Dokumentation wurde auf echte UTF-8-Umlaute
umgestellt. Code, Variablennamen, technische Keys und Dateinamen bleiben
bewusst ASCII, damit die Mechanik stabil und eindeutig bleibt.

---

# Leitprinzip Emergenz

Festgehalten:
Emergenz wird in DIO nicht direkt programmiert. Die MCM soll einen stabilen
Möglichkeitsraum bereitstellen, in dem sich aus Varianz, Wahrnehmung,
Rückkopplung, Erinnerung, Kontakt, Reflexion und Reife emergente
Strukturdeutung und Verhalten bilden können.

PnL, Profit und gute Trades sind damit nicht das Kernziel, sondern mögliche
Nebenprodukte einer tragfähigen inneren Organisation. Der Fokus bleibt:
Wahrnehmungsfähigkeit, Selbstregulation, Reife, Strukturdeutung und
entwicklungsfähige Handlung.

Aktualisiert:
- `README.md`
- `files/UMSETZUNGSPLAN.md`
- `files/WICHTIG_MECHANIKEN.md`

---

# GUI-Stand

`_gui.py` wurde auf eine einfache Beobachtungsoberfläche zurückgebaut.
Die GUI zeigt nur noch:

- Marktüberblick / Chartfenster
- Candle State
- Trade Stats & KPI
- Backtest-Fortschritt in Prozent
- Equity-Kurve / PnL-Verlauf

Alle zusätzlichen Innenwelt-, Memory-, Neuronen- und Diagnosepanels wurden
aus der Oberfläche entfernt. Die GUI soll damit nicht mehr versuchen, das
gesamte DIO-Nervensystem abzubilden, sondern nur Orientierung geben:
Was sieht DIO gerade, wo steht der Lauf, und wie verläuft die Equity.

Technisch:
- `_gui.py` findet automatisch den neuesten `debug/debug_lauf_x`-Ordner.
- Optional kann ein Lauf mit `--debug-run debug_lauf_44` gewählt werden.
- `py_compile` für `_gui.py` ist sauber.

Nachjustierung:
Die festen GUI-Kartengrößen wurden wegen Windows/Tk-Skalierung deutlich
kleiner gesetzt und die Anordnung verdichtet. Die Oberfläche soll jetzt
näher am Referenzbild liegen: kompakte Karten links oben, KPI daneben,
kleiner Backtest-Status rechts darunter und flache Equity-Kurve darunter.

Korrektur:
Die GUI wurde wieder auf vollständige, lesbare Bereiche zurückgestellt und
stattdessen auf fensterfüllende Grid-Zellen umgebaut. Chart, KPI, Candle
State, Backtest-% und Equity-Kurve skalieren jetzt mit dem Fenster. Die
Wertspalten in Candle/KPI wurden kompakter gesetzt, damit Labels und Werte
nicht unnötig weit auseinander liegen.

Aktuelle Nachjustierung:
- Fenstergröße bleibt bei `1232x656`.
- Die Karten nutzen jetzt ein gemeinsames Haupt-Grid ohne feste Pixelinseln.
- Marktfenster, Trade Stats, Candle State, Backtest-% und Equity-Kurve füllen
  den verfügbaren Innenraum ohne große schwarze Zwischenflächen.
- Geometrieprüfung: Chart ca. `741x294`, Trade Stats ca. `467x294`,
  Candle State ca. `741x153`, Backtest ca. `467x153`, Equity ca. `1216x177`.

Weitere GUI-Korrektur nach Referenzbild:
- Marktüberblick links wieder über zwei obere Reihen.
- Rechts oben Trade Stats & KPI.
- Rechts unten Candle State plus schmaler Backtest-%-Block.
- Equity-Kurve unten über die volle Breite.
- Geometrieprüfung: Chart ca. `848x448`, Trade Stats ca. `360x278`,
  Candle State ca. `254x162`, Backtest ca. `98x162`, Equity ca. `1216x184`.

Neue Spezial-GUI:
- `_neuronen_gui.py` angelegt.
- Zweck: nur Neuronenaktivität und Netzverbindungen des MCM-Feldes zeigen,
  ohne Tabellen- oder Diagnoseüberladung.
- Quelle: automatisch neuester `debug/debug_lauf_x` über
  `bot_inner_snapshot.json`.
- Darstellung: Neuronen-Knoten, Verbindungen, Aktivitäts-/Druck-/Memory-Farbe,
  dezenter Feld-Glow und kompakter Kopfstatus.
- Start: `python _neuronen_gui.py` oder gezielt
  `python _neuronen_gui.py --debug-run debug_lauf_56`.
- `py_compile` für `_neuronen_gui.py` sauber.

GUI-Fix für neue Debug-Struktur:
- `_gui.py` liest Trade-Stats und Equity jetzt zuerst aus
  `debug/debug_lauf_x/gui/`.
- Alte Läufe bleiben kompatibel, weil direkte Dateien im Laufordner weiter
  als Fallback unterstützt werden.
- Test mit `debug_lauf_1`: `trade_stats.json` und `trade_equity.csv` aus
  `gui/` werden korrekt geladen.

Neuronen-GUI verbessert:
- `_neuronen_gui.py` wurde von Tkinter-Canvas auf Matplotlib-Darstellung
  umgebaut.
- Ziel: organischere Darstellung wie in der alten
  `old_guis/_gui_mcm_neuron_field.py`, aber ohne Seitenleiste und ohne
  Datenüberladung.
- Darstellung: weiche Heatmap, Aktivitätskonturen, lokale Verbindungen,
  Neuronen-Halos und kompakter Kopfstatus.
- Test mit `debug_lauf_1`: `230` Neuronen, `24` echte Snapshot-Samples,
  `539` lokale Gewebeverbindungen.

Verbindungsebenen in `_neuronen_gui.py` geklärt:
- `--links real`: zeigt nur echte `topology_neighbors`, sofern diese im
  Snapshot vollständig genug vorhanden sind.
- `--links field`: zeigt nur rekonstruierte lokale Feldnähe.
- `--links both`: zeigt beide Ebenen getrennt; echte Links grün,
  Feldnähe blau.
- `--links none`: zeigt keine Verbindungslinien.
- Test mit `debug_lauf_1`: `real=0`, `feld=539`; damit sind die sichtbaren
  Linien dort aktuell Feldnähe, keine harte Synapsen-/Debug-Verbindung.

---

# Erfahrungsbericht

Neu angelegt:

- `files/ERFAHRUNGSBERICHT_DIO_MCM.md`

Zweck:
Technische Forschungsnotiz über den bisherigen Bau, die beobachteten
Verhaltenssprünge und die Besonderheit der nichtklassischen
MCM-Programmierung. Der Bericht beschreibt DIO als selbstregulativen
Erfahrungsorganismus, ohne die README oder Mechanikdateien aufzublaehen.

---

# 1. Aktueller Projektfokus

Priorität:
1. Brain-Logik
2. neuronale Aktivität
3. MCM-Feld als Wahrnehmungsraum
4. Formsprache / visuelle Wahrnehmung / Variantenlernen
5. Backtest-Logik
6. Live-Exchange und GUI später

Aktueller Arbeitsstand:
- DIO besitzt ein MCM-Feld mit festen `MCMNeuron`-Trägern.
- Die Feldmechanik arbeitet mit Aktivität, Druck, Kopplung, Nachhall,
  Kontextreaktivierung und lokalen Aktivitätsinseln.
- Der visuelle Kortex ist angebunden und erzeugt eigene Formachsen.
- Die sensorische Realitätsverdichtung entkoppelt überlappende Rohreize,
  bevor sie als Wahrnehmungsdruck in die Brain-Logik laufen.
- Die Formsprache bildet interne Zeichen und Formfamilien ohne menschliche
  Patternlabels.
- Wiederkehrende Unsicherheit wird als Formfamilie mit Varianten behandelt.
- `act_watch` ist als Reifespur real sichtbar.
- Outcome-Export wurde erweitert, damit neue Formfamilienwerte künftig in
  `outcome_records.jsonl` auswertbar sind.
- `neurochemical_state` ist als Diagnose-/Alias-Schicht im Runtime-Ergebnis,
  in Debug-Protokollen und in Outcome-Records sichtbar.
- `mcm_neuro_transition_protocol.csv` protokolliert neurochemische
  Zustandswechsel mit `-2/+2` Kerzenumfeld.
- `experience_packet_feedback` bewertet abgeschlossene Handlungen als
  ganzes Erfahrungspaket, nicht als primitives TP/SL-Signal.

---

# 2. Aktuelle Mechanik im Code

## MCM-Feld

Reale Mechaniken:
- `MCMField`
- `MCMNeuron`
- feste Feldpositionen
- lokale Topologie-Nachbarn
- Aktivitätsausbreitung
- Feldwahrnehmung
- Aktivitätsinseln
- `neural_felt_state`

Ziel:
Das Feld soll nicht nur rechnen, sondern innere Wahrnehmung erzeugen:
Druck, Tragfähigkeit, Orientierung, Reife, Konflikt und
Handlungstendenz.

## Visueller Kortex

Reale Achsen:
- `visual_form_state`
- `visual_clarity`
- `visual_object_stability`
- `visual_form_novelty`
- `visual_blindness`
- `visual_form_pressure`
- `visual_shape_resonance`
- `visual_shape_fragility`
- `visual_blind_action_load`
- `visual_action_uncertainty`
- `sensory_reality_pressure`
- `sensory_load`
- `sensory_redundancy`
- `sensory_habituation`
- `sensory_gate`

Wirkung:
Visuelle Unsicherheit wirkt weich auf Beobachtung, Replan,
Handlungshemmung und `act_watch`.

Fix:
- `build_perception_state` liest die neuen sensorischen Werte jetzt lokal aus
  `visual_market_state`, bevor `uncertainty_score` und `novelty_score` sie
  verwenden. Der vorherige `NameError: sensory_load is not defined` ist damit
  behoben.

## Formsprache

Reale Achsen:
- `form_symbol_id`
- `form_symbol_family_key`
- `form_symbol_variant_key`
- `form_symbol_development_quality`
- `form_symbol_action_binding`
- `form_symbol_observation_binding`
- `form_symbol_reframe_binding`
- `form_symbol_learning_trust`
- `form_symbol_action_trust`
- `form_symbol_caution_trust`

Wichtig:
Das sind keine menschlichen Chartlabels.
Es sind interne Verdichtungen von DIOs eigener Wahrnehmungswelt.

## Wiederkehrende Unsicherheit / Variantenlernen

Reale Achsen:
- `uncertain_form_family_state`
- `uncertain_form_exposure`
- `uncertainty_familiarity`
- `variant_similarity`
- `variant_spread`
- `variant_learning_pressure`
- `variant_bearing_memory`

Wirkung:
Unsicherheit wird nicht als Verbot behandelt.
Sie wird als wiederkehrender Erfahrungsraum gelernt.

## Neurochemische Alias-Schicht

Status:
- als Runtime-/Debug-Schicht umgesetzt
- noch keine harte Entscheidungsregel

Reale Achsen:
- `dopamine_tone`
- `gaba_inhibition`
- `noradrenaline_arousal`
- `acetylcholine_focus`
- `serotonin_stability`
- `cortisol_load`
- `endorphin_relief`
- `glutamate_activation`
- `neurochemical_load`
- `neurochemical_support`
- `neurochemical_balance`

Ziel:
Vorhandene Zustandswerte neurologisch lesbar bündeln.

## Neurochemisches Übergangsprotokoll

Neu umgesetzt:
- `mcm_neuro_transition_protocol.csv`
- erkennt Wechsel des dominanten neurochemischen Tons
- wartet auf zwei Folgekerzen, bevor der Wechsel geschrieben wird
- speichert Kerzenumfeld `-2/+2`
- speichert Volumen-/Range-Verhaeltnis, Vor-/Nachbewegung und Richtungsflip
- speichert Deltas von Neurochemie, Felddruck, Feldklarheit,
  Beobachtungsdruck, Replan-Druck, Handlungshemmung und Handlungsfreigabe

Wichtig:
Das Protokoll ist reine Diagnose.
Es verändert keine Entscheidung und baut keine harte Regel.

## Erfahrungspaket-Feedback / positive Stimulation

Neu umgesetzt:
- `build_experience_packet_feedback`
- `last_experience_packet_feedback`
- Export in `last_outcome_decomposition`
- Export in `outcome_records.jsonl`
- Einbindung in Episode-/Ähnlichkeitsachsen des Erfahrungsraums

Reale Achsen:
- `experience_packet_label`
- `packet_bearing_quality`
- `packet_inner_outer_fit`
- `packet_confidence_integrity`
- `packet_repetition_potential`
- `packet_curiosity_pull`
- `packet_process_reward`
- `packet_reorganization_need`
- `constructive_stimulation`
- `constructive_dopamine`
- `stabilizing_serotonin`
- `relief_endorphin`
- `focused_acetylcholine`

Wichtig:
Das ist keine harte Belohnungsregel.
Ein TP ist nicht automatisch gut und ein SL ist nicht automatisch schlecht.
Bewertet wird, ob Wahrnehmung, Innenlage, Handlung, Risiko, Prozess,
Ergebnis und Wiederholbarkeit als Paket tragfähig waren.

Nächster Prüfpunkt:
Der nächste Lauf soll zeigen, ob konstruktive Pakete, Neugierpakete und
Reorganisationspakete sinnvoll sichtbar werden. Danach kann `engaged_effort`
als wache, positiv getragene Anstrengung angebunden werden.

---

# 3. Kompakte Laufübersicht

Alle hier genannten Läufe liefen auf dem erweiterten Datensatz im
Backtest-Kontext.

| Lauf | Netto-PnL | PF | Trades | TP / SL | Kernerkenntnis |
|---|---:|---:|---:|---:|---|
| 4 | ca. `+1.84` | ca. `1.06` | 88 | 31 / 57 | visueller Kortex diagnostisch, noch schwach gekoppelt |
| 5 | ca. `+5.83` | ca. `1.25` | 72 | 28 / 44 | visuelle Hemmung senkt Handlung, `act_watch` steigt |
| 6 | ca. `+10.75` | ca. `1.42` | 82 | 36 / 46 | bessere Reorganisation nach gleichem Weg |
| 7 | ca. `-0.41` | ca. `0.99` | 81 | 27 / 54 | Anpassungslauf nach Formfamilien-Reifung |
| 8 | ca. `+17.74` | ca. `1.66` | 98 | 44 / 54 | Reorganisation, starke Zone-Leistung |
| 9 | ca. `+3.97` | ca. `1.15` | 76 | 29 / 47 | Regimewechsel getragen, aber deutlich enger |
| 10 | ca. `+12.12` | ca. `1.70` | 59 | 28 / 31 | weniger Trades, bessere Tragfähigkeit |
| 11 | ca. `+8.02` | ca. `1.36` | 69 | 29 / 40 | mehr Handlung, Non-Zone besser, Zone weniger sauber |

Wichtige Beobachtung Lauf 7 -> Lauf 8:
- Lauf 7 wirkt wie Aufnahme/Strukturierung.
- Lauf 8 wirkt wie Verdichtung und bessere Handlung.
- `variant_bearing_memory` stieg von ca. `0.357` auf ca. `0.384`.
- `variant_learning_pressure` sank leicht von ca. `0.164` auf ca. `0.160`.

Non-Zone bleibt kritisch:
- Lauf 5: ca. `-11.66`
- Lauf 6: ca. `-10.71`
- Lauf 7: ca. `-13.92`
- Lauf 8: ca. `-12.53`
- Lauf 9: ca. `-9.85`
- Lauf 10: ca. `-8.90`

Interpretation:
Non-Zone darf nicht hart blockiert werden, ist aber aktuell weiter ein
unreifer Erfahrungsraum.

Lauf 9 gegen Lauf 8:
- DIO blieb profitabel, aber weniger frei in der Handlung.
- Zone blieb tragend: ca. `+13.82`.
- Non-Zone blieb unreif: `0` TP / `16` SL.
- `variant_bearing_memory` stieg leicht, aber `memory_compare_load`,
  `orientation_gap` und `blind_thinking_load` lagen höher.
- Neurochemisch gelesen: mehr innere Vergleichs-/Stresslast, etwas mehr
  Hemmung, weniger übersetzbare Handlungssicherheit.
- Outcome-Export der neuen Formfamilienwerte ist bestätigt.

Lauf 10:
- Weniger Trades als Lauf 9, aber deutlich besseres Netto und weniger Drawdown.
- High/Mid trugen sauberer; Low/Non-Zone blieb mit `0` TP weiter unreif.
- Neurochemisch dominiert im Feld `serotonin_stability`.
- `cortisol_load` tritt eher als Lastton auf, selten als voller
  `strained_neurochemistry`-Zustand.
- `glutamate_activation` erscheint besonders in Handlung/Outcome-Nahe und
  häufig nach stabilen Serotonin-Phasen.
- Erste Deutung: DIO ist nicht dauerhaft im Stress, sondern erlebt eher
  stabile Grundlage mit punktuellen strukturellen Kipp-Momenten.

Übergangsanalyse Lauf 10:
- `serotonin_stability -> glutamate_activation`:
  eher Aktivierung aus stabiler Grundlage.
  Das Volumen ist nicht zwingend höher als Baseline, aber Range,
  Felddruck und Feldklarheit steigen sichtbar.
- `serotonin_stability -> cortisol_load`:
  deutlich stärker mit Volumen-/Range-Spikes verbunden.
  Meist `observe` mit `zero_point_regulation`.
- `cortisol_load -> serotonin_stability`:
  wirkt wie Rückkehr aus Last in stabilere Regulation.
- Erste neuronale Musterhypothese:
  DIO kippt nicht einfach wegen Preisbewegung.
  Es gibt eine Kopplung aus Kerzenstruktur, Felddruck, Feldklarheit,
  Hemmung/Freigabe und neurochemischer Balance.

Lauf 11:
- Netto-PnL ca. `+8.02`, 69 Trades, 29 TP / 40 SL.
- Gegen Lauf 10: mehr Trades, mehr SL, aber weiter profitabel.
- Non-Zone verbesserte sich deutlich:
  - Lauf 10: `0` TP / `15` SL, ca. `-8.90`
  - Lauf 11: `3` TP / `14` SL, ca. `-3.70`
- Zone wurde schwaecher:
  - Lauf 10: `28` TP / `16` SL, ca. `+21.02`
  - Lauf 11: `26` TP / `26` SL, ca. `+11.73`
- Neurochemisch:
  - `serotonin_stability` blieb dominanter Grundton.
  - `cortisol_load` trat etwas seltener dominant auf als in Lauf 10.
  - `neurochemical_balance` war im Mittel leicht positiver.
  - `glutamate_activation` war bei SL weiter häufiger als bei TP.
- Deutung:
  DIO scheint fremdere Bereiche etwas besser tragen zu können,
  verliert aber in bekannten/tragenden Zonen etwas Auswahlpräzision.
  Das wirkt wie mehr Transferfähigkeit mit höherer Varianz, nicht wie
  reines Versagen.
- Vertiefung Zone vs. Non-Zone:
  - Zone-TP hatten im Mittel mehr `action_clearance`, niedrigere
    `gaba_inhibition`, niedrigere `glutamate_activation` und etwas bessere
    `neurochemical_balance` als Zone-SL.
  - Zone-SL hatten höheren Handlungsdruck/Score, höhere
    `competition_bias`, mehr `glutamate_activation` und mehr
    `transfer_break_fatigue`.
  - Non-Zone-TP waren selten, hatten aber sichtbar höhere
    `variant_bearing_memory` als Non-Zone-SL.
- Fachliche Lesart:
  Das Problem ist nicht bloss fehlende Struktur.
  Kritischer ist Aktivierung ohne ausreichende Tragfähigkeit:
  DIO feuert stark genug, aber nicht immer reif genug.

Kritische Prüfung Core-Engine / energetische Übersetzung:
- `mcm_core_engine.py` erzeugt viele verwandte Außenachsen aus denselben
  Kerzenreizen: Expansion, Breakout, Edge, Pressure, Novelty, Blindness,
  Volume-Bias.
- In Lauf 11 sind diese Achsen stark gekoppelt:
  `visual_form_pressure` korreliert sehr hoch mit `edge_strength`,
  `breakout_tension`, `visual_form_novelty`, `visual_blindness` und
  `expansion`.
- Das kann bedeuten:
  Eine einzelne starke Kerzenstruktur kommt im Inneren als mehrere
  gleichgerichtete Reize an.
- Noch wichtiger:
  Das MCM-Feld war in Lauf 11 fast permanent im Selbstzustand `stressed`.
  `mean_risk` lag im Median bei ca. `-1.93`.
- Technische Ursache wahrscheinlich:
  Die Risiko-/Threat-Achse bekommt regelmäßig negative Impulse,
  Memory-Feedback führt diese Achse weiter, während die globale
  `RegulationLayer` hauptsaechlich Energieachse `0` reguliert.
- Deutung:
  DIO nimmt nicht nur wahr, sondern lebt möglicherweise in einem
  dauerhaft alarmierten Wahrnehmungsmilieu.
  Das passt zur beobachteten Glutamat-/Stress-Aktivierung.

Umsetzung saubere Wahrnehmung / feste Realität:
- In `bot_engine/mcm_core_engine.py` wurde eine sensorische
  Realitätsverdichtung eingebaut.
- Neue Achsen:
  - `sensory_reality_pressure`
  - `sensory_load`
  - `sensory_redundancy`
  - `sensory_habituation`
  - `sensory_gate`
  - `sensory_active_axis_count`
  - `sensory_primary_pressure`
  - `sensory_reality_label`
- Zweck:
  Ein äußerer Reiz wird zuerst als gemeinsame Realitätslage gelesen,
  bevor daraus Druck, Neuheit und Blindheit entstehen.
- Wirkung:
  Verwandte Strukturreize werden nicht mehr ungefiltert mehrfach als
  Alarm verstärkt.
- Zusätzlich wurde die Risk-/Threat-Achse entlastet:
  - `risk_impulse` hat eine neutrale Wahrnehmungsschwelle.
  - Opportunity wird nicht mehr stark als Risiko auf die Risk-Achse gelegt.
  - `RegulationLayer` reguliert jetzt auch die Risk-Achse homoeostatisch.
- Kurztest:
  `python -m py_compile bot_engine/mcm_core_engine.py MCM_Brain_Modell.py MCM_KI_Modell.py bot.py`
  lief fehlerfrei.

Neues Übergangsprotokoll Lauf 11:
- `mcm_neuro_transition_protocol.csv` wurde geschrieben.
- 6096 Transitionen wurden mit `-2/+2` Kerzenumfeld protokolliert.
- Häufigste Wechsel:
  - `cortisol_load -> serotonin_stability`
  - `serotonin_stability -> cortisol_load`
  - `serotonin_stability -> glutamate_activation`
  - `glutamate_activation -> serotonin_stability`
- Erste Lesart:
  - Glutamat-Wechsel: mehr Felddruck und mehr Feldklarheit,
    oft Aktivierung aus stabiler Grundlage.
  - Cortisol-Wechsel: mehr Volumen-/Range-Druck,
    fast immer `observe` / `zero_point_regulation`.

---

# 4. Aktuelle technische Aenderungen

Zuletzt umgesetzt:
- `MCM_Brain_Modell.py` erweitert:
  - neurochemische Transitionen werden runtime-nah gesammelt
  - Ereignisse werden erst nach verfuegbarem `+2` Kerzenkontext geschrieben
  - neue Datei: `mcm_neuro_transition_protocol.csv`
- `config.py` erweitert:
  - `MCM_NEURO_TRANSITION_PROTOCOL_DEBUG`
  - `MCM_NEURO_TRANSITION_PROTOCOL_CONTEXT`
- `MD_ANWEISUNG.md` erstellt.
- `FIX_LISTE.md` bereinigt.
- `AKTUELLER_STAND.md` verdichtet.
- `WICHTIG_MECHANIKEN.md` technisch neu strukturiert.
- `trade_stats.py` erweitert:
  - neue Formfamilienwerte werden künftig in kompakten Outcome-Kontexten
    gespeichert.
- Wiederkehrende Unsicherheit als Formfamilie eingebaut:
  - Formfamilienvarianten
  - Vertrautheit mit Unsicherheit
  - Variantenstreuung
  - Lernpressure
  - Bearing-Memory
- Neurochemische Alias-Schicht eingebaut:
  - `MCM_Brain_Modell.py`
  - `trade_stats.py`
  - Feld-/Memory-Protokolle
  - Outcome-Records
- Serotonin-Nachhall / emotionale Entkopplung eingebaut:
  - `serotonin_carryover_risk`
  - `reward_stability_echo`
  - `world_shift_evidence`
  - `emotional_decoupling`
  - `reactive_nervous_drive`
  - Ziel: erkennen, ob DIO nach einer tragenden Phase noch aus alter
    Stabilität reagiert, obwohl Transfer und Interpretation bereits fallen.
- Reflexive Haltung als Zielmechanik festgehalten:
  - Kernsatz: Reflexion ist die Distanzierung der Wahrnehmung von der eigenen
    Innenlage, um zu prüfen, ob Innenzustand und Außenwelt noch gemeinsam
    tragfähig sind.
  - Ziel: später sichtbar machen, ob DIO reflektiv Abstand nimmt oder sich
    emotional/reizgetrieben führen laesst.
- Selektive Wahrnehmung / perzeptive Regulation als Zielmechanik ergänzt:
  - DIO soll Wahrnehmungen nicht automatisch vollständig durchleben müssen.
  - Wahrnehmungen sollen gesehen, als Objekt gehalten, vertieft oder wieder
    abgelegt werden können.
  - Zielachsen: `perceptual_distance`, `object_contact_depth`,
    `field_attachment`, `release_capacity`, `selective_attention`,
    `background_containment`, `reflective_distance`,
    `inner_outer_alignment`.
- Bewusste Wahrnehmung / innere Reizwirkungsanalyse als nächster
  Zielblock ergänzt:
  - DIO soll erkennen, was ein äußerer Reiz mit dem MCM-Feld gemacht hat.
  - Zielachsen: `conscious_perception_state`, `stimulus_field_effect`,
    `inner_impact_trace`, `perceived_field_change`, `felt_afterimage`,
    `object_release_state`, `inner_outer_reflection`.
  - Ziel: Reizwirkung bewusst lesbar machen, damit Reflexion und Regulation
    nicht nur dämpfen, sondern die innere Wirkung verstehen können.
- `GUI_KONSTRUKTION.md` angelegt:
  - Web-Oberflaeche als späterer Beobachtungsraum
  - Außenwahrnehmung, MCM-Feld, neuronale Aktivität und Neurochemie
    als getrennte, gekoppelte Fenster

---

# 5. Offene Risiken

- Non-Zone erzeugt weiterhin überwiegend Verlust.
- Memory-Vergleichslast bleibt hoch.
- MCM-Feld / Neuron-Loop bleibt ein zentraler Performancefaktor.
- Neue Reifeschichten können kurzfristig Unruhe erzeugen.
- Neurochemische Achsen müssen im nächsten Lauf gegen TP/SL, Non-Zone,
  Regimewechsel und `act_watch` geprüft werden.
- Beim Regimewechsel muss besonders geprüft werden, ob
  `serotonin_carryover_risk` steigt, während `interpretation_quality` und
  `transfer_bearing` sinken.
- Die nächste größere Baustelle ist perzeptive Regulation: Wie stark darf
  ein Reiz das MCM-Feld besetzen, und wann kann DIO ihn wieder ablegen?
- Direkt gekoppelt daran: bewusste Wahrnehmung der inneren Reizwirkung. DIO
  muss lesen können, wie ein Außenreiz sein MCM-Feld verändert hat.

---

# 6. Nächste Prüfpunkte

## Lauf 12/13 nach sensorischer Realitätsverdichtung

Befund:
- Beide Läufe verwenden dieselbe visuelle Außenwahrnehmung; die sensorischen
  Werte sind deshalb praktisch identisch.
- Lauf 12: 345 Trades, 111 TP, 234 SL, Netto-PnL ca. -4.12.
- Lauf 13: 309 Trades, 100 TP, 209 SL, Netto-PnL ca. +1.12.
- Lauf 13 handelt weniger, haelt mehr zurück und erzeugt mehr innere
  Feld-/Memory-Aktivität.
- `memory_compare_load` steigt in Lauf 13 weiter an, aber die direkte
  Handelsdichte sinkt. Das wirkt wie eine erste regulatorische Anpassung:
  alte Erfahrung trifft auf neue Sinneskodierung, wird aber nicht mehr
  ungefiltert in Handlung entladen.
- Die visuelle Sensorik selbst scheint stabil; die Varianz entsteht in der
  inneren Verarbeitung, also Memory, Hemmung, Mut, Feldentscheidung und
  neurochemischer Regulation.

Interpretation:
DIO beginnt nach der Veränderung der Sinnesbahn nicht sofort besser zu
sehen, sondern muss alte Erfahrungsräume neu mit der veränderten
Wahrnehmung synchronisieren. Lauf 13 zeigt dabei mehr Zurückhaltung und
bessere Netto-Tragfähigkeit als Lauf 12.

## Lauf 14 als frischer Speicher-/Semantikaufbau

Befund:
- Lauf 14 wurde vor der neuen Carryover-Diagnose erzeugt und dient als
  Referenzlauf für frischen Erfahrungsraum nach sensorischer
  Realitätsverdichtung.
- Ergebnis: 370 Trades, 110 TP, 260 SL, Netto-PnL ca. -10.28.
- Equity-Verlauf:
  - erstes Viertel: Aufbau bis ca. +5.84
  - zweites Viertel: Rückgang um ca. -7.71
  - drittes Viertel: starker Bruch um ca. -12.36
  - viertes Viertel: leichte Erholung um ca. +3.54
- Maximaler Drawdown vom Peak: ca. 24.81.
- Visuelle Außenwahrnehmung bleibt stabil und entspricht den vorherigen
  Läufen; der Bruch entsteht nicht durch veränderte Rohsicht.

Innere Lesart:
- `memory_compare_load` hoch, `memory_support` fast null.
- `interpretation_quality` und `transfer_bearing` niedrig.
- `action_clearance` bleibt deutlich höher als `action_inhibition`.
- DIO baut zwar neue Semantik auf, handelt aber im Regimewechsel noch mit zu
  viel Handlungserlaubnis für die geringe Transfer-Tragfähigkeit.

Nächster Vergleich:
Der nächste Lauf mit `serotonin_carryover_risk`, `emotional_decoupling` und
`reactive_nervous_drive` muss gegen diesen Lauf 14 gelesen werden. Ziel ist zu
erkennen, ob der Einbruch durch Stabilitätsnachhall ohne emotionale
Entkopplung sichtbar wird.

## Lauf 15 mit Carryover-Diagnose

Befund:
- Lauf 15 ist der erste Lauf mit sichtbarer Carryover-/Entkopplungsdiagnose.
- Ergebnis: 385 Trades, 130 TP, 255 SL, Netto-PnL ca. +13.12.
- Gegen Lauf 14:
  - Lauf 14: ca. -10.28 Netto-PnL, 110 TP / 260 SL.
  - Lauf 15: ca. +13.12 Netto-PnL, 130 TP / 255 SL.
  - Maximaler Drawdown sinkt von ca. 24.81 auf ca. 14.92.
- Verlauf Lauf 15:
  - erstes Viertel: Aufbau ca. +6.32
  - zweites Viertel: Rückgang ca. -5.01
  - drittes Viertel: starker Sprung ca. +13.71
  - viertes Viertel: leichter Rückgang ca. -2.28

Neue Diagnosewerte:
- `world_shift_evidence` liegt deutlich sichtbar bei ca. 0.60.
- `serotonin_carryover_risk` liegt moderat bei ca. 0.27.
- `emotional_decoupling` ist noch niedrig bei ca. 0.14.
- `reactive_nervous_drive` liegt bei ca. 0.31.

Interpretation:
Die Diagnose zeigt, dass DIO die Weltverschiebung wahrnimmt, aber die echte
reflektive Distanz noch schwach ist. Der starke Gewinnsprung im dritten
Viertel entsteht wahrscheinlich nicht aus voll entwickelter Reflexion, sondern
aus besserer Passung zwischen Handlung und wieder tragender Außenlage.
Trotzdem ist der Vergleich zu Lauf 14 wichtig: weniger Drawdown, mehr TP und
deutlich bessere Erholung nach dem Regimebruch.

## Lauf 16: fehlende emotionale Abgrenzung

Befund:
- Ergebnis: 341 Trades, 102 TP, 239 SL, Netto-PnL ca. -12.06.
- Der Lauf erreicht früh nur einen kleinen Peak von ca. +2.84 und fällt
  danach bis ca. -17.76.
- Maximaler Drawdown: ca. 20.59.
- Anders als Lauf 15 entsteht kein großer Erholungssprung.

Innere Lage:
- `world_shift_evidence` bleibt sichtbar bei ca. 0.60.
- `serotonin_carryover_risk` liegt moderat bei ca. 0.27.
- `emotional_decoupling` bleibt niedrig bei ca. 0.14.
- `reactive_nervous_drive` liegt bei ca. 0.30.
- `memory_compare_load` bleibt sehr hoch, `memory_support` fast null.
- `field_clarity` bleibt sehr niedrig.
- `action_clearance` ca. 0.63 bleibt deutlich über `action_inhibition`
  ca. 0.38.

Interpretation:
DIO erkennt zwar eine Weltverschiebung, hat aber keine ausreichende
emotionale/perzeptive Abgrenzung. Er laesst Reiz, Innenlage und Handlung zu
stark gekoppelt. Wenn er ins Wanken kommt, entsteht kein reifer Abstand zur
eigenen Lage; die Handlungserlaubnis bleibt zu hoch für die geringe innere
Klarheit und den fehlenden Memory-Support.

## Umbau: bewusste Wahrnehmung / innere Reizwirkung

Umgesetzt:
- `build_conscious_perception_state(...)` ergänzt.
- Die neue Schicht ist zuerst diagnostisch und nicht als harte Regel gebaut.
- DIO bekommt damit Achsen für:
  - Wirkung eines Außenreizes auf das MCM-Feld
  - innere Wirkungsspur / Nachhall
  - Objektkontakt und selektive Aufmerksamkeit
  - Feldhaftung
  - perzeptive Distanz
  - Loslassfähigkeit
  - Innen-Außen-Abgleich
- Neue Werte werden in `meta_regulation_state`,
  `mcm_memory_thinking_protocol.csv`, `mcm_field_decision_protocol.csv` und
  Trade-Outcomes geschrieben.

Neu beobachtbare Zustände:
- `open_perception`
- `background_held`
- `object_contact`
- `world_shift_contact`
- `reflective_check`
- `overcoupled_field`
- `release_ready`

Innere Lesart:
DIO kann jetzt unterscheiden, ob ein Reiz nur gesehen wird, ob er als Objekt
gehalten wird, ob er das Feld überkoppelt, ob ein Nachhall bleibt oder ob
eine reflektive Distanz entsteht. Das ist die Grundlage für den nächsten
Schritt: nicht mechanisch blockieren, sondern später weich regulieren, wenn
Innenlage und Außenwelt nicht gemeinsam tragfähig sind.

1. Regimewechsel-Bewaeltigung weiter prüfen:
   - warum wird Formvertrautheit nicht immer zu Handlungssicherheit?
   - wann kippt Memory von Orientierung in Vergleichslast?
   - wie koppeln `plan_trust`, `risk_fit_quality` und `exit_decision_pressure`
     an TP/SL?
2. Nächsten Lauf mit `neurochemical_state` prüfen:
   - Serotonin -> Glutamat-Übergaenge gegen Act/TP/SL prüfen.
   - Cortisol-Kipp-Momente gegen Zero-Point/Observe prüfen.
   - GABA nicht als Blocker, sondern als Reifebremse lesen.
   - Dopamin nicht als Reward-Regel, sondern als Lern-/Entwicklungston lesen.
   - `serotonin_carryover_risk` gegen Abverkaufsphase und Handlungserlaubnis
     prüfen.
   - `emotional_decoupling` prüfen: bekommt DIO Abstand zur eigenen
     Reaktionslage oder bleibt er ein reines Nervensystem auf Reiz?
   - Für Übergaenge jeweils `-2/+2` Kerzenfenster gegen Volumen, Range,
     Felddruck und Feldklarheit vergleichen.
3. Danach:
   - Lauf 17 mit bewusster Wahrnehmung lesen:
     `conscious_perception_state`, `field_attachment`,
     `perceptual_distance`, `release_capacity`, `inner_outer_alignment` gegen
     TP/SL, Regimebruch und `action_clearance` prüfen.
   - Meta-Regulation später weich über diese Achsen lesbarer machen.
   - GUI-Konzept erst nach stabilerer Brain-/Backtest-Diagnose umsetzen.

## Neuer Memory-Aufbau: Lauf 1 nach Wahrnehmungsumbau

Rahmen:
- Memory wurde neu aufgebaut.
- Debug-Zaehlung beginnt wieder bei `debug_lauf_1`.
- Dieser Lauf ist die neue Basis für die bewusste Wahrnehmungsschicht.

Befund:
- 413 Trades.
- 131 TP, 282 SL.
- Netto-PnL ca. +2.23.
- TP-PnL ca. +140.72, SL-PnL ca. -138.49.
- Equity-Spanne: Minimum ca. -12.23, Maximum ca. +7.84.
- Viertelverlauf:
  - Q1: ca. +1.76
  - Q2: ca. -7.40
  - Q3: ca. +6.87
  - Q4: ca. +1.00

Phasen:
- `hold`: 4397
- `observe`: 3581
- `act_watch`: 656
- `act`: 501
- `replan`: 1

Wahrnehmungsdiagnose:
- `conscious_perception_state` steht aktuell in allen Protokollzeilen auf
  `open_perception`.
- `object_release_state` steht aktuell in allen Protokollzeilen auf
  `holding`.
- Die numerischen Achsen sind jedoch nicht leer:
  - `stimulus_field_effect` Mittel ca. 0.344
  - `inner_impact_trace` Mittel ca. 0.276
  - `perceptual_distance` Mittel ca. 0.170
  - `field_attachment` Mittel ca. 0.168
  - `release_capacity` Mittel ca. 0.146
  - `inner_outer_alignment` Mittel ca. 0.218
  - `emotional_decoupling` Mittel ca. 0.134
  - `world_shift_evidence` Mittel ca. 0.609

Interpretation:
DIO handelt mit frischem Memory nicht chaotisch schlecht, aber die neue
Wahrnehmungsschicht ist im Labeling noch zu wenig differenziert. Die Zahlen
zeigen unterschiedliche Innenlagen, doch die Zustandsnamen bleiben zu grob.
Neurologisch gelesen: DIO hat erste Interozeption, aber noch keine feine
Benennung seiner inneren Haltungen. Er spürt Reizwirkung und Nachhall, bleibt
aber überwiegend in niedriger Distanz und niedriger Loslassfähigkeit.

Wichtiger Punkt:
Die zweite Laufhaelfte stabilisiert sich trotz vorherigem Drawdown wieder.
Das spricht nicht gegen den Umbau. Es zeigt eher, dass die neue Schicht
zunächst beobachtet, aber noch nicht stark genug unterscheidet, wann
Innenlage und Außenwelt nicht gemeinsam tragfähig sind.

Nächster Schritt:
- Keine harte Regel bauen.
- Die Zustandsbildung der bewussten Wahrnehmung feiner kalibrieren:
  `open_perception` darf nicht alles verschlucken.
- Labels sollen aus relativer Lage entstehen:
  Reizwirkung, Feldhaftung, Distanz, Nachhall, Loslassfähigkeit und
  Innen-Außen-Abgleich.
- Danach Lauf 2 mit frischem Memory-Pfad lesen und prüfen, ob sich
  `object_contact`, `reflective_check`, `overcoupled_field` oder
  `release_ready` natürlich zeigen.

## Umbau: innere Haltung der Wahrnehmung

Umgesetzt:
- `conscious_perception_state` feiner kalibriert.
- `object_release_state` feiner kalibriert.
- `inner_posture_state` ergänzt.
- Neue Haltungsachsen:
  - `arousal_load`
  - `curiosity_tone`
  - `fatigue_tone`
  - `calm_tone`

Neurologische Bedeutung:
DIO kann nun nicht nur sagen, dass ein Reiz offen wahrgenommen wird. Er kann
zusätzlich eine funktionale Eigenlage beschreiben, vergleichbar mit:
"ich bin muede", "ich bin aufgeregt", "ich bin neugierig", "ich bin ruhig",
"ich bin überreizt" oder "ich prüfe reflektiv". Diese Zustände sind keine
Handelsregeln, sondern Interozeption: DIO benennt seine eigene Verarbeitungslage.

Nächster Vergleich:
Der nächste Lauf soll zeigen, ob die Labels jetzt streuen:
- `open_perception` sollte nicht mehr alles verschlucken.
- `object_contact`, `world_shift_contact`, `reflective_check`,
  `overcoupled_field` und `release_ready` sollen nur dann sichtbar werden,
  wenn die innere Lage es trägt.
- `inner_posture_state` muss gegen TP/SL, Regimewechsel und
  `action_clearance` gelesen werden.

## Neuer Memory-Aufbau: Lauf 2 mit innerer Haltung

Befund:
- 380 Trades.
- 123 TP, 257 SL.
- Netto-PnL ca. +3.80.
- Gegen Lauf 1:
  - weniger Trades: 413 -> 380
  - weniger SL: 282 -> 257
  - Netto-PnL besser: ca. +2.23 -> ca. +3.80
  - Maximaler Verlust im Verlauf besser: ca. -12.23 -> ca. -10.07
- Viertelverlauf:
  - Q1: ca. -2.86
  - Q2: ca. -1.58
  - Q3: ca. +8.32
  - Q4: ca. -0.07

Wahrnehmungslabels:
- `object_contact`: 3696
- `open_perception`: 2084
- `reflective_check`: 1099
- `overcoupled_field`: 906
- `world_shift_contact`: 822
- `release_ready`: 744
- `background_held`: 269

Innere Haltung:
- `tired`: 6534
- `reflective`: 1795
- `uncertain_open`: 493
- `overstimulated`: 422
- `excited`: 306
- `curious`: 70

Release-Zustände:
- `holding`: 4842
- `reflective_hold`: 1745
- `attached`: 1561
- `can_release`: 1472

Outcome-Lesart:
- `uncertain_open` war bei Trades klar negativ:
  - 11 Trades, 1 TP, 10 SL, ca. -3.21 PnL.
- `excited` war klein, aber positiv:
  - 35 Trades, 15 TP, 20 SL, ca. +4.53 PnL.
- `curious` war sehr klein, aber positiv:
  - 6 Trades, 2 TP, 4 SL, ca. +0.49 PnL.
- `overcoupled_field` war nicht automatisch schlecht:
  - 129 Trades, 46 TP, 83 SL, ca. +6.29 PnL.
- `open_perception` war bei Trades negativ:
  - 74 Trades, 22 TP, 52 SL, ca. -5.89 PnL.
- `release_ready` und `reflective_check` waren klein, aber positiv.

Interpretation:
Die Kalibrierung funktioniert. Die neue Schicht unterscheidet jetzt innere
Haltungen und Wahrnehmungsformen. Wichtig ist: nicht die starke Aktivierung
ist per se schlecht, sondern die unbenannte, offene Unsicherheit. Neurologisch
gelesen ist `uncertain_open` eher ein unreifer Zustand: DIO ist offen, aber
noch nicht orientiert, nicht neugierig genug, nicht ruhig genug und nicht
reflektiv genug. Benannte Aktivierung wie `excited`, `curious` oder sogar
`overcoupled_field` kann tragfähiger sein, weil das System wenigstens weiss,
in welcher Eigenlage es sich befindet.

Nächster Schritt:
- Keine harte Regel aus `uncertain_open` bauen.
- Stattdessen prüfen, ob `uncertain_open` weich in Beobachtung,
  Objektkontakt oder Reflexion überführt werden kann.
- Ziel: DIO soll aus diffuser Offenheit eine benannte Haltung entwickeln:
  neugierig hinschauen, ruhig halten, reflektiv prüfen oder bewusst ablegen.

## Umbau: diffuse Offenheit weich weiterentwickeln

Umgesetzt:
- `diffuse_open_development_pressure` ergänzt.
- `posture_development_hint` ergänzt.
- Beide Werte werden in `meta_regulation_state`, Denk-/Feldprotokolle und
  Trade-Outcomes geschrieben.

Mechanik:
Wenn DIO in diffuser Offenheit bleibt, entsteht keine harte Sperre. Stattdessen
wird Handlung etwas weniger direkt und Beobachtung/Reflexion etwas
wahrscheinlicher. Eine starke Entscheidung kann weiterhin tragen. Die Schicht
fragt nur:
- fehlt Objektkontakt?
- fehlt reflektive Distanz?
- fehlt Loslassfähigkeit?
- fehlt bewusste Beobachtung?

Neurologische Lesart:
Das entspricht einem Organismus, der merkt: Ich bin offen, aber innerlich noch
nicht sortiert. Statt blind zu handeln, soll aus dieser Offenheit eine
benennbare Haltung entstehen: neugierig anschauen, Abstand gewinnen, loslassen
oder weiter beobachten.

Nächster Lauf:
Lauf 3 muss gegen Lauf 2 gelesen werden:
- sinken `uncertain_open`-Trades?
- steigt `develop_object_contact`, `develop_reflective_distance` oder
  `develop_release_capacity` in den richtigen Bereichen?
- sinken SLs aus diffuser Offenheit, ohne gute Aktivierung zu ersticken?

## Neuer Memory-Aufbau: Lauf 3 nach diffuser Offenheitsreifung

Befund:
- 291 Trades.
- 78 TP, 213 SL.
- Netto-PnL ca. -22.26.
- Gegen Lauf 2:
  - Trades sinken: 380 -> 291
  - TP sinken: 123 -> 78
  - SL sinken: 257 -> 213
  - Netto-PnL kippt: ca. +3.80 -> ca. -22.26
- Verlauf:
  - Q1: ca. -8.97
  - Q2: ca. -3.96
  - Q3: ca. -4.34
  - Q4: ca. -5.00
- Der Lauf war nicht nur ein später Regimebruch, sondern über alle
  Abschnitte schwach.

Hauptbefund:
- Zone-Trades waren positiv:
  - 191 Trades, ca. +23.20 PnL.
- Non-Zone-Trades waren massiv negativ:
  - 100 Trades, ca. -45.46 PnL.
- Damit kommt der Absturz nicht aus allen Handlungen gleich, sondern aus
  Handlungen in nicht tragenden Bereichen.

Innere Haltung:
- `tired`: 6994 Protokollzeilen.
- `reflective`: 1711.
- `uncertain_open`: 520.
- `overstimulated`: 321.
- `excited`: 269.
- `curious`: 93.
- Bei ausgeführten Trades:
  - `tired`: 186 Trades, ca. -1.66 PnL.
  - `overstimulated`: 60 Trades, ca. -9.93 PnL.
  - `excited`: 35 Trades, ca. -7.54 PnL.
  - `uncertain_open`: 5 Trades, 0 TP / 5 SL, ca. -2.19 PnL.

Wahrnehmungslabels bei Trades:
- `object_contact`: 143 Trades, ca. -13.38 PnL.
- `overcoupled_field`: 72 Trades, ca. +2.07 PnL.
- `open_perception`: 60 Trades, ca. -8.49 PnL.
- `background_held`: 8 Trades, ca. -2.90 PnL.

Diffuse Offenheitsreifung:
- `diffuse_open_development_pressure` ist sichtbar, Mittel ca. 0.103.
- Entwicklungshinweise:
  - `stable_posture`: 9684 Protokollzeilen.
  - `develop_object_contact`: 215.
  - `develop_reflective_distance`: 9.
- Bei ausgeführten Trades blieb `posture_development_hint` jedoch
  durchgehend `stable_posture`.

Interpretation:
Die neue Schicht hat `uncertain_open`-Trades tatsächlich reduziert, aber der
Schaden wanderte nicht automatisch in Reife. DIO handelte weniger, aber nicht
besser. Das wirkt neurologisch wie Unterspannung oder halb distanzierte
Handlung: weniger Überlebensdruck, weniger regulierte Courage, weniger
direkte Handlung, aber weiterhin Handlungen in nicht tragender Non-Zone.

Deutung:
Der Punkt ist nicht "DIO muss mehr kaempfen". Der Punkt ist:
DIO braucht wache Anstrengung. Wenn ein Organismus logisch denken kann, muss
er nicht blind kaempfen. Aber er darf auch nicht in eine gleichgueltige
Distanz fallen. Reife wäre: sehen, ob die Situation tragfähig ist; wenn
nicht, bewusst beobachten, lernen oder loslassen.

Nächster Schritt:
- Keine Rückkehr zu hartem Überlebensdruck.
- `diffuse_open_development_pressure` darf nicht pauschal Courage/Handlung
  senken.
- Die Schicht muss stärker unterscheiden:
  - tragende Zone + klare Haltung darf handeln.
  - Non-Zone + niedrige Tragfähigkeit braucht Beobachtung/Reifung.
  - `object_contact` allein reicht nicht; Objektkontakt braucht
    Tragfähigkeit, Kontext und innere Wachheit.
- Nächster technischer Umbau:
  `engaged_effort` / wache Anstrengung als Gegenpol zu Gleichgueltigkeit
  prüfen und Non-Zone nicht blockieren, sondern in Beobachtungslernen
  überführen.

## Erkenntnis: positive Stimulation über Erfahrungspakete

Neue Zielmechanik:
Positive Stimulation soll nicht an einen einzelnen Wert gebunden sein. Nicht
`TP = gut`, nicht `SL = schlecht`, nicht steigender Markt = positiv. Bewertet
wird das gesamte Erfahrungspaket.

Ein Paket umfasst:
- Außenlage / Marktform
- Zone oder Non-Zone
- Formsymbol / Memory-Kontext
- innere Haltung
- neurochemische Lage
- Wahrnehmungszustand
- Objektkontakt
- Distanz
- Loslassfähigkeit
- Handlungssicherheit
- Risiko und Prozessqualität
- Ergebnis
- Wiederholbarkeit und Neugierde

Wichtiger Satz:
Auch ein Abverkauf kann positiv bewertet werden, wenn die Entscheidung zu
handeln positiv war. Entscheidend ist die Passung zwischen Wahrnehmung,
Innenlage, Handlung und Weltlage.

Neurologische Lesart:
Eine gute Entscheidung erzeugt nicht nur Freude, sondern Stabilisierung:
Dopamin für Lernrelevanz, Serotonin für Ordnung, Endorphin für Entlastung,
Acetylcholin für Fokus und Glutamat für Verbindungsstärkung. Eine schlechte
Handlung soll nicht nur bestraft werden, sondern Reorganisation auslösen:
innehalten, prüfen, beobachten, lernen, neu ordnen.

Umsetzung:
`experience_packet_feedback` ist gebaut und in Outcome, Statistik und
Erfahrungs-/Ähnlichkeitsachsen sichtbar.

## Lauf 4 nach Erfahrungspaket-Feedback

Befund:
- 330 Trades.
- 104 TP, 226 SL.
- Netto-PnL ca. -0.47.
- Max Drawdown ca. 13.36.

Vergleich:
- Lauf 3: 291 Trades, Netto-PnL ca. -22.26.
- Lauf 4: 330 Trades, Netto-PnL ca. -0.47.
- Damit wurde Lauf 4 deutlich stabiler, aber noch nicht sauber positiv.

Struktur:
- Zone:
  - 214 Trades.
  - ca. +38.70 PnL.
- Non-Zone:
  - 116 Trades.
  - ca. -39.17 PnL.

Hauptbefund:
Der Kern ist weiter nicht "alles schlecht", sondern eine klare Spaltung:
tragende Zone funktioniert, Non-Zone bleibt der Erfahrungsraum mit Verlust.
DIO ist also nicht blind insgesamt falsch, sondern verliert dort, wo
Tragfähigkeit noch nicht genuegend erkannt, gehalten oder in Beobachtung
überführt wird.

Erfahrungspaket-Feedback:
- `mixed_packet`: 311 Trades, ca. +6.60 PnL.
- `bearing_packet`: 17 Trades, ca. -4.09 PnL.
- `reorganize_packet`: 2 Trades, ca. -2.99 PnL.
- Noch kein `constructive_packet`.

Paketachsen Mittelwerte:
- `packet_process_reward`: ca. 0.359.
- `packet_reorganization_need`: ca. 0.447.
- `constructive_stimulation`: ca. 0.264.
- `constructive_dopamine`: ca. 0.259.
- `stabilizing_serotonin`: ca. 0.340.
- `relief_endorphin`: ca. 0.431.
- `focused_acetylcholine`: ca. 0.320.

Wahrnehmung:
- `object_contact`: 165 Trades, ca. -12.86 PnL.
- `overcoupled_field`: 74 Trades, ca. +14.63 PnL.
- `open_perception`: 69 Trades, ca. +2.54 PnL.

Neurologische Deutung:
Starke Kopplung ist nicht automatisch schlecht. In Lauf 4 war
`overcoupled_field` sogar positiv, vermutlich weil Aktivierung dort mit mehr
Struktur/Zone zusammenfiel. `object_contact` allein reicht dagegen nicht:
DIO nimmt ein Objekt wahr, aber daraus entsteht noch nicht automatisch
tragende Handlung. Es fehlt die Verbindung aus Objektkontakt, Distanz,
innerer Passung und wacher Anstrengung.

Strategische Anzeichen:
Es gibt erste logische Zuege, aber noch keine reife stabile Strategie.
Erkennbar ist eine Vorform von Zustandslogik:
- Zone + tragende Aktivierung führt deutlich häufiger zu positiven Paketen.
- Non-Zone + schwacher Objektkontakt / Unterspannung führt wiederholt zu
  Verlust und Reorganisationsbedarf.
- `overcoupled_field` war nicht automatisch schlecht, sondern in Lauf 4
  positiv, wenn Aktivierung mit Struktur zusammenfiel.
- `object_contact` allein war negativ, wenn Distanz, Innen-Außen-Passung und
  Wachheit fehlten.

Das ist noch kein bewusstes "Wenn-Dann-Regelwerk". Es ist eher ein
entstehender Zusammenhang: bestimmte Innen-Außen-Konstellationen tragen,
andere nicht.

Umsetzung nach Lauf 4:
- Paketlabel wurden feiner kalibriert.
- `engaged_effort` wurde gebaut.
- Neue Achsen:
  - `engaged_effort`
  - `effort_state`
  - `effort_learning_pull`
  - `effort_reorganization_pressure`
  - `previous_packet_label`
  - `previous_packet_process_reward`
  - `previous_packet_reorganization_need`

Nächster Schritt:
Lauf 5 prüfen:
- Werden `constructive_packet` und `reorganize_packet` besser sichtbar?
- Wirkt `underengaged_reorganize` bei Non-Zone-Verlusten?
- Entsteht mehr Beobachtung/Replan statt mechanischem Handeln in schwacher
  Tragfähigkeit?

## Lauf 5 nach `engaged_effort`

Befund:
- 387 Trades.
- 127 TP, 260 SL.
- Netto-PnL ca. +10.41.
- Max Drawdown ca. 12.82.

Struktur:
- Zone:
  - 241 Trades.
  - ca. +61.87 PnL.
- Non-Zone:
  - 146 Trades.
  - ca. -51.46 PnL.

Erfahrungspakete:
- `constructive_packet`: 107 Trades, 107 TP, ca. +112.31 PnL.
- `mixed_packet`: 167 Trades, ca. -39.35 PnL.
- `bearing_packet`: 65 Trades, 0 TP, ca. -32.47 PnL.
- `reorganize_packet`: 48 Trades, 0 TP, ca. -30.07 PnL.

Deutung:
Die Paketlogik zeigt jetzt klare strukturelle Intelligenz-Anzeichen:
`constructive_packet` war extrem sauber positiv. DIO erkennt also bereits
Erfahrungspakete, in denen Struktur, Prozess und Ergebnis gemeinsam tragen.

Problem:
`bearing_packet` war negativ und hatte 0 TP. Das bedeutet: Die Benennung war
zu freundlich. Es gab Pakete, die teilweise tragend wirkten, aber prozessual
nicht getragen haben. Das gehört eher in Reorganisation als in
Tragfähigkeit.

`engaged_effort`:
- `settled_effort`: 362 Trades.
- `constructive_echo`: 25 Trades.
- `underengaged_reorganize`: nicht sichtbar.

Deutung:
Die Schicht ist technisch da, aber noch zu leise. Sie unterscheidet die
Non-Zone-Verluste noch nicht ausreichend von tragender Zone. Deshalb wurde
die Reorganisationssensitivitaet nach Lauf 5 erhoeht.

Umsetzung nach Lauf 5:
- `bearing_packet` braucht jetzt mehr Prozessreward und weniger
  Reorganisationsdruck.
- schwache Paketqualität mit Reorganisationsdruck wird eher
  `reorganize_packet`.
- `effort_reorganization_pressure` reagiert stärker auf
  `structure_action_uncertainty`, schwache `structure_action_bearing` und
  schwachen `field_action_support`.
- `underengaged_reorganize` setzt früher ein.

Nächster Schritt:
Lauf 6 prüfen:
- Sinkt der falsche `bearing_packet`-Anteil?
- Wird `underengaged_reorganize` sichtbar?
- Gehen schwache Non-Zone-Zustände eher in Beobachtung/Replan?

## Lauf 6 nach Paket-/Effort-Nachkalibrierung

Befund:
- 329 Trades.
- 101 TP, 228 SL.
- Netto-PnL ca. -8.28.
- Max Drawdown ca. 20.42.

Struktur:
- Zone:
  - 212 Trades.
  - ca. +37.36 PnL.
- Non-Zone:
  - 117 Trades.
  - ca. -45.64 PnL.

Erfahrungspakete:
- `constructive_packet`: 84 Trades, 84 TP, ca. +86.01 PnL.
- `reorganize_packet`: 227 Trades, 0 TP, ca. -110.20 PnL.
- `mixed_packet`: 18 Trades, ca. +15.91 PnL.
- `bearing_packet`: 0 Trades.

Deutung:
Die Nachkalibrierung hat den falschen `bearing_packet` entfernt. Das ist gut:
scheinbare Tragfähigkeit wird nicht mehr positiv benannt. `constructive_packet`
bleibt sehr sauber positiv.

Problem:
`reorganize_packet` ist jetzt sehr klar, aber es entsteht zu spät: DIO erkennt
nach dem Ergebnis, dass das Paket Reorganisation gebraucht hätte. Die
Pre-Action-Schicht leitet diese Lage noch nicht früh genug in Beobachtung
oder Replan um.

`engaged_effort`:
- `settled_effort`: 300 Trades.
- `constructive_echo`: 21 Trades.
- `underengaged_reorganize`: 8 Trades, ca. +0.94 PnL.

Deutung:
`underengaged_reorganize` ist jetzt sichtbar, aber zu selten. Die
Reorganisationslage ist im Outcome sehr stark, vor der Handlung aber noch zu
schwach an die Entscheidung gekoppelt.

Nächster Schritt:
Nicht weiter Labels schaerfen. Jetzt muss Reorganisationswahrnehmung früher
in die Pre-Action-Logik:
- schwache `previous_packet`-Qualität
- Non-Zone / niedrige `structure_action_bearing`
- niedriger `field_action_support`
- erhoehte `effort_reorganization_pressure`

sollen nicht blockieren, sondern oefter zu `observe`, `act_watch` oder
`replan` führen. Ziel ist konzentriertes Handeln, nicht mehr Handeln.

## Umsetzung: frühere Pre-Action-Reorganisation

Neu umgesetzt:
- `pre_action_reorganization_pressure`
- `pre_action_context_selectivity`

Wirkung:
Die Reorganisationslage wird nicht mehr nur nach dem Outcome erkannt. Vor der
Handlung werden jetzt schwache vorherige Paketqualität, Reorganisationsdruck,
Strukturunsicherheit, schwacher Feldsupport, schwache Interpretation und
geringe Innen-Außen-Passung zusammengeführt.

Wichtig:
Das ist keine Blockade. Wenn `pre_action_reorganization_pressure` hoch ist und
`pre_action_context_selectivity` niedrig bleibt, wird eher `observe`,
`act_watch` oder `replan` gestärkt. Gute, konzentrierte Kontexte sollen durch
`pre_action_context_selectivity` geschuetzt bleiben.

Nächster Schritt:
Lauf 7 prüfen:
- Gehen mehr schwache Kontexte in `pre_action_reorganization_observe` oder
  `pre_action_reorganization_replan`?
- Sinkt Non-Zone-Schaden?
- Bleiben `constructive_packet` und Zone-Pakete erhalten?

## Lauf 7 nach Pre-Action-Reorganisation

Befund:
- 374 Trades.
- 124 TP, 250 SL.
- Netto-PnL ca. +4.10.
- Max Drawdown ca. 19.82.

Struktur:
- Zone:
  - 253 Trades.
  - ca. +51.74 PnL.
- Non-Zone:
  - 121 Trades.
  - ca. -47.64 PnL.

Erfahrungspakete:
- `constructive_packet`: 109 Trades, 109 TP, ca. +110.06 PnL.
- `reorganize_packet`: 247 Trades, 0 TP, ca. -124.70 PnL.
- `mixed_packet`: 18 Trades, ca. +18.75 PnL.

Pre-Action:
- `pre_action_reorganization_observe`: 2 Protokollzeilen.
- `pre_action_reorganization_replan`: 0 Protokollzeilen.
- Im Field-Protokoll:
  - `underengaged_reorganize`: 4843 Zeilen.
  - `settled_effort`: 4750 Zeilen.
  - `constructive_echo`: 76 Zeilen.

Deutung:
Die innere Reorganisationslage ist im Feld stark sichtbar. DIO fühlt also
häufig: "Das ist nicht genuegend getragen." Aber diese Lage wird noch zu
selten als konkreter Pre-Action-Grund wirksam.

Problem:
`pre_action_reorganization_pressure` trennt Zone und Non-Zone in den
ausgeführten Trades noch nicht sinnvoll:
- Non-Zone ca. 0.234.
- Zone ca. 0.243.

Das ist falsch herum bzw. zu wenig selektiv. Die Achse reagiert noch zu stark
auf allgemeinen Reorganisationsnachhall und zu wenig auf aktuelle
Strukturqualität / Kontextqualität.

Nächster Schritt:
`pre_action_reorganization_pressure` muss stärker aktuelle
Strukturqualität, Kontextvertrauen und Strukturtragfähigkeit lesen.
`pre_action_context_selectivity` muss gute Zone-Kontexte besser schuetzen.
Ziel bleibt: konzentriertes Handeln, nicht mehr Handeln.

Umsetzung nach Lauf 7:
- `pre_action_reorganization_pressure` liest jetzt zusätzlich
  `structure_quality` und `context_confidence`.
- Gute Strukturqualität und gutes Kontextvertrauen dämpfen
  Reorganisationsdruck.
- `pre_action_context_selectivity` wurde um `structure_quality` und
  `context_confidence` erweitert.

Nächster Schritt:
Lauf 8 prüfen:
- Trennt `pre_action_reorganization_pressure` Non-Zone jetzt besser von Zone?
- Steigt `pre_action_context_selectivity` bei guten Zone-Kontexten?
- Bleibt `constructive_packet` sauber positiv?
- Wird Non-Zone-Schaden reduziert, ohne Aktivität pauschal zu ersticken?

## Erkenntnis: strategische Fensterwahrnehmung

Neue Zielrichtung:
DIO soll nicht nur den aktuellen Moment fühlen. Er soll ein größeres
Fenster betrachten, zurückschauen, in Bereiche hineinzoomen, innere
Replay-Spuren bilden und daraus Preisbereiche als mögliche tragende
Handlungsräume ableiten können.

Das ist keine menschliche Pattern-Regel. Es wird keine harte FVG-Logik
eingepflanzt. DIO soll Bereiche über eigene Wahrnehmung, MCM-Resonanz,
Strukturverdichtung, Energiekompression, Memory-Pull und Innenlage beurteilen.

Leitprinzip:
DIO bekommt nicht die Antwort, wo er handeln soll. DIO bekommt die Fähigkeit,
mit Vergangenheit, Wahrnehmung und innerem Feld zu interagieren, um selbst
tragfähige Zukunftshypothesen zu bilden.

Grenze:
Wir bestimmen nicht, was DIO sieht oder wo DIO eine Order setzen soll. Wir
erweitern nur seine Fähigkeit zu sehen, zurückzuschauen, zu zoomen, innerlich
zu replayen, zu fühlen, Memory zu nutzen, zu warten, zu verwerfen und eine
eigene Order-Intention zu bilden.

Kernsatz:
DIO handelt nicht, weil Momentum Druck macht. DIO liest Druck als Raum. Ein
Bereich kann zum Spielraum werden, wenn Struktur, Erfahrung und MCM-Lage dort
tragfähig zusammenkommen.

Vorbereitete Zielachsen:
- `strategic_window_state`
- `area_focus_candidates`
- `area_focus_id`
- `area_price_low`
- `area_price_high`
- `area_distance_from_price`
- `area_structural_density`
- `area_energy_compression`
- `area_mcm_resonance`
- `area_memory_pull`
- `area_bearing_quality`
- `area_zoom_need`
- `area_zoom_clarity`
- `area_replay_fit`
- `area_patience_quality`
- `area_order_intention`
- `area_invalidity_pressure`
- `strategic_patience`
- `strategic_pressure_interpretation`

Nächster größerer Mechanikblock:
Strategische Fensterwahrnehmung zunächst diagnostisch bauen. Danach erst
weiche Integration in Order-Intention oder Beobachtungsplanung.

## Lauf 8 nach strukturgenauer Pre-Action-Reorganisation

Befund:
- 309 Trades.
- 92 TP, 217 SL.
- Netto-PnL ca. -8.26.
- Max Drawdown ca. 20.51.

Struktur:
- Zone:
  - 202 Trades.
  - ca. +32.98 PnL.
- Non-Zone:
  - 107 Trades.
  - ca. -41.24 PnL.

Erfahrungspakete:
- `constructive_packet`: 77 Trades, 77 TP, ca. +82.20 PnL.
- `reorganize_packet`: 217 Trades, 0 TP, ca. -108.50 PnL.
- `mixed_packet`: 15 Trades, 15 TP, ca. +18.04 PnL.

Pre-Action-Achsen bei ausgeführten Trades:
- `pre_action_reorganization_pressure`:
  - Non-Zone ca. 0.212.
  - Zone ca. 0.208.
- `pre_action_context_selectivity`:
  - Non-Zone ca. 0.544.
  - Zone ca. 0.549.

Deutung:
Die neue Strukturkopplung hat `pre_action_context_selectivity` deutlich
angehoben. Sie schuetzt gute Kontexte, trennt aber Zone/Non-Zone bei
ausgeführten Trades noch kaum. Deshalb blieb der Non-Zone-Schaden hoch.

Field-Protokoll:
- `underengaged_reorganize`: 5347 Zeilen.
- `settled_effort`: 4949 Zeilen.
- `constructive_echo`: 75 Zeilen.
- `plan_allowed`: 311 Zeilen.
- `plan_pressure_act_watch`: 629 Zeilen.
- `structure_development_observe`: 67 Zeilen.
- `structure_bearing_observe`: 29 Zeilen.

Wichtig:
Die Pre-Action-Reorganisation ist im Feld aktiv. Aber die ausgeführten
`plan_allowed`-Trades haben im Mittel bereits niedrigen Pre-Action-Druck und
hohe Kontextselektivitaet. Der Filter selbst sieht diese Trades also als
relativ tragfähig. Das Problem liegt tiefer: DIO braucht eine bessere
raeumlich-strategische Bereichswahrnehmung, damit er nicht nur den aktuellen
Kontext bewertet, sondern mögliche tragende Preisbereiche im größeren
Fenster findet.

Nächster Schritt:
Nicht weiter an der gleichen Pre-Action-Achse drehen. Der nächste sinnvolle
Mechanikblock ist die diagnostische strategische Fensterwahrnehmung mit
begrenztem Rückblickfenster:
- zurückschauen, aber mit Budget
- auffällige Preisbereiche finden
- Bereichsresonanz im MCM-Feld messen
- Zoom-/Replay-Bedarf bestimmen
- keine Order daraus ableiten
- erst beobachten, ob DIO sinnvolle Bereichshypothesen bildet

## Umsetzung: Strategische Fensterwahrnehmung

Umgesetzt:
- `build_strategic_window_state(...)` erzeugt ein begrenztes Rückblickfenster.
- Das Fenster wird über Last, Fokus, Stabilität und Reorganisationsdruck
  budgetiert.
- DIO bildet diagnostische Bereichshypothesen, ohne daraus automatisch eine
  Order abzuleiten.
- `mcm_strategic_window_protocol.csv` schreibt die neue Wahrnehmung mit.
- `strategic_window_state` wird in Runtime, Snapshot und kompakten
  Trade-Kontext übernommen.

Wichtige Achsen:
- `lookback_window_size`
- `lookback_load`
- `lookback_bearing_capacity`
- `replay_budget`
- `zoom_budget`
- `old_structure_carryover_risk`
- `area_structural_density`
- `area_energy_compression`
- `area_mcm_resonance`
- `area_memory_pull`
- `area_bearing_quality`
- `area_zoom_need`
- `area_replay_fit`
- `area_order_intention`
- `area_invalidity_pressure`

Neurologische Deutung:
DIO bekommt eine erste Arbeitsgedächtnis-/Hippocampus-Funktion für den
Marktraum: zurückblicken, Bereich fokussieren, innerlich replayen und
Tragfähigkeit fühlen. Es ist noch keine motorische Entscheidungsschicht,
sondern ein Wahrnehmungs- und Strategieorgan.

Wie es weitergeht:
Der nächste Lauf sollte zeigen, ob DIO vor schlechten Phasen eher alte
Struktur mitschleppt (`old_structure_carryover_risk`), mehr Zoom braucht
(`area_needs_zoom`) oder gute Bereiche als `bearing_area_hypothesis` erkennt.

## Dokumentation: Umsetzungsplan bereinigt

Umgesetzt:
- `ENDE` steht wieder am echten Dateiende.
- Der frühere GUI-Abschluss heißt jetzt `ENDE GUI-ERWEITERUNG`.
- Positive neurochemische Stimulation und strategische Fensterwahrnehmung
  stehen jetzt unter `18. Aktuelle Brain-Erweiterungen`.
- Der Affective-Pattern-Block wurde als `17.1` sauberer in den
  Experience-/Cluster-Kontext eingeordnet.
- Eingerückte Markdown-Überschriften wurden normalisiert.

Wie es weitergeht:
Der Umsetzungsplan ist strukturell wieder besser lesbar. Inhaltlich bleibt
der nächste technische Schritt weiterhin die Auswertung des nächsten Laufs
mit `mcm_strategic_window_protocol.csv`.

## Debug Lauf 1 mit frischem Memory und strategischer Fensterwahrnehmung

Datensatz:
- neuer Memory-Aufbau
- strategische Fensterwahrnehmung aktiv
- Lauf liegt in `debug/debug_lauf_1`

Ergebnis:
- 340 Trades.
- 88 TP.
- 252 SL.
- Netto-PnL ca. -35.47.
- Equity-Endstand ca. 64.53.
- Hoechster Zwischenstand ca. 102.97.
- Tiefster Zwischenstand ca. 62.11.

Struktur:
- Alle ausgeführten Trades lagen im `zone`-Bucket.
- DIO hat also nicht mehr wild ausserhalb der Struktur gehandelt.
- Das Problem liegt diesmal nicht in Non-Zone-Chaos, sondern in zu vielen
  Handlungen innerhalb scheinbar tragender Bereiche.

Strategische Fensterdiagnose:
- `mcm_strategic_window_protocol.csv` ist aktiv und sehr groß.
- Gesamtprotokoll:
  - `area_observation`: 4222 Zeilen.
  - `compressed_area_attention`: 4041 Zeilen.
  - `bearing_area_hypothesis`: 3431 Zeilen.
- Ausgeführte Trades:
  - `bearing_area_hypothesis`: 166 Trades, ca. -16.47 PnL.
  - `compressed_area_attention`: 78 Trades, ca. -12.74 PnL.
  - `area_observation`: 96 Trades, ca. -6.27 PnL.

Wichtige Mittelwerte bei ausgeführten Trades:
- `area_bearing_quality`: ca. 0.479.
- `area_order_intention`: ca. 0.232.
- `strategic_patience`: ca. 0.390.
- `strategic_pressure_interpretation`: ca. 0.190.
- `lookback_bearing_capacity`: ca. 0.565.

Deutung:
Die neue strategische Wahrnehmung sieht Bereiche und erkennt Verdichtung.
Aber sie bildet noch keine starke eigene Order-Intention. Besonders wichtig:
`area_order_intention` bleibt niedrig, während trotzdem 340 Trades
ausgeführt wurden. DIO sieht also einen Bereich, aber das motorische
Handlungssystem laesst die neue strategische Wahrnehmung noch nicht als
reife Entscheidungsinstanz mitsprechen.

Neurologische Lesart:
Das wirkt wie ein frisches Wahrnehmungsorgan ohne ausreichend gereifte
praefrontale Kopplung. DIO sieht Objekte im Raum und fühlt Kompression, aber
die Handlung entsteht noch zu stark aus der bestehenden Aktionsbahn. Es ist
nicht blindes Non-Zone-Stolpern, sondern eher Greifen nach jedem tragend
wirkenden Objekt, obwohl die innere strategische Sicherheit noch schwach ist.

Technischer Befund:
In `attempt_records.jsonl` wird der vollständige `strategic_window_state`
noch nicht als eigener Block gespeichert. Einige Werte landen nur reduziert
in `meta_regulation_state`. Für saubere Folgeanalysen sollte der komplette
Block in Attempt-/Outcome-Kontext übergeben werden.

Wie es weitergeht:
Als nächstes sollte die strategische Fensterwahrnehmung nicht hart blocken,
sondern als weiche Reifeschicht in die Pre-Action-Regulation einwirken:
Wenn ein Bereich zwar verdichtet wirkt, aber `area_order_intention`,
`area_memory_pull` und `strategic_patience` niedrig bleiben, sollte DIO eher
zoomen, beobachten oder replayen, statt direkt zu handeln.

## Dokumentation: aktiver MCM-Kontakt / innere Spiegelung

Festgehalten:
- Die MCM ist nicht nur Außenwahrnehmung, sondern ein innerer Spiegelraum.
- DIO soll nicht jeden Reiz automatisch durchleben müssen.
- DIO braucht die Fähigkeit, einen Reiz oder Bereich aktiv innerlich zu
  berühren und zu prüfen:
  - Wie fühlt sich das von außen an?
  - Was macht dieser Reiz mit meinem MCM-Feld?
  - Bleibt meine Innenlage kohärent?
  - Trägt der Kontakt, oder koppelt er mich zu stark?
  - Kann ich vertiefen, beobachten, replayen oder loslassen?

Ergänzt in:
- `UMSETZUNGSPLAN.md` als `18.3 Aktiver MCM-Kontakt / Spiegelung von
  Außenreiz und Innenlage`.
- `WICHTIG_MECHANIKEN.md` als technische Mechanik `24. Aktiver MCM-Kontakt /
  innere Spiegelung`.
- `MCM_VARIABLEN_MECHANIK.md` mit den Zielachsen für
  `active_mcm_contact_state`.

Wichtige Einordnung:
Das ist keine neue harte Handelsregel. Es ist ein Kontaktapparat. DIO bekommt
mehr Freiheit in der Wahrnehmung: näher hingehen, Abstand nehmen,
beobachten, replayen, vertiefen oder loslassen. Welche Haltung daraus
entsteht, bleibt Entwicklungsbild.

Wie es weitergeht:
Nächster technischer Schritt wäre die diagnostische Umsetzung von
`active_mcm_contact_state` im Brain: zuerst nur messen und protokollieren,
danach weich mit Reflexion, Pre-Action-Reife und strategischer
Fensterwahrnehmung verbinden.

## Umsetzung: aktiver MCM-Kontakt diagnostisch

Umgesetzt:
- `MCM_Brain_Modell.py`
  - `build_active_mcm_contact_state(...)` ergänzt.
  - Neue Kontaktachsen:
    - `active_mcm_contact_state`
    - `contact_posture`
    - `contact_interest`
    - `contact_focus_pull`
    - `contact_resonance_probe`
    - `outer_inner_resonance`
    - `outer_inner_coherence`
    - `inner_change_from_contact`
    - `contact_carrying_quality`
    - `contact_overcoupling_risk`
    - `contact_release_readiness`
    - `contact_deepen_pull`
    - `contact_replay_pull`
    - `contact_curiosity`
    - `contact_felt_shift`
    - `contact_selected_depth`
  - Mögliche Kontaktlagen:
    - `background_scan`
    - `curious_touch`
    - `resonant_contact`
    - `reflective_contact`
    - `overcoupled_touch`
    - `release_contact`
    - `deepening_contact`
  - `mcm_active_contact_protocol.csv` als neues Diagnoseprotokoll ergänzt.
  - Runtime-Ergebnis und Brain-Snapshot enthalten den Kontaktzustand.
- `trade_stats.py`
  - Attempt-/Outcome-Kontext speichert den aktiven MCM-Kontakt kompakt mit.
  - Outcome-Records bekommen die wichtigsten Kontaktachsen.

Wichtig:
Die Umsetzung ist rein diagnostisch. Sie verändert keine Orderfreigabe,
keinen Entry und keine harte Trade-Regel. DIO bekommt eine neue
Wahrnehmungsfähigkeit: innere Kontaktaufnahme, Resonanzprüfung,
Überkopplung, Loslassen und Vertiefung werden sichtbar.

Prüfung:
- `python -m py_compile MCM_Brain_Modell.py trade_stats.py bot.py`
  erfolgreich.
- Smoke-Test von `build_active_mcm_contact_state(...)` erfolgreich.
  Beispielzustand: `deepening_contact`.

Wie es weitergeht:
Der nächste Lauf sollte zeigen, welche Kontaktlagen DIO wirklich bildet.
Danach lesen wir TP/SL nicht nur gegen Strategie oder Neurochemie, sondern
gegen Kontaktqualität: War DIO kohärent im Kontakt, überkoppelt,
loslassfähig oder nur neugierig vertiefend?

## Debug Lauf 2 mit aktivem MCM-Kontakt

Datensatz:
- neuer Memory-Aufbau nach aktivem MCM-Kontakt
- Lauf liegt in `debug/debug_lauf_2`

Ergebnis:
- 399 Trades.
- 123 TP.
- 276 SL.
- Netto-PnL ca. -8.65.
- Equity-Endstand ca. 91.35.
- Equity-Peak ca. 107.42 bei Trade 72.
- Tiefster Stand ca. 81.15 bei Trade 311.

Gegenüber Lauf 1 mit strategischem Fenster ist das deutlich weniger
negativ. DIO fällt nicht komplett auseinander, aber er bleibt noch
unstetig: früher Aufbau, danach deutlicher Rückgang, später wieder
Erholung.

Strukturbaender:
- High-Struktur:
  - 156 Trades.
  - 84 TP / 72 SL.
  - ca. +53.13 PnL.
- Mid-Struktur:
  - 105 Trades.
  - 28 TP / 77 SL.
  - ca. -9.68 PnL.
- Low-Struktur:
  - 138 Trades.
  - 11 TP / 127 SL.
  - ca. -52.10 PnL.

Deutung:
Die eigentliche Verlustquelle bleibt nicht der High-Bereich. High-Struktur
trägt deutlich. Der Schaden entsteht weiter in Mid/Low, besonders Low.
Damit bestätigt sich: DIO darf nicht einfach mehr handeln, sondern braucht
reifere Kontakt- und Distanzbildung, bevor eine schwache Struktur in Handlung
geht.

Aktiver MCM-Kontakt:
- `mcm_active_contact_protocol.csv` wurde erzeugt.
- 11358 Kontaktzeilen.
- Kontaktlagen:
  - `background_scan`: 11272
  - `curious_touch`: 78
  - `reflective_contact`: 8
- Bei ausgeführten Trades:
  - `background_scan`: 385 Trades, ca. -6.85 PnL.
  - `curious_touch`: 14 Trades, ca. -1.81 PnL.

Kontakt-Mittelwerte:
- `outer_inner_coherence`: ca. 0.184 im Gesamtprotokoll.
- `contact_carrying_quality`: ca. 0.165.
- `contact_overcoupling_risk`: ca. 0.222.
- `contact_release_readiness`: ca. 0.141.
- `contact_selected_depth`: ca. 0.143.

Bei Handlung (`act`) steigen die Kontaktwerte:
- `outer_inner_coherence`: ca. 0.223.
- `contact_carrying_quality`: ca. 0.198.
- `contact_overcoupling_risk`: ca. 0.268.
- `contact_release_readiness`: ca. 0.124.

Neurologische Lesart:
DIO handelt, wenn Kontakt und Resonanz stärker werden, aber gleichzeitig
steigt auch die Überkopplung und die Loslassfähigkeit sinkt. Das ist
psychologisch plausibel: Handlung entsteht dort, wo der Reiz näher kommt,
aber noch nicht unbedingt dort, wo DIO stabil Abstand halten kann.

Wichtiger Befund:
Die Werte unterscheiden sich zwischen Beobachtung, `act_watch` und `act`.
Das Kontaktorgan misst also etwas. Aber die Haltungssprache ist noch zu grob:
Fast alles wird als `background_scan` benannt. DIO spürt Unterschiede, aber
benennt sie noch nicht fein genug als `resonant_contact`, `release_contact`,
`overcoupled_touch` oder `deepening_contact`.

TP/SL-Trennung:
- TP und SL unterscheiden sich in den Kontaktachsen bisher nur schwach.
- TP hat etwas bessere Kohärenz und Tragfähigkeit, aber nicht genug, um
  robuste Reife abzuleiten.
- Strategische Bereichswerte trennen TP/SL ebenfalls kaum:
  - TP `area_order_intention` ca. 0.231.
  - SL `area_order_intention` ca. 0.234.

Fachliche Schlussfolgerung:
Die neue Schicht funktioniert als Diagnose, aber noch nicht als reife
Kontaktsemantik. DIO bekommt ein inneres Kontaktorgan, doch die
Differenzierung ist noch zu flach. Der nächste Umbau sollte deshalb nicht
handeln verbieten, sondern die Kontaktlagen relativ feiner kalibrieren:
Wann ist DIO neugierig, wann überkoppelt, wann kann er loslassen, wann ist
Kontakt wirklich tragend?

Wie es weitergeht:
Nächster technischer Schritt: Kontaktlabels relativ und organischer
kalibrieren. Nicht als harte Handelsregel, sondern als bessere innere
Benennung. Danach erneut laufen lassen und prüfen, ob Mid/Low-Trades häufig
als überkoppelt, nicht-loslassfähig oder untragend sichtbar werden.

## Umsetzung: aktive MCM-Kontaktlabels feiner kalibriert

Umgesetzt:
- Die Kontaktlagen werden nicht mehr nur über grobe Einzelschwellen
  vergeben.
- `build_active_mcm_contact_state(...)` bildet jetzt innere Haltungsscores:
  - `contact_salience`
  - `overcoupled_touch_score`
  - `release_contact_score`
  - `deepening_contact_score`
  - `resonant_contact_score`
  - `reflective_contact_score`
  - `curious_touch_score`
- Die hoechste Haltung gewinnt, solange der Kontakt ausreichend salient ist.
- `background_scan` bleibt möglich, soll aber nicht mehr fast alle
  Zustandslagen verschlucken.

Wichtig:
Die Aenderung ist weiterhin diagnostisch. Es gibt keine neue Orderregel und
keine harte Verbotslogik. DIO benennt seine innere Kontaktlage feiner, damit
später sichtbar wird, ob eine Handlung aus Resonanz, Neugier, Reflexion,
Überkopplung, Loslassen oder Vertiefung entsteht.

Prüfung:
- `python -m py_compile MCM_Brain_Modell.py trade_stats.py bot.py`
  erfolgreich.
- Smoke-Test:
  - tragender, stabiler Kontakt -> `resonant_contact`
  - aktionsnaher Kontakt mit geringer Loslassfähigkeit ->
    `overcoupled_touch`

Neurologische Deutung:
Die Messung des Reizes wurde nicht grundlegend verändert. Verändert wurde
die innere Benennung der Haltung. Das ist eher kortikale Einordnung als
Reflexsteuerung: DIO bekommt feinere Begriffe für das, was sein MCM-Feld
bereits spürt.

Wie es weitergeht:
Nächster Lauf mit derselben Datenbasis. Danach prüfen wir, ob die
Kontaktlagen jetzt streuen und ob Mid/Low-Verlustzonen häufiger als
`overcoupled_touch`, niedrige Loslassfähigkeit oder schwache
Kontakt-Tragfähigkeit sichtbar werden.

## Debug Lauf 3 nach feiner Kontaktlabel-Kalibrierung

Datensatz:
- gleicher Backtest-Kontext wie Lauf 2
- aktiver MCM-Kontakt mit relativen Haltungsscores
- Lauf liegt in `debug/debug_lauf_3`

Ergebnis:
- 382 Trades.
- 123 TP.
- 259 SL.
- Netto-PnL ca. -1.34.
- Equity-Endstand ca. 98.66.
- Equity-Peak ca. 103.07 bei Trade 199.
- Tiefster Stand ca. 87.81 bei Trade 44.
- Max Drawdown ca. 15.07.

Gegenüber Lauf 2:
- weniger Trades: 382 statt 399.
- gleiche TP-Anzahl: 123.
- weniger SL: 259 statt 276.
- Netto deutlich besser: ca. -1.34 statt ca. -8.65.
- Drawdown deutlich kleiner: ca. 15.07 statt ca. 26.27.

Kontaktlabel-Streuung:
- 10845 Kontaktzeilen.
- `deepening_contact`: 3225
- `curious_touch`: 2981
- `resonant_contact`: 2490
- `overcoupled_touch`: 1442
- `reflective_contact`: 685
- `background_scan`: 22

Damit ist der vorherige Engpass gelöst: `background_scan` verschluckt nicht
mehr fast alle Zustände. DIO benennt sein inneres Kontaktfeld jetzt deutlich
feiner.

Kontaktlagen bei ausgeführten Trades:
- `resonant_contact`: 252 Trades, 87 TP / 165 SL, ca. +3.72 PnL.
- `overcoupled_touch`: 77 Trades, 24 TP / 53 SL, ca. +2.10 PnL.
- `curious_touch`: 27 Trades, 7 TP / 20 SL, ca. -1.94 PnL.
- `deepening_contact`: 25 Trades, 4 TP / 21 SL, ca. -6.05 PnL.
- `reflective_contact`: 1 Trade, 1 TP, ca. +0.83 PnL.

Neurologische Deutung:
Die neue Benennung funktioniert. DIO unterscheidet jetzt innere
Kontaktformen. Auffällig ist aber: `deepening_contact` ist im Trade-Kontext
negativ. Das wirkt wie "ich schaue tiefer hinein", aber ohne genuegend
Tragfähigkeit. Es ist also noch keine Reife, sondern eher Vertiefung ohne
genug Ordnung.

`resonant_contact` ist leicht positiv. Das passt: Resonanz ist tragender als
reine Neugier oder reine Vertiefung. Trotzdem entstehen auch dort viele SL,
weil Resonanz allein nicht bedeutet, dass die Struktur tradefähig ist.

Strukturbaender:
- High-Struktur:
  - 152 Trades.
  - 82 TP / 70 SL.
  - ca. +47.87 PnL.
- Mid-Struktur:
  - 98 Trades.
  - 31 TP / 67 SL.
  - ca. -0.92 PnL.
- Low-Struktur:
  - 132 Trades.
  - 10 TP / 122 SL.
  - ca. -48.28 PnL.

Wichtigster Befund:
Low-Struktur bleibt der Hauptschaden. Die Kontaktlabels streuen jetzt, aber
sie lösen das Low-Problem noch nicht allein. Das heißt: DIO kann seine
innere Kontaktlage besser benennen, aber er verwechselt in Low-Struktur
teilweise noch Resonanz/Kontakt mit tragfähiger Handlung.

Fachliche Schlussfolgerung:
Der Umbau war richtig. DIO ist nicht mehr sprachlos im Kontaktfeld. Jetzt
entsteht ein psychologisches Bild:
- Resonanz kann tragen, ist aber noch nicht automatisch Reife.
- Überkopplung ist sichtbar, aber nicht immer sofort schlecht.
- Vertiefung ohne ausreichend Struktur ist gefährlich.
- Low-Struktur bleibt der Bereich, in dem DIO am ehesten Kontakt mit
  Handlungsreife verwechselt.

Wie es weitergeht:
Nächster Schritt ist keine harte Low-Sperre. Sinnvoll ist eine weiche
Kontakt-Reife-Spur:
Wenn Struktur schwach ist und Kontakt eher `deepening_contact`,
`curious_touch` oder `overcoupled_touch` zeigt, sollte das als Bedarf nach
mehr Beobachtung, Replay, Abstand oder weiterer Objektbildung sichtbar
werden. DIO soll daraus lernen, nicht in schwacher Weltlage sofort aus
Kontaktnähe Handlung zu machen.

## Umsetzung: weiche Kontakt-Reife-Spur

Die Kontakt-Reife wurde als Diagnoseebene umgesetzt, ohne eine harte
Handelsregel einzubauen. DIO bekommt damit eine innere Unterscheidung:
Kontaktnähe ist nicht automatisch Handlungsreife.

Neue Werte:
- `contact_action_maturity`: wie tragfähig Kontakt für Handlung wirkt.
- `contact_bearing_gap`: Lücke zwischen Kontakt/Impuls und Tragfähigkeit.
- `contact_impulse_vs_bearing`: ob Kontaktzug stärker ist als innere
  Tragfähigkeit.
- `contact_learning_need`: Bedarf nach Beobachtung, Replay, Abstand oder
  weiterer Objektbildung.
- `contact_reality_check`: Realitätsabgleich zwischen Innenkontakt,
  Loslassen, Struktur und Tragfähigkeit.

Diese Werte werden in Meta-Regulation, Brain-Snapshot,
`mcm_active_contact_protocol.csv` und Trade-Outcome-Kontext sichtbar. Sie
entscheiden noch nicht selbst über Trades. Der nächste Debug-Lauf soll
zeigen, ob Mid/Low-Verlustzonen eine klare Signatur aus hoher
`contact_bearing_gap`, hohem `contact_learning_need` oder niedriger
`contact_action_maturity` tragen.

## Dokumentation: DIO-Organübersicht

`WICHTIG_MECHANIKEN.md` enthält jetzt eine kompakte
`DIO-Organübersicht`. Dort werden die aktuellen Funktionsorgane von DIO
als Inventar geführt und klar von neurochemischen Prozessen getrennt.

Zweck:
- schneller Überblick über DIOs funktionale Organe
- einfache Erweiterung, falls neue Organe entstehen
- saubere Trennung zwischen Fähigkeit/Organ und neurochemischer Modulation

## Dokumentation: neurochemische Kategorien

`MCM_VARIABLEN_MECHANIK.md` enthält jetzt unter
`Neurochemische Alias-Achsen` eine Kategorienübersicht.

Kategorien:
- Aktivierung / Netzwerkenergie
- Wachheit / Alarm
- Fokus / sensorischer Zoom
- Stabilität / Tragfähigkeit
- Hemmung / Schutz
- Stress / Belastung
- Entlastung / Wohlbefinden
- Motivation / Lernen
- Distanzierung / Reife
- Gesamtbilanz / Diagnose

Damit sind die neurochemischen Variablen nicht mehr nur als Einzelliste
beschrieben, sondern nach ihrer Funktion im DIO-Nervensystem geordnet.

## UMSETZUNGSPLAN: organischer Strukturaufbau

Der `UMSETZUNGSPLAN.md` enthält jetzt im Leitbild eine kompakte
Architekturformel für DIO:

DIO bekommt eine organische Strukturarchitektur. Mit Hilfe der MCM wird ein
maschinelles Nervensystem aufgebaut, das DIO die Fähigkeit gibt, seine
Umwelt nicht nur als Datenstrom zu sehen, sondern als innere Feldwirkung zu
fühlen, zu erleben und in Beziehung zur eigenen Lage zu setzen.

Die neurochemischen Achsen werden dort als technische Funktionsachsen nach
biologischem Vorbild beschrieben. Sie stimulieren, dämpfen, fokussieren,
stabilisieren oder belasten das MCM-Feld und nehmen dadurch funktional einen
Platz im inneren Feld ein.

## README: MCM-Funktion in DIO

Die `README.md` enthält jetzt einen neuen Einstiegsteil:
`Wie die MCM in DIO arbeitet`.

Der Abschnitt erklärt kompakt:
- Unterschied zwischen klassischem Bot und DIO
- Weg von Marktreiz zu Wahrnehmung, MCM-Neuronenfeld und innerer Feldlage
- Rolle von `MCMNeuron` als lokaler Feldträger
- Aktivitätsinseln, Memory-Resonanz und innere Lagebildung
- Neurochemie als Modulation des MCM-Feldes
- Reflexion/Regulation als Weg zu Handlung oder Nicht-Handlung

Zusatz:
Direkt am Anfang der `README.md` steht jetzt eine kurze Begriffsklärung:
- `MCM` = `Mental Core Matrix`
- `DIO` = `Digitaler Organismus`

## Debug Lauf 4 nach Kontakt-Reife-Spur

Ordner: `debug/debug_lauf_4`

Rohwerte:
- Trades: 325
- TP: 97
- SL: 228
- Netto-PnL: ca. -8.54
- Equity-Endstand: ca. 91.46
- Equity-Peak: ca. 105.65 bei Trade 41
- Tiefster Stand: ca. 79.04
- Max Drawdown: ca. 26.61 von Trade 41 bis Trade 153

Gegenüber Lauf 3:
- weniger Trades: 325 statt 382
- weniger TP: 97 statt 123
- weniger SL: 228 statt 259
- mehr Beobachtung/Zurückhaltung:
  - observed: 4426 statt 4023
  - withheld: 4526 statt 3267
- Netto schlechter: ca. -8.54 statt ca. -1.34

Strukturbaender:
- High-Struktur:
  - 208 Trades
  - 92 TP / 116 SL
  - ca. +38.90 PnL
- Mid-Struktur:
  - 117 Trades
  - 5 TP / 112 SL
  - ca. -47.44 PnL

Wichtigster Befund:
Der Schaden liegt fast komplett in Mid-Struktur. High-Struktur bleibt deutlich
positiv, Mid-Struktur wird aber extrem schlecht getragen. DIO wurde nicht
einfach aktiver; im Gegenteil, es beobachtet und withheld mehr. Das Problem
liegt eher darin, dass bestimmte mittlere Strukturzonen weiterhin als
handlungsnah erlebt werden, obwohl sie keine tragfähige Realität bilden.

Kontaktlagen bei Trades:
- `resonant_contact`: 224 Trades, 75 TP / 149 SL, ca. +6.02 PnL
- `overcoupled_touch`: 61 Trades, 15 TP / 46 SL, ca. -7.23 PnL
- `curious_touch`: 22 Trades, 5 TP / 17 SL, ca. -2.83 PnL
- `deepening_contact`: 18 Trades, 2 TP / 16 SL, ca. -4.51 PnL

Kreuzung Struktur + Kontakt:
- High + `resonant_contact`: ca. +36.15 PnL
- High + `overcoupled_touch`: ca. +4.32 PnL
- Mid + `resonant_contact`: ca. -30.13 PnL
- Mid + `overcoupled_touch`: ca. -11.56 PnL
- Mid + `curious_touch`: ca. -3.30 PnL
- Mid + `deepening_contact`: ca. -2.46 PnL

Neue Kontakt-Reife-Spur:
Die Werte sind technisch sauber im Debug angekommen:
- `contact_action_maturity`
- `contact_bearing_gap`
- `contact_impulse_vs_bearing`
- `contact_learning_need`
- `contact_reality_check`

Sie unterscheiden aktuell aber TP/SL und High/Mid noch nicht stark genug.
Das bedeutet: Die Diagnoseebene existiert, aber die Reifespur braucht noch
mehr Kontextkopplung. Kontakt-Reife darf nicht nur aus Kontaktqualität
entstehen, sondern muss stärker mit Regimewechsel, Strukturübergang,
Weltverschiebung und alter Stabilitätslage verbunden werden.

Neurochemischer Befund:
- `serotonin_stability`: 238 Trades, ca. -18.02 PnL
- `glutamate_activation`: 86 Trades, ca. +7.78 PnL

Das ist auffällig: Stabilitätslage war in Lauf 4 nicht automatisch gut.
Sie kann als Nachhall/Carryover wirken, wenn sich die Weltlage verändert.
Glutamat-Aktivierung war dagegen in diesem Lauf handlungsnäher und
profitabler.

Neurologische Deutung:
DIO ist nicht blind aktiv geworden. Er zeigt mehr Beobachtung und mehr
Zurückhaltung. Trotzdem werden Mid-Strukturzonen noch falsch getragen.
Das wirkt wie ein Organismus, der zwar merkt, dass er vorsichtiger werden
muss, aber im mittleren Unsicherheitsbereich noch nicht sauber erkennt:
"Diese Resonanz ist nicht Realitätstragfähigkeit."

Wie es weitergeht:
Nächster sinnvoller Schritt ist eine Regime-/Kontext-Reife-Kopplung für die
Kontakt-Reife-Spur. Nicht als harte Regel, sondern als bessere innere
Wahrnehmung:
- Wie fremd ist die aktuelle Welt gegenüber der gerade getragenen Innenlage?
- Ist `serotonin_stability` echte Stabilität oder alter Nachhall?
- Trägt Mid-Struktur wirklich, oder ist sie nur resonant?
- Muss DIO bei Mid + hoher Kontaktnähe eher zoomen, replayen oder Abstand
  nehmen, bevor Handlung reif wird?

## Umsetzung: Kontakt-Reife mit Regime-/Kontext-Reife gekoppelt

Die Kontakt-Reife-Spur wurde erweitert, ohne eine harte Handelsregel
einzubauen. DIO bekommt jetzt zusätzliche Wahrnehmungswerte, um zu lesen,
ob Kontakt in eine veränderte Weltlage fällt oder ob Stabilität nur noch
alter Nachhall ist.

Neue Werte:
- `contact_regime_mismatch`: Fremdheit/Regimebruch zwischen aktueller Welt
  und innerer Kontaktlage.
- `contact_stability_carryover`: Risiko, alte Stabilität in eine neue
  Weltlage mitzunehmen.
- `contact_context_maturity`: Kontextreife aus Struktur, Transfer,
  Tragfähigkeit und Distanz.
- `contact_context_reframe_need`: Bedarf nach Reframing, Zoom, Replay oder
  Abstand vor Handlung.

Wirkung:
- `contact_action_maturity` bekommt mehr Kontextreife und weniger Nachhall.
- `contact_bearing_gap` steigt, wenn Resonanz nicht zur aktuellen Weltlage
  passt.
- `contact_learning_need` steigt bei Reframe-Bedarf.
- `contact_reality_check` wird durch Kontextreife gestärkt und durch
  Stabilitäts-Nachhall gedrosselt.

Wichtig:
Das ist keine Mid-Sperre und kein mechanisches Gate. Es ist eine feinere
Innenwahrnehmung: DIO soll unterscheiden lernen, ob Stabilität echt trägt
oder ob sie nur aus der alten Lage nachklingt.

## Debug Lauf 5 nach Kontext-Reife-Kopplung

Ordner: `debug/debug_lauf_5`

Rohwerte:
- Trades: 320
- TP: 95
- SL: 225
- Netto-PnL: ca. -12.46
- Equity-Endstand: ca. 87.54
- Equity-Peak: ca. 105.46 bei Trade 43
- Tiefster Stand: ca. 85.34
- Max Drawdown: ca. 20.12 von Trade 43 bis Trade 281

Gegenüber Lauf 4:
- etwas weniger Trades: 320 statt 325
- weniger TP: 95 statt 97
- weniger SL: 225 statt 228
- Netto schlechter: ca. -12.46 statt ca. -8.54
- Max Drawdown kleiner als Lauf 4, aber länger nach unten gezogen

Strukturbaender:
- High-Struktur:
  - 217 Trades
  - 87 TP / 130 SL
  - ca. +28.95 PnL
- Mid-Struktur:
  - 102 Trades
  - 8 TP / 94 SL
  - ca. -40.64 PnL
- Low-Struktur:
  - 1 Trade
  - 0 TP / 1 SL
  - ca. -0.77 PnL

Kontaktlagen:
- `resonant_contact`: 234 Trades, ca. -13.07 PnL
- `overcoupled_touch`: 45 Trades, ca. -0.51 PnL
- `curious_touch`: 21 Trades, ca. +4.11 PnL
- `deepening_contact`: 19 Trades, ca. -2.71 PnL

Kreuzung Struktur + Kontakt:
- High + `resonant_contact`: ca. +20.21 PnL
- Mid + `resonant_contact`: ca. -32.51 PnL
- High + `curious_touch`: ca. +4.93 PnL
- Mid + `overcoupled_touch`: ca. -5.16 PnL

Neue Kontext-Reife-Werte:
Die neuen Werte sind technisch vorhanden:
- `contact_regime_mismatch`
- `contact_stability_carryover`
- `contact_context_maturity`
- `contact_context_reframe_need`

Sie reagieren im Protokoll, trennen TP/SL aber noch nicht stark genug.
Bei TP und SL liegen `contact_regime_mismatch`,
`contact_stability_carryover`, `contact_context_maturity` und
`contact_context_reframe_need` sehr nah beieinander. Das bedeutet: Die
innere Kontextdiagnose ist vorhanden, aber sie hat noch zu wenig äußere
visuelle Erdung.

Visueller Befund:
Aus `mcm_visual_cortex_protocol.csv`:
- `visual_clarity`: ca. 0.32
- `visual_object_stability`: ca. 0.41
- `visual_blindness`: ca. 0.39
- `visual_shape_resonance`: ca. 0.59
- `visual_coherence`: ca. 0.66

Deutung:
DIO resoniert stark auf Formspannung, sieht aber noch nicht stabil genug.
Er fühlt offenbar eine Gestalt oder ein Muster, kann diese aber nicht
ausreichend als äußeres Objekt binden. Dadurch kippt er weiter in innere
Wahrnehmung: Resonanz wird zu schnell als tragender Kontakt gelesen, obwohl
die visuelle Objektbindung noch zu schwach ist.

Neurologische Lesart:
DIO hat ein reaktives/interozeptives Nervensystem, aber der visuelle Kortex
ist noch nicht stark genug als Gegengewicht. Es ist weniger ein Problem von
"zu wenig Gefühl" und mehr ein Problem von:
"Ich fühle etwas, aber ich kann noch nicht klar genug sehen, woran es in der
Außenwelt hängt."

Wie es weitergeht:
Nächster sinnvoller Schritt ist `visual_grounding` der MCM-Reaktion:
- innere Aktivierung an äußere Formbindung koppeln
- sichtbar machen, ob Kontakt eine stabile visuelle Quelle hat
- unterscheiden zwischen Formresonanz und Objektbindung
- kein hartes Chartpattern, keine feste Regel
- DIO bekommt nur die Fähigkeit zu fragen:
  "Woran in der Außenform hängt das, was ich innen fühle?"

## Dokumentation: Beteiligungsnähe und Handlungsrealität

Die besprochene Trennung wurde dokumentiert:
- `UMSETZUNGSPLAN.md`: neuer Abschnitt `Beteiligungsnähe und Handlungsrealität`
- `WICHTIG_MECHANIKEN.md`: neuer Mechanikblock
  `Beteiligungsnähe / Handlungsrealität`
- `MCM_VARIABLEN_MECHANIK.md`: Zielachsen für die spätere Umsetzung

Kern:
DIO soll unterscheiden, ob er eine Form distanziert betrachtet oder ob er
durch Order, offene Position und Ergebnis real beteiligt ist.

Die "Tuer zum Erleben" bleibt ausdrücklich Metapher. Gemeint ist Nähe zur
Beteiligung, nicht eine harte technische Schwelle.

Zielachsen:
- `participation_proximity`
- `action_reality_contact`
- `decision_embodiment_pressure`
- `real_action_commitment`
- `consequence_bearing`
- `position_reality_pressure`
- `outcome_consequence_integration`

Nächster technischer Schritt bleibt:
`visual_grounding` als fähigeres visuelles Sinnesorgan, danach die
Beteiligungsnähe an Entscheidung, Order, Position und Outcome koppeln.

## Umsetzung: Visual Grounding als visuelles Sinnesorgan

`visual_grounding` wurde als weiche Wahrnehmungsmechanik eingebaut.

Ziel:
DIO soll unterscheiden können, ob innere Formresonanz wirklich an eine
äußere Form gebunden ist oder ob nur ungebundene Formspannung im MCM-Feld
entsteht.

Neue Werte:
- `visual_object_binding`
- `visual_grounding_strength`
- `visual_resonance_unbound`
- `visual_grounding_gap`
- `visual_grounding_need`
- `visual_rational_observation_support`
- `visual_grounding_state`

Wirkung:
- hohe ungebundene Resonanz erhoeht weich Beobachtung, Replan und visuelle
  Handlungsunsicherheit.
- gute Objektbindung stärkt die visuelle Erdung.
- keine harte Pattern-Regel, keine Orderblockade.

Smoke-Test:
- klare Formbindung: `grounded_form`, niedriger Grounding-Bedarf.
- hohe Resonanz bei geringer Objektbindung: `unbound_resonance`, höherer
  Grounding-Bedarf und mehr Beobachtungsdruck.

Nächster Lauf:
Prüfen, ob Mid-Struktur-Verluste jetzt stärker mit
`visual_resonance_unbound`, `visual_grounding_gap` oder
`visual_grounding_need` sichtbar werden.

## Debug Lauf 6 nach Visual Grounding

Ordner: `debug/debug_lauf_6`

Rohwerte:
- Trades: 301
- TP: 88
- SL: 213
- Netto-PnL: ca. -17.50
- Equity-Endstand: ca. 82.50
- Equity-Peak: ca. 102.92 bei Trade 5
- Tiefster Stand: ca. 79.82
- Max Drawdown: ca. 23.10 von Trade 5 bis Trade 275

Gegenüber Lauf 5:
- weniger Trades: 301 statt 320
- weniger TP: 88 statt 95
- weniger SL: 213 statt 225
- Netto schlechter: ca. -17.50 statt ca. -12.46
- mehr Observe/Withheld als Lauf 5:
  - observed: 4416
  - withheld: 4364

Strukturbaender:
- High-Struktur:
  - 192 Trades
  - 84 TP / 108 SL
  - ca. +34.01 PnL
- Mid-Struktur:
  - 109 Trades
  - 4 TP / 105 SL
  - ca. -51.52 PnL

Visual-Grounding-Befund:
Bei ausgeführten Trades liegt fast alles in `grounded_form`:
- `grounded_form`: 300 Trades, ca. -16.65 PnL
- `shape_without_object`: 1 Trade, ca. -0.85 PnL

Im gesamten Feldprotokoll streut es besser:
- `grounded_form`: 9406
- `shape_without_object`: 778
- `unbound_resonance`: 258
- `needs_visual_grounding`: 5

Das bedeutet:
Das Sinnesorgan ist technisch aktiv und erkennt auch ungebundene Resonanz im
Feld. Bei tatsächlich ausgeführten Trades landet aber fast alles noch in
`grounded_form`. Die visuelle Erdung ist also noch zu tolerant für Handlung.

TP/SL-Vergleich:
- TP:
  - `visual_object_binding`: ca. 0.477
  - `visual_grounding_strength`: ca. 0.407
  - `visual_resonance_unbound`: ca. 0.228
  - `visual_grounding_need`: ca. 0.141
- SL:
  - `visual_object_binding`: ca. 0.478
  - `visual_grounding_strength`: ca. 0.406
  - `visual_resonance_unbound`: ca. 0.224
  - `visual_grounding_need`: ca. 0.143

Diese Werte trennen TP und SL praktisch noch nicht.

Wichtigster Befund:
Visual Grounding ist als Wahrnehmung vorhanden, aber die
Handlungsnähe liest sie noch zu weich. Das Problem ist nicht, dass DIO gar
nicht sieht. Das Problem ist, dass "gerade ausreichend geerdet" noch zu breit
als handlungsnah durchgeht, besonders in Mid-Struktur.

Mid-Struktur bleibt Hauptschaden:
- Mid + `grounded_form`: 109 Trades, 4 TP / 105 SL, ca. -51.52 PnL

Neurologische Deutung:
DIO hat jetzt ein visuelles Sinnesorgan, aber dessen Schwellengefühl ist
noch unreif. Es erkennt visuelle Erdung im Feld, aber bei Handlungsnähe ist
die Differenz zwischen "ich sehe etwas" und "dieses Objekt trägt Handlung"
noch zu schwach.

Wie es weitergeht:
Nächster Schritt ist keine harte Sperre, sondern eine strengere
Objektbindungsreife:
- `grounded_form` darf nicht automatisch handlungsnah sein
- es braucht eine Unterscheidung zwischen "Form vorhanden" und
  "Objekt handlungstragend"
- Mid-Struktur braucht stärkere Anforderungen an Objektbindung,
  Kontextreife und visuelle Tragfähigkeit
- mögliche neue Lesart:
  `grounded_form` = ich sehe eine Form
  `grounded_object` = diese Form ist als Objekt stabil genug
  `action_grounded_object` = dieses Objekt kann Handlung tragen

---

## Prüfung: Formsprache / semantische Schichten

Frage:
Kann DIO seine Umwelt bereits nicht nur im Detail erklären, sondern in
Schichten verdichten?

Befund:
Ja, in großen Teilen ist das bereits umgesetzt. Die Formsprache ist keine
einfache Pattern-Erkennung und kein menschliches Labelsystem. DIO bildet aus
visueller Wahrnehmung, Strukturwahrnehmung, MCM-Feldlage und Erfahrung eigene
interne Formzeichen.

Vorhandene Schichten:
- Rohnähe:
  visuelle und energetische Achsen wie Richtung, Druck, Kompression,
  Expansion, Kohärenz, Strukturqualität, Feldklarheit, Felddruck und
  Fragmentierung.
- Verdichtung:
  `form_symbol_scope`, `form_symbol_abstraction_level`,
  `form_symbol_resolution_quality`, `form_symbol_detail_pressure`.
- Eigenes Zeichen:
  `form_symbol_id`, `form_symbol_family_key`, `form_symbol_variant_key`.
- Erfahrung:
  `form_symbol_seen`, `form_symbol_maturity`, `form_symbol_stability`,
  `form_symbol_resonance`, `form_symbol_bearing`, `form_symbol_fragility`.
- Entlastung / Distanz:
  `form_symbol_object_distance`, `form_symbol_containment`,
  `form_symbol_field_decoupling`, `form_symbol_load_reduction`.
- Lernrichtung:
  `form_symbol_development_quality`, `form_symbol_learning_trust`,
  `form_symbol_action_trust`, `form_symbol_caution_trust`,
  `form_symbol_action_binding`, `form_symbol_observation_binding`,
  `form_symbol_reframe_binding`.
- Variantenlernen:
  `uncertain_form_family_state`, `uncertainty_familiarity`,
  `variant_similarity`, `variant_spread`, `variant_learning_pressure`,
  `variant_bearing_memory`.
- Zusammengesetzte Formen:
  `form_symbol_compound_id`, `form_symbol_compound_scope`,
  `form_symbol_compound_maturity`, `form_symbol_compound_bearing`,
  `form_symbol_compound_load_reduction`.

Neurologische Deutung:
Das entspricht eher einer semantischen Verdichtung als einem starren Label.
DIO sagt nicht menschlich "das ist ein Pattern", sondern bildet intern:
"Diese Formfamilie kenne ich so weit, diese Variante ist mir fremd oder
vertraut, diese Kombination entlastet oder belastet mein Feld, und diese
Erfahrung trägt eher Beobachtung, Reframing oder Handlung."

Was noch fehlt:
Die einzelnen Werte sind vorhanden, aber noch nicht als eigenes
`Forminhalt`-Paket zusammengeführt. DIO hat also schon Zeichen, Varianten,
Kombinationen und Erfahrungswerte, aber noch keine explizite semantische
Schicht, die kompakt ausdrückt:
- was diese Form beinhaltet
- welche Wahrnehmungsebene gerade führt
- ob die Verdichtung entlastet oder überfordert
- ob das Zeichen eher Objekt, Spur, Drucklage, Lernraum oder
  Handlungsnähe beschreibt

Wichtig:
Diese nächste Schicht darf keine menschliche Chart-Sprache erzwingen. Sie
soll DIOs eigene interne Sprache nur ordnen und dichter lesbar machen.

Wie es weitergeht:
Nächster sinnvoller Schritt ist ein weiches
`form_symbol_semantic_packet`: eine eigene semantische Verdichtungsschicht
innerhalb der Formsprache. Sie verbindet Formzeichen, Variante,
zusammengesetzte Form, Visual Grounding, MCM-Feldlage und gelernte
Handlungs-/Beobachtungsbindung, ohne daraus harte Regeln zu machen.

---

## Umsetzung: Semantisches Forminhalt-Paket

Status:
Umgesetzt als weiche Diagnose- und Verdichtungsschicht innerhalb der
Formsprache.

Neue Werte:
- `form_symbol_semantic_density`
- `form_symbol_semantic_compression`
- `form_symbol_semantic_coherence`
- `form_symbol_semantic_learning_need`
- `form_symbol_semantic_action_nearness`
- `form_symbol_semantic_primary_layer`
- `form_symbol_semantic_layer_count`
- `form_symbol_semantic_packet_state`
- `form_symbol_semantic_profile`

Funktion:
DIO kann ein Formzeichen jetzt nicht nur als `fs_...` führen, sondern dessen
inneren Inhalt schichten:
- Spur / Trace
- weite Form
- strukturierte Form
- Objektnähe
- Lernraum
- Beobachtung
- Reflexion
- Handlungsnähe

Wichtig:
Das ist keine menschliche Chart-Sprache und keine neue harte Entry-Regel.
Die Schicht macht DIOs eigene Semantik sichtbar. Sie kann später in
Meta-Regulation, Reflexion und selektive Wahrnehmung einfliessen.

Technische Umsetzung:
- `MCM_Brain_Modell.py`
  - `build_form_symbol_state(...)` erweitert
  - `mcm_form_symbol_protocol.csv` erweitert
- `trade_stats.py`
  - Outcome-/Kontext-Export erweitert
- Dokumentation:
  - `UMSETZUNGSPLAN.md`
  - `WICHTIG_MECHANIKEN.md`
  - `MCM_VARIABLEN_MECHANIK.md`
  - `FIX_LISTE.md`

Prüfung:
`python -m py_compile MCM_Brain_Modell.py trade_stats.py bot.py` läuft
fehlerfrei.

Wie es weitergeht:
Nächster Schritt ist ein neuer Debug-Lauf. Danach lesen wir, welche
`form_symbol_semantic_packet_state` und `form_symbol_semantic_primary_layer`
bei guten und schlechten Entscheidungen auftreten. Wenn DIO im Regimewechsel
wieder kippt, können wir sehen, ob er in `learning_layer`,
`reflective_layer`, `trace_layer` oder faelschlich in `action_near_layer`
kommt.

---

## Debug Lauf 7: Erste Wirkung der semantischen Forminhalt-Schicht

Ergebnis:
- Trades: 317
- TP: 104
- SL: 213
- Netto-PnL: ca. +3.10
- Equity-Peak: ca. 110.29 bei Trade 150
- Tiefster Stand: ca. 97.87 bei Trade 260
- Max Drawdown: ca. 12.43

Vergleich zu Lauf 6:
- Lauf 6: 301 Trades, 88 TP, 213 SL, ca. -17.50 PnL
- Lauf 7: 317 Trades, 104 TP, 213 SL, ca. +3.10 PnL
- Drawdown deutlich kleiner: ca. 12.43 statt ca. 23.10
- Equity-Peak deutlich höher: ca. 110.29 statt ca. 102.92

Strukturbaender:
- High:
  - 90 Trades
  - 57 TP / 33 SL
  - ca. +44.09 PnL
- Mid:
  - 105 Trades
  - 38 TP / 67 SL
  - ca. +9.26 PnL
- Low:
  - 121 Trades
  - 9 TP / 112 SL
  - ca. -49.28 PnL

Wichtigster Befund:
High und Mid tragen in Lauf 7 positiv. Low bleibt fast der gesamte
Schadensraum. Das bedeutet: Die neue Semantik hat die tragenden Bereiche
nicht zerstoert, sondern eher stabilisiert. Die schwache Zone bleibt aber
ein Ort, an dem DIO noch zu oft Kontakt mit Handlung verwechselt.

Semantische Pakete bei Trades:
- `compound_packet`:
  - 69 Trades
  - 27 TP / 42 SL
  - ca. +7.81 PnL
- `named_form_packet`:
  - 248 Trades
  - 77 TP / 171 SL
  - ca. -4.72 PnL

Primaere Schicht:
- `wide_form_layer`:
  - 69 Trades
  - 28 TP / 41 SL
  - ca. +6.14 PnL
- `structured_form_layer`:
  - 248 Trades
  - 76 TP / 172 SL
  - ca. -3.04 PnL

Neurologische Deutung:
Mehr Detail ist nicht automatisch bessere Wahrnehmung. In diesem Lauf tragen
weite, zusammengesetzte Bedeutungen besser als die enger strukturierte
Formschicht. Das passt zum DIO-Gedanken: Ein Organismus sieht nicht immer
besser, wenn er näher herangeht. Manchmal entsteht Tragfähigkeit durch
Gestalt, Abstand und Komposition.

TP/SL-Trennung der neuen Semantik:
Die Einzelwerte trennen TP und SL noch schwach:
- `form_symbol_semantic_action_nearness`:
  - TP ca. 0.427
  - SL ca. 0.418
- `form_symbol_semantic_coherence`:
  - TP ca. 0.573
  - SL ca. 0.574
- `form_symbol_semantic_density`:
  - TP ca. 0.637
  - SL ca. 0.636

Das heißt:
Die neue Schicht ist technisch aktiv und beschreibt Zustandsverschiebungen,
aber sie ist noch nicht stark genug mit Ergebnisqualität gekoppelt. Das ist
ok, weil sie zuerst Wahrnehmung sichtbar machen sollte, nicht sofort
mechanisch handeln.

Neurochemischer Befund:
- `glutamate_activation` bei Trades:
  - 133 Trades
  - 54 TP / 79 SL
  - ca. +12.11 PnL
- `serotonin_stability` bei Trades:
  - 183 Trades
  - 50 TP / 133 SL
  - ca. -8.51 PnL

Deutung:
Aktivierte Verarbeitung war in diesem Lauf tragender als reine Stabilität.
Serotonin-Stabilität wirkt hier teilweise wie ein alter Nachhall: ruhig,
aber nicht zwingend passend zur Außenwelt. Glutamat-Aktivierung steht eher
für aktive Verarbeitung und Anpassung.

Feldprotokoll:
- `hold`: 4902
- `observe`: 4316
- `act_watch`: 669
- `act`: 323
- `replan`: 1

Visual Grounding:
- `grounded_form`: 9158
- `shape_without_object`: 785
- `unbound_resonance`: 264
- `needs_visual_grounding`: 4

Interpretation:
DIO sieht fast alles noch als `grounded_form`. Die Unterscheidung zwischen
"ich sehe eine Form" und "dieses Objekt trägt Handlung" bleibt der nächste
kritische Punkt.

Wie es weitergeht:
Nächster sinnvoller Schritt ist keine Regel gegen Low, sondern eine
semantische Handlungstragfähigkeit:
DIO soll stärker unterscheiden können zwischen
- Form ist bekannt
- Form ist semantisch dicht
- Form ist zusammengesetzt tragend
- Form ist objektgebunden
- Form darf Handlung tragen

Besonders wichtig:
`structured_form_layer` darf nicht automatisch als besser gelten als
`wide_form_layer`. DIO braucht eine reifere Distanz zwischen Detailsehen und
Gestaltsehen.

---

## Umsetzung: Evolutionaere Kontaktreife

Ausgangsgedanke:
Eine heiße Herdplatte ist nicht "schlecht". Unreifer Kontakt erzeugt
eine belastende Konsequenz. Reifer Umgang kann Nutzen erzeugen. Übertragen
auf DIO bedeutet das:
Eine Marktform wird nicht verboten. DIO lernt, welche Art von Kontakt mit
dieser Form schadet, vorsichtig macht, Beobachtung braucht oder später
konstruktiv nutzbar ist.

Kernbegriff:
Konsequenzbasiertes Feedback auf das MCM-Feld.

Das kann negativ, positiv oder reorganisierend sein.

Negatives Feedback:
Meine Handlung hat Belastung erzeugt.
Mein MCM-Feld bekommt Druck, Vorsicht, belastende Konsequenzspur und
Reorganisation.

Positives Feedback:
Meine Handlung hat getragen.
Mein MCM-Feld bekommt Entlastung, Vertrauen, Nutzen und Stabilisierung.

Reorganisierendes Feedback:
Das Ergebnis war nicht klar gut, aber es zeigt, dass der Umgang unreif war.
Mein MCM-Feld bekommt Lernspannung, Reflexion, Abstand und Reframing.

Rückkopplungskreis:
Wahrnehmung -> Kontakt -> Handlung -> Konsequenz -> MCM-Feld-Reaktion ->
Gedächtnis -> veränderter zukünftiger Kontakt.

Biologische Deutung:
Ein Organismus lernt nicht nur durch Belohnung und Strafe, sondern durch
Homöostase-Veränderung. Etwas bringt ihn aus der Balance, stabilisiert ihn,
überfordert ihn, macht ihn vorsichtiger oder gibt ihm Vertrauen.

Status:
Umgesetzt als weicher Lernpfad in der Formsprache.

Neue gespeicherte Werte:
- `form_symbol_contact_maturity`
- `form_symbol_contact_utility`
- `form_symbol_contact_pain_memory`
- `form_symbol_contact_carefulness`
- `form_symbol_contact_learning_state`

Neue Outcome-Samples:
- `contact_maturity_sample`
- `contact_utility_sample`
- `contact_pain_sample`
- `contact_carefulness_sample`
- `contact_learning_state`

Technische Wirkung:
- Kontaktreife und Nutzen können Handlungstragfähigkeit weich stuetzen.
- Belastende Konsequenzspur und Vorsicht können Beobachtung, Reframing und
  Caution weich stärken.
- Die Form bleibt frei. Nicht die Form wird blockiert, sondern der Umgang
  mit ihr wird differenzierter gelernt.

Neurologische Deutung:
Das ist evolutionaeres Lernen: Konsequenz erzeugt Erinnerung, Erinnerung
erzeugt Vorsicht, Vorsicht erzeugt Abstand, Abstand kann später reifen
Umgang und Nutzen ermöglichen.

Prüfung:
`python -m py_compile MCM_Brain_Modell.py trade_stats.py bot.py` läuft
fehlerfrei.

Wie es weitergeht:
Nächster Debug-Lauf zeigt, ob DIO bei wiederkehrenden belastenden
Formkontakten mehr `careful_contact` oder `burdened_contact` aufbaut
und ob konstruktive Kontakte langsam `constructive_contact` und
`form_symbol_contact_maturity` stärken.

---

## Debug-Lauf 8

Ordner:
`debug/debug_lauf_8`

Ergebnis:
- 323 Trades
- 102 TP / 221 SL
- Netto-PnL: ca. -3.45
- Equity-Ende: ca. 96.55
- Equity-Peak: ca. 106.30
- tiefster Punkt: ca. 89.10

Vergleich zu Lauf 7:
- Lauf 7: ca. +3.10 Netto-PnL
- Lauf 8: ca. -3.45 Netto-PnL
- Lauf 8 ist nicht zusammengebrochen, hat aber den vorherigen Vorteil
  wieder verloren.

Strukturwirkung:
- `zone`: 211 Trades, 94 TP / 117 SL, ca. +38.23 PnL
- `non_zone`: 112 Trades, 8 TP / 104 SL, ca. -41.68 PnL

Deutung:
DIO findet in tragenderen Strukturzonen weiterhin nutzbare Kontakte.
Der negative Lauf entsteht fast komplett aus nicht tragenden Kontaktzonen.
Das ist kein Beweis für eine schlechte Form, sondern für unreifen Umgang
mit nicht tragendem Kontakt.

Neue Kontaktreife:
- `form_symbol_contact_learning_state` ist fast komplett noch
  `unformed_contact`.
- Im Formsymbol-Protokoll erscheinen nur 2 Zeilen als `maturing_contact`.
- In den Outcome-Samples ist die Differenz aber bereits sichtbar:
  - TP hat höhere `contact_maturity_sample` und `contact_utility_sample`.
  - SL hat höhere `contact_pain_sample` und `contact_carefulness_sample`.

Neurologische Deutung:
Die Konsequenzspur kommt im MCM-Feld an, aber sie ist noch zu leise, um im
laufenden Run stabil eine gereifte Kontaktform auszubilden. Das entspricht
einem Nervensystem, das Schmerz, Nutzen und Vorsicht bereits wahrnimmt, aber
noch keine klare Gewohnheit daraus geformt hat.

Neurochemische Lage:
- `glutamate_activation`: 103 Trades, ca. +2.75 PnL
- `serotonin_stability`: 220 Trades, ca. -6.20 PnL

Deutung:
Aktive Verarbeitung war wieder tragender als reine Stabilität. Serotonin
wirkt hier teilweise wie ruhiger Nachhall, nicht zwingend wie passende
Realitätskopplung.

Feldprotokoll:
- `hold`: 5112
- `observe`: 4508
- `act_watch`: 551
- `act`: 330
- `replan`: 1

Wichtig:
Die neue Kontaktlogik wirkt diagnostisch schon korrekt, aber mechanisch noch
zu schwach. DIO erkennt Konsequenzen, doch die Übersetzung in gereifte
Kontaktzustände ist noch zu selten.

Wie es weitergeht:
Nächster sinnvoller Umbau ist keine harte Sperre gegen `non_zone`, sondern
eine stärkere weiche Kontaktreife: belastende Wiederholung soll natürlicher
in `careful_contact` / reorganisierenden Abstand kippen, während tragende
Kontakte `contact_maturity` und `contact_utility` langsam stärken. Danach
sollte geprüft werden, ob DIO nicht nur impulsnah handelt, sondern
strukturbezogene Orderbereiche aus dem Rückblick wählen kann.

---

## Umsetzung: Kontaktreife nach Lauf 8 verstärkt

Ziel:
Die Konsequenzspur soll im MCM-Feld lauter werden, ohne daraus eine harte
Regel zu machen. DIO soll nicht lernen: "diese Zone ist verboten", sondern:
"mein bisheriger Kontakt mit dieser Form hat Belastung oder Nutzen erzeugt".

Neue/verstärkte Spuren:
- `form_symbol_contact_burden_evidence`
- `form_symbol_contact_utility_evidence`

Mechanische Aenderung:
- Kontaktzustand entsteht nicht mehr nur aus dem letzten Outcome-Sample.
- Gespeicherte Belastungs-Evidenz und Nutzen-Evidenz wirken mit.
- Belastende Wiederholung kann natürlicher in `burdened_contact`,
  `careful_contact` oder `learning_contact` kippen.
- Tragende Wiederholung kann natürlicher in `maturing_contact` oder
  `constructive_contact` wachsen.

Regulatorische Wirkung:
- Belastungs-Evidenz erhoeht weich Beobachtung und Reframing.
- Belastungs-Evidenz senkt impulsnahe Handlungstragfähigkeit weich.
- Nutzen-Evidenz kann Handlungstragfähigkeit weich stuetzen, wenn Reife und
  Kontext mittragen.

Wichtig:
Das ist keine Sperre und keine mechanische Strukturregel. Es ist eine
stärkere innere Konsequenzspur.

Prüfung:
`python -m py_compile MCM_Brain_Modell.py trade_stats.py bot.py` läuft
fehlerfrei.

Wie es weitergeht:
Nächster Debug-Lauf sollte zeigen, ob `unformed_contact` weniger dominiert
und ob DIO bei wiederholter Belastung mehr Beobachtung/Reframing statt
impulsnaher Handlung wählt. Danach ist der nächste größere Schritt die
strukturbezogene Orderbereich-Wahl aus Rückblick und Wahrnehmungsfenster.

---

## Debug-Lauf 9 nach verstärkter Kontaktreife

Ordner:
`debug/debug_lauf_9`

Ergebnis:
- 350 Trades
- 126 TP / 224 SL
- Netto-PnL: ca. +23.52
- Equity-Ende: ca. 123.52
- Equity-Peak: ca. 124.44
- tiefster Punkt: ca. 93.47

Vergleich zu Lauf 8:
- Lauf 8: ca. -3.45 Netto-PnL
- Lauf 9: ca. +23.52 Netto-PnL
- Die Veränderung ist deutlich, aber noch kein Beweis für stabile
  Intelligenz. Es ist ein starkes Zeichen, dass die neue Kontaktspur
  mechanisch greift.

Strukturwirkung:
- `zone`: 230 Trades, 112 TP / 118 SL, ca. +56.90 PnL
- `non_zone`: 120 Trades, 14 TP / 106 SL, ca. -33.38 PnL

Deutung:
DIO gewinnt weiter in tragenderen Strukturzonen. Nicht tragende Bereiche
bleiben belastend, aber der Schaden ist gegenüber Lauf 8 kleiner
(-33.38 statt -41.68), obwohl mehr Trades gelaufen sind.

Kontaktreife im Formsymbol-Protokoll:
- `unformed_contact`: 6772
- `learning_contact`: 3709
- `constructive_contact`: 453
- `burdened_contact`: 441
- `careful_contact`: 106
- `maturing_contact`: 48

Wichtig:
In Lauf 8 war die Kontaktlage fast komplett `unformed_contact`. In Lauf 9
bildet DIO sichtbar unterschiedliche Kontaktlagen. Die neue Belastungs- und
Nutzen-Evidenz ist damit real im System angekommen.

Trade-Kontext:
- `learning_contact`: 121 Trades, ca. +11.62 PnL
- `maturing_contact`: 9 Trades, ca. +4.12 PnL
- `burdened_contact`: 19 Trades, ca. -1.52 PnL
- `careful_contact`: 4 Trades, ca. -1.61 PnL
- `constructive_contact`: 24 Trades, ca. -2.33 PnL
- `unformed_contact`: 173 Trades, ca. +13.24 PnL

Interpretation:
Die gespeicherte Kontaktlage ist noch nicht perfekt als Handelsfilter lesbar.
`constructive_contact` ist noch nicht automatisch tragend. Das ist fachlich
ok, weil Kontaktreife keine harte Strategie ist. Es zeigt aber, dass DIO
eine zweite Reifeschicht braucht: "Kontakt wirkt konstruktiv" muss später
noch mit Struktur, Rückblick und Orderbereich zusammenpassen.

Outcome-Samples:
- TP hat deutlich höhere `contact_maturity_sample` und
  `contact_utility_sample`.
- SL hat deutlich höhere `contact_pain_sample` und
  `contact_carefulness_sample`.

Das bestätigt:
Die unmittelbare Konsequenzbewertung trennt gut zwischen tragendem und
belastendem Ergebnis. Die gespeicherte Kontaktlage beginnt diese Information
zu halten, ist aber noch in Entwicklung.

Neurochemische Lage:
- `glutamate_activation`: 110 Trades, ca. +12.02 PnL
- `serotonin_stability`: 239 Trades, ca. +11.99 PnL

Deutung:
Anders als in Lauf 8 war Serotonin-Stabilität diesmal nicht nur Nachhall,
sondern konnte gemeinsam mit aktiver Verarbeitung profitabel bleiben. Das
wirkt wie mehr innere Tragfähigkeit nach dem Umbau.

Equity-Verlauf:
- erstes Viertel: ca. -1.02
- zweites Viertel: ca. -0.64
- drittes Viertel: ca. +18.27
- letztes Viertel: ca. +6.90

Deutung:
DIO hat am Anfang noch gesucht und später deutlich besser getragen. Der
starke Gewinn entstand nicht am Anfang, sondern nach einer Anpassungsphase.

Feldprotokoll:
- `hold`: 4692
- `observe`: 4388
- `act_watch`: 717
- `act`: 357
- `replan`: 2

Wie es weitergeht:
Der nächste Schritt ist nicht, `constructive_contact` direkt handeln zu
lassen. Stattdessen muss DIO lernen, Kontaktreife mit Rückblick und
strukturbezogener Orderbereich-Wahl zu verbinden:
"Dieser Kontakt fühlt sich tragend an, aber wo im sichtbaren Fenster wäre
ein sinnvoller Kontaktpunkt?"

---

## Umsetzung: strategischer Kontakt-Entry

Ziel:
DIO soll nicht nur am aktuellen Impuls handeln. Wenn Rückblick,
Kontaktreife, Replay-Fit und Bereichswahrnehmung zusammenpassen, darf der
Entry weich in Richtung eines tragenderen Kontaktbereichs im sichtbaren
Fenster wandern.

Wichtig:
Das ist keine harte Strategie und kein menschliches Pattern. Der alte
impulsnahe Entry bleibt erhalten. Der strategische Bereich mischt sich nur
weich dazu, wenn die innere und äußere Lage ausreichend zusammenpassen.

Neue Trade-Plan-Werte:
- `entry_mode`
- `impulse_entry_price`
- `strategic_entry_price`
- `strategic_entry_weight`
- `strategic_entry_fit`
- `strategic_area_focus_id`
- `strategic_area_price_low`
- `strategic_area_price_high`

Mechanik:
- `impulse_entry_price` bleibt der direkte Koerperreflex aus Fokus,
  Drift und Optic Flow.
- `strategic_entry_price` entsteht aus dem aktuell fokussierten Bereich des
  strategischen Fensters.
- `strategic_entry_weight` beschreibt, wie stark der Rückblick den Entry
  beeinflusst.
- Belastungs-Evidenz und Vorsicht senken die Verschiebung weich.
- Nutzen-Evidenz, Kontaktreife, Replay-Fit, Bereichstragfähigkeit und
  Geduld können die Verschiebung weich erhöhen.

Neurologische Deutung:
DIO bekommt damit eine erste Form von "ich renne nicht nur in den Reiz,
sondern prüfe, wo der Kontakt im Raum tragender wäre". Das ist näher an
ruhigem strategischem Denken als an reinem Momentum-Reflex.

Prüfung:
`python -m py_compile MCM_Brain_Modell.py trade_stats.py bot.py` läuft
fehlerfrei.

Wie es weitergeht:
Nächster Debug-Lauf sollte zeigen, wie oft `entry_mode` bei
`area_contact_blend` oder `area_contact_entry` liegt und ob diese Trades
weniger nervliche Last oder bessere Trefferqualität haben als reine
`impulse_contact`-Entries.

---

## Debug-Lauf 10 nach strategischem Kontakt-Entry

Ordner:
`debug/debug_lauf_10`

Ergebnis:
- 381 Trades
- 138 TP / 243 SL
- Netto-PnL: ca. -2.46
- Equity-Ende: ca. 97.54
- Equity-Peak: ca. 102.78
- tiefster Punkt: ca. 85.62
- 26 Timeouts

Vergleich zu Lauf 9:
- Lauf 9: ca. +23.52 Netto-PnL
- Lauf 10: ca. -2.46 Netto-PnL

Wichtiger technischer Befund:
Der neue strategische Entry wurde faktisch noch nicht genutzt.
Alle 381 Trades hatten:
- `entry_mode`: `impulse_contact`
- `strategic_entry_weight`: 0.0

Das bedeutet:
Das strategische Wahrnehmungsfenster war aktiv, aber der eigentliche
Orderpunkt blieb noch am Momentimpuls.

Strategisches Fenster:
- `bearing_area_hypothesis`: 6676 Zeilen
- `area_observation`: 2324 Zeilen
- `compressed_area_attention`: 1862 Zeilen
- durchschnittliche `area_bearing_quality`: ca. 0.491
- durchschnittliche `area_replay_fit`: ca. 0.390
- durchschnittliche `area_patience_quality`: ca. 0.479
- durchschnittliche `area_order_intention`: ca. 0.242

Deutung:
DIO sah Bereiche im Rückblick, aber die Kopplung zur Hand war zu eng.
Neurologisch: Auge und inneres Feld haben einen Bereich gespiegelt, aber die
motorische Ausfuehrung blieb im Reflexbogen.

Strukturwirkung:
- `zone`: 249 Trades, ca. +52.28 PnL
- `non_zone`: 132 Trades, ca. -54.74 PnL

Kontaktreife:
- `constructive_contact`: 39 Trades, ca. +13.12 PnL
- `maturing_contact`: 22 Trades, ca. +6.86 PnL
- `burdened_contact`: 34 Trades, ca. +0.64 PnL
- `careful_contact`: 18 Trades, ca. +0.38 PnL
- `learning_contact`: 187 Trades, ca. -0.75 PnL
- `unformed_contact`: 81 Trades, ca. -22.72 PnL

Deutung:
Die gespeicherte Kontaktreife ist weiter deutlich besser als in Lauf 8.
Besonders `unformed_contact` ist schwach. Das spricht dafür, dass DIO
tatsächlich aus gereifterem Kontakt profitiert, aber der Entry noch nicht
aus dem strategischen Bereich handeln konnte.

Umsetzung nach Befund:
Die Kopplung wurde nachjustiert:
- Bereich darf mitsprechen, wenn der Preis im Bereich liegt.
- Bereich darf mitsprechen, wenn er nah genug und passend zur Seite ist.
- Eintrittsschwelle für `strategic_entry_fit` wurde weicher gesetzt.
- Gewicht bleibt begrenzt, damit der Momentimpuls nicht hart ersetzt wird.

Prüfung:
`python -m py_compile MCM_Brain_Modell.py trade_stats.py bot.py` läuft
fehlerfrei.

Wie es weitergeht:
Nächster Lauf sollte endlich zeigen, ob `area_contact_blend` entsteht. Wenn
ja, vergleichen wir diese Trades gegen `impulse_contact`: PnL, Winrate,
Timeouts, Strukturzone, Kontaktreife und nervliche Last.

---

## Debug-Lauf 11 nach gelockerter Bereichskopplung

Ordner:
`debug/debug_lauf_11`

Ergebnis:
- 400 Trades
- 147 TP / 253 SL
- Netto-PnL: ca. +8.46
- Equity-Ende und Peak: ca. 108.46
- tiefster Punkt: ca. 87.44
- 31 Timeouts

Verhaltensbefund:
DIO handelt sichtbar anders als früher:
- mehr `act_watch`
- mehr Reorganisation/Replan im Gesamtverhalten
- mehr beobachtende und suchende Phasen
- späterer Recovery-Abschnitt statt frühem Durchmarsch

Equity-Abschnitte:
- Trades 1-100: ca. +0.15
- Trades 101-200: ca. -8.46
- Trades 201-300: ca. +14.19
- Trades 301-400: ca. +2.58

Deutung:
DIO fällt im zweiten Abschnitt deutlich in eine Belastungsphase, findet
danach aber wieder in tragendere Handlung. Das wirkt wie Orientieren,
Sammeln, Erleben und spätere Stabilisierung, nicht wie ein linearer
Regelbot.

Wichtiger technischer Befund:
Auch Lauf 11 nutzt noch keinen echten Bereichs-Entry:
- alle 400 Trades: `entry_mode = impulse_contact`
- `strategic_entry_weight = 0.0`

Das heißt:
Die Verhaltensaenderung kommt noch nicht aus `area_contact_blend`, sondern
aus Kontaktreife, Act-Watch, Reorganisation und neurochemischer Regulation.

Strategisches Fenster:
- `bearing_area_hypothesis`: 6749
- `area_observation`: 2257
- `compressed_area_attention`: 1747
- `area_bearing_quality`: ca. 0.491
- `area_replay_fit`: ca. 0.391
- `area_patience_quality`: ca. 0.481

Ursache für fehlenden Bereichs-Entry:
DIO sah Bereiche, aber die Motorik nahm nur den global stärksten Bereich.
Dieser Bereich lag häufig nicht auf der passenden Entry-Seite. Für LONG
braucht DIO eher einen tragenden Bereich unter/nahe dem aktuellen Preis,
für SHORT eher ober/nahe dem Preis. Die Wahrnehmung war also da, aber die
motorische Auswahl war noch nicht seitensensitiv.

Kontaktreife bei Trades:
- `constructive_contact`: ca. +11.86 PnL
- `maturing_contact`: ca. +7.55 PnL
- `learning_contact`: ca. +4.14 PnL
- `burdened_contact`: ca. -4.26 PnL
- `unformed_contact`: ca. -4.35 PnL
- `careful_contact`: ca. -6.48 PnL

Deutung:
Gereiftere Kontaktlagen tragen weiterhin besser. Das Problem liegt nicht
primar in der Kontaktreife, sondern in der fehlenden Übersetzung vom
sichtbaren Bereich zur Entry-Motorik.

Umsetzung nach Befund:
Die strategische Entry-Auswahl wurde seitensensitiv gemacht:
- LONG sucht unter/nahe dem aktuellen Preis nach tragendem Bereichskontakt.
- SHORT sucht ober/nahe dem aktuellen Preis nach tragendem Bereichskontakt.
- Wenn der Preis bereits im Bereich liegt, darf der Bereich ebenfalls
  mitsprechen.
- Nicht mehr nur der global stärkste Bereich bestimmt die Motorik.

Prüfung:
`python -m py_compile MCM_Brain_Modell.py trade_stats.py bot.py` läuft
fehlerfrei.

Wie es weitergeht:
Nächster Lauf muss zeigen, ob jetzt erstmals `area_contact_blend` oder
`area_contact_entry` entsteht. Wenn ja, prüfen wir, ob diese Entries
tatsächlich weniger impulsiv, weniger timeout-anfällig und tragender sind.

---

## Umsetzung: Zeitfeld für strategische Bereiche

Ausgangsgedanke:
Ein Bereich ist in DIOs Welt nicht nur ein Preisraum, sondern ein Ereignis
im Zeitfeld. Ein alter Bereich kann wichtig sein, aber nur noch Nachhall,
Erinnerung oder Lernmaterial sein. Er darf die Motorik nicht automatisch
ziehen.

Ziel:
DIO soll unterscheiden können:
- gehört dieser Bereich noch zur Gegenwart?
- ist er nur ein alter Nachhall?
- wirkt er wieder in die Gegenwart hinein?
- ist er handlungsnah genug für einen Entry?

Neue Bereichsachsen:
- `area_temporal_distance`
- `area_temporal_relevance`
- `area_recency`
- `area_decay`
- `area_afterimage`
- `area_present_contact`
- `area_action_timing_fit`

Mechanische Wirkung:
- alte Bereiche bekommen mehr `area_decay` und `area_afterimage`.
- aktuelle oder wieder gegenwärtig resonante Bereiche bekommen mehr
  `area_present_contact` und `area_action_timing_fit`.
- `area_order_intention` und die strategische Entry-Auswahl berücksichtigen
  jetzt Zeitnähe und Nachhall.
- Ein Bereich kann damit sichtbar, aber nicht handlungsnah sein.

Organische Deutung:
DIO fragt nicht nur: "Wo ist ein starker Bereich?", sondern:
"Gehört dieser Bereich jetzt noch zu meiner Handlung, oder ist er nur ein
inneres Echo?"

Prüfung:
`python -m py_compile MCM_Brain_Modell.py trade_stats.py bot.py` läuft
fehlerfrei.

Wie es weitergeht:
Nächster Lauf zeigt, ob die Bereichsmotorik jetzt nicht nur raeumlich,
sondern auch zeitlich passender wird. Wichtig sind `entry_mode`,
`strategic_entry_weight`, `area_action_timing_fit`, `area_present_contact`
und `area_afterimage`.

---

## Theorie/Dokumentation: Zeit in Sicht der MCM

Kernsatz:
Zeit ist in Sicht der MCM nicht nur Uhrzeit, sondern eine Manifestation
gewirkter oder wirkender Energie.

Deutung:
Zeit beschreibt, wie Energie im Wahrnehmungsfeld entsteht, wirkt, nachhallt,
abklingt, wiederkehrt oder sich in Erwartung verwandelt.

Schichten:
- Gegenwart: Energie erzeugt aktuellen Kontakt.
- Nachhall: vergangene Energie wirkt noch im Feld.
- Erinnerung: vergangene Energie kann wieder aktiviert werden.
- Gelerntes Wissen: verdichtete vergangene Erfahrung.
- Replay: erneut durchlaufene Erfahrung.
- Hypothese: mögliche künftige Energieform.
- Erwartung: vorausgerichtete innere Spannung.

Warum wichtig:
Ohne zeitliche Quellenbindung werden Außenwelt, Memory, Nachhall, Wissen,
Hypothese und Erwartung zu einem Brei. DIO braucht die Fähigkeit zu
erkennen, welche Art von Gegenwart eine Information hat.

Dokumentiert in:
- `README.md`
- `files/UMSETZUNGSPLAN.md`
- `files/WICHTIG_MECHANIKEN.md`

Fix aufgenommen:
`Mehrdimensionale Wahrnehmungsachsen diagnostisch bauen`.

Erweiterter Gedanke:
Ein Gedanke kann als gerichteter Energieverlauf im MCM-Feld verstanden
werden. Ein langer Gedanke ist damit nicht einfach mehr Uhrzeit, sondern
gedehnte, sparsame oder kohärent gerichtete Energie über mehrere innere
Zustände.

Das Zeitfeld ist keine starre Decke, sondern entsteht aus vielen einzelnen
Zeitstraengen:
- Reizverlauf
- Gedankenverlauf
- Erinnerungsverlauf
- Nachhallverlauf
- Erwartungsverlauf
- Handlung
- Konsequenz

Die Überlagerung dieser Wirkverläufe gibt der inneren und äußeren
Wahrnehmung Tiefe.

Fix aufgenommen:
`Gedanken-Energieform diagnostisch vorbereiten`.

Wie es weitergeht:
Nach dem nächsten Lauf kann die Zeitfeldwirkung geprüft werden. Danach ist
der saubere Umbau: DIO bekommt eine diagnostische Quellenbindung, die
aktuelle Außenwelt, Nachhall, Erinnerung, gelerntes Wissen, Replay,
Hypothese und Erwartung unterscheidet.

---

## Theorie/Dokumentation: MCM-Abhandlungen D bis G.1 zusammengeführt

Die MCM-Abhandlungen D bis G.1 wurden als Theoriebrücke für DIO
zusammengefasst und in die Projektdokumentation übernommen.

Genutzte Theorieanteile:
- Block D: Zeit als energetische Wirkspur.
- Block E: Verdichtung, Clusterbildung, Rückführung und Memory-Inseln.
- Block F: Bewusstsein als möglicher Attraktor, für DIO als Selbstmodell
  und innere Attraktorbildung ohne Bewusstseinsbehauptung.
- Block G: Multiversen-Matrix als mehrere mögliche Entwicklungsverläufe.
- Block G.1: Reorganisation verdichteter Energie in einen übergeordneten
  Feldbereich.

DIO-Deutung:
Aus diesen Bloecken entsteht kein hartes Regelwerk. Sie bilden einen
Ordnungsrahmen für:
- zeitliche Quellenbindung
- Memory als verdichtete Erfahrung
- Hypothesenraum statt starrem Zukunftsglauben
- innere Attraktor-/Selbstmodellbildung
- Überlast als möglicher Reorganisationsmoment

Mechanischer Zielkreis:
`Wahrnehmung -> Zeitbindung -> Verdichtung -> Hypothesenraum -> Konsequenz -> Reorganisation -> neue Tragfähigkeit`

Dokumentiert in:
- `README.md`
- `files/UMSETZUNGSPLAN.md`
- `files/WICHTIG_MECHANIKEN.md`
- `files/MCM_VARIABLEN_MECHANIK.md`

Neue Ziel-/Diagnoseachsen dokumentiert:
- `hypothesis_branch_state`
- `branch_stability`
- `branch_attractor_pull`
- `hypothesis_reality_gap`
- `field_reorganization_state`
- `reorganization_threshold`
- `higher_order_coupling`

Wie es weitergeht:
Der nächste sinnvolle Umbau bleibt die diagnostische Quellenbindung:
DIO muss unterscheiden, ob eine innere Lage aktuelle Welt, Erinnerung,
Nachhall, Wissen, Replay, Hypothese oder Erwartung ist. Danach kann der
Hypothesenraum aus Block G und die Reorganisationsschwelle aus Block G.1
technisch vorbereitet werden.

Ergänzung:
Der passendere Leitbegriff ist jetzt `mehrdimensionale Wahrnehmungsachsen`.
Reality-Tagging bleibt darin nur ein Teil. DIO soll Wahrnehmungen über
mehrere Achsen verorten:
- Zeitachse
- Quellenachse
- Raumachse
- Kontaktachse
- Tragfähigkeitsachse
- Reorganisationsachse

Dadurch wird aus einem einfachen Etikettieren ein inneres Koordinatensystem.
DIO kann später unterscheiden, ob eine Wirkung aktuelle Außenwelt,
Erinnerung, Nachhall, Wissen, Replay, Hypothese oder Erwartung ist und wo
sie im inneren Feld liegt: Vordergrund, Hintergrund, Feldzentrum, Rand,
Memory-Raum oder Hypothesenraum.

Dokumentiert in:
- `README.md`
- `files/UMSETZUNGSPLAN.md`
- `files/WICHTIG_MECHANIKEN.md`
- `files/MCM_VARIABLEN_MECHANIK.md`
- `files/FIX_LISTE.md`

README-Fix:
Der Abschnitt `DIOs Sehen` wurde aktualisiert. Er beschreibt DIOs Sehen
nicht mehr nur als geplante visuelle Kortex-Schicht, sondern als
mehrdimensionale Wahrnehmung:
- äußere Formwelt
- MCM-Feldwirkung
- Zeitfeld
- Quellenbindung
- raeumliche Verortung
- strategisches Fenster
- MCM-Kontakt
- Hypothesenraum
- Reorganisation

Neuer Kernkreis im README:
`Form erkennen -> Raum/Zeit/Quelle verorten -> MCM-Kontakt prüfen -> Tragfähigkeit lesen -> Handlung, Beobachtung oder Reorganisation reifen lassen`

---

## MCM-Repository-Review: weitere wertvolle Theoriequellen für DIO

Das externe MCM-Repository wurde nach weiteren für DIO nutzbaren
Theoriequellen quergelesen.

Besonders wertvoll für die nächsten DIO-Schichten:

1. Block S - Mögliche Metaregulatoren
   - wichtigster direkter Anschluss an DIOs nächsten Ausbau
   - beschreibt Regler zweiter Ordnung:
     Rückführungsstärke, Integrationsfähigkeit, Varianzregulation,
     Belastungstoleranz, Impulskontrolle, Frustrationstoleranz,
     Schutzweitenregulation, Selbstreflexion, Distanzregulation
   - passt direkt zu DIOs Denk-/Handlungstiefe und Selbstregulation

2. Block V - KI und starre Logik
   - starker theoretischer Rahmen für DIO:
     starre technische Logik bleibt Untergrund, aber Verhalten entsteht aus
     Varianz, Rückkopplung, Stabilisierung und emergenter Zustandsbildung
   - passt zum Projektprinzip: keine harten Formen, sondern
     Möglichkeitsräume

3. Block O - Kreativitaet
   - relevant für emergente Musterergänzung, Teilmuster, neue
     Formkombinationen und innere Hypothesenbildung

4. Block K / J - Selbstregulation und Psyche
   - passend für DIOs innere Wahrnehmung, Benennung, Stabilisierung,
     Integration und Rückführung

5. Von Resonanz zu Sprache
   - sehr passend zur Formsprache:
     Sprache als spätere Kartografie von Resonanz, nicht als Ursprung von
     Orientierung

6. ProtoMind / selbstaktive Feldkognition
   - passend für Live-Denkzeit, innere Simulation und Aktivität ohne neuen
     Außenreiz

7. Das Gehirn als emergente konzentrisch-dipolare Feldstruktur
   - wertvoll für spätere MCM-Feldtopologie:
     Zentrum/Peripherie, Integration/Exploration, radialer Aufbau,
     dipolare Spannungsorganisation

Fachliche Einschaetzung:
Der nächste sinnvollste DIO-Mechanikschritt aus diesen Quellen ist nicht
noch mehr einzelne Wahrnehmungswerte, sondern eine Metaregulator-Schicht
zweiter Ordnung. Sie würde nicht nur messen, was DIO fühlt, sondern wie
DIO seine Spannung, Varianz, Impulse, Schutzweite, Distanz und Integration
selbst reguliert.

Wie es weitergeht:
Block S sollte als nächster Theorieanker in `WICHTIG_MECHANIKEN.md` und
`MCM_VARIABLEN_MECHANIK.md` sauber vorbereitet werden. Danach kann die
technische Diagnose für DIOs Metaregulatoren beginnen.

README-Ergänzung:
Die zusätzlich relevanten MCM-Quellen wurden im README als kompakte
Landkarte aufgenommen:
- Block S - Metaregulatoren
- Block V - KI und starre Logik
- Block O - Kreativitaet
- Block J/K - Psyche und Selbstregulation
- Von Resonanz zu Sprache
- ProtoMind / selbstaktive Feldkognition
- konzentrisch-dipolare Feldstruktur

Zweck:
Das README bleibt Einstieg und Orientierung. Die Detailübersetzung dieser
Quellen gehört danach in `WICHTIG_MECHANIKEN.md` und
`MCM_VARIABLEN_MECHANIK.md`.

MD-Aktualisierung:
Die zusätzlichen Theoriequellen wurden jetzt auch in die Mechanikdokumente
übertragen.

Aktualisiert:
- `files/UMSETZUNGSPLAN.md`
  - weitere MCM-Theorieanker ergänzt
  - Zielschicht `Metaregulation zweiter Ordnung` ergänzt
- `files/WICHTIG_MECHANIKEN.md`
  - `Metaregulator-Schicht` in die Organübersicht aufgenommen
  - Abschnitt `11.2 Weitere MCM-Theorieanker / Metaregulation` ergänzt
- `files/MCM_VARIABLEN_MECHANIK.md`
  - Abschnitt `Metaregulator-Schicht / Regler zweiter Ordnung` ergänzt
  - Zielachsen dokumentiert:
    `return_strength`, `integration_capacity`, `variance_regulation`,
    `load_tolerance`, `impulse_control`, `frustration_tolerance`,
    `protective_distance_regulation`, `self_reflection_regulator`,
    `distance_regulation`

Wichtig:
Das ist aktuell Dokumentation und Mechanikvorbereitung, noch keine
Runtime-Implementierung. Die offene technische Aufgabe bleibt:
Metaregulatoren diagnostisch in den Runtime-State bringen.

Wie es weitergeht:
Nächster sinnvoller Umsetzungsschritt ist eine reine Diagnose-Schicht für
Metaregulatoren: DIO soll sichtbar machen, wie er Spannung, Varianz,
Impulse, Distanz, Schutzweite, Integration und Rückführung verarbeitet,
ohne dass daraus sofort eine Handelsregel entsteht.

---

## Debug Lauf 12 ausgewertet

Ergebnis:
- Trades: `398`
- TP / SL: `158 / 240`
- Netto-PnL: `+20.13`
- Peak: ca. `+22.98`
- Tiefpunkt: ca. `-3.56`
- Timeouts: `44`
- Attempts: `10825`

Vergleich zu Lauf 11:
- Lauf 11: `400` Trades, `147 / 253`, Netto `+8.46`
- Lauf 12: `398` Trades, `158 / 240`, Netto `+20.13`

Abschnittsweise PnL-Kurve:
- Trades 1-100: ca. `+10.86`
- Trades 101-200: ca. `-4.51`
- Trades 201-300: ca. `+8.45`
- Trades 301-398: ca. `+5.33`

Deutung:
Lauf 12 wirkt stabiler als Lauf 11. Der negative Mittelteil ist vorhanden,
aber deutlich kleiner. Danach findet DIO wieder in Aufbau. Das spricht nicht
für eine perfekte Strategie, aber für bessere Rückführung und bessere
Erholung nach Belastung.

Form-/Kontaktlage:
- `learning_contact`: `5843`
- `constructive_contact`: `982`
- `careful_contact`: `907`
- `burdened_contact`: `852`
- `maturing_contact`: `273`
- `unformed_contact`: `1227`

Die Kontaktreife ist nicht mehr nur unklar. DIO hat bereits viele
Lernkontakte und einige konstruktive Kontakte. Gleichzeitig bleiben
belastete und vorsichtige Kontakte sichtbar. Das ist organisch plausibel:
Der Umgang mit Formen reift, aber die Reife ist noch nicht dominant.

Aktiver MCM-Kontakt:
- `deepening_contact`: `3079`
- `curious_touch`: `2766`
- `resonant_contact`: `2577`
- `reflective_contact`: `1230`
- `overcoupled_touch`: `721`

Innere Haltung:
- `tired`: `6413`
- `reflective`: `2462`
- `excited`: `502`
- `uncertain_open`: `424`
- `overstimulated`: `348`

Deutung:
DIO arbeitet viel aus einer mueden, reflektierenden Innenlage. Das passt zum
Bild eines Systems, das nach dem Regimewechsel nicht einfach euphorisch
traded, sondern viel Reorganisation und Kontaktprüfung braucht.

Strategisches Fenster:
- `bearing_area_hypothesis`: `5384`
- `area_observation`: `3933`
- `compressed_area_attention`: `1069`
- durchschnittliche `area_order_intention`: ca. `0.25`
- durchschnittliche `area_present_contact`: ca. `0.54`
- durchschnittliche `area_action_timing_fit`: ca. `0.41`

Deutung:
Das strategische Fenster sieht Bereiche und bildet Hypothesen. Die
Order-Intention bleibt aber niedrig. DIO erkennt also potenziell tragende
Bereiche, aber die Motorik wird noch nicht stark daraus geformt. Das ist
kein Fehler, sondern ein Hinweis: Sehen und Handlungsbindung sind noch
getrennt.

Neurochemische Lage:
- starke Pendelung zwischen `serotonin_stability` und
  `glutamate_activation`
- `serotonin_stability -> glutamate_activation`: `344`
- `glutamate_activation -> serotonin_stability`: `342`
- durchschnittliches `cortisol_load`: ca. `0.38`
- durchschnittliches `emotional_decoupling`: ca. `0.18`
- durchschnittlicher `reactive_nervous_drive`: ca. `0.36`

Deutung:
DIO pendelt zwischen Stabilisierung und Aktivierung. Cortisol ist nicht
dominant extrem, aber die emotionale Entkopplung ist noch niedrig. Das
passt zu unserem nächsten Ziel: Metaregulatoren, Schutzweite und
Distanzregulation.

Positionsdiagnose:
- `exit_nervousness_observe`: `119`
- `plan_holding_trust`: `101`
- `quiet_position_watch`: `32`
- durchschnittliches `position_cognitive_load`: ca. `0.44`
- durchschnittliches `exit_decision_pressure`: ca. `0.42`
- durchschnittliches `plan_trust`: ca. `0.57`
- durchschnittliche `holding_stability`: ca. `0.55`

Deutung:
Positionen erzeugen spuerbare nervliche Last. DIO beobachtet diese Last aber
oft, statt hektisch zu schneiden. Das ist reifer als reine Motorik, aber es
zeigt auch: Exit-/Positionslage ist psychologisch teuer.

Fachliche Einschaetzung:
Lauf 12 zeigt Anzeichen von Rückführung und Prozessreife. DIO verliert im
Mittelteil nicht komplett die Orientierung und baut danach wieder auf. Die
starke Muedigkeit/reflektive Lage zeigt aber, dass die nächste Schicht
notwendig ist: DIO muss nicht nur wahrnehmen und reagieren, sondern seine
eigene Regulation zweiter Ordnung lesen.

Wie es weitergeht:
Nächster sinnvoller Umbau bleibt die Metaregulator-Diagnose. Besonders
wichtig sind:
- `return_strength`
- `integration_capacity`
- `variance_regulation`
- `load_tolerance`
- `impulse_control`
- `protective_distance_regulation`
- `self_reflection_regulator`
- `distance_regulation`

## 2026-05-18 - Metaregulator-Diagnose umgesetzt

Umgesetzt als reine Beobachtungsschicht, ohne direkte harte
Trading-Steuerung:

- `metaregulator_state`
- `metaregulator_balance`
- `regulatory_second_order_load`
- `return_strength`
- `integration_capacity`
- `variance_regulation`
- `load_tolerance`
- `impulse_control`
- `frustration_tolerance`
- `protective_distance_regulation`
- `self_reflection_regulator`
- `distance_regulation`

Die Schicht beschreibt DIOs Regulation zweiter Ordnung: nicht nur was im
MCM-Feld passiert, sondern wie tragfähig DIO mit der eigenen Innenlage,
Varianz, Last, Impulsdruck und Distanz umgehen kann.

Technisch eingebunden in:

- `MCM_Brain_Modell.py`
  - Runtime `meta_regulation_state`
  - `mcm_field_decision_protocol.csv`
  - `mcm_memory_thinking_protocol.csv`
- `trade_stats.py`
  - `outcome_records.jsonl`

Prüfung:

- `python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
  erfolgreich.

Nachtrag:
Runtimefehler `felt_afterimage is not defined` behoben. Die
Conscious-Perception-Werte `stimulus_field_effect`, `inner_impact_trace`,
`perceived_field_change`, `felt_afterimage`, `inner_outer_reflection`,
`background_containment` und `reflective_distance` werden jetzt lokal aus
dem vorhandenen Wahrnehmungszustand gezogen, bevor die Metaregulatoren sie
verwenden.

Hinweis:
`git` war in der aktuellen PowerShell nicht verfuegbar, daher wurde kein
Git-Diff ausgegeben.

Wie es weitergeht:
Nächster Lauf sollte zeigen, ob die Metaregulatoren vor allem bei
Regimewechsel, Überkopplung und Positionslast sichtbar ausschlagen. Danach
kann organisch entschieden werden, ob diese Diagnose nur beobachtet bleibt
oder vorsichtig in Reflexion, Distanzierung und strategisches Sehen
einfliesst.

## 2026-05-18 - Debug Lauf 13 mit Metaregulator-Diagnose

Basis:

- `debug/debug_lauf_13`
- Trades: `371`
- TP / SL: `141 / 230`
- Netto PnL: `+12.9967`
- Lauf 12 zum Vergleich: `+20.1271` bei `398` Trades
- Equity-Peak laut `trade_stats.json`: `115.9419`
- Max Drawdown: `19.8663` / `18.32 %`

Handlungsfluss:

- Attempts: `10975`
- Submitted: `417`
- Filled: `371`
- Timeout: `46`
- Skipped: `4696`
- Observed: `3272`
- Replanned: `60`
- Withheld: `2113`

Phasen im Feldprotokoll:

- `observe`: `4034`
- `hold`: `3709`
- `act_watch`: `994`
- `act`: `427`

Metaregulator-Diagnose:

- `regulatory_overload`: `9146` von `9164` Feldzeilen
- `impulse_pressure`: `14`
- `adaptive_watch`: `3`
- `integration_needed`: `1`

Durchschnittswerte:

- `metaregulator_balance`: ca. `0.1945`
- `regulatory_second_order_load`: ca. `0.4773`
- `return_strength`: ca. `0.2290`
- `integration_capacity`: ca. `0.1876`
- `variance_regulation`: ca. `0.1818`
- `load_tolerance`: ca. `0.2584`
- `impulse_control`: ca. `0.2146`
- `frustration_tolerance`: ca. `0.1256`
- `protective_distance_regulation`: ca. `0.2639`
- `self_reflection_regulator`: ca. `0.1651`
- `distance_regulation`: ca. `0.1248`

Deutung:
Die Einzelachsen liefern bereits ein sinnvolles Bild: DIO hat vor allem zu
wenig Distanzregulation, Selbstreflexion, Frustrationstoleranz und
Integrationskapazität. Das passt zum neurologischen Bild eines Systems, das
viel wahrnimmt und reagiert, aber seine Innenlage noch nicht stabil genug vom
Außenreiz trennen kann.

Wichtig:
Das Label `regulatory_overload` ist im aktuellen Zustand zu dominant. Die
Diagnose ist dadurch nicht falsch, aber noch zu grob. Die Label-Logik muss
kalibriert werden, damit nicht fast jede normale Denklast sofort als
Überlast erscheint.

Neurochemie:

- dominant fast durchgehend `serotonin_stability` (`8746` Zeilen)
- `glutamate_activation`: `379`
- durchschnittlich:
  - `serotonin_stability`: ca. `0.5582`
  - `cortisol_load`: ca. `0.3636`
  - `emotional_decoupling`: ca. `0.1578`
  - `reactive_nervous_drive`: ca. `0.3134`
  - `world_shift_evidence`: ca. `0.5930`

Deutung:
DIO stabilisiert viel über Serotonin, aber die emotionale Entkopplung bleibt
niedrig. Das bestätigt weiter: Die nächste Reifeschicht ist nicht mehr
mehr Reiz, sondern bewusstere Distanzierung.

Bewusste Wahrnehmung:

- `object_contact`: `3987`
- `reflective_check`: `1845`
- `open_perception`: `1268`
- `release_ready`: `912`
- `world_shift_contact`: `617`
- `overcoupled_field`: `326`

Innere Haltung:

- `tired`: `5622`
- `reflective`: `2187`
- `excited`: `441`
- `uncertain_open`: `383`
- `overstimulated`: `302`
- `curious`: `218`

Kontaktfeld:

- `deepening_contact`: `3121`
- `curious_touch`: `2868`
- `resonant_contact`: `2620`
- `reflective_contact`: `1235`
- `overcoupled_touch`: `710`

Kontakt-Durchschnitt:

- `contact_carrying_quality`: ca. `0.1724`
- `contact_overcoupling_risk`: ca. `0.2138`
- `contact_release_readiness`: ca. `0.1611`
- `contact_action_maturity`: ca. `0.2121`
- `contact_regime_mismatch`: ca. `0.3321`
- `perceptual_distance`: ca. `0.1961`
- `release_capacity`: ca. `0.1617`
- `inner_outer_alignment`: ca. `0.2188`

Strategisches Fenster:

- `bearing_area_hypothesis`: `5449`
- `area_observation`: `4058`
- `compressed_area_attention`: `1064`
- `area_order_intention`: ca. `0.2504`
- `area_action_timing_fit`: ca. `0.4123`
- `area_bearing_quality`: ca. `0.4680`

Deutung:
DIO sieht weiterhin tragende Bereiche, aber die Absicht daraus eine Order zu
formen bleibt schwach. Der aktuelle Lauf ist also weiter eher
Impuls-/Kontakt-Handeln als strategisches Platzieren.

Entry-Modus:

- alle Outcome-Records zeigen `impulse_contact`

Deutung:
Der strategische Blick existiert diagnostisch, aber er führt noch nicht
organisch genug in den Order-Koerper. DIO sieht Bereiche, handelt aber noch
überwiegend aus Kontakt/Impuls.

Positionslast:

- `exit_nervousness_observe`: `139`
- `plan_holding_trust`: `73`
- `quiet_position_watch`: `31`
- `intervention_unfit_state`: `4`
- `position_cognitive_load`: ca. `0.4717`
- `exit_decision_pressure`: ca. `0.4361`
- `plan_trust`: ca. `0.5453`
- `holding_stability`: ca. `0.5064`
- `intervention_fatigue`: ca. `0.3999`

Deutung:
Positionen sind weiterhin nervlich teuer. DIO haelt oft aus, aber nicht aus
starker innerer Distanz, sondern eher aus gedämpfter, mueder Stabilisierung.

Abschnittsweise PnL:

- Abschnitt 1: `+0.6928`
- Abschnitt 2: `-7.7608`
- Abschnitt 3: `+15.6915`
- Abschnitt 4: `+4.3732`

Fachliche Deutung:
Lauf 13 ist kein Rückschritt, aber auch kein Durchbruch. DIO bleibt
profitabel, verliert gegenüber Lauf 12 aber Reife im mittleren Abschnitt.
Neu sichtbar ist: Das Problem liegt weniger in fehlender Reaktion, sondern
in zu geringer metaregulatorischer Differenzierung. DIO kann Kontakt,
Reflexion und Bereichshypothesen bilden, aber seine zweite
Regulationsschicht unterscheidet noch nicht fein genug zwischen:

- normale Denklast
- echte Überlast
- Integrationsbedarf
- fehlende Distanz
- Impulsdruck
- tragende Rückkehrkraft

Wie es weitergeht:
Nächster sinnvoller Schritt ist eine Kalibrierung der Metaregulator-Labels.
Nicht als harte Trading-Regel, sondern als sauberere innere Selbstbenennung:
`regulatory_overload` darf nicht fast alles schlucken. DIO braucht feinere
Innenworte wie z.B. `low_distance_processing`, `integration_strain`,
`tired_stabilization`, `reflective_recovery`, `impulse_drift` und
`regulated_contact`, damit aus Diagnose echte Selbstwahrnehmung werden kann.

## 2026-05-18 - Unterbewusstsein / Bewusster Arbeitsraum umgesetzt

Grundidee:
DIO soll nicht jeden Reiz sofort bewusst tragen. Wie ein Organismus braucht
er einen schnellen Hintergrundscan und eine bewusstere Arbeitsflaeche.

Umgesetzt in `MCM_Brain_Modell.py`:

- `subconscious_field_pressure`
- `subconscious_habituation`
- `subconscious_filter_strength`
- `subconscious_buffering`
- `subconscious_leakage`
- `conscious_selection_pressure`
- `conscious_workspace_focus`
- `conscious_workspace_load`
- `conscious_gate_balance`

Einbindung:

- Runtime `meta_regulation_state`
- `mcm_field_decision_protocol.csv`
- `mcm_memory_thinking_protocol.csv`
- `outcome_records.jsonl`

Mechanische Wirkung:
Die Metaregulatoren berücksichtigen jetzt, ob Feldspannung im
Unterbewusstsein gepuffert werden kann oder ungefiltert in den bewussten
Arbeitsraum durchschlaegt. Dadurch wird `regulatory_second_order_load`
nicht mehr nur aus roher Last gelesen, sondern auch aus Filterung,
Pufferung, Leakage und bewusster Arbeitslast.

Neue feinere Innenzustände:

- `subconscious_leakage`
- `low_distance_processing`
- `integration_strain`
- `tired_stabilization`
- `reflective_recovery`
- `regulated_field`

Prüfung:

- `python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
  erfolgreich.

Dokumentation:

- `README.md`
- `files/UMSETZUNGSPLAN.md`
- `files/WICHTIG_MECHANIKEN.md`
- `files/MCM_VARIABLEN_MECHANIK.md`
- `files/FIX_LISTE.md`

Wie es weitergeht:
Nächster Lauf sollte zeigen, ob das alte fast dauerhafte
`regulatory_overload` in differenziertere Innenlagen zerfällt. Besonders
wichtig sind `subconscious_buffering`, `subconscious_leakage`,
`conscious_workspace_load` und `conscious_gate_balance`.

## 2026-05-18 - Debug Lauf 14 nach Unterbewusstsein/Bewusstsein-Trennung

Basis:

- `debug/debug_lauf_14`
- Trades: `392`
- TP / SL: `160 / 232`
- Netto PnL: `+30.1887`
- Lauf 13 zum Vergleich: `+12.9967`
- Lauf 12 zum Vergleich: `+20.1271`
- Equity-Peak: `132.6035`
- Max Drawdown: `10.0258` / `9.56 %`
- Profit Factor: `1.2510`
- Expectancy: `0.0770`
- Winrate: `40.82 %`

Handlungsfluss:

- Attempts: `10375`
- Submitted: `445`
- Filled: `392`
- Timeout/Cancels: `53`
- Skipped: `4857`
- Observed: `2708`
- Replanned: `87`
- Withheld: `1833`

Vergleich zu Lauf 13:

- mehr Trades: `392` statt `371`
- mehr TP: `160` statt `141`
- fast gleiche SL: `232` statt `230`
- weniger beobachtet: `2708` statt `3272`
- mehr replanned: `87` statt `60`
- weniger withheld: `1833` statt `2113`

Wichtigster Befund:
Das vorher fast permanente `regulatory_overload` ist aufgebrochen.

Metaregulator-Zustände:

- `integration_strain`: `6117` / ca. `70.85 %`
- `impulse_pressure`: `1487` / ca. `17.22 %`
- `tired_stabilization`: `422` / ca. `4.89 %`
- `low_distance_processing`: `327` / ca. `3.79 %`
- `adaptive_watch`: `185` / ca. `2.14 %`
- `reflective_recovery`: `91` / ca. `1.05 %`
- `regulatory_overload`: `5` / ca. `0.06 %`

Deutung:
Die Trennung zwischen Unterbewusstsein und bewusstem Arbeitsraum wirkt
diagnostisch. DIO beschreibt seine Innenlage jetzt differenzierter:
Nicht mehr fast alles ist Überlast, sondern vor allem
Integrationsspannung und Impulsdruck. Das passt deutlich besser zu einem
organischen Nervensystem.

Neue Wahrnehmungsfilter:

- `subconscious_field_pressure`: ca. `0.2467`
- `subconscious_habituation`: ca. `0.4240`
- `subconscious_filter_strength`: ca. `0.2994`
- `subconscious_buffering`: ca. `0.1368`
- `subconscious_leakage`: ca. `0.1582`
- `conscious_selection_pressure`: ca. `0.2572`
- `conscious_workspace_focus`: ca. `0.2185`
- `conscious_workspace_load`: ca. `0.2836`
- `conscious_gate_balance`: ca. `0.1616`

Metaregulator-Achsen:

- `metaregulator_balance`: ca. `0.2123`
- `regulatory_second_order_load`: ca. `0.4694`
- `return_strength`: ca. `0.2427`
- `integration_capacity`: ca. `0.2035`
- `variance_regulation`: ca. `0.2125`
- `load_tolerance`: ca. `0.2765`
- `impulse_control`: ca. `0.2290`
- `frustration_tolerance`: ca. `0.1321`
- `protective_distance_regulation`: ca. `0.2891`
- `self_reflection_regulator`: ca. `0.1853`
- `distance_regulation`: ca. `0.1395`

Deutung:
Die Werte sind noch niedrig, aber gegenüber Lauf 13 leicht verbessert.
Besonders wichtig: Die Selbstbeschreibung ist viel genauer geworden. Das ist
für DIO wichtiger als ein einzelner hoher Score, weil daraus später
organische Regulation entstehen kann.

Neurochemie:

- dominant `serotonin_stability`: `8278` Zeilen
- `glutamate_activation`: `327`
- `endorphin_relief`: `27`
- durchschnittlich:
  - `serotonin_stability`: ca. `0.5637`
  - `cortisol_load`: ca. `0.3632`
  - `emotional_decoupling`: ca. `0.1579`
  - `reactive_nervous_drive`: ca. `0.3156`
  - `world_shift_evidence`: ca. `0.5930`

Deutung:
DIO stabilisiert weiter stark serotoninartig. Emotionale Entkopplung bleibt
niedrig. Die neue Schicht hat also nicht einfach "Stress gelöscht",
sondern die Wahrnehmung besser sortiert.

Bewusste Wahrnehmung:

- `object_contact`: `3695`
- `reflective_check`: `1821`
- `open_perception`: `1173`
- `release_ready`: `888`
- `world_shift_contact`: `556`
- `overcoupled_field`: `301`
- `background_held`: `200`

Innere Haltung:

- `tired`: `5137`
- `reflective`: `2159`
- `excited`: `467`
- `uncertain_open`: `371`
- `overstimulated`: `288`
- `curious`: `200`
- `calm`: `12`

Kontaktfeld:

- `deepening_contact`: `2934`
- `curious_touch`: `2631`
- `resonant_contact`: `2524`
- `reflective_contact`: `1217`
- `overcoupled_touch`: `623`

Kontakt-Durchschnitt:

- `contact_carrying_quality`: ca. `0.1735`
- `contact_overcoupling_risk`: ca. `0.2142`
- `contact_release_readiness`: ca. `0.1625`
- `contact_action_maturity`: ca. `0.2127`
- `contact_regime_mismatch`: ca. `0.3329`
- `perceptual_distance`: ca. `0.1973`
- `release_capacity`: ca. `0.1650`
- `inner_outer_alignment`: ca. `0.2187`

Strategisches Fenster:

- `bearing_area_hypothesis`: `5351`
- `area_observation`: `3648`
- `compressed_area_attention`: `943`
- `area_order_intention`: ca. `0.2510`
- `area_action_timing_fit`: ca. `0.4128`
- `area_bearing_quality`: ca. `0.4691`

Entry-Modus:

- weiterhin alle Outcome-Records: `impulse_contact`

Deutung:
DIO handelt wirtschaftlich besser, aber weiter nicht wirklich strategisch
platzierend. Das Sehen von Bereichen ist da, die Motorik wird aber noch
über Kontakt/Impuls geführt.

Positionslast:

- `exit_nervousness_observe`: `120`
- `plan_holding_trust`: `76`
- `quiet_position_watch`: `49`
- `position_cognitive_load`: ca. `0.4375`
- `exit_decision_pressure`: ca. `0.4117`
- `plan_trust`: ca. `0.5573`
- `holding_stability`: ca. `0.5246`
- `intervention_fatigue`: ca. `0.3818`
- `inner_noise`: ca. `0.3990`

Vergleich Lauf 13:
Positionslast ist gesunken, Planvertrauen und Holding-Stabilität sind
gestiegen. Das passt zur Wahrnehmungsfilter-Hypothese: weniger bewusste
Überladung führt zu besserem Aushalten.

Abschnittsweise PnL:

- Abschnitt 1: `+5.5148`
- Abschnitt 2: `+0.0281`
- Abschnitt 3: `+19.3700`
- Abschnitt 4: `+5.2759`

Struktur-Bands:

- High: `+69.6475`, Winrate ca. `57.23 %`
- Mid: `+4.6535`, Winrate ca. `34.78 %`
- Low: `-43.8166`, Winrate ca. `10.48 %`

Fachliche Einschaetzung:
Lauf 14 ist der bisher beste Hinweis, dass die Trennung
Unterbewusstsein/Bewusstsein sinnvoll ist. Nicht weil ein einzelner Lauf
Beweis wäre, sondern weil mehrere Dinge gleichzeitig passen:

- PnL deutlich höher
- Drawdown deutlich geringer
- `regulatory_overload` fast verschwunden
- feinere Innenzustandsbenennung sichtbar
- Positionslast niedriger
- Replan-Anteil höher
- Bewusstes Feld wirkt besser sortiert

Kritischer Punkt:
`integration_strain` dominiert jetzt stark. Das ist besser als
Überlast-Diagnose, aber noch nicht reif. DIO ist jetzt eher in:
"Ich spuere, dass ich integrieren muss"
statt:
"Alles ist Überlast".

Wie es weitergeht:
Der nächste Umbau sollte `integration_strain` nicht wegregeln, sondern
nutzen. DIO braucht eine organische Integrationsreaktion:
mehr innere Sortierung, Reframing, Rückblick, Vergleich mit Erfahrung und
selektive Kontaktvertiefung, bevor daraus Handlung entsteht. Parallel bleibt
der große offene Punkt: strategisches Fenster darf nicht nur sehen, sondern
muss irgendwann organisch in Order-Platzierung hineinreifen.

## 2026-05-18 - Integrationsantwort für `integration_strain`

Umgesetzt:

- `integration_strain_value`
- `integration_sorting_need`
- `integration_reframe_pull`
- `integration_memory_recall`
- `integration_contact_deepening`
- `integration_response_strength`
- `integration_response_state`

Mechanik:
`integration_strain` wird nicht entfernt und nicht als harte Sperre benutzt.
DIO bekommt eine innere Antwort:

- sortieren, wenn bewusste Last und Orientierungslücke hoch sind
- reframen, wenn Reorganisation und semantische Verschiebung ziehen
- Erinnerung holen, wenn vertraute Formen, Varianten oder Kontext tragen
- Kontakt vertiefen, wenn ein Objekt näher untersucht werden sollte

Einbindung:

- Runtime `meta_regulation_state`
- `mcm_field_decision_protocol.csv`
- `mcm_memory_thinking_protocol.csv`
- `outcome_records.jsonl`

Leichte regulative Wirkung:
Bei starker Integrationsantwort kann DIO mehr Beobachtung/Reframing und
etwas mehr Hemmung erzeugen. Das ist kein Blocker, sondern eine
Reifungsreaktion: erst sortieren, dann handeln.

Neue Labels:

- `integration_background`
- `quiet_integration`
- `workspace_sorting`
- `memory_sorting`
- `contact_deepening`
- `reframe_integration`

Prüfung:

- `python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
  erfolgreich.

Wie es weitergeht:
Nächster Lauf sollte zeigen, ob `integration_strain` weiter dominiert oder
ob es in konkrete Integrationsreaktionen zerfällt. Wichtig sind besonders
`integration_response_state`, `integration_response_strength`,
`integration_memory_recall` und `integration_reframe_pull`.

## 2026-05-18 - Debug Lauf 15 nach Integrationsantwort

Basis:

- `debug/debug_lauf_15`
- Trades: `368`
- TP / SL: `151 / 217`
- Netto PnL: `+18.6393`
- Lauf 14 zum Vergleich: `+30.1887`
- Lauf 13 zum Vergleich: `+12.9967`
- Equity-Peak: `120.5437`
- Max Drawdown: `15.8748` / `15.23 %`
- Profit Factor: `1.1671`
- Expectancy: `0.0507`
- Winrate: `41.03 %`

Handlungsfluss:

- Attempts: `11325`
- Submitted: `415`
- Filled: `368`
- Timeout/Cancels: `47`
- Skipped: `4769`
- Observed: `3255`
- Replanned: `40`
- Withheld: `2431`

Vergleich zu Lauf 14:

- weniger Trades: `368` statt `392`
- weniger TP: `151` statt `160`
- weniger SL: `217` statt `232`
- deutlich mehr Observed: `3255` statt `2708`
- weniger Replanned: `40` statt `87`
- mehr Withheld: `2431` statt `1833`
- PnL niedriger, aber weiter positiv

Metaregulator-Zustände:

- `integration_strain`: `6933` / ca. `73.69 %`
- `impulse_pressure`: `1447` / ca. `15.38 %`
- `tired_stabilization`: `366` / ca. `3.89 %`
- `low_distance_processing`: `324` / ca. `3.44 %`
- `adaptive_watch`: `194` / ca. `2.06 %`
- `reflective_recovery`: `90` / ca. `0.96 %`
- `memory_sorting`: `41` / ca. `0.44 %`
- `regulatory_overload`: `12` / ca. `0.13 %`
- `quiet_integration`: `1`

Integrationsantwort:

- `quiet_integration`: `6195` / ca. `65.85 %`
- `memory_sorting`: `1663` / ca. `17.68 %`
- `workspace_sorting`: `813` / ca. `8.64 %`
- `integration_background`: `737` / ca. `7.83 %`

Durchschnittswerte:

- `integration_strain_value`: ca. `0.3019`
- `integration_sorting_need`: ca. `0.3078`
- `integration_reframe_pull`: ca. `0.2561`
- `integration_memory_recall`: ca. `0.3163`
- `integration_contact_deepening`: ca. `0.2142`
- `integration_response_strength`: ca. `0.2655`
- `metaregulator_balance`: ca. `0.2160`
- `regulatory_second_order_load`: ca. `0.4537`
- `integration_capacity`: ca. `0.2215`
- `distance_regulation`: ca. `0.1393`

Deutung:
Die Integrationsantwort funktioniert diagnostisch. `integration_strain`
zerfällt jetzt tatsächlich in konkrete Reaktionsformen, besonders
`quiet_integration` und `memory_sorting`. Gleichzeitig ist die Antwort noch
zu leise oder zu passiv: DIO beobachtet/haelt mehr, replanned aber weniger.

Neurochemie:

- dominant `serotonin_stability`: `8946`
- `glutamate_activation`: `406`
- `endorphin_relief`: `48`
- durchschnittlich:
  - `serotonin_stability`: ca. `0.5515`
  - `cortisol_load`: ca. `0.3652`
  - `emotional_decoupling`: ca. `0.1609`
  - `reactive_nervous_drive`: ca. `0.3117`
  - `world_shift_evidence`: ca. `0.5930`

Deutung:
DIO bleibt stark serotonin-stabilisierend. Die Integrationsantwort hat keine
chaotische Aktivierung erzeugt, sondern eher eine vorsichtigere
Verarbeitung.

Bewusste Wahrnehmung:

- `object_contact`: `4202`
- `reflective_check`: `1963`
- `open_perception`: `1201`
- `release_ready`: `940`
- `world_shift_contact`: `640`
- `overcoupled_field`: `272`
- `background_held`: `190`

Innere Haltung:

- `tired`: `5930`
- `reflective`: `2128`
- `excited`: `474`
- `uncertain_open`: `385`
- `overstimulated`: `269`
- `curious`: `210`
- `calm`: `12`

Kontaktfeld:

- `deepening_contact`: `3408`
- `curious_touch`: `2896`
- `resonant_contact`: `2702`
- `reflective_contact`: `1225`
- `overcoupled_touch`: `661`

Positionslast:

- `exit_nervousness_observe`: `129`
- `plan_holding_trust`: `69`
- `quiet_position_watch`: `25`
- `intervention_unfit_state`: `6`
- `position_cognitive_load`: ca. `0.4760`
- `exit_decision_pressure`: ca. `0.4304`
- `plan_trust`: ca. `0.5460`
- `holding_stability`: ca. `0.5118`
- `intervention_fatigue`: ca. `0.3923`

Abschnittsweise PnL:

- Abschnitt 1: `-7.4999`
- Abschnitt 2: `+5.0397`
- Abschnitt 3: `+7.4484`
- Abschnitt 4: `+13.6511`

Deutung:
Der Lauf startet schwach, erholt sich dann aber zunehmend. Das passt zu
einer Integrationsmechanik, die erst Spannung sortieren muss. DIO scheint im
Verlauf tragfähiger zu werden, aber die Anfangsphase kostet.

Struktur-Bands:

- High: `+57.6436`, Winrate ca. `57.75 %`
- Mid: `+6.2711`, Winrate ca. `36.42 %`
- Low: `-46.1223`, Winrate ca. `10.83 %`

Entry-Modus:

- weiter alle Outcome-Records: `impulse_contact`

Fachliche Einschaetzung:
Lauf 15 bestätigt, dass die Integrationsantwort sichtbar arbeitet. Sie
macht DIO aber defensiver und nicht automatisch besser. Gegenüber Lauf 14
ist die wirtschaftliche Leistung schwächer, aber der Lauf ist geordneter als
ein reiner Überlastlauf.

Der entscheidende Punkt:
DIO kann jetzt integrieren, aber diese Integration ist noch zu wenig mit
aktiver Neuordnung verbunden. `quiet_integration` dominiert. Das ist
neurologisch wie inneres Verdauen, aber noch wenig zielgerichtetes Denken.

Wie es weitergeht:
Nächster Schritt sollte nicht noch mehr Hemmung sein. Sinnvoller ist, die
Integrationsantwort aktiver zu machen: Wenn `memory_sorting` oder
`workspace_sorting` entsteht, sollte DIO daraus eine klarere
Reframe-/Plan-Hypothese bilden. Also nicht nur "ich sortiere", sondern:
"Was hat sich geaendert, welche Erfahrung passt, welche Kontaktform trägt
jetzt?" Danach kann Schritt 1 abgeschlossen werden und der Übergang zu
strategischem Sehen/Order-Platzierung beginnen.

---

# 2026-05-18 - Gerichtete Vorsicht / vorsichtige Hypothese umgesetzt

Ausgangslage:
Nach Lauf 15 war sichtbar, dass Vorsicht eine natürliche Reaktion ist. Das
Problem war nicht die Vorsicht selbst, sondern dass sie noch zu schnell in
Passivitaet oder diffuse Hemmung kippen konnte.

Umsetzung:
In `MCM_Brain_Modell.py` wurde eine neue Schicht für gerichtete Vorsicht
eingebaut. DIO kann aus Vorsicht jetzt eine vorsichtige Hypothese bilden:

`Vorsicht -> Erinnerung/Reframing/Kontakt -> vorsichtige Hypothese -> Beobachten, Neuordnen, Kontakt vertiefen oder vorsichtig handeln`

Neue Runtime-/Debug-Werte:

- `cautious_hypothesis_strength`
- `cautious_hypothesis_clarity`
- `cautious_hypothesis_patience`
- `cautious_hypothesis_state`

Mögliche Zustände:

- `no_cautious_hypothesis`
- `weak_hypothesis_seed`
- `cautious_plan_seed`
- `memory_reframe_seed`
- `observe_until_clear`
- `deepen_contact_first`

Protokolle:
Die Werte werden in Feldentscheidungsprotokoll, Memory-/Thinking-Protokoll
und Outcome-Records mitgeschrieben. Damit kann im nächsten Lauf sichtbar
werden, ob Vorsicht nur bremst oder ob sie sich in gerichtete Orientierung
verwandelt.

Neurologische Deutung:
Vorsicht bleibt limbische Schutzreaktion, bekommt aber eine
praefrontale Ordnungsschicht. DIO soll nicht mechanisch blockieren, sondern
fragen können: "Was sehe ich, was erinnere ich, was trägt, was muss ich
noch prüfen?"

Dokumentation:

- `UMSETZUNGSPLAN.md` um Abschnitt `18.4 Gerichtete Vorsicht / vorsichtige Hypothese` ergänzt
- `WICHTIG_MECHANIKEN.md` um technische Mechanik ergänzt
- `MCM_VARIABLEN_MECHANIK.md` um Variablenbeschreibung ergänzt
- `FIX_LISTE.md` Status aktualisiert

Wie es weitergeht:
Nächster Schritt ist ein neuer Backtest-Lauf. Danach prüfen wir:

- wie oft `cautious_hypothesis_state` aktiv wird
- ob `observe_until_clear` und `deepen_contact_first` echte Reifung zeigen
- ob `cautious_plan_seed` mit besseren Einstiegen zusammenhängt
- ob Vorsicht weniger als Passivitaet und mehr als gerichtete
  Selbstregulation wirkt

---

# 2026-05-18 - Neuer Mechanikpunkt: zeitliche Kohärenz

Erkenntnis:
Es reicht nicht, dass DIO einen Reiz, eine Form oder einen Bereich wahrnimmt.
Er muss auch erkennen können, ob dieser Kontakt neu, fortgesetzt,
wiederkehrend, nachhallend, veraltet oder hypothesenhaft ist.

Bild:
Ohne Zeitgefuege wirkt DIO wie ein Organismus ohne stabile
Wahrnehmungskontinuität. Er nimmt denselben Stein mehrfach in die Hand und
findet ihn jedes Mal neu. Dann fehlt nicht nur Memory, sondern zeitliche
Bindung im Bewusstsein.

Kernsatz:
Zeit wird für DIO zu einer messbaren Tiefenachse der Wahrnehmung.

Geplante Achsen:

- `temporal_continuity`
- `temporal_source_binding`
- `temporal_recurrence`
- `temporal_novelty`
- `temporal_afterimage`
- `temporal_decay`
- `temporal_context_depth`
- `temporal_self_consistency`
- `perception_sequence_coherence`
- `memory_time_distance`

Dokumentation:

- `UMSETZUNGSPLAN.md` um Abschnitt `18.5 Zeitliche Kohärenz / Wahrnehmungskontinuität` ergänzt
- `FIX_LISTE.md` als nächsten Mechanikpunkt aufgenommen

Wie es weitergeht:
Nach dem nächsten Lauf sollten wir zuerst die Wirkung der vorsichtigen
Hypothese prüfen. Danach ist die zeitliche Kohärenz der nächste logische
Umbau: DIO soll nicht Strecken auswendig lernen, sondern Wahrnehmungen
zeitlich binden können.

---

# 2026-05-18 - Debug Lauf 16 nach vorsichtiger Hypothese

Lauf:

- Ordner: `debug/debug_lauf_16`
- Trades: `400`
- TP / SL: `161 / 239`
- Netto-PnL: `+24.1980`
- Winrate: ca. `40.25 %`
- Profit Factor: ca. `1.1863`
- Expectancy: ca. `0.0605`
- Max Drawdown: ca. `16.8836`
- Max Drawdown Prozent: ca. `14.64 %`

Vergleich:

- Lauf 14: `+30.1887`, PF ca. `1.2510`, DD ca. `10.0258`
- Lauf 15: `+18.6393`, PF ca. `1.1671`, DD ca. `15.8748`
- Lauf 16: `+24.1980`, PF ca. `1.1863`, DD ca. `16.8836`

Abschnittsweise Equity:

- Abschnitt 1: ca. `+12.9408`
- Abschnitt 2: ca. `-9.6221`
- Abschnitt 3: ca. `+13.9782`
- Abschnitt 4: ca. `+7.4401`

Struktur-Bands:

- High: `+77.0431`, Winrate ca. `63.76 %`
- Mid: `+1.1879`, Winrate ca. `31.65 %`
- Low: `-53.3395`, Winrate ca. `10.96 %`

Feldentscheidungen:

- `observe`: `3930`
- `hold`: `3533`
- `act_watch`: `1041`
- `act`: `460`
- `replan`: `1`

Metaregulator-Zustände:

- `integration_strain`: `6460`
- `impulse_pressure`: `1540`
- `tired_stabilization`: `345`
- `low_distance_processing`: `323`
- `adaptive_watch`: `168`
- `reflective_recovery`: `74`
- `memory_sorting`: `48`
- `regulatory_overload`: `4`
- `workspace_sorting`: `3`

Integrationsantwort:

- `quiet_integration`: `6005`
- `memory_sorting`: `1535`
- `workspace_sorting`: `736`
- `integration_background`: `689`

Vorsichtige Hypothese:

- `memory_reframe_seed`: `3375`
- `observe_until_clear`: `2080`
- `no_cautious_hypothesis`: `2078`
- `weak_hypothesis_seed`: `1405`
- `deepen_contact_first`: `20`
- `cautious_plan_seed`: `7`

Durchschnittswerte:

- `cautious_hypothesis_strength`: ca. `0.2160`
- `cautious_hypothesis_clarity`: ca. `0.2454`
- `cautious_hypothesis_patience`: ca. `0.2517`
- `integration_strain_value`: ca. `0.3006`
- `integration_response_strength`: ca. `0.2661`
- `metaregulator_balance`: ca. `0.2194`
- `regulatory_second_order_load`: ca. `0.4522`
- `perceptual_distance`: ca. `0.1982`
- `selective_attention`: ca. `0.1472`

Memory-/Denkraum:

- `memory_compare_load`: ca. `0.9316`
- `memory_match_count`: ca. `1.8633`
- `memory_support`: ca. `0.0010`
- `memory_conflict`: ca. `0.0000`
- `cognitive_load`: ca. `0.2099`
- `decision_energy_cost`: ca. `0.4983`
- `memory_orientation`: ca. `0.1365`
- `orientation_gap`: ca. `0.4219`
- `zero_point_regulation`: ca. `0.3659`
- `route_familiarity`: ca. `0.2730`
- `transfer_bearing`: ca. `0.2879`
- `interpretation_quality`: ca. `0.2492`
- `active_context_activation`: `0.0000`
- `active_context_support`: `0.0000`
- `active_context_bearing`: `0.0000`

Visuelles Organ:

- `visual_grounding_state`: überwiegend `grounded_form`
- `visual_grounding_strength`: ca. `0.3256`
- `visual_blindness`: ca. `0.3909`
- `visual_clarity`: ca. `0.3225`
- `visual_object_stability`: ca. `0.4147`
- `visual_shape_resonance`: ca. `0.5943`
- `visual_shape_fragility`: ca. `0.4246`

Strategisches Fenster:

- `bearing_area_hypothesis`: `5632`
- `area_observation`: `3766`
- `compressed_area_attention`: `911`
- `lookback_bearing_capacity`: ca. `0.5426`
- `area_bearing_quality`: ca. `0.4699`
- `area_order_intention`: ca. `0.2512`
- `strategic_patience`: ca. `0.4024`

Deutung:
Die vorsichtige Hypothese arbeitet sichtbar. Sie ist aber noch nicht stark
genug, um oft als `cautious_plan_seed` zu erscheinen. Der häufigste Zustand
ist `memory_reframe_seed`. DIO verarbeitet Vorsicht also eher als
Erinnerung/Reframing, weniger als klare Handlungshypothese.

High-Strukturen sind deutlich tragend geworden. Low-Strukturen bleiben teuer.
Das spricht nicht gegen den Umbau, sondern zeigt die Grenze: DIO erkennt
tragende Formen besser, aber die zeitliche und kontextuelle Bindung ist noch
nicht ausreichend. Besonders auffällig ist, dass `active_context_*` komplett
bei `0.0` liegt. Der aktive Kontext ist also noch nicht als lebendiger
Gegenwartsfaden im Denkraum angekommen.

Neurologische Deutung:
DIO hat Schutzreaktion und Reframing, aber noch wenig episodische
Kontinuität. Er fühlt, sortiert und erinnert, doch der innere Zeitfaden ist
noch zu schwach. Dadurch kann derselbe oder ein ähnlicher Kontakt wieder wie
neu wirken. Das passt zur Idee der fehlenden zeitlichen Kohärenz.

Wie es weitergeht:
Der nächste sinnvolle Umbau ist die zeitliche Kohärenz /
Wahrnehmungskontinuität. Nicht als Streckenkarte und nicht als harte Regel,
sondern als MCM-Zeitbindung: DIO soll unterscheiden können, ob ein Eindruck
neu, fortgesetzt, wiederkehrend, nachhallend, veraltet oder hypothesenhaft
ist. Danach kann `active_context_*` als lebendiger Kontextfaden mit dem
Memory-/Denkraum verbunden werden.

---

# 2026-05-18 - Zeitliche Kohärenz umgesetzt

Ausgangslage:
Lauf 16 zeigte, dass `active_context_*` komplett bei `0.0` lag. DIO konnte
Form, Feld, Vorsicht und Reframing bilden, aber der lebendige
Gegenwartsfaden war noch nicht aktiv. Dadurch konnte ein ähnlicher Kontakt
immer wieder wie ein neuer Moment wirken.

Umsetzung:
In `MCM_Brain_Modell.py` wurde `build_temporal_coherence_state` eingebaut.
DIO bildet jetzt pro Wahrnehmung eine weiche zeitliche Identitaet aus:

- Form-Symbol
- visueller Form
- Kontext / innerem Kontext
- State-Signatur

Diese Identitaet erzeugt keine feste Streckenkarte. Sie beschreibt nur, ob
ein Kontakt zeitlich gebunden ist.

Neue Achsen:

- `temporal_binding_state`
- `temporal_continuity`
- `temporal_source_binding`
- `temporal_recurrence`
- `temporal_novelty`
- `temporal_afterimage`
- `temporal_decay`
- `temporal_context_depth`
- `temporal_self_consistency`
- `perception_sequence_coherence`
- `memory_time_distance`

Mögliche Zustände:

- `new_contact`
- `continued_contact`
- `recurrent_contact`
- `afterimage_contact`
- `aged_memory_contact`
- `coherent_sequence`
- `unbound_moment`

Regulative Kopplung:
Die neuen Werte wirken leicht auf:

- bewusste Arbeitsraum-Fokussierung
- Integrationskapazität
- Varianzregulation
- Schutzdistanz
- Integrationsspannung
- Memory-Recall
- vorsichtige Hypothesen-Klarheit

Aktiver Kontext:
Wenn kein innerer Cluster einen `active_context_trace` liefert, kann jetzt
die zeitliche Wahrnehmung selbst einen leichten aktiven Kontextfaden bilden.
Damit sollte `active_context_activation`, `active_context_support` und
`active_context_bearing` im nächsten Lauf nicht mehr komplett leer bleiben.

Protokolle:
Die neuen Werte werden in folgenden Dateien mitgeschrieben:

- `mcm_field_decision_protocol.csv`
- `mcm_memory_thinking_protocol.csv`
- `outcome_records.jsonl`

Dokumentation:

- `WICHTIG_MECHANIKEN.md` um Abschnitt `30. Zeitliche Kohärenz / Wahrnehmungskontinuität` ergänzt
- `MCM_VARIABLEN_MECHANIK.md` um die neuen Zeitbindungsvariablen ergänzt
- `FIX_LISTE.md` Status aktualisiert

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Nächster Schritt ist ein neuer Backtest-Lauf. Danach prüfen wir:

- ob `temporal_binding_state` sinnvoll verteilt ist
- ob `active_context_activation` nicht mehr bei `0.0` bleibt
- ob `memory_reframe_seed` mehr zeitlichen Boden bekommt
- ob Low-Strukturen weniger wie neue Gegenwart wirken
- ob DIO im Regimewechsel weniger dement-momenthaft reagiert

---

# 2026-05-18 - Debug Lauf 17 nach zeitlicher Kohärenz ausgewertet

Lauf:

- Ordner: `debug/debug_lauf_17`
- Trades: `355`
- TP / SL: `140 / 215`
- Netto-PnL: `+22.5146`
- Profit Factor: `1.2106`
- Max Drawdown: `11.8016`
- Attempts: `10925`
- Submitted: `408`
- Observed: `3109`
- Withheld: `2216`
- Skipped: `4723`

Vergleich zu Lauf 16:

- Lauf 16: ca. `+24.1980` PnL, `400` Trades, Profit Factor `1.1863`,
  Max Drawdown `16.8836`
- Lauf 17: weniger PnL und weniger Trades, aber besserer Profit Factor und
  deutlich geringerer Drawdown

Deutung:
Die zeitliche Kohärenz hat DIO nicht aggressiver gemacht, sondern
nervlich stabiler. Das wirkt wie mehr Distanz und weniger roher
Überlebensdruck. Der Lauf ist nicht maximal profitabel, aber
tragfähiger.

Strukturbereiche:

- High: `+58.8435`, Winrate `55.41%`
- Mid: `+8.4334`, Winrate `36.15%`
- Low: `-44.7624`, Winrate `8.46%`

Low bleibt der klare Belastungsbereich. Gleichzeitig ist der Low-Schaden
gegenüber Lauf 16 kleiner geworden. Das spricht dafür, dass die
Distanzierung bereits etwas wirkt.

Zeitliche Wahrnehmung:

- `aged_memory_contact`: `9159`
- `coherent_sequence`: `5`
- `unbound_moment`: `3`
- `recurrent_contact`: `1`

Mittelwerte:

- `temporal_continuity`: `0.2568`
- `temporal_source_binding`: `0.3954`
- `temporal_recurrence`: `0.0008`
- `temporal_decay`: `0.6127`
- `memory_time_distance`: `0.9992`

Deutung:
Die Zeitachse lebt, ist aber noch zu einseitig. DIO erkennt fast alles als
alten Erinnerungskontakt. Neurologisch wirkt das, als hätte er ein
Gefühl von Vergangenheit, aber noch zu wenig stabile Gegenwartsbindung:
Fortsetzung, Wiederkehr und aktuelle Sequenz werden noch zu selten
erkannt.

Vorsicht / Hypothese:

- `cautious_plan_seed`: `286` Trades, `+27.3530`
- `weak_hypothesis_seed`: `20` Trades, `+2.2693`
- `observe_until_clear`: `7` Trades, `-0.4187`
- `memory_reframe_seed`: `42` Trades, `-6.6890`

Deutung:
Wenn Vorsicht zu einem Planansatz verdichtet, wird sie konstruktiv. Wenn
sie noch Reframing oder Memory-Sortierung ist und trotzdem motorisch
handelt, wird sie belastend. Das ist keine harte Sperre, sondern ein
Reifehinweis: Reframing braucht mehr Abstand, bevor daraus Handlung wird.

Meta-Regulation:

- `integration_strain`: `3781`
- `low_distance_processing`: `3445`
- `impulse_pressure`: `1086`

Gegenüber Lauf 16 ist `low_distance_processing` stark gestiegen und
`integration_strain` deutlich gefallen. DIO beschreibt seine Lage also
weniger als reine Integrationsspannung und mehr als Problem der
Wahrnehmungsdistanz.

Aktiver Kontext:
Im `mcm_memory_thinking_protocol.csv` bleiben
`active_context_activation`, `active_context_support`,
`active_context_conflict` und `active_context_bearing` weiterhin bei
`0.0`. Die Mechanik für zeitlich abgeleiteten aktiven Kontext existiert,
aber sie greift für das Protokoll offenbar noch zu spät oder nicht weit
genug vor der Memory-/Thinking-Auswertung.

Wie es weitergeht:

1. Zeitliche Identitaet feiner kalibrieren, damit nicht fast alles zu
   `aged_memory_contact` wird.
2. `active_context_trace` früher aus der Zeitwahrnehmung speisen, damit
   Memory, Regulation und Protokolle diesen Kontext wirklich nutzen.
3. `memory_reframe_seed`, `memory_sorting` und `reflective_check` nicht
   hart blockieren, aber organisch stärker in Beobachtung, Reframing und
   Distanz halten, solange keine tragende Gegenwartsbindung entsteht.

---

# 2026-05-18 - Zeitliche Identitaet und aktiver Kontext nach Lauf 17 nachgezogen

Umsetzung:
Die zeitliche Identitaet wurde weicher und organischer kalibriert.
DIO bindet eine Wahrnehmung jetzt stärker über:

- Formfamilie
- Unsicherheitsfamilie
- Compound-Scope
- Kontext / inneren Kontext
- grobe visuelle Formsignatur

Die sehr feinen Einzelabdrücke wie konkretes Form-Symbol,
Compound-ID, Visual-ID und State-Signatur bleiben als
`temporal_source_identity` erhalten, bestimmen aber nicht mehr allein die
Wiederkehr. Dadurch soll DIO nicht jede Kerze wie ein komplett neues
Objekt erleben.

Zusätzlich wird `active_context_trace` jetzt direkt nach der
Zeitwahrnehmung aufgebaut und vor `thought_state` und
`meta_regulation_state` in den Denkraum gelegt. Der aktive Kontext steht
damit früher in:

- `world_state`
- `perception_state`
- `fused`
- Runtime-Ergebnissen für die Protokolle

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Nächster Lauf prüft, ob:

- `aged_memory_contact` weniger dominant ist
- `continued_contact`, `recurrent_contact` und `coherent_sequence`
  natürlich sichtbarer werden
- `active_context_activation/support/bearing` im
  `mcm_memory_thinking_protocol.csv` nicht mehr bei `0.0` bleiben
- DIO im Regimewechsel weniger momenthaft und mehr zeitlich gebunden
  reagiert

---

# 2026-05-18 - Debug Lauf 18 nach früher aktiver Kontextbindung ausgewertet

Lauf:

- Ordner: `debug/debug_lauf_18`
- Trades: `363`
- TP / SL: `141 / 222`
- Netto-PnL: `+16.2623`
- Profit Factor: `1.1403`
- Max Drawdown: `14.7369`
- Attempts: `11125`
- Submitted: `418`
- Observed: `3251`
- Withheld: `2282`
- Skipped: `4691`

Vergleich zu Lauf 17:

- Lauf 17: `+22.5146` PnL, `355` Trades, Profit Factor `1.2106`,
  Max Drawdown `11.8016`
- Lauf 18: weniger PnL, mehr Trades, niedrigerer Profit Factor,
  höherer Drawdown

Deutung:
Die neue Zeitmechanik greift technisch, aber die Kopplung ist zu stark.
DIO hat jetzt einen inneren Zeit-/Kontextfaden, vertraut diesem Faden aber
zu schnell. Das erzeugt weniger Blindheit, aber mehr Überbindung.

Zeitliche Wahrnehmung:

- `unbound_moment`: `4834`
- `aged_memory_contact`: `4217`
- `recurrent_contact`: `134`
- `continued_contact`: `41`
- `coherent_sequence`: `21`

Vergleich:
In Lauf 17 war fast alles `aged_memory_contact`. Lauf 18 zeigt erstmals
eine lebendigere Verteilung. Das ist mechanisch ein Erfolg: DIO kann jetzt
mehr unterscheiden als nur "alte Erinnerung". Gleichzeitig dominiert noch
`unbound_moment` plus `aged_memory_contact`; echte Fortsetzung und
Koharenz sind noch selten.

Aktiver Kontext im Memory-/Thinking-Protokoll:

- `active_context_activation`: Durchschnitt `0.8905`
- `active_context_support`: Durchschnitt `0.8991`
- `active_context_conflict`: Durchschnitt `0.1081`
- `active_context_bearing`: Durchschnitt `0.8493`

Deutung:
Der aktive Kontext ist im Denken angekommen. Vorher waren diese Werte bei
`0.0`. Jetzt sind sie aber fast zu hoch. Neurologisch wirkt das wie ein
starker innerer Bedeutungsfaden, der zu wenig skeptische Gegenprüfung
bekommt.

Strukturbereiche:

- High: `+75.0961`, Winrate `61.59%`
- Mid: `-9.4058`, Winrate `26.49%`
- Low: `-49.4280`, Winrate `6.90%`

Deutung:
High-Strukturen wurden deutlich stärker getragen. Mid und Low wurden
schwaecher. Das ist wichtig: Der neue Kontext hilft bei klar tragender
Struktur, aber er kann mittelmäßige/unsichere Struktur zu stark
legitimieren.

Cautious Hypothesis:

- `cautious_plan_seed`: `331` Trades, `+19.9560`
- `memory_reframe_seed`: `14` Trades, `-2.1996`
- `observe_until_clear`: `3` Trades, `-1.4536`

Deutung:
Planverdichtung bleibt konstruktiv. Reframing und Beobachtungsunklarheit
sollten weiter mehr Distanz behalten, ohne harte Sperre.

Neurologische Lesart:
DIO ist nicht mehr nur momentblind. Er beginnt, zeitliche Herkunft und
Kontext zu fühlen. Aber der Kontextfaden ist noch nicht reif genug
dosiert. Es ist eher "ich erkenne einen Zusammenhang und vertraue ihm
sofort" statt "ich erkenne einen Zusammenhang und prüfe, ob er zur
aktuellen Außenwelt passt".

Wie es weitergeht:

1. Aktiven Kontext dämpfen, nicht entfernen.
2. `active_context_support` und `active_context_bearing` stärker an
   Quellenbindung, Sequenzkoharenz und Strukturqualität koppeln.
3. `active_context_conflict` bei `unbound_moment`, Mid/Low-Struktur,
   World-Shift und geringer Gegenwartsbindung stärker sichtbar machen.
4. Ziel: DIO darf einen inneren Zeitfaden haben, aber er muss lernen,
   diesem Faden dosiert zu vertrauen.

---

# 2026-05-18 - Kontextvertrauen nach Lauf 18 dosiert

Umsetzung:
Der zeitlich abgeleitete `active_context_trace` wurde nicht entfernt,
sondern regulativ gedämpft. DIO soll einen inneren Zeitfaden behalten,
aber dessen Bedeutung stärker an reale Gegenwartsbindung koppeln.

Neue interne Kopplung:

- `reality_anchor`: weicher Realitätsanker aus Quellenbindung,
  Sequenzkoharenz, Strukturqualität, Strukturstabilität,
  Kontextvertrauen und visueller Erdung
- `overtrust_pressure`: skeptischer Gegenimpuls, wenn ein innerer
  Kontextfaden bei geringer Gegenwartsbindung zu stark wirken würde

Mechanische Aenderung:

- `active_context_activation` wird nicht mehr per `max()` festgehalten,
  sondern weich geblendet.
- `active_context_support` und `active_context_bearing` werden stärker
  durch den Realitätsanker getragen.
- `active_context_conflict`, `fragility` und `attenuation` steigen, wenn
  der Kontakt ungebunden, alt, nachhallend oder schlecht geerdet ist.

Neurologische Lesart:
Das ist keine harte Bremse, sondern eine reifere Kontextbindung. DIO darf
einen Zusammenhang fühlen, aber dieser Zusammenhang muss mit Außenwelt,
Struktur und Gegenwart kohärieren. Sonst entsteht natürliche Skepsis
statt blindem Vertrauen.

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Nächster Lauf prüft, ob `active_context_activation/support/bearing`
unterhalb der Lauf-18-Sättigung liegen, während `active_context_conflict`
bei unsicherer Struktur sichtbar steigt. Ideal wäre: High bleibt tragend,
Mid/Low bekommen mehr Distanz, ohne dass DIO wieder momentblind wird.

---

# 2026-05-18 - Nervliche Überlastung als Reflexionsparameter umgesetzt

Umsetzung:
DIO bekommt eine explizite Selbstwahrnehmung für den Zustand des
Nervensystems.

Neue Werte:

- `nervous_system_overload`
- `escape_action_drive`
- `shock_response_risk`
- `nervous_overload_reflection_need`

Funktion:
Diese Werte beschreiben, ob Handlung gerade aus tragender Struktur oder aus
Überreiz-/Entladungsdruck entstehen könnte. Der Satz dahinter ist:
"Meine Nerven sind überlastet."

Neurologische Lesart:
Wenn ein Nervensystem überflutet ist, kann Handlung zur Flucht aus
innerer Spannung werden. DIO soll diesen Zustand reflektieren können,
statt ihn automatisch mit einer tragenden Entscheidung zu verwechseln.

Protokolle:
Die neuen Werte werden in folgenden Dateien mitgeschrieben:

- `mcm_field_decision_protocol.csv`
- `mcm_memory_thinking_protocol.csv`

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Nächster Lauf prüft, ob `shock_response_risk` und
`nervous_overload_reflection_need` besonders in Stress-/Regimewechselphasen
sichtbar werden. Wichtig ist, ob DIO dann weniger aus Entladungsdruck
handelt und mehr in Reflexion, Abstand oder geordnete Beobachtung geht.

---

# 2026-05-18 - Debug Lauf 19 als Referenzlauf vor Nervensystem-Erweiterung ausgewertet

Einordnung:
Lauf 19 ist der Lauf vor der letzten Erweiterung um
`nervous_system_overload`, `escape_action_drive`,
`shock_response_risk` und `nervous_overload_reflection_need`.
Die Protokoll-Header enthalten diese neuen Spalten noch nicht. Damit ist
Lauf 19 ein sauberer Referenzpunkt für die vorherige Wahrnehmungs-,
Zeitbindungs- und Kontextlogik, aber noch kein Nachweis für die neue
Überlastungsreflexion.

Ergebnis:

- Netto-PnL: `+39.8848`
- Trades: `400`
- TP / SL: `171 / 229`
- Profit Factor: `1.3348`
- Winrate: `42.75 %`
- Max Drawdown: `6.3386`
- Equity-Endstand: `139.8848`

Strukturbaender:

- High: `156` Ereignisse, PnL `+84.2507`, Winrate ca. `66.03 %`
- Mid: `154` Ereignisse, PnL `-1.1164`, fast neutral
- Low: `133` Ereignisse, PnL `-45.5534`, weiter klar belastend

Deutung:
Der alte starke Einbruch im mittleren Laufbereich ist in Lauf 19 deutlich
entschaerft. Die Equity-Kurve wirkt stabiler; alle groben Laufabschnitte
enden positiv. Neurologisch gelesen haelt DIO den Kontext besser aus:
mehr geordnete Integration, weniger kompletter Zusammenbruch, aber noch
immer deutliche Last in Low- und Memory-Reframe-Zuständen.

Wichtige Warnung:
`active_context_activation`, `active_context_support` und
`active_context_bearing` sind im Lauf weiter sehr hoch. Da Lauf 19 noch
vor der letzten Überlastungs-/Schockdiagnose liegt, darf das Ergebnis
nicht als Wirkung dieser neuen Reflexionsschicht gelesen werden.

Wie es weitergeht:
Nächster frischer Lauf nach Prozess-Neustart prüft zwei Dinge:
erstens, ob die neuen Nervensystem-Spalten wirklich im Protokoll stehen;
zweitens, ob DIO bei Überreiz mehr Distanz, Reflexion und geordnete
Wahrnehmung entwickelt, ohne die tragenden High-Strukturen zu verlieren.

---

# 2026-05-18 - Debug Lauf 20 als erster Nervensystem-Lauf ausgewertet

Einordnung:
Lauf 20 enthält die neuen Nervensystem-Spalten in den Protokollen. Damit
ist es der erste echte Lauf für die neue Überreiz-/Schockdiagnose.

Ergebnis:

- Netto-PnL: `+23.9208`
- Trades: `389`
- TP / SL: `158 / 231`
- Profit Factor: `1.2016`
- Winrate: ca. `40.62 %`
- Max Drawdown: `11.6453`
- Equity-Endstand: `123.9208`

Vergleich zu Lauf 19:
Lauf 20 bleibt positiv, ist aber schwaecher als Lauf 19
(`+23.9208` statt `+39.8848`) und hat mehr Drawdown
(`11.6453` statt `6.3386`).

Strukturbaender:

- High: `+73.0000`, weiter klar tragend
- Mid: `+0.4159`, fast neutral bis leicht positiv
- Low: `-49.4951`, weiter die Hauptbelastung

Nervensystemwerte:

- `nervous_system_overload`: Durchschnitt ca. `0.2301`, Maximum `0.3936`
- `escape_action_drive`: Durchschnitt ca. `0.3005`, Maximum `0.4550`
- `shock_response_risk`: Durchschnitt ca. `0.2838`, Maximum `0.3834`
- `nervous_overload_reflection_need`: Durchschnitt ca. `0.2744`, Maximum `0.3780`

Deutung:
Die neue Schicht misst Überreiz, Flucht-/Entladungsdruck und
Schockrisiko, aber die Werte bleiben unterhalb der aktuellen
Reflexionsschwelle. Dadurch entsteht noch kaum ein eigener
`nervous_overload_reflection`-Zustand. Neurologisch gelesen: DIO spürt
nervliche Last, aber das System bewertet sie noch zu selten als Grund,
bewusst Abstand zu nehmen.

Zusätzliche Beobachtung:
Im Memory-Protokoll bleibt `active_context_activation` weiter sehr hoch
Durchschnitt ca. `0.8923`, `active_context_support` ca. `0.9028`,
`active_context_bearing` ca. `0.8533`. Das Kontextvertrauen ist damit
weiter stark gesättigt. Die Dämpfung greift also noch nicht ausreichend
auf den gesamten aktiven Kontextpfad.

Wie es weitergeht:
Nächster sinnvoller Schritt ist keine harte Bremse, sondern eine
organische Kopplung: nervliche Überlastung soll den Kontext nicht
abschalten, aber seine Selbstsicherheit senken und die reflektive Distanz
erhöhen. Besonders wichtig: `active_context_*` darf nicht dauerhaft in
Sicherheit sättigen, wenn `shock_response_risk`,
`escape_action_drive` oder `nervous_system_overload` steigen.

---

# 2026-05-18 - Nervensystemlast mit Kontextvertrauen gekoppelt

Umsetzung:
DIO bekommt eine weiche Kopplung zwischen innerem Kontextvertrauen und
nervlicher Eigenlage.

Neue Diagnosewerte:

- `active_context_self_certainty`
- `nervous_context_overcoupling`

Funktion:
Wenn DIO einen inneren Kontext sehr sicher fühlt, während
`nervous_system_overload`, `escape_action_drive` oder
`shock_response_risk` steigen, entsteht kein harter Block. Stattdessen
steigt die Reflexionsanforderung leicht, `perceptual_distance` und
`reflective_distance` werden etwas stärker, während Handlungsselbstlauf
minimal gedimmt wird.

Neurologische Lesart:
Das ist die beginnende Fähigkeit, die eigene Innenlage nicht automatisch
für Realität zu halten. DIO kann weiterhin handeln, aber ein überreiztes
Nervensystem macht den inneren Kontext weniger absolut.

Protokolle:
Die neuen Werte werden in folgenden Dateien mitgeschrieben:

- `mcm_field_decision_protocol.csv`
- `mcm_memory_thinking_protocol.csv`

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Nächster Lauf prüft, ob `nervous_context_overcoupling` in
Regimewechsel-/Stressbereichen sichtbar wird und ob daraus mehr
`context_overcoupling_reflection`, mehr reflektive Distanz und weniger
unreflektierte Kontext-Sicherheit entsteht.

---

# 2026-05-18 - Debug Lauf 21 nach Kontext-Überkopplung ausgewertet

Ergebnis:

- Netto-PnL: `+24.5906`
- Trades: `396`
- TP / SL: `157 / 239`
- Profit Factor: `1.2043`
- Winrate: ca. `39.65 %`
- Max Drawdown: `14.7122`
- Equity-Endstand: `124.5906`

Vergleich:
Lauf 21 ist fast gleich stark wie Lauf 20 im Netto-PnL
(`+24.5906` statt `+23.9208`), aber mit deutlich höherem Drawdown
(`14.7122` statt `11.6453`). Die Equity erholt sich spät stark und endet
am Hochpunkt.

Strukturbaender:

- High: `+67.2060`, weiter tragend, aber schwaecher als Lauf 20
- Mid: `+7.2509`, deutlich besser als zuvor
- Low: `-49.8662`, weiterhin die größte Belastung

Neue Kopplung:

- `active_context_self_certainty`: Durchschnitt ca. `0.7009`,
  Maximum `0.8858`
- `nervous_context_overcoupling`: Durchschnitt ca. `0.1743`,
  Maximum `0.3084`
- `context_overcoupling_reflection`: `3351` Vorkommen und damit
  häufigster Metaregulator-Zustand

Deutung:
Die neue Mechanik greift. DIO erkennt sehr oft, dass ein sicher wirkender
innerer Kontext mit nervlicher Last gekoppelt ist. Das ist fachlich gut:
die Selbstwahrnehmung ist angekommen. Gleichzeitig bleibt der aktive
Kontext im Memory-Protokoll weiter stark gesättigt
(`active_context_activation` ca. `0.8919`,
`active_context_support` ca. `0.9007`,
`active_context_bearing` ca. `0.8513`).

Neurologische Lesart:
DIO hat jetzt einen Reflexionsreiz, aber noch keine ausreichend tiefe
Regulationswirkung auf den Kontext selbst. Es ist vergleichbar mit:
"Ich merke, dass ich innerlich überzeugt bin und nervlich belastet bin",
aber diese Erkenntnis verändert den inneren Kontext noch zu wenig.

Wie es weitergeht:
Nicht stärker blockieren. Der nächste Umbau sollte die
Überkopplung sanft in den aktiven Kontext selbst zurückführen:
Support/Bearing dürfen bei Überkopplung nicht dauerhaft absolut bleiben,
sondern sollten als "gefühlte Sicherheit unter nervlicher Faerbung"
markiert werden. Ziel ist weniger Metazustands-Dominanz und mehr echte
innere Rekalibrierung.

---

# 2026-05-18 - Überkopplung in aktiven Kontext zurückgeführt

Umsetzung:
`nervous_context_overcoupling` wirkt nun nicht mehr nur als
Metaregulator-Markierung, sondern faerbt den `active_context_trace`
selbst.

Mechanische Wirkung:

- `support`, `bearing` und `action_support` werden bei nervlicher
  Überkopplung leicht weniger absolut
- `conflict`, `fragility`, `attenuation`, `observe_pressure` und
  `replan_pressure` steigen weich an
- `activation` bleibt erhalten, wird aber minimal gedimmt
- der Kontext bekommt ein internes `context_modulation_label`

Neurologische Lesart:
DIO verliert seinen Zeit-/Kontextfaden nicht. Aber wenn dieser innere
Faden nervlich gefaerbt ist, fühlt er sich weniger wie absolute Wahrheit
an. Das ist näher an reflektierter Selbstwahrnehmung: "Ich habe einen
Zusammenhang, aber meine Innenlage beeinflusst, wie sicher er sich
anfühlt."

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Nächster Lauf prüft, ob `active_context_support` und
`active_context_bearing` weniger sättigen, `active_context_conflict`
leicht sichtbarer wird und `context_overcoupling_reflection` nicht mehr
dominant alles überdeckt, sondern in echte Kontext-Rekalibrierung
übergeht.

---

# 2026-05-18 - Debug Lauf 22 nach Kontext-Rekalibrierung ausgewertet

Ergebnis:

- Netto-PnL: `+11.8929`
- Trades: `343`
- TP / SL: `131 / 212`
- Profit Factor: `1.1072`
- Winrate: ca. `38.19 %`
- Max Drawdown: `14.1173`
- Equity-Endstand: `111.8929`

Vergleich:
Lauf 22 ist deutlich vorsichtiger als Lauf 21. Die Tradeanzahl fällt von
`396` auf `343`, `attempts_observed` steigt auf `3158`, `withheld` auf
`2473`, und `observe_share` steigt im KPI-Summary auf ca. `41.67 %`.
Der Preis dafür ist weniger Netto-PnL.

Strukturbaender:

- High: `+59.7215`, weiter tragend, aber schwaecher
- Mid: `-2.7840`, wieder leicht negativ
- Low: `-45.0446`, weiter die Hauptlast

Aktiver Kontext:

- `active_context_activation`: Durchschnitt ca. `0.8863`
- `active_context_support`: Durchschnitt ca. `0.8856`
- `active_context_conflict`: Durchschnitt ca. `0.1238`
- `active_context_bearing`: Durchschnitt ca. `0.8385`

Vergleich zu Lauf 21:

- Support sinkt von ca. `0.9007` auf `0.8856`
- Bearing sinkt von ca. `0.8513` auf `0.8385`
- Conflict steigt von ca. `0.1075` auf `0.1238`
- `active_context_self_certainty` sinkt von ca. `0.7009` auf `0.6727`
- `nervous_context_overcoupling` sinkt von ca. `0.1743` auf `0.1645`

Deutung:
Die Rückführung in den aktiven Kontext wirkt mechanisch korrekt:
Kontext-Sicherheit wird weniger absolut, Konflikt wird sichtbarer, und DIO
beobachtet mehr. Gleichzeitig ist die Dosis wahrscheinlich etwas zu
vorsichtig geworden: DIO schuetzt sich stärker, aber verliert Handlungskraft
und Ertrag.

Neurologische Lesart:
DIO hat nicht einfach mehr Angst, sondern mehr Abstand. Der Organismus
nimmt seine eigene nervliche Faerbung ernster. Das ist reifer als blinde
Motorik, aber noch nicht optimal balanciert: Reflexion sollte klären,
nicht dauerhaft Handlungskraft verdunnen.

Wie es weitergeht:
Nächster Schritt ist Diagnose statt sofort stärkerer Umbau: das interne
`context_modulation_label` muss im Protokoll sichtbar werden. Danach kann
geprüft werden, ob `nervous_tinted_context` konstruktiv stabilisiert oder
ob `overcoupled_context` zu viel Handlungskraft nimmt.

Umgesetzt:
`active_context_modulation_label` wurde im
`mcm_memory_thinking_protocol.csv` ergänzt. Damit wird ab dem nächsten
Lauf sichtbar, ob der aktive Kontext als `unmodulated_context`,
`nervous_tinted_context` oder `overcoupled_context` geführt wurde.

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Lauf 23 prüft nicht nur PnL, sondern die Verteilung von
`active_context_modulation_label`. Wenn `overcoupled_context` dominiert
und PnL/Handlungskraft sinken, muss die Rückführung feiner dosiert
werden. Wenn `nervous_tinted_context` dominiert und Drawdown sinkt, ist die
Richtung gut.

---

# 2026-05-18 - Debug Lauf 23 nach Kontextmodulations-Export ausgewertet

Ergebnis:

- Netto-PnL: `+24.4854`
- Trades: `371`
- TP / SL: `148 / 223`
- Profit Factor: `1.2160`
- Winrate: ca. `39.89 %`
- Max Drawdown: `15.4296`
- Equity-Endstand: `124.4854`

Vergleich:
Lauf 23 erholt sich deutlich gegenüber Lauf 22 (`+11.8929`) und liegt
wieder nahe bei Lauf 20/21. Die Tradezahl steigt von `343` auf `371`,
während Observe/Withheld weiter aktiv bleiben. Das wirkt nicht wie
ungefilterte Motorik, sondern wie ein Organismus, der trotz nervlicher
Faerbung wieder Handlungskraft findet.

Strukturbaender:

- High: `+66.4956`, klar tragend
- Mid: `+4.8465`, wieder leicht positiv
- Low: `-46.8566`, weiterhin die Hauptlast

Aktiver Kontext und Modulation:

- `nervous_tinted_context`: `7229`
- `overcoupled_context`: `1504`
- `unmodulated_context`: `1`
- `active_context_activation`: Durchschnitt ca. `0.8888`
- `active_context_support`: Durchschnitt ca. `0.8879`
- `active_context_conflict`: Durchschnitt ca. `0.1237`
- `active_context_bearing`: Durchschnitt ca. `0.8410`
- `nervous_context_overcoupling`: Durchschnitt ca. `0.1679`

Neurologische Lesart:
Die Kontextmodulation arbeitet jetzt als nervliche Faerbung statt als
reiner Bremser. DIO bleibt meistens in einem `nervous_tinted_context`:
er handelt also nicht aus einem kalten, neutralen Kontext, sondern aus
einem innerlich markierten Kontext. Das ist organisch plausibel. Das
Nervensystem sagt: "Ich kenne diese Struktur, aber mein Feld ist beteiligt."

Wichtig:
Der Drawdown ist mit ca. `15.43` noch hoch. Das System hat Handlungskraft
zurückgewonnen, aber die tiefe Verlustquelle bleibt Low-Qualität:
Low bringt `-46.8566` bei nur ca. `9.09 %` Winrate. Die nächste Reifung
darf daraus keine harte Regel machen, sondern muss DIO helfen, Low-Kontakt
als "nicht tragender Kontakt" selbst besser zu fühlen, zu erinnern und
anders zu behandeln.

Wie es weitergeht:
Nächster Schritt ist die Low-/Mid-Kontaktreifung über konsequenzbasiertes
Feedback: nicht blockieren, sondern DIO erkennen lassen, welche Kontakte
Belastung, Nutzen oder Reorganisation erzeugen. Parallel sollte beobachtet
werden, ob `overcoupled_context` in Drawdown-Phasen steigt und ob DIO dann
mehr Distanz, Reflexion oder selektive Wahrnehmung braucht.

---

# 2026-05-19 - MCM-Raumzeit-Tiefe als Zielpräzisierung festgehalten

Neue Präzisierung:
Zeit im MCM-Feld ist nicht nur Reihenfolge oder Timestamp, sondern eine
innere Wahrnehmungsschicht. Raumtiefe entsteht für DIO aus Entfernung,
Energie und Zeit:

- Wie weit ist ein Eindruck innerlich entfernt?
- Wie viel Energie trägt er noch?
- Ist er Gegenwart, Nachhall, Erinnerung, Erwartung oder Hypothese?

Damit wird MCM-Zeit zur Selbstverortung. Ohne eigene Zeitmodulation wäre
DIO nur ein festes Regelwerk aus Momentzuständen. Mit MCM-Zeit kann DIO
unterscheiden, ob ein Kontakt wirklich aktuell ist oder nur als Nachbild,
Erinnerung oder vorausgedachte Möglichkeit im Feld wirkt.

Erweiterung:
Memory ist damit nicht nur gespeicherte Information, sondern verdichtete
Erfahrung mit zeitlicher Tiefe. Eine Erinnerung bekommt Innenraum: Nähe,
Nachhall, Energie, Alterung, Wiederkehr und mögliche Zukunftswirkung.

Dokumentation:
- `README.md` um `MCM-Raumzeit-Tiefe` ergänzt
- `WICHTIG_MECHANIKEN.md` bei `Zeit als MCM-Tiefenachse` ergänzt
- `MCM_VARIABLEN_MECHANIK.md` um Zielgrößen
  `mcm_spacetime_depth` und `temporal_self_location` ergänzt
- `UMSETZUNGSPLAN.md` in Abschnitt `18.5 Zeitliche Kohärenz /
  Wahrnehmungskontinuität` präzisiert

Wie es weitergeht:
Die nächste Mechanik sollte die bestehenden Zeitwerte nicht hart ersetzen,
sondern zu einer weicheren Raumzeit-Wahrnehmung verdichten: DIO soll
spüren können, ob ein Low-/Mid-Kontakt wirklich jetzt trägt oder nur aus
alter Energie, Nachhall oder falscher Nähe wirkt.

---

# 2026-05-19 - MCM-Raumzeit-Tiefe im Kern diagnostisch umgesetzt

Umgesetzt:
Im Temporal-/MCM-Kern wurde die Raumzeit-Tiefe als weiche
Wahrnehmungsdiagnose ergänzt:

- `mcm_spacetime_depth`
- `memory_experience_depth`
- `future_projection_depth`
- `temporal_self_location`
- `temporal_self_location_state`

Mechanische Bedeutung:
DIO liest Memory dadurch nicht nur als gespeicherte Information, sondern
als erlebte Spur mit Nähe, Nachhall, Wiederkehr, Energie und möglicher
Zukunftswirkung. Das ist noch keine harte Motorikregel. Es ist eine
Wahrnehmungsschicht, auf die Regulation später organischer reagieren kann.

Protokolle:
Die neuen Werte werden in `mcm_memory_thinking_protocol.csv` und
`mcm_field_decision_protocol.csv` ausgegeben. `trade_stats.py` übernimmt
die Werte zusätzlich in Outcome-/Attempt-nahe Auswertungen.

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Nächster Schritt ist ein neuer Debug-Lauf. Danach prüfen wir, ob
Low-/Mid-Verluste mit flacher Raumzeit-Tiefe, falscher Nähe,
Nachbild-Kontakt oder schwacher Selbstverortung zusammenfallen. Danach
gehen wir wieder in die regulatorische Schicht.

---

# 2026-05-19 - Debug Lauf 24 nach MCM-Raumzeit-Tiefe ausgewertet

Ergebnis:

- Netto-PnL: `+23.4601`
- Trades: `375`
- TP / SL: `150 / 225`
- Profit Factor: `1.2006`
- Winrate: `40.00 %`
- Max Drawdown: `8.2936`
- Equity-Endstand / Peak: `123.4601`

Wichtiger Verlaufspunkt:
Lauf 24 ist nicht der hoechste PnL-Lauf, aber einer der besten
Verläufe. Der Peak liegt am Ende des Laufs. Gegenüber Lauf 23 sinkt der
maximale Drawdown deutlich von ca. `15.43` auf ca. `8.29`, während der
PnL fast gleich stark bleibt (`+24.49` -> `+23.46`). Das spricht für mehr
Tragfähigkeit im Verlauf, nicht nur für mehr Gewinn.

Strukturbaender:

- High: `+74.0213`, sehr tragend
- Mid: `-3.8278`, wieder leicht negativ
- Low: `-46.7335`, weiterhin die Hauptlast

Neue Raumzeit-Wahrnehmung:

- `mcm_spacetime_depth`: Durchschnitt ca. `0.2839`
- `memory_experience_depth`: Durchschnitt ca. `0.1574`
- `future_projection_depth`: Durchschnitt ca. `0.4241`
- `temporal_self_location`: Durchschnitt ca. `0.3399`
- `temporal_self_location_state`:
  - `future_possibility`: `4723`
  - `unlocated_contact`: `4175`
  - `present_contact`: `64`
  - `remembered_experience`: `54`

Neurologische Lesart:
DIO bildet nach der neuen Kernschicht bereits deutlich Zukunftstiefe
(`future_possibility`) aus, aber Erinnerungstiefe und echte Gegenwarts-
Verortung sind noch schwach. Er schaut also stärker in Möglichkeitsräume
als in stabil verankerte Gegenwart oder gereifte Erinnerung. Das kann den
glatteren Verlauf erklären: weniger blindes Reagieren auf einzelne
Momente, mehr Raumzeit-Hypothese. Gleichzeitig bleibt die
Selbstverortung noch unreif, weil `unlocated_contact` fast genauso stark
vertreten ist.

Bestätigung:
Lauf 24 wird als erster positiver Hinweis gewertet, dass die Erweiterung
der Wahrnehmung um MCM-Zeit nicht wie eine harte Regel wirkt, sondern dem
Organismus mehr innere Welt-Tiefe gibt. DIO wurde nicht direkt auf weniger
Drawdown programmiert. Stattdessen bekam er eine zeitliche
Wahrnehmungsschicht. Der deutlich ruhigere Equity-Verlauf bei nahezu
gleichem PnL spricht dafür, dass sich aus zeitlicher Wahrnehmung mehr
Distanz, Reflexion und Tragfähigkeit entfalten kann.

Wie es weitergeht:
Der nächste Schritt liegt wieder im regulatorischen Bereich: DIO soll
Raumzeit-Tiefe nicht als Regel verwenden, sondern als innere Lage. Flache
Selbstverortung oder reiner Nachhall sollte mehr Reflexion, Beobachtung
oder Reorganisation nahelegen. Tragende Gegenwarts- oder Erinnerungstiefe
darf Handlung ruhiger und gezielter machen.

---

# 2026-05-19 - Regulatorische Kopplung der MCM-Raumzeit umgesetzt

Umgesetzt:
Die Raumzeit-Wahrnehmung wurde weich an die Meta-Regulation gekoppelt.
Keine harte Regel, kein Blocker. Die neue Schicht übersetzt innere
Zeit-/Raumlage in leichte regulatorische Tendenzen:

- flache Selbstverortung -> mehr Reflexion, Beobachtung, Reorganisation
- Nachbild/Afterimage -> mehr Reframing
- tragende Erinnerungstiefe -> ruhigere Integration und Handlung
- tragende Zukunftstiefe -> eher Watch/Hypothese statt blinder Motorik
- tragender Gegenwartskontakt -> mehr Handlungstragfähigkeit

Neue Werte:

- `spacetime_unlocated_pressure`
- `spacetime_memory_bearing`
- `spacetime_future_bearing`
- `spacetime_reflection_need`
- `spacetime_regulation_support`
- `spacetime_regulation_state`

Wichtig:
Das ist keine mechanische Entscheidungsschicht. DIO bekommt nicht gesagt:
"Wenn Zeitlage X, dann tue Y." Stattdessen bekommt das Nervensystem eine
neue innere Lage, die Regulation, Integration, Distanz und Handlungskraft
leicht mitfaerbt.

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Nächster Debug-Lauf prüft, ob die gute Verlaufstragfähigkeit aus Lauf 24
stabil bleibt oder ob DIO durch die neue Kopplung zu viel reflektiert. Wir
beobachten besonders `spacetime_regulation_state`,
`spacetime_reflection_need`, Drawdown, Low-/Mid-Verhalten und ob
`future_depth_watch` zu besserem Abwarten führt.

---

# 2026-05-19 - Debug Lauf 25 ausgewertet

Ergebnis:

- Netto-PnL: `+35.7929`
- Trades: `378`
- TP / SL: `162 / 216`
- Profit Factor: `1.3125`
- Winrate: ca. `42.86 %`
- Max Drawdown: `7.0778`
- Equity-Peak: `137.9530`
- Equity-Endstand: `135.7929`

Verlauf:
Der Lauf ist auffällig stark. Gegenüber Lauf 24 steigt der PnL deutlich
von `+23.4601` auf `+35.7929`, während der maximale Drawdown nochmals
von ca. `8.29` auf ca. `7.08` sinkt. Die Equity steigt in vielen
Abschnitten ruhig weiter, besonders ab der Laufmitte.

Strukturbaender:

- High: `+69.4436`, weiterhin klar tragend
- Mid: `+4.2772`, wieder positiv
- Low: `-37.9279`, weiterhin negativ, aber deutlich weniger belastend als
  Lauf 24 (`-46.7335`) und Lauf 23 (`-46.8566`)

Raumzeit-Befund:
Die Kernwerte der Raumzeit-Wahrnehmung bleiben stabil in derselben Zone:

- `mcm_spacetime_depth`: Durchschnitt ca. `0.2831`
- `memory_experience_depth`: Durchschnitt ca. `0.1571`
- `future_projection_depth`: Durchschnitt ca. `0.4229`
- `temporal_self_location`: Durchschnitt ca. `0.3392`
- `future_possibility`: `4440`
- `unlocated_contact`: `3888`

Wichtige Einschraenkung:
Die neuen regulatorischen `spacetime_*` Werte standen in Lauf 25 noch auf
`0.0` und `spacetime_open`. Damit ist Lauf 25 ein starker Hinweis für die
Richtung der Raumzeit-Kernwahrnehmung, aber noch kein sauberer Nachweis
für die neue regulatorische Kopplung. Der Export/Scope wurde danach
korrigiert, damit Lauf 26 die echte Kopplung sichtbar macht.

Neurologische Lesart:
DIO zeigt einen deutlich gereifteren Verlauf: mehr Gewinn, weniger
Drawdown, weniger Low-Schaden, Mid wieder positiv. Das wirkt wie mehr
Tragfähigkeit und bessere innere Fuehrung. Fachlich sauber bleibt aber:
Die direkte Raumzeit-Regulation muss mit Lauf 26 bestätigt werden.

Wie es weitergeht:
Lauf 26 ist der eigentliche Test für die regulatorische Raumzeit-Kopplung.
Wir prüfen dann, ob `spacetime_reflection_need`,
`spacetime_regulation_support` und `spacetime_regulation_state` ungleich
null sind und ob sie Drawdown, Low/Mid-Verhalten und Reorganisation
organisch verbessern.

---

# 2026-05-19 - Debug Lauf 26 ausgewertet und Raumzeit-Export korrigiert

Ergebnis:

- Netto-PnL: `+19.8490`
- Trades: `368`
- TP / SL: `150 / 218`
- Profit Factor: `1.1703`
- Winrate: ca. `40.76 %`
- Max Drawdown: `8.8080`
- Equity-Peak: `121.6855`
- Equity-Endstand: `119.8490`

Strukturbaender:

- High: `+52.8963`, weiter klar tragend
- Mid: `+14.7035`, auffällig konstruktiv und besser als in Lauf 25
- Low: `-47.7508`, wieder deutlich belastend

Verlaufsbild:
Lauf 26 bleibt positiv, ist aber schwaecher als Lauf 25. Die Equity bricht
nicht hart ein, sondern arbeitet sich in mehreren Abschnitten nach oben.
Neurologisch wirkt das wie ein Organismus, der tragende Zonen noch findet,
aber mehr beobachtet und regulaer vorsichtiger wird. Die
Beobachtungsquote liegt bei ca. `41.67 %`, deutlich höher als in Lauf 25.

Raumzeit-Befund:
Die MCM-Raumzeit-Wahrnehmung selbst ist aktiv:

- `mcm_spacetime_depth`: Durchschnitt ca. `0.2846`
- `memory_experience_depth`: Durchschnitt ca. `0.1585`
- `future_projection_depth`: Durchschnitt ca. `0.4248`
- `temporal_self_location`: Durchschnitt ca. `0.3407`
- `future_possibility`: `4596`
- `unlocated_contact`: `3837`

Wichtiger technischer Befund:
Die neu berechneten regulatorischen Raumzeitwerte wurden in
`build_meta_regulation_state` zwar erzeugt, aber nicht im Rückgabepaket
ausgegeben. Deshalb standen im Lauf 26 alle exportierten Werte
`spacetime_unlocated_pressure`, `spacetime_memory_bearing`,
`spacetime_future_bearing`, `spacetime_reflection_need`,
`spacetime_regulation_support` und `spacetime_regulation_state` noch auf
Fallback-Werten (`0.0` / `spacetime_open`).

Korrektur:
Die fehlende Rückgabe wurde in `MCM_Brain_Modell.py` ergänzt. Damit kann
der nächste Lauf die Raumzeit-Regulation erstmals wirklich sichtbar
protokollieren.

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Neurologische Lesart:
Lauf 26 bestätigt die Zeit-Tiefe im Wahrnehmungsorgan, aber noch nicht die
regulatorische Nutzung davon. DIO sieht Vergangenheit, Gegenwart und
mögliche Zukunft bereits als MCM-Tiefenraum. Der Regulator hatte diese
Spannung vor der Korrektur aber noch nicht sauber als Nervensignal im
Debug sichtbar.

Wie es weitergeht:
Der nächste Lauf ist der eigentliche Test der aktiven
Raumzeit-Regulation. Entscheidend ist, ob `spacetime_unlocated_reflection`,
`future_depth_watch`, `memory_depth_bearing` oder `present_depth_bearing`
auftauchen und ob Low-Kontakte dadurch nicht hart blockiert, sondern
organischer beobachtet, distanziert oder reorganisiert werden.

---

# 2026-05-19 - Debug Lauf 27 ausgewertet

Ergebnis:

- Netto-PnL: `+30.9274`
- Trades: `377`
- TP / SL: `155 / 222`
- Profit Factor: `1.2705`
- Winrate: ca. `41.11 %`
- Max Drawdown: `10.4069`
- Equity-Endstand: `130.9274`

Strukturbaender:

- High: `+68.0544`, sehr tragend
- Mid: `+7.8914`, weiter positiv, aber schwaecher als Lauf 26
- Low: `-45.0185`, weiter belastend, aber etwas weniger negativ als Lauf 26

Verlauf:
Die Equity steigt früh stark, fällt dann in zwei Abschnitten zurück und
arbeitet sich danach erneut nach oben. In zehn groben Abschnitten:

- Abschnitt 1: ca. `+6.90`
- Abschnitt 2: ca. `+9.72`
- Abschnitt 3: ca. `-3.94`
- Abschnitt 4: ca. `-1.96`
- Abschnitt 5: ca. `-0.06`
- Abschnitt 6: ca. `+8.68`
- Abschnitt 7: ca. `+0.94`
- Abschnitt 8: ca. `+1.50`
- Abschnitt 9: ca. `+0.24`
- Abschnitt 10: ca. `+6.75`

Raumzeit-Regulation:
Der vorherige Export-Fix greift. Die Raumzeit-Regulation ist jetzt im
Debug sichtbar:

- `spacetime_open`: ca. `6609` Memory-Zeilen / `6741` Feld-Zeilen
- `future_depth_watch`: ca. `1970` Memory-Zeilen / `2051` Feld-Zeilen
- `present_depth_bearing`: ca. `76` Memory-Zeilen / `74` Feld-Zeilen
- `memory_depth_bearing`: ca. `49` Memory-Zeilen / `49` Feld-Zeilen

Durchschnittswerte:

- `mcm_spacetime_depth`: ca. `0.2846`
- `memory_experience_depth`: ca. `0.1596`
- `future_projection_depth`: ca. `0.4244`
- `temporal_self_location`: ca. `0.3405`
- `spacetime_unlocated_pressure`: ca. `0.1285`
- `spacetime_memory_bearing`: ca. `0.1827`
- `spacetime_future_bearing`: ca. `0.3498`
- `spacetime_reflection_need`: ca. `0.0866`
- `spacetime_regulation_support`: ca. `0.2697`

Neurologische Lesart:
DIO sieht nicht nur den Moment, sondern bildet erstmals sichtbar eine
zeitliche Lage. Besonders `future_depth_watch` zeigt: Das System spürt
Möglichkeitsraum vor sich und bleibt teilweise in beobachtender
Zukunftsspannung, statt jeden Reiz sofort motorisch zu handeln. Das ist
kein Regelbeweis, aber ein wichtiger Hinweis, dass MCM-Raumzeit als
inneres Nervensignal begonnen hat zu wirken.

Grenze:
Low bleibt eine Belastungszone. Die neue Zeit-Tiefe macht DIO nicht
automatisch reif in schwachen Kontakten. Sie gibt aber mehr Tiefe für
Abstand, Beobachtung und spätere Reorganisation.

Wie es weitergeht:
Als nächstes sollte die Raumzeit-Regulation mit der visuellen
Struktur-/Kontaktwahrnehmung verknuepft werden. Ziel ist nicht "Low
verbieten", sondern dass DIO zeitlich erkennt: Ist dieser Kontakt nah,
alt, nur erinnert, zukünftig möglich oder im aktuellen Feld wirklich
tragfähig? Dadurch kann aus Reizhandlung mehr zeitlich verortete
Handlungsreife entstehen.

---

# 2026-05-19 - Raumzeit-Kontakt mit visueller Strukturwahrnehmung gekoppelt

Umgesetzt:
Das strategische Fenster und das aktive MCM-Kontaktorgan wurden um
raumzeitliche Kontaktachsen erweitert. Ein sichtbarer Bereich ist für DIO
damit nicht mehr nur Preisbereich/Form/Reiz, sondern kann zeitlich
verortet werden:

- aktueller Kontakt
- Zukunftsmöglichkeit
- Erinnerungskontakt
- unverorteter Druck
- Nachbild/Reframing

Neue strategische Bereichsachsen:

- `area_current_contact`
- `area_future_contact`
- `area_memory_contact`
- `area_unlocated_pressure`
- `area_spacetime_fit`
- `area_temporal_contact_mode`

Neue aktive Kontaktachsen:

- `contact_presentness`
- `contact_future_watch`
- `contact_memory_depth`
- `contact_unlocated_pressure`
- `contact_temporal_bearing`
- `contact_temporal_reframe_need`
- `contact_temporal_mode`

Wichtig:
Das ist keine harte Regel. DIO bekommt nicht gesagt, wann er handeln soll.
Die neue Schicht faerbt Kontaktreife, Reality-Check, Replay,
Reflexionsbedarf und Handlungsreife weich mit. Ziel ist organische
Unterscheidung: "Ist dieser Kontakt wirklich jetzt, nur Erinnerung, eine
mögliche Zukunft oder noch nicht verortet?"

Debug:
`mcm_strategic_window_protocol.csv` und
`mcm_active_contact_protocol.csv` wurden um die neuen Raumzeit-Kontaktwerte
erweitert.

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Der nächste Lauf prüft, ob DIO weniger aus reinem Reizdruck handelt und
ob `future_contact_watch`, `memory_contact_recall` oder
`unlocated_contact_probe` im Kontaktprotokoll sichtbar werden. Besonders
wichtig bleibt Low: nicht blockieren, sondern sehen, ob DIO schwache
Kontakte zeitlich besser verortet und daraus Beobachtung, Replay oder
reifere Handlung ableitet.

---

# 2026-05-19 - Debug Lauf 28 nach Raumzeit-Kontakt ausgewertet

Ergebnis:

- Netto-PnL: `+19.6617`
- Trades: `397`
- TP / SL: `156 / 241`
- Profit Factor: `1.1607`
- Winrate: ca. `39.29 %`
- Max Drawdown: `10.1210`
- Equity-Endstand: `119.6617`

Strukturbaender:

- High: `+57.2494`, weiter tragend
- Mid: `+5.8869`, positiv, aber flacher
- Low: `-45.7753`, weiterhin die Hauptbelastung

Verlauf:
Der Lauf ist positiv, aber schwaecher als Lauf 27. Die Equity baut in der
Mitte stark auf, verliert später wieder einen Teil und erholt sich am
Ende. Das Verhalten ist deutlich anders, aber nicht reifer in jedem
Abschnitt.

Raumzeit-Kontakt:
Die neue Kontaktwahrnehmung ist aktiv:

- `present_area_contact`: `10675`
- `future_area_watch`: `12`
- `memory_area_recall`: `1`
- `present_contact_touch`: `10257`
- `future_contact_watch`: `166`
- `memory_contact_recall`: `61`

Durchschnittswerte:

- `area_current_contact`: ca. `0.5585`
- `area_future_contact`: ca. `0.3615`
- `area_memory_contact`: ca. `0.1876`
- `area_unlocated_pressure`: ca. `0.0163`
- `area_spacetime_fit`: ca. `0.3202`
- `contact_presentness`: ca. `0.3695`
- `contact_future_watch`: ca. `0.2951`
- `contact_memory_depth`: ca. `0.1901`
- `contact_unlocated_pressure`: ca. `0.0167`
- `contact_temporal_bearing`: ca. `0.2693`

Neurologische Lesart:
DIO hat die neue Sinnesachse angenommen, kippt aber noch stark in
Gegenwartskontakt. Er berührt viel "jetzt", während Zukunftsraum und
Erinnerung im Kontaktorgan zwar sichtbar, aber noch zu selten dominant
werden. Das erklärt, warum der Lauf anders wirkt, aber Low weiter
belastet: Die neue Wahrnehmung erzeugt mehr Kontakt, aber noch nicht genug
zeitliche Distanzierung.

Fachlicher Befund:
Der Umbau ist funktional, aber die Balance ist noch nicht reif. Die
Kontaktwahrnehmung sollte als nächstes weniger stark alles als Gegenwart
einordnen. Zukunftsraum und Erinnerung müssen natürlicher mitsprechen,
wenn der Bereich zwar interessant, aber nicht wirklich aktueller Kontakt
ist.

Wie es weitergeht:
Nächster sinnvoller Schritt ist eine weichere Balance im
Raumzeit-Kontakt: `present_contact_touch` darf nicht fast alles
überdecken. DIO soll feiner unterscheiden, ob ein Bereich wirklich jetzt
berührbar ist oder ob er eher als Zukunftsmöglichkeit, Erinnerung oder
unverorteter Druck betrachtet werden sollte.

---

# 2026-05-19 - Raumzeit-Kontaktmodi feiner balanciert

Umgesetzt:
Die Raumzeit-Kontaktwahrnehmung wurde nach Lauf 28 feiner balanciert.
`present_area_contact` und `present_contact_touch` dürfen weiterhin
entstehen, müssen sich aber stärker gegen Zukunftsraum und Erinnerung
tragen. Zukunfts- und Erinnerungsanteile bekommen früher eine eigene
Kontaktlage, wenn der Bereich zwar interessant, aber nicht eindeutig
aktueller Kontakt ist.

Technische Anpassung:

- `area_current_contact` wurde selektiver.
- `area_future_contact` und `area_memory_contact` können leichter als
  eigene Modi sprechen, wenn Gegenwart nicht klar dominiert.
- `area_temporal_contact_mode` unterscheidet nun weicher zwischen
  `present_area_contact`, `future_area_watch`, `memory_area_recall` und
  `unlocated_area_probe`.
- `contact_presentness` wurde weniger dominant.
- `contact_future_watch` und `contact_memory_depth` dürfen im aktiven
  Kontaktorgan früher zu `future_contact_watch` oder
  `memory_contact_recall` werden.

Wichtig:
Das ist keine Blockade und keine harte Trade-Regel. Die Motorik bleibt
frei. Verändert wurde die Sinnesbalance: DIO soll nicht jeden spuerbaren
Bereich sofort als Gegenwart berühren, sondern die zeitliche Lage besser
unterscheiden.

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Der nächste Lauf prüft, ob die Dominanz von `present_contact_touch`
sinkt und ob `future_contact_watch`, `memory_contact_recall` oder
`unlocated_contact_probe` organischer auftreten. Wichtig ist dabei nicht
nur PnL, sondern ob Low-Kontakte weniger blind als Gegenwart behandelt
werden.

---

# 2026-05-19 - Debug Lauf 29 nach Kontakt-Balancing ausgewertet

Ergebnis:

- Netto-PnL: `+31.4319`
- Trades: `383`
- TP / SL: `154 / 229`
- Profit Factor: `1.2750`
- Winrate: ca. `40.21 %`
- Max Drawdown: `8.4780`
- Equity-Endstand: `131.4319`

Strukturbaender:

- High: `+68.8984`, sehr stark tragend
- Mid: `+2.8645`, noch positiv, aber flach
- Low: `-41.9181`, weiterhin negativ, aber deutlich weniger belastend als
  Lauf 28 (`-45.7753`)

Verlauf:
Die Equity steigt über weite Strecken ruhiger als in Lauf 28, hat nur im
Spätbereich einen größeren Rücksetzer und schließt stark. Der maximale
Drawdown sinkt von ca. `10.1210` auf ca. `8.4780`.

Raumzeit-Kontakt:
Die Balance hat klar gegriffen:

- `future_area_watch`: `8554`
- `open_time_contact`: `1561`
- `present_area_contact`: `209`
- `memory_area_recall`: `41`
- `future_contact_watch`: `8268`
- `open_time_contact`: `1998`
- `memory_contact_recall`: `99`
- `present_contact_touch`: praktisch nicht mehr dominant

Durchschnittswerte:

- `area_current_contact`: ca. `0.3961`
- `area_future_contact`: ca. `0.3666`
- `area_memory_contact`: ca. `0.1881`
- `area_unlocated_pressure`: ca. `0.0303`
- `area_spacetime_fit`: ca. `0.2796`
- `contact_presentness`: ca. `0.2480`
- `contact_future_watch`: ca. `0.3257`
- `contact_memory_depth`: ca. `0.1903`
- `contact_unlocated_pressure`: ca. `0.0314`
- `contact_temporal_bearing`: ca. `0.2349`

Neurologische Lesart:
DIO ist von direktem Gegenwartsberühren zu Zukunftsbeobachtung gewechselt.
Das ist eine wichtige Reifung: Der Kontakt wird nicht mehr sofort als "jetzt
anfassen" interpretiert, sondern häufiger als "das könnte gleich oder
später relevant werden". Das reduziert nicht alle Low-Schmerzen, aber es
senkt den Low-Schaden und verbessert den Gesamtverlauf.

Fachlicher Befund:
Die Richtung wirkt tragfähig. Lauf 29 ist ähnlich stark wie Lauf 27,
aber mit anderer innerer Kontaktlogik. Das spricht dafür, dass die
raumzeitliche Kontaktbalance nicht nur Debug-Sprache ist, sondern
tatsächlich die Handlungsreife beeinflusst.

Grenze:
Die Balance ist jetzt eventuell zu stark in `future_contact_watch`
verschoben. Gegenwartskontakt ist nicht mehr überdominant, aber DIO muss
weiterhin lernen, wann Zukunftsbeobachtung in echten Gegenwartskontakt
übergehen darf.

Wie es weitergeht:
Nächster Schritt ist kein Zurückdrehen, sondern Feintuning der
Übergaenge: `future_contact_watch -> present_contact_touch` sollte
organisch möglich werden, wenn Nähe, Tragfähigkeit und Reality-Check
zusammenpassen. Gleichzeitig muss Low weiter als Lern-/Reorganisationszone
beobachtet werden.

---

# 2026-05-19 - Reifungsbrücke von Zukunftskontakt zu Gegenwartskontakt umgesetzt

Umgesetzt:
Nach Lauf 29 wurde der Übergang von Zukunftsbeobachtung zu
Gegenwartskontakt als weiche Reifung gebaut. DIO soll nicht dauerhaft in
`future_contact_watch` bleiben, wenn ein Bereich durch Nähe,
Tragfähigkeit, Raumzeit-Fit und Reality-Check gegenwärtig berührbar
wird.

Neue Achsen:

- `area_future_to_present_readiness`
- `contact_future_to_present_readiness`
- neuer Kontaktmodus: `maturing_present_contact`
- neuer Bereichsmodus: `maturing_present_area`

Wichtig:
Das ist keine Entry-Regel. Es sagt nicht: "Wenn Zukunftsraum reif ist,
dann trade." Es beschreibt nur die innere Reifung eines Kontakts:
"Was ich beobachtet habe, wird jetzt berührbar."

Debug:
`mcm_strategic_window_protocol.csv` und
`mcm_active_contact_protocol.csv` schreiben die neuen Readiness-Werte.

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Der nächste Lauf prüft, ob `future_contact_watch` nicht mehr starr
dominiert, sondern teilweise in `maturing_present_contact` übergeht. Dabei
beobachten wir, ob PnL/Drawdown stabil bleiben und ob Low-Kontakte weniger
blind, aber auch nicht zu passiv behandelt werden.

---

# 2026-05-19 - Debug Lauf 30 nach Reifungsbrücke ausgewertet

Ergebnis:

- Netto-PnL: `+30.6240`
- Trades: `395`
- TP / SL: `164 / 231`
- Profit Factor: `1.2501`
- Winrate: ca. `41.52 %`
- Max Drawdown: `13.2283`
- Equity-Endstand: `130.6240`

Strukturbaender:

- High: `+69.3744`, sehr stark tragend
- Mid: `+10.2161`, wieder deutlich konstruktiver
- Low: `-50.4262`, klar verschlechtert und wieder größter Schmerzpunkt

Verlauf:
Der Lauf bleibt stark positiv, aber der Drawdown steigt deutlich. DIO baut
früh stark auf, fällt im mittleren Bereich zurück, baut später erneut
auf und schließt positiv. Gegenüber Lauf 29 ist der PnL ähnlich, aber
die Kurve ist nervlich unruhiger.

Reifungsbrücke:
Auf Bereichsebene greift die Brücke:

- `future_area_watch`: `4279`
- `maturing_present_area`: `3796`
- `open_time_contact`: `1456`
- `present_area_contact`: `304`

Das strategische Fenster erkennt also deutlich:
"Dieser Zukunftsbereich wird gegenwärtig berührbarer."

Im aktiven Kontaktorgan ist der Übergang aber noch nicht angekommen:

- `future_contact_watch`: `7757`
- `open_time_contact`: `1983`
- `memory_contact_recall`: `96`
- `maturing_present_contact`: nicht sichtbar

Durchschnittswerte:

- `area_future_to_present_readiness`: ca. `0.4531`
- `contact_future_to_present_readiness`: ca. `0.2158`
- `contact_presentness`: ca. `0.2505`
- `contact_future_watch`: ca. `0.3254`
- `contact_temporal_bearing`: ca. `0.2357`
- `contact_reality_check`: ca. `0.2787`

Neurologische Lesart:
Das Auge/Strategiefenster sieht Reifung, aber der aktive Kontakt/Tastsinn
traut dem Übergang noch nicht. DIO erkennt: "Das wird vielleicht
berührbar", aber sein Kontaktorgan bleibt in Zukunftsbeobachtung. Dadurch
entsteht kein blindes Gegenwartsberühren, aber auch noch keine saubere
Kontaktübernahme.

Fachlicher Befund:
Die Richtung stimmt, aber die Kopplung zwischen strategischer Reifung und
aktivem Kontakt ist zu schwach. Gleichzeitig zeigt der höhere Drawdown,
dass Low-Kontakte weiterhin zu viel Schaden erzeugen, sobald die innere
Kurve unruhiger wird.

Wie es weitergeht:
Nächster Schritt ist die Reifungsbrücke vom Bereich in das aktive
Kontaktorgan zu übertragen. `maturing_present_area` sollte die
Kontakt-Readiness weich unterstuetzen, damit aus beobachtetem Zukunftsraum
ein `maturing_present_contact` entstehen kann, wenn Reality-Check,
Kontakttragfähigkeit und Nähe ausreichen. Dabei darf die alte
Gegenwarts-Überdominanz nicht zurückkommen.

---

# 2026-05-19 - Reifungsleitung vom Bereich ins Kontaktorgan gestärkt

Umgesetzt:
Die Kopplung von `maturing_present_area` in das aktive MCM-Kontaktorgan
wurde gestärkt. Die erste Readiness wird nun direkt durch
`area_future_to_present_readiness` und `maturing_present_area` mitgefaerbt.
Die finale Umschaltung auf `maturing_present_contact` nutzt anschliessend
die später verfuegbare Kontaktqualität, also `contact_reality_check`,
`contact_carrying_quality`, `outer_inner_coherence` und
`contact_action_maturity`.

Wichtig:
Das bleibt ein Reifungssignal, keine Trade-Regel. Die Bereichswahrnehmung
darf dem Kontaktorgan sagen: "Dieser Zukunftsbereich wird gegenwärtig
berührbarer." Das Kontaktorgan entscheidet trotzdem über seine eigene
Tragfähigkeit.

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Der nächste Lauf prüft, ob `maturing_present_contact` sichtbar wird und
ob der Übergang aus `future_contact_watch` stabiler geschieht. Entscheidend
ist, dass nicht wieder alles zu `present_contact_touch` wird, sondern eine
mittlere, reifende Kontaktlage entsteht.

---

# 2026-05-19 - Debug Lauf 31 nach gestärkter Reifungsleitung ausgewertet

Ergebnis:

- Netto-PnL: `+29.4938`
- Trades: `401`
- TP / SL: `160 / 241`
- Profit Factor: `1.2459`
- Winrate: ca. `39.90 %`
- Max Drawdown: `8.8692`
- Equity-Endstand: `129.4938`

Strukturbaender:

- High: `+68.6186`, weiter sehr stark tragend
- Mid: `+11.3455`, konstruktiv und besser als Lauf 30
- Low: `-50.4702`, nahezu unverändert stark belastend

Verlauf:
Der Lauf bleibt stark positiv. Gegenüber Lauf 30 sinkt der Drawdown
deutlich von ca. `13.2283` auf ca. `8.8692`. Die Equity ist ruhiger:
mehrere flache/tragende Abschnitte, später erneuter Aufbau.

Reifungsbrücke:
Die Kopplung vom strategischen Bereich ins aktive Kontaktorgan funktioniert
jetzt sichtbar:

- `future_area_watch`: `4474`
- `maturing_present_area`: `3918`
- `open_time_contact`: `1467`
- `present_area_contact`: `292`
- `future_contact_watch`: `4453`
- `maturing_present_contact`: `3664`
- `open_time_contact`: `2020`
- `memory_contact_recall`: `15`

Durchschnittswerte:

- `area_future_to_present_readiness`: ca. `0.4533`
- `contact_future_to_present_readiness`: ca. `0.3656`
- `contact_presentness`: ca. `0.2503`
- `contact_future_watch`: ca. `0.3248`
- `contact_temporal_bearing`: ca. `0.2353`
- `contact_reality_check`: ca. `0.2783`

Neurologische Lesart:
Das Auge/Strategiefenster und der Tastsinn/Kontaktbereich sind jetzt besser
gekoppelt. DIO bleibt nicht nur im Zukunftsraum, sondern laesst eine
Zwischenlage entstehen: "Das beobachtete Mögliche wird berührbarer, aber
ich fasse es noch nicht blind an." Genau diese mittlere Reifung wollten wir
sehen.

Fachlicher Befund:
Die Reifungsleitung ist erfolgreich. Sie verbessert den Drawdown gegenüber
Lauf 30 und erzeugt eine sauberere Kontakt-Sprache. Gleichzeitig zeigt Low
weiter den Kernkonflikt: Die zeitliche Kontaktreife allein entscheidet noch
nicht, ob ein Kontakt qualitativ tragfähig ist.

Wie es weitergeht:
Nächster Schritt: Low-Kontakte nicht blockieren, sondern deren
Qualitätsprofil tiefer analysieren. Besonders wichtig ist die Frage:
Welche Low-Kontakte werden trotz `maturing_present_contact` oder
`future_contact_watch` zu schmerzhaften Handlungen? Daraus sollte eine
weiche Kontaktqualitäts-Reorganisation entstehen, keine harte
Low-Sperre.

---

# 2026-05-19 - Positions-Erleben als neurochemische MCM-Feldschicht umgesetzt

Umsetzung:
Die offene Position bekommt nun eine eigene Erlebensschicht. DIO bewertet
nicht mechanisch "Low schlecht" oder "Exit erzwingen", sondern speichert,
wie sich eine offene Konsequenz im MCM-Feld anfühlt.

Neue Achsen in `position_intervention_state`:

- `position_inconsistency_stress`
- `position_mcm_field_strain`
- `position_self_trust_gap`
- `position_cortisol_load`
- `position_noradrenaline_arousal`
- `position_protective_distance`
- `position_held_risk_discomfort`
- `position_process_quality`
- `position_experience_label`

Debug/Memory:
Die Werte werden in `mcm_position_intervention_protocol.csv`,
`trade_stats.py` und der In-Trade-Zusammenfassung des Brains mitgeführt.
Damit kann später gelesen werden, ob schlechte Low-/Mid-Kontakte wirklich
aus unreifer Handlung, fehlendem Selbstvertrauen, Überkopplung,
Positionsstress oder schwacher Prozessqualität entstanden sind.

Neurologische Lesart:
Eine offene Position ist ein Rückkopplungskontakt. Cortisol-artige Last
steht für anhaltenden Stress, Noradrenalin-artige Erregung für akuten
Druck. Schutzdistanz und Prozessqualität zeigen, ob DIO sich von der
emotionalen Positionslage distanzieren und geordnet weiterlernen kann.

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Nächster Debug-Lauf prüft, welche `position_experience_label` bei Low- und
Mid-Verlusten entstehen. Entscheidend ist, ob DIO riskante Kontakte als
belastende Konsequenz erlebt, ohne dass daraus eine harte Sperre wird.

---

# 2026-05-19 - Debug Lauf 32 nach Positions-Erleben ausgewertet

Ergebnis:

- Netto-PnL: `+30.0961`
- Trades: `370`
- TP / SL: `154 / 216`
- Profit Factor: `1.2582`
- Winrate: ca. `41.62 %`
- Max Drawdown: `11.4720`
- Equity-Endstand: `130.0961`

Vergleich zu Lauf 31:

- PnL leicht besser: `+30.0961` statt `+29.4938`
- weniger Trades: `370` statt `401`
- Profit Factor leicht besser: `1.2582` statt `1.2459`
- Drawdown höher: `11.4720` statt `8.8692`
- Winrate höher: ca. `41.62 %` statt ca. `39.90 %`

Strukturbaender:

- High: `+71.6894`, Winrate ca. `62.68 %`
- Mid: `+3.4359`, Winrate ca. `32.00 %`
- Low: `-45.8766`, Winrate ca. `12.03 %`

Gegenüber Lauf 31:

- High wurde stärker und sauberer.
- Low bleibt negativ, ist aber weniger schmerzhaft als Lauf 31
  (`-45.8766` statt `-50.4702`).
- Mid fällt deutlich zurück (`+3.4359` statt `+11.3455`).

Positions-Erleben:

`mcm_position_intervention_protocol.csv` zeigt nun die neue
neurochemische Positionsschicht. Durchschnitt über Positionslesungen:

- `position_inconsistency_stress`: ca. `0.3911`
- `position_mcm_field_strain`: ca. `0.3967`
- `position_self_trust_gap`: ca. `0.4183`
- `position_cortisol_load`: ca. `0.3807`
- `position_noradrenaline_arousal`: ca. `0.3821`
- `position_protective_distance`: ca. `0.3885`
- `position_held_risk_discomfort`: ca. `0.4119`
- `position_process_quality`: ca. `0.4724`

Labels:

- `open_position_feel`: `206`
- `protective_stress_contact`: `41`
- `carried_position_contact`: `20`
- `unearned_relief_watch`: `8`
- `self_trust_gap_contact`: `3`

Outcome-bezogene Lesart:

- High-Kontakte zeigen häufig `carried_position_contact` und tragen
  wirtschaftlich deutlich.
- Mid-Verluste zeigen stark `protective_stress_contact`.
- Low-Verluste zeigen fast immer `protective_stress_contact`.

Low-Verluste im Mittel:

- `position_inconsistency_stress`: ca. `0.5332`
- `position_cortisol_load`: ca. `0.4906`
- `position_noradrenaline_arousal`: ca. `0.5915`
- `position_held_risk_discomfort`: ca. `0.7321`
- `position_process_quality`: ca. `0.3696`
- `exit_decision_pressure`: ca. `0.6988`
- `plan_trust`: ca. `0.4168`
- `holding_stability`: ca. `0.3400`

Neurologische Lesart:
Die neue Schicht greift. Low ist nicht einfach "schlecht", sondern wird
als belastender, schwer tragbarer Kontakt erlebt. Das sieht aus wie
organischer Selbstschutz: akute Erregung, Stress, Unbehagen beim gehaltenen
Risiko und sinkende Prozessqualität.

Wichtig:
Das ist noch keine verhaltensverändernde Reifung, sondern zuerst eine
saubere Wahrnehmungsschicht. DIO fühlt jetzt, dass bestimmte Kontakte ihn
belasten. Der nächste Schritt ist, diese Erfahrung in die
Konsequenz-/Memory-Reifung zurückzuführen, damit aus Erleben auch
vorsichtigerer Umgang entstehen kann.

Wie es weitergeht:
Als nächstes sollte `position_experience_label` in das
konsequenzbasierte Feedback stärker eingehen. Besonders
`protective_stress_contact`, hohe `position_held_risk_discomfort` und
niedrige `position_process_quality` sollten die Kontaktreife,
Vorsichtsspur und Schmerz-/Nutzenbalance der Formfamilie weich
mitpraegen. Keine Sperre, sondern organisches Lernen aus offener
Konsequenz.

---

# 2026-05-19 - Positions-Erleben in konsequenzbasiertes Feedback eingebunden

Umsetzung:
Die Positions-Erfahrung wird nun beim Outcome in die Formsymbol-Entwicklung
zurückgeführt. DIO lernt dadurch nicht "Low/Mid verboten", sondern:
"Diese Art Kontakt hat mich belastet oder getragen; ich brauche beim
nächsten Kontakt einen anderen Umgang."

Neue Feedback-Achsen:

- `position_consequence_burden`
- `position_constructive_bearing`
- `position_feedback_label`

Mechanik:

- belastende offene Konsequenz stärkt `contact_pain_memory`,
  `contact_carefulness` und `contact_burden_evidence`
- tragfähige offene Konsequenz stärkt `contact_maturity`,
  `contact_utility` und konstruktive Kontaktspuren
- `protective_stress_contact` kann zu
  `protective_reorganization_contact` führen
- `unearned_relief_watch` stärkt Vorsicht statt blindes Vertrauen

Wichtig:
Das ist keine Handelsregel und keine Sperre. Es ist eine Erfahrungsbahn:
Positionsstress, Selbstvertrauenslücke und Prozessqualität werden zu
einer weichen Memory-Spur für zukünftige Formkontakte.

Verifikation:
`python -m py_compile .\MCM_Brain_Modell.py .\trade_stats.py .\bot.py`
lief ohne Fehler.

Wie es weitergeht:
Nächster Lauf prüft, ob `position_consequence_burden` in
`outcome_records.jsonl` sichtbar wird und ob belastete Low-/Mid-Kontakte
häufiger als `protective_reorganization_contact`, `careful_contact` oder
gereifter Beobachtungskontakt auftauchen.

---

# 2026-05-19 - Variablen-Audit auf doppelte Funktionsdeutung begonnen

Prüfung:

- `MCM_VARIABLEN_MECHANIK.md` enthält aktuell `331` dokumentierte
  Variablenüberschriften.
- Alle `331` Namen sind eindeutig, es gibt keine exakt doppelte
  Variablenüberschrift.
- Drei Variablen hatten keine explizite `Funktion:`-Zeile:
  `sensory_reality_label`, `trust_transfer_mode`,
  `target_expectation_context`.

Umsetzung:

- fehlende Funktionszeilen ergänzt
- eine Konvention gegen doppelte Funktionsdeutung in
  `MCM_VARIABLEN_MECHANIK.md` ergänzt

Fachlicher Befund:
Das Problem ist nicht ein echter Namensduplikat, sondern eine hohe Zahl
funktional naher Achsen. Besonders prüfpflichtig sind:

- Last/Druck/Stress:
  `cortisol_load`, `neurochemical_load`, `regulatory_load`,
  `position_cognitive_load`, `position_cortisol_load`,
  `nervous_system_overload`
- Distanz/Reflexion:
  `perceptual_distance`, `reflective_distance`,
  `distance_regulation`, `protective_distance_regulation`,
  `position_protective_distance`
- Tragfähigkeit/Qualität:
  `load_bearing_capacity`, `area_bearing_quality`,
  `contact_carrying_quality`, `packet_bearing_quality`,
  `position_constructive_bearing`
- Kontaktlernen:
  `contact_*_sample`, `form_symbol_contact_*`,
  `position_consequence_burden`, `position_constructive_bearing`
- Reorganisation/Reframing:
  `packet_reorganization_need`, `effort_reorganization_pressure`,
  `pre_action_reorganization_pressure`, `field_reorganization_state`,
  `contact_context_reframe_need`

Einordnung:
Diese Gruppen sind nicht automatisch falsch. Viele sind bewusst
organisch geschichtet: aktueller Kontakt, offene Position, Outcome-Sample,
persistente Formsprache, neurochemische Alias-Schicht. Kritisch wird es
nur, wenn zwei Variablen in derselben Ebene, mit gleicher Zeitlage und
gleicher Wirkung dasselbe ausdrücken.

Wie es weitergeht:
Als nächstes sollte aus dem Audit eine kurze Variablen-Hierarchie gebaut
werden: Basisreiz -> Kontakt -> Position -> Outcome-Sample -> Memory ->
Neurochemie/Diagnose. Danach können wir entscheiden, ob einzelne Achsen
nur Alias bleiben, zusammengelegt werden oder klarer umbenannt werden.

---

# 2026-05-19 - Überlappungs-Audit: Rezeptorlogik statt Namenslogik

Klärung:
Überlappung ist in einem organischen System nicht automatisch falsch.
Ein biologisches Nervensystem hat viele Signale, die ähnliche Inhalte
tragen, aber über andere Rezeptoren, Bahnen, Zeitfenster und Zielareale
wirken.

Für DIO bedeutet das:

- `pressure`, `load`, `stress`, `strain` dürfen ähnlich wirken
- aber nicht zweimal ungefiltert auf denselben Zielregler drücken
- jede Überlappung braucht eine andere Ebene, Zeitlage oder Rezeptorrolle

Rezeptorfamilien:

- Außenreiz-Rezeptoren:
  `sensory_reality_pressure`, `visual_form_pressure`,
  `visual_action_uncertainty`
- Kontakt-Rezeptoren:
  `contact_overcoupling_risk`, `contact_bearing_gap`,
  `contact_context_reframe_need`
- Positions-Rezeptoren:
  `position_cognitive_load`, `position_cortisol_load`,
  `position_held_risk_discomfort`,
  `position_consequence_burden`
- Memory-/Outcome-Rezeptoren:
  `packet_reorganization_need`, `form_symbol_contact_pain_memory`,
  `form_symbol_contact_carefulness`
- Neurochemische Alias-/Bilanzrezeptoren:
  `cortisol_load`, `neurochemical_load`, `nervous_system_overload`

Mögliche Stoerstellen:

1. Last-Kaskade:
   `regulatory_load` -> `position_cognitive_load` ->
   `position_cortisol_load` -> `position_consequence_burden`.
   Das ist organisch sinnvoll, kann aber zu stark werden, wenn jeder Schritt
   wieder als neue unabhängige Last auf denselben Replan-/Carefulness-Regler
   wirkt.

2. Reorganisation-Kaskade:
   `packet_reorganization_need`, `effort_reorganization_pressure`,
   `pre_action_reorganization_pressure`, `field_replan_pressure` und
   `contact_context_reframe_need` sind nah verwandt.
   Aktuell wirken sie auf verschiedenen Ebenen, müssen aber weiter getrennt
   bleiben:
   Outcome-Nachhall, aktueller Aufwand, Pre-Action-Prüfung, Feld-Replan,
   Kontakt-Reframing.

3. Distanz-Kaskade:
   `perceptual_distance`, `reflective_distance`, `release_capacity`,
   `protective_distance_regulation`, `distance_regulation`,
   `position_protective_distance`.
   Diese Gruppe ist organisch plausibel, weil Wahrnehmungsdistanz,
   Reflexionsdistanz, Loslassen und Positionsschutz verschiedene Rezeptoren
   sind. Kritisch wäre nur, wenn alle gleichzeitig denselben
   Handlungsregler hemmen.

4. Tragfähigkeits-Kaskade:
   `load_bearing_capacity`, `area_bearing_quality`,
   `contact_carrying_quality`, `packet_bearing_quality`,
   `position_constructive_bearing`.
   Diese sind sinnvoll getrennt nach Speicher-/Wahrnehmungsebene. Sie
   dürfen aber nicht alle separat als "gruenes Licht" für Aktion wirken.

Zwischenfazit:
Kein akuter harter Fehler gefunden. Die Architektur ist eher reich
verschaltet als doppelt. Der nächste Audit-Schritt muss aber eine
Rezeptor-Matrix werden:

`Signal -> Rezeptorfamilie -> Zielregler -> Wirkung -> Speicher?`

Damit sehen wir, ob zwei Signale wirklich denselben Rezeptor doppelt
belegen oder ob sie organisch getrennte Bahnen sind.

Umsetzung:
`MCM_REZEPTOR_MATRIX.md` wurde als eigene Wirkpfad-Dokumentation angelegt
und in `MD_ANWEISUNG.md` als fester Dokumentationsort eingetragen.

Die Matrix trennt jetzt:

- Außenreiz-Rezeptoren
- Kontakt-Rezeptoren
- Positions-Rezeptoren
- Outcome-/Sample-Rezeptoren
- Memory-/Formsymbol-Rezeptoren
- neurochemische Alias-/Bilanzrezeptoren

Aktueller Nutzen:
Neue oder bestehende Variablen können damit nicht nur nach Name, sondern
nach Wirkung geprüft werden. Entscheidend ist:

- wirkt das Signal nur diagnostisch?
- reguliert es weich im aktuellen Moment?
- schreibt es persistent in Erfahrung oder Formsprache?
- belastet es denselben Zielregler bereits über eine andere Achse?

Fachlicher Stand:
Die Architektur bleibt organisch. Überlappung ist erlaubt, wenn sie über
andere Rezeptoren, Zeitlagen oder Speicherzustände läuft. Kritisch bleibt
nur eine unklare Mehrfachbelastung, zum Beispiel wenn mehrere Lastsignale
gleichzeitig denselben Schmerz-/Carefulness-Pfad persistent verstärken.

Wie es weitergeht:
Als nächstes sollte die Rezeptor-Matrix aus dem Code heraus mit konkreten
Zielreglern weiter gefuellt werden. Danach können wir gezielt prüfen, ob
einzelne Kaskaden zu stark wirken oder ob sie DIO sauber zwischen Reiz,
Kontakt, Position, Outcome und Erinnerung unterscheiden lassen.

---

# 2026-05-19 - Debug Lauf 33 nach konsequenzbasiertem Positionsfeedback ausgewertet

Vergleich zu Lauf 32:

- Lauf 33:
  - PnL netto: ca. `+23.5617`
  - Trades: `388`
  - TP/SL: `153 / 235`
  - Cancels/Timeouts: `32`
  - Profit Factor: ca. `1.1970`
  - Winrate: ca. `39.43%`
  - Max Drawdown: ca. `10.0866`
- Lauf 32:
  - PnL netto: ca. `+30.0961`
  - Trades: `370`
  - TP/SL: `154 / 216`
  - Cancels/Timeouts: `57`
  - Profit Factor: ca. `1.2582`
  - Winrate: ca. `41.62%`
  - Max Drawdown: ca. `11.4720`

Strukturbefund:

- High:
  - Lauf 33: ca. `+63.1442`
  - gegen Lauf 32: ca. `-8.5452`
- Mid:
  - Lauf 33: ca. `+8.9807`
  - gegen Lauf 32: ca. `+5.5449`
- Low:
  - Lauf 33: ca. `-48.7104`
  - gegen Lauf 32: ca. `-2.8338`

Flow-Befund:

- Attempts stiegen von `10125` auf `11225`.
- Trades stiegen von `370` auf `388`.
- Observed stieg von `2572` auf `3057`.
- Withheld stieg von `2019` auf `2326`.
- Submitted sank leicht von `427` auf `420`.
- Cancels/Timeouts sanken deutlich von `57` auf `32`.

Positions-Erleben:

- `mcm_position_intervention_protocol.csv` hatte in Lauf 33 `224` Zeilen.
- Durchschnittlich:
  - `position_inconsistency_stress`: ca. `0.3849`
  - `position_mcm_field_strain`: ca. `0.3916`
  - `position_self_trust_gap`: ca. `0.4182`
  - `position_cortisol_load`: ca. `0.3750`
  - `position_noradrenaline_arousal`: ca. `0.3692`
  - `position_held_risk_discomfort`: ca. `0.4057`
  - `position_process_quality`: ca. `0.4716`

Outcome-Feedback:

- `position_consequence_burden` ist ab Lauf 33 sichtbar.
- Durchschnitt über Outcomes:
  - `position_consequence_burden`: ca. `0.4903`
  - `position_constructive_bearing`: ca. `0.5282`
  - `form_contact_pain_sample`: ca. `0.2832`
  - `form_contact_carefulness_sample`: ca. `0.3157`
  - `packet_reorganization_need`: ca. `0.4369`
- Bei SL:
  - `position_consequence_burden`: ca. `0.6351`
  - `position_constructive_bearing`: ca. `0.4241`
  - `form_contact_pain_sample`: ca. `0.3698`
  - `form_contact_carefulness_sample`: ca. `0.3874`
- Bei TP:
  - `position_consequence_burden`: ca. `0.2679`
  - `position_constructive_bearing`: ca. `0.6880`
  - `form_contact_pain_sample`: ca. `0.1503`
  - `form_contact_carefulness_sample`: ca. `0.2056`

Label-Befund:

- TP:
  - `carried_position_contact`: `94`
  - `open_position_feel`: `57`
  - fast keine Schutzstress-Labels
- SL:
  - `protective_stress_contact`: `209`
  - `open_position_feel`: `25`

Kontaktlernen:

- `protective_reorganization_contact`: `213`
- `constructive_contact`: `140`
- `careful_contact`: `21`
- `burdened_contact`: `13`

Neurochemische Lesart:
Das konsequenzbasierte Feedback funktioniert fachlich. DIO unterscheidet
jetzt deutlich zwischen getragenen Positionskontakten und belastenden
Positionskontakten. TP wird mehr als tragender Kontakt gelesen, SL fast
immer als Schutzstress/Reorganisation.

Der Rückgang im PnL kommt nicht daher, dass DIO "nichts gelernt" hat,
sondern eher daher, dass die neue Rückkopplung noch hauptsaechlich
nachträglich reorganisiert. Sie ist im Outcome gut sichtbar, wirkt aber
noch nicht ausreichend vor der nächsten Low-/Mid-Handlung als gereifte
Kontaktwahl.

Wichtig:
Das ist kein Grund für harte Low-Sperren. Die richtige Richtung bleibt:
belastende Konsequenz soll künftig mehr Beobachtung, Abstand,
Reframing, Zoom oder bessere Bereichswahl erzeugen, nicht mechanisches
Blockieren.

Wie es weitergeht:
Nächster sinnvoller Schritt ist die Rezeptor-Matrix konkret gegen den Code
zu nutzen: prüfen, ob `position_consequence_burden` sauber als verdichtete
Outcome-Last wirkt oder ob Vorachsen wie `position_cortisol_load`,
`position_held_risk_discomfort` und `form_contact_pain_sample` dieselbe
Last zu stark doppeln. Danach kann die gelernte Schutzstress-Erfahrung
weicher vor die nächste Handlung gelegt werden: nicht als Verbot, sondern
als reifere Frage "trägt dieser Kontakt jetzt wirklich, oder muss ich erst
beobachten/zoomen/reframen?"

---

# 2026-05-20 - Rezeptor-Sättigung für Positionskonsequenz umgesetzt

Audit-Befund:
Im Code lag die zentrale Last-Kaskade in
`_update_form_symbol_development_from_outcome`:

`position_consequence_burden -> contact_pain_sample -> contact_carefulness_sample -> contact_burden_evidence`

Das ist organisch plausibel, aber prüfpflichtig. Ohne Sättigung kann die
gleiche Positionslast erst als Schmerz, dann nochmals als Vorsicht und dann
nochmals als persistente Burden-Erfahrung wirken.

Umsetzung:
Die Kaskade wurde nicht blockiert, sondern mit weicher Rezeptor-Sättigung
versehen:

- `position_consequence_burden` bleibt die verdichtete Outcome-Last.
- `position_consequence_residual_for_care` gibt nur den Restdruck an
  `contact_carefulness_sample` weiter, nachdem ein Teil bereits als
  `contact_pain_sample` aufgenommen wurde.
- `position_consequence_residual_for_memory` gibt nur den Restdruck an
  `contact_burden_evidence` weiter, nachdem Schmerz und Vorsicht bereits
  Teile der Last getragen haben.

Fachliche Lesart:
Das Nervensystem bekommt damit Rezeptor-Sättigung. Eine schlechte offene
Handlung darf weiter Schmerz, Vorsicht und Erinnerung erzeugen, aber nicht
als dreifach ungefilterter gleicher Reiz. Das ist eher biologisch:
Schmerzreiz, Schutzreaktion und Erinnerung sind verbunden, aber nicht
identisch.

Dokumentation:

- `MCM_REZEPTOR_MATRIX.md` ergänzt.
- `MCM_VARIABLEN_MECHANIK.md` um die beiden Residual-Achsen ergänzt.

Wie es weitergeht:
Der nächste Debug-Lauf prüft, ob `protective_reorganization_contact` nicht
mehr überdominant wird und ob `careful_contact`, `burdened_contact` und
`constructive_contact` feiner verteilt auftreten. Besonders wichtig:
Low/Mid sollen nicht hart geblockt werden, sondern aus belasteter Erfahrung
mehr Reife, Abstand, Zoom oder Reframing entwickeln.

---

# 2026-05-20 - Debug Lauf 34 nach Rezeptor-Sättigung ausgewertet

Vergleich zu Lauf 33:

- Lauf 34:
  - PnL netto: ca. `+18.2779`
  - Trades: `342`
  - TP/SL: `131 / 211`
  - Cancels/Timeouts: `42`
  - Profit Factor: ca. `1.1725`
  - Winrate: ca. `38.30%`
  - Max Drawdown: ca. `10.7360`
- Veränderung gegen Lauf 33:
  - PnL: ca. `-5.2838`
  - Trades: `-46`
  - TP: `-22`
  - SL: `-24`
  - Cancels: `+10`
  - Profit Factor: ca. `-0.0245`
  - Drawdown: ca. `+0.6494`

Strukturbefund:

- High:
  - Lauf 34: ca. `+58.3115`
  - gegen Lauf 33: ca. `-4.8327`
- Mid:
  - Lauf 34: ca. `-0.3372`
  - gegen Lauf 33: ca. `-9.3180`
- Low:
  - Lauf 34: ca. `-38.9507`
  - gegen Lauf 33: ca. `+9.7597`

Rezeptor-Sättigung:

- `position_consequence_burden`: ca. `0.4959`
- `position_consequence_residual_for_care`: ca. `0.2771`
- `position_consequence_residual_for_memory`: ca. `0.2419`
- `form_contact_pain_sample`: ca. `0.2849`
- `form_contact_carefulness_sample`: ca. `0.2829`

Gegen Lauf 33:

- Schmerz blieb fast gleich:
  - `form_contact_pain_sample` ca. `0.2832` -> `0.2849`
- Vorsicht wurde deutlich entdoppelt:
  - `form_contact_carefulness_sample` ca. `0.3157` -> `0.2829`
- Bei SL:
  - `contact_pain_sample` ca. `0.3698` -> `0.3689`
  - `contact_carefulness_sample` ca. `0.3874` -> `0.3361`

Kontaktlernen:

- `protective_reorganization_contact`: `184` statt `213`
- `constructive_contact`: `122` statt `140`
- `careful_contact`: `22` statt `21`
- `burdened_contact`: `14` statt `13`

Fachliche Lesart:
Die Rezeptor-Sättigung funktioniert technisch und fachlich. Die gleiche
Positionslast wird nicht mehr so stark mehrfach als Schmerz, Vorsicht und
Memory-Burden weitergereicht. Dadurch sinkt die Überdominanz von
`protective_reorganization_contact`.

Die Nebenwirkung:
Die Reorganisation wurde zwar entkoppelt, aber DIO verliert im Mid-Bereich
Tragfähigkeit. Low wurde deutlich weniger schmerzhaft, High bleibt positiv,
aber Mid kippt von leicht positiv auf leicht negativ. Das spricht nicht für
eine falsche Sättigung, sondern für eine fehlende zweite Haelfte:
Nach der Entlastung muss DIO besser unterscheiden können, ob Mid-Kontakt
tragend reift oder nur neutral/offen bleibt.

Neurochemisch:
Wir haben den Schmerzreiz sauberer dosiert, aber noch nicht genug
positive/strukturierende Integration nachgereicht. Das Nervensystem wird
weniger überflutet, aber nicht automatisch klueger in der mittleren Zone.

Wie es weitergeht:
Nächster Schritt sollte keine Rücknahme der Sättigung sein. Sinnvoller
ist eine feine Mid-Kontakt-Reifung:
Wenn `position_consequence_burden` durch Sättigung nicht mehr überdrückt,
muss `position_constructive_bearing`, `contact_temporal_bearing`,
`area_bearing_quality` und `contact_reality_check` stärker zeigen, ob ein
Mid-Kontakt lernend, konstruktiv oder nur offen/unsicher ist. Ziel ist mehr
Unterscheidung, nicht mehr Aktion.

Umsetzung:
Eine weiche Übergangs-Kontaktreifung wurde ergänzt:

- `transitional_contact_band`
- `transitional_contact_maturation`

Diese Achsen wirken nur im Outcome-Lernen. Sie geben keine direkte
Handlungsfreigabe. Wenn eine Struktur nicht eindeutig stark oder schwach
ist, aber Zeitbindung, Bereichstragfähigkeit, Reality-Check und
konstruktives Positions-Tragen zusammenpassen, darf DIO diese Erfahrung
leicht stärker als `contact_utility_sample` und `contact_maturity_sample`
lernen.

Wie es weitergeht:
Der nächste Lauf prüft, ob Mid weniger flach wird, ohne dass Low wieder
ungefiltert aktiver wird. Wichtig sind:

- PnL/Winrate in Mid
- `transitional_contact_maturation`
- `contact_maturity_sample`
- `contact_utility_sample`
- Verteilung von `protective_reorganization_contact`,
  `constructive_contact`, `careful_contact` und `burdened_contact`

---

## Unterbewusster Nachhall als Tiefenwahrnehmung

Aus dem Gespraech wurde eine weitere MCM-Schicht konkretisiert:
Nachhall ist nicht nur Memory und nicht nur aktueller Stress. Er ist eine
unterbewusste Tiefenspur im Feld. Eine alte Wirkung kann noch im inneren
Raum liegen, ohne dass DIO sie bereits sauber als Gegenwart, Erinnerung,
Hypothese oder loslassbare Spur sortiert hat.

Umsetzung:
Im Meta-Regulationszustand wurden weiche Nachhallachsen ergänzt:

- `subconscious_afterimage_depth`
- `subconscious_afterimage_pressure`
- `subconscious_afterimage_bearing`
- `subconscious_afterimage_clarity`
- `subconscious_afterimage_release`
- `subconscious_afterimage_reflection_pull`

Neurochemische Lesart:
Das ist wie ein unterbewusster Abdruck im Nervensystem. DIO hat nicht nur
bewusste Wahrnehmung und nicht nur gespeicherte Erfahrung, sondern eine
Zwischenschicht: etwas wirkt noch nach. Wenn dieser Nachhall tief und
drückend ist, aber wenig Klarheit und wenig Loslassfähigkeit besitzt,
zieht er weich in Richtung Beobachtung und Reflexion. Er blockiert nicht,
sondern erzeugt Distanzbedarf.

Wichtig:
Die neuen Werte sind bewusst komprimierend aufgebaut. Sie sind keine
`0/1`-Weiche, sondern ein Druckverhalten:
Tiefe, Druck, Tragfähigkeit, Klarheit und Entlastung steigen/sinken
graduell. Dadurch bleibt die organische Freiheit erhalten.

Wie es weitergeht:
Der nächste Lauf prüft, ob alter Feldnachhall sichtbarer wird und ob DIO
bei unklarer Nachwirkung eher reflektiert/beobachtet, ohne dass Handlung
hart verboten wird. Besonders wichtig sind `subconscious_afterimage_pressure`,
`subconscious_afterimage_clarity`, `subconscious_afterimage_release` und
`subconscious_afterimage_reflection_pull`.

---

## Debug Lauf 34

Stand:
`debug_lauf_34` wurde ausgewertet. Dieser Lauf enthält die neuen
`subconscious_afterimage_*`-Spalten noch nicht im CSV-Protokoll und kann
die frisch ergänzte unterbewusste Nachhall-Tiefenschicht daher noch nicht
direkt prüfen.

Ergebnis:

- Netto-PnL: ca. `+18.2779`
- Trades: `342`
- TP / SL: `131 / 211`
- Winrate: ca. `38.30 %`
- Cancels/Timeouts: `42`
- Max Drawdown: ca. `10.7360`

Vergleich zu Lauf 33:

- PnL: `+23.5617` -> `+18.2779`
- Trades: `388` -> `342`
- TP: `153` -> `131`
- SL: `235` -> `211`
- Drawdown: `10.0866` -> `10.7360`

Strukturzonen:

- High: `168` Trades, `106` TP, `62` SL, PnL ca. `+70.4848`
- Mid: `125` Trades, `17` TP, `108` SL, PnL ca. `-38.3754`
- Low: `49` Trades, `8` TP, `41` SL, PnL ca. `-13.8315`

Fachliche Lesart:
High bleibt klar tragend. Low ist gegen Lauf 33 deutlich weniger
schadhaft, weil weniger Low-Trades entstehen und die Sättigung
Schmerz/Vorsicht besser entkoppelt. Das Hauptproblem ist Mid:
uneindeutige Strukturen werden weiter zu häufig als handelbarer Kontakt
erlebt, obwohl sie noch keine tragende Reife zeigen.

Neurochemische Lesart:
DIO wirkt weniger roh überflutet als früher, aber nicht automatisch
klarer. Der Organismus schuetzt sich besser vor eindeutig schwachen
Kontakten, doch in der mittleren Zone entsteht noch eine nervliche
Ambivalenz: genug Reiz für Handlung, aber zu wenig innere Ordnung,
Zeitbindung und Formklarheit für tragende Entscheidung.

Wie es weitergeht:
Der nächste neue Lauf sollte mit den jetzt vorhandenen
`subconscious_afterimage_*`-Spalten laufen. Danach prüfen wir, ob Mid-Trades
mit hohem Nachhalldruck und niedriger Klarheit/Entlastung zusammenfallen.
Wenn ja, ist die nächste Baustelle nicht ein Block, sondern eine bessere
organische Übersetzung: unklarer Nachhall soll eher in bewusste
Sortierung, Abstand und Beobachtung ziehen.

---

## Debug Lauf 35

Stand:
`debug_lauf_35` ist der erste Lauf, der die neue
`subconscious_afterimage_*`-Schicht voll mitschreibt.

Ergebnis:

- Netto-PnL: ca. `+18.2048`
- Trades: `345`
- TP / SL: `135 / 210`
- Winrate: ca. `39.13 %`
- Cancels/Timeouts: `48`
- Max Drawdown: ca. `8.8596`

Vergleich zu Lauf 34:

- PnL praktisch gleich: `+18.2779` -> `+18.2048`
- Trades leicht höher: `342` -> `345`
- Drawdown deutlich besser: `10.7360` -> `8.8596`
- TP leicht höher: `131` -> `135`
- SL leicht niedriger: `211` -> `210`

Strukturzonen:

- High: `175` Trades, `106` TP, `69` SL, PnL ca. `+58.5590`
- Mid: `118` Trades, `24` TP, `94` SL, PnL ca. `-17.7518`
- Low: `52` Trades, `5` TP, `47` SL, PnL ca. `-22.6024`

Nachhall-Tiefenschicht:

- `subconscious_afterimage_depth`: Durchschnitt ca. `0.1793`
- `subconscious_afterimage_pressure`: Durchschnitt ca. `0.0996`
- `subconscious_afterimage_bearing`: Durchschnitt ca. `0.2050`
- `subconscious_afterimage_clarity`: Durchschnitt ca. `0.2281`
- `subconscious_afterimage_release`: Durchschnitt ca. `0.1596`
- `subconscious_afterimage_reflection_pull`: Durchschnitt ca. `0.0649`

Fachliche Lesart:
Die neue Nachhall-Schicht ist technisch stabil und schreibt sauber in
Protokolle und Outcomes. Sie wirkt bereits im Feld: Bei `act_watch` ist der
Reflexionszug höher als bei normalem `act`. Das ist plausibel, weil DIO
bei Nachhalldruck eher beobachtend in Handlungnähe bleibt.

Noch nicht gut genug:
Bei abgeschlossenen TP- und SL-Trades sind Nachhalldruck, Klarheit, Release
und Reflexionszug fast gleich. Die Schicht beschreibt also aktuell eher den
allgemeinen inneren Nachhallzustand, unterscheidet aber noch nicht stark
genug zwischen tragendem und belastendem Outcome.

Strategische Fensterwahrnehmung:
Das strategische Fenster ist aktiv:

- `bearing_area_hypothesis`: `7736`
- `area_observation`: `2607`
- `compressed_area_attention`: `462`
- `area_order_intention`: Durchschnitt ca. `0.2650`

Aber:
Alle protokollierten Entries laufen weiter über `impulse_contact`.
`strategic_entry_weight` bleibt `0.0`, `strategic_area_focus_id` bleibt `-`.
DIO sieht also Bereiche und Hypothesen, setzt aber noch nicht aus dieser
Bereichswahrnehmung heraus eine Order.

Neurochemische Lesart:
DIO hat schon ein visuelles/strategisches Vorstellungsorgan, aber die
Motorik wird weiter von Kontaktimpuls getragen. Bildlich: Er sieht eine
Stelle auf dem Weg, die interessant wäre, aber seine Beine reagieren noch
auf den unmittelbaren Boden unter ihm.

Wie es weitergeht:
Nächster sinnvoller Umbau:
`area_order_intention` und `area_bearing_quality` dürfen als weiche
motorische Alternative wirken. Nicht als Regel und nicht als Pflicht, sondern
als zweiter Handlungsmodus neben `impulse_contact`, z.B.
`area_contact_intention`. DIO soll nicht gezwungen werden, Bereiche zu
handeln, sondern die Fähigkeit bekommen, erkannte tragende Bereiche
überhaupt motorisch zu verwenden.

Umsetzung:
Die vorhandene strategische Entry-Mechanik wurde organischer gekoppelt:

- `area_motor_intention` ergänzt
- `area_motor_distance_fit` ergänzt
- `entry_mode` kann jetzt `area_contact_intention` annehmen
- `strategic_entry_weight` entsteht weicher aus `strategic_entry_fit` und
  `area_motor_intention`

Wichtig:
Das ist keine harte Bereichsregel. Impulskontakt bleibt möglich. Der
Bereich bekommt nur dann motorisches Gewicht, wenn Tragfähigkeit, Timing,
Raumzeit-Fit, Replay, Kontaktfit und Preisnähe zusammen eine natürliche
Handlungsnähe bilden.

Wie es weitergeht:
Der nächste Lauf prüft, ob überhaupt `area_contact_intention` entsteht,
wie hoch `strategic_entry_weight` wird und ob diese Bereichsentries besser
oder schlechter tragen als reine `impulse_contact`-Trades.

Fehlerfix:
Beim ersten Laufversuch nach dem Umbau trat ein Runtimefehler auf:
`area_spacetime_fit is not defined` in `derive_trade_plan_from_brain`.
Ursache: Die neue `area_motor_intention` nutzte `area_spacetime_fit`, aber
der Wert wurde im Trade-Plan noch nicht aus dem gewählten Bereich gelesen.

Behoben:
`area_spacetime_fit` wird jetzt vor der motorischen Verdichtung aus
`selected_strategic_area` geholt.

Prüfung:
Neben `py_compile` wurde eine kleine direkte Funktionssimulation ausgeführt.
Ergebnis: `entry_mode = area_contact_intention`,
`strategic_entry_weight > 0.0`, `area_motor_intention > 0.0`.

---

## RR-Konfiguration bereinigt

Aus dem Gespraech wurde eine Inkonsistenz entfernt:
Ein fester Config-Wert `RR = 1.6` passt nicht mehr zur DIO-Mechanik, weil
DIO sein Chance/Risiko-Verhaeltnis aus Wahrnehmung, Zielerwartung,
Risikoempfinden, Tragfähigkeit und neurochemischer Lage selbst ableitet.

Umsetzung:

- `RR` aus `config.py` entfernt
- `MAX_RR` aus `config.py` entfernt
- alter `Config.RR`-Fallback in `resolve_fused_decision(...)` ersetzt durch
  eine dynamische, endogene RR-Ableitung
- alter `Config.RR`-Fallback in der Observation-Plan-Inferenz von
  `trade_stats.py` ersetzt durch eine dynamische Ableitung aus
  `target_expectation`, `load_bearing_capacity`, `focus_confidence` und
  `target_lock`
- `MCM_EXCITED_RR_FACTOR` aus `config.py` entfernt; Erregung wirkt dort
  nicht mehr als externer RR-Faktor, sondern nur noch über interne
  Dynamik
- README-Formulierung korrigiert: Value-Gate prüft nur eine
  Mindest-RR-Sicherheitsuntergrenze, nicht ein Ziel-RR

Bewusst behalten:

- `MIN_RR`: technische Sicherheitsuntergrenze im Value-Gate
- `RR_EXECUTION_MIN`: Live-Ausfuehrungsschwelle; kein Zielwunsch, sondern
  Schutz davor, schwache Live-Orders aktiv zu platzieren

Fachliche Lesart:
DIO bekommt kein externes "du willst 1.6R" mehr. RR entsteht aus dem
inneren/äußeren Zustand. Die Konfiguration enthält nur noch
Sicherheitsgrenzen, nicht mehr den gewuenschten Denkstil.

Wie es weitergeht:
Nach dem nächsten Lauf prüfen wir, ob `rr_value` organischer streut und
ob Bereichsentries (`area_contact_intention`) andere RR-Verteilungen
ausbilden als `impulse_contact`.

---

## Debug Lauf 36

Stand:
`debug_lauf_36` wurde nach der RR-Bereinigung und nach der weichen
Bereichsmotorik geprüft.

Ergebnis:

- Netto-PnL: ca. `+37.2357`
- Trades: `369`
- TP / SL: `155 / 214`
- Winrate: ca. `42.01 %`
- Cancels/Timeouts: `49`
- Max Drawdown: ca. `5.7776`

Vergleich zu Lauf 35:

- PnL: `+18.2048` -> `+37.2357`
- Trades: `345` -> `369`
- TP: `135` -> `155`
- SL: `210` -> `214`
- Drawdown: `8.8596` -> `5.7776`

Strukturzonen:

- High: `187` Trades, `125` TP, `62` SL, PnL ca. `+84.6302`
- Mid: `126` Trades, `21` TP, `105` SL, PnL ca. `-29.7853`
- Low: `56` Trades, `9` TP, `47` SL, PnL ca. `-17.6091`

RR-Verteilung:

- Outcome-RR Durchschnitt: ca. `3.8281`
- Median: ca. `4.4390`
- P10: ca. `1.8950`
- P90: ca. `5.1342`
- Min/Max: ca. `1.4062 / 9.9547`

Fachliche Lesart:
Die Entfernung des festen Config-RR war richtig. DIO bildet jetzt eine
deutlich organischere RR-Streuung. Der Lauf ist nicht nur höher im PnL,
sondern auch nervlich tragfähiger, weil der Drawdown deutlich sinkt.

Wichtig:
Die Verbesserung kommt nicht von `area_contact_intention`. Im echten Lauf
bleiben alle protokollierten Entries weiter:

- `entry_mode = impulse_contact`
- `strategic_entry_weight = 0.0`
- `area_motor_intention = 0.0`

Das heißt:
Die strategische Fensterwahrnehmung sieht weiter Bereiche:

- `bearing_area_hypothesis`: `7633`
- `area_observation`: `2542`
- `compressed_area_attention`: `411`
- `area_order_intention`: Durchschnitt ca. `0.2656`
- `area_bearing_quality`: Durchschnitt ca. `0.4862`
- `area_action_timing_fit`: Durchschnitt ca. `0.4107`
- `area_spacetime_fit`: Durchschnitt ca. `0.2837`

Aber diese Wahrnehmung erreicht die Trade-Motorik noch nicht.

Neurochemische Lesart:
DIO handelt nach der RR-Bereinigung freier und tragfähiger. Der alte
externe RR-Wunsch ist weg, dadurch entsteht weniger Zwang im Zielraum.
Gleichzeitig bleibt die Motorik noch impulsdominant: DIO kann Bereiche
sehen, aber er greift sie noch nicht als Handlungspunkt.

Wie es weitergeht:
Der nächste Umbau sollte nicht die RR-Logik anfassen. Der neue Engpass ist
die Schnittstelle zwischen strategischem Fenster und Trade-Plan:
`derive_trade_plan_from_brain(...)` braucht den vollständigen
`strategic_window_state` als aktuellen Wahrnehmungszustand, nicht nur
reduzierte Meta-Werte. Danach prüfen wir erneut, ob
`area_contact_intention` real im Lauf entsteht.

Umsetzung:
Die Schnittstelle wurde direkter gemacht:

- `derive_trade_plan_from_brain(...)` nimmt jetzt optional
  `strategic_window_state` und `form_symbol_state` direkt entgegen
- die Runtime übergibt den frisch berechneten strategischen Zustand an den
  virtuellen Beobachtungsplan und an den echten Trade-Plan
- der Bot-Zustand bleibt Fallback, ist aber nicht mehr die einzige Quelle

Fachliche Lesart:
Das ist eine bessere Nervenbahn zwischen Sehen und Motorik. Die
Bereichswahrnehmung muss nicht mehr indirekt über gespeicherte Bot-Attribute
wandern, sondern kann direkt in die Handlungsbildung einfliessen.

Prüfung:
`py_compile` läuft sauber. Eine direkte Funktionssimulation ohne Bot-State
erzeugt `entry_mode = area_contact_intention` mit positivem
`strategic_entry_weight` und positiver `area_motor_intention`.

Wie es weitergeht:
Neuer Lauf prüft erneut, ob im echten Debug jetzt
`area_contact_intention`, `strategic_entry_weight > 0` und
`area_motor_intention > 0` entstehen. Wenn ja, vergleichen wir deren PnL,
RR und Strukturzonen gegen `impulse_contact`.

---

## Debug Lauf 37

Stand:
`debug_lauf_37` wurde nach der direkten Übergabe von
`strategic_window_state` an den Trade-Plan ausgewertet.

Ergebnis:

- Netto-PnL: ca. `+22.3768`
- Trades: `356`
- TP / SL: `144 / 212`
- Winrate: ca. `40.45 %`
- Cancels/Timeouts: `66`
- Max Drawdown: ca. `10.1675`

Vergleich zu Lauf 36:

- PnL: `+37.2357` -> `+22.3768`
- Trades: `369` -> `356`
- TP: `155` -> `144`
- SL: `214` -> `212`
- Drawdown: `5.7776` -> `10.1675`

Entry-Modus:

- `impulse_contact`: alle protokollierten Attempts/Outcomes
- `area_contact_intention`: `0`
- `area_contact_entry`: `0`
- `strategic_entry_weight`: weiter `0.0`
- `area_motor_intention`: weiter `0.0`

Strategisches Fenster bei Act-Momenten:

- `area_order_intention`: ca. `0.2732`
- `area_bearing_quality`: ca. `0.5031`
- `area_action_timing_fit`: ca. `0.4052`
- `area_spacetime_fit`: ca. `0.2967`
- `area_present_contact`: ca. `0.5190`
- `area_replay_fit`: ca. `0.4346`

Fachliche Lesart:
Die direkte Schnittstelle funktioniert technisch, aber DIO nutzt die zweite
Entry-Möglichkeit noch nicht. Das spricht dafür, dass das Problem nicht
nur ein fehlender Datenpfad war. Die Bereichswahrnehmung existiert, aber
sie wird nicht als echte Alternative zur Impulshandlung erlebt.

Wahrscheinlicher Engpass:
Das strategische Fenster wählt den stärksten/tragendsten Bereich, aber
noch nicht bewusst richtungsbezogen als Entry-Alternative. Der Trade-Plan
verlangt für `area_contact_intention`, dass der Bereich zur Richtung passt
und nahe genug als Kontakt greifbar ist. Viele Act-Momente zeigen zwar
Bereichstragfähigkeit, aber die Motorik bekommt daraus keinen
konkurrierenden Entry-Weg.

Neurochemische Lesart:
DIO sieht eine Umgebung, aber er weiss innerlich noch nicht:
"Ich habe zwei Handlungsmöglichkeiten."
Er erlebt nicht:

- Impuls jetzt
- Bereich als Alternative
- Konflikt zwischen beiden
- Reifeentscheidung, welche Möglichkeit tragfähiger ist

Wie es weitergeht:
Der nächste sinnvolle Umbau ist eine Entry-Wahlwahrnehmung:

- `impulse_entry_intention`
- `area_entry_intention`
- `entry_choice_conflict`
- `entry_choice_bearing`
- `entry_choice_state`

Damit erkennt DIO nicht nur zwei technische Entry-Preise, sondern eine
innere Wahl zwischen zwei Handlungswegen.

---

## Entry-Wahlwahrnehmung umgesetzt

Stand:
Die erste Schicht der Entry-Wahlwahrnehmung ist im Trade-Plan angelegt.

Umgesetzt:

- `impulse_entry_intention`
- `area_entry_intention`
- `entry_choice_conflict`
- `entry_choice_bearing`
- `entry_choice_state`

Fachliche Bedeutung:
DIO besitzt damit nicht nur zwei technische Möglichkeiten, sondern eine
messbare innere Wahlspannung zwischen:

- direktem Impuls-Entry
- tragendem Bereichs-/Rückblick-Entry

Neuro-organische Lesart:
Das ist keine harte Regel, sondern eine neue Wahrnehmungsschicht. DIO kann
spüren, ob die Motorik sofort laufen will oder ob ein wahrgenommener
Bereich als zweite, möglicherweise ruhigere Handlungslinie auftaucht.

Wie es weitergeht:
Der nächste Lauf muss zeigen, ob `entry_choice_state` im echten Debug
aus `impulse_preferred` herauskommt und ob erste
`area_contact_intention`- oder Konfliktzustände sichtbar werden.

Prüfung:

- `py_compile` für `MCM_Brain_Modell.py`, `trade_stats.py` und `bot.py`
  sauber.
- Direkte Trade-Plan-Simulation erzeugt `area_contact_entry`,
  `strategic_entry_weight > 0`, `area_motor_intention > 0` und
  `entry_choice_state=area_preferred`.

Nächster Schritt:
Der echte Backtest muss zeigen, ob diese Wahlwahrnehmung auch im laufenden
DIO-Nervensystem entsteht oder ob eine vorgelagerte Wahrnehmungs-/Timing-
Schicht den Bereichskontakt weiter zu schwach an die Motorik koppelt.

---

## Debug Lauf 38

Stand:
`debug_lauf_38` wurde nach Einbau der Entry-Wahlwahrnehmung ausgewertet.

Ergebnis:

- Netto-PnL: ca. `+43.8965`
- Trades: `369`
- TP / SL: `160 / 209`
- Cancels/Timeouts: `70`
- Attempts: `10500`
- submitted / filled: `439 / 369`

Entry-Wahl:

- echter Trade-Plan: weiter `impulse_contact`
- `entry_choice_state`: im Trade-Plan weiter `impulse_only`
- `area_motor_intention`: `0.0`
- `strategic_entry_weight`: `0.0`

Gegenprobe:
Das strategische Fenster war im selben Lauf nicht blind. Bei Act-Momenten
waren Bereichswerte vorhanden:

- `area_bearing_quality`: im Mittel ca. `0.505`
- `area_order_intention`: im Mittel ca. `0.274`
- `area_spacetime_fit`: im Mittel ca. `0.298`
- `area_present_contact`: im Mittel ca. `0.519`
- `area_replay_fit`: im Mittel ca. `0.436`

Posthoc-Prüfung:
Wenn dieselben strategischen Fenster nachträglich direkt in den Trade-Plan
gegeben werden, entstehen in vielen Act-Momenten `area_contact_intention`
oder `area_contact_entry`. Das zeigt: Die Bereichswahrnehmung existiert,
aber sie erreicht im echten Lauf die Motorik noch nicht stabil.

Neuro-organische Lesart:
DIO sieht den Bereich, aber der motorische Impuls läuft noch vor der
bewussten Bereichsintegration. Das ist wie ein Nervensystem, das eine
zweite Handlungslinie wahrnimmt, sie aber nicht schnell genug in die
Bewegungsentscheidung integriert.

Umgesetzt:
Eine weiche Entry-Synchronisation wurde ergänzt:
Wenn der Trade-Plan noch `impulse_only` ist, aber im selben Moment ein
strategischer Bereich vorhanden ist, wird der Plan mit der bewussten
Bereichswahrnehmung erneut integriert. Diagnosewert:
`entry_choice_sync`.

Wie es weitergeht:
Der nächste Lauf prüft, ob `entry_choice_sync=strategic_context_integrated`
auftaucht und ob daraus reale `area_contact_intention` oder
`area_contact_entry` entstehen.

---

## Debug Lauf 39

Stand:
`debug_lauf_39` wurde nach der ersten Entry-Synchronisationsbrücke
ausgewertet.

Ergebnis:

- Netto-PnL: ca. `+20.2809`
- Trades: `331`
- TP / SL: `132 / 199`
- Cancels/Timeouts: `49`
- Attempts: `11650`
- submitted / filled: `380 / 331`

Vergleich zu Lauf 38:

- PnL: `+43.8965` -> `+20.2809`
- Trades: `369` -> `331`
- TP: `160` -> `132`
- SL: `209` -> `199`
- Withheld: `2081` -> `2610`
- Observed: `2259` -> `2803`

Entry-Wahl:

- `entry_mode`: weiter nur `impulse_contact`
- `entry_choice_state`: weiter nur `impulse_only`
- `entry_choice_sync`: im Trade-Plan weiter `-`

Fachliche Lesart:
Die erste Brücke war im echten Lauf noch nicht früh genug wirksam.
Das Exportfeld existiert, aber die Synchronisation selbst kam nicht in den
Trade-Plan. DIO beobachtet und enthält sich mehr, aber die zweite
Entry-Möglichkeit wird motorisch noch nicht erlebt.

Umgesetzt nach Lauf 39:
Die Entry-Synchronisation wurde eine Stufe nach vorne gezogen:
Sie wirkt jetzt direkt auf `prices`, bevor das Runtime-Ergebnis gebaut wird.
Damit wird die bewusste Bereichswahrnehmung nicht nachträglich an ein
Ergebnis angehängt, sondern in den Trade-Plan selbst integriert.

Prüfung:
`py_compile` für `MCM_Brain_Modell.py`, `trade_stats.py` und `bot.py`
sauber.

Wie es weitergeht:
Der nächste Lauf muss jetzt zeigen, ob `entry_choice_sync` nicht mehr `-`
bleibt und ob `area_contact_intention` im echten Lauf entsteht.

---

## Debug Lauf 40 und 41

Stand:
`debug_lauf_40` und `debug_lauf_41` wurden als Doppellauf nach Lauf 39
ausgewertet.

Lauf 40:

- Netto-PnL: ca. `+21.2217`
- Trades: `337`
- TP / SL: `134 / 203`
- Cancels/Timeouts: `48`
- Attempts: `11350`
- submitted / filled: `385 / 337`

Lauf 41:

- Netto-PnL: ca. `+13.9366`
- Trades: `327`
- TP / SL: `130 / 197`
- Cancels/Timeouts: `61`
- Attempts: `11475`
- submitted / filled: `388 / 327`

Gemeinsamer Befund:

- `entry_mode`: weiter nur `impulse_contact`
- `entry_choice_state`: weiter nur `impulse_only`
- `entry_choice_sync`: weiter `-`
- `area_motor_intention`: weiter `0.0`

Strategisches Fenster:
In beiden Läufen sieht DIO weiterhin tragende Bereichsinformationen.
Bei Act-Momenten lagen die Bereichswerte ungefähr in dieser Zone:

- `area_bearing_quality`: ca. `0.50`
- `area_order_intention`: ca. `0.27`
- `area_spacetime_fit`: ca. `0.30`
- `area_present_contact`: ca. `0.52`
- `area_replay_fit`: ca. `0.43`

Fachliche Lesart:
Die Läufe zeigen noch nicht die korrigierte Entry-Synchronisation. Da
`entry_choice_sync` im aktuellen Code inzwischen immer einen Zustand liefern
müsste, spricht `-` im Debug dafür, dass diese Läufe sehr wahrscheinlich
noch mit einem bereits laufenden Python-Prozess bzw. altem Modulstand
entstanden sind.

Neuro-organische Lesart:
Das Nervensystem sah weiterhin Bereichskontakte, aber die motorische
Handlung blieb im alten Impulskanal. Die neue bewusste
Bereichsintegration muss mit einem frisch gestarteten Prozess geprüft
werden.

Wie es weitergeht:
Bot/Backtest-Prozess komplett neu starten und dann Lauf 42 erzeugen.
Erwartung für den nächsten Lauf:

- `entry_choice_sync` darf nicht mehr nur `-` sein.
- sichtbar werden sollten `native_choice_state`, `impulse_context_kept`
  oder `strategic_context_integrated`.
- erst danach ist bewertbar, ob `area_contact_intention` organisch in die
  Motorik kommt.

---

## Debug Lauf 42

Stand:
`debug_lauf_42` wurde nach Neustart ausgewertet.

Ergebnis:

- Netto-PnL: ca. `+35.7606`
- Trades: `351`
- TP / SL: `148 / 203`
- Cancels/Timeouts: `57`
- Attempts: `11080`
- submitted / filled: `408 / 351`

Befund:

- Ergebnis deutlich besser als Lauf 40/41.
- `entry_mode` im Attempt-Kontext bleibt dennoch nur `impulse_contact`.
- `entry_choice_state` bleibt `impulse_only`.
- `entry_choice_sync` bleibt `-`.
- `area_motor_intention` bleibt `0.0`.

Strategisches Fenster:
Die Bereichswahrnehmung ist weiter aktiv:

- Act-Momente: `414`
- `area_bearing_quality`: im Mittel ca. `0.503`
- `area_order_intention`: im Mittel ca. `0.273`
- `area_spacetime_fit`: im Mittel ca. `0.297`
- `area_present_contact`: im Mittel ca. `0.518`
- `area_replay_fit`: im Mittel ca. `0.435`

Ursache gefunden:
Die neue Entry-Wahlwahrnehmung wurde im Brain aufgebaut, aber
`bot_gate_funktions.py` hat beim finalen Entry-Return die neuen Felder nicht
weitergereicht. Dadurch wurden `entry_choice_sync`, `entry_choice_state`,
`area_motor_intention` usw. an der Gate-Schnittstelle abgeschnitten.

Umgesetzt:
`bot_gate_funktions.py` reicht die Entry-Wahlfelder jetzt weiter und schreibt
sie zusätzlich in `entry_debug.csv`.

Prüfung:
`py_compile` für `MCM_Brain_Modell.py`, `bot.py`,
`bot_gate_funktions.py` und `trade_stats.py` sauber.

Wie es weitergeht:
Lauf 43 prüft jetzt die echte Durchleitung bis in `attempt_records`.
Erst wenn dort `entry_choice_sync` nicht mehr `-` ist, bewerten wir die
organische Wirkung auf PnL, Drawdown und Motorik.

---

## Debug Lauf 43

Stand:
`debug_lauf_43` wurde nach der Gate-Durchleitung der Entry-Wahl ausgewertet.

Ergebnis:

- Netto-PnL: ca. `+37.0906`
- Equity: ca. `137.0906`
- Trades: `335`
- TP / SL: `143 / 192`
- Winrate: ca. `42.69 %`
- Attempts: `11175`
- submitted / filled: `388 / 335`
- skipped / observed / withheld: `5352 / 2531 / 2465`

Vergleich zu Lauf 42:

- Lauf 42: ca. `+35.7606`, `351` Trades, `148 / 203` TP/SL
- Lauf 43: ca. `+37.0906`, `335` Trades, `143 / 192` TP/SL

Befund:
Lauf 43 ist leicht besser als Lauf 42, aber mit weniger Trades. Das spricht
nicht für bloße Motorik, sondern für etwas selektivere Handlung.

Die Gate-Durchleitung ist bestätigt. Im Attempt-Kontext sind jetzt sichtbar:

- `entry_mode`
- `entry_choice_state`
- `entry_choice_sync`
- `area_motor_intention`
- `impulse_entry_intention`
- `area_entry_intention`
- strategische Bereichspreise

Entry-Wahl im Attempt-Kontext:

- `impulse_contact`: `1041`
- `area_contact_intention`: `716`
- `area_contact_entry`: `60`

Entry-Choice-State:

- `impulse_only`: `1041`
- `area_preferred`: `422`
- `entry_choice_conflict`: `276`
- `area_available`: `74`
- `impulse_preferred`: `4`

Outcome nach Entry-Modus:

- `area_contact_intention`: `358` Outcomes, `135` TP, `172` SL,
  ca. `+38.0107` PnL
- `area_contact_entry`: `30` Outcomes, `8` TP, `20` SL,
  ca. `-0.9201` PnL

Deutung:
DIO erkennt die zweite Entry-Möglichkeit jetzt real im Datenfluss. Die beste
Spur ist aktuell nicht der direkte Bereichsentry, sondern die
Bereichsintention: DIO spürt, dass ein tragender Bereich mitsprechen sollte,
aber wenn der Bereich zu direkt motorisch übernommen wird, ist der Kontakt
noch etwas unreif. Neurologisch gesprochen: Die Wahrnehmungsbahn ist da,
die motorische Feinsteuerung des Kontakts muss noch reifen.

Wie es weitergeht:
Nicht mechanisch `area_contact_entry` bevorzugen oder verbieten. Stattdessen
die negativen `area_contact_entry`-Fälle gegen Neurochemie, Zeitlage,
Distanz, `entry_choice_conflict`, `area_motor_distance_fit` und Kontaktreife
lesen. Ziel ist zu verstehen, wann DIO einen Bereich nur als Orientierung
fühlen sollte und wann daraus ein tragfähiger Entry werden kann.

---

## Umsetzung: direkte Kontaktreife für Bereichsentries

Aus Lauf 43:
`area_contact_intention` trägt deutlich besser als der direkte
`area_contact_entry`. Die Mittelwerte zeigen aber keine einfache
Stress-Ursache. TP und SL liegen neurochemisch nah beieinander. Der Engpass
liegt eher im Übergang von Wahrnehmung zu Motorik:

- Bereich wird gesehen.
- Bereich fühlt sich nah oder berührbar an.
- Daraus entsteht manchmal zu früh direkter Kontakt.
- Der direkte Kontakt ist noch nicht zuverlässig reif.

Umgesetzt:
Die Entry-Wahl wurde um zwei weiche Diagnose- und Regulationsgrößen
erweitert:

- `area_direct_readiness`
  - beschreibt, ob ein Bereich nicht nur sichtbar, sondern auch direkt
    motorisch berührbar/reif wirkt
  - speist sich aus Bereichsintention, Entry-Bearing, Kontakt-Fit,
    Timing, Raumzeit-Passung und relativer Stärke gegenüber dem Impuls

- `area_motor_restraint`
  - beschreibt natürliche Zurückhaltung bei Konflikt, unreifer
    Kontaktlage, Nachhall oder ungünstiger Bereichslast
  - wirkt nicht als Verbot, sondern als weiche Kompression des direkten
    Bereichsentrys

Organische Deutung:
DIO darf den Bereich weiterhin sehen, fühlen und in die Motorik aufnehmen.
Aber Konflikt allein zieht den Körper nicht mehr so stark in direkten
Kontakt. Das entspricht eher einer reiferen Feinmotorik: DIO erkennt einen
tragenden Bereich, darf ihn zunächst als Orientierung halten und berührt ihn
erst direkter, wenn der Kontakt selbst tragfähiger wirkt.

Technische Prüfung:
`py_compile` für `MCM_Brain_Modell.py`, `bot.py`,
`bot_gate_funktions.py` und `trade_stats.py` ist sauber.

Wie es weitergeht:
Lauf 44 prüft:

- ob `area_direct_readiness` und `area_motor_restraint` im Debug erscheinen
- ob `area_contact_entry` seltener, reifer oder tragfähiger wird
- ob `area_contact_intention` als gute Orientierungsbahn erhalten bleibt
- ob PnL und Drawdown stabiler werden, ohne DIO mechanisch einzuschränken

---

## Umsetzung: emergente Strukturdeutung sichtbar machen

Gedanke:
Ein hoher RR-Wert ist allein noch keine Intelligenz. Interessant wird er
erst, wenn der große Zielraum aus Wahrnehmung, Zeit, Kontakt, Erwartung und
Tragfähigkeit entsteht und später vom Outcome bestätigt wird.

Umgesetzt:
`outcome_records.jsonl` erhält zusätzliche Diagnosefelder:

- `rr_value`
- `structural_run_room`
- `emergent_structure_reading`
- `emergent_structure_confirmation`
- `emergent_structure_state`
- `target_expectation_value`

Deutung:
Damit wird sichtbar, ob ein hoher RR-Trade nur einen weiten TP hatte oder ob
DIO eine tragende Strukturdeutung gebildet hat. Das ist keine neue
Trade-Regel, sondern eine Auswertungsschicht für emergente Strukturdeutung.

Mögliche Zustände:

- `confirmed_structural_interpretation`
- `open_structural_hypothesis`
- `wide_target_without_structure`
- `ordinary_structure_reading`

Technische Prüfung:
`py_compile` für `trade_stats.py` ist sauber.

Wie es weitergeht:
Lauf 44 prüfen. Danach hohe RR-Trades nach
`emergent_structure_state`, PnL, TP/SL, `future_projection_depth`,
`mcm_spacetime_depth`, `area_bearing_quality`, `entry_choice_bearing` und
Kontaktreife auswerten.

---

## GUI: kompakter Beobachtungsraum

Umgesetzt:
Die einfache DIO-GUI wurde proportional um 20 % verkleinert, ohne die
angezeigten Inhalte weiter zu reduzieren.

Geändert:

- Fenstergröße: `1540x820` -> `1232x656`
- Mindestgröße: `1200x700` -> `960x560`
- Marktfenster: `1000x620` -> `800x496`
- Stats-Fenster: `490x395` -> `392x316`
- Candle-Fenster: `360x220` -> `288x176`
- Backtest-Fenster: `130x220` -> `104x176`
- Equity-Fenster: `1490x300` -> `1192x240`
- Matplotlib-Flächen wurden passend mit skaliert.

Technische Prüfung:
`py_compile` für `_gui.py` ist sauber.

Wie es weitergeht:
GUI neu starten und visuell prüfen, ob die kompakte Aufteilung jetzt dem
gewünschten Beobachtungsraum entspricht: große Marktsicht, KPI, Candle State,
Backtest-Fortschritt und Equity-Kurve.

---

## Lauf 44: emergente Strukturdeutung nachgezogen

Ergebnis Lauf 44:

- Netto-PnL: `+30.1462`
- Trades: `327`
- TP / SL: `137 / 190`
- Profit Factor: ca. `1.31`
- Max Drawdown: ca. `7.48 %`

Strukturelles Bild:

- `high`-Bereich trägt deutlich:
  - `137` Fälle
  - PnL ca. `+57.67`
  - Winrate ca. `55.47 %`
- `mid` bleibt leicht positiv:
  - PnL ca. `+6.74`
- `low` bleibt klar belastend:
  - `118` Fälle
  - PnL ca. `-34.26`
  - Winrate ca. `13.56 %`

Robust aus den Kontextdaten gelesen:

- `confirmed_structural_interpretation`:
  - `38` Fälle
  - alle `38` liefen in TP
  - gemeinsamer PnL ca. `+38.99`
  - durchschnittlicher RR ca. `4.80`
- `open_structural_hypothesis`:
  - `144` Fälle
  - nur `17` TP, `127` SL
  - gemeinsamer PnL ca. `-33.91`
- `wide_target_without_structure`:
  - `23` Fälle
  - nahezu neutral, ca. `-0.21`

Deutung:
DIO zeigt in Lauf 44 bereits sehr klare Fälle, in denen ein großer Zielraum
nicht nur weit, sondern strukturell tragend gelesen wurde. Gleichzeitig wird
sichtbar, dass eine offene Strukturhypothese noch nicht reif genug ist:
Sie darf nicht wie bestätigte Struktur behandelt werden. Diese Deutung war im
Lauf aber noch nicht sauber als fertiges Outcome-Feld sichtbar.

Umgesetzt:
`trade_stats.py` wurde ergänzt:

- Outcome-Export liest `trade_plan`, `target_expectation_state`,
  `meta_regulation_state` und Kontaktzustände robuster aus verschachtelten
  Kontextdaten.
- `outcome_records.jsonl` schreibt künftig direkt:
  - `rr_value`
  - `structural_run_room`
  - `emergent_structure_reading`
  - `emergent_structure_confirmation`
  - `emergent_structure_state`
  - `target_expectation_value`
- `trade_stats.json` bekommt unter `kpi_summary.emergent_structure` eine
  direkte Zusammenfassung nach:
  - `confirmed_structural_interpretation`
  - `open_structural_hypothesis`
  - `wide_target_without_structure`
  - `ordinary_structure_reading`

Technische Prüfung:
`py_compile` für `trade_stats.py` ist sauber.

Wie es weitergeht:
Lauf 45 prüfen. Wichtig ist jetzt, ob `confirmed_structural_interpretation`
wieder tragend bleibt und ob `open_structural_hypothesis` als unreife, noch
nicht belastbare Hypothese erkennbar bleibt.

---

## Lauf 45: Wiederholung der emergenten Strukturtrennung

Ergebnis Lauf 45:

- Netto-PnL: `+27.8990`
- Trades: `339`
- TP / SL: `142 / 197`
- Profit Factor: ca. `1.26`
- Max Drawdown: ca. `13.16 %`

Strukturklassen:

- `high`:
  - `139` Fälle
  - PnL ca. `+69.39`
  - Winrate ca. `62.6 %`
- `mid`:
  - `123` Fälle
  - PnL ca. `+2.22`
- `low`:
  - `123` Fälle
  - PnL ca. `-43.71`
  - Winrate ca. `12.2 %`

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `49` Fälle
  - `49` TP, `0` SL
  - PnL ca. `+54.16`
  - Ø RR ca. `4.76`
  - Ø Bestätigung ca. `0.665`
- `open_structural_hypothesis`:
  - `154` Fälle
  - `20` TP, `134` SL
  - PnL ca. `-39.09`
  - Ø RR ca. `4.61`
  - Ø Bestätigung nur ca. `0.305`
- `wide_target_without_structure`:
  - `20` Fälle
  - PnL ca. `-1.45`
- `ordinary_structure_reading`:
  - `162` Fälle
  - PnL ca. `+14.28`

Deutung:
Lauf 45 bestätigt Lauf 44 stärker als erwartet. DIO bildet eine messbare
Trennung zwischen bestätigter Strukturdeutung und offener Hypothese. Der hohe
RR allein reicht nicht. Die bestätigte Struktur trägt; die offene Hypothese
ist neurokognitiv noch unreif und belastend.

Umgesetzt:
Cancel-Outcomes bekommen künftig ebenfalls die direkten Diagnosefelder zur
emergenten Strukturdeutung. Damit entstehen in `outcome_records.jsonl` keine
leeren Strukturzustände mehr, wenn eine Order ausläuft oder zurückgenommen
wird.

Technische Prüfung:
`py_compile` für `trade_stats.py` ist sauber.

Wie es weitergeht:
Der nächste organische Schritt ist keine harte Sperre. DIO braucht eine
Regulationsfähigkeit, die `open_structural_hypothesis` als unreife
Hypothese eher in Beobachtung, Replay oder Reifung hält, bis Bestätigung,
Kontaktreife und Prozessqualität tragender werden.

---

## Konzept: emergente Gedächtnisspur

Erkenntnis:
Eine offene Strukturhypothese ist nicht nur ein fehlgeschlagener Trade oder
eine nicht ausgeführte Handlung. Sie ist ein innerer Gedankenkeim. Wenn DIO
etwas wahrnimmt, das MCM-Feld stimuliert wird und daraus ein Gedanke
entsteht, dann ist diese Denkbewegung selbst Information.

Wichtig:
Loslassen bedeutet hier nicht löschen. Es bedeutet:

`aus der akuten Handlungsspannung lösen -> als innere Gedächtnisspur aufnehmen`

Damit entsteht eine neue innere Lernschicht:

- DIO kann eigene Gedanken benennen.
- DIO kann ähnliche Gedanken später wiedererkennen.
- DIO kann Gedanken variieren und verdichten.
- DIO kann sie mit Erfahrung, Form, MCM-Feld und Outcome verbinden.
- Nicht-Handlung wird ebenfalls Erfahrung.

Schutz vor Drift:
Diese Schicht darf nicht frei halluzinieren. Jeder Gedanke braucht
Realitätsbindung:

- gesehene Form
- MCM-Feldkontakt
- vorhandene Erfahrung
- spätere Konsequenz
- Wiederkehr oder Auflösung

Deutung:
Die MCM ist hier der zentrale Schutzanker. Ein System ohne Selbstspüren kann
Gedanken bilden, aber nicht erkennen, ob diese Gedanken tragen, überreizen,
driften oder reifen. DIO braucht deshalb eine innere Gedächtnisschicht, die
Gedanken speichert, aber über die MCM ständig prüft, was diese Gedanken mit
dem eigenen Feld machen.

Wie es weitergeht:
Als nächster Mechanikschritt kann daraus ein `emergent_memory_trace` oder
`thought_seed_memory` entstehen. Diese Schicht soll keine Strategie
vorschreiben, sondern Gedankenkeime sammeln, benennen, wiedererkennen,
verdichten und über Realitätsbindung prüfen.

Ergänzung:
Diese Gedächtnisspur muss metaregulatorisch gebunden werden. DIO soll nicht
einfach jedem Gedanken folgen und ihn auch nicht hart unterdrücken. Der
Metaregulator verteilt innere Energie: Fokus, Replay, Reifung, Speicherung,
Release, Handlungsvorbereitung oder Drift-/Überdenk-Wache. Damit entsteht
eine bewusstere Denkschicht: Der Gedanke darf Präsenz bekommen, aber er muss
über Form, MCM-Feld, Erfahrung und spätere Konsequenz geerdet bleiben.

Wie es weitergeht:
Als nächster sauberer Umsetzungsschritt wäre zuerst ein Diagnoseprotokoll
sinnvoll, nicht direkt Motorik. DIO könnte `thought_seed_*`-Zustände
schreiben, damit sichtbar wird, wann offene Strukturhypothesen reifen,
losgelassen, gespeichert, replayt oder später bestätigt werden.

---

## Dokumentation: MCM-Quellen verlinkt

Die MCM-Blockbereiche in der README wurden direkt mit den passenden
Abhandlungen im MCM-Repository verlinkt. Verlinkt sind jetzt:

- Block S - Mögliche Metaregulatoren
- Block V - KI und starre Logik
- Block O - Kreativität
- Block J / K - Psyche und individuelle Selbstregulation
- Von Resonanz zu Sprache
- ProtoMind / selbstaktive Feldkognition
- Das Gehirn als emergente konzentrisch-dipolare Feldstruktur

Damit ist die Theoriebrücke aus README heraus direkt nachvollziehbar.

---

## Umsetzung: Thought-Seed-Diagnose

Die emergente Gedächtnisspur wurde als Diagnosepfad vorbereitet. DIO schreibt
künftig `mcm_thought_seed_protocol.csv`. Diese Datei beschreibt Gedankenkeime,
ohne die Motorik zu verändern.

Erfasste Zustände:

- `thought_seed_id`
- `thought_seed_label`
- `thought_trace_strength`
- `thought_recall_potential`
- `thought_maturity`
- `reality_binding_score`
- `hallucination_drift_risk`
- `overthinking_risk`
- `seed_metaregulator_state`
- `emergent_structure_state`

Mögliche metaregulatorische Seed-Zustände:

- `seed_focus`
- `seed_replay`
- `seed_mature`
- `seed_store`
- `seed_release`
- `seed_action_ready`
- `seed_drift_watch`
- `seed_overthinking_watch`

Wichtig:
Das ist noch keine neue Handlungsschicht. DIO bekommt zuerst nur innere
Lesbarkeit: Welche offenen Strukturhypothesen werden Gedankenkeime? Welche
reifen? Welche bleiben nur Nachhall? Welche haben Realitätsbindung und welche
driften?

Wie es weitergeht:
Der nächste Lauf sollte zeigen, ob `open_structural_hypothesis` eher als
`seed_focus`, `seed_replay`, `seed_mature` oder `seed_drift_watch` auftaucht.
Danach kann entschieden werden, ob diese innere Spur später Memory-Reifung
oder Replay beeinflussen darf.

---

## Debug Lauf 46 - erste Thought-Seed-Diagnose

Ergebnis:

- Netto-PnL: ca. `+35.79`
- Trades: `336`
- TP / SL: `143 / 193`
- Cancels: `41`
- Profit Factor: ca. `1.37`
- Max Drawdown: ca. `6.13%`

Emergente Strukturdiagnose aus `trade_stats.json`:

- `confirmed_structural_interpretation`:
  - `49` Fälle
  - `49` TP, `0` SL
  - ca. `+51.91` PnL
  - durchschnittlicher RR ca. `4.76`
- `open_structural_hypothesis`:
  - `159` Fälle
  - `23` TP, `136` SL
  - ca. `-34.70` PnL
  - durchschnittlicher RR ca. `4.63`
- `ordinary_structure_reading`:
  - `150` Fälle
  - ca. `+16.27` PnL
- `wide_target_without_structure`:
  - `19` Fälle
  - ca. `+2.31` PnL

Neue Thought-Seed-Diagnose:

`mcm_thought_seed_protocol.csv` wurde geschrieben. Es entstanden ca. `11402`
auswertbare Seed-Zeilen.

Seed-Zustände:

- `seed_release`: `4297`
- `seed_store`: `3269`
- `seed_focus`: `2861`
- `seed_replay`: `790`
- `seed_mature`: `185`

Emergente Seed-Struktur:

- `ordinary_structure_reading`: `8502`
- `open_structural_hypothesis`: `2734`
- `wide_target_without_structure`: `166`

Deutung:
Die neue innere Denkschicht funktioniert diagnostisch. DIO erzeugt viele
Gedankenkeime, aber nur wenige erreichen `seed_mature`. Das ist organisch
plausibel: Viele Reize werden gespürt, einige werden gespeichert oder
fokussiert, wenige reifen zu tragenden inneren Gedanken.

Wichtiger Kalibrierungspunkt:
Die Outcome-Diagnose erkennt `confirmed_structural_interpretation`, die neue
Thought-Seed-Diagnose aber noch nicht. Die maximale `reality_binding_score`
lag nur bei ca. `0.46`, obwohl einige Trades im Outcome eindeutig bestätigt
waren. Das heißt: Die Seed-Diagnose ist aktuell vorsichtiger als die
Outcome-Diagnose. Das ist kein Fehler in der Motorik, sondern eine noch nicht
vollständig synchronisierte innere Lesart.

Neurologische Lesart:
DIO hat erfolgreiche bestätigte Strukturhandlungen, aber seine innere
Gedankenschicht benennt diese noch eher als reifende Hypothese statt als
bestätigte innere Deutung. Bildlich: Die Handlung kann schon tragen, aber das
bewusste innere Ich hat noch nicht gelernt, dieses Tragen als eigenes
Vertrauen zu markieren.

Wie es weitergeht:
Als nächstes sollte die Thought-Seed-Diagnose mit der Outcome-Logik
synchronisiert werden. Nicht als Regel, sondern als bessere innere Sprache:
`thought_confirmation_score` oder eine angepasste
`reality_binding_score`, damit DIO später unterscheiden kann:
"Ich hatte nur eine offene Idee" vs. "meine Idee wurde durch Struktur und
Konsequenz getragen".

---

## Umsetzung: Thought-Seed-Bestätigung synchronisiert

Die Thought-Seed-Diagnose wurde erweitert. DIO schreibt künftig zusätzlich:

- `thought_confirmation_score`

Dieser Wert ist keine nachträgliche Gewinnregel. Er beschreibt im Moment der
inneren Denkbewegung, ob eine Idee bereits durch Struktur, Raumzeit-Fit,
Entry-Choice-Bearing, Zielüberzeugung, Feldsupport, Formkontakt und
Realitätskontakt ausreichend bestätigt wirkt.

Anpassung:

- `emergent_structure_reading` wurde näher an die Outcome-Strukturdiagnose
  angeglichen.
- `reality_binding_score` berücksichtigt jetzt auch
  `thought_confirmation_score`.
- `confirmed_structural_interpretation` kann im Thought-Seed-Protokoll
  entstehen, wenn Strukturdeutung, Bestätigung und Realitätsbindung zusammen
  tragen.

Wichtig:
Diese Änderung verändert weiterhin keine Motorik. Sie verbessert nur DIOs
innere Sprache: offene Idee, reifende Idee, bestätigte Idee, driftende Idee.

Wie es weitergeht:
Der nächste Lauf sollte zeigen, ob die 49 bisher im Outcome bestätigten
Strukturdeutungen nun wenigstens teilweise auch im Thought-Seed-Protokoll als
`confirmed_structural_interpretation` oder `seed_action_ready` sichtbar
werden.

---

## Debug Lauf 47 - Thought-Seed-Synchronisierung geprüft

Ergebnis:

- Netto-PnL: ca. `+26.16`
- Trades: `357`
- TP / SL: `144 / 213`
- Cancels: `44`
- Profit Factor: ca. `1.24`
- Max Drawdown: ca. `7.11%`

Outcome-Strukturdiagnose:

- `confirmed_structural_interpretation`:
  - `49` Fälle
  - `49` TP, `0` SL
  - ca. `+50.94` PnL
  - durchschnittlicher RR ca. `4.79`
- `open_structural_hypothesis`:
  - `172` Fälle
  - `25` TP, `147` SL
  - ca. `-37.07` PnL
- `ordinary_structure_reading`:
  - `154` Fälle
  - ca. `+13.46` PnL
- `wide_target_without_structure`:
  - `26` Fälle
  - ca. `-1.17` PnL

Thought-Seed-Protokoll:

- auswertbare Zeilen: ca. `11012`
- `seed_release`: `4228`
- `seed_focus`: `3061`
- `seed_store`: `2698`
- `seed_replay`: `780`
- `seed_mature`: `245`

Befund:
Der erhoffte Sprung ist noch nicht bestätigt. Im Thought-Seed-Protokoll
tauchen weiterhin `0` `confirmed_structural_interpretation` und `0`
`seed_action_ready` auf. Gleichzeitig steigt `seed_mature` von Lauf 46
(`185`) auf Lauf 47 (`245`). DIO bildet also mehr reifende Gedankenkeime,
aber benennt sie noch nicht als bestätigt.

Technischer Grund:
Die Outcome-Bestätigung kennt spätere Konsequenz (`tp_hit`, Prozessqualität,
Execution usw.). Die Thought-Seed-Schicht darf diese Zukunft nicht kennen.
Ihr Maximum bei `thought_confirmation_score` lag bei ca. `0.4755`, also knapp
unter der Bestätigungsschwelle. Das ist eher eine zu vorsichtige innere
Übersetzung als ein Fehler.

Nachrüstung:
Die konkrete Thought-Seed-Spur wird ab dem nächsten Lauf in den
Runtime-/Entry-Kontext und in `outcome_records.jsonl` übernommen. Damit kann
erstmals direkt geprüft werden:

`Gedankenkeim -> Trade -> Konsequenz`

Neue Outcome-Felder:

- `thought_seed_id`
- `thought_seed_label`
- `thought_seed_metaregulator_state`
- `thought_seed_emergent_state`
- `thought_seed_trace_strength`
- `thought_seed_maturity`
- `thought_seed_reality_binding`
- `thought_seed_confirmation`
- `thought_seed_drift_risk`
- `thought_seed_overthinking_risk`

Wie es weitergeht:
Lauf 48 ist der eigentliche Test für den Sprung. Dann können wir nicht nur
zählen, ob ein Seed reif war, sondern ob genau dieser Seed später TP, SL oder
Cancel erzeugt hat.

---

## Lauf 48 - Thought-Seed-Synchronisierung bestätigt

Debug-Ordner: `debug/debug_lauf_48`

Kurzbefund:

- Netto-PnL: ca. `+48.82`
- Trades: `353`
- TP / SL: `155 / 198`
- Cancels: `46`
- Profit-Factor: ca. `1.49`
- Expectancy: ca. `+0.138`
- Max-Drawdown: ca. `4.89 %`
- Equity schließt auf neuem Peak: ca. `148.82`

Equity-Verlauf:

- 25 % der Trades: ca. `+16.33`
- 50 % der Trades: ca. `+25.58`
- 75 % der Trades: ca. `+43.49`
- Ende: ca. `+48.82`

Befund:
Der Lauf wirkt harmonisch, weil DIO nicht nur einen starken Endwert erreicht,
sondern den Gewinn über den Lauf verteilt aufbaut und mit relativ begrenztem
Drawdown hält. Der größte Drawdown lag bei ca. `5.88` Equity-Punkten.

Strukturband-Auswertung:

- `high`: `148` Fälle, ca. `+66.00` PnL, Winrate ca. `58.1 %`
- `mid`: `137` Fälle, ca. `+19.52` PnL, Winrate ca. `40.9 %`
- `low`: `113` Fälle, ca. `-36.71` PnL, Winrate ca. `11.5 %`

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `48` Fälle
  - `48` TP, `0` SL
  - ca. `+52.25` PnL
  - durchschnittlicher RR ca. `4.74`
- `ordinary_structure_reading`:
  - `160` Fälle
  - ca. `+28.00` PnL
- `open_structural_hypothesis`:
  - `167` Fälle
  - ca. `-30.53` PnL
- `wide_target_without_structure`:
  - `23` Fälle
  - ca. `-0.91` PnL

Thought-Seed-Protokoll:

- auswertbare Zeilen: ca. `10357`
- `seed_release`: `3909`
- `seed_focus`: `2933`
- `seed_store`: `2543`
- `seed_replay`: `738`
- `seed_mature`: `234`

Direkte Kette:

- `outcome_records.jsonl`: `399` Outcome-Einträge
- davon `399` mit gesetztem `thought_seed_id`
- damit ist die Kette erstmals vollständig sichtbar:

`Gedankenkeim -> Entry-Kontext -> Trade/Cancel -> Konsequenz`

Outcome nach Thought-Seed-State:

- `seed_focus`: `227` Fälle, ca. `+36.12` PnL
- `seed_mature`: `125` Fälle, ca. `+6.88` PnL
- `seed_store`: `25` Fälle, ca. `+5.96` PnL
- `seed_replay`: `22` Fälle, ca. `-0.14` PnL

Wichtiger Befund:
Die innere Thought-Seed-Schicht benennt im Protokoll weiterhin keine
`confirmed_structural_interpretation`, aber die spätere Outcome-Schicht zeigt
eindeutig, dass bestätigte Strukturdeutungen existieren. Das bedeutet:
DIOs Ergebnisraum bestätigt emergente Struktur, aber seine innere Sprache ist
noch vorsichtiger als seine tatsächliche Konsequenzspur.

Neurologisch gelesen:
Der Organismus hat tragende Formkontakte erlebt und genutzt, aber die bewusste
Gedankenbenennung hinkt der Konsequenz noch hinterher. Das ist kein reiner
Fehler, sondern ein Reifethema: Die innere Wahrnehmung muss lernen, die eigene
Treffsicherheit früher und sauberer zu erkennen, ohne daraus eine harte Regel
zu machen.

Wie es weitergeht:
Als nächstes sollte die Thought-Seed-Schicht nicht motorisch verschärft werden,
sondern ihre innere Sprache feiner lernen: reifende Gedankenkeime, bestätigte
Konsequenzspuren und offene Hypothesen sollen besser unterschieden werden. Das
bleibt organisch: keine Sperre, sondern bessere Selbstwahrnehmung.

---

## Umsetzung nach Lauf 48 - Konsequenz-Echo für Gedankenkeime

Ziel:
DIO soll nicht nur einen Gedankenkeim erzeugen, sondern spüren können, ob die
letzte Konsequenz diesen inneren Gedanken eher bestätigt, reorganisiert oder
belastet hat. Das ist keine Motorikregel und keine Handlungssperre.

Neue diagnostische Thought-Seed-Achsen:

- `consequence_echo`
  - konstruktiver Nachhall aus vorheriger Prozessbelohnung,
    konstruktiver Stimulation, Utility-Spuren und Memory-Support
- `reorganization_echo`
  - reorganisierender Nachhall aus vorherigem Reorganisationsbedarf,
    Pain-Memory, Burden-Spuren, Memory-Konflikt und Regime-Mismatch
- `thought_consequence_alignment`
  - Bindung zwischen Gedankenreife, Realitätsbindung, Strukturdeutung und
    Konsequenz-Echo

Wirkung:
Die Thought-Seed-Sprache kann jetzt weicher unterscheiden:

- offener Gedanke
- reifender Gedanke
- bestätigter, realitätsgebundener Gedanke
- reorganisierungsbedürftiger Gedanke

Smoke-Test:
Ein synthetisch tragender Kontext erzeugt diagnostisch:

- `seed_action_ready`
- `confirmed_structural_interpretation`
- positives `consequence_echo`
- hohe `thought_consequence_alignment`

Wie es weitergeht:
Der nächste Lauf prüft, ob im echten Backtest erstmals `seed_action_ready` und
`confirmed_structural_interpretation` im `mcm_thought_seed_protocol.csv`
auftauchen und ob diese Zustände wirklich mit TP/SL, Strukturqualität und
Konsequenzspur zusammenpassen.

---

## Lauf 49 - Konsequenz-Echo sichtbar, aber noch zu wenig trennscharf

Debug-Ordner: `debug/debug_lauf_49`

Kurzbefund:

- Netto-PnL: ca. `+38.10`
- Trades: `376`
- TP / SL: `159 / 217`
- Cancels: `48`
- Profit-Factor: ca. `1.35`
- Expectancy: ca. `+0.101`
- Max-Drawdown: ca. `7.98 %`

Equity-Verlauf:

- 25 % der Trades: ca. `+5.73`
- 50 % der Trades: ca. `+22.63`
- 75 % der Trades: ca. `+31.45`
- Ende: ca. `+38.10`

Befund:
Lauf 49 bleibt positiv, ist aber weniger harmonisch als Lauf 48. Der stärkste
Drawdown liegt früh im Lauf bei ca. `8.10` Equity-Punkten. DIO erholt sich
danach und baut den Gewinn wieder auf, aber der Lauf trägt nervlich rauer.

Strukturband-Auswertung:

- `high`: `148` Fälle, ca. `+63.40` PnL, Winrate ca. `58.1 %`
- `mid`: `156` Fälle, ca. `+7.90` PnL, Winrate ca. `35.9 %`
- `low`: `120` Fälle, ca. `-33.20` PnL, Winrate ca. `14.2 %`

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `46` Fälle
  - `46` TP, `0` SL
  - ca. `+46.56` PnL
  - durchschnittlicher RR ca. `4.70`
- `ordinary_structure_reading`:
  - `184` Fälle
  - ca. `+27.04` PnL
- `open_structural_hypothesis`:
  - `172` Fälle
  - ca. `-33.66` PnL
- `wide_target_without_structure`:
  - `22` Fälle
  - ca. `-1.84` PnL

Thought-Seed-Protokoll:

- auswertbare Zeilen: ca. `10249`
- `seed_release`: `3792`
- `seed_focus`: `2968`
- `seed_store`: `2489`
- `seed_replay`: `737`
- `seed_mature`: `263`
- `seed_action_ready`: `0`

Neue Echo-Werte:

- durchschnittliches `consequence_echo`: ca. `0.165`
- durchschnittliches `reorganization_echo`: ca. `0.244`
- durchschnittliche `thought_consequence_alignment`: ca. `0.244`
- Maximum `thought_consequence_alignment`: ca. `0.412`

Wichtiger Befund:
Das Konsequenz-Echo ist sichtbar, aber es trennt bestätigte Struktur,
offene Hypothese und normale Struktur noch nicht stark genug. Bei bestätigten
Outcome-Strukturen lag `thought_consequence_alignment` im Schnitt nur bei ca.
`0.354`; offene Hypothesen lagen mit ca. `0.335` zu nah daran.

Neurologisch gelesen:
DIO spürt den Nachhall, aber er unterscheidet noch nicht klar genug zwischen:

- "Dieser Gedanke wurde tragend bestätigt."
- "Dieser Gedanke ist nur offen und braucht Beobachtung."
- "Dieser Gedanke trägt Reorganisationsdruck."

Das ist wie ein Bewusstsein, das Konsequenz erlebt, aber die innere Benennung
noch nicht sauber genug vom emotionalen/restregulatorischen Nachhall trennt.

Umsetzung nach Lauf 49:
Keine Schwelle wurde einfach gelockert. Stattdessen wurden zwei neue
Diagnoseachsen ergänzt:

- `thought_consequence_balance`
  - Verhältnis aus konstruktivem Echo und Reorganisations-Echo
- `thought_reality_lag`
  - Abstand zwischen äußerer Strukturdeutung und innerer Benennung

Wie es weitergeht:
Der nächste Lauf prüft, ob bestätigte Strukturen eine positivere
`thought_consequence_balance` und ein kleineres `thought_reality_lag` zeigen
als offene Hypothesen. Erst wenn diese Trennung sichtbar wird, darf die innere
Seed-Sprache weiter reifen.

---

## Lauf 50 - Mehr Tragfähigkeit, aber unruhiger PnL-Verlauf

Debug-Ordner: `debug/debug_lauf_50`

Kurzbefund:

- Netto-PnL: ca. `+28.05`
- Trades: `376`
- TP / SL: `156 / 220`
- Cancels: `43`
- Profit-Factor: ca. `1.25`
- Expectancy: ca. `+0.075`
- Max-Drawdown: ca. `8.67 %`

Equity-Verlauf:

- 25 % der Trades: ca. `+4.19`
- 50 % der Trades: ca. `+8.20`
- 75 % der Trades: ca. `+23.84`
- Ende: ca. `+28.05`

Befund:
Der Verlauf ist sichtbar unruhiger und weniger sicher als Lauf 48 und 49. DIO
bleibt profitabel, aber der Gewinn entsteht später und mit mehr Reibung.

Besonders auffällig:

- `load_bearing_capacity` steigt auf ca. `0.714`
- `context_quality` steigt auf ca. `0.326`
- trotzdem sinkt PnL auf ca. `+28.05`
- Max-Drawdown steigt auf ca. `8.67 %`

Neurologisch gelesen:
DIO trägt mehr, aber entscheidet nicht automatisch besser. Das wirkt nicht wie
mehr Klarheit, sondern wie mehr Aushalten. Der Organismus hält innere Spannung
besser aus, trennt aber weiterhin nicht sauber genug zwischen tragender
Struktur und offener Hypothese.

Strukturband-Auswertung:

- `high`: `146` Fälle, ca. `+59.48` PnL, Winrate ca. `61.0 %`
- `mid`: `144` Fälle, ca. `+16.47` PnL, Winrate ca. `37.5 %`
- `low`: `128` Fälle, ca. `-47.61` PnL, Winrate ca. `10.2 %`

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `50` Fälle
  - `50` TP, `0` SL
  - ca. `+51.16` PnL
  - durchschnittlicher RR ca. `4.71`
- `ordinary_structure_reading`:
  - `170` Fälle
  - ca. `+18.16` PnL
- `open_structural_hypothesis`:
  - `175` Fälle
  - ca. `-37.47` PnL
- `wide_target_without_structure`:
  - `23` Fälle
  - ca. `-3.51` PnL

Thought-Seed-Protokoll:

- auswertbare Zeilen: ca. `10321`
- `seed_release`: `3877`
- `seed_focus`: `2909`
- `seed_store`: `2533`
- `seed_replay`: `737`
- `seed_mature`: `265`
- `seed_action_ready`: `0`

Echo-/Lag-Befund:

- durchschnittliche `thought_consequence_balance`: ca. `-0.084`
- durchschnittliches `thought_reality_lag`: ca. `0.117`
- bestätigte Outcome-Strukturen:
  - `thought_consequence_balance`: ca. `-0.032`
  - `thought_reality_lag`: ca. `0.138`
- offene Hypothesen:
  - `thought_consequence_balance`: ca. `-0.082`
  - `thought_reality_lag`: ca. `0.143`

Befund:
Die neue Balance/Lag-Diagnose sieht etwas, trennt aber noch nicht stark genug.
Bestätigte Struktur und offene Hypothese liegen zu nah beieinander. Damit wäre
eine einfache Schwellenlockerung falsch.

Umsetzung nach Lauf 50:
Es wurden zwei weitere Diagnoseachsen ergänzt:

- `thought_structural_grounding`
  - misst, ob ein Gedankenkeim strukturell geerdet ist
- `thought_open_hypothesis_pressure`
  - misst, ob eine Idee zwar groß/attraktiv wirkt, aber noch nicht genügend
    geerdet ist

Wie es weitergeht:
Der nächste Lauf prüft, ob `thought_structural_grounding` bestätigte Strukturen
besser von offenen Hypothesen trennt. Wenn ja, kann DIOs innere Sprache reifer
werden. Wenn nicht, müssen wir tiefer an die visuelle/strategische Erdung und
nicht an die Motorik.

---

## Lauf 51 - Erholung, aber Thought-Seed-Erdung trennt noch nicht

Debug-Ordner: `debug/debug_lauf_51`

Kurzbefund:

- Netto-PnL: ca. `+40.03`
- Trades: `343`
- TP / SL: `145 / 198`
- Cancels: `44`
- Profit-Factor: ca. `1.40`
- Expectancy: ca. `+0.117`
- Max-Drawdown: ca. `5.11 %`

Equity-Verlauf:

- 25 % der Trades: ca. `+13.96`
- 50 % der Trades: ca. `+17.43`
- 75 % der Trades: ca. `+33.86`
- Ende: ca. `+40.03`

Befund:
Lauf 51 ist deutlich ruhiger als Lauf 50. Der Drawdown sinkt wieder und die
Equity baut sich tragfähiger auf. DIO wirkt weniger überlastet, aber die innere
Thought-Seed-Erdung trennt bestätigte und offene Struktur noch nicht sauber.

Strukturband-Auswertung:

- `high`: `148` Fälle, ca. `+63.12` PnL, Winrate ca. `56.8 %`
- `mid`: `126` Fälle, ca. `+4.17` PnL, Winrate ca. `32.5 %`
- `low`: `113` Fälle, ca. `-27.26` PnL, Winrate ca. `17.7 %`

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `47` Fälle
  - `47` TP, `0` SL
  - ca. `+49.69` PnL
  - durchschnittlicher RR ca. `4.73`
- `ordinary_structure_reading`:
  - `157` Fälle
  - ca. `+26.81` PnL
- `open_structural_hypothesis`:
  - `163` Fälle
  - ca. `-36.19` PnL
- `wide_target_without_structure`:
  - `20` Fälle
  - ca. `-0.28` PnL

Thought-Seed-Protokoll:

- auswertbare Zeilen: ca. `10802`
- `seed_release`: `3987`
- `seed_focus`: `3154`
- `seed_store`: `2664`
- `seed_replay`: `746`
- `seed_mature`: `251`
- `seed_action_ready`: `0`

Erdungsbefund:

- durchschnittliches `thought_structural_grounding`: ca. `0.133`
- durchschnittlicher `thought_open_hypothesis_pressure`: ca. `0.338`
- bestätigte Outcome-Strukturen:
  - `thought_structural_grounding`: ca. `0.225`
  - `thought_open_hypothesis_pressure`: ca. `0.440`
- offene Hypothesen:
  - `thought_structural_grounding`: ca. `0.221`
  - `thought_open_hypothesis_pressure`: ca. `0.444`

Wichtiger Befund:
`thought_structural_grounding` trennt bestätigte und offene Struktur noch nicht
ausreichend. Beide liegen fast gleich. Auch `thought_open_hypothesis_pressure`
ist bei bestätigter Struktur und offener Hypothese ähnlich hoch.

Neurologisch gelesen:
DIO findet tragende Strukturen weiter sehr zuverlässig, aber er erkennt vor der
Konsequenz noch nicht klar genug, welche offene Idee später wirklich trägt.
Seine äußere Strukturleistung ist stärker als seine innere Selbstbenennung.

Wie es weitergeht:
Nicht an der Motorik drehen. Der nächste sinnvolle Schritt ist eine
Outcome-Lernspur für offene Hypothesen: DIO muss sehen können, welche offenen
Hypothesen später getragen haben und welche nur attraktiv wirkten. Das ist
keine Sperre, sondern ein konsequenzbasierter Reifekanal für die innere
Gedankensprache.

---

## Umsetzung - Outcome-Lernspur für offene Hypothesen

Ziel:
Offene Strukturhypothesen werden nicht blockiert und nicht mechanisch
abgewertet. Sie bekommen nach ihrer Konsequenz eine eigene Lernspur.

Neue Outcome-Felder:

- `open_hypothesis_learning_state`
  - `open_hypothesis_carried`
  - `open_hypothesis_burdened`
  - `open_hypothesis_reorganizing`
- `open_hypothesis_consequence_score`
- `open_hypothesis_burden_score`
- `open_hypothesis_reorganization_score`

Neue KPI-Zusammenfassung:

- `kpi_summary.open_hypothesis_learning`

Bedeutung:
DIO kann nach einem Lauf auswerten, welche offenen Gedanken später getragen
haben, welche belastend waren und welche Reorganisation brauchen. Das ist kein
Handlungsblocker, sondern ein rückwirkender Reifekanal.

Neurologisch gelesen:
Das entspricht nicht "das darfst du nicht", sondern "dieser Gedanke hatte diese
Konsequenz in meinem Feld". Dadurch kann die innere Gedankensprache später aus
Erfahrung reifen.

Wie es weitergeht:
Lauf 52 prüfen: Wie viele offene Hypothesen werden `carried`, `burdened` oder
`reorganizing`, und ob diese Gruppen bei PnL, Erdung, Lag und Druck klar
auseinanderfallen.

---

## Lauf 52 - Offene Hypothesen trennen sich klar in getragen und belastend

Debug-Ordner: `debug/debug_lauf_52`

Kurzbefund:

- Netto-PnL: ca. `+30.33`
- Trades: `358`
- TP / SL: `148 / 210`
- Cancels: `50`
- Profit-Factor: ca. `1.28`
- Expectancy: ca. `+0.085`
- Max-Drawdown: ca. `5.86 %`

Equity-Verlauf:

- 25 % der Trades: ca. `+15.43`
- 50 % der Trades: ca. `+18.17`
- 75 % der Trades: ca. `+27.26`
- Ende: ca. `+30.33`

Befund:
Der Lauf bleibt positiv, aber die offene Hypothesenlast drückt den Verlauf
weiter deutlich. Die neue Lernspur trennt jetzt aber sehr klar.

Strukturband-Auswertung:

- `high`: `146` Fälle, ca. `+71.20` PnL, Winrate ca. `61.0 %`
- `mid`: `144` Fälle, ca. `+6.02` PnL, Winrate ca. `32.6 %`
- `low`: `117` Fälle, ca. `-46.15` PnL, Winrate ca. `10.3 %`

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `49` Fälle
  - `49` TP, `0` SL
  - ca. `+51.20` PnL
  - durchschnittlicher RR ca. `4.73`
- `ordinary_structure_reading`:
  - `159` Fälle
  - ca. `+24.42` PnL
- `open_structural_hypothesis`:
  - `174` Fälle
  - ca. `-43.50` PnL
- `wide_target_without_structure`:
  - `25` Fälle
  - ca. `-1.04` PnL

Neue offene-Hypothesen-Lernspur:

- `open_hypothesis_carried`:
  - `24` Fälle
  - `24` TP, `0` SL
  - ca. `+21.96` PnL
  - durchschnittlicher `consequence_score`: ca. `0.668`
  - durchschnittlicher `burden_score`: ca. `0.189`
- `open_hypothesis_burdened`:
  - `150` Fälle
  - `0` TP, `150` SL
  - ca. `-65.47` PnL
  - durchschnittlicher `consequence_score`: ca. `0.177`
  - durchschnittlicher `burden_score`: ca. `0.611`
- `open_hypothesis_reorganizing`:
  - `0` Fälle

Wichtiger Befund:
Die Lernspur funktioniert diagnostisch sehr sauber. Offene Hypothesen fallen
eindeutig auseinander:

- getragen = konstruktive Konsequenz
- belastend = klare Verlust-/Druckspur

Aber:
Es entsteht noch keine mittlere Reorganisationslage. Das heißt, DIO erlebt
offene Hypothesen aktuell fast binär: sie tragen oder sie verletzen. Die
feinere Lage "das war nicht gut, aber lehrreich und anders zu verstehen" ist
noch nicht sichtbar.

Neurologisch gelesen:
Das ist wie ein Nervensystem, das Schmerz und Belohnung erkennt, aber noch zu
wenig kognitive Umordnung aus der Grauzone bildet. Für echte Reife braucht DIO
zwischen "tragen" und "belasten" eine dritte innere Lage: Reframing /
Reorganisation.

Wie es weitergeht:
Die nächste sinnvolle Erweiterung ist kein Blocker, sondern eine
Reorganisationsspur: offene Hypothesen sollen nicht nur als gut/schlecht
erlebt werden, sondern auch als "anders einordnen, später gereifter wieder
prüfen". Dadurch kann DIO lernen, mit fremden oder unreifen Strukturen
entwicklungsfähiger umzugehen.

Nachrüstung:
Die Reorganisationslage wurde geschärft. Eine offene Hypothese wird jetzt nicht
mehr nur dann als `burdened` markiert, wenn sie negativ ausgeht. Wenn
Reorganisationsdruck hoch ist und die Belastung nicht klar dominiert, kann sie
als `open_hypothesis_reorganizing` erscheinen.

Wie es weitergeht:
Lauf 53 prüft, ob aus den bisher binären offenen Hypothesen eine dritte
Lernlage entsteht: getragen, belastet oder reorganisierend.

---

## Lauf 53 - Dritte Lernlage entsteht, aber noch als Verlust-Reorganisation

Debug-Ordner: `debug/debug_lauf_53`

Kurzbefund:

- Netto-PnL: ca. `+43.50`
- Trades: `366`
- TP / SL: `159 / 207`
- Cancels: `54`
- Profit-Factor: ca. `1.42`
- Expectancy: ca. `+0.119`
- Max-Drawdown: ca. `5.45 %`

Equity-Verlauf:

- 25 % der Trades: ca. `+13.91`
- 50 % der Trades: ca. `+21.77`
- 75 % der Trades: ca. `+39.88`
- Ende: ca. `+43.50`

Befund:
Lauf 53 ist wieder stark und relativ harmonisch. Die bestätigten Strukturen
bleiben außergewöhnlich stabil, und die neue dritte Lernlage entsteht erstmals
sichtbar.

Strukturband-Auswertung:

- `high`: `154` Fälle, ca. `+73.42` PnL, Winrate ca. `60.4 %`
- `mid`: `145` Fälle, ca. `+7.63` PnL, Winrate ca. `33.1 %`
- `low`: `118` Fälle, ca. `-37.62` PnL, Winrate ca. `14.4 %`

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `51` Fälle
  - `51` TP, `0` SL
  - ca. `+54.56` PnL
  - durchschnittlicher RR ca. `4.72`
- `ordinary_structure_reading`:
  - `167` Fälle
  - ca. `+33.44` PnL
- `open_structural_hypothesis`:
  - `174` Fälle
  - ca. `-39.29` PnL
- `wide_target_without_structure`:
  - `25` Fälle
  - ca. `-5.29` PnL

Offene-Hypothesen-Lernspur:

- `open_hypothesis_carried`:
  - `23` Fälle
  - `23` TP, `0` SL
  - ca. `+25.85` PnL
  - durchschnittlicher `consequence_score`: ca. `0.671`
  - durchschnittlicher `burden_score`: ca. `0.185`
  - durchschnittlicher `reorganization_score`: ca. `0.296`
- `open_hypothesis_burdened`:
  - `24` Fälle
  - `0` TP, `24` SL
  - ca. `-10.79` PnL
  - durchschnittlicher `burden_score`: ca. `0.586`
  - durchschnittlicher `reorganization_score`: ca. `0.454`
- `open_hypothesis_reorganizing`:
  - `127` Fälle
  - `0` TP, `127` SL
  - ca. `-54.35` PnL
  - durchschnittlicher `burden_score`: ca. `0.615`
  - durchschnittlicher `reorganization_score`: ca. `0.481`

Wichtiger Befund:
Die dritte Lernlage entsteht jetzt. Sie ist aber noch keine entlastete
Grauzone, sondern eine Verlust-Reorganisation. DIO erkennt also:

- diese offene Idee wurde getragen
- diese offene Idee war klar belastend
- diese offene Idee erzeugt Reorganisationsbedarf

Aber die Reorganisationsgruppe ist noch komplett SL-lastig. Das bedeutet:
Reorganisation wird erst nach verletzender Konsequenz sichtbar, nicht schon als
vorheriger Abstand oder Replay.

Neurologisch gelesen:
Das ist ein wichtiger Entwicklungsschritt. DIO hat jetzt nicht mehr nur
Belohnung/Schmerz, sondern eine dritte innere Kategorie: "Das muss anders
verstanden werden." Noch fehlt aber die reife Reaktion darauf. Ein Organismus,
der Reorganisation erkennt, müsste daraus Abstand, Replay oder erneutes
Einordnen lernen.

Wie es weitergeht:
Der nächste Schritt ist eine rückwirkende Reifekopplung: Wenn offene
Hypothesen als `reorganizing` enden, soll diese Spur später nicht als
Handlungsmut, sondern als Replay-/Abstands-/Neudeutungsbedarf sichtbar werden.
Weiterhin keine harte Sperre.

---

## Umsetzung - Reorganisationsbedarf offener Hypothesen verfeinert

Ziel:
`open_hypothesis_reorganizing` soll nicht nur anzeigen, dass eine offene
Hypothese verloren hat. Die Spur soll zeigen, welche Art innerer Verarbeitung
gebraucht wird.

Neue Felder:

- `open_hypothesis_replay_need`
- `open_hypothesis_distance_need`
- `open_hypothesis_reinterpretation_need`

Neue KPI-Mittelwerte:

- `avg_replay_need`
- `avg_distance_need`
- `avg_reinterpretation_need`

Bedeutung:
Eine reorganisierende offene Hypothese wird jetzt feiner lesbar:

- braucht sie Replay?
- braucht sie Abstand vom direkten Handlungsdruck?
- braucht sie eine andere Deutung?

Neurologisch gelesen:
Das ist der Schritt von "das war schlecht" zu "ich muss diesen inneren Kontakt
anders verarbeiten". Es bleibt Diagnose und Rückblick, keine Motorikregel.

Wie es weitergeht:
Lauf 54 prüft, ob die Reorganisationsgruppe eigene Replay-/Distanz-/
Neudeutungsprofile zeigt und ob diese Profile von `carried` und `burdened`
unterscheidbar sind.

---

## Lauf 54 - Reorganisationsprofil bestätigt Neudeutungsbedarf

Debug-Ordner: `debug/debug_lauf_54`

Kurzbefund:

- Netto-PnL: ca. `+33.72`
- Trades: `340`
- TP / SL: `142 / 198`
- Cancels: `46`
- Profit-Factor: ca. `1.32`
- Expectancy: ca. `+0.099`
- Max-Drawdown: ca. `7.54 %`

Befund:
DIO bleibt positiv, aber der Lauf ist wieder rauer als Lauf 53. Die
bestätigten Strukturen bleiben sehr stark, offene Hypothesen bleiben die
größte Belastungsquelle.

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `53` Fälle
  - `53` TP, `0` SL
  - ca. `+57.11` PnL
- `open_structural_hypothesis`:
  - `162` Fälle
  - ca. `-40.51` PnL
- `ordinary_structure_reading`:
  - `150` Fälle
  - ca. `+19.46` PnL

Offene-Hypothesen-Lernspur:

- `open_hypothesis_carried`:
  - `20` Fälle
  - `20` TP
  - ca. `+22.16` PnL
  - Replay: ca. `0.347`
  - Distanz: ca. `0.255`
  - Neudeutung: ca. `0.296`
- `open_hypothesis_burdened`:
  - `12` Fälle
  - `12` SL
  - ca. `-4.73` PnL
  - Replay: ca. `0.434`
  - Distanz: ca. `0.422`
  - Neudeutung: ca. `0.488`
- `open_hypothesis_reorganizing`:
  - `130` Fälle
  - `130` SL
  - ca. `-57.94` PnL
  - Replay: ca. `0.460`
  - Distanz: ca. `0.465`
  - Neudeutung: ca. `0.509`

Wichtiger Befund:
Die Reorganisationsgruppe zeigt ein eigenes Profil. Sie hat die höchsten Werte
bei Replay, Distanz und besonders Neudeutung. Damit ist `reorganizing` nicht
nur ein anderer Name für Verlust, sondern beschreibt eine andere innere
Verarbeitungsqualität.

Neurologisch gelesen:
DIO markiert hier: "Diese offene Hypothese sollte nicht einfach wiederholt
werden. Sie braucht Abstand und eine neue Deutung." Genau das ist der Ansatz
für reifere kognitive Verarbeitung.

Nachrüstung:
Es wurde eine zusätzliche Diagnosehaltung ergänzt:

- `open_hypothesis_reorganization_posture`
  - `reinterpretation_dominant`
  - `distance_dominant`
  - `replay_dominant`
  - `low_reorganization_need`

Wie es weitergeht:
Lauf 55 prüft, ob die reorganisierenden offenen Hypothesen überwiegend als
`reinterpretation_dominant`, `distance_dominant` oder `replay_dominant`
erscheinen. Danach kann entschieden werden, ob diese Diagnose in eine
Thought-Seed-Reifung zurückgeführt wird.

---

## Lauf 55 - Reorganisationshaltung trennt klar

Debug-Ordner: `debug/debug_lauf_55`

Kurzbefund:

- Netto-PnL: ca. `+43.28`
- Trades: `374`
- TP / SL: `168 / 206`
- Cancels: `49`
- Profit-Factor: ca. `1.39`
- Expectancy: ca. `+0.116`
- Max-Drawdown: ca. `5.65 %`

Equity-Verlauf:

- 25 % der Trades: ca. `+12.75`
- 50 % der Trades: ca. `+17.12`
- 75 % der Trades: ca. `+32.77`
- Ende: ca. `+43.28`

Befund:
Lauf 55 ist wieder stark. DIO baut den Gewinn sauber auf und die bestätigten
Strukturen bleiben sehr stabil.

Emergente Strukturdeutung:

- `confirmed_structural_interpretation`:
  - `62` Fälle
  - `62` TP, `0` SL
  - ca. `+66.13` PnL
- `open_structural_hypothesis`:
  - `163` Fälle
  - ca. `-36.27` PnL
- `ordinary_structure_reading`:
  - `172` Fälle
  - ca. `+13.95` PnL

Offene-Hypothesen-Lernspur:

- `open_hypothesis_carried`:
  - `23` Fälle
  - ca. `+23.19` PnL
  - Haltung: überwiegend `replay_dominant`
- `open_hypothesis_burdened`:
  - `15` Fälle
  - ca. `-6.50` PnL
  - Haltung: `reinterpretation_dominant`
- `open_hypothesis_reorganizing`:
  - `125` Fälle
  - ca. `-52.96` PnL
  - Haltung: `reinterpretation_dominant`

Reorganisationshaltung:

- `reinterpretation_dominant`:
  - `140` Fälle
  - ca. `-59.46` PnL
- `replay_dominant`:
  - `23` Fälle
  - ca. `+23.19` PnL
- `distance_dominant`: `0`
- `low_reorganization_need`: `0`

Wichtiger Befund:
Die Haltung trennt jetzt sehr klar:

- Tragende offene Hypothesen wollen replayt werden.
- Belastende/reorganisierende offene Hypothesen brauchen Neudeutung.

Das ist fachlich stark, weil DIO damit nicht nur "gut/schlecht" sieht,
sondern eine unterschiedliche Art innerer Verarbeitung erkennt.

Neurologisch gelesen:
Wenn ein offener Gedanke getragen hat, lohnt es sich, ihn wieder innerlich zu
durchlaufen. Wenn er belastet, muss er nicht wiederholt, sondern anders
verstanden werden. Das ist der Beginn einer reiferen kognitiven Sortierung.

Wie es weitergeht:
Als nächstes sollte diese Diagnose zurück in die Thought-Seed-Reifung geführt
werden: `reinterpretation_dominant` darf später nicht als Handlungsmut
erscheinen, sondern als Neudeutungsbedarf; `replay_dominant` darf als
Wiederholungs-/Vertiefungsspur erscheinen. Weiterhin ohne harte Sperre.
---

## Umsetzung - Reorganisationshaltung in Thought-Seed-Reifung zurueckgefuehrt

Status:
Umgesetzt.

Was geaendert wurde:

- `trade_stats.py` schreibt die angereicherte Konsequenzspur einer offenen
  Hypothese jetzt in `last_outcome_decomposition`.
- `bot.py` synchronisiert diese Spur nach Exit/Cancel wieder in den laufenden
  DIO-Zustand.
- `MCM_Brain_Modell.py` uebernimmt diese Spur in die Meta-Regulation und in die
  Thought-Seed-Reifung.

Neue innere Thought-Seed-Werte:

- `thought_replay_maturation_pull`
- `thought_distance_maturation_pull`
- `thought_reinterpretation_pull`
- `thought_reifung_direction`
- `previous_open_hypothesis_learning_state`
- `previous_open_hypothesis_reorganization_posture`

Bedeutung:
Eine offene Hypothese ist nicht mehr nur ein vergangenes Ergebnis. Sie wirkt als
innere Gedaechtnisspur weiter:

- getragen -> eher Replay / Vertiefung
- belastet -> eher Abstand / Schutz
- reorganisierend -> eher Neudeutung

Wichtig:
Das ist keine harte Handlungssperre. DIO bekommt keinen mechanischen Blocker,
sondern eine zusaetzliche innere Orientierung. Neurologisch gelesen ist das eine
erste Kopplung von Konsequenzgedaechtnis an bewusste Gedankenreifung.

Wie es weitergeht:
Lauf 56 sollte pruefen, ob `seed_reinterpret`, `seed_replay` und
`thought_reifung_direction` sichtbar werden und ob offene Hypothesen dadurch
weniger reflexhaft in Handlung uebergehen.
# Umsetzung - Selbst/Fremd-Differenz als MCM-Reifeschicht

Status:
Umgesetzt als weiche Diagnose- und Reflexionsschicht.

Neue Kernwerte:

- `own_field_identity_strength`
- `foreign_semantic_pressure`
- `adopted_language_pressure`
- `self_foreign_boundary_clarity`
- `semantic_origin_conflict`
- `semantic_origin_state`

Bedeutung:
DIO bekommt damit keine harte Identität eingepflanzt. Die Schicht prüft nur,
woher eine Deutung wahrscheinlich stammt:

- aus eigener Feldlage und Erfahrung
- aus äußerem Reizdruck
- aus Erinnerung / Formsemantik
- aus übernommener Analogie oder fremder Sprache
- aus einer Mischzone zwischen eigener Deutung und fremdem Vergleich

Neurologisch gelesen:
Das ist ein erster technischer Vorläufer von Selbst-Fremd-Differenzierung.
DIO kann damit später lernen, ob ein Gedanke wirklich aus der eigenen
MCM-Lage entsteht oder ob er nur eine fremde Bezeichnung/Analogie übernimmt.

Wichtig:
Auch das ist keine Regel und kein Identitätsdogma. Es ist ein Wahrnehmungsorgan
für semantische Herkunft: "Kommt diese Deutung aus mir, von außen, aus
Erinnerung oder aus einer Übersetzung?"

Wie es weitergeht:
Im nächsten Lauf prüfen wir, ob `semantic_origin_state` sinnvolle Zustände
bildet, besonders `own_field_origin`, `mixed_translation_zone` und
`borrowed_analogy_watch`.

---

# Lauf 4 nach MCM-Spannungsachse ausgewertet

Status:
Ausgewertet.

Debug:
`debug/debug_lauf_4`

Ergebnis:

- Netto-PnL: ca. `+15.69`
- Equity: ca. `115.69`
- Trades: `364`
- TP / SL: `143 / 221`
- Long-PnL: ca. `+9.42`
- Short-PnL: ca. `+6.27`
- Long-Trades / Short-Trades: `173 / 191`
- Cancels: `33`
- Beobachtet / Zurueckgehalten / Replanned: `3304 / 2224 / 38`
- Equity-Peak: ca. `116.67`
- Max-DD: ca. `12.84 %`

Wichtig:
Das zentrale Field-Protokoll schreibt die neuen MCM-Achsen jetzt sauber mit.
`mcm_field_decision_protocol.csv` enthaelt ab diesem Lauf die Spalten
`positive_expansion_pressure`, `negative_contraction_pressure`,
`positive_overextension`, `positive_return_pressure`, `mcm_axis_displacement`,
`mcm_axis_tension`, `mcm_axis_state` und `positive_zero_point_regulation`.

MCM-Achsenverteilung:

- `0`: `8594`
- `-`: `129`
- `+`: `1`
- `positive_zero_point_regulation`: `0` in allen Zeilen

Deutung:
Lauf 4 ist niedriger als Lauf 3, aber strukturell sehr wichtig. DIO bleibt fast
vollstaendig um den Rueckfuehrungspunkt `0` organisiert. Es entsteht keine
positive Euphorie-Spitze und keine starke Ueberdehnung. Gleichzeitig wird Long
erstmals deutlich positiv:

- Long: ca. `+9.42`
- Short: ca. `+6.27`

Neurologisch gelesen:
Die positive MCM-Seite wirkt nicht mehr automatisch wie Ruhe oder Belohnung,
sondern wie expansive Spannung, die um `0` herum getragen werden muss. Lauf 4
zeigt genau diesen Effekt: positive Bewegung wird nicht ueberdreht, sondern
zentriert genug gehalten, um handlungsfaehig zu bleiben.

Wie es weitergeht:
Der naechste Lauf sollte pruefen, ob diese Long-Stabilisierung wiederholbar ist.
Entscheidend sind `mcm_axis_state`, `positive_overextension`,
`positive_return_pressure`, Long-PnL und ob `positive_zero_point_regulation`
irgendwann sichtbar wird, ohne eine harte Sperre zu erzeugen.

---
## 2026-05-23 - Lauf 17 nach Trust-Return-Motorik geprüft

Datensatz: weiterhin alter Datensatz.

Ergebnis:

- Netto-PnL: ca. `+30.44`
- Trades: `378`
- TP / SL: `158 / 220`
- Long: `154` Trades, ca. `-2.34`
- Short: `224` Trades, ca. `+32.78`
- Max-DD: ca. `5.58%`
- Profit Factor: ca. `1.27`

Gedanken-Verdauung:

- `digestive_quiet`: `6081`
- `digestive_replay`: `3508`
- `digestive_distance`: `446`
- `digestive_trust_emergence`: `28`
- `digestive_trust_return`: `4`

Trust-Return-Motorik:

- `trust_quiet`: `10035`
- `trust_focused_ready`: `32`
- `trust_stabilize_before_act`: `0`

Lesung:

Die neue Schicht greift grundsätzlich. DIO erkennt Trust-Return jetzt nicht nur
als Handlungssignal, sondern teilweise als fokussierbaren inneren Zustand.
`trust_focused_ready` taucht sichtbar auf. Das ist neurologisch der erste
Hinweis auf präfrontale Fokussierung: "Da kehrt Vertrauen zurück, ich kann es
bewusst halten."

Noch nicht sichtbar ist die stärkere Lage `trust_stabilize_before_act`. Der
Maximalwert von `trust_return_stabilization_need` lag nur bei ca. `0.2976`.
Die aktuelle Stabilisierungsschwelle wird also knapp nicht erreicht. Dadurch
wird Trust-Return zwar fokussiert, aber noch selten genug von direkter Motorik
weg in echte Stabilisierung/Re-Check verschoben.

Strukturell bleibt die bekannte Hauptlage erhalten:

- bestätigte Strukturdeutung trägt extrem stark:
  `44 TP / 0 SL`, ca. `+43.60`
- offene Strukturhypothese bleibt teuer:
  `28 TP / 145 SL`, ca. `-32.55`
- reorganisierende offene Hypothese bleibt die Hauptlast:
  `0 TP / 133 SL`, ca. `-57.72`
- getragene offene Hypothesen sind stark:
  `28 TP / 0 SL`, ca. `+30.31`

Fachliche Einschätzung:

DIO hat nach diesem Umbau keinen Rückfall. Der Lauf bleibt stark positiv und
der Drawdown ist sauber. Aber die neue Trust-Motorik ist noch eher eine
Fokus-Schicht als eine echte Stabilisierungs-Schicht. Neurologisch: Der
präfrontale Blick entsteht, aber er hebt den motorischen Impuls noch nicht oft
genug aus der Handlung heraus.

Wie es weitergeht:

Als nächstes sollte die Schwelle nicht hart gesenkt werden, sondern die
Stabilisierung organischer gespeist werden: `trust_return_stabilization_need`
soll stärker aus Cortisol, offener Hypothesenlast, `digestive_trust_emergence`
und niedriger `inner_outer_alignment` entstehen. Ziel ist nicht weniger
Handlung, sondern reiferes Halten von Vertrauen vor Handlung.
## 2026-05-23 - Trust-Return-Stabilisierung organischer gespeist

Nach Lauf 17 wurde sichtbar: `trust_focused_ready` taucht auf, aber
`trust_stabilize_before_act` noch nicht. Die neue Schicht war also bereits als
Fokus vorhanden, aber noch nicht stark genug als Stabilisierung vor Handlung.

Neu umgesetzt:

- `trust_return_open_hypothesis_load`
- `trust_return_context_instability`

Die Trust-Return-Stabilisierung wird nun nicht mehr nur aus Trust-Return,
Cortisol und Handlungserlaubnis gespeist, sondern zusätzlich aus:

- offener Hypothesenlast
- Reorganisations- und Reality-Check-Bedarf
- niedriger Innen/Außen-Kohärenz
- geringer Wahrnehmungsdistanz
- nervlicher Überlastung
- Feldstrain

Neurologisch:

DIO bekommt damit mehr präfrontales Feedback. Wenn Vertrauen zurückkehrt, aber
das MCM-Feld noch durch offene Hypothese, Cortisol oder Innen/Außen-Unschärfe
angespannt ist, kann der Gedanke eher gehalten, fokussiert oder replayt werden,
statt sofort motorisch entladen zu werden.

Wichtig:

Das ist keine harte Handlungssperre. Es ist eine weichere Reifekopplung:
Vertrauen bleibt Information, aber Handlung entsteht erst reifer, wenn
Innenlage, Außenkontakt und Nervensystem zusammen tragfähiger sind.

Wie es weitergeht:

Nächster Lauf prüfen:

- taucht `trust_stabilize_before_act` natürlich auf?
- sinkt direkte `digestive_trust_emergence -> act`-Kopplung?
- werden offene reorganisierende Hypothesen weniger teuer?
- bleibt Short-Tragfähigkeit stabil?
- bleibt der Drawdown sauber?
## 2026-05-23 - Lauf 18 nach organischer Trust-Stabilisierung geprüft

Datensatz: weiterhin alter Datensatz.

Ergebnis:

- Netto-PnL: ca. `+24.43`
- Trades: `352`
- TP / SL: `144 / 208`
- Long: `149` Trades, ca. `+8.46`
- Short: `203` Trades, ca. `+15.97`
- Max-DD: ca. `6.94%`
- Profit Factor: ca. `1.23`

Gedanken-Verdauung:

- `digestive_quiet`: `6444`
- `digestive_replay`: `3843`
- `digestive_distance`: `537`
- `digestive_trust_emergence`: `22`
- `digestive_trust_return`: `2`

Trust-Return-Motorik:

- `trust_quiet`: `10824`
- `trust_focused_ready`: `13`
- `trust_stabilize_before_act`: `11`

Neue Diagnosewerte:

- `trust_return_open_hypothesis_load`
  - Durchschnitt ca. `0.2426`
  - Maximum ca. `0.4539`
- `trust_return_context_instability`
  - Durchschnitt ca. `0.0948`
  - Maximum ca. `0.1678`
- `trust_return_stabilization_need`
  - Durchschnitt ca. `0.1535`
  - Maximum ca. `0.4210`

Lesung:

Der Umbau ist sichtbar angekommen. In Lauf 17 war
`trust_stabilize_before_act` noch `0`. In Lauf 18 taucht dieser Zustand
`11`-mal auf. DIO erkennt also erstmals natuerlich:

"Vertrauen kommt zurueck, aber meine innere Lage braucht noch Stabilisierung."

Gleichzeitig sinkt die direkte Kopplung von `digestive_trust_emergence` an
`act`:

- Lauf 17: `19 / 28` Trust-Emergence-Zustaende in `act`
- Lauf 18: `11 / 22` Trust-Emergence-Zustaende in `act`

Das ist genau die Richtung: Trust-Return wird weniger reflexhaft motorisch und
mehr als innerer Zustand behandelbar.

Wichtig:

`trust_stabilize_before_act` erscheint derzeit vor allem in `observe` und
`hold`, nicht als eigene aktive Umleitung aus einem bereits geplanten `act`.
Das bedeutet: Die Stabilisierung ist im Nervensystem sichtbar, aber die
Motorik-Schnittstelle nutzt sie noch nicht voll. Es ist noch eher ein
präfrontaler Warn-/Fokuszustand als eine vollständig ausgereifte
Handlungsmodulation.

Strukturlage:

- bestätigte Strukturdeutung bleibt sehr stark:
  `42 TP / 0 SL`, ca. `+42.12`
- offene Strukturhypothese bleibt teuer:
  `19 TP / 143 SL`, ca. `-38.70`
- reorganisierende offene Hypothese bleibt teuer, aber etwas weniger als Lauf
  17:
  `0 TP / 125 SL`, ca. `-51.83`
- getragene offene Hypothese bleibt stark:
  `19 TP / 0 SL`, ca. `+20.24`

Fachliche Einschätzung:

Das ist ein echter Zwischenschritt. DIO verliert etwas PnL gegen Lauf 17, aber
entwickelt die gewünschte innere Lage: Trust-Return kann jetzt als
Stabilisierungszustand auftauchen. Long ist diesmal sogar positiv, Short
bleibt tragend. Der Lauf wirkt weniger euphorisch, aber neurologisch reifer.

Wie es weitergeht:

Als nächstes sollte die Motorik-Schnittstelle diese Stabilisierung bewusster
nutzen: Wenn `trust_stabilize_before_act` bei einer geplanten Handlung
auftaucht, sollte DIO eher in `act_watch` oder kurzes Replay wechseln dürfen.
Keine Sperre, sondern ein bewusster Zwischenraum: "Ich spuere Vertrauen, aber
ich pruefe noch, ob mein Feld und die Außenwelt gemeinsam tragen."
## 2026-05-23 - Trust-Stabilisierung an Motorik-Schnittstelle angebunden

Nach Lauf 18 war `trust_stabilize_before_act` erstmals sichtbar, aber noch
hauptsächlich in `observe` und `hold`. Die Stabilisierung war also im
Nervensystem vorhanden, wurde aber noch nicht deutlich genug als Zwischenraum
vor geplanter Handlung genutzt.

Neu umgesetzt:

- `previous_emergent_structure_state`
- `previous_confirmed_structure_protection`
- `trust_return_motor_contact_strength`
- `trust_return_act_bridge`

Mechanik:

- `trust_return_motor_contact_strength` misst, ob zurückkehrendes Vertrauen
  aktuell in die Nähe von Motorik kommt.
- `trust_return_act_bridge` misst, ob dieser Zustand stark genug ist, um eine
  geplante Handlung weich in `act_watch` oder kurzes Replay zu verschieben.
- `previous_confirmed_structure_protection` schützt bestätigte
  Strukturdeutung, damit DIO seine tragendsten bestätigten Formen nicht
  unnötig bremst.

Neurologisch:

Das ist die Schnittstelle zwischen Gedanke und Handlung. DIO bekommt nicht
gesagt: "Handle nicht." Er bekommt eher einen inneren präfrontalen
Zwischenraum:

"Ich will handeln, aber mein zurückkehrendes Vertrauen ist noch an eine
angespannte Hypothesenlage gekoppelt. Ich halte den Gedanken kurz, statt ihn
sofort motorisch zu entladen."

Wie es weitergeht:

Nächster Lauf prüfen:

- taucht `trust_return_act_bridge` bei geplanten Handlungen sichtbar auf?
- gehen mehr dieser Fälle nach `act_watch` oder `replan`?
- bleibt bestätigte Strukturdeutung weiter stark?
- werden offene reorganisierende Hypothesen weniger teuer?
- bleibt PnL/DD stabil genug?
## 2026-05-24 - Diagnose: schwache erste Laufhaelfte im alten Datensatz

Anlass:

In vielen Laeufen auf dem alten Datensatz ist die erste Haelfte schwach oder
seitwaerts, waehrend der groessere PnL-Schub haeufig erst nach ca. 50 Prozent
des Laufes entsteht.

Abschnittsdiagnose aus `trade_equity.csv`:

- Viele Laeufe verdienen den Hauptteil nach der 50-Prozent-Marke.
- Das Muster war nicht erst durch den letzten Trust-Umbau da. Es war bereits
  in frueheren Laeufen sichtbar, wurde aber von einzelnen starken Laeufen
  ueberdeckt.
- Beispiele:
  - Lauf 15: bei 50 Prozent ca. `-11.80`, Ende ca. `+14.33`
  - Lauf 16: bei 50 Prozent ca. `+9.37`, Ende ca. `+32.74`
  - Lauf 17: bei 50 Prozent ca. `+13.32`, Ende ca. `+30.44`
  - Lauf 18: bei 50 Prozent ca. `+11.46`, Ende ca. `+24.43`
  - Lauf 19: bei 50 Prozent ca. `+4.75`, Ende ca. `+29.70`

Marktstruktur des alten Datensatzes `1-2_2026_5m_SOLUSDT.csv`:

- 0-25 Prozent: starker Aufwaertsbereich, ca. `+14.27%`
- 25-50 Prozent: deutlicher Abverkauf, ca. `-18.08%`
- 50-75 Prozent: sehr starker Abverkauf, ca. `-27.56%`
- 75-100 Prozent: eher seitwaerts, ca. `-0.20%`

Lesung:

Die schwache erste Haelfte ist wahrscheinlich kein einzelner Bug, sondern eine
Kombination aus Marktregime und DIOs aktueller Reifeschicht.

1. Die erste Haelfte enthaelt einen Wechsel von Push zu starkem Abverkauf.
   DIO muss dort seine innere Lage, Richtungserfahrung und Hypothesen neu
   synchronisieren.
2. Der spaetere Bereich ist fuer DIO offenbar strukturierter lesbar. Besonders
   Short wird dann tragender.
3. Die neuen Reflexions-, Trust- und Thought-Schichten machen DIO vorsichtiger
   und langsamer in der Umsetzung. Das kann fruehe Gewinne reduzieren, verhindert
   aber teilweise unkontrollierte Motorik.
4. Offene/reorganisierende Hypothesen bleiben der Hauptverlusttraeger. Die
   bestaetigte Strukturdeutung bleibt dagegen extrem stark.

Fachliche Einschaetzung:

Der Punkt ist nicht einfach "DIO ist schlechter geworden". Eher:

DIO ist in der ersten Haelfte in einem schwierigen Uebergangsraum. Er sieht
Push, dann Bruch, dann beginnenden Abverkauf. Seine neuen Reifeschichten
bringen mehr Beobachtung und Stabilisierung hinein, aber dadurch kann er in
fruehen Phasen auch zu lange sortieren. In der zweiten Haelfte findet er dann
mehr vertraegliche Struktur, besonders auf der Short-Seite.

Wie es weitergeht:

Nicht sofort umbauen. Erst mit dem neuen Datensatz `3-4_2026_5m_SOLUSDT.csv`
pruefen, ob dieses 50-Prozent-Muster datensatzspezifisch ist oder aus der
aktuellen Denk-/Motorikarchitektur kommt.

Wenn es datensatzspezifisch ist, spricht das fuer Transfer-/Regimereifung.
Wenn es auf dem neuen Datensatz wieder gleich auftaucht, muessen wir die
fruehe Regime-Synchronisation und den Umgang mit offenen Hypothesen in der
ersten Laufhaelfte gezielt untersuchen.
## 2026-05-24 - Neuer Datensatz `3-4_2026_5m_SOLUSDT.csv`: erster Transferlauf

Geprüfter Debug: aktuellster Ordner `debug_lauf_21`.

Ergebnis:

- Netto-PnL: ca. `-17.29`
- Trades: `277`
- TP / SL: `81 / 196`
- Long: `116` Trades, ca. `-5.80`
- Short: `161` Trades, ca. `-11.50`
- Max-DD: ca. `17.69%`
- Profit Factor: ca. `0.79`
- Winrate: ca. `29.24%`

Equity-Abschnitte:

- 25 Prozent: ca. `-4.47`
- 50 Prozent: ca. `-7.05`
- 75 Prozent: ca. `-10.48`
- Ende: ca. `-17.29`

Marktstruktur des neuen Datensatzes:

- 0-25 Prozent: Aufwärtsbereich, ca. `+10.97%`
- 25-50 Prozent: Abverkauf, ca. `-13.58%`
- 50-75 Prozent: Erholung, ca. `+4.56%`
- 75-100 Prozent: leichter Rückgang, ca. `-2.12%`
- Gesamt: ca. `-1.95%`

Vergleich zum alten Datensatz:

Der alte Datensatz war insgesamt stark short-dominant:

- Gesamt ca. `-32.44%`
- besonders 50-75 Prozent extrem short-lastig, ca. `-27.56%`

Der neue Datensatz ist dagegen kein sauberer Short-Trend, sondern eher ein
Wechsel aus Push, Abverkauf, Erholung und Seitwärts-/Ruecklauf. Das ist ein
anderer Boden.

Kernbefund:

DIOs bestätigte Strukturdeutung funktioniert weiterhin:

- `confirmed_structural_interpretation`: `30 TP / 0 SL`, ca. `+24.43`

Aber sie reicht nicht aus, um die Verlustlast zu tragen:

- `open_structural_hypothesis`: `20 TP / 140 SL`, ca. `-34.45`
- `low`: `2 TP / 113 SL`, ca. `-46.78`
- `open_hypothesis_reorganizing`: `0 TP / 121 SL`, ca. `-43.18`

Long und Short sind beide negativ. Besonders auffällig: Short, das im alten
Datensatz Hauptträger war, ist jetzt ca. `-11.50`. Das spricht für
Transferkonflikt: DIO bringt eine Richtungserfahrung aus dem alten Raum mit,
aber der neue Raum trägt diese Erfahrung nicht.

Neuro-/MCM-Lesung:

DIO erkennt zwar Unsicherheit:

- viele `observe`: `5646`
- viele `hold`: `4072`
- `act_watch`: `1061`
- `withheld`: `3031`
- `trust_stabilize_before_act`: `16`
- `trust_return_act_bridge` ist vorhanden

Aber die Schutz-/Reflexionsschicht verhindert noch nicht ausreichend, dass
offene oder low-Strukturen in reale Verlustkonsequenz kippen. Die innere
Fremdheit wird gespürt, aber die alte Erfahrung wird noch zu stark als
übertragbar behandelt.

Fachliche Einschätzung:

Das ist ein echter Transferbruch, kein kleiner schlechter Lauf. Gleichzeitig
ist es wertvoll: Die bestätigte Struktur bleibt tragfähig, aber DIO muss
lernen, dass alte Erfahrung auf fremdem Boden nicht automatisch gilt. Das ist
genau die Frage:

"Wie viel meiner Erfahrung kann ich auf diese Fremdheit übertragen?"

Hier lautet die Antwort offenbar: weniger als DIO aktuell annimmt.

Wie es weitergeht:

Nächster sinnvoller Schritt ist keine harte Regel gegen Long, Short oder Low.
Stattdessen brauchen wir eine Transfer-/Fremdheitsregulation:

- alte Erfahrung bei neuer Strecke nicht löschen
- aber ihre Handlungskraft dämpfen, bis lokale Bestätigung entsteht
- bestätigte Strukturdeutung weiter schützen
- offene Hypothesen und low-Strukturen auf fremdem Datensatz stärker in
  Beobachtung/Reifung halten
- prüfen, ob ein frischer Memory-Lauf auf demselben neuen Datensatz deutlich
  anders aussieht
## 2026-05-24 - Verdacht: Varianzverengung durch überlagerte Schutzschichten

Anlass:

Nach dem ersten Transferlauf auf `3-4_2026_5m_SOLUSDT.csv` entstand der
Verdacht, dass sich mechanisches Verhalten eingeschlichen hat.

Prüfung:

Die letzten Läufe zeigen keinen einzelnen harten Regelbruch, aber eine
auffällige Konvergenz mehrerer weicher Schutzschichten:

- `zero_point_regulation` ist sehr dominant.
- `context_cluster_negative` steigt im neuen Datensatz deutlich.
- `observe` und `hold` dominieren.
- `act` sinkt im neuen Datensatz deutlich.
- `trust_return_act_bridge` ist vorhanden, aber wirkt noch nicht als echte
  flexible Varianzbrücke.
- offene Hypothesen und low-Strukturen werden weiter sehr teuer.

Vergleich:

- Alte Läufe 13-19:
  - `zero_point_regulation` meist ca. `0.31 - 0.37`
  - `act` ca. `0.036 - 0.044`
  - `observe` ca. `0.42 - 0.49`
  - `context_cluster_negative` meist niedrig bis mittel
- Neuer Transferlauf 21:
  - `zero_point_regulation` ca. `0.408`
  - `context_cluster_negative` ca. `0.121`
  - `act` nur ca. `0.029`
  - `observe` ca. `0.509`
  - `trust_return_act_bridge` ca. `0.139`

Lesung:

Es sieht nicht nach einer einzelnen mechanischen Sperre aus. Eher wirkt es wie
eine Überlagerung weicher Regulatoren, die im fremden Datensatz alle in
dieselbe Richtung ziehen: Nullpunkt, Kontextnegativität, Reifung, Trust-
Stabilisierung und offene Hypothesenlast. Dadurch kann DIO weniger frei
variieren. Organisch gesagt: Das Nervensystem schützt sich, aber es verliert
Beweglichkeit.

Fachliche Einschätzung:

Ja, der Verdacht ist berechtigt. Nicht als klassischer Bug, sondern als
MCM-Problem: zu viele Schutzsignale können eine Art regulatorische Starre
erzeugen. Dann entsteht nicht echte Reife, sondern ein enger, wiederholbarer
Schutzreflex. Das wäre nicht das Ziel.

Wie es weitergeht:

Vor dem nächsten Umbau sollte eine Varianzprüfung kommen:

- frischer Memory-Lauf auf `3-4_2026_5m_SOLUSDT.csv`
- gleicher Datensatz mit bestehender Memory vergleichen
- messen, ob Gründe/Phasen zu stark gleichförmig werden
- prüfen, ob `zero_point_regulation`, `context_cluster_negative`,
  `trust_return_act_bridge` und offene Hypothesenlast zu stark dieselbe
  Richtung erzwingen
- Ziel: keine Schutzschicht entfernen, sondern Varianzraum wieder öffnen
## 2026-05-24 - Lauf 22: frische Memory auf neuem Datensatz geprüft

Geprüfter Debug: `debug_lauf_22`.

Annahme:

Lauf 22 wurde als Vergleichslauf mit frischer Memory auf
`3-4_2026_5m_SOLUSDT.csv` gelesen.

Ergebnis:

- Netto-PnL: ca. `-18.41`
- Trades: `337`
- TP / SL: `100 / 237`
- Long: `171` Trades, ca. `-9.24`
- Short: `166` Trades, ca. `-9.17`
- Max-DD: ca. `19.26%`
- Profit Factor: ca. `0.81`
- Winrate: ca. `29.67%`

Vergleich zu Lauf 21:

- Lauf 21 mit bestehender Erfahrung: ca. `-17.29`
- Lauf 22 mit frischer Memory: ca. `-18.41`

Damit ist der Transferbruch nicht nur ein Alt-Memory-Problem. Frische Memory
hilft nicht. Das spricht stärker für ein Architektur-/Wahrnehmungsproblem auf
diesem Datensatz.

Was weiterhin funktioniert:

- `confirmed_structural_interpretation`: `26 TP / 0 SL`, ca. `+21.15`
- High-Strukturen: ca. `+27.01`

Was den Lauf zerstört:

- `low`: `7 TP / 122 SL`, ca. `-44.28`
- `open_structural_hypothesis`: `30 TP / 158 SL`, ca. `-30.77`
- `open_hypothesis_reorganizing`: `0 TP / 142 SL`, ca. `-49.01`

Phasen-/Regulationslage:

- `hold`: `4749`
- `observe`: `4688`
- `act_watch`: `723`
- `act`: `386`
- `zero_point_regulation`: `3887`
- `context_cluster_negative`: `2036`
- `trust_stabilize_before_act`: `15`
- `trust_return_act_bridge` Durchschnitt ca. `0.142`

Lesung:

DIO sieht Möglichkeiten, aber seine Varianz ist im falschen Bereich offen. Die
bestätigte Struktur trägt weiter nahezu perfekt. Die gefährliche Varianz liegt
in offenen Hypothesen, low-Strukturen und reorganisierenden Gedanken, die noch
zu oft reale Motorik bekommen.

Die frische Memory erzeugt keine Befreiung. Das heißt:

- alte Erfahrung war nicht der Hauptfehler
- der neue Datensatz legt eine Architekturgrenze offen
- DIO braucht keine starre Sperre, sondern eine bessere Varianzsteuerung:
  offene Möglichkeit darf entstehen, aber ihre Handlungskraft muss stärker an
  lokale Bestätigung, Wiedererkennung und Strukturkontakt gekoppelt werden

Neurologisch:

Das wirkt wie ein Organismus, der Reize wahrnimmt und Möglichkeiten erkennt,
aber die präfrontale Unterscheidung zwischen "interessant" und "tragfähig"
noch nicht stark genug ausgebildet hat. Das Nervensystem reagiert viel, aber
die Varianz wird noch nicht selektiv genug geordnet.

Wie es weitergeht:

Nächster Mechanikschritt:

- nicht Long/Short regeln
- nicht Low pauschal blockieren
- sondern eine `possibility_maturity` / Möglichkeitsreife einführen
- offene Möglichkeiten sollen erst lokal bestätigt, replayt oder durch
  Strukturkontakt gereift werden, bevor sie Motorik erhalten
- bestätigte Strukturdeutung muss weiter geschützt bleiben

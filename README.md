# Statistik Projekt HS25 – Report

## 1. Projektüberblick

In diesem Projekt analysieren wir IST-Daten des öffentlichen Verkehrs aus dem **Open Transport Data**-Kontext (SBB/Open-Data-Feed). Unser Fokus liegt auf **Verspätungen** (Ankunft/Abfahrt) und darauf, ob sich diese systematisch durch Faktoren wie **Tageszeit**, **Wochentag**, **Station/Bahnhof** oder **Urbanität** unterscheiden lassen.  

Neben der Statistik war ein zentraler Teil des Projekts die **technische Umsetzbarkeit**: Die Rohdaten sind sehr gross, weshalb wir eine robuste Datenpipeline und performante Tools (insb. Polars + Parquet) benötigt haben.

---

## 2. Projektstruktur & Reproduzierbarkeit

Damit das Projekt trotz sehr grosser Rohdaten reproduzierbar und übersichtlich bleibt, ist das Repository klar in **Code (Pipeline)**, **Daten** und **Analysen (Notebooks)** getrennt.

### 2.1 Ordnerstruktur

```text
Statistik_Projekt_HS25-main/
├─ .gitignore
├─ .python-version
├─ requirements.txt
├─ uv.lock
├─ src/
│  ├─ io_zip_processing.py
│  ├─ aggregate_month.py
│  └─ utils.py
├─ data/
│  └─ external/
│     ├─ dienststellen.csv
│     ├─ switzerland.geojson
│     └─ Boundaries_K4_GDETYP2020_20240101_de.gpkg
└─ notebooks/
   ├─ N01_EDA.ipynb
   ├─ N02.ipynb
   ├─ N03.ipynb
   ├─ N04.ipynb
   ├─ N05.ipynb
   ├─ N06.ipynb
   ├─ N07.ipynb
   ├─ N08.ipynb
   ├─ N09.ipynb
   ├─ N10.ipynb
   ├─ N11.ipynb
   ├─ bahnhof-mining.ipynb
   └─ bahnhof-mining-hypothese.ipynb
```
## 2.2 `src/` – Datenpipeline & Hilfsfunktionen

In `src/` liegt die Logik, um aus grossen Rohdaten handhabbare Analyse-Dateien zu erzeugen.

- **`src/io_zip_processing.py`**  
  Verarbeitet die heruntergeladenen **ZIP-Rohdaten** (Parsing/Extraktion) und schreibt strukturierte Zwischenstände als Parquet.

- **`src/aggregate_month.py`**  
  Aggregiert/vereinheitlicht die Zwischenstände zu einer **Monats-Parquet-Datei**.

- **`src/utils.py`**  
  Hilfsfunktionen (z.B. ressourcenschonendes Laden/Verarbeiten), um Kernel-Crashes und RAM-Probleme zu reduzieren.

---

## 2.3 `data/` – Datenablage (sauber getrennt nach Typ)

- **`data/external/` (im Repo enthalten)**  
  Zusätzliche, kleine Referenzdaten für Geo-/Mapping-Analysen:
  - `dienststellen.csv` (Stations-/Dienststelleninfos)
  - `switzerland.geojson` (Schweiz-Umriss für Kartenplots)
  - `Boundaries_...gpkg` (Gemeinde-/Boundary-Daten für Urban/Rural-Analysen)

- **`data/raw/`, `data/interim/`, `data/processed/` (bewusst nicht im Repo)**  
  Diese Ordner sind nicht versioniert (u.a. wegen Datengrösse) und werden über `.gitignore` ausgeschlossen.

  Konzeptuell ist der Datenfluss wie folgt:
  - `data/raw/`: Rohdaten (z.B. heruntergeladene ZIP-Dateien)
  - `data/interim/`: Zwischenstände aus `io_zip_processing.py`
  - `data/processed/`: finale Analyse-Dateien (Parquet), z.B. Monatsdatei und bereinigte “Trains only”-Datei

Diese Trennung erlaubt reproduzierbare Analysen, ohne riesige Rohdaten in Git einzuchecken. Falls ihr  den data Ordner vollständig benötigt, können wir diesen gerne noch nachreichen. 

---

## 2.4 `notebooks/` – Analyse-Notebooks

Alle statistischen Auswertungen liegen in `notebooks/` und bauen logisch aufeinander auf. Details dazu folgen in Abschnitt 5.

---

## 3. Python-Umgebung und Tools

Das Projekt wurde in einer lokalen Python-Umgebung mit Jupyter Notebooks entwickelt. Wegen der Datengrösse war Performance entscheidend.

**Wichtigste Tools/Libraries:**
- `polars` für DataFrame-Verarbeitung (Performance, speichereffizient)
- `numpy`, `scipy`, `statsmodels` für Statistik, Tests und Regression
- `matplotlib` / `plotly` für Visualisierung
- `geopandas` / Geo-Tools + Matching-Libraries für die Urban/Rural- und Geo-Teile

### Warum Polars statt Pandas?

Beim Arbeiten mit der vollen Monatsdatei kam es wiederholt zu Kernel-Crashes. Polars ist spaltenorientiert, schneller und speicherschonender; der Umstieg war ein entscheidender Schritt, um das Projekt stabil weiterzuführen.

---

## 4. Vorgehen / Projektablauf

### 4.1 Motivation für einen ganzen Monat statt einzelner Tage

Die Open-Transport-IST-Daten sind grundsätzlich in Tagesdateien verfügbar. Ein einzelner Tag ist jedoch oft wenig aussagekräftig, da Störungen, Wetter oder Events den Tag stark verzerren können. Deshalb entschieden wir uns für eine Monatsanalyse (September), um stabilere Muster zu erhalten.

### 4.2 Problem: Rohdaten sind zu gross

Der Download und die Verarbeitung des gesamten Monats im Rohformat wären sehr speicher- und rechenintensiv (Grössenordnung > 50 GB). Auf normaler Laptop-Hardware war das nicht zuverlässig handhabbar.

### 4.3 Lösung: ZIP → Parquet Pipeline

Um die Daten effizient zu speichern und schneller analysieren zu können, haben wir eine Pipeline aufgebaut:

1. Download der ZIP-Dateien des gewünschten Zeitraums  
2. Parsing/Processing der Inhalte mit `src/io_zip_processing.py`  
   → Ausgabe als strukturierte Zwischenstände (Parquet)  
3. Monatsaggregation mit `src/aggregate_month.py`  
   → eine Monatsdatei als Parquet (deutlich kleiner, schneller zu laden)

**Warum Parquet?**
- deutlich kleinere Dateigrösse dank Kompression
- schnelleres Einlesen
- spaltenorientiertes Arbeiten (nur benötigte Spalten werden geladen)

### 4.4 Erste Notebook-Phase und Ressourcenproblem

Zu Beginn sind wir inhaltlich der Vorlesungsstruktur gefolgt (EDA → Deskriptiv → Inferenz → Tests → Regression). In dieser Phase kam es mehrfach zu Kernel-Abstürzen durch:
- zu grosse Tabellen im RAM
- speicherintensive Joins/Gruppierungen/Plots
- begrenzte Hardware-Ressourcen

### 4.5 Scope-Entscheidung: “Trains only”

Um das Projekt robust abschliessen zu können, entschieden wir uns, die Analyse auf Zugverbindungen zu beschränken. Dadurch sank die Datenmenge auf ca. 4.5 Mio. Zeilen, was auf normaler Hardware gut analysierbar war, ohne das Thema inhaltlich zu verlieren.

Ab diesem Punkt wurden zentrale Teile der Notebooks neu aufgesetzt und die finalen Resultate basieren auf der “Trains only”-Datenbasis.

---

## 5. Notebook-Guide: Inhalt pro Notebook (in sinnvoller Reihenfolge)

### 5.1 Basisdaten erstellen

#### `N01_EDA.ipynb` – Data Engineering & Cleaning (Basis)
- Filter auf Züge
- Missing-Value-Analyse (inkl. Interpretation: strukturell vs. technisch)
- Umgang mit fehlenden Delay-Werten (z.B. robuste Imputation mit Median pro Linie + Fallback)
- Feature Engineering (Wochentag, Weekend, Stunde/Zeitband etc.)
- Export einer bereinigten Basisdatei (Parquet), die als Input für die folgenden Notebooks dient

---

### 5.2 Vorlesungsnahe Grundlagen (Beschreiben & Schätzen)

#### `N02.ipynb` – Deskriptive Statistik
- Verteilungen von Ankunfts-/Abfahrtsverspätungen
- Kennzahlen, Visualisierungen
- Ausreisseranalyse nach Tukey/IQR

#### `N03.ipynb` – Zusammenhänge / Korrelation (Trains only)
- Feature Engineering (z.B. Stunde, Pünktlichkeit)
- Spearman-Korrelationsanalyse und Heatmap

#### `N04.ipynb` – Wahrscheinlichkeitstheorie am Datensatz
- ECDF, Law of Large Numbers (kumulativer Mittelwert)
- Vergleiche (z.B. Rush-Hour vs Off-Peak)
- didaktische Ergänzungen (z.B. Simpson-Paradoxon)

#### `N05.ipynb` – Schätzen & Konfidenzintervalle
- CI für Mittelwert (t-basiert)
- CI für Anteile (Pünktlichkeit)
- Bootstrap (z.B. Median, Differenzen, CIs)

---

### 5.3 Hypothesentests & Vergleiche

#### `N07.ipynb` – H11: Einfluss der Tageszeit
- Einteilung in Zeitfenster
- globaler Gruppenvergleich mit Kruskal–Wallis
- Effektgrösse Epsilon-Squared (ε²), weil sie zu einem rank-basierten Test passt und die Stärke des Effekts (nicht nur Signifikanz) quantifiziert
- Post-hoc paarweise Tests (Mann–Whitney) mit Korrektur

#### `N09.ipynb` – A/B-Vergleich (z.B. Zürich HB vs St. Gallen)
- Vergleich zweier Bahnhöfe
- Welch t-Test + Mann–Whitney U
- Effektgrössen und Bootstrap zur Differenzabschätzung

#### `N06.ipynb` – Urban vs. Rural & Geo-Analyse
- Join von Stationsdaten mit Gemeinde-/Boundary-Daten (`data/external/`)
- Matching/Normalisierung von Namen (inkl. Fuzzy Matching)
- Vergleich von Verspätungen zwischen urbanen und ländlichen Gebieten
- Geo-Visualisierungen / Aggregationen

---

### 5.4 Regression

#### `N10.ipynb` – Lineare Regression (verbessertes Modell)
- OLS-Modellierung
- Modellverbesserungen (z.B. nichtlineare Terme/Transformationen)
- Diagnoseplots (Residuals, QQ, Cook’s Distance)

#### `N11.ipynb` – Multiple Regression & Interaktionen
- Basis-Modell vs. Interaktionsmodell (z.B. hour × weekday)
- Modellvergleich via AIC/BIC
- Multikollinearität (VIF)
- Panelmodell mit Fixed Effects (Haltestellen-FE)
- Interpretation der Effekte

---

### 5.5 Bahnhof-Mining (Empfehlung TA Götz Henrik)

#### `bahnhof-mining.ipynb`
- Explorative Bahnhof-Analyse (Aggregation pro Bahnhof, Kartenplots, Filterung nach Mindestanzahl Beobachtungen)
- Ziel: Muster pro Bahnhof sichtbar machen (Auf-/Abbau von Verspätungen)

#### `bahnhof-mining-hypothese.ipynb`
- Hypothese: Bahnhöfe können Verspätungen systematisch “abbauen” oder “aufbauen”
- Analyse von Kennzahlen wie `delta_delay` (Änderung entlang der Fahrt bzw. stationäre Muster)
- Ergebnis: In der Schweiz sind die Muster insgesamt sehr homogen; wir konnten daraus keine starken, stabilen Erkenntnisse ableiten
- Trotzdem im Repo belassen, um diese explorative Spur (und die TA-Empfehlung) nachvollziehbar zu dokumentieren

---

### 5.6 Sonstiges

#### `N08.ipynb`
- Experimentier-/Zwischenschritte (u.a. Chi² und erste OLS-Ideen)
- nicht zentral für die finalen Resultate, aber als Dokumentation der Iteration enthalten

---

## 6. Kurzfazit zum Vorgehen

Unser Vorgehen war iterativ:
- Wir starteten mit dem vollständigen Monatsdatensatz und stellten schnell fest, dass Ressourcen/Performance limitieren.
- Über den Umstieg auf Parquet + Polars und die Scope-Entscheidung “Trains only” wurde das Projekt stabil.
- Danach konnten wir die Vorlesungsinhalte (Deskriptiv, Inferenz, Hypothesentests, Regression) sauber auf einer konsistenten Datenbasis umsetzen.
- Explorative Erweiterungen wie das Bahnhof-Mining (TA-Empfehlung) haben wir dokumentiert, auch wenn daraus in der Schweiz keine starken Unterschiede ableitbar waren.

## 7. Table of Contribution

### Detaillierte Aufgabenverteilung nach Notebooks

| Notebook | Thema / Statistische Analyse | Teammitglieder |
| :--- | :--- | :--- |
| **N01_EDA.ipynb** | Data Engineering, Cleaning & Filterung (Trains only) | Gemeinsam |
| **N02.ipynb** | Deskriptive Statistik & Ausreisseranalyse (Tukey) | Elia | 
| **N03.ipynb** | Korrelationsanalyse (Spearman) & Heatmaps | Leon |
| **N04.ipynb** | Wahrscheinlichkeitstheorie, ECDF & Law of Large Numbers | Bruno|
| **N05.ipynb** | Inferenzstatistik: Konfidenzintervalle & Bootstrapping | ELia |
| **N06.ipynb** | Urban vs. Rural Analyse & Geo-Matching (BFS-Daten) | Elia |
| **N07.ipynb** | Hypothesentest Tageszeit (Kruskal-Wallis & Mann-Whitney) | Leon |
| **N08.ipynb** | Experimentelle Analysen (Chi²-Tests & OLS-Entwürfe) | Elia |
| **N09.ipynb** | A/B-Vergleich (Zürich vs. St. Gallen) & Effektgrössen | Bruno |
| **N10.ipynb** | Lineare Regression (Transformationen & Diagnoseplots) | Bruno |
| **N11.ipynb** | Multiple Regression, Interaktionseffekte & VIF-Check | Bruno |
| **bahnhof-mining.ipynb** | Explorative Analyse der Bahnhof-Strukturen | Leon |
| **bahnhof-mining-hypothese.ipynb**| Prüfung der "Puffer-Hypothese" ($\Delta$ Delay Analyse) | Leon |

## 8. Methodische Zusatzdokumentation

Zur vollständigen Nachvollziehbarkeit des Projekts sind folgende begleitende Dokumente im Repository enthalten:

- **[Fallnotiz](Fallnotiz.md)**  
  Dokumentation zentraler Daten-, Scope- und Modellentscheidungen inkl. Verweis auf die jeweiligen Notebooks.

- **[Table of Prompts](Table_of_Prompts.md)**  
  Transparente Übersicht über den Einsatz von LLM-Unterstützung im Projektverlauf.

# Table of Prompts

## N01_EDA.ipynb (Data Engineering / Cleaning)

- „Ich habe eine große Parquet-Datei. Wie lade ich sie in **Polars** möglichst speicherschonend (scan_parquet vs read_parquet) und filtere direkt nur die relevanten Zeilen/Spalten?“
- „Wie filtere ich in Polars nur **Zugverbindungen** aus dem IST-Datensatz (welche Spalte/Filterstrategie ist typisch)?“
- „Wie erstelle ich in Polars eine **Missing-Value-Übersicht** pro Spalte mit Anzahl und Prozent und gebe sie als Tabelle aus?“
- „Wie mache ich eine **Missing-Values Heatmap** (z.B. mit seaborn) aus einem Polars-DataFrame, ohne alles zu groß zu machen (Sampling)?“
- „Ich habe `delay_arrival_s` und `delay_departure_s` in Sekunden. Wie erstelle ich `delay_min` in Minuten und behandle negative/extreme Werte sinnvoll?“
- „Welche Arten fehlender Werte treten in IST-Daten typischerweise auf und wie werden sie konzeptionell unterschieden?“
- „Welche robuste Imputationsstrategie eignet sich für fehlende Delay-Werte mit Median pro Linie oder Betreiber und einem globalen Fallback, und wie setzt man das in Polars um?“
- „Wie kann ich in Polars eine Imputation machen, bei der ich zuerst pro Gruppe (`line`, `operator`) den Median berechne und dann per Join zurückmerge?“
- „Wie validiere ich nach der Imputation, dass sich Verteilung/Kennzahlen nicht ‘kaputt’ verändern (Before/After Vergleich, Plots)?“
- „Wie erstelle ich Features aus einem Timestamp: `hour`, `weekday`, `is_weekend` (Polars `dt.*`)?“
- „Wie exportiere ich den bereinigten Datensatz sauber als `istdata_trains_clean.parquet` und stelle sicher, dass Datentypen korrekt bleiben?“
- „Welche Schritte und Ebenen sind bei der Dokumentation eines Datenflusses in Data-Science-Projekten üblich?“

---

## N02.ipynb (Deskriptive Statistik)

- „Wie berechne ich für `delay_min` die wichtigsten **Lage- und Streuungsmaße** und stelle sie kompakt als Tabelle dar?“
- „Wie kann ich in Polars robust die **Quantile** (0.25/0.5/0.75/0.9/0.99) berechnen?“
- „Wie implementiere ich die **Tukey-IQR Ausreißerregel** (mild/extreme) und zähle Ausreißer-Anteile?“
- „Wie mache ich Histogramme/Boxplots bei Millionen Zeilen ohne Kernel-Crash (Sampling, Binning, Clip bei 99%-Quantil)?“
- „Wie erstelle ich einen Plot mit Histogramm und vertikalen Referenzlinien für Median und Mittelwert inklusive Beschriftung?“
- „Wie erstelle ich eine **ECDF** (Empirical CDF) für Verspätungen und stelle sie sauber dar?“
- „Welche statistischen Konzepte beschreiben schiefe Verteilungen mit Heavy Tails und welche Kennwerte sind dafür geeignet?“
- „Wie mache ich einen Vergleich Ankunft vs Abfahrt (zwei Verteilungen in einem Plot, gleiche Skala, Outlier-Handling)?“
- „Wie ändere ich Plot-Farben/Theme so, dass es report-tauglich aussieht (Seaborn theme, grid, font sizes, rotate labels)?“

---

## N03.ipynb (Korrelation / Zusammenhänge, Trains-only)

- „Wie baue ich Features wie `is_punctual` (z.B. <= 3 Minuten) und berechne Pünktlichkeitsquote pro Gruppe?“
- „Wie berechne ich eine **Spearman-Korrelationsmatrix** für numerische Variablen und plotte eine Heatmap?“
- „Wie wähle ich nur numerische Spalten aus und behandle fehlende Werte sauber, bevor ich eine Spearman-Korrelation berechne?“
- „Wie visualisiere ich Unterschiede zwischen Betreibern/Operatoren (Boxplot je Betreiber) und verhindere, dass es durch viele Kategorien unlesbar wird (Top-N + Rest)?“
- „Wie aggregiere ich pro Bahnhof Kennzahlen: Mean/Median Delay, Anzahl Züge, Anteil pünktlich – und plotte das sinnvoll?“
- „Welche Unterschiede bestehen zwischen Pearson- und Spearman-Korrelation bei schief verteilten Daten?“

---

## N04.ipynb (Wahrscheinlichkeitstheorie am Datensatz)

- „Wie kann ich das **Gesetz der großen Zahlen** im Datensatz visualisieren, etwa über einen kumulativen Mittelwert über Zeit oder Index?“
- „Wie plotte ich ECDFs für zwei Gruppen (Rush-Hour vs Off-Peak) und vergleiche sie in einem Plot?“
- „Wie kann ich aus dem Datensatz eine Ereignisvariable definieren (z.B. ‘> 5 Min verspätet’) und **Relative Risk / Odds Ratio** berechnen?“
- „Wie mache ich einen einfachen Poisson/Verteilungs-Exkurs passend zu Verspätungsereignissen (Counts pro Zeitfenster)?“
- „Was ist das Simpson-Paradoxon und wie lässt es sich anhand eines Datensatzes veranschaulichen?“
- „Welche Konzepte werden verwendet, um Unterschiede zwischen ECDFs zu analysieren?“

---

## N05.ipynb (Schätzen & Konfidenzintervalle / Bootstrap)

- „Wie berechne ich ein **t-Konfidenzintervall** für den Mittelwert der Verspätung (Delay in Minuten)?“
- „Wie berechne ich ein Konfidenzintervall für einen **Anteil** (z.B. Pünktlichkeit) und welche Methode ist sinnvoll (Normalapprox vs Wilson)?“
- „Wie implementiere ich **Bootstrapping** für den Median der Verspätung (z.B. 10’000 Resamples) und gebe ein 95%-CI aus?“
- „Wie visualisiere ich die Bootstrap-Verteilung und markiere ein Konfidenzintervall im Plot?“
- „Was unterscheidet Punktschätzer, Standardfehler und Konfidenzintervalle konzeptionell?“
- „Welche bekannten Probleme treten bei Signifikanztests mit sehr großen Stichproben auf?“

---

## N06.ipynb (Urban vs Rural + Geo-Analyse + Hotspots)

### Datenintegration / Mapping Gemeinde & BPUIC

- „Ich habe `BPUIC` in den Verspätungsdaten und in `dienststellen.csv` gibt es `number` / `municipalityName` / `cantonAbbreviation`. Wie mappe ich `BPUIC` → Gemeinde/Kanton sauber (Polars + Pandas Join)?“
- „In `dienststellen.csv` sind Gemeindenamen manchmal wie `Zürich (Kreis 1)`. Wie entferne ich Klammerzusätze robust (Regex), damit Joins funktionieren?“
- „Ich habe Gemeindenamen aus SBB-Stationen, aber sie stimmen nicht exakt mit den BFS-Gemeinden in der GeoPackage-Datei überein. Wie mache ich **Fuzzy Matching** mit Kanton-Einschränkung, um False Matches zu vermeiden?“
- „Wie entwickle ich eine robuste Matching-Strategie für Gemeindenamen mit einem einfachen Regel-Ansatz und einem Fallback über Ähnlichkeitssuche, und wie wende ich das als Mapping in Polars an?“

### Urban/Rural Klassifizierung + Tests

- „In der GeoPackage-Datei gibt es eine STALAN/GDETYP-Klassifikation. Wie mappe ich Typ 1/2 → urban und Rest → rural und merge das mit meinen Daten?“
- „Welche nichtparametrischen Tests werden für Gruppenvergleiche bei nicht normalverteilten Daten verwendet?“
- „Wie plotte ich Urban vs Rural Delay-Verteilungen als KDE/Violin/Boxplot mit guter Lesbarkeit (und ggf. Clip bei 99%-Quantil)?“
- „Wie untersuche ich die **Interaktion von Regionstyp und Tageszeit** (z.B. Mean Delay je Stunde für urban/rural + zwei Linien)?“

### Geospatiale Analyse / Hotspots (Folium)

- „Ich möchte eine **Folium Choropleth/GeoJson-Karte** für Ø Verspätung pro Gemeinde erstellen. Wie mache ich das mit GeoPandas → WGS84 (EPSG:4326) und Folium?“
- „Mein GPKG enthält 3D-Geometrien (Z-Koordinaten) und Folium meckert. Wie entferne ich Z-Koordinaten mit `shapely.ops.transform` (remove_z)?“
- „Wie erstelle ich eine Folium-Karte mit Gemeinde-Polygonen eingefärbt nach `mean_delay` und einem Tooltip mit `gemeinde`, `mean_delay`, `region_type` und `n_trains`?“
- „Wie baue ich eine **StepColormap** (branca) mit diskreten Bins (z.B. [-1,0,1,2,3,4]) und setze Farben so, dass niedrige Werte grün und hohe rot sind?“
- „Wie ändere ich die Farben/Opacity/Border-Lines in Folium (style_function), damit es besser aussieht (weißes Border, fillOpacity 0.7)?“
- „Wie speichere ich die Folium-Karte als `map.html`, damit wir sie im Report/Abgabe zeigen können?“

### Netzknoten / Verkehrsaufkommen vs Pünktlichkeit

- „Wie aggregiere ich pro Gemeinde/Bahnhof `n_trains` (Verkehrsaufkommen) und `mean_delay` und plotte ‘Aufkommen vs Verspätung’ als Scatter (log-scale für Aufkommen)?“
- „Wie bilde ich `log_n_trains = log(1+n_trains)` und schätze anschließend ein OLS-Modell `mean_delay ~ log_n_trains`, und welche Outputs sollte ich zur Modellbewertung betrachten?“
- „Wie mache ich einen Plot mit `sns.regplot`, aber mit transparenten Punkten (alpha=0.3) und farbiger Regressionslinie (rot)?“
- „Welche theoretischen Zusammenhänge werden zwischen Verkehrsaufkommen und Verspätungen diskutiert?“

### Kantonaler Vergleich (Urban–Rural Gap)

- „Wie mache ich ein Pivot: `kanton × region_type` und berechne die Differenz `rural - urban` je Kanton?“
- „Wie erstelle ich einen Barplot für die Differenz `rural - urban` je Kanton und hebe positive und negative Werte visuell unterscheidbar hervor?“
- „Wie rotiere ich Kanton-Labels, setze eine Null-Linie, und mache den Plot report-tauglich (figsize, title padding, grid)?“

---

## N07.ipynb (H11 Tageszeit-Effekt + Post-hoc + Regression-Check)

- „Ich will Tageszeit in sinnvolle Zeitbänder einteilen (z.B. 0–5, 6–9, 10–15, 16–19, 20–23). Wie mache ich das in Pandas/Polars?“
- „Meine Delay-Daten sind nicht normalverteilt. Wie teste ich Unterschiede zwischen mehreren Zeitbändern mit **Kruskal–Wallis**?“
- „Wie wird die Effektgröße Epsilon-Squared für Kruskal–Wallis berechnet und interpretiert?“
- „Nach Kruskal–Wallis: Wie mache ich paarweise **Mann–Whitney U**-Tests für alle Zeitband-Paare und korrigiere Multiple Testing (Holm/FDR)?“
- „Wie erstelle ich eine Ergebnis-Tabelle für paarweise Tests mit Paar, p_raw, p_adj, Signifikanz und Effekt-Richtung?“
- „Wie visualisiere ich die Zeitband-Unterschiede: Boxplot nach Zeitband + Punkte (jitter) mit Sampling?“
- „Ich will kurz Regression-Annahmen checken: QQ-Plot, Residuals vs Fitted, Cook’s Distance. Wie mache ich das schnell in Python?“
- „Warum sind lineare Modelle bei stark schief verteilten Zielvariablen problematisch?“


---

## N08.ipynb (Chi² / Multiple Testing / erste OLS-Ideen)

- „Ich habe `is_punctual` und Kategorien wie `weekday` oder `time_band`. Wie mache ich eine Kreuztabelle und einen **Chi-Quadrat-Test** (scipy) für Unabhängigkeit?“
- „Ich teste mehrere Gruppenvergleiche (viele Kategorien). Wie mache ich eine **Multiple-Testing-Korrektur** (Benjamini–Hochberg / Holm) für viele p-Werte?“
- „Wie berechne ich eine Effektgröße zum Chi²-Test (Cramér’s V) und interpretiere sie?“
- „Ich möchte trotzdem ein OLS ausprobieren: `delay_min ~ hour + C(weekday)`. Wie setze ich das auf und welche Diagnoseplots brauche ich?“
- „Wie kann ich Variablen transformieren (z.B. log(1+delay)) um Ausreißer-Effekt zu reduzieren?“
- „Welche diagnostischen Kriterien sprechen gegen den Einsatz von OLS-Modellen?“

---

## N09.ipynb (A/B Testing: Zürich HB vs St. Gallen)

- „Ich will die Ankunftsverspätung zweier Bahnhöfe vergleichen (Zürich HB vs St. Gallen). Wie filtere ich den Datensatz sauber nach `HALTESTELLEN_NAME`?“
- „Welche Tests eignen sich für den Vergleich zweier Gruppen bei ungleicher Varianz und nicht-normalen Verteilungen, und welche Voraussetzungen haben sie?“
- „Wie berechne ich eine Effektgröße (z.B. Cohen’s d / rank-biserial) für den Bahnhofvergleich?“
- „Wie mache ich ein **Bootstrap** (10’000) für die Differenz der Mittelwerte/Mediane inkl. 95%-CI?“
- „Wie visualisiere ich die Verteilungen beider Bahnhöfe vergleichbar, etwa mit überlagerten Histogrammen oder Dichtekurven und zusätzlichen Boxplots?“
- „Wie stelle ich im Plot sicher, dass Ausreißer die Skala nicht sprengen (Clip/Zoom/Quantil-Limits)?“

---

## N10.ipynb (Regression – verbessertes OLS-Modell + Diagnose)

- „Ich möchte `delay_min` modellieren über `hour` und `weekday`. Wie baue ich ein OLS-Modell mit `statsmodels.formula.api`?“
- „Wie füge ich **polynomiale Terme** hinzu (z.B. `I(hour**2)`) und interpretiere die Nichtlinearität?“
- „Welche Transformation ist sinnvoll bei Delay (z.B. `log(1+delay)`), und wie setze ich das in der Formel um?“
- „Welche Diagnoseplots sind für ein OLS-Modell sinnvoll und wie interpretiert man sie, etwa Residuals vs Fitted, QQ-Plot und Cook’s Distance?“
- „Wie finde ich einen sinnvollen Cutoff für Cook’s Distance und markiere Influential Points im Plot?“
- „Welche typischen Einschränkungen bleiben bei linearen Modellen trotz erklärter Trends bestehen?“

---

## N11.ipynb (Interaktionen + VIF + Panel Fixed Effects)

- „Wie baue ich ein OLS-Modell mit Interaktion **hour × weekday** (z.B. `hour*C(Wochentag)`) in statsmodels?“
- „Wie vergleiche ich Basismodell vs Interaktionsmodell mit **AIC/BIC** und interpretiere den Trade-off (Fit vs Komplexität)?“
- „Wie berechne ich **VIF** für ein Modell mit vielen Dummies/Interaktionen und wie interpretiere ich hohe VIF-Werte?“
- „Ich möchte ein **Panelmodell mit Fixed Effects** pro Haltestelle bauen: Aggregation `HALTESTELLEN_NAME × date × hour × weekday`. Wie bereite ich den Panel-Index (entity, time) vor?“
- „Wie fitten wir `PanelOLS` (linearmodels) mit `EntityEffects` und **clustered SE** auf entity-level?“
- „Worin unterscheiden sich Fixed-Effects-Modelle und gepoolte OLS-Modelle konzeptionell?“
- „Welche Annahmen und Einsatzgebiete sprechen für Fixed-Effects-Modelle bei unbeobachteter, stationsspezifischer Heterogenität?“

---

## bahnhof-mining.ipynb (Bahnhof-Mining: Kartenplots Delta-Delay)

### Join Dienststellen / Koordinaten

- „Ich habe die externe Datei `dienststellen.csv` mit Spalten wie `operatingPointKilometerMasterNumber`, `Geoposition`, `designationOfficial`. Wie lese ich die ein und extrahiere `lat/lon` aus `Geoposition` (String ‘lat, lon’)?“
- „In meinem IST-Datensatz ist die Bahnhof-ID `BPUIC`. In `dienststellen.csv` scheint `operatingPointKilometerMasterNumber` dazu zu passen. Wie joine ich das sauber (Cast to string, strip)?“
- „Ich will nur Stationen mit gültiger Geoposition. Wie droppe ich Nulls und fehlerhafte Koordinaten robust?“
- „Wie benenne ich Spalten um, damit es eindeutig ist (`operatingPointKilometerMasterNumber` → `BPUIC`) und später alles konsistent bleibt?“

### Delta-Delay Definition

- „Ich möchte messen, ob an einem Bahnhof Verspätung eher **abgebaut** oder **aufgebaut** wird. Ist `delta_delay_min = (delay_departure_s - delay_arrival_s)/60` eine sinnvolle Definition? Welche Fallstricke gibt es?“
- „Wie filtere ich unrealistische Werte von `delta_delay_min` (z.B. extrem große Sprünge) und setze sinnvolle Grenzen?“
- „Wie aggregiere ich pro Bahnhof `mean_delta` und `n_obs` für den ganzen Monat?“
- „Wie setze ich eine Mindestanzahl Beobachtungen (`MIN_OBS_MONTH`, `MIN_OBS_DAY`), damit kleine Stationen keine Zufallsartefakte erzeugen?“

### Karte (Matplotlib) + Schweiz-Grenze (GeoJSON)

- „Ich habe `switzerland.geojson`. Wie zeichne ich die Schweiz-Grenze in Matplotlib (Polygon/MultiPolygon) als Basemap?“
- „Mein GeoJSON hat eine verschachtelte Struktur. Wie schreibe ich eine robuste Schleife, die sowohl Polygon als auch MultiPolygon plottet?“
- „Wie mache ich einen Scatter-Plot der Stationen (lon/lat), wobei die Farbe `mean_delta` ist und die Punktgröße von `sqrt(n_obs)` abhängt?“
- „Ich will eine diverging Colormap (blau=negativ=Puffer, rot=positiv=Verspätung). Welche Colormap ist passend und wie setze ich `vmin=-VMAX`, `vmax=VMAX`?“
- „Wie erstelle ich eine Colorbar mit Label ‘Delta (Minuten) – Blau=Puffer | Rot=Verspätung’ und setze Titel/Achsen sauber?“
- „Wie setze ich feste Achsen-Limits für CH (`xlim`, `ylim`), damit alle Plots dieselbe Skala haben?“
- „Wie kann ich die Karten als PNG speichern (`plt.savefig`) ohne abgeschnittene Labels (tight_layout, dpi)?“
- „Wie ändere ich Farben/Alpha/edgecolors, damit der Plot ‘clean’ aussieht (alpha=0.8, edgecolors='none')?“

### Tages-Schleife (30 Tage)

- „Ich will für jeden `BETRIEBSTAG` einen eigenen Plot erzeugen. Wie iteriere ich über alle Tage, aggregiere pro Tag pro BPUIC und plotte das automatisch?“
- „Wie verhindere ich, dass die Tagesplots zu langsam werden (z.B. vorherige Gruppierungen, effiziente Filter, weniger Stationen)?“
- „Wie mache ich die Titel dynamisch (z.B. ‘Verspätungsentwicklung am YYYY-MM-DD’) und speichere die Plots automatisch in einen Ordner?“
- „Wie stelle ich sicher, dass bei Tagen ohne Daten nichts crasht (if agg_day.height > 0 else print)?“

---

## bahnhof-mining-hypothese.ipynb (H12 Puffer-Effekt: Hypothese + Korrelation/Regression)

- „Ich habe pro Bahnhof `mean_delta_delay` und `anzahl_zuege`. Wie teste ich, ob größere Bahnhöfe eher Verspätung abbauen (Korrelation)?“
- „Welche Korrelation eignet sich bei Nichtlinearität und Heavy Tails besser, Pearson oder Spearman, und wie interpretiert man die Kennwerte korrekt?“
- „Wie baue ich einen Scatter-Plot: x=Anzahl Züge (log-Skala), y=Mean Delta Delay, inkl. Trendline und guter Beschriftung?“
- „Wie annotiere ich die wichtigsten Bahnhöfe im Plot (z.B. Top-10 nach `anzahl_zuege`) mit Namen (`HALTESTELLEN_NAME`)?“
- „Wie kann ich die y-Achse so labeln, dass klar ist: <0 bedeutet ‘Zeit aufgeholt’, >0 bedeutet ‘Verspätung erzeugt’? “
- „Wie setze ich eine diverging Norm, die um 0 zentriert ist (z.B. `TwoSlopeNorm(vcenter=0)`), damit Farben symmetrisch sind?“
- „Wie untersuche ich den Zusammenhang zwischen `mean_delta_delay` und `anzahl_zuege` mit einem Regressionsansatz (inkl. sinnvoller Transformationen), und welche Diagnose- und Interpretationspunkte sollte ich dabei beachten?“
- „Wir sehen in der Schweiz kaum Unterschiede zwischen Bahnhöfen. Nach welchen Kriterien werden Effekte in empirischen Analysen als schwach oder nicht robust eingeordnet?“
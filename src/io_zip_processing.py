from pathlib import Path
import zipfile
import pandas as pd

# -----------------------------------------------------------
# KONFIGURATION
# -----------------------------------------------------------

RAW_ZIP = Path("data/raw/ist-daten-v2-2025-09.zip")
OUTPUT_DIR = Path("data/interim")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

COLUMNS = [
    "BETRIEBSTAG",
    "FAHRT_BEZEICHNER",
    "BETREIBER_ID",
    "BETREIBER_ABK",
    "BETREIBER_NAME",
    "PRODUKT_ID",
    "LINIEN_ID",
    "LINIEN_TEXT",
    "VERKEHRSMITTEL_TEXT",
    "ZUSATZFAHRT_TF",
    "FAELLT_AUS_TF",
    "BPUIC",
    "HALTESTELLEN_NAME",
    "ANKUNFTSZEIT",
    "AN_PROGNOSE",
    "AN_PROGNOSE_STATUS",
    "ABFAHRTSZEIT",
    "AB_PROGNOSE",
    "AB_PROGNOSE_STATUS",
    "DURCHFAHRT_TF",
]

# -----------------------------------------------------------
# FUNKTIONEN
# -----------------------------------------------------------

def parse_datetime_safe(series: pd.Series) -> pd.Series:
    """Parst ISO-Timestamps robust (inkl. +0200 / +01 etc.) zu UTC-Datetime."""
    return pd.to_datetime(series, errors="coerce", utc=True)

def process_csv_from_zip(zip_path: Path, filename: str, filter_real: bool = True):
    """Verarbeitet eine Tages-CSV aus dem ZIP-Archiv, filtert auf reale IST-Daten
    und entfernt nur technisch unmögliche Werte (> ±1 Tag)."""
    print(f"🔹 Verarbeite {filename}")
    with zipfile.ZipFile(zip_path) as z:
        with z.open(filename) as f:
            df = pd.read_csv(
                f,
                sep=";",
                usecols=lambda x: x in COLUMNS,
                dtype={
                    "BETREIBER_NAME": "category",
                    "BETREIBER_ABK": "category",
                    "PRODUKT_ID": "category",
                    "VERKEHRSMITTEL_TEXT": "category",
                    "LINIEN_ID": "category",
                    "LINIEN_TEXT": "category",
                    "HALTESTELLEN_NAME": "category",
                    "FAELLT_AUS_TF": "boolean",
                    "DURCHFAHRT_TF": "boolean",
                    "AN_PROGNOSE_STATUS": "category",
                    "AB_PROGNOSE_STATUS": "category",
                },
                low_memory=False,
            )

    # --- Datumsfelder parsen ---
    for col in ["ANKUNFTSZEIT", "AN_PROGNOSE", "ABFAHRTSZEIT", "AB_PROGNOSE"]:
        if col in df.columns:
            df[col] = parse_datetime_safe(df[col])

    # --- Flags für echte IST-Zeiten ---
    if "AN_PROGNOSE_STATUS" in df.columns:
        df["AN_IS_REAL"] = df["AN_PROGNOSE_STATUS"].str.upper().isin(["REAL", "IST"])
    if "AB_PROGNOSE_STATUS" in df.columns:
        df["AB_IS_REAL"] = df["AB_PROGNOSE_STATUS"].str.upper().isin(["REAL", "IST"])

    df["HAS_REAL"] = df.get("AN_IS_REAL", False) | df.get("AB_IS_REAL", False)

    # --- Optional: nur reale Fahrten behalten ---
    if filter_real:
        df = df[df["HAS_REAL"]]
        print(f"🧭 Nur reale Daten: {len(df):,} Zeilen verbleiben")

    # --- Verspätung berechnen ---
    df["delay_arrival_s"] = (
        df["AN_PROGNOSE"] - df["ANKUNFTSZEIT"]
    ).dt.total_seconds()
    df["delay_departure_s"] = (
        df["AB_PROGNOSE"] - df["ABFAHRTSZEIT"]
    ).dt.total_seconds()

    # --- Technisches Cleaning: nur plausible Werte (±1 Tag) ---
    MAX_DELAY = 86400  # 1 Tag = 24 * 60 * 60 Sekunden
    for col in ["delay_arrival_s", "delay_departure_s"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[~df[col].between(-MAX_DELAY, MAX_DELAY), col] = pd.NA

    # --- Nur Zeilen mit mindestens einem gültigen Delay ---
    df = df.dropna(subset=["delay_arrival_s", "delay_departure_s"], how="all")

    # --- Pünktlichkeitsflag ---
    df["on_time"] = df["delay_arrival_s"].abs() <= 60

    # --- Speichern ---
    out_path = OUTPUT_DIR / f"{filename.replace('.csv', '.parquet')}"
    df.to_parquet(out_path, compression="snappy")
    print(f"✅ Gespeichert: {out_path} ({len(df):,} Zeilen)\n")

def process_month(zip_path: Path, max_days: int = 2, filter_real: bool = True):
    """Verarbeitet die ersten max_days CSV-Dateien eines Monats."""
    with zipfile.ZipFile(zip_path) as z:
        csv_files = [n for n in z.namelist() if n.endswith(".csv")]
        print(f"📦 Archiv enthält {len(csv_files)} CSV-Dateien.")
        for name in csv_files[:max_days]:
            process_csv_from_zip(zip_path, name, filter_real=filter_real)

if __name__ == "__main__":
    process_month(RAW_ZIP, max_days=30, filter_real=True)

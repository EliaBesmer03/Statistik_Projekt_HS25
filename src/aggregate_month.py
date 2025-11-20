from pathlib import Path
import pandas as pd

INTERIM_DIR = Path("data/interim")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Monat definieren (wichtig für Dateiname)
MONTH = "2025-09"

def combine_interim_files(month=MONTH):
    files = sorted(INTERIM_DIR.glob(f"*{month}*.parquet"))
    if not files:
        print("⚠️ Keine Dateien gefunden für", month)
        return

    print(f"📦 Füge {len(files)} Dateien für {month} zusammen...")

    dfs = []
    for f in files:
        df = pd.read_parquet(f)
        dfs.append(df)
        print(f"  → {f.name}: {len(df):,} Zeilen")

    df_all = pd.concat(dfs, ignore_index=True)
    print(f"✅ Gesamtdatensatz: {len(df_all):,} Zeilen")

    # Optional: nur relevante Spalten behalten
    keep_cols = [
        "BETRIEBSTAG", "BETREIBER_NAME", "PRODUKT_ID", "LINIEN_TEXT",
        "HALTESTELLEN_NAME", "ANKUNFTSZEIT", "ABFAHRTSZEIT", "delay_arrival_s", "delay_departure_s",
        "on_time", "FAELLT_AUS_TF", "BPUIC"
    ]
    df_all = df_all[[c for c in keep_cols if c in df_all.columns]]

    # Speichern
    out_file = OUTPUT_DIR / f"istdata_real_{month}.parquet"
    df_all.to_parquet(out_file, compression="snappy")
    print(f"💾 Gespeichert unter: {out_file}")

if __name__ == "__main__":
    combine_interim_files()

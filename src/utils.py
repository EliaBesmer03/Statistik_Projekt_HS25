# utils.py
import pyarrow.parquet as pq
import pandas as pd

def load_parquet_safely(path, batch_size=250000):
    """
    Lädt eine Parquet-Datei RAM-schonend.
    Nutzt Arrow-Batches → verhindert Kernel-Crashes.
    """

    parquet_file = pq.ParquetFile(path)
    batches = []

    for batch in parquet_file.iter_batches(batch_size=batch_size):
        # RAM-freundliche Pandas-Konvertierung
        df_chunk = batch.to_pandas(split_blocks=True, self_destruct=True)
        batches.append(df_chunk)

    # Am Ende alle Chunks zusammenfügen
    df = pd.concat(batches, ignore_index=True)

    return df

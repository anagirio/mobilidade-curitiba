"""Calibracao GEH: simulado (M) vs contado (C), em veic/h.
CSV de entrada: via,contado_vph,simulado_vph.  Valido se >=85% das vias tem GEH<5."""
import sys, math, pandas as pd

def geh(m, c):
    return 0.0 if (m + c) == 0 else math.sqrt(2 * (m - c) ** 2 / (m + c))

if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1])
    df["geh"] = [geh(m, c) for m, c in zip(df.simulado_vph, df.contado_vph)]
    pct = (df.geh < 5).mean() * 100
    print(df.round(2).to_string(index=False))
    print(f"\n{pct:.0f}% das vias com GEH<5 ->", "VALIDO" if pct >= 85 else "RECALIBRAR")

"""Painel de KPIs. Rodar: streamlit run dashboard/app.py"""
import glob, json, streamlit as st, pandas as pd
st.title("Mobilidade Urbana: As-Is vs To-Be")
rows = [json.load(open(f)) for f in glob.glob("sim/out/kpis_*.json")]
if rows: st.dataframe(pd.DataFrame(rows).set_index("cenario"))
else: st.info("Rode o As-Is e o To-Be primeiro (veja o README).")

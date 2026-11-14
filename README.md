# Mobilidade Urbana, Sustentabilidade e Sistemas Ciber-Fisicos (Curitiba)

Projeto de Ciencias do Ambiente (UTFPR). Este repositorio e o esqueleto da parte de Computacao.

## Setup
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    export SUMO_HOME="$(python -c 'import sumo; print(sumo.SUMO_HOME)')"

## Estrutura
- `sim/`: rede, rotas e configs do SUMO (hoje com uma grade 4x4 de PLACEHOLDER)
- `control/adaptive_tls.py`: controle semaforico adaptativo via TraCI
- `mqtt/`: integracao com sensores virtuais (Mosquitto)
- `analysis/geh.py`, `analysis/kpis.py`: calibracao GEH e KPIs
- `dashboard/app.py`: painel Streamlit

## Rodar o placeholder
    python control/adaptive_tls.py --no-control   # As-Is (programa fixo)
    python control/adaptive_tls.py                # To-Be (adaptativo)
    python analysis/kpis.py
    streamlit run dashboard/app.py

## Trocar pela rede real do quadrilatero central (M1)
1. Rode `python $SUMO_HOME/tools/osmWebWizard.py` e selecione a area entre Av. Pres. Kennedy,
   Calcadao da XV, Av. Mal. Floriano Peixoto, Al. Dr. Muricy/Martim Afonso, R. Mariano Torres
   e Av. Mario Tourinho (ou baixe o .osm e use `netconvert --osm-files x.osm -o sim/curitiba.net.xml --tls.guess`).
2. Confira no QGIS e ajuste faixas, sentidos e semaforos.
3. Gere a demanda para os picos 06:30-09:00 e 17:00-19:00 com as contagens do IPPUC/URBS e calibre com `analysis/geh.py`.
4. Crie o tipo `brt` no `.rou.xml` (vClass="bus") para ativar a prioridade no controlador.

## Contrato de dados (JSON)
Ver secao 5 do manual: timestamp, intersection_id, sensors[], instantaneous_metrics.

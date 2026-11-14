# Plano de Trabalho: Mobilidade Urbana, Sustentabilidade e Sistemas Ciber-Fisicos

**Unidade curricular:** Ciencias do Ambiente (UTFPR)
**Area de atuacao:** Engenharia de Computacao (modelagem, simulacao e dados)
**Area de estudo:** quadrilatero central de Curitiba (Av. Pres. Kennedy, Calcadao da XV de Novembro, Av. Mal. Floriano Peixoto, Al. Dr. Muricy / Martim Afonso, R. Mariano Torres, Av. Mario Tourinho)
**Janelas de pico analisadas:** 06:30 a 09:00 e 17:00 a 19:00
**Ultima atualizacao:** 13/11/2026

---

## 1. Resumo do que ja foi feito

- [x] Leitura do manual do projeto e levantamento dos requisitos da Computacao.
- [x] Estrutura do repositorio criada (`sim/`, `control/`, `mqtt/`, `dashboard/`, `analysis/`, `docs/`).
- [x] Ambiente Python configurado (`.venv`, `requirements.txt`: SUMO, TraCI, sumolib, pandas, Streamlit, paho-mqtt).
- [x] **Rede de teste (placeholder):** grade 4x4 sintetica em `sim/placeholder.net.xml`, com 16 cruzamentos semaforizados, usada apenas para validar o pipeline.
- [x] **Demanda de teste:** 1.500 veiculos em 30 min (`sim/routes.rou.xml`, gerada com `randomTrips.py`, semente 42).
- [x] **Controlador adaptativo** (`control/adaptive_tls.py`): TraCI/Python, verde minimo de 10 s e maximo de 45 s, decisao pela fila (pressao simplificada) e prioridade para veiculo do tipo `brt`.
- [x] **Calibracao GEH** (`analysis/geh.py`): calcula o GEH por via e verifica o criterio de 85% das vias com GEH < 5.
- [x] **KPIs** (`analysis/kpis.py`): tempo de viagem, atraso medio e CO2 total a partir do `tripinfo.xml`.
- [x] Esqueletos de integracao: `mqtt/subscriber.py` (broker Mosquitto) e `dashboard/app.py` (Streamlit).
- [x] Pipeline validado de ponta a ponta no computador local (As-Is e To-Be rodando).
- [x] Wizard de importacao do OpenStreetMap (`osmWebWizard.py`) aberto e testado.

### Resultado do teste do pipeline (rede sintetica, NAO usar no relatorio)

| Cenario | Fila media (veiculos parados) | Velocidade media |
|---|---|---|
| As-Is (semaforo fixo) | 30,2 | 6,4 m/s |
| To-Be (adaptativo) | 8,9 | 8,6 m/s |

Estes numeros servem so para provar que a cadeia simular, controlar, medir e comparar funciona. Eles nao descrevem Curitiba.

---

## 2. O que falta, por marco (CDIO)

### M1: Conceber (diagnostico e arquitetura de dados)

- [ ] Gerar a rede real do quadrilatero no `osmWebWizard.py` (area pequena, carros e onibus; desmarcar "Add Polygons").
- [ ] Revisar a rede no SUMO-GUI / `netedit`: sentidos das vias, faixas, semaforos nos cruzamentos.
- [ ] Conferir o recorte no QGIS e anexar o mapa viario preliminar ao relatorio.
- [ ] Levantar dados abertos: Portal de Dados Abertos da Prefeitura (URBS e IPPUC), itinerarios do BRT, shapefiles viarios.
- [ ] Obter contagens de veiculos por via (IPPUC/URBS ou contagem manual de VPD).
- [ ] Combinar com Eletrica/Automacao e Mecanica o **contrato de dados JSON** (secao 4).
- [ ] Redigir o relatorio tecnico do M1 (diagnostico, mapa preliminar, arquitetura logica de dados).

**Entregavel M1:** relatorio de diagnostico ambiental, mapa viario preliminar e arquitetura logica de dados.

### M2: Desenhar (cenario As-Is calibrado)

- [ ] Montar a demanda real para os picos 06:30 a 09:00 e 17:00 a 19:00.
- [ ] Rodar o As-Is (`--no-control`) na rede real.
- [ ] Calibrar com `analysis/geh.py` ate **>= 85% das vias com GEH < 5**.
- [ ] Alinhar com a Mecanica o perfil da frota (flex, diesel comercial, hibridos/eletricos, transporte publico) e o modelo de emissoes (PHEMlight ou HBEFA).
- [ ] Calcular pegada de carbono e poluentes do cenario de referencia nas janelas de pico.

**Entregavel M2:** arquivos do cenario base calibrado no SUMO e memorial de calculo ambiental.

### M3: Implementar (controle e integracao)

- [ ] Adaptar `control/adaptive_tls.py` para a rede real (fases reais, prioridade BRT com o tipo `brt` definido no `.rou.xml`).
- [ ] Implementar onda verde adaptativa nos corredores principais.
- [ ] Integrar MQTT: `mqtt/subscriber.py` recebe os sensores virtuais (Wokwi/Node-RED) e repassa a ocupacao ao controlador.
- [ ] Definir os topicos MQTT e documentar o diagrama de malha fechada.
- [ ] Modelar o fluxo de modais ativos (travessia de pedestres no Calcadao da XV, faixas exclusivas para ciclistas).

**Entregavel M3:** repositorio de codigo com algoritmos de controle, integracao MQTT e esquematicos dos sensores.

### M4: Operar (cenario To-Be e comparacao)

- [ ] Rodar o To-Be na rede real com as intervencoes.
- [ ] Comparar As-Is vs To-Be: reducao de filas, atraso por veiculo, velocidade media da rede.
- [ ] Consolidar com a Mecanica a reducao percentual de GEE e material particulado, e com o grupo a estimativa de ruido.
- [ ] Finalizar o painel de KPIs (Streamlit) com os dois cenarios.
- [ ] Escrever o artigo ou relatorio executivo e preparar a defesa em banca.

**Entregavel M4:** artigo/relatorio com a comparacao dos cenarios, analise de viabilidade para Curitiba e defesa multidisciplinar.

---

## 3. Como rodar o que existe hoje

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export SUMO_HOME="$(python -c 'import sumo; print(sumo.SUMO_HOME)')"
mkdir -p sim/out

python control/adaptive_tls.py --no-control   # As-Is (semaforo fixo)
python control/adaptive_tls.py                # To-Be (adaptativo)
python analysis/kpis.py                       # resumo dos KPIs
streamlit run dashboard/app.py                # painel
```

Para usar a rede real, passe `--cfg sim/<pasta_do_cenario>/osm.sumocfg`.

---

## 4. Contrato de dados (JSON) entre subsistemas

Payload emitido pela simulacao de hardware (Automacao) e consumido pelo gerenciador semaforico (Computacao) e pelo modelo de emissoes (Mecanica):

```json
{
  "timestamp": "2026-08-21T17:30:00Z",
  "intersection_id": "cruzamento_rua_xv_floriano",
  "sensors": [
    { "sensor_id": "sensor_indutivo_lane_1", "state": "occupied", "vehicle_speed_kmh": 14.5 }
  ],
  "instantaneous_metrics": {
    "queue_length_meters": 32.0,
    "co2_grams_per_second": 12.4
  }
}
```

Topicos MQTT propostos (a validar com o grupo): `curitiba/<intersection_id>/sensors` e `curitiba/<intersection_id>/metrics`.

---

## 5. Criterios de avaliacao e onde cada um aparece

| Criterio | Peso | Onde atendemos |
|---|---|---|
| Rigor tecnico e calibracao | 30% | `analysis/geh.py`, memorial do M2 |
| Qualidade da solucao de engenharia | 30% | `control/`, `mqtt/`, prioridade BRT e modais ativos |
| Analise de impacto ambiental | 20% | KPIs As-Is vs To-Be, emissoes (Mecanica), ruido |
| Colaboracao e processo | 20% | commits consistentes no Git, documentacao em Markdown (`docs/`) |

---

## 6. Riscos e pendencias

- **Dados de contagem:** sem contagens reais por via nao ha calibracao GEH. Pedir ao professor/IPPUC/URBS o quanto antes.
- **Qualidade do OSM:** sentidos de vias e semaforos podem vir errados; reservar tempo para correcao no `netedit`.
- **Integracao entre areas:** o contrato JSON precisa ser fechado no M1 para ninguem ficar bloqueado.
- **Prazo:** o manual cita "Semestre Letivo 2026/1" no cabecalho, mas o arquivo e de 2026_2. Confirmar datas dos marcos com o professor.

## 7. Divisao de responsabilidades

| Area | Responsavel | Entregas principais |
|---|---|---|
| Computacao | Ana Luisa Girio | SUMO, TraCI, painel de KPIs, GEH |
| Eletrica e Automacao | _(nome)_ | Sensores IoT, malha fechada, MQTT/Wokwi/Node-RED |
| Mecanica | _(nome)_ | Emissoes (PHEMlight/HBEFA), frota, ruido |

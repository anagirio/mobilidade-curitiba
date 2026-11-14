"""Controle semaforico adaptativo via TraCI (pressao simplificada + prioridade BRT).

Uso: python control/adaptive_tls.py [--cfg sim/placeholder.sumocfg] [--no-control]
A cada MIN_GREEN segundos decide se estende a fase verde atual ou avanca,
comparando a fila (veiculos parados) nas vias com verde x vias com vermelho.
"""
import argparse, json, os, sys
import traci

MIN_GREEN, MAX_GREEN = 10, 45
BRT_VTYPE = "brt"  # tipo de veiculo que recebe prioridade


def lane_queue(lane):
    return traci.lane.getLastStepHaltingNumber(lane)


def phase_pressure(tls, state):
    """Soma fila nas lanes controladas com verde (g/G) e com vermelho (r)."""
    links = traci.trafficlight.getControlledLinks(tls)
    green = red = 0
    brt_waiting = False
    for i, ch in enumerate(state):
        if not links[i]:
            continue
        in_lane = links[i][0][0]
        q = lane_queue(in_lane)
        if ch in "gG":
            green += q
        elif ch == "r":
            red += q
        if ch == "r":
            for v in traci.lane.getLastStepVehicleIDs(in_lane):
                if traci.vehicle.getTypeID(v) == BRT_VTYPE:
                    brt_waiting = True
    return green, red, brt_waiting


def step_controller(tls, last_switch, t):
    prog = traci.trafficlight.getAllProgramLogics(tls)[0]
    n = len(prog.phases)
    ph = traci.trafficlight.getPhase(tls)
    state = traci.trafficlight.getRedYellowGreenState(tls)
    if "y" in state.lower() or "G" not in state.upper().replace("g", "G"):
        return last_switch  # nao interrompe amarelo
    elapsed = t - last_switch
    if elapsed < MIN_GREEN:
        return last_switch
    green, red, brt = phase_pressure(tls, state)
    if elapsed >= MAX_GREEN or brt or red > green + 1:
        traci.trafficlight.setPhase(tls, (ph + 1) % n)
        return t
    return last_switch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cfg", default="sim/placeholder.sumocfg")
    ap.add_argument("--no-control", action="store_true", help="roda As-Is (programa fixo)")
    ap.add_argument("--out", default="sim/out/kpis.json")
    a = ap.parse_args()

    os.makedirs("sim/out", exist_ok=True)

    traci.start(["sumo", "-c", a.cfg, "--no-step-log", "true"])
    tls_ids = traci.trafficlight.getIDList()
    last = {t: 0 for t in tls_ids}
    queue_samples, speed_samples = [], []
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        t = traci.simulation.getTime()
        if not a.no_control:
            for tls in tls_ids:
                last[tls] = step_controller(tls, last[tls], t)
        if int(t) % 10 == 0:
            ids = traci.vehicle.getIDList()
            if ids:
                queue_samples.append(sum(traci.vehicle.getSpeed(v) < 0.1 for v in ids))
                speed_samples.append(sum(traci.vehicle.getSpeed(v) for v in ids) / len(ids))
    traci.close()
    k = {
        "cenario": "As-Is" if a.no_control else "To-Be",
        "fila_media_veic": sum(queue_samples) / max(len(queue_samples), 1),
        "velocidade_media_ms": sum(speed_samples) / max(len(speed_samples), 1),
    }
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(k, open(a.out.replace(".json", f"_{k['cenario']}.json"), "w"), indent=2)
    print(k)


if __name__ == "__main__":
    sys.exit(main())

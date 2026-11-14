"""Le tripinfo.xml do SUMO e resume tempo de viagem, atraso e emissao total de CO2."""
import sys, xml.etree.ElementTree as ET, statistics as st

def main(tripinfo="sim/out/tripinfo.xml"):
    t = ET.parse(tripinfo).getroot().findall("tripinfo")
    dur = [float(x.get("duration")) for x in t]
    loss = [float(x.get("timeLoss")) for x in t]
    co2 = [float(e.get("CO2_abs", 0)) for x in t for e in x.findall("emissions")]
    print(f"veiculos: {len(t)} | viagem media: {st.mean(dur):.1f}s | atraso medio: {st.mean(loss):.1f}s")
    if co2: print(f"CO2 total: {sum(co2)/1e6:.2f} kg")

if __name__ == "__main__":
    main(*sys.argv[1:])

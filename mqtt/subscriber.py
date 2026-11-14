"""Esqueleto MQTT: recebe sensores virtuais (Automacao) e publica metricas (Computacao).
Broker local: mosquitto -v   (porta 1883). Topicos: curitiba/<intersection_id>/sensors|metrics"""
import json, paho.mqtt.client as mqtt

def on_message(c, u, msg):
    p = json.loads(msg.payload)
    print(msg.topic, p.get("intersection_id"), len(p.get("sensors", [])), "sensores")
    # TODO M3: repassar ocupacao ao controlador (control/adaptive_tls.py)

if __name__ == "__main__":
    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    c.on_message = on_message
    c.connect("localhost", 1883)
    c.subscribe("curitiba/+/sensors")
    c.loop_forever()

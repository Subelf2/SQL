import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc, props=None):
    print(f"Connected with result code {rc}")
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print(f"Message received: {msg.topic} {msg.payload.decode()}")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # Removed the invalid argument

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)
mqttc.publish("test/topic", "Ca va Madin ?", retain=True)
mqttc.loop_forever()

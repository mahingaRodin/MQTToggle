import paho.mqtt.client as mqtt
import threading
import time
import sys

# MQTT Configuration
BROKER_ADDRESS = "broker.emqx.io"
PORT = 1883
TOPIC = "/student_group/light_control"
CLIENT_ID = "python_iot_simulator_v2"

# Light state
light_state = "OFF"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
        client.subscribe(TOPIC)
        print(f"📡 Subscribed to {TOPIC}")
    else:
        print(f"❌ Connection failed with code {rc}")
        sys.exit(1)

def on_message(client, userdata, msg):
    global light_state
    message = msg.payload.decode().strip()
    print(f"📩 Received: {message}")
    
    if message in ["ON", "OFF"]:
        light_state = message
        print(f"💡 Light is now {light_state}")
    else:
        print(f"⚠️ Unknown command: {message}")

def publish_messages(client):
    while True:
        user_input = input("Enter command (ON/OFF/EXIT): ").strip().upper()
        if user_input in ["ON", "OFF"]:
            client.publish(TOPIC, user_input)
            print(f"📤 Sent: {user_input}")
        elif user_input == "EXIT":
            print("🛑 Exiting...")
            client.disconnect()
            sys.exit(0)
        else:
            print("⚠️ Invalid command. Use ON, OFF, or EXIT.")

client = mqtt.Client(client_id=CLIENT_ID, callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message

try:
    print(f"🔄 Connecting to MQTT broker at {BROKER_ADDRESS}...")
    client.connect(BROKER_ADDRESS, PORT, 60)
    threading.Thread(target=publish_messages, args=(client,), daemon=True).start()
    client.loop_forever()
except KeyboardInterrupt:
    print("\n🛑 Stopped by user")
    client.disconnect()
    sys.exit(0)

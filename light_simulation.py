import paho.mqtt.client as mqtt

#callback when the client connects to the broker 
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe('/student_group/light_control') 
        print("Done")
    else:
        print(f"Connection failed with code {rc}")

#callback when a message is received
def on_message(client, userdata, msg):
    command = msg.payload.decode('utf-8')
    if command == "ON":
        print("💡 Light is TURNED ON")
    elif command == "OFF":
        print("💡 Light is TURNED OFF")
    else:
        print(f"Unknown command: {command}")

#set up the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#connect to the broker 
broker = "localhost"
port = 1883
client.connect(broker, port)

#start the loop to listen for Messages
client.loop_forever()
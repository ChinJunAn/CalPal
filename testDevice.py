import paho.mqtt.client as mqtt
from time import sleep
import json
import base64

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    sleep(2);
    sendData()

def sendData():
    # Path to the image file
    image_path = "../pics/apple.jpg"

    # Read the image file as binary data
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    struct_data = {
        "pic":image_base64,
        "weight":500
    }

    # Serialize the struct to JSON
    data = json.dumps(struct_data)
    print("Sending pic and weight.")
    client.publish("pic/esp", payload=data, qos=1)

client = mqtt.Client()
client.on_connect = on_connect
client.connect("localhost", 1883, 60)
client.loop_forever()



import paho.mqtt.client as mqtt
from PIL import Image
from io import BytesIO
import os
import base64
import json

def on_connect(client, userdata, flags, rc):
	print("Connected with result code: " + str(rc))
	client.subscribe("pic/esp")

def on_message(client, userdata, message):
	print("received something")

	# receive a tuple = (imageData, weight)
	data = message.payload
	struct_data = json.loads(data)
	
	# Save image in a file
	image_bytesio = BytesIO(base64.b64decode(struct_data["pic"]))
	img = Image.open(image_bytesio)
	# Save the image as a JPEG file
	try:
		os.remove('/Picture/test.jpg')
	except OSError:
		pass
	img.save("Picture/test.jpg", "JPEG")

	# Save weight somewhere
	weight = struct_data["weight"]

def connectMQTT():
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("localhost", 1883, 60)
	client.loop_forever()
import paho.mqtt.client as mqtt
from PIL import Image
from io import BytesIO
import os
import base64
import json
import variables

def on_connect(client, userdata, flags, rc):
	print("Connected with result code: " + str(rc))
	client.subscribe("pic/esp")

def on_message(client, userdata, message):
	print("received something")

	# receive a tuple = (imageData, weight)
	data = message.payload
	struct_data = json.loads(data)

	# Save weight somewhere
	weight = struct_data["weight"]

	# Save image in a file
	image_bytesio = BytesIO(base64.b64decode(struct_data["pic"]))
	img = Image.open(image_bytesio)

	# Save the image as a JPEG file
	try:
		files = os.listdir(variables.image_dir)
		for file in files:
			file_path = os.path.join(variables.image_dir, file)
			try:
				if os.path.isfile(file_path):
					os.remove(file_path)
			except Exception as e:
				print(f"Error deleting file: {file_path} - {e}")
	except OSError:
		pass
	img_name = variables.image_dir+str(weight)+".jpg"
	img.save(img_name, "JPEG")

def connectMQTT():
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("localhost", 1883, 60)
	client.loop_forever()

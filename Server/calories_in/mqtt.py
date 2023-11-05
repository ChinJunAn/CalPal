import paho.mqtt.client as mqtt
from PIL import Image, ImageFile
from io import BytesIO
import os
import base64
import json
import calories_in.variables as variables

def save_for_classify(img, weight):
	# Save the image as a JPEG file in calories_in/picture
	try:
		files = os.listdir(variables.image_dir_from_mqtt)
		for file in files:
			file_path = os.path.join(variables.image_dir_from_mqtt, file)
			try:
				if os.path.isfile(file_path):
					os.remove(file_path)
			except Exception as e:
				print(f"Error deleting file: {file_path} - {e}")
	except OSError:
		pass
	img_name = variables.image_dir_from_mqtt+str(weight)+".jpg"
	img.save(img_name, "JPEG")

def save_for_static(img):
	# Save the image as a JPEG file in Server/static
	try:
		file_path = os.path.join(variables.image_dir_from_static, "picture.jpg")
		try:
			if os.path.isfile(file_path):
				os.remove(file_path)
		except Exception as e:
				print(f"Error deleting file: {file_path} - {e}")			
	except OSError:
		pass
	img_name = variables.image_dir_from_static+"picture.jpg"
	img.save(img_name, "JPEG")

def on_connect(client, userdata, flags, rc):
	print("Connected with result code: " + str(rc))
	client.subscribe("esp/cam")

def on_message(client, userdata, message):
	ImageFile.LOAD_TRUNCATED_IMAGES = True
	print("received something")

	# receive a tuple = (imageData, weight)
	data = message.payload
	#struct_data = json.loads(data)

	# Save weight somewhere
	#weight = struct_data["weight"]
	weight = 500

	# Save image in a file
	#image_bytesio = BytesIO(base64.b64decode(struct_data["pic"]))
	image_bytesio = BytesIO(base64.b64decode(data))
	img = Image.open(image_bytesio)

	save_for_classify(img, weight)
	save_for_static(img)

def connectMQTT():
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("localhost", 1883, 60)
	client.loop_forever()
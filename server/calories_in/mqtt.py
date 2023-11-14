import paho.mqtt.client as mqtt
from PIL import Image, ImageFile
from io import BytesIO
import os
import base64
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
	# Save the image as a JPEG file in server/static
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
	print("MQTT for Calories-In connected: " + str(rc))
	client.subscribe("esp/cam")

def on_message(client, userdata, message):
	ImageFile.LOAD_TRUNCATED_IMAGES = True
	print("received something from Calories-In")

	data = str(message.payload.decode("utf-8"))
	imageData, weight = data.split("\n")

	# Save image in a file
	image_bytesio = BytesIO(base64.b64decode(imageData))
	img = Image.open(image_bytesio)

	save_for_classify(img, weight)
	save_for_static(img)

def connectCIMQTT():
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("localhost", 1883, 60)
	client.loop_forever()
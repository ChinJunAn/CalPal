#to receive messages
import paho.mqtt.client as mqtt
import csv
import calories_out.variables as variables

def on_connect(client, userdata, flags, rc):
	print("MQTT for Calories-Out: " + str(rc))
	client.subscribe("esp/imu")

def on_message(client, userdata, message):
	print("received something from Calories-Out")
	data = str(message.payload.decode("utf-8"))
	lines = data.split("\n")
	with open(variables.csv_file_path, 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
		for line in lines:
			# Split each line into a list containing a single element
			csvwriter.writerow(line.split(','))

def connectCOMQTT():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_forever()
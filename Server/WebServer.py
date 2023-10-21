from flask import Flask, request, render_template
from Classifier import caloriesInFunc
from MQTT import connectMQTT
import os
import threading
import Variables
# Create the Flask object
app = Flask(__name__, static_url_path='/static')

item = "Place food on smart plate"
weight = ""
calories_in = "Then click on the \"Calories-In\" button"
activity = "Go for a run with the activity tracker"
duration = ""
calories_out = "Then click on the \"Calories-Out\" button"
net_calories = "Get both Calories-In and Calories-Out first!!"

template_data = {
    "food": item,
    "weight": weight,
    "caloriesIn": calories_in,
    "activity": activity,
    "duration": duration,
    "caloriesOut": calories_out,
    "netCalories": net_calories
}
def updateTemplateData(item, weight, calories_in, activity, duration, calories_out, net_calories):
    global template_data
    template_data = {
        "food": item,
        "weight": weight,
        "caloriesIn": calories_in,
        "activity": activity,
        "duration": duration,
        "caloriesOut": calories_out,
        "netCalories": net_calories
    }

calories_in_flag = False
calories_out_flag = False
def updateNetCalories():
    global net_calories, calories_in_flag, calories_out_flag
    if calories_in_flag and calories_out_flag:
        global net_calories
        net_calories = str(float(calories_in) - float(calories_out))

@app.route('/')
def root():
    return render_template('index.html', info = template_data), 200

@app.route('/Calories_In')
def caloriesIn():
    try:    
        results = caloriesInFunc(Variables.image_dir)
        if results is not None:
            global item, weight, calories_in, calories_in_flag
            item, weight, calories_in = results
            calories_in_flag = True
        updateNetCalories()
        updateTemplateData(item, weight, calories_in, activity, duration, calories_out, net_calories)
        return render_template('index.html', info = template_data), 200
    except Exception as e:
        return render_template('index.html', info = {"title":"No item found ", "name":e}), 200

@app.route('/Calories_Out')
def caloriesOut():
    try:
        #activty, duration, calories_out = caloriesOutFunc()
        return render_template('index.html', info = template_data), 200
    except Exception as e:
        return render_template('index.html', info = {"title":"No item found ", "name":e}), 200

def main():
    global client, db, col, app
    thread = threading.Thread(target=connectMQTT)
    thread.start()
    app.run(port = 3237)

if __name__ == '__main__':
    main()

'''
# Examples of how to render a template. Also note
# how we use requests.args.get to extract GET parameters
@app.route('/index', methods = ['GET'])
def index():
    """ Demo routine to show how to pass parameters through GET """

    # Extract GET parameters from request object
    name = request.args.get('name')

    if name is None:
        name = 'Bob Jones'

    return render_template('index.html', info = {"title":"Hello World", "name":name}), 200
'''
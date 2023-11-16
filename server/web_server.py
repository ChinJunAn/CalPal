from flask import Flask, request, render_template
from calories_in.classifier import caloriesInFunc
from calories_out.classifier import calculate_calories_burned
from calories_in.mqtt import connectCIMQTT
from calories_out.mqtt import connectCOMQTT
import threading
import calories_in.variables as ciVariables
import calories_out.variables as coVariables
# from calories_out.variables import CNNPhysicalActivityClassifier
import database_utility
import aggregate

# Create the Flask object
app = Flask(__name__, static_url_path='/static')

item = "Place food on smart plate"
weight = " "
calories_in = "Then click on the \"Calories-In\" button"
activity = "Sit, walk, or run with the activity tracker"
calories_out = "Then click on the \"Calories-Out\" button"
duration = " "
net_calories = "Get both Calories-In and Calories-Out first!!"

template_data = {
    "food": item,
    "weight": weight,
    "caloriesIn": calories_in,
    "activity": activity,
    "caloriesOut": calories_out,
    "duration": duration,
    "netCalories": net_calories
}
def updateTemplateData(item, weight, calories_in, activity, calories_out, duration, net_calories):
    global template_data
    template_data = {
        "food": item,
        "weight": weight,
        "caloriesIn": calories_in,
        "activity": activity,
        "caloriesOut": calories_out,
        "duration": duration,
        "netCalories": net_calories
    }

def updateNetCalories():
    global net_calories
    print(database_utility.checkAggregate())
    if database_utility.checkAggregate():
        global net_calories
        calories_in_fromdb = database_utility.getTotalCaloriesIn()
        calories_out_fromdb = database_utility.getTotalCaloriesOut()
        print(calories_in_fromdb, calories_out_fromdb)
        net_calories = aggregate.inform(round(calories_in_fromdb - calories_out_fromdb,2))
    else:
        net_calories = "Get both Calories-In and Calories-Out first!!"

@app.route('/')
def root():
    #update graph
    database_utility.updateGraph()
    return render_template('index.html', info = template_data), 200

@app.route('/Calories_In')
def caloriesIn():
    try:    
        results = caloriesInFunc(ciVariables.image_dir_from_webserver)
        if results is not None:
            global item, weight, calories_in
            item, weight, calories_in = results
        # insert into db
        database_utility.insertCaloriesIn(calories_in, item)
        # update graph
        database_utility.updateGraph()
        updateNetCalories()
        updateTemplateData(item, weight, calories_in, activity, calories_out, duration, net_calories)
        return render_template('index.html', info = template_data), 200
    except Exception as e:
        return render_template('error.html', info = {"title":"No item found ", "name":e}), 200

@app.route('/Revert_Calories_In')
def revertCaloriesIn():
    database_utility.revertCaloriesIn()
    database_utility.updateGraph()
    updateNetCalories()
    updateTemplateData(item, weight, calories_in, activity, calories_out, duration, net_calories)
    return render_template('index.html', info = template_data), 200

@app.route('/Calories_Out')
def caloriesOut():
    try:
        results = calculate_calories_burned(coVariables.real_time_accelerometer_data_path)
        print(results)
        if results is not None:
            global calories_out, duration, activity
            calories_out, duration, activity = results

        database_utility.insertCaloriesOut(calories_out, activity)
        database_utility.updateGraph()
        updateNetCalories()
        updateTemplateData(item, weight, calories_in, activity, calories_out, duration, net_calories)
        return render_template('index.html', info = template_data), 200
    except Exception as e:
        return render_template('error.html', info = {"title":"No item found ", "name":e}), 200

@app.route('/Revert_Calories_Out')
def revertCaloriesOut():
    database_utility.revertCaloriesOut()
    database_utility.updateGraph()
    updateNetCalories()
    return render_template('index.html', info = template_data), 200

def main():
    #start db
    database_utility.createDB()
    thread = threading.Thread(target=connectCIMQTT)
    thread.start()
    thread = threading.Thread(target=connectCOMQTT)
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
from flask import Flask, request, render_template
from calories_in.classifier import caloriesInFunc
from calories_in.mqtt import connectCIMQTT
from calories_out.mqtt import connectCOMQTT
import threading
import calories_in.variables as ciVariables
import calories_out.variables as coVariables
import database_utility
import aggregate
# Create the Flask object
app = Flask(__name__, static_url_path='/static')

item = "Place food on smart plate"
weight = " "
calories_in = "Then click on the \"Calories-In\" button"
activity = "Go for a run with the activity tracker"
duration = " "
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
        net_calories = aggregate.inform(float(calories_in) - float(calories_out))

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
            global item, weight, calories_in, calories_in_flag
            item, weight, calories_in = results
            calories_in_flag = True
        updateNetCalories()
        updateTemplateData(item, weight, calories_in, activity, duration, calories_out, net_calories)
        #insert into db
        database_utility.insertCaloriesIn(calories_in, item)
        #update graph
        database_utility.updateGraph()
        return render_template('index.html', info = template_data), 200
    except Exception as e:
        return render_template('error.html', info = {"title":"No item found ", "name":e}), 200

@app.route('/Revert_Calories_In')
def revertCaloriesIn():
    database_utility.revertCaloriesIn()
    #update graph
    database_utility.updateGraph()
    return render_template('index.html', info = template_data), 200

@app.route('/Calories_Out')
def caloriesOut():
    try:
        #results = caloriesOutFunc() --> PLS DO THIS FUNCTION SOKHNA :))))
        # if results is not None:
        #     global item, weight, calories_in, calories_in_flag
        #     item, weight, calories_in = results
        #     calories_in_flag = True

        #test codes
        global calories_out_flag, calories_out
        calories_out = 20
        calories_out_flag = True
        updateNetCalories()
        updateTemplateData(item, weight, calories_in, activity, duration, calories_out, net_calories)
        
        return render_template('index.html', info = template_data), 200
    except Exception as e:
        return render_template('error.html', info = {"title":"No item found ", "name":e}), 200

@app.route('/Revert_Calories_Out')
def revertCaloriesOut():
    database_utility.revertCaloriesOut()
    #update graph
    database_utility.updateGraph()
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
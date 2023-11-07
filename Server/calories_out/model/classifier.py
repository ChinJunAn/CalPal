import pandas as pd
import numpy as np
import torch
import server.calories_out.model.variables as variables

# TODO: modify data input 
data = pd.read_csv('calories_out/real_time_accelerometer_data.csv')

# assumption is user weight == 65 kg (average human weight)
def calculate_calories_burned():
    met = classify_physical_activity(data[-1])
    activity_duration = 5
    total_calories_burned = (met * 3.5 * 65 / 200) * activity_duration
    print(total_calories_burned) # change to return later 

def classify_physical_activity(accelerometer_data):
    met_values = variables.met_values
    model = torch.load(variables.model)
   
    return met_values[predicted_physical_activity.item()] # met value for physical activity



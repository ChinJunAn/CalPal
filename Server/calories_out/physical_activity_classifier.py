import pandas as pd
import numpy as np
import server.calories_out.calories_out_variables as variables



def classify_physical_activity():
    met_value = variables.met_values
    # TODO: build model to classify physical activity type





    return met_value[predicted_physical_activity.item()]


def calculate_calories_burned(met, user_weight, activity_duration, heart_rate_bpm):
    # TODO: modify these based on calculations or average, widely-accepted values 
    resting_heart_rate = 80
    max_heart_rate = 80
    
    # Calculate calories burned without heart rate adjustment
    calories_burned_without_heart_rate = (met * 3.5 * user_weight / 200) * activity_duration
    heart_rate_factor = (heart_rate_bpm - resting_heart_rate) / max_heart_rate
    # Adjust calories using the heart rate factor
    calories_with_heart_rate = calories_burned_without_heart_rate * heart_rate_factor

    return calories_with_heart_rate



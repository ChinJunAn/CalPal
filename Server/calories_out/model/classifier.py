from collections import Counter
import os
import pandas as pd
import numpy as np
import torch
import torch.nn.functional as F
from physical_activity_model import CNNPhysicalActivityClassifier
import variables

curr_directory = os.path.dirname(os.path.realpath(__file__))
server_directory = os.path.abspath(os.path.join(curr_directory, '..', '..'))
csv_file_path = os.path.join(server_directory, 'calories_out', 'real_time_accelerometer_data.csv')
data = pd.read_csv(csv_file_path)


model = CNNPhysicalActivityClassifier()

def calculate_total_time_elapsed(data):
    timestamps_ms = data.iloc[:, 0]
    total_time_ms = timestamps_ms.iloc[-1] - timestamps_ms.iloc[0]
    total_time_minutes = total_time_ms / (1000 * 60)
    return total_time_minutes

# assume user weight == 65 kg (average human weight)
def calculate_calories_burned(accelerometer_data):
    met = classify_physical_activity(accelerometer_data, model)
    activity_duration = calculate_total_time_elapsed(accelerometer_data)
    total_calories_burned = (((met * 3.5 * 65) / 200) * activity_duration)
    return f'You have burned a total of {total_calories_burned} calories.'

def classify_physical_activity(accelerometer_data, model):
    model.eval()
    input_data = []

    for entry in accelerometer_data:
        values = entry.split(',')
        input_point = [float(value) for value in values]
        input_data.append(input_point)

    input_data = torch.tensor(input_data, dtype=torch.float32)

    # Transpose to match the expected shape (batch_size, channels, sequence_length)
    input_data = input_data.transpose(1, 0).unsqueeze(1)
    
    with torch.no_grad():
        outputs = model(input_data)
    
    predictions = F.softmax(outputs, dim=1)
    _, predicted_labels = torch.max(predictions, 1)

    predicted_labels = predicted_labels.tolist()
    most_frequent_label = Counter(predicted_labels).most_common(1)[0][0]

    class_labels = ['sitting', 'walking', 'running']
    most_frequent_activity = class_labels[most_frequent_label]
    met_value = variables.met_values.get(most_frequent_activity, 1.0)
    return met_value

print(calculate_calories_burned(data))
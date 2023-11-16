from collections import Counter
import pandas as pd
import torch
import torch.nn.functional as F
import calories_out.variables as variables

def calculate_total_time_elapsed(data):
    data_no_nan = data.dropna()
    if data_no_nan.empty:
        return 0.0
    timestamps_ms = data_no_nan.iloc[:, 0]
    total_time_ms = timestamps_ms.iloc[-1] - timestamps_ms.iloc[0]
    total_time_minutes = total_time_ms / (1000 * 60)
    return round(total_time_minutes, 2)

def classify_physical_activity(accelerometer_data):
    model = torch.load(variables.model)
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

    class_labels = ['Sitting', 'Walking', 'Running']
    most_frequent_activity = class_labels[most_frequent_label]
    met_value = variables.met_values.get(most_frequent_activity, 1.0)
    return met_value, most_frequent_activity

# assume user weight == 65 kg (average human weight)
def calculate_calories_burned(path):
    accelerometer_data = pd.read_csv(path)
    met, activity = classify_physical_activity(accelerometer_data)
    activity_duration = calculate_total_time_elapsed(accelerometer_data)
    total_calories_burned = (((met * 3.5 * 65) / 200) * activity_duration)
    return total_calories_burned, activity_duration, activity
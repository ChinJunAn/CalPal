import pandas as pd
import calories_out.variables as variables

def calculate_total_time_elapsed(data):
    data_no_nan = data.dropna()
    if data_no_nan.empty:
        return 0.0
    timestamps_ms = data_no_nan.iloc[:, 0]
    total_time_ms = timestamps_ms.iloc[-1] - timestamps_ms.iloc[0]
    total_time_minutes = total_time_ms / (1000 * 60)
    return round(total_time_minutes, 2)

def classify_physical_activity(data):
    row_diff_abs  = data.diff().abs().iloc[:, -3:]
    row_sums = row_diff_abs.sum(axis=1) / 500
    average_sum = row_sums.mean()

    if average_sum < variables.walk_ave_acc[0]:
        return variables.met_values["Sitting"], "Sitting"
    elif variables.walk_ave_acc[0] <= average_sum <= variables.walk_ave_acc[1]:
        return variables.met_values["Walking"], "Walking"
    elif variables.walk_ave_acc[1] < average_sum:
        return variables.met_values["Runningg"], "Running"

# assume user weight == 65 kg (average human weight)
def calculate_calories_burned(path):
    accelerometer_data = pd.read_csv(path)
    activity_duration = calculate_total_time_elapsed(accelerometer_data)
    met, activity = classify_physical_activity(accelerometer_data)
    total_calories_burned = round(((met * 3.5 * 65) / 200) * activity_duration,2)
    return total_calories_burned, activity_duration, activity
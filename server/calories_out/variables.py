#  met values for specific physical activities (per minute)
met_values = {
    "Sitting": 1.8,
    "Walking": 3.55,
    "Running": 7.5
}

# average acceleration for walking
walk_ave_acc = (10, 100)

model = "calories_out/model.pth"
real_time_accelerometer_data_path = "calories_out/data/real_time_accelerometer_data.csv"
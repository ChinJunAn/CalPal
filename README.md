# CalPal: Your guide to better exercise and eating habits
An IoT system created by: Chin Jun An, Fall Sokhna, Keeve Kang, Pulipaka Sai Nandini

# Intro 
  Many individuals grapple with this question: Am I exercising too much and eating too little or am I eating too much and not exercising enough? This is a challenge that many individuals face when striving to improve dietary and exercise habits for better health. Our team is developing an IoT system to help users make informed decisions about their calorie intake and exercise routines. 
  
  This system will help users gauge the time and effort needed to burn off the calories from the food they have consumed. Additionally, it will predict the amount of calories they need to consume based on their exercise routines to promote a healthier and more energized lifestyle. Since what constitutes “healthy and fit” can vary based on individual goals, age, genetics, and preexisting health conditions, it is advisable to consult with a healthcare professional for personalized diet recommendations such as daily calorie intake (doing so will ensure more accurate results for each unique individual). This innovative feature will enable individuals to understand their calorie balance, monitor their exercise routines, manage their diet more effectively, and help them achieve their fitness and weight management goals.

# System Architecture 
<img width="303" alt="Screenshot 2023-10-14 at 8 48 17 PM" src="https://github.com/sokhnarfall/CalPal/assets/84427104/c7a25351-1d59-4bd4-9017-e4cec9cc09d2">

# Sensors /Actuators/Hardware Used
Our IOT system is composed of 2 parts: a Calories-In tracker and a Calories-Out tracker.
The Calorie-In tracker will utilize a weight sensor and a camera to calculate the number of calories a specific fruit or vegetable has.

| Module  | Purpose |
| ------------- | ------------- |
| Digital Load Cell Weight Sensor + HX711 Weighing Sensors Ad Module.  | Determine the weight of the food  |
| ESP32-CAM WiFi + Bluetooth Module Camera  | Capture images for food identification.  |
| Inertial Measurement Unit (IMU) module  | Calculate movement and the corresponding amount of calories burned  |

# Machine Learning Models
Our system uses the CNN model to facilitate the identification of foods. We have found existing datasets that would supplement the training of the model. For better accuracy, we will be capturing and using the images of foods to further improve our model.




import torch.nn as nn
import torch.nn.functional as F

class CNNPhysicalActivityClassifier(nn.Module):
    def __init__(self):
        super(CNNPhysicalActivityClassifier, self).__init__()
        self.conv1 = nn.Conv1d(1, 32, kernel_size=3, padding=1)
        self.maxpool = nn.MaxPool1d(kernel_size=2)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(96, 64)  
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(64, 3)  # 3 output neurons for sitting, walking, running

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.maxpool(x)
        x = self.flatten(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x) 
        return x

#  met values for specific physical activities (per minute)
met_values = {
    "Sitting": 1.8,
    "Walking": 3.55,
    "Running": 7.5
}

model = "calories_out/model.pth"
real_time_accelerometer_data_path = "calories_out/data/real_time_accelerometer_data.csv"
import os
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import calories_out.model.variables as variables

# Load data
# current_directory = os.getcwd()
# file_path = os.path.join(current_directory, 'server/calories_out/model/accelerometer_data.csv')
data = pd.read_csv(variables.accelerometer_data_path)

# label data
X = data[['x_gyro', 'y_gyro', 'z_gyro', 'x_accel', 'y_accel', 'z_accel']]
Y = data['activity']

# transform categorical variables (sitting, walking, running) to numerical values (0, 1, 2)
label_encoder = LabelEncoder()
Y = label_encoder.fit_transform(Y)

# data is normally distributed, apply standard scaler for mean of 0 and SD of 1
scaler = StandardScaler()
X = scaler.fit_transform(X)

X = X.reshape(X.shape[0], 1, X.shape[1])
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=10)

X_train = torch.from_numpy(X_train).float()
y_train = torch.from_numpy(y_train).long()
X_test = torch.from_numpy(X_test).float()
y_test = torch.from_numpy(y_test).long()

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

model = CNNPhysicalActivityClassifier()
optimizer = optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()

# Train the model
# num_epochs = 100
# batch_size = 50

# for epoch in range(num_epochs):
#     for i in range(0, len(X_train), batch_size):
#         inputs = X_train[i:i + batch_size]
#         labels = y_train[i:i + batch_size]
#         optimizer.zero_grad()
#         outputs = model(inputs)
#         loss = criterion(outputs, labels)
#         loss.backward()
#         optimizer.step()

#     if (epoch + 1) % 10 == 0:
#         print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')


model.eval()
with torch.no_grad():
    outputs = model(X_test)
    _, predicted = torch.max(outputs, 1)
    accuracy = (predicted == y_test).sum().item() / len(y_test)

# print(f'Test Accuracy on test data: {accuracy:.4f}')
save_path = '/Users/sokhna/Downloads/CalPal/server/calories_out/model/physical-activity-model.pth'
torch.save(model, save_path)


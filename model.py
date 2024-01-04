import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('sensor_data.csv', names=['sound_sensor', 'motion_sensor', 'current_time', 'heater_status'])

# Convert boolean values to 0 and 1
data['heater_status'] = data['heater_status'].astype(int)

# Split the data into features and labels
X = data[['sound_sensor', 'motion_sensor', 'current_time']].values.astype(np.float32)
y = data['heater_status'].values.astype(np.float32)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert NumPy arrays to PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.FloatTensor(y_train)
X_test_tensor = torch.FloatTensor(X_test)
y_test_tensor = torch.FloatTensor(y_test)

# Define a simple neural network
class HeaterModel(nn.Module):
    def __init__(self):
        super(HeaterModel, self).__init__()
        self.fc = nn.Linear(3, 1)  # 3 input features, 1 output (binary classification)

    def forward(self, x):
        x = torch.sigmoid(self.fc(x))
        return x

# Initialize the model, loss function, and optimizer
model = HeaterModel()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    # Forward pass
    outputs = model(X_train_tensor)
    loss = criterion(outputs.squeeze(), y_train_tensor)

    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Print training loss
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

torch.save(model.state_dict(), 'heater_model.pth')

# Evaluate the model on the test set
with torch.no_grad():
    model.eval()
    predictions = model(X_test_tensor).squeeze().round().numpy()
    accuracy = np.mean(predictions == y_test)
    print(f'Accuracy on test set: {accuracy:.2%}')
    

def predict(new_data_tensor):
    loaded_model = HeaterModel()
    loaded_model.load_state_dict(torch.load('heater_model.pth'))
    loaded_model.eval()
    with torch.no_grad():
        predictions = loaded_model(new_data_tensor).squeeze().round().numpy()

    return predictions
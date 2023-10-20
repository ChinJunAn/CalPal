#second test
from PIL import Image
import os
import torch
from torchvision import transforms
import sys
import Variables

def classifyItem(image_path):
    class_mapping = Variables.class_mapppings
        
    # Load the entire model
    model = torch.load("model.pth")

    # Load and preprocess the new image
    transform = transforms.Compose([
        transforms.Resize((100, 100)),  # Resize as per your model's input size
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalize pixel values to [-1, 1]
    ])

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # Add a batch dimension
    image = image.to(device) # convert data to be GPU suitable

    # Perform inference
    with torch.no_grad():
        outputs = model(image)

    # Convert probabilities to class scores
    class_scores = torch.softmax(outputs, dim=1)

    # Get the predicted class
    _, predicted_class = torch.max(class_scores, 1)

    # Print or use the predicted class and class scores
    print(f'Predicted Class: {predicted_class.item()}')
    print(f'Predicted Class: {class_mapping[predicted_class.item()]}')
    return class_mapping[predicted_class.item()]

def calculateCal(image_file, item):
    calorieTable = Variables.calories_table
    weight = image_file[8:-4]
    return str((calorieTable[item]/100)*float(weight))

if __name__ == "__main__":
    image_path = sys.argv[1]
    classifyItem(image_path)






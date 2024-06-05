import os
import numpy as np
import torch
import glob
import torch.nn as nn
from torchvision import datasets
from torchvision.transforms import transforms
from torch.utils.data import DataLoader
from torch.optim import Adam
from torch.autograd import Variable
import torchvision
import pathlib
from PIL import Image


# Model Tanımı
class YogaPoseCNN(nn.Module):
    def __init__(self, num_classes=5):
        super(YogaPoseCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.relu1 = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2)

        self.conv2 = nn.Conv2d(32, 64, 3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.relu2 = nn.ReLU()

        self.conv3 = nn.Conv2d(64, 128, 3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.relu3 = nn.ReLU()

        self.conv4 = nn.Conv2d(128, 256, 3, stride=1, padding=1)
        self.bn4 = nn.BatchNorm2d(256)
        self.relu4 = nn.ReLU()

        self.gap = nn.AdaptiveAvgPool2d((1, 1))
        self.fc1 = nn.Linear(256, 128)
        self.relu5 = nn.ReLU()
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.pool(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu2(x)
        x = self.pool(x)

        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu3(x)
        x = self.pool(x)

        x = self.conv4(x)
        x = self.bn4(x)
        x = self.relu4(x)
        x = self.gap(x)
        x = x.view(-1, 256)
        x = self.fc1(x)
        x = self.relu5(x)
        x = self.fc2(x)
        return x


# Resim Dönüştürücü
def convert_image(image):
    if image.mode == 'P' or (image.mode == 'RGBA' and image.getextrema()[3][0] < 255):
        return image.convert('RGBA')
    return image


def load_image(path):
    image = Image.open(path)
    image = convert_image(image)
    return image


# Modeli Eğitme
def train_model(data_dir, model_path, num_epochs=10):
    transformer = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation([90, 180]),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])

    train_dataset = datasets.ImageFolder(root=os.path.join(data_dir, 'train'), transform=transformer)
    val_dataset = datasets.ImageFolder(root=os.path.join(data_dir, 'val'), transform=transformer)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

    model = YogaPoseCNN(num_classes=5)  # 109 sınıf
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)

    best_accuracy = 0.0
    patience = 5
    for epoch in range(num_epochs):
        # Eğitim
        model.train()
        train_accuracy = 0.0
        train_loss = 0.0
        for i, (images, labels) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.cpu().data * images.size(0)
            _, prediction = torch.max(outputs.data, 1)
            train_accuracy += int(torch.sum(prediction == labels.data))
        train_accuracy = train_accuracy / len(train_dataset)
        train_loss = train_loss / len(train_dataset)

        # Değerlendirme
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        val_accuracy = 100 * correct / total
        print(
            f'Epoch [{epoch + 1}/{num_epochs}], Train Loss: {train_loss}, Train Accuracy: {train_accuracy}, Validation Loss: {val_loss / len(val_loader)}, Accuracy: {val_accuracy}')

        # En iyi modeli kaydetme
        if val_accuracy > best_accuracy:
            best_accuracy = val_accuracy
            torch.save(model.state_dict(), model_path)
            patience = 5
        else:
            patience -= 1
            if patience == 0:
                print(f'Early stopping at epoch {epoch + 1}')
                break

    print(f'Model training complete and saved as {model_path}')


if __name__ == '__main__':
    data_dir = 'C:\\Users\\sevde\\PycharmProjects\\YogaPoseClassify\\userDatabase'
    model_path = 'C:\\Users\\sevde\\PycharmProjects\\YogaPoseClassify\\userDatabase\\yoga_pose_model.pth'
    train_model(data_dir, model_path)

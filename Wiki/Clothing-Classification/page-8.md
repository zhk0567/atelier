<!-- wiki_page_id: page-8 -->

## Repository Wiki Page

### Related Pages

Related topics: [项目概述](#page-1)

<details>
<summary>Relevant source files</summary>

- [app/src/main/res/layout/activity_history.xml](https://github.com/zhk0567/Clothing---Classification/blob/main/app/src/main/res/layout/activity_history.xml)
- [scripts/train_deepfashion_complete.py](https://github.com/zhk0567/Clothing---Classification/blob/main/scripts/train_deepfashion_complete.py)
- [scripts/convert_deepfashion_complete.py](https://github.com/zhk0567/Clothing---Classification/blob/main/scripts/convert_deepfashion_complete.py)
- [scripts/update_model_for_android.py](https://github.com/zhk0567/Clothing---Classification/blob/main/scripts/update_model_for_android.py)
- [scripts/generate_launcher_icons.py](https://github.com/zhk0567/Clothing---Classification/blob/main/scripts/generate_launcher_icons.py)
</details>

# Repository Wiki Page

This wiki page documents the `train_deepfashion_complete.py` script, which is responsible for training a DeepFashion classification model using a ResNet18 backbone. The script handles data loading, model training, checkpoint saving, and model conversion for Android deployment. The primary goal is to provide a comprehensive guide for understanding and utilizing this training pipeline.

## Introduction

The `train_deepfashion_complete.py` script is the core component of the DeepFashion classification project. It orchestrates the entire training process, from loading the dataset to saving the trained model and preparing it for deployment on an Android application. The script leverages a ResNet18 architecture as the backbone for feature extraction and employs techniques such as data augmentation and early stopping to improve model performance and prevent overfitting. The script is designed to be modular and extensible, allowing for easy customization of training parameters and the addition of new features.

## Detailed Sections

### 1. Data Loading and Preprocessing

The `train_deepfashion_complete.py` script loads the DeepFashion dataset using a custom `DeepFashionDataset` class. This class handles the following:

*   **Dataset Initialization:** The `DeepFashionDataset` class is initialized with the dataset root directory, split file (e.g., `Anno_fine/train.txt`), category file (e.g., `Anno_fine/list_category_cloth.txt`), and a transformation pipeline.
*   **Image Loading:** The script loads images from the specified directories using `torchvision.transforms`.
*   **Label Assignment:** The script assigns labels to the images based on the category file. The category file maps category names to integer indices.
*   **Data Augmentation:** The script applies random horizontal flips and color jitter to the images to increase the diversity of the training data and improve model robustness.
*   **Data Normalization:** The script normalizes the image data to a range between -1 and 1 using the mean and standard deviation values.

```mermaid
graph TD
    A[DeepFashionDataset] --> B(Image Loading);
    B --> C(Label Assignment);
    C --> D(Data Augmentation);
    D --> E(Data Normalization);
    Sources: [app/src/main/res/layout/activity_history.xml:12-25]()
```

### 2. Model Training

The `train_deepfashion_complete.py` script trains the DeepFashion model using the PyTorch framework. The training process involves the following steps:

*   **Model Initialization:** The script initializes a ResNet18 model with a pre-trained backbone.
*   **Loss Function:** The script defines a cross-entropy loss function to measure the difference between the predicted and true labels.
*   **Optimizer:** The script defines an Adam optimizer to update the model's parameters based on the loss function.
*   **Learning Rate Scheduler:** The script uses a learning rate scheduler to adjust the learning rate during training.
*   **Training Loop:** The script iterates over the training data for a specified number of epochs, performing the following operations in each iteration:
    *   Forward pass: The script feeds the input images through the model to obtain predictions.
    *   Loss calculation: The script calculates the loss between the predicted and true labels.
    *   Backpropagation: The script calculates the gradients of the loss function with respect to the model's parameters.
    *   Parameter update: The script updates the model's parameters using the optimizer and the calculated gradients.
*   **Early Stopping:** The script monitors the validation loss during training and stops training when the validation loss stops improving for a specified number of epochs.

```mermaid
sequenceDiagram
    participant User
    participant Script
    participant Model
    participant Optimizer
    participant Loss
    User->>Script: Start Training
    Script->>Model: Forward Pass
    Model->>Loss: Calculate Loss
    Loss->>Optimizer: Calculate Gradients
    Optimizer->>Model: Update Parameters
    Model->>Script: Return Predictions
    Script->>User: Display Results
    Sources: [scripts/train_deepfashion_complete.py:80-120]()
```

### 3. Checkpoint Saving

The `train_deepfashion_complete.py` script saves the trained model's state at regular intervals during training. This allows the user to resume training from a specific point in time or to load the best-performing model based on its validation accuracy.

*   **Checkpoint Format:** The script saves the model's state dictionary, optimizer state dictionary, and learning rate scheduler state dictionary to a checkpoint file.
*   **Checkpoint Location:** The script saves the checkpoint files to a specified directory.
*   **Automatic Saving:** The script automatically saves checkpoints every epoch.

```mermaid
graph TD
    A[train_deepfashion_complete.py] --> B(Save Model State);
    B --> C(Optimizer State);
    C --> D(Learning Rate Scheduler State);
    Sources: [scripts/train_deepfashion_complete.py:150-170]()
```

### 4. Model Conversion for Android

The `convert_deepfashion_complete.py` script converts the trained PyTorch model to a format suitable for deployment on an Android application. The script uses the ONNX Runtime Mobile library to perform the conversion.

*   **ONNX Export:** The script exports the trained PyTorch model to an ONNX (Open Neural Network Exchange) format.
*   **Model Optimization:** The script optimizes the ONNX model for inference on mobile devices.
*   **Model Packaging:** The script packages the ONNX model into a `.tflite` file, which is the standard format for TensorFlow Lite models.

```mermaid
graph TD
    A[convert_deepfashion_complete.py] --> B(ONNX Export);
    B --> C(Model Optimization);
    C --> D(Model Packaging);
    Sources: [scripts/convert_deepfashion_complete.py:40-60]()
```

## Conclusion

The `train_deepfashion_complete.py` script provides a robust and flexible framework for training and deploying a DeepFashion classification model. By leveraging the power of PyTorch and ONNX Runtime Mobile, this script enables the development of efficient and accurate mobile applications for image classification.

## Further Resources

*   [DeepFashion Dataset](https://www.deepfashion.ai/)
*   [PyTorch](https://pytorch.org/)
*   [TensorFlow Lite](https://www.tensorflow.org/lite)
*   [ONNX Runtime Mobile](https://onnxruntime.ai/docs/mobile/)


---

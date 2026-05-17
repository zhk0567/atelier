<!-- wiki_page_id: page-9 -->

## 后端系统

### Related Pages

Related topics: [系统架构](#page-2)

<details>
<summary>Relevant source files</summary>
- [DeepFashionClassifier/DeepFashionClassifier.kt](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/DeepFashionClassifier.kt)
- [DeepFashionClassifier/data/DeepFashionDataset.java](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/data/DeepFashionDataset.java)
- [DeepFashionClassifier/data/split_file.py](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/data/split_file.py)
- [DeepFashionClassifier/scripts/train_deepfashion_complete.py](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/scripts/train_deepfashion_complete.py)
- [DeepFashionClassifier/scripts/update_model_for_android.py](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/scripts/update_model_for_android.py)
</details>

# 后端系统

后端系统是DeepFashion项目中的核心组件，负责处理图像数据、模型训练和模型部署。它主要负责数据的加载、预处理、模型训练、模型评估以及模型转换和部署。 本系统依赖于深度学习模型（ResNet18）进行图像分类，并提供训练和推理接口。

## 架构概述

后端系统主要由以下几个模块组成：

*   **数据加载模块:** 负责从存储位置加载训练数据，包括图像和类别标签。
*   **模型训练模块:** 负责使用训练数据训练深度学习模型（ResNet18）。
*   **模型评估模块:** 负责使用验证数据集评估模型的性能。
*   **模型转换模块:** 负责将训练好的模型转换为适用于Android应用的目标格式（ONNX）。
*   **API接口:** 提供训练、评估和模型转换的接口。

![数据流图](https://i.imgur.com/w1uQ49M.png)
*Sources: [DeepFashionClassifier/DeepFashionDataset.java:128-138](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/data/DeepFashionDataset.java:128-138), [DeepFashionClassifier/scripts/train_deepfashion_complete.py:88-113](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/scripts/train_deepfashion_complete.py:88-113))

## 数据加载模块

数据加载模块负责从存储位置加载训练数据，包括图像和类别标签。 它实现了以下功能：

*   从标注文件（如 `Anno_fine/train.txt`）中读取图像路径和类别标签。
*   根据文件夹名称推断类别名称。
*   对图像进行预处理，例如调整大小、归一化等。
*   将预处理后的图像和类别标签存储在内存中。

![数据加载流程图](https://i.imgur.com/u6sL96j.png)
*Sources: [DeepFashionClassifier/data/DeepFashionDataset.java:145-165](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/data/DeepFashionDataset.java:145-165), [DeepFashionClassifier/scripts/train_deepfashion_complete.py:54-73](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/scripts/train_deepfashion_complete.py:54-73))

## 模型训练模块

模型训练模块负责使用训练数据训练深度学习模型（ResNet18）。 它实现了以下功能：

*   加载预训练的ResNet18模型。
*   使用训练数据对模型进行微调。
*   使用优化器（如Adam）更新模型参数。
*   监控训练过程中的损失和准确率。
*   保存训练好的模型。

![模型训练流程图](https://i.imgur.com/10s9f3z.png)
*Sources: [DeepFashionClassifier/scripts/train_deepfashion_complete.py:74-93](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/scripts/train_deepfashion_complete.py:74-93))

## 模型评估模块

模型评估模块负责使用验证数据集评估模型的性能。 它实现了以下功能：

*   加载验证数据集。
*   使用模型对验证数据集进行预测。
*   计算预测结果的准确率、精确率、召回率等指标。
*   将评估结果保存到文件中。

![模型评估流程图](https://i.imgur.com/9zW4Xo6.png)
*Sources: [DeepFashionClassifier/scripts/train_deepfashion_complete.py:94-113](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/scripts/train_deepfashion_complete.py:94-113))

## 模型转换模块

模型转换模块负责将训练好的模型转换为适用于Android应用的目标格式（ONNX）。 它实现了以下功能：

*   将训练好的模型保存为ONNX格式。
*   将ONNX模型转换为TFLite格式。
*   将TFLite模型打包到Android应用中。

![模型转换流程图](https://i.imgur.com/oQ5J8jN.png)
*Sources: [DeepFashionClassifier/scripts/update_model_for_android.py:33-50](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/scripts/update_model_for_android.py:33-50))

## API接口

后端系统提供以下API接口：

*   `train()`:  训练模型。
*   `evaluate()`: 评估模型。
*   `convert()`: 转换模型。

这些接口允许其他模块访问和使用后端系统的功能。

## 总结

后端系统是DeepFashion项目中的核心组件，负责处理图像数据、模型训练和模型部署。 它通过模块化的设计，实现了数据的加载、模型训练、模型评估和模型转换等关键功能。

<details>
<summary>Relevant source files</summary>
- [DeepFashionClassifier/DeepFashionClassifier.kt](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/DeepFashionClassifier.kt)
- [DeepFashionClassifier/data/DeepFashionDataset.java](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/data/DeepFashionDataset.java)
- [DeepFashionClassifier/data/split_file.py](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/data/split_file.py)
- [DeepFashionClassifier/scripts/train_deepfashion_complete.py](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/scripts/train_deepfashion_complete.py)
- [DeepFashionClassifier/scripts/update_model_for_android.py](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/scripts/update_model_for_android.py)
</details>


---

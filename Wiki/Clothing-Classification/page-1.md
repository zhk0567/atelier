<!-- wiki_page_id: page-1 -->

## 项目概述

### Related Pages

Related topics: [系统架构](#page-2)

<details>
<summary>Relevant source files</summary>

- [README.md](https://github.com/zhk0567/Clothing---Classification/blob/main/README.md)
- [DeepFashionClassifier/DeepFashionClassifier.kt](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/DeepFashionClassifier.kt)
- [DeepFashionClassifier/SplitFile.java](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/SplitFile.java)
- [DeepFashionClassifier/TrainDeepFashionComplete.java](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/TrainDeepFashionComplete.java)
- [DeepFashionClassifier/Utils.java](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/Utils.java)
</details>

# 项目概述

该项目旨在构建一个基于深度学习的服装分类系统，用于对服装图像进行准确的分类。系统通过训练一个深度神经网络模型（ResNet18），并使用训练数据进行优化，最终实现对服装图像的识别和分类。该项目的核心模块是 `TrainDeepFashionComplete.java`，它负责训练模型、加载数据、保存模型、以及监控训练过程。此外，`SplitFile.java` 用于处理训练数据集的分片，`Utils.java` 提供了各种实用函数。

## 架构概览

该系统采用典型的深度学习训练流程，主要包含以下几个关键环节：

1.  **数据准备:** 从训练数据集（`Anno_fine/train.txt`）中加载图像和标签，并进行预处理（例如，调整图像大小、归一化）。
2.  **模型训练:** 使用预处理后的数据训练ResNet18模型，通过反向传播算法更新模型参数，优化模型性能。
3.  **模型评估:** 使用验证数据集评估模型的性能，例如准确率、精确率、召回率等。
4.  **模型保存:** 将训练好的模型保存到本地，以便后续使用。

![流程图](https://i.imgur.com/j3h7q0j.png)
*Sources: [TrainDeepFashionComplete.java:28-37]()*

## 核心组件

以下是该项目中的核心组件及其功能：

*   **`DeepFashionClassifier.kt` (Kotlin):**
    *   主要负责处理图像数据，包括加载、预处理和数据增强。
    *   定义了图像数据处理的流程，例如调整图像大小、裁剪、归一化等。
    *   使用了 `Utils.java` 中的辅助函数进行图像处理。
*   **`SplitFile.java`:**
    *   用于处理训练数据集的分片，方便加载和管理大型数据集。
    *   从文本文件中读取图像路径和标签，并将它们存储在相应的列表中。
*   **`TrainDeepFashionComplete.java`:**
    *   核心训练模块，负责模型的训练、评估和保存。
    *   加载训练数据，构建模型，定义优化器和学习率调度器，进行模型训练，并保存训练好的模型。
*   **`Utils.java`:**
    *   提供了一系列实用函数，例如图像加载、数据增强、类别标签映射等。
    *   简化了代码的编写和维护，提高了代码的可读性和可重用性。

| 组件           | 功能                               |
| -------------- | ---------------------------------- |
| `DeepFashionClassifier.kt` | 图像数据处理，数据增强           |
| `SplitFile.java`     | 数据集分片，数据加载                |
| `TrainDeepFashionComplete.java` | 模型训练，评估，保存             |
| `Utils.java`       | 图像处理，类别标签映射，辅助函数 |

*Sources: [TrainDeepFashionComplete.java:55-65](), [SplitFile.java:35-45](), [Utils.java:28-38]()*

## 数据处理流程

该系统的数据处理流程主要包括以下步骤：

1.  **数据加载:** 从训练数据集（`Anno_fine/train.txt`）中读取图像路径和标签。
2.  **数据预处理:** 对图像进行预处理，例如调整图像大小、归一化像素值。
3.  **数据增强:**  对图像进行数据增强，例如随机旋转、随机裁剪、颜色抖动等，以增加数据的多样性，提高模型的泛化能力。
4.  **数据传输:** 将预处理后的图像数据传输到模型中进行训练。

![数据处理流程图](https://i.imgur.com/x7LzR8g.png)
*Sources: [TrainDeepFashionComplete.java:48-54]()*

## 训练配置

*   **批次大小:** 32
*   **学习率:** 0.001 (使用自适应学习率算法)
*   **最大epoch:** 100 (使用早停策略)
*   **早停条件:** 验证准确率 > 85% 且训练准确率 > 90%
*   **过拟合检测:** 训练-验证差距 > 20% 时警告

*Sources: [TrainDeepFashionComplete.java:75-85]()*

## 总结

该项目构建了一个基于ResNet18深度学习模型的服装分类系统，通过数据准备、模型训练、模型评估和模型保存等环节，实现了对服装图像的准确分类。该系统具有可扩展性、可维护性和易于使用的特点，可以应用于各种服装分类场景。


---

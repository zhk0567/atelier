<!-- wiki_page_id: page-5 -->

## 上传图片分类

### Related Pages

Related topics: [项目概述](#page-1)

<details>
<summary>Relevant source files</summary>

- [app/src/main/java/com/deepfashion/classifier/FullImageActivity.kt](https://github.com/zhk0567/Clothing---Classification/blob/main/app/src/main/java/com/deepfashion/classifier/FullImageActivity.kt)
- [scripts/train_deepfashion_complete.py](https://github.com/zhk0567/Clothing---Classification/blob/main/scripts/train_deepfashion_complete.py)
- [scripts/convert_deepfashion_complete.py](https://github.com/zhk0567/Clothing---Classification/blob/main/scripts/convert_deepfashion_complete.py)
- [Category and Attribute Prediction Benchmark/Anno_fine/train.txt](https://github.com/zhk0567/Clothing---Classification/blob/main/Category%20and%20Attribute%20Prediction%20Benchmark/Anno_fine/train.txt)
- [Category and Attribute Prediction Benchmark/Anno_fine/train_cate.txt](https://github.com/zhk0567/Clothing---Classification/blob/main/Category%20and%20Attribute%20Prediction%20Benchmark/Anno_fine/train_cate.txt)
</details>

# 上传图片分类

## 简介

“上传图片分类”模块负责接收用户上传的服装图片，并利用训练好的DeepFashion模型进行分类识别。该模块的核心功能包括图片预处理、模型推理、结果展示和分类结果保存。它与训练脚本 `scripts/train_deepfashion_complete.py` 紧密协作，用于完成图像分类任务。该模块依赖于 `FullImageActivity.kt` 负责UI交互和结果展示，并与模型进行通信。

## 架构与组件

“上传图片分类”模块的架构主要由以下几个组件构成：

1.  **UI 组件 (FullImageActivity.kt):** 负责用户交互，接收用户上传的图片，显示分类结果，并提供相应的操作界面。
2.  **模型加载器:**  负责加载训练好的DeepFashion模型，并进行模型推理。
3.  **数据预处理模块:**  对上传的图片进行预处理，例如调整大小、归一化等，以满足模型输入的要求。
4.  **结果展示模块:**  将模型推理的结果展示给用户，并提供相应的反馈机制。
5.  **模型保存模块:**  将分类结果保存到本地或服务器，以便后续使用。

![上传图片分类架构图](https://i.imgur.com/your_diagram_url_here.png)
(Note: Replace `https://i.imgur.com/your_diagram_url_here.png` with the actual URL of a Mermaid diagram representing the architecture.)

## 详细步骤

### 1. 图片上传与预处理

用户通过 `FullImageActivity.kt`  界面上传服装图片。该活动首先对图片进行预处理，包括调整大小、归一化等操作，以适应模型的要求。预处理的具体步骤可以参考 `scripts/train_deepfashion_complete.py` 中对数据预处理的实现。

### 2. 模型推理

预处理后的图片数据被传递给模型加载器，模型加载器负责加载训练好的DeepFashion模型，并对图片进行分类推理。模型推理的具体实现可以在 `scripts/convert_deepfashion_complete.py` 中找到。

### 3. 结果展示

模型推理的结果被传递给结果展示模块，该模块将分类结果展示给用户。 `FullImageActivity.kt`  负责将模型输出的类别标签显示在界面上。

### 4. 结果保存

分类结果可以被保存到本地或服务器，以便后续使用。 具体实现可以参考 `scripts/train_deepfashion_complete.py` 中保存模型的代码。

## 数据流

![图片上传分类数据流图](https://i.imgur.com/your_data_flow_diagram_url_here.png)
(Note: Replace `https://i.imgur.com/your_data_flow_diagram_url_here.png` with the actual URL of a Mermaid diagram representing the data flow.)

## API 接口

| 接口名称          | 方法   | 参数                               | 返回值          | 描述                               |
| ----------------- | ------ | ---------------------------------- | ---------------- | ---------------------------------- |
| `classifyImage`   | POST  | `imagePath` (图片路径), `model` (模型对象) | `category_idx` | 对图片进行分类识别，返回类别索引 |

## 配置文件

训练脚本 `scripts/train_deepfashion_complete.py` 包含以下配置参数：

| 参数名称        | 类型   | 默认值 | 描述                               |
| --------------- | ------ | ------ | ---------------------------------- |
| `batch_size`    | int    | 32     | 批次大小                           |
| `learning_rate` | float  | 0.001  | 学习率                             |
| `max_epochs`    | int    | 100    | 最大训练轮数                        |

## 总结

“上传图片分类”模块是DeepFashion项目中的一个重要组成部分，它实现了服装图片的自动分类识别功能。通过结合训练好的DeepFashion模型和用户友好的UI界面，该模块为用户提供了便捷的服装分类服务。


---

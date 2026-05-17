<!-- wiki_page_id: page-6 -->

## 数据流

### Related Pages

Related topics: [系统架构](#page-2)

<details>
<summary>Relevant source files</summary>

- [DeepFashionClassifier/DeepFashionClassifier.kt](https://github.com/zhk0567/Clothing---Classification/blob/main/DeepFashionClassifier/DeepFashionClassifier.kt)
- [scripts/train_deepfashion_complete.py](https://github.com/zhk0567/Clothing---Classification/blob/main/scripts/train_deepfashion_complete.py)
- [scripts/convert_deepfashion_complete.py](https://github.com/zhk0567/Clothing---Classification/blob/main/scripts/convert_deepfashion_complete.py)
- [scripts/update_model_for_android.py](https://github.com/zhk0567/Clothing---Classification/blob/main/scripts/update_model_for_android.py)
- [scripts/generate_launcher_icons.py](https://github.com/zhk0567/Clothing---Classification/blob/main/scripts/generate_launcher_icons.py)
</details>

# 数据流

## 简介

“数据流”模块负责DeepFashion分类器中的图像数据处理和模型推理流程。它接收来自数据预处理模块的图像数据，经过一系列的转换和预处理，然后将数据传递给训练好的模型进行分类，最后将分类结果返回给用户。该模块的核心目标是高效、准确地执行图像分类任务，并提供必要的接口供其他模块调用。

## 详细结构

### 1. 数据流架构

数据流主要由以下几个部分组成：

*   **图像输入**: 接收来自数据预处理模块的图像数据。
*   **数据预处理**: 对图像数据进行必要的预处理，例如调整大小、归一化等。
*   **模型推理**: 使用训练好的模型对预处理后的图像数据进行分类。
*   **结果输出**: 将分类结果返回给用户。

![数据流架构图](https://i.imgur.com/yq9s39G.png)

*Sources: [scripts/train_deepfashion_complete.py:10-13]()*

### 2. 主要组件

*   **DeepFashionClassifier 类 (DeepFashionClassifier.kt)**：
    *   负责加载模型权重、构建模型结构、执行模型推理。
    *   `forward()` 方法：接收图像数据，通过模型进行分类，返回分类结果。
    *   `__init__()` 方法：初始化模型，加载模型权重，设置分类类别数量。
    *   `_infer_category()` 方法：根据文件夹名称推断类别名。
*   **数据预处理模块 (未提供具体文件)**：
    *   负责对图像数据进行预处理，例如调整大小、归一化等。
*   **模型推理模块 (未提供具体文件)**：
    *   负责使用训练好的模型对预处理后的图像数据进行分类。
*   **结果输出模块 (未提供具体文件)**：
    *   负责将分类结果返回给用户。

![DeepFashionClassifier 类图](https://i.imgur.com/yq9s39G.png)

*Sources: [DeepFashionClassifier/DeepFashionClassifier.kt:22-35]()*

### 3. 数据流流程

1.  数据预处理模块接收原始图像数据，并进行预处理。
2.  预处理后的图像数据传递给 DeepFashionClassifier 类。
3.  DeepFashionClassifier 类加载模型权重，构建模型结构，执行模型推理。
4.  模型推理的结果（分类结果）传递给结果输出模块。
5.  结果输出模块将分类结果返回给用户。

![数据流流程图](https://i.imgur.com/zQ5wY4G.png)

*Sources: [scripts/train_deepfashion_complete.py:20-25]()*

### 4. 关键函数和类

| 组件            | 函数/类              | 功能                               |
| --------------- | --------------------- | ---------------------------------- |
| DeepFashionClassifier | `forward()`          | 执行模型推理，返回分类结果            |
| DeepFashionClassifier | `_infer_category()`   | 根据文件夹名称推断类别名            |
| 数据预处理模块    | (未定义)             | 图像数据预处理 (调整大小，归一化等) |
| 模型推理模块    | (未定义)             | 使用模型进行分类                  |

![关键函数和类图](https://i.imgur.com/yq9s39G.png)

*Sources: [DeepFashionClassifier/DeepFashionClassifier.kt:22-35]()*

### 5. 转换模型到TFLite

数据流的另一个关键部分是模型转换到TFLite格式，以便在Android应用中部署。
1.  使用 `convert_deepfashion_complete.py` 脚本将训练好的PyTorch模型转换为ONNX格式。
2.  使用 `update_model_for_android.py` 脚本将ONNX模型转换为TFLite格式。
3.  将生成的TFLite模型复制到DeepFashionClassifier Android应用的 assets 目录中。

![模型转换流程图](https://i.imgur.com/zQ5wY4G.png)

*Sources: [scripts/convert_deepfashion_complete.py:15-25]()*

## 总结

“数据流”模块是DeepFashion分类器中的核心组成部分，它负责高效地处理图像数据，执行模型推理，并将结果返回给用户。通过对数据流的理解和优化，可以提高DeepFashion分类器的性能和效率。


---

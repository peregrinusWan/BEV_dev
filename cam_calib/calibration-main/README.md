# 相机标定工具

这是一个多功能相机标定工具，支持单目、双目和鱼眼相机的标定。它使用OpenCV和棋盘格图案进行标定，并将结果保存为YAML文件。同时，它还可以选择性地对原始图像进行校正并保存。

## 功能

- **单目标定**: 计算单个相机的内参矩阵和畸变系数。
- **双目标定**: 计算左右两个相机的内参、畸变系数，以及它们之间的旋转和平移关系。
- **鱼眼相机标定**: 专为鱼眼镜头设计，计算其内参和畸变模型。
- **图像校正**: 使用计算出的参数来校正（去畸变）原始图像。
- **参数保存**: 将所有标定参数保存到易于阅读和解析的 `.yaml` 文件中。
- **模块化设计**: 代码结构清晰，易于理解和扩展。

## 安装依赖

首先，请确保你已经安装了Python 3。然后通过`pip`安装所需的库：

```bash
pip install -r requirements.txt
```

## 文件结构准备

请按照以下结构组织你的标定图片：

```
camera_calibration_project/
│
└── images/
    ├── mono/       # <-- 用于单目标定的图片
    │   ├── 1.jpg
    │   └── ...
    ├── stereo/     # <-- 用于双目标定的图片
    │   ├── left/
    │   │   ├── 1.jpg
    │   │   └── ...
    │   └── right/
    │       ├── 1.jpg
    │       └── ...
    └── fisheye/    # <-- 用于鱼眼标定的图片
        ├── 1.jpg
        └── ...
```

## 如何运行

所有操作都通过 `main.py` 脚本和命令行参数完成。

### 示例命令

#### 1. 单目标定

- **只进行标定，不校正图像**

```bash
python main.py --type mono --input_dir images/mono/ --pattern_size 9x6 --square_size 25
```

- **标定并保存校正后的图像**

```bash
python main.py --type mono --input_dir images/mono/ --pattern_size 9x6 --square_size 25 --undistort
```

#### 2. 双目标定

- **只进行标定**

```bash
python main.py --type stereo --input_dir images/stereo/ --pattern_size 9x6 --square_size 25
```

- **标定并保存立体校正后的图像**

```bash
python main.py --type stereo --input_dir images/stereo/ --pattern_size 9x6 --square_size 25 --undistort
```

#### 3. 鱼眼相机标定

- **标定并保存校正后的图像**

```bash
python main.py --type fisheye --input_dir images/fisheye/ --pattern_size 9x6 --square_size 25 --undistort
```

### 参数说明

- `--type`: **[必需]** 标定类型。可选值: `mono`, `stereo`, `fisheye`。
- `--input_dir`: **[必需]** 包含标定图片的文件夹路径。
- `--pattern_size`: **[必需]** 棋盘格内部角点的数量，格式为 `宽度x高度` (例如 `9x6`)。
- `--square_size`: **[必需]** 棋盘格中每个方块的实际边长（单位自定，但要统一，如毫米 `mm`）。
- `--output_dir`: [可选] 输出文件夹的路径。默认为 `./output/`。
- `--undistort`: [可选] 一个开关参数。如果提供此参数，程序将保存校正后的图像。

## 输出结果

程序运行后，将在指定的 `--output_dir` (默认为 `output`) 文件夹下生成以下内容：

- `output/params/`: 存放标定参数的 `.yaml` 文件。
  - `mono_calib.yaml`
  - `stereo_calib.yaml`
  - `fisheye_calib.yaml`
- `output/*_undistorted/`: 如果使用了 `--undistort` 参数，这里会存放校正后的图像。
  - `mono_undistorted/`
  - `stereo_undistorted/left/` 和 `stereo_undistorted/right/`
  - `fisheye_undistorted/`
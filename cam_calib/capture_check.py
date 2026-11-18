import cv2
import numpy as np
import glob
import os

img_dir = r"D:\.research_project\Bev_dev\BEV_dev\calib_imgs\*.png"
images = sorted(glob.glob(img_dir))

print(f"当前工作目录: {os.getcwd()}")
print(f"搜索路径: {img_dir}")
print(f"找到 {len(images)} 张图\n")

if len(images) == 0:
    print("没有找到图片！尝试其他后缀...")
    images = sorted(glob.glob(r"D:\.research_project\Bev_dev\BEV_dev\calib_imgs\*"))
    print(f"文件夹里所有文件: {images}")
    exit()

for i, fname in enumerate(images):
    img = cv2.imread(fname)
    if img is None:
        print(f"图{i:03d}: ✗ 无法读取文件")
        continue

    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 棋盘格尺寸改成你自己的！现在是 (6,9) 内角点
    ret, corners = cv2.findChessboardCorners(
        gray, (7, 5),
        cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
    )
    
    if ret:
        x = corners[:, 0, 0]
        y = corners[:, 0, 1]
        x_min, x_max = x.min(), x.max()
        y_min, y_max = y.min(), y.max()

        cover_x = (x_max - x_min) / w * 100
        cover_y = (y_max - y_min) / h * 100
        center_x = (x_min + x_max) / 2 / w * 100
        center_y = (y_min + y_max) / 2 / h * 100

        # 判断是否靠近边缘
        near_edge = (center_x < 25 or center_x > 75 or center_y < 25 or center_y > 75)
        edge_mark = " ⚠边缘" if near_edge else ""

        print(f"图{i:03d}: ✓ 覆盖 {cover_x:3.0f}%x{cover_y:3.0f}% 位置({center_x:3.0f}%,{center_y:3.0f}) 分辨率{w}x{h}{edge_mark}")
    else:
        print(f"图{i:03d}: ✗ 未检测到角点  分辨率{w}x{h}")
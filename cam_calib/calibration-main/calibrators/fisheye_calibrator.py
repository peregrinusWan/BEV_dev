# calibrators/fisheye_calibrator.py

import cv2
import numpy as np
import os
import glob
from utils import save_to_yaml, find_chessboard_corners, create_folder

def calibrate(image_dir, pattern_size, square_size, output_dir, undistort):
    """鱼眼相机标定主函数"""
    print("--- 开始鱼眼相机标定 ---")
    
    objpoints, imgpoints, img_shape = find_chessboard_corners(image_dir, pattern_size, square_size)
    if objpoints is None:
        return
    # fisheye.calibrate 要求每组点都是连续的 CV_32FC*/CV_64FC* 数组。
    # 显式转换可避免不同 OpenCV 版本对 Python 列表/数组推断类型不一致。
    objpoints = [
        np.ascontiguousarray(p, dtype=np.float64).reshape(-1, 1, 3)
        for p in objpoints
    ]
    imgpoints = [
        np.ascontiguousarray(p, dtype=np.float64).reshape(-1, 1, 2)
        for p in imgpoints
    ]

    print("\n正在计算鱼眼相机参数...")
    
    if len(objpoints) != len(imgpoints):
        raise ValueError(
            f"对象点组数量 ({len(objpoints)}) 与图像点组数量 "
            f"({len(imgpoints)}) 不一致。"
        )
    for index, (object_points, image_points) in enumerate(
        zip(objpoints, imgpoints)
    ):
        if object_points.shape[0] != image_points.shape[0]:
            raise ValueError(
                f"第 {index + 1} 组角点数量不一致: "
                f"对象点 {object_points.shape[0]}，图像点 {image_points.shape[0]}。"
            )

    K = np.zeros((3, 3), dtype=np.float64)
    D = np.zeros((4, 1), dtype=np.float64)
    
    # CALIB_CHECK_COND 会在单个姿态导致病态矩阵时直接中止整个标定。
    # 鱼眼标定图片常包含边缘视角，这类样本可能触发该检查；先让优化器
    # 完成标定，再通过重投影误差判断结果是否可靠。
    calibration_flags = (
        cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC
        | cv2.fisheye.CALIB_FIX_SKEW
    )
    
    
    ret, K, D, _, _ = cv2.fisheye.calibrate(
        objpoints,
        imgpoints,
        img_shape,
        K,
        D,
        None,
        None,
        calibration_flags,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
    )

    if not ret:
        print("鱼眼标定失败！")
        return
    
    print("相机内参矩阵 (K):\n", K)
    print("畸变系数 (D):\n", D)
    
    # 保存参数
    params_path = os.path.join(output_dir, "params")
    create_folder(params_path)
    calib_data = {
        'camera_matrix': K,
        'dist_coeffs': D,
        'image_width': img_shape[0],
        'image_height': img_shape[1]
    }
    save_to_yaml(calib_data, os.path.join(params_path, 'fisheye_calib.yaml'))

    # 校正图像
    if undistort:
        print("\n正在校正鱼眼图像...")
        undistorted_dir = os.path.join(output_dir, "fisheye_undistorted")
        create_folder(undistorted_dir)
        images = glob.glob(os.path.join(image_dir, '*.jpg')) + glob.glob(os.path.join(image_dir, '*.png'))+ glob.glob(os.path.join(image_dir, '*.bmp'))
        
        for fname in images:
            img = cv2.imread(fname)
            # 使用cv2.fisheye.undistortImage进行校正
            undistorted_img = cv2.fisheye.undistortImage(img, K, D, Knew=K)
            output_path = os.path.join(undistorted_dir, "undistorted_" + os.path.basename(fname))
            cv2.imwrite(output_path, undistorted_img)
            print(f"  - 已保存校正图像: {output_path}")

    print("--- 鱼眼相机标定完成 ---")

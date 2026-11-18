import os
from utils import create_folder

def get_config():
    """返回标定配置。运行前直接修改这里的参数即可。"""
    return {
        # 可选值: 'mono'、'stereo'、'fisheye'
        'calibration_type': 'mono',
        # 双目标定时，该目录下必须包含 left 和 right 子文件夹
        'input_dir': 'D:\\.research_project\\Bev_dev\\BEV_dev\\calib_imgs',
        'output_dir': 'output',
        # 棋盘格内部角点数：(列数, 行数)
        'pattern_size': (7, 5),
        # 棋盘格方块边长，单位自定，但需要保持一致
        'square_size': 25.0,
        # 是否保存校正后的图像
        'undistort': True,
    }


def main():
    config = get_config()
    calibration_type = config['calibration_type']
    if calibration_type not in ('mono', 'stereo', 'fisheye'):
        print("错误: calibration_type 必须是 'mono'、'stereo' 或 'fisheye'。")
        return

    pattern_size = config['pattern_size']
    if (not isinstance(pattern_size, tuple) or len(pattern_size) != 2
            or not all(isinstance(value, int) and value > 0 for value in pattern_size)):
        print("错误: pattern_size 必须是类似 (9, 6) 的正整数元组。")
        return

    if not isinstance(config['square_size'], (int, float)) or config['square_size'] <= 0:
        print("错误: square_size 必须是大于 0 的数字。")
        return

    try:
        create_folder(config['output_dir'])
    except OSError as error:
        print(f"错误: 无法创建输出文件夹: {error}")
        return

    # 根据类型调用相应的标定器
    if calibration_type == 'mono':
        from calibrators import mono_calibrator
        mono_calibrator.calibrate(
            image_dir=config['input_dir'],
            pattern_size=pattern_size,
            square_size=config['square_size'],
            output_dir=config['output_dir'],
            undistort=config['undistort']
        )
    elif calibration_type == 'fisheye':
        from calibrators import fisheye_calibrator
        fisheye_calibrator.calibrate(
            image_dir=config['input_dir'],
            pattern_size=pattern_size,
            square_size=config['square_size'],
            output_dir=config['output_dir'],
            undistort=config['undistort']
        )
    elif calibration_type == 'stereo':
        from calibrators import stereo_calibrator
        left_dir = os.path.join(config['input_dir'], 'left')
        right_dir = os.path.join(config['input_dir'], 'right')
        if not os.path.isdir(left_dir) or not os.path.isdir(right_dir):
            print(f"错误: 双目标定需要 '{config['input_dir']}' 文件夹下包含 'left' 和 'right' 子文件夹。")
            return
        stereo_calibrator.calibrate(
            left_dir=left_dir,
            right_dir=right_dir,
            pattern_size=pattern_size,
            square_size=config['square_size'],
            output_dir=config['output_dir'],
            undistort=config['undistort']
        )

if __name__ == '__main__':
    main()
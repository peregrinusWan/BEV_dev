import cv2
import numpy as np

def evaluate_straightness_simple(image_path, output_path=None):
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图像: {image_path}")
        return None
    
    h, w = img.shape[:2]
    print(f"图像尺寸: {w}x{h}")
    
    # 动态缩放：限制最大显示宽度 1400，保证窗口不超屏
    max_display_w = 1400
    scale = min(1.0, max_display_w / w)
    display_w = int(w * scale)
    display_h = int(h * scale)
    
    # 缩放后的显示图（仅用于展示和点击）
    display = cv2.resize(img, (display_w, display_h))
    
    print("请在图像上沿着一条直线边缘点击至少5个点")
    print("点击完成后，按 ESC 键退出")
    points = []  # 存原图坐标
    
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # 显示坐标 -> 原图坐标
            ox, oy = x / scale, y / scale
            points.append([float(ox), float(oy)])
            print(f"  已选点 {len(points)}: 显示({x},{y}) -> 原图({ox:.1f},{oy:.1f})")
            
            # 画圈在显示图上（用小半径）
            cv2.circle(display, (x, y), 3, (0, 0, 255), -1)
            cv2.imshow("Select points on straight line", display)
    
    cv2.imshow("Select points on straight line", display)
    cv2.setMouseCallback("Select points on straight line", click_event)
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
    cv2.destroyAllWindows()
    
    if len(points) < 3:
        print("至少需要3个点")
        return None
    
    pts = np.array(points, dtype=np.float32)
    
    # 拟合直线（基于原图坐标，精度不损失）
    vx, vy, x0, y0 = cv2.fitLine(pts, cv2.DIST_L2, 0, 0.01, 0.01)
    vx, vy = float(vx[0]), float(vy[0])
    x0, y0 = float(x0[0]), float(y0[0])
    
    # 计算点到直线距离
    distances = []
    for pt in pts:
        d = abs(vy * (float(pt[0]) - x0) - vx * (float(pt[1]) - y0))
        distances.append(d)
    
    mean_error = float(np.mean(distances))
    max_error = float(np.max(distances))
    
    print(f"\n=== 直线度评估 ===")
    print(f"采样点数: {len(points)}")
    print(f"平均偏差: {mean_error:.3f} 像素 (原图尺度)")
    print(f"最大偏差: {max_error:.3f} 像素")
    
    if mean_error < 0.5:
        print("评级: ★★★★★ 优秀")
    elif mean_error < 1.0:
        print("评级: ★★★★☆ 良好")
    elif mean_error < 2.0:
        print("评级: ★★★☆☆ 合格")
    else:
        print("评级: ★☆☆☆☆ 不合格")
    
    # 绘制结果（在原图上画，保存高清）
    result = img.copy()
    for pt, d in zip(points, distances):
        pt_x, pt_y = int(pt[0]), int(pt[1])
        color = (0, 255, 0) if d < 1 else (0, 165, 255) if d < 2 else (0, 0, 255)
        cv2.circle(result, (pt_x, pt_y), 8, color, -1)
        cv2.putText(result, f"{d:.1f}px", (pt_x+10, pt_y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
    
    # 画拟合直线（贯穿原图）
    length = max(w, h) * 2
    x1 = int(x0 - vx * length)
    y1 = int(y0 - vy * length)
    x2 = int(x0 + vx * length)
    y2 = int(y0 + vy * length)
    cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 3)
    
    if output_path:
        cv2.imwrite(output_path, result)
        print(f"结果已保存(原图): {output_path}")
    
    # 结果图也缩放显示，避免巨大
    result_display = cv2.resize(result, (display_w, display_h))
    cv2.imshow("Straightness Evaluation (缩放显示)", result_display)
    print("查看结果后，按任意键关闭窗口")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return {
        'mean_error': mean_error,
        'max_error': max_error,
        'points': points
    }

if __name__ == "__main__":
    image_path = "D:\\.research_project\\Bev_dev\\BEV_dev\\calib_imgs\\DSC_9210.JPG"
    result = evaluate_straightness_simple(image_path, "straightness_result.jpg")
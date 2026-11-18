import cv2
import numpy as np

# 4个相机的索引
camera_indices = [0, 2, 3, 4]  # 根据你的实际情况修改

caps = []
for idx in camera_indices:
    cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    caps.append(cap)

# 创建可缩放的窗口
window_name = "4 Fisheye Cameras"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 1000, 750)

print("按 q 退出")

while True:
    frames = []
    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        if ret:
            # 添加相机ID标签
            cv2.putText(frame, f"Camera {camera_indices[i]}", (20, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            frames.append(frame)
        else:
            frames.append(np.zeros((960, 1280, 3), dtype=np.uint8))
    
    # 2x2网格拼接
    top = cv2.hconcat([frames[0], frames[1]])
    bottom = cv2.hconcat([frames[2], frames[3]])
    grid = cv2.vconcat([top, bottom])
    
    cv2.imshow(window_name, grid)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

for cap in caps:
    cap.release()
cv2.destroyAllWindows()
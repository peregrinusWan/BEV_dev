import cv2
import os



save_dir = "calib_imgs"
os.makedirs(save_dir, exist_ok=True)

cap = cv2.VideoCapture(0)  # 0是默认相机，多相机试1/2
# 固定分辨率（按你镜头实际支持的最大来，例如1920x1080）
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cnt = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("读不到帧")
        break

    cv2.imshow("preview", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):  # 按 s 存一张
        name = os.path.join(save_dir, f"calib02_{cnt:03d}.png")
        cv2.imwrite(name, frame)  # PNG 无压缩，别用.jpg
        print("saved", name)
        cnt += 1
    elif key == ord('q'):  # 按 q 退出
        break

cap.release()
cv2.destroyAllWindows()
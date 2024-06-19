import cv2
import numpy as np

# 加载视频
video_path = "./data/4.1.avi"
cap = cv2.VideoCapture(video_path)

# Lucas-Kanade光流法的参数
lk_params = dict(winSize=(10, 10), maxLevel=3, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# 初始化帧计数
frame_count = 0
ret, old_frame = cap.read()

old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = np.array([[551, 13]], dtype=np.float32).reshape(-1, 1, 2)
tracked_points = []
tracked_points_history = []  # 存储追踪点的历史记录

# 视频输出设置
output_path = "./data/tracked_video.avi"
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

while cap.isOpened() and frame_count < 1248:
    ret, frame = cap.read()
    if not ret:
        break
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    if st[0] == 1:
        tracked_points.append(p1[0].ravel())
        tracked_points_history.append(p1[0].ravel())  # 存储当前帧的追踪点坐标
        a, b = p1[0].ravel()
        frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 0, 255), -1)
    old_gray = frame_gray.copy()
    p0 = p1.reshape(-1, 1, 2)
    frame_count += 1

    # 将带有特征点的帧写入视频
    out.write(frame)

cap.release()
out.release()

# 将追踪点坐标保存到文件
tracked_points_history = np.array(tracked_points_history)
np.savetxt('./data/tracked_points.txt', tracked_points_history, fmt='%d')

print("视频处理完成，并已保存到:", output_path)
print("追踪点坐标已保存到: ./data/tracked_points.txt")

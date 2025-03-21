import cv2
import numpy as np

# 输入视频路径
video_paths = ["video1.mp4", "video2.mp4", "video3.mp4", "video4.mp4"]

# 读取视频
caps = [cv2.VideoCapture(v) for v in video_paths]

# 获取视频参数（假设所有视频尺寸、帧率一致）
frame_width = int(caps[0].get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(caps[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(caps[0].get(cv2.CAP_PROP_FPS))
output_size = (frame_width * 2, frame_height * 2)

# 创建输出视频
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 mp4 编码
out = cv2.VideoWriter("output_2x2.mp4", fourcc, fps, output_size)

while True:
    frames = []
    ret_vals = []
    
    # 读取四个视频的帧
    for cap in caps:
        ret, frame = cap.read()
        ret_vals.append(ret)
        if ret:
            frames.append(frame)
        else:
            frames.append(np.zeros((frame_height, frame_width, 3), dtype=np.uint8))  # 如果某个视频结束，填充黑屏

    # 如果所有视频都读取完毕，结束
    if not any(ret_vals):
        break

    # 拼接 2×2 屏幕
    top_row = np.hstack((frames[0], frames[1]))  # 拼接上排
    bottom_row = np.hstack((frames[2], frames[3]))  # 拼接下排
    combined_frame = np.vstack((top_row, bottom_row))  # 合并上下排

    # 写入到输出视频
    out.write(combined_frame)

# 释放资源
for cap in caps:
    cap.release()
out.release()
cv2.destroyAllWindows()

print("拼接完成，生成 output_2x2.mp4")

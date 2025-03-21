import cv2
import numpy as np

video_paths = ["video1.mp4", "video2.mp4", "video3.mp4", "video4.mp4"]
caps = [cv2.VideoCapture(v) for v in video_paths]

frame_width = int(caps[0].get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(caps[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(caps[0].get(cv2.CAP_PROP_FPS))
output_size = (frame_width * 2, frame_height * 2)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("output_2x2_annotated.mp4", fourcc, fps, output_size)

def annotate_frame(frame, index):
    overlay_size = 40
    cv2.rectangle(frame, (0, 0), (overlay_size, overlay_size), (0, 0, 0), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    text = str(index + 1)
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_x = (overlay_size - text_size[0]) // 2
    text_y = (overlay_size + text_size[1]) // 2
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 0, 255), thickness, cv2.LINE_AA)
    return frame

while True:
    frames = []
    ret_vals = []

    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        ret_vals.append(ret)
        if ret:
            frame = annotate_frame(frame, i)
            frames.append(frame)
        else:
            blank = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
            blank = annotate_frame(blank, i)
            frames.append(blank)

    if not any(ret_vals):
        break

    top_row = np.hstack((frames[0], frames[1]))
    bottom_row = np.hstack((frames[2], frames[3]))
    combined_frame = np.vstack((top_row, bottom_row))

    out.write(combined_frame)


for cap in caps:
    cap.release()
out.release()
cv2.destroyAllWindows()

print("拼接完成并已标注编号：output_2x2_annotated.mp4")

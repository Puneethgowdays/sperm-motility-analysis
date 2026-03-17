import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
import math

# Load trained model
model = YOLO("best.pt")

# Tracking dictionary
tracks = defaultdict(list)

# Video paths
input_video = "input_video.avi"
output_video = "output_video.avi"

cap = cv2.VideoCapture(input_video)

fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

frame_id = 0

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(
        frame,
        persist=True,
        conf=0.1,
        tracker="bytetrack.yaml"
    )

    boxes = results[0].boxes

    if boxes is not None:

        for box in boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            track_id = int(box.id[0]) if box.id is not None else -1

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            tracks[track_id].append((cx, cy))

            # Draw detection
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

            cv2.putText(frame,
                        f"ID:{track_id}",
                        (x1,y1-5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0,255,0),
                        1)

    out.write(frame)

    frame_id += 1

cap.release()
out.release()

print("Processing finished")
print("Output saved as:", output_video)
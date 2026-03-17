from ultralytics import YOLO
import os

model = YOLO("runs/detect/train/weights/best.pt")

SOURCE = "test/images"

results = model.predict(source=SOURCE, conf=0.4)

print("\n===== FINAL WHO MORPHOLOGY RESULTS =====\n")

for r in results:

    boxes = r.boxes.xyxy.cpu().numpy()
    classes = r.boxes.cls.cpu().numpy()
    names = model.names

    parts = {}

    for box, cls in zip(boxes, classes):
        label = names[int(cls)]
        x1, y1, x2, y2 = box

        w = x2 - x1
        h = y2 - y1
        area = w * h

        parts[label] = {"h": h, "area": area}

    if "Head" not in parts or "Tail" not in parts:
        print(os.path.basename(r.path), "→ ABNORMAL (insufficient detection)")
        continue

    head_area = parts["Head"]["area"]
    head_h = parts["Head"]["h"]
    tail_ratio = parts["Tail"]["h"] / head_h

    neck_ratio = None
    if "Neck" in parts:
        neck_ratio = parts["Neck"]["h"] / head_h

    abnormal = False

    # WHO-inspired rules (pixel-relative)
    if head_area < 90 or head_area > 180:
        abnormal = True

    if tail_ratio < 2.3:
        abnormal = True

    if neck_ratio and neck_ratio > 0.85:
        abnormal = True

    if abnormal:
        print(os.path.basename(r.path), "→ WHO RESULT: ABNORMAL")
    else:
        print(os.path.basename(r.path), "→ WHO RESULT: NORMAL")

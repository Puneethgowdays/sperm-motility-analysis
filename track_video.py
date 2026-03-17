from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

model.track(
    source="input_video.avi",
    conf=0.4,
    save=True,
    tracker="botsort.yaml"
)

print("Tracking finished.")
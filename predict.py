from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

model.predict(
    source="test/images",
    conf=0.4,
    save=True
)

print("Prediction complete")

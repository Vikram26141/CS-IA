import os
os.system("pip install -q ultralytics")
from ultralytics import YOLO
model = YOLO("yolov8n.pt")
model.train(
    data="/content/drive/MyDrive/football_yolo/ball.yaml",
    epochs=5,
    imgsz=640,
    freeze=10,
    project="/content/drive/MyDrive/football_yolo/runs",
    name="ball_ft"
)

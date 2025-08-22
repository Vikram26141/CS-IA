from ultralytics import YOLO
model = YOLO("yolov8n.pt")
model.train(data="data/ball.yaml", epochs=5, imgsz=640, freeze=10)

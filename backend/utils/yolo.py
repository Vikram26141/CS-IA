from ultralytics import YOLO
import os, uuid
import torch
import cv2

def detect(input_path, vid_id=None, tasks=None):
    
    original_torch_load = torch.load
    
    def safe_torch_load(*args, **kwargs):
        kwargs['weights_only'] = False
        return original_torch_load(*args, **kwargs)
    
   
    torch.load = safe_torch_load
    
    try:

        ball_model_path = "models/yolov8/ball.pt"
        if os.path.exists(ball_model_path):
            model = YOLO(ball_model_path)
        else:
            model = YOLO("yolov8n.pt")
        out_dir = f"data/processed/{uuid.uuid4()}"
        
        
        if vid_id and tasks:
            cap = cv2.VideoCapture(input_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
            tasks[vid_id]["total_frames"] = total_frames
            tasks[vid_id]["processed_frames"] = 0
        
      
        results = model.predict(input_path, save=True, project=out_dir, name="", stream=True)
        
        if vid_id and tasks:
            frame_count = 0
            for result in results:
                frame_count += 1
                tasks[vid_id]["processed_frames"] = frame_count
                progress = int((frame_count / total_frames) * 100)
                tasks[vid_id]["progress"] = progress
        else:
           
            list(results)
        
        return out_dir
    finally:
       
        torch.load = original_torch_load
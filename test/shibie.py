import torch
from PIL import Image
import numpy as np
import cv2
from pathlib import Path
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression, scale_coords
from yolov5.utils.torch_utils import select_device

def detect_objects(img_path, conf_thres=0.4, iou_thres=0.5, device=''):
    # Load model
    model = attempt_load("yolov5s", map_location=device)

    # Set device
    device = select_device(device)

    # Read image
    img0 = cv2.imread(img_path)

    # Convert image to RGB
    img = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)

    # Inference
    results = model(img)

    # Process detections
    pred = results.pred[0]
    pred = non_max_suppression(pred, conf_thres, iou_thres)

    # Draw bounding boxes
    for det in pred:
        if det is not None and len(det):
            det[:, :4] = scale_coords(img.shape[1:], det[:, :4], img0.shape).round()

            for *xyxy, conf, cls in det:
                label = f'{model.names[int(cls)]} {conf:.2f}'
                xyxy = [int(i) for i in xyxy]
                cv2.rectangle(img0, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
                cv2.putText(img0, label, (xyxy[0], xyxy[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return img0

if __name__ == "__main__":
    # Path to image
    img_path = 'temp.png'

    # Perform inference
    output_img = detect_objects(img_path)

    # Display result
    cv2.imshow('YOLOv5 Object Detection', output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

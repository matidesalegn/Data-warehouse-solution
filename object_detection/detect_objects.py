import os
import torch
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.datasets import LoadImages
from yolov5.utils.general import non_max_suppression, scale_coords
from yolov5.utils.plots import save_one_box
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

def detect_images(source='raw_data/images', weights='yolov5s.pt', imgsz=640):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = DetectMultiBackend(weights, device=device)
    stride, names, pt = model.stride, model.names, model.pt
    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
    results = []

    for path, img, im0s, vid_cap, s in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.float() / 255.0
        if len(img.shape) == 3:
            img = img[None]

        pred = model(img, augment=False, visualize=False)
        pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)

        for i, det in enumerate(pred):
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    save_one_box(xyxy, im0s, file=path.replace(source, 'object_detection/detection_results'), BGR=True)
                    results.append({'image': path, 'bbox': xyxy, 'confidence': conf.item(), 'class': names[int(cls)]})
                    logger.info(f"Detected {names[int(cls)]} with confidence {conf:.2f} in {path}")

    return results

if __name__ == '__main__':
    detect_images()
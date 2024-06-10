import os
import subprocess

def setup_yolo():
    # Clone YOLOv5 repository
    if not os.path.exists('yolov5'):
        subprocess.run(['git', 'clone', 'https://github.com/ultralytics/yolov5.git'], check=True)

    # Install YOLOv5 dependencies
    subprocess.run(['pip', 'install', '-r', 'yolov5/requirements.txt'], check=True)
    subprocess.run(['pip', 'install', 'opencv-python'], check=True)
    subprocess.run(['pip', 'install', 'torch', 'torchvision'], check=True)

if __name__ == '__main__':
    setup_yolo()
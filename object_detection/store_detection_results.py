import os
import logging
import yaml
import cv2
import torch
import psycopg2
from pathlib import Path

# Check and print the current working directory
current_directory = os.getcwd()
print(f'Current working directory: {current_directory}')

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/object_detection_db.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Load configuration
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

db_config = config['postgres']

# COCO Class Names
COCO_CLASSES = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
    "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
    "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza",
    "donut", "cake", "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "TVmonitor", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
    "scissors", "teddy bear", "hair drier", "toothbrush"
]

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
        logging.info('Connected to PostgreSQL database')
        return conn
    except Exception as e:
        logging.error(f'Error connecting to database: {str(e)}')
        return None

def create_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detection_datas (
                    id SERIAL PRIMARY KEY,
                    image_path TEXT,
                    box_coordinates TEXT,
                    confidence_score FLOAT,
                    class_label TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            logging.info('Table detection_datas is ready')
    except Exception as e:
        logging.error(f'Error creating table: {str(e)}')

def detect_objects_in_images(image_paths):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Load YOLOv5s model
    results = []
    for image_path in image_paths:
        img = cv2.imread(image_path)  # Read image using OpenCV
        result = model(img)  # Perform object detection
        results.append((image_path, result))
        logging.info(f"Detected objects in {image_path}")
    return results

def process_detection_results(results):
    processed_results = []
    for image_path, result in results:
        for *box, conf, cls in result.pred[0]:
            # Convert tensor values to floats
            box_coords = ','.join(map(lambda x: str(float(x)), box))
            confidence_score = float(conf)
            class_label = COCO_CLASSES[int(cls)]  # Map class index to class name
            processed_results.append((image_path, box_coords, confidence_score, class_label))
            logging.info(f"Processed detection: {image_path}, {box_coords}, {confidence_score}, {class_label}")
    return processed_results

def store_detection_data_to_database(conn, detection_datas):
    try:
        with conn.cursor() as cursor:
            insert_query = """
                INSERT INTO detection_datas (image_path, box_coordinates, confidence_score, class_label)
                VALUES (%s, %s, %s, %s);
            """
            for data in detection_datas:
                cursor.execute(insert_query, data)
                logging.info(f"Inserting detection: {data}")
            conn.commit()
            logging.info(f'Successfully inserted {len(detection_datas)} records into database')
    except Exception as e:
        logging.error(f'Error storing data to database: {str(e)}')
        print(f'Error storing data to database: {str(e)}')  # Print for debugging

if __name__ == '__main__':
    # Update the path to the images directory
    image_directory = 'D:/Data warehouse solution/object_detection/yolov5/data/images'
    absolute_image_directory = os.path.abspath(image_directory)
    print(f'Absolute path to images directory: {absolute_image_directory}')

    if not os.path.exists(absolute_image_directory):
        logging.error(f'The directory {absolute_image_directory} does not exist.')
        print(f'The directory {absolute_image_directory} does not exist.')
    else:
        image_paths = [os.path.join(absolute_image_directory, img) for img in os.listdir(absolute_image_directory) if img.endswith(('.jpg', '.jpeg', '.png'))]

        if image_paths:
            logging.info(f'Found {len(image_paths)} images in {absolute_image_directory}')
            print(f'Found {len(image_paths)} images in {absolute_image_directory}')

            results = detect_objects_in_images(image_paths)
            processed_results = process_detection_results(results)

            logging.info(f'Processed detection results for {len(processed_results)} images')
            print(f'Processed detection results for {len(processed_results)} images')

            conn = connect_to_db()
            if conn:
                create_table(conn)
                store_detection_data_to_database(conn, processed_results)
                conn.close()
            else:
                logging.error('Could not connect to database')
                print('Could not connect to database')
        else:
            logging.warning(f'No images found in {absolute_image_directory}')
            print(f'No images found in {absolute_image_directory}')
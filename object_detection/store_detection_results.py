import psycopg2
import logging
import json

# Configure logging
logging.basicConfig(filename='logs/detection.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(message)s')

# PostgreSQL connection parameters
db_params = {
    'dbname': 'data_warehouse',
    'user': 'postgres',
    'password': 'Mati@1993',
    'host': 'localhost',
    'port': 5432
}

# Connect to PostgreSQL
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS detection_results (
    id SERIAL PRIMARY KEY,
    image_id TEXT,
    class_label TEXT,
    confidence FLOAT,
    bounding_box INT[]
)
""")
conn.commit()

def store_detection_results(detections):
    try:
        for detection in detections:
            image_id = detection['image_id']
            for det in detection['detections']:
                class_label = det['class_label']
                confidence = det['confidence']
                bounding_box = det['bounding_box']
                cur.execute("""
                INSERT INTO detection_results (image_id, class_label, confidence, bounding_box)
                VALUES (%s, %s, %s, %s)
                """, (image_id, class_label, confidence, bounding_box))
        conn.commit()
        logging.info("Detection results stored successfully.")
    except Exception as e:
        logging.error(f"Error storing detection results: {e}")
        conn.rollback()

# Example detection results
detections = [
    {
        "image_id": "image_001",
        "detections": [
            {
                "class_label": "person",
                "confidence": 0.98,
                "bounding_box": [100, 150, 200, 250]
            },
            {
                "class_label": "bicycle",
                "confidence": 0.87,
                "bounding_box": [50, 80, 150, 200]
            }
        ]
    }
]

# Store detection results
store_detection_results(detections)

# Close connection
cur.close()
conn.close()
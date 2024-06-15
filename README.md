# Data Warehouse Solution for Ethiopian Medical Businesses

## Introduction

This project aims to develop a comprehensive data warehouse solution to store and analyze data related to Ethiopian medical businesses. The data, scraped from Telegram channels, is consolidated into a centralized system. This enables efficient data collection, cleaning, transformation, and analysis, ultimately supporting better decision-making and insights.

## Business Need and Goals

A centralized data warehouse addresses the challenge of fragmented data sources, making it easier to extract meaningful insights. By consolidating data from various Telegram channels, businesses can perform comprehensive analyses to identify trends, patterns, and correlations that inform strategic decisions.

## Key Learning Outcomes

- Telegram scraping using Telethon
- Setting up and managing a data warehouse using PostgreSQL
- Understanding ETL/ELT processes for data transformation
- Object detection using YOLO
- Creating and exposing APIs using FastAPI

## Project Structure

The project is organized into several components, each responsible for a specific part of the data pipeline, ensuring smooth development and maintenance.

### Directory Structure

```
medical_data_warehouse/
├── api/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── requirements.txt
├── data_collection/
│   ├── telegram_scraper.py
│   ├── logging_config.yaml
│   ├── channels.txt
│   ├── requirements.txt
│   ├── raw_data/
│   │   ├── messages.csv
│   │   └── images/
│   └── logs/
│       └── scraping.log
├── data_cleaning/
│   ├── cleaned_data/
│   │   └── messages_cleaned.csv
│   ├── dbt_project/
│   │   ├── dbt_project.yml
│   │   ├── models/
│   │   └── sources.yml
│   ├── cleaned_data.sql
│   ├── transformed_data.sql
├── object_detection/
│   ├── yolo_setup.py
│   ├── detect_objects.py
│   ├── requirements.txt
│   └── detection_results/
│       └── results.csv
├── data_warehouse/
│   ├── setup_postgresql.py
│   ├── schema.sql
│   └── requirements.txt
├── tests/
│   ├── test_scraper.py
│   ├── test_clean_data.py
│   ├── test_yolo.py
│   ├── test_api.py
│   └── test_warehouse.py
├── logs/
│   └── scraping.log
├── README.md
└── .gitignore
```

### Detailed Directory Descriptions

- **`data_collection/`**: Contains scripts and configurations for data scraping from Telegram.
  - `telegram_scraper.py`: Script for scraping Telegram data.
  - `requirements.txt`: Dependencies for the data collection process.
  - `logging_config.yaml`: Configuration for logging.
  - `raw_data/`: Directory for storing raw scraped data.
  - `messages.csv`: CSV file to store scraped messages.
  - `images/`: Directory to store scraped images.

- **`data_cleaning/`**: Contains scripts for data cleaning and transformation.
  - `dbt_project/`: Directory for DBT project.
  - `dbt_project.yml`: DBT project configuration file.
  - `models/`: Directory for DBT models.
  - `cleaned_data.sql`: SQL script for cleaning data.
  - `transformed_data.sql`: SQL script for transforming data.

- **`object_detection/`**: Contains scripts for setting up and running YOLO object detection.
  - `yolo_setup.py`: Script for setting up the YOLO environment.
  - `detect_objects.py`: Script for detecting objects in images.
  - `requirements.txt`: Dependencies for object detection.
  - `detection_results/`: Directory to store object detection results.
  - `results.csv`: CSV file to store detection results.

- **`api/`**: Contains scripts for creating and running the FastAPI application.
  - `main.py`: Main script for the FastAPI application.
  - `database.py`: Script for database configuration using SQLAlchemy.
  - `models.py`: Script defining SQLAlchemy models.
  - `schemas.py`: Script defining Pydantic schemas.
  - `crud.py`: Script implementing CRUD operations.
  - `requirements.txt`: Dependencies for FastAPI.

- **`data_warehouse/`**: Contains scripts and configurations for setting up the data warehouse.
  - `setup_postgresql.py`: Script for setting up PostgreSQL database.
  - `schema.sql`: SQL script for creating database schema.
  - `requirements.txt`: Dependencies for data warehouse setup.

- **`tests/`**: Contains test scripts for various components of the project.
  - `test_scraper.py`: Test cases for the scraper.
  - `test_clean_data.py`: Test cases for data cleaning.
  - `test_yolo.py`: Test cases for YOLO object detection.
  - `test_api.py`: Test cases for the FastAPI application.
  - `test_warehouse.py`: Test cases for the data warehouse.

- **`logs/`**: Directory for storing log files.
  - `scraping.log`: Log file for scraping processes.

- **`README.md`**: Documentation and instructions for the project.

- **`.gitignore`**: Specifies files and directories to be ignored by git.

## Initial Setup

### Initialize Git Repository

```bash
cd medical_data_warehouse
git init
git add .
git commit -m "Initial project structure setup"
```

### Set Up Virtual Environments and Install Dependencies

```bash
# Data Collection
cd data_collection
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

# Data Cleaning
cd data_cleaning
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

# Object Detection
cd object_detection
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

# API
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

# Data Warehouse
cd data_warehouse
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..
```

## Development Steps

### Task 1: Data Collection Pipeline

- **Telegram Scraping using Telethon**
  - Set up Telethon and authenticate with the Telegram API.
  - Identify and list the target channels.
  - Develop scripts to extract data and store it in a temporary database or local files.
  - Implement logging to monitor the scraping process and capture errors.

### Task 2: Data Cleaning and Transformation

- **Cleaning Raw Data**
  - Remove duplicates.
  - Handle missing values.
  - Standardize formats.
- **Data Transformation using DBT**
  - Transform data according to business requirements.
- **Storing Cleaned Data**
  - Store cleaned data in the database.

### Task 3: Data Warehouse Design and Implementation

- **Database Schema Design**
  - Design a database schema optimized for storing and querying large volumes of data.
- **Implementing Relational DBMS (PostgreSQL)**
  - Set up and configure PostgreSQL as the relational database management system.
- **Integrating and Enriching Data**
  - Combine data from multiple sources and ensure data consistency and quality.

#### Data Integration and Enrichment

- **ETL and ELT Processes**
  - Implement ETL/ELT processes to manage data flow from various sources into the data warehouse.
- **Combining Data from Multiple Sources**
  - Develop strategies to integrate and enrich data from different sources.

### Task 3: Object Detection Using YOLO

- **Setting Up YOLO Environment**
  - Set up the YOLO environment for object detection.
- **Collecting and Preparing Images**
  - Collect and prepare images for object detection.
- **Running Object Detection**
  - Run object detection on collected images and store results.

### Task 4: Exposing Data via FastAPI

- **Setting Up FastAPI Environment**
  - Set up the FastAPI environment for API development.
- **Creating API Endpoints**
  - Develop API endpoints for data retrieval and manipulation.
- **CRUD Operations**
  - Implement CRUD operations for interacting with the database.

### Testing, Validation, and Deployment

- **Testing Data Pipelines and APIs**
  - Test the entire data pipeline and API endpoints.
- **Validation of Data Quality and Object Detection Results**
  - Validate data quality and object detection results.
- **Deployment and Maintenance Strategies**
  - Develop strategies for deployment and ongoing maintenance.

## Conclusion and Recommendations

- **Summary of Findings**
  - Summarize the insights and findings from the data analysis.
- **Recommendations for Future Work**
  - Provide recommendations for future improvements and expansions of the data warehouse solution.
- **Insights and Actionable Intelligence**
  - Highlight actionable insights derived from the data analysis.

## Repository

For more details and the complete code, please visit the [GitHub repository](https://github.com/matidesalegn/Data-warehouse-solution.git).
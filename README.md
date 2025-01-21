# Receipt Processor API

A simple Django-based API for processing receipts and calculating reward points based on specific rules. This project uses Django REST Framework and is Dockerized for easy setup and deployment.

---

## Features

- **Submit a Receipt**: Processes a receipt and assigns it a unique ID.
- **Calculate Points**: Retrieves points awarded for a receipt based on predefined rules.
- **Dockerized**: Easily run the application using Docker and Docker Compose.
- **SQLite Database**: Uses Django's default SQLite database for persistence.

---

## API Endpoints

### **1. Submit a Receipt**
**Endpoint**: `/receipts/process`  
**Method**: `POST`  
*
### **1. Get a Receipt points**
**Endpoint**: `/receipts/{id}/points`  
**Method**: `GET`  
*

---

## Prerequisites
- Python 3.11+
- Docker and Docker Compose (if using Docker)
- pip (Python package manager)


---

## Local Setup

```bash
git clone https://github.com/caffeinelover1012/receipt_processor.git
cd receipt-processor
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

The application will be available at http://localhost:8000.

## Docker Setup

```bash
docker-compose build
docker-compose up
```
The application will be available at http://localhost:8000.


## Run Tests

```bash
python manage.py test
```


Shubh Khandelwal    
(shubhvk10@gmail.com)
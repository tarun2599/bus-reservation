# Bus Reservation System API

A Django REST API for managing bus reservations. This system allows users to search for buses based on source, destination, and date, make seat reservations, and view their booking history.

## Features

- Search buses based on source, destination, and date
- Seat reservation system
- View reservation history
- Swagger API documentation

## Tech Stack

- Python 3.10
- Django 4.2.7
- Django REST Framework 3.14
- SQLite Database
- drf-yasg for API documentation

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/tarun2599/bus-reservation.git
cd bus-reservation
```

### 2. Create and activate virtual environment
```bash
python -m venv newtonschool
source newtonschool/bin/activate  # On Windows: newtonschool\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Load sample bus data
```bash
python manage.py loaddata bus_reservation/fixtures/bus_data.json
```

### 6. Run development server
```bash
python manage.py runserver
```

### 7. Api Documentation
API documentation is available via Swagger UI at:

Swagger UI: http://localhost:8000/swagger/

## 8. Postman Collection

You can download the Postman collection to test the API endpoints.

[Download Postman Collection](https://elements.getpostman.com/redirect?entityId=30001369-62cbd1ff-0a45-4a58-9f05-a2e57c851854&entityType=collection)

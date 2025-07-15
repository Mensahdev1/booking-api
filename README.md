# Booking Conflict Checker API

A FastAPI-based API service for managing room bookings and preventing booking conflicts.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API:
```bash
uvicorn main:app --reload
```

3. Run with Docker:
```bash
docker build -t booking-api .
docker run -p 8000:8000 booking-api
```

## API Endpoints

### Get Bookings for a Date
```http
GET /bookings/{date}
```
Example:
```bash
curl http://localhost:8000/bookings/2025-07-15
```

### Create New Booking
```http
POST /bookings
```
Example:
```bash
curl -X POST http://localhost:8000/bookings \
  -H "Content-Type: application/json" \
  -d '{"room_id": "101", "date": "2025-07-15", "start_time": "09:00", "end_time": "11:00"}'
```

## Assumptions
- Time format is in 24-hour format (HH:MM)
- Booking dates are in YYYY-MM-DD format
- No timezone handling (all times are local)
- No authentication required
- In-memory storage is used for simplicity
- Room IDs are strings

## Error Handling
- 400 Bad Request: Invalid date format or booking conflicts
- 500 Internal Server Error: Unexpected errors

## Logging
- All booking operations are logged
- Error details are logged for debugging

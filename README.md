# Booking Conflict Checker API

A FastAPI-based API service for managing room bookings with conflict detection.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables (optional):
```bash
# Create .env file with:
SERVER_PORT=8000    # Default port
MAX_BOOKINGS_PER_DAY=100  # Maximum bookings per day
```

3. Run the API:
```bash
uvicorn main:app --reload
```

4. Run with Docker:
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
Response:
```json
[
    {
        "room_id": "101",
        "date": "2025-07-15",
        "start_time": "09:00",
        "end_time": "11:00",
        "id": "booking_1"
    }
]
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
Response:
```json
{
    "room_id": "101",
    "date": "2025-07-15",
    "start_time": "09:00",
    "end_time": "11:00",
    "id": "booking_1"
}
```

## Error Responses

### Invalid Date Format
```json
{
    "detail": "Invalid date format. Please use YYYY-MM-DD format (e.g., 2025-07-15)"
}
```

### Invalid Time Format
```json
{
    "detail": "Invalid time format. Please use HH:MM format (e.g., 09:00)"
}
```

### Time Order Error
```json
{
    "detail": "End time must be after start time"
}
```

### Booking Conflict
```json
{
    "detail": "Room 101 is already booked during this time. Existing booking: 09:00 to 11:00"
}
```

## Assumptions
1. All times are in 24-hour format (HH:MM)
2. Dates follow YYYY-MM-DD format
3. No timezone handling (all times are local)
4. Room IDs are strings
5. In-memory storage is used for simplicity
6. No authentication required
7. Maximum 100 bookings per day

## Technical Details
- FastAPI backend
- Pydantic models for data validation
- Environment-based configuration
- Modular code structure
- Basic logging
- Unit tests included
- Docker support

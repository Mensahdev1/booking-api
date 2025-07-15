import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_booking_success():
    """Test successful booking creation"""
    response = client.post(
        "/bookings",
        json={
            "room_id": "101",
            "date": "2025-07-16",
            "start_time": "09:00",
            "end_time": "11:00"
        }
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["room_id"] == "101"

def test_create_booking_invalid_date():
    """Test booking creation with invalid date format"""
    response = client.post(
        "/bookings",
        json={
            "room_id": "101",
            "date": "2025/07/16",
            "start_time": "09:00",
            "end_time": "11:00"
        }
    )
    assert response.status_code == 400
    assert "Invalid date format" in response.json()["detail"]

def test_create_booking_invalid_time():
    """Test booking creation with invalid time format"""
    response = client.post(
        "/bookings",
        json={
            "room_id": "101",
            "date": "2025-07-16",
            "start_time": "9:00",
            "end_time": "11:00"
        }
    )
    assert response.status_code == 400
    assert "End time must be after start time" in response.json()["detail"]

def test_get_bookings():
    """Test getting bookings for a date"""
    # Create a booking first
    client.post(
        "/bookings",
        json={
            "room_id": "101",
            "date": "2025-07-16",
            "start_time": "09:00",
            "end_time": "11:00"
        }
    )
    
    response = client.get("/bookings/2025-07-16")
    assert response.status_code == 200
    assert len(response.json()) > 0

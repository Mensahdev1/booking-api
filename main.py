from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVER_PORT = int(os.getenv('SERVER_PORT', 8000))
MAX_BOOKINGS_PER_DAY = int(os.getenv('MAX_BOOKINGS_PER_DAY', 100))

app = FastAPI(title="Booking Conflict Checker")

bookings = {}

class Booking(BaseModel):
    room_id: str
    date: str
    start_time: str
    end_time: str

class BookingResponse(Booking):
    id: str

class BookingService:
    @staticmethod
    def validate_date(date: str):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD format (e.g., 2025-07-15)")

    @staticmethod
    def validate_time(time: str):
        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            raise ValueError("Invalid time format. Please use HH:MM format (e.g., 09:00)")

    @staticmethod
    def check_time_order(start_time: str, end_time: str):
        if end_time <= start_time:
            raise ValueError("End time must be after start time")

    @staticmethod
    def check_conflicts(booking: Booking, existing_bookings: List[Booking]):
        for existing_booking in existing_bookings:
            if existing_booking.room_id == booking.room_id:
                if (booking.start_time < existing_booking.end_time and 
                    booking.end_time > existing_booking.start_time):
                    raise ValueError(
                        f"Room {booking.room_id} is already booked during this time. "
                        f"Existing booking: {existing_booking.start_time} to {existing_booking.end_time}"
                    )

    @staticmethod
    def generate_booking_id(existing_bookings: List[Booking]):
        return f"booking_{len(existing_bookings) + 1}"

@app.get("/bookings/{date}")
def get_bookings(date: str):
    try:
        return bookings.get(date, [])
    except Exception as e:
        logger.error(f"Error fetching bookings: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/bookings", response_model=BookingResponse)
def create_booking(booking: Booking):
    try:
        BookingService.validate_date(booking.date)
        BookingService.validate_time(booking.start_time)
        BookingService.validate_time(booking.end_time)
        BookingService.check_time_order(booking.start_time, booking.end_time)

        existing_bookings = bookings.get(booking.date, [])
        BookingService.check_conflicts(booking, existing_bookings)

        if len(existing_bookings) >= MAX_BOOKINGS_PER_DAY:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum number of bookings ({MAX_BOOKINGS_PER_DAY}) reached for this date"
            )

        booking_id = BookingService.generate_booking_id(existing_bookings)
        if booking.date not in bookings:
            bookings[booking.date] = []
        bookings[booking.date].append(BookingResponse(**booking.dict(), id=booking_id))
        
        logger.info(f"Created booking {booking_id} for room {booking.room_id}")
        return BookingResponse(**booking.dict(), id=booking_id)
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        logger.error(f"HTTP error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )

@app.get("/")
def root():
    return {"message": "Welcome to Booking Conflict Checker API"}

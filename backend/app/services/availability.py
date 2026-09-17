from datetime import datetime

def check_availability(check_in: str, check_out: str, adults: int) -> dict:
    """
    Mock function to check room availability.
    In a real system, this would query a database or external API.
    """
    try:
        ci_date = datetime.strptime(check_in, "%Y-%m-%d")
        co_date = datetime.strptime(check_out, "%Y-%m-%d")
    except ValueError:
        return {"available": False, "message": "Invalid date format. Please use YYYY-MM-DD."}
        
    if co_date <= ci_date:
        return {"available": False, "message": "Check-out date must be after check-in date."}
        
    if adults < 1:
        return {"available": False, "message": "At least 1 adult is required."}
        
    if adults > 4:
        return {"available": False, "message": "No single room can accommodate more than 4 guests."}
        
    # Deterministic mock logic: unavailable on the 13th of any month or Christmas
    if ci_date.day == 13 or (ci_date.month == 12 and ci_date.day == 25):
        return {"available": False, "message": f"Sorry, we are fully booked for those dates ({check_in} to {check_out})."}
    
    available_rooms = []
    if adults <= 2:
        available_rooms.append("Standard Room (₹150/night)")
    if adults <= 3:
        available_rooms.append("Suite (₹250/night)")
    if adults <= 4:
        available_rooms.append("Family Room (₹200/night)")
    
    if available_rooms:
        return {
            "available": True,
            "message": f"We have rooms available for your dates ({check_in} to {check_out}).",
            "options": available_rooms
        }
    else:
        return {"available": False, "message": "Sorry, we have no availability for those dates."}

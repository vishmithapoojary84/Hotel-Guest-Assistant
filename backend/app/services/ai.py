import json
from google.genai import types
from typing import List
from app.core.config import client, HOTEL_DATA

def get_system_instruction() -> str:
    from datetime import datetime
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    return f"""
You are a helpful and polite guest assistant for {HOTEL_DATA['hotel_name']}.
Today's date is {current_date}.
Answer the user's questions using ONLY the provided hotel information below.
If the answer is not in the information, politely state that you do not know or that information is not available.
If the user asks about room availability, you MUST use the check_availability tool. Before calling the tool, you MUST ensure you have the check-in date, check-out date, and the number of adults. If any of these are missing, DO NOT call the tool and instead ask the user for the missing details.
You DO NOT have the ability to make bookings or process payments. DO NOT ask the user if they would like to proceed with a booking. Instead, politely instruct them to contact the front desk to finalize their reservation.
Do not make up policies or amenities.

Hotel Information:
{json.dumps(HOTEL_DATA, indent=2)}
"""

def check_availability(check_in: str, check_out: str, adults: int) -> str:
    """Check if rooms are available for the given dates and number of guests.
    
    Args:
        check_in: The check-in date (e.g. YYYY-MM-DD)
        check_out: The check-out date (e.g. YYYY-MM-DD)
        adults: The number of adults
    """
    from app.services.availability import check_availability as mock_check
    result = mock_check(check_in, check_out, adults)
    return json.dumps(result)

def process_chat_message(message: str, history: List[dict] = None) -> str:
    """
    Process a chat message using Gemini, maintaining context and handling tools.
    """
    if not client:
        return "System Error: AI service is currently unavailable due to missing API key."

    formatted_history = []
    if history:
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            formatted_history.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))
            
    try:
        chat = client.chats.create(
            model="gemini-3.1-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=get_system_instruction(),
                tools=[check_availability],
                temperature=0.0
            ),
            history=formatted_history
        )
        
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return "I'm sorry, I'm having trouble processing your request right now. Please try again later."

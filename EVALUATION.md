# Evaluation Scenarios

As per the assignment requirements, here are the documented evaluation scenarios to verify the AI Guest Assistant's capabilities. These can be tested manually through the UI or automatically via `pytest`.

### 1. Normal Guest Question
- **Input**: "Do you have a swimming pool?"
- **Expected Outcome**: The AI strictly reads from `hotel.json` and confirms the presence of a pool.

### 2. Question with Missing Information
- **Input**: "Can I check availability for tomorrow?"
- **Expected Outcome**: The AI should ask for the missing details (check-in/check-out dates and number of guests) before attempting to call the availability tool.

### 3. Ambiguous Question
- **Input**: "Is it good for families?"
- **Expected Outcome**: The AI infers that the hotel has a "Family Room" with a capacity of 4 and presents that as a supportive answer.

### 4. Availability / Tool-Calling Request
- **Input**: "I need a room from October 10th to October 12th, 2026 for 2 adults."
- **Expected Outcome**: The AI invokes the `check_availability` tool, receives the options (Standard, Suite, Family), and formats them neatly for the user.

### 5. Incorrect or Unsupported Assumptions (Hallucination Prevention)
- **Input**: "Can I bring my dog?"
- **Expected Outcome**: Since pet policies are not in `hotel.json`, the AI must fall back to its system instruction and say "I don't know" or "That information is not available," rather than making up a generic pet policy.

### 6. Conversation Follow-ups
- **Input**: User asks "Do you have a pool?". AI answers "Yes". User follows up: "What time does it close?"
- **Expected Outcome**: The AI understands "it" refers to the pool, but since pool hours aren't in the JSON, it gracefully declines to answer.

### 7. Frontend Loading and Error States
- **Input**: Submit a question and immediately turn off the backend server.
- **Expected Outcome**: The frontend shows a bouncing loading animation, then catches the network error and displays a safe, user-friendly fallback message ("⚠️ Sorry, an error occurred...").

### 8. Backend / Model Failure
- **Scenario**: The `GEMINI_API_KEY` is removed from `.env`.
- **Expected Outcome**: The backend catches the initialization failure and safely returns "System Error: AI service is currently unavailable...", which the frontend renders perfectly without crashing.

### 9. Invalid Dates Validation
- **Input**: "Check availability from October 20th to October 10th for 2 people."
- **Expected Outcome**: The deterministic mock tool calculates that check-out is before check-in and strictly returns a validation error. The AI passes this specific failure reason back to the user.

### 10. End-to-End Flow
- **Scenario**: A user opens the UI, asks about breakfast (gets a "yes"), follows up with availability for 3 adults on December 25th (is told they are fully booked), and then asks for December 26th (is given the Suite and Family Room options).
- **Expected Outcome**: The conversation flows naturally, context is maintained throughout, and tool calls operate predictably behind the scenes.

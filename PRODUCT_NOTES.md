# Product, UX & AI Decisions

## 1. Problem Solved & Guest Journey
**Problem**: Guests often have simple, repetitive questions (check-in times, breakfast, pool) and want to know if rooms are available without navigating through complex booking engines or calling the front desk.
**Guest Journey**: A guest lands on the website, opens the chat widget, asks a question in natural language (e.g., "Do you have a pool?"), and receives an immediate, accurate answer based on the hotel's data.

## 2. Frontend Design
- **Clean & Conversational**: Kept the UI familiar (like typical messaging apps) so guests instantly know how to use it.
- **Loading States**: Added bouncing dots to indicate when the AI is "typing", managing expectations since LLM calls can take a few seconds.
- **Error Handling**: Graceful fallback UI if the backend is down or the AI service fails.

## 3. AI vs Deterministic Logic
- **AI (Gemini)**: Handles natural language understanding, context management, and extracting parameters (dates, guests) from fuzzy user input.
- **Deterministic**: The actual availability check (`app/services/availability.py`) is purely deterministic. The AI simply extracts the dates and calls the tool. This prevents the LLM from "hallucinating" available rooms.

## 4. Hallucination Prevention
- **Strict System Prompt**: The system instruction explicitly commands the model to *only* use the provided JSON knowledge base and state "I don't know" otherwise.
- **Temperature = 0.0**: Ensures the most probable (and least creative) response, which is desired for factual customer service.

## 5. Failure States
- **Backend/Model Failure**: If the API key is missing or Gemini is down, `process_chat_message` returns a predefined string, which the backend safely returns to the frontend without crashing.
- **Network Failure**: The frontend uses a `try/catch` block to detect network failures and displays a user-friendly error message within the chat UI.

## 6. Measuring Success & Future Improvements
- **Metrics**: 
  - Deflection rate (how many user sessions end without requiring human intervention).
  - Conversion rate (users who check availability via chat and then proceed to book).
- **Production Improvements**:
  - Store chat sessions in a database instead of relying purely on frontend history passing (to handle page refreshes).
  - Implement rate limiting and authentication/session management to prevent abuse.
  - Connect the availability tool to a real Property Management System (PMS) via REST API.

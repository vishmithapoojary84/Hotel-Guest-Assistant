# Oceanview Resort Guest Assistant

A full-stack AI-powered hotel guest assistant.

## Tech Stack
- **Frontend**: React + Vite + CSS
- **Backend**: FastAPI + Python (managed with `uv`)
- **AI Model**: Google Gemini (`google-genai` SDK)

## Setup Instructions

### 1. Backend Setup
1. Navigate to the `backend` directory.
2. Initialize and activate the virtual environment using `uv`:
   ```bash
   cd backend
   uv venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Add your Gemini API key to `.env`: `GEMINI_API_KEY=your_api_key_here`
5. Run the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

### 2. Frontend Setup
1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```

## Architecture & Data Flow
1. **Frontend**: A React application providing a conversational UI. It sends user queries along with chat history to the backend API.
2. **Backend**: A FastAPI service that receives the chat requests.
3. **AI Integration**: Uses Google's `google-genai` SDK with Gemini. The model is given a strict system prompt containing the hotel's knowledge base (`app/data/hotel.json`) and a tool for checking availability.
4. **Availability Tool**: A deterministic Python function (`check_availability`) that Gemini can invoke when a user asks for room availability.

## Backend API Example

You can test the chat endpoint directly using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Do you have a pool?", "history": []}'
```

**Response**:
```json
{
  "reply": "Yes, Oceanview Resort has a swimming pool."
}
```

## AI Tools Used
- **Antigravity AI Assistant**: Used as the primary pair-programming agent to architect, write, and test the full-stack codebase.
- **Google Gemini 3.1 Pro/Flash-Lite**: The underlying foundation models powering both the development assistant and the hotel chatbot itself.

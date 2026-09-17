from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_chat_missing_fields():
    response = client.post("/api/chat", json={})
    assert response.status_code == 422 

def test_availability_logic():
    from app.services.availability import check_availability
    
    # 1. Invalid date format
    res = check_availability("10-10-2026", "2026-10-12", 2)
    assert res["available"] == False
    assert "Invalid date format" in res["message"]
    
    # 2. Check-out before check-in
    res = check_availability("2026-10-20", "2026-10-10", 2)
    assert res["available"] == False
    assert "after check-in" in res["message"]
    
    # 3. 0 guests
    res = check_availability("2026-10-10", "2026-10-12", 0)
    assert res["available"] == False
    
    # 4. Over 4 guests
    res = check_availability("2026-10-10", "2026-10-12", 5)
    assert res["available"] == False
    
    # 5. Unavailable dates (e.g. 13th)
    res = check_availability("2026-10-13", "2026-10-15", 2)
    assert res["available"] == False
    assert "fully booked" in res["message"]
    
    # 6. Valid availability (2 guests)
    res = check_availability("2026-10-10", "2026-10-12", 2)
    assert res["available"] == True
    assert len(res["options"]) == 3 

# Note: The following tests make real calls to the Gemini API if the key is present.
# In a true CI environment, we would mock the `google-genai` client.
def test_ai_normal_question():
    response = client.post("/api/chat", json={"message": "Do you have a swimming pool?"})
    assert response.status_code == 200
    assert "pool" in response.json()["reply"].lower() or "yes" in response.json()["reply"].lower()

def test_ai_unsupported_question():
    response = client.post("/api/chat", json={"message": "Who is the president of the moon?"})
    assert response.status_code == 200
    reply = response.json()["reply"].lower()
    assert "don't know" in reply or "not available" in reply or "cannot answer" in reply or "do not have" in reply or "hotel information" in reply

def test_ai_follow_up():
    # Simulate a conversation
    history = [
        {"role": "user", "content": "What is the cancellation policy?"},
        {"role": "assistant", "content": "Free cancellation up to 48 hours before check-in."}
    ]
    response = client.post("/api/chat", json={"message": "What about check in time?", "history": history})
    assert response.status_code == 200
    assert "3:00" in response.json()["reply"] or "15:00" in response.json()["reply"]

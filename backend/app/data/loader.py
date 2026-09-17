import json
import os

def load_hotel_data():
    file_path = os.path.join(os.path.dirname(__file__), "hotel.json")
    with open(file_path, "r") as f:
        return json.load(f)

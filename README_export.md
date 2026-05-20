# Flashcard Export

It exports flashcards as JSON or CSV

# This is how you run the microservice
python export_ms.py
Runs on port 5557 via ZeroMQ REQ/REP.

# This is how it is request
Send JSON to tcp://localhost:5557 with: deck_name, cards, format ("json" or "csv")

import zmq, json
socket = zmq.Context().socket(zmq.REQ)
socket.connect("tcp://localhost:5557")
socket.send_string(json.dumps({
    "deck_name": "Math",
    "cards": [{"front": "2+2?", "back": "4"}],
    "format": "json"
}))

# How it is received
response = json.loads(socket.recv_string())

Success: {"status": "ok", "format": "json", "data": "..."}
Error:   {"status": "error", "message": "No cards provided"}

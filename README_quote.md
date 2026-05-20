# Quote of the Day Microservice

This microservice gives a motivational quote randomly

# How the microservice is started
python quote_ms.py
Runs on port 5559 via ZeroMQ REQ/REP.

# How it is requested
Send JSON to tcp://localhost:5559 with: topic ("perseverance", "focus", "general", or "random")

import zmq, json
socket = zmq.Context().socket(zmq.REQ)
socket.connect("tcp://localhost:5559")
socket.send_string(json.dumps({
    "topic": "perseverance"
}))

# How it is reciveved
response = json.loads(socket.recv_string())

Success: {"status": "ok", "quote": "...", "author": "...", "category": "perseverance"}
Error:   {"status": "error", "message": "Unknown category 'basketball'", "available_categories": [...]}

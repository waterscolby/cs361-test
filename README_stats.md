# Study Stats 

This microservice logs study session data and gives the stats back

# How it is run 
python stats_ms.py
Runs on port 5558 via ZeroMQ REQ/REP.

# How it is requested
Send JSON to tcp://localhost:5558 with: action ("log", "get", or "reset"), user_id, session_data (for log only)

import zmq, json
socket = zmq.Context().socket(zmq.REQ)
socket.connect("tcp://localhost:5558")
socket.send_string(json.dumps({
    "action": "get",
    "user_id": "colby"
}))

# How it is recieved
response = json.loads(socket.recv_string())

Success (get): {"status": "ok", "total_reviewed": 10, "sessions": 2, "avg_rating": 3.3}
Success (log): {"status": "ok", "message": "Session logged"}
Error:         {"status": "error", "message": "Unknown action"}

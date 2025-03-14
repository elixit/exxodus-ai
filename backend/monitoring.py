import json
import datetime

def log_activity(log_file, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"logs/{log_file}", "a") as log:
        log.write(f"[{timestamp}] {message}\n")

def track_outreach(client_email):
    with open("backend/clients.json", "r+") as file:
        clients = json.load(file)
        if client_email in clients:
            clients[client_email]["outreach_sent"] += 1
            file.seek(0)
            json.dump(clients, file, indent=4)

def track_response(client_email):
    with open("backend/clients.json", "r+") as file:
        clients = json.load(file)
        if client_email in clients:
            clients[client_email]["responses"] += 1
            file.seek(0)
            json.dump(clients, file, indent=4)

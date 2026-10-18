import json
from pathlib import Path

def load_tickets(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8")as file:
            return json.load(file)
    
    except FileNotFoundError as error:
        return {}

    except json.JSONDecodeError as error:
        raise ValueError(
            f"cannot load tickets, invalid Json in {file_path}: {error}"
            ) from error

def save_tickets(tickets,file_path):
        with open(file_path, 'w', encoding="utf-8")as file:
            json.dump(tickets, file, indent=4)
        
import os
import json
import logging
from datetime import datetime, timedelta

ECONOMY_PATH = os.path.join("data", "economy.json")

def load_economy_data():
    # Завантаження даних економіки. Бо без цього бот нічого не знає про гроші. 💰
    with open(ECONOMY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_economy_data(data):
    # Збереження даних економіки. Бо гроші мають бути під контролем. 🏦
    with open(ECONOMY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def update_credit_data(user_id, amount, interest_rate):
    data = load_economy_data()
    user_data = data.get(user_id, {"wallet": 0, "bank": 0, "credit": 0, "credit_date": None})

    if user_data["credit_date"] is None:
        user_data["credit_date"] = datetime.now().isoformat()
    
    credit_date = datetime.fromisoformat(user_data["credit_date"])
    days_passed = (datetime.now() - credit_date).days

    if days_passed > 0:
        interest = user_data["credit"] * (interest_rate / 100) * days_passed
        user_data["credit"] += interest
        user_data["credit_date"] = datetime.now().isoformat()

    user_data["credit"] += amount
    data[user_id] = user_data
    save_economy_data(data)

def get_user_credit(user_id):
    data = load_economy_data()
    return data.get(user_id, {}).get("credit", 0)

def reset_user_credit(user_id):
    data = load_economy_data()
    if user_id in data:
        data[user_id]["credit"] = 0
        data[user_id]["credit_date"] = None
        save_economy_data(data)
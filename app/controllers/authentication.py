import bcrypt
from app import db

def get_user_by_email(email: str):
    return db["users"].find_one({"email": email})

def create_user(email: str, name: str, password: str, phone: str):
    password = bytes(password, 'utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    payload = {
        "email": email,
        "name": name,
        "password": hashed_password,
        "phone": phone,
        "ticket": ""
    }
    db["users"].insert_one(payload)

    return payload

def update_ticket(email: str, ticket: str):
    db["users"].update_one({"email": email}, {"$set": {"ticket": ticket}})
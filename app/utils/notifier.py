from functools import partial
from fastapi import BackgroundTasks

db_users: dict[str, dict] = {
    "fer": {
        "id": 1,
        "username": "fer",
        "email": "mferna.92@gmail.com",
        "password": "ferpass#hash"
    },
    "ana": {
        "id": 2,
        "username": "ana",
        "email": "ana@example.com",
        "password": "ana123#hash"
    },
    "luis": {
        "id": 3,
        "username": "luis",
        "email": "luis@example.com",
        "password": "luis123#hash"
    },
    "maria": {
        "id": 4,
        "username": "maria",
        "email": "maria@example.com",
        "password": "maria123#hash"
    },
    "jose": {
        "id": 5,
        "username": "jose",
        "email": "jose@example.com",
        "password": "jose123#hash"
    },
    "carla": {
        "id": 6,
        "username": "carla",
        "email": "carla@example.com",
        "password": "carla123#hash"
    }
}

def send_email(email: str, subject: str, body: str) -> None:
    # ToDo: Integrate SENDGRID, SMTPLIB, etc
    print(f"Sending email to {email} | Subject: {subject} | Body: {body}")

def notify_admins(product_sku: str, user: str, background_tasks: BackgroundTasks):
    other_admins = [u for u in db_users.values() if u["username"] != user]
    for admin in other_admins:
        background_tasks.add_task(partial(
                send_email,
                admin["email"], 
                f"Product {product_sku} updated", 
                "Details..."
            ))


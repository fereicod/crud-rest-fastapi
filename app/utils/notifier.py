from functools import partial
from app.routers.admin import db_users
from fastapi import BackgroundTasks


def send_email(email: str, subject: str, body: str) -> None:
    # ToDo: Integrate SENDGRID, SMTPLIB, etc
    print(f"Sending email to {email} | Subject: {subject} | Body: {body}")

def notify_admins(product: dict, user: str, background_tasks: BackgroundTasks):
    other_admins = [u for u in db_users.values() if u["username"] != user]
    for admin in other_admins:
        background_tasks.add_task(partial(
                send_email,
                admin["email"], 
                f"Product {product['sku']} updated", 
                "Details..."
            ))


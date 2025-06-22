from celery import shared_task
from twilio.rest import Client
from app.models import User
from celery.schedules import crontab

import os

@shared_task


def register_tasks(celery):
    celery.conf.beat_schedule = {
        "daily-sms-reminder": {
            "task": "app.tasks.reminders.send_daily_sms_reminders",
            "schedule": 30.0,  # 6 PM IST
        }
    }
@shared_task
def send_daily_sms_reminders():
    from app import db
    from app.models import User
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

    users = User.query.filter_by(role='user').all()

    print(f"[DEBUG] Found {len(users)} users")
    for user in users:
        print(f"[DEBUG] Checking user {user.id} - {user.phone_number}")
        if user.phone_number:
            print(f"[DEBUG] Sending SMS to {user.phone_number}")
            client.messages.create(
                body="📢 Daily Parking Reminder: Don't forget to book your spot today!",
                from_=os.getenv("TWILIO_PHONE_NUMBER"),
                to=user.phone_number
            )


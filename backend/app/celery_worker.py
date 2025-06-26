from celery import Celery
from app import create_app, db, mail
from celery.schedules import crontab

# Step 1: Initialize Flask app
flask_app = create_app()

# Step 2: Make Celery app
def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["broker_url"],
        backend=app.config["result_backend"]
    )
    celery.conf.update(app.config)

    celery.conf.timezone = 'Asia/Kolkata'
    celery.conf.enable_utc = False

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(flask_app)

# Step 3: Import and register tasks *after* celery is defined
from app.tasks.export import register_tasks as register_export_tasks
from app.tasks.reminders import register_tasks as register_reminder_tasks
from app.tasks.monthly import register_tasks as register_monthly_tasks

register_export_tasks(celery)
register_reminder_tasks(celery)
register_monthly_tasks(celery, db, mail)


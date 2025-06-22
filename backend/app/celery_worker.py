from celery import Celery
from app import create_app
from celery.schedules import crontab

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

flask_app = create_app()
celery = make_celery(flask_app)

from app.tasks.export import register_tasks as register_export_tasks
from app.tasks.reminders import register_tasks as register_reminder_tasks


register_export_tasks(celery)
register_reminder_tasks(celery)



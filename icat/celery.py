import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'icat.settings')

app = Celery('icat')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks(['common.tasks.tasks'])


app.conf.beat_schedule = {
    'send_phising_email': {
        'task': 'common.tasks.tasks.send_phising_email',
        'schedule': crontab(hour=6, minute=0),
    }
}

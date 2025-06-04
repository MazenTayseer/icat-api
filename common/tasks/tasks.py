from icat import celery_app


@celery_app.task
def send_phising_email():
    print("Sending phising email")

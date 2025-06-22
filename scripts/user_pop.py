from setup import django_setup

django_setup()

from django.contrib.auth import get_user_model

if __name__ == "__main__":
    get_user_model().objects.all().delete()
    get_user_model().objects.create_user(
        email="mazen_tayseer@icloud.com",
        first_name="Mazen",
        last_name="Tayseer",
        password="Test1234",
        receive_emails=True,
    )

    print("Database populated successfully")

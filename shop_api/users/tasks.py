from celery import shared_task
from time import sleep
from django.conf import settings
from django.core.mail import send_mail
from users.models import CustomUser
from datetime import date

@shared_task
def add(x, y):
    print(f'args {x} and {y}')
    sleep(10)
    return x + y


@shared_task
def send_otp_mail(email, code):
    print(10* "#")
    send_mail(
        "Registration for you",
        f"Ваш одноразовый код: {code}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return 'OK'


@shared_task
def process_inactive_users():
    inactive_users = CustomUser.objects.filter(is_active=False)
    for user in inactive_users:
        user.delete()
    return f'Processed {inactive_users.count()} inactive users'


@shared_task
def sent_birthdate_emails():
    today = date.today()
    birthdate_users = CustomUser.objects.filter(
        is_active=True,
        birthdate__month=today.month,
        birthdate__day=today.day
    )

    for user in birthdate_users:
        send_mail(
            'Happy Birthday!',
            f'🎉 Поздравляем {user.email} с днем рождения! 🎉',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    return f'Sent birthday emails to {birthdate_users.count()} users'

import datetime
import environ

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

env = environ.Env()
environ.Env.read_env()

def final_send_mail(reg_try):
    context = {
        'registration_link': f'http://127.0.0.1:8000/registration/{reg_try.code}'
        # more data here for customisation email.
    }

    registration_mail = {
        'subject': 'DjangoBoy Blog registration',
        'message': 'DjangoBoy Blog registration',  # todo: Don't send message
        'from_email': env('auth_user'),
        'recipient_list': [reg_try.email],
        'fail_silently': False,
        'auth_user': env('auth_user'),
        'auth_password': env('auth_password'),
        'html_message': render_to_string('registration_mail.html', context=context),
    }
    send_mail(**registration_mail)


def final_creation(validated_data, reg_try):
    user = User.objects.create(
        username=validated_data['username'],
        email=reg_try.email,
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name']
    )
    user.set_password(validated_data['password'])
    user.save()
    reg_try.confirmation_time = datetime.datetime.now()
    reg_try.save()
    return user

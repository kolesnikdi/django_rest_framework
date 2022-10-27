import os
import random
import string

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings


def final_send_mail(reg_try):
    context = {
        'registration_link': f'{settings.HOST}/registration/{reg_try.code}'
        # more data here for customisation email.
    }

    registration_mail = {
        'subject': 'DjangoBoy Blog registration',
        'message': 'DjangoBoy Blog registration',
        'from_email': os.environ.get('auth_user', 'segareta@ukr.net'),
        'recipient_list': [reg_try.email],
        'fail_silently': False,
        'auth_user': os.environ.get('auth_user', 'segareta@ukr.net'),
        'auth_password': os.environ.get('auth_password', 'pNyBVB8lOlC4CfM5'),
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
    reg_try.confirmation_time = timezone.now()
    reg_try.save()
    return user

# todo - Навіть і не знаю чи лаконічніше тримати це тут чи в фікстурах.
# def randomizer_choice(name_for_randomize):
#     data_for_randomizer = ''.join(random.choice(string.hexdigits) for i in range(10))
#     if name_for_randomize == 'email':
#         return data_for_randomizer + "@gmail.com"
#     if name_for_randomize in ['username', 'password', 'password2']:
#         return data_for_randomizer
#     elif name_for_randomize in ['first_name', 'last_name']:
#         return ''.join(random.choice(string.ascii_letters) for i in range(10)).title()
#     if name_for_randomize == 'user':
#         user = {
#             'username': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
#             'first_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
#             'last_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
#             'password': data_for_randomizer
#         }
#         return user

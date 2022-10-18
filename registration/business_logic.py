import datetime

from django.contrib.auth.models import User

mail = {
    'subject': 'DjangoBoy Blog registration',
    'message': 'Here is your registration url--->',  # todo: Don't send message
    'from_email': 'segareta@ukr.net',
    'fail_silently': False,
    'auth_user': 'segareta@ukr.net',
    'auth_password': 'pNyBVB8lOlC4CfM5',
}


def final_creation(serializer, reg_try):
    user = User.objects.create(
        username=serializer.validated_data['username'],
        email=reg_try.email,
        first_name=serializer.validated_data['first_name'],
        last_name=serializer.validated_data['last_name']
    )
    user.set_password(serializer.validated_data['password'])
    user.save()
    reg_try.confirmation_time = datetime.datetime.now().replace(microsecond=0)
    # todo: Can we change only - auto_now=True or we must import datetime and set?
    reg_try.save()
    return user, reg_try

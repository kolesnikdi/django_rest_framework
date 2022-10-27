import pytest
import random
import string

from django.urls import reverse
from rest_framework.test import APIClient
from registration.models import RegistrationTry


# @pytest.fixture(scope='function')
# def randomizer_choice(name_for_randomize): # todo - not supported. Can't take argument
#    data_for_randomizer = ''.join(random.choice(string.hexdigits) for i in range(10))
#    if name_for_randomize == 'email':
#       return data_for_randomizer + "@gmail.com"
#    if name_for_randomize in ['username', 'password', 'password2']:
#       return data_for_randomizer
#    if name_for_randomize in ['first_name', 'last_name']:
#       return ''.join(random.choice(string.ascii_letters) for i in range(10)).title()
#    if name_for_randomize == 'user':
#       user = {
#          'username': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
#          'first_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
#          'last_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
#          'password': data_for_randomizer
#       }
#       return user


# @pytest.fixture(scope='function')  # todo - ValueError: class fixtures not supported (maybe in the future)
# class Randomizer_choice:
#
#    data_for_randomizer = ''.join(random.choice(string.hexdigits) for i in range(10))
#
#    @pytest.fixture(scope='function')
#    def r_email(self):
#       return self.data_for_randomizer + "@gmail.com"
#
#    def upp2_data(self):
#       """ randomize data for username, password, password2"""
#       return self.data_for_randomizer
#
#    def _name(self):
#       """ randomize data for first_name, last_name"""
#       return ''.join(random.choice(string.ascii_letters) for i in range(10)).title()
#
#    def user(self):
#       user = {
#          'username': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
#          'first_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
#          'last_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
#          'password': self.data_for_randomizer
#       }
#       return user

data_for_randomizer = ''.join(random.choice(string.hexdigits) for i in range(10))


@pytest.fixture(scope='function')
def random_email():
    return data_for_randomizer + "@gmail.com"


@pytest.fixture(scope='function')
def random_upp2_data():
    """ randomize data for username, password, password2"""
    return ''.join(random.choice(string.hexdigits) for i in range(10))


@pytest.fixture(scope='function')
def random_name():
    """ randomize data for first_name, last_name"""
    return ''.join(random.choice(string.ascii_letters) for i in range(10)).title()


@pytest.fixture(scope='function')
def random_user():
    user = {
        'username': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
        'first_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
        'last_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
        'password': data_for_randomizer
    }
    return user


@pytest.fixture
def reg_try(random_email, api_client):
    url = reverse('registration')
    data = {
        'email': random_email,
    }
    response = api_client.post(url, data=data, format='json')
    return response


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def reg_done_code(api_client, reg_try, random_user):
    data_reg_try = RegistrationTry.objects.get(email=reg_try.data['email'])
    code = data_reg_try.code
    url = reverse('registration_confirm', args=[code])
    random_user.update({'password2': random_user['password']})
    response = api_client.post(url, data=random_user, format='json')
    for_check_reg_try = RegistrationTry.objects.get(id=data_reg_try.id)
    return for_check_reg_try.code

# todo - can not finde way to make @pytest.mark.django_db(autouse=True)
# @pytest.fixture(autouse=True)
# @pytest.mark.django_db
# def django_db():
#    ...
#
# @pytest.fixture(autouse=True)
# class TestTest:
#     @pytest.mark.django_db

# @pytest.mark.django_db
# @pytest.fixture(scope='session', autouse=True)
# def db(request, django_db_blocker):
#     """
#     Override pytest-django `db` fixture to be session scoped
#     """
#     django_db_blocker.unblock()
#     return

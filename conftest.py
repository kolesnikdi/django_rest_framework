import pytest
import random
import string

from django.urls import reverse
from rest_framework.test import APIClient

from blog.models import Post
from registration.models import RegistrationTry

"""randomizers"""


@pytest.fixture(scope='function')
def randomizer():
    return Randomizer()


class Randomizer:

    def email(self):
        """ randomize data for email"""
        return ''.join(random.choice(string.hexdigits) for i in range(10)) + "@gmail.com"

    def upp2_data(self):
        """ randomize data for username, password, password2"""
        return ''.join(random.choice(string.hexdigits) for i in range(10))

    def random_name(self):
        """ randomize data for first_name, last_name"""
        return ''.join(random.choice(string.ascii_letters) for i in range(10)).title()

    def user(self):
        """ randomize data user"""
        user = {
            'username': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
            'first_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
            'last_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
            'password': ''.join(random.choice(string.hexdigits) for i in range(10))
        }
        return user


@pytest.fixture(scope='function')  # just for practice
def randomizer_func():
    def _choice(name_for_randomize):
        if name_for_randomize == 'email':
            return ''.join(random.choice(string.hexdigits) for i in range(10)) + "@gmail.com"
        if name_for_randomize in ['username', 'password', 'password2']:
            return ''.join(random.choice(string.hexdigits) for i in range(10))
        if name_for_randomize in ['first_name', 'last_name']:
            return ''.join(random.choice(string.ascii_letters) for i in range(10)).title()
        if name_for_randomize == 'user':
            user = {
                'username': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
                'first_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
                'last_name': ''.join(random.choice(string.ascii_letters) for i in range(10)).title(),
                'password': ''.join(random.choice(string.hexdigits) for i in range(10))
            }
            return user

    return _choice


"""created custom users"""


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope='function')
def my_user(django_user_model, randomizer):
    return django_user_model.objects.create_user(username=randomizer.random_name(), password=randomizer.upp2_data())


@pytest.fixture(scope='function')
def my_user_second(django_user_model, randomizer):
    return django_user_model.objects.create_user(username=randomizer.upp2_data(), password=randomizer.random_name())


@pytest.fixture(scope='function')
def authenticated_client(api_client, my_user):
    api_client.force_login(my_user)
    api_client.user = my_user
    yield api_client  # return api_client with authenticated user (like method)


@pytest.fixture(scope='function')
def authenticated_user(api_client, my_user_second):
    api_client.force_login(my_user_second)
    return my_user_second  # return authenticated user
    # return api_client.force_login(my_user) # return only authentication


"""fixture for registration app"""


@pytest.fixture
def reg_try(randomizer, api_client):
    url = reverse('registration')
    data = {
        'email': randomizer.email(),
    }
    response = api_client.post(url, data=data, format='json')
    return response


@pytest.fixture
def reg_done_code(api_client, reg_try, randomizer):
    validated_data = randomizer.user()
    data_reg_try = RegistrationTry.objects.get(email=reg_try.data['email'])
    url = reverse('registration_confirm', args=[data_reg_try.code])
    validated_data.update({'password2': validated_data['password']})
    api_client.post(url, data=validated_data, format='json')
    for_check_reg_try = RegistrationTry.objects.get(id=data_reg_try.id)
    return for_check_reg_try.code


"""fixture for blog app"""


@pytest.fixture
def created_blog(my_user, randomizer):
    blog = Post.objects.create(author=my_user, title=randomizer.random_name(), text=randomizer.upp2_data())
    return blog


@pytest.fixture
def created_blog_bu_user_second(my_user_second, randomizer):
    blog = Post.objects.create(author=my_user_second, title=randomizer.random_name(), text=randomizer.upp2_data())
    return blog

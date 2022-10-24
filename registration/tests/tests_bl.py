import pytest
import uuid

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status

from registration.business_logic import final_creation, randomizer_choice
from registration.models import RegistrationTry
from registration.serializers import CreateRegisterTrySerializer

# todo: how to use Factory? And what ia it?
# todo: Can we do as below?
# @pytest.fixture
# def user_data():
#    return {'email': randomizer_choice('email'), 'username': randomizer_choice('username')}


@pytest.fixture
def api_client():               # todo: For why we need it?
   from rest_framework.test import APIClient
   return APIClient()


class TestBLFunctional:

    @pytest.mark.django_db
    def test_final_creation(self):
        validated_data = randomizer_choice('user')
        reg_try = RegistrationTry.objects.create(email=randomizer_choice('email'),)

        result = final_creation(validated_data, reg_try)

        assert isinstance(result, User)
        assert result.username == validated_data['username']
        assert result.first_name == validated_data['first_name']
        assert result.last_name == validated_data['last_name']
        assert result.email == reg_try.email

        assert reg_try.id is not None        #Did you mean this? # TODO: get reg_try from DB bu id
        assert reg_try.creation_time is not None
        assert reg_try.confirmation_time is not None

    # @pytest.mark.django_db
    # @pytest.mark.parametrize(
    #     'email, password, status_code', [
    #         ('', '', 400),
    #         ('', randomizer_choice('password'), 400),
    #         (randomizer_choice('email'), '', 400),
    #         (randomizer_choice('email'), 'invalid_pass', 400),
    #         (randomizer_choice('email'), randomizer_choice('password'), 201)]
    #          )
    # def test_login_data_validation(self, email, password, status_code, api_client):
    #     url = reverse('rest_framework:login')
    #     data = {
    #         'email': email,
    #         'password': password,
    #     }
    #     response = api_client.post(url, data=data, format='json')
    #     assert response.status_code == status_code

    @pytest.mark.django_db
    @pytest.mark.parametrize('email', ['abc@abc.com'])
    def test_login_data_validation(self, email, api_client):
        url = reverse('registration')
        data = {
            'email': email,
        }
        response = api_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        response_json = response.json()

        assert response_json
        assert set(response_json.keys()) == set(CreateRegisterTrySerializer.Meta.fields)
        assert response_json['email'] == email





    # @pytest.mark.django_db
    # @pytest.mark.parametrize(
    #     'username, email, first_name, last_name, password, status_code', [
    #         (randomizer_choice('username'), randomizer_choice('email'), randomizer_choice('first_name'),  # todo - Нащо ми тут задаєм параметри, якщо потім їх вказуємо в pytest.param?
    #          randomizer_choice('last_name'), 'invalid_pass', 400),  # todo - Це взаємопризнана команда що пароль не вірний?
    #         pytest.param(None, None, None, None, None, 400,marks=pytest.mark.bad_request),
    #         pytest.param(None, None, None, None,'strong_pass', 400, marks=pytest.mark.bad_request,
    #                      id='bad_request_with_pass'),  # todo - Це взаємопризнана команда що пароль вірний?
    #         pytest.param(None, randomizer_choice('email'), None, None, 400, marks=[pytest.mark.bad_request, pytest.mark.xfail],
    #                      id='incomprehensible_behavior'),
    #         pytest.param(randomizer_choice('username'), randomizer_choice('email'), randomizer_choice('first_name'),
    #                      randomizer_choice('last_name'), randomizer_choice('password'), 201,
    #                      marks=pytest.mark.success_request),
    #     ]
    # )
    # def test_registration_confirm_data_validation(self, username, email, first_name, last_name,
    #                                         password, status_code, api_client):
    #     url = reverse('registration_confirm')
    #     validated_data = {
    #         'username': username,
    #         'email': email,
    #         'first_name': first_name,
    #         'last_name': last_name,
    #         'password': password
    #     }
    #     response = api_client.post(url, data=validated_data)
    #     assert response.status_code == status_code
    #     assert isinstance(response, User)
    #     assert response.username == validated_data['username']
    #     assert response.first_name == validated_data['first_name']
    #     assert response.last_name == validated_data['last_name']
    #     assert response.email == validated_data['email']

    # @pytest.mark.django_db
    # def test_registration_confirm_data_validation(self, status_code, api_client):
    #     url = reverse('registration')
    #     validated_data = {'email': randomizer_choice('email'), 'status_code': 201}
    #     response = api_client.post(url, data=validated_data)
    #
    #     assert isinstance(response, RegistrationTry)
    #     assert isinstance(response.code, uuid.uuid4)
    #     assert response.status_code == validated_data['status_code']
    #     assert response.id is not None  # Did you mean this? # TODO: get reg_try from DB bu id
    #     assert response.creation_time is not None
    #     assert response.confirmation_time is not None

    # @pytest.mark.django_db
    # def test_view(client):
    #    url = reverse('post')
    #    response = client.get(url)
    #    assert response.status_code == 200



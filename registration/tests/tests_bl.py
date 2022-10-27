import pytest
import uuid

from django.contrib.auth.models import User
from django.urls import reverse, NoReverseMatch

from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError

from registration.business_logic import final_creation
from registration.models import RegistrationTry
from registration.serializers import CreateRegisterTrySerializer, RegisterConfirmSerializer, UserSerializer


#todo: how to use Factory? And what it is?

class TestValidatePassword:

    def test_passwords_equal(self, random_upp2_data):
        attrs = {
            'password': random_upp2_data,
            'password2': random_upp2_data,
        }

        result = RegisterConfirmSerializer.validate(None, attrs)  # todo it wants self so I give None
        assert result['password'] == result['password2']

    def test_passwords_different(self, random_upp2_data, random_name):
        attrs = {
            'password': random_upp2_data,
            'password2': random_name,
        }

        with pytest.raises(ValidationError) as exc:
            RegisterConfirmSerializer.validate(None, attrs)
        assert "Password fields didn't match." in str(exc.value)
        assert exc.type == ValidationError


class TestBusinessLogic:

    @pytest.mark.django_db
    def test_final_creation(self, random_user, random_email):
        validated_data = random_user
        reg_try = RegistrationTry.objects.create(email=random_email, )

        result = final_creation(validated_data, reg_try)

        assert isinstance(result, User)
        assert result.username == validated_data['username']
        assert result.first_name == validated_data['first_name']
        assert result.last_name == validated_data['last_name']
        assert result.email == reg_try.email
        for_check_reg_try = RegistrationTry.objects.filter(id=reg_try.id).first()
        assert for_check_reg_try.confirmation_time is not None


class TestApiClientView:

    @pytest.mark.django_db
    def test_registration_valid_data(self, reg_try):
        response = reg_try
        assert response.status_code == status.HTTP_201_CREATED
        response_json = response.json()
        assert response_json  # todo - What we check by this command?
        assert set(response_json.keys()) == set(CreateRegisterTrySerializer.Meta.fields)
        assert response_json['email'] == reg_try.data['email']

    @pytest.mark.django_db
    def test_registration_null_data(self, api_client):
        url = reverse('registration')
        data = {
            'email': None,
        }
        response = api_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_json = response.json()
        assert response_json  # todo - What we check by this command?

    @pytest.mark.django_db
    def test_full_registration_valid_data(self, api_client, reg_try, random_user):
        data_reg_try = RegistrationTry.objects.get(email=reg_try.data['email'])
        code = data_reg_try.code
        url = reverse('registration_confirm', args=[code])
        random_user.update({'password2': random_user['password']})
        response = api_client.post(url, data=random_user, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        response_json = response.json()
        assert response_json  # todo - What we check by this command?
        assert set(response_json.keys()) == set(UserSerializer.Meta.fields)
        assert response_json['username'] == random_user['username']
        assert response_json['email'] == reg_try.data['email']
        assert response_json['blogs'] == []
        for_check_reg_try = RegistrationTry.objects.get(id=data_reg_try.id)
        assert for_check_reg_try.confirmation_time is not None
        for_check_user = User.objects.get(username=random_user['username'])
        assert for_check_user.first_name == random_user['first_name']
        assert for_check_user.last_name == random_user['last_name']

    @pytest.mark.django_db
    def test_full_registration_reg_done_code(self, api_client, random_user, reg_done_code):
        url = reverse('registration_confirm', args=[reg_done_code])
        random_user.update({'password2': random_user['password']})
        response = api_client.post(url, data=random_user, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_json = response.json()
        assert response_json  # todo - What we check by this command?
        assert response_json['detail'] == 'Not found.'

    @pytest.mark.django_db
    def test_full_registration_invalid_code(self,
                                            random_upp2_data):  # todo: тут перевірка на рівні - django.urls - тому не бачу необхідності в перевірці.
        with pytest.raises(NoReverseMatch) as exc:
            reverse('registration_confirm', args=[random_upp2_data])
        assert exc.type == NoReverseMatch

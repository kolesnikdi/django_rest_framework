import pytest

from registration.business_logic import final_creation

from registration.models import RegistrationTry


# TODO: randomizer.number_int()


class TestBLFunctional:

    @pytest.mark.django_db
    def test_final_creation(self):
        # Todo: make new data each time
        validated_data = {
            'username': 'asdfghj',
            'first_name': 'asdfghj',
            'last_name': 'asdfghj',
            'password': 'asdfghj',
        }

        reg_try = RegistrationTry.objects.create(
            email='sdfghj@ghjkl.ghj',  # Todo: make new email each time
        )

        result = final_creation(validated_data, reg_try)

        # TODO: check result is instance User

        # TODO: result.username == validated_data['username']
        # TODO: result.first_name == validated_data['first_name']
        # TODO: result.last_name == validated_data['last_name']
        # TODO: result.email == reg_try.email

        # TODO: get reg_try from DB bu id
        # TODO: reg_try.confirmation_time is not None




# class TestExample:
#
#     @pytest.mark.parametrize('argument1', (1, 2, 3, 4, 5))
#     def test_blank(self, argument1):
#         print('-->' * argument1)
#         assert isinstance(argument1, int)

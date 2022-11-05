import pytest

from django.urls import reverse

from rest_framework import status, exceptions

from blog.serializers import SnippetSerializer


class TestSnippetViewSet:

    @pytest.mark.django_db
    def test_authenticated(self, api_client):
        url = reverse('rest_framework:login')
        data = {
            'username': 'DjangoBoy2',
            'password': '122122saassaass',
        }
        response = api_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_post_not_authenticated(self, api_client, randomizer):
        url = reverse('post-list')
        data = {
            'title': randomizer.random_name(),
            'text': randomizer.upp2_data(),
        }
        response = api_client.post(url, data=data, format='json')
        assert response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_post_valid_data(self, authenticated_client, randomizer):
        url = reverse('post-list')
        data = {
            'title': randomizer.random_name(),
            'text': randomizer.upp2_data(),
        }
        response = authenticated_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()
        assert set(response.json().keys()) == set(SnippetSerializer.Meta.fields)
        assert response.json()['title'] == data['title']
        assert response.json()['text'] == data['text']

    @pytest.mark.django_db
    def test_post_invalid_data(self, authenticated_client, randomizer):
        url = reverse('post-list')
        data = {
            'title': None,
            'text': None,
        }
        response = authenticated_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()
        assert response.json()['title'] == ['This field may not be null.']
        assert response.json()['text'] == ['This field may not be null.']

    @pytest.mark.django_db
    def test_post_valid_data_change(self, api_client, created_blog, randomizer):
        url = reverse('post-detail', kwargs={'pk': created_blog.id})
        data = {
            'title': randomizer.random_name(),
            'text': randomizer.upp2_data(),
        }
        response = api_client.put(url, data=data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()
        assert set(response.json().keys()) == set(SnippetSerializer.Meta.fields)
        assert response.json()['title'] != created_blog.title
        assert response.json()['text'] != created_blog.text

    @pytest.mark.django_db
    def test_post_valid_data_change_not_owner(self, authenticated_client, created_blog, randomizer):  # todo maybe pytest don`t see permisions?
        url = reverse('post-detail', kwargs={'pk': created_blog.id})
        data = {
            'title': randomizer.random_name(),
            'text': randomizer.upp2_data(),
        }
        response = authenticated_client.put(url, data=data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_post_valid_data_delete(self, authenticated_client, created_blog, randomizer):
        url = reverse('post-detail', kwargs={'pk': created_blog.id})
        response = authenticated_client.delete(url, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_post_valid_data_delete_not_owner(self, authenticated_client, created_blog_bu_user_second):  # todo maybe pytest don`t see permisions?
        url = reverse('post-detail', kwargs={'pk': created_blog_bu_user_second.id})
        response = authenticated_client.delete(url, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

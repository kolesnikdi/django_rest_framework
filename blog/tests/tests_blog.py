import pytest

from django.urls import reverse

from rest_framework import status

from blog.models import Comment
from blog.serializers import SnippetSerializer, CommentsSerializer


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
            'comments': Comment.objects.all(),  # modify or delete. According to line 8 'comments' blog. serializer
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
    def test_post_valid_data_change(self, authenticated_client, created_blog, randomizer):
        url = reverse('post-detail', kwargs={'pk': created_blog.id})
        data = {
            'title': randomizer.random_name(),
            'text': randomizer.upp2_data(),
            'comments': Comment.objects.all(),  # modify or delete. According to line 8 'comments' blog. serializer
        }
        response = authenticated_client.put(url, data=data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()
        assert set(response.json().keys()) == set(SnippetSerializer.Meta.fields)
        assert response.json()['title'] != created_blog.title
        assert response.json()['text'] != created_blog.text

    @pytest.mark.django_db
    def test_post_valid_data_change_not_owner(self, authenticated_client, created_blog_user_second, randomizer):  # todo maybe pytest don`t see permisions?
        url = reverse('post-detail', kwargs={'pk': created_blog_user_second.id})
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
    def test_post_valid_data_delete_not_owner(self, authenticated_client, created_blog_user_second):
        url = reverse('post-detail', kwargs={'pk': created_blog_user_second.id})
        response = authenticated_client.delete(url, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_comment_in_blog(self, authenticated_client, randomizer):

        url1 = reverse('post-list')
        data1 = {
            'title': randomizer.random_name(),
            'text': randomizer.upp2_data(),
            'comments': Comment.objects.all(),  # modify or delete. According to line 8 'comments' blog. serializer
        }
        response_blog = authenticated_client.post(url1, data=data1, format='json')

        url2 = reverse('comments', kwargs={'id': response_blog.json()['id']})
        data2 = {
            'text': randomizer.upp2_data(),
        }
        response_comment = authenticated_client.post(url2, data=data2, format='json')

        assert response_comment.status_code == status.HTTP_201_CREATED
        assert response_comment.json()
        assert response_blog.json()['author'] == response_comment.json()['author']
        comment_in_blog = Comment.objects.get(id=response_blog.json()['id'])
        assert comment_in_blog.text == data2['text']


class TestCommentsView:

    @pytest.mark.django_db
    def test_comment_authenticated(self, api_client, created_blog, randomizer):
        url = reverse('comments', kwargs={'id': created_blog.id})
        data = {
            'text': randomizer.upp2_data(),
        }
        response = api_client.post(url, data=data, format='json')
        assert response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_post_valid_data(self, authenticated_client, created_blog, randomizer):
        url = reverse('comments', kwargs={'id': created_blog.id})
        data = {
            'text': randomizer.upp2_data(),
        }
        response = authenticated_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()
        assert set(response.json().keys()) == set(CommentsSerializer.Meta.fields)
        assert response.json()['text'] == data['text']
        comment_in_blog = Comment.objects.get(id=created_blog.id)
        assert comment_in_blog.text == data['text']
        assert comment_in_blog.author == authenticated_client.user

    @pytest.mark.django_db
    def test_post_invalid_data(self, authenticated_client, created_blog, randomizer):
        url = reverse('comments', kwargs={'id': created_blog.id})
        data = {
            'text': None,
        }
        response = authenticated_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()
        assert response.json()['text'] == ['This field may not be null.']

    @pytest.mark.django_db
    def test_post_invalid_blog_id(self, authenticated_client, randomizer):      # todo Мабуть перевірити ніяк
        url = reverse('comments', kwargs={'id': randomizer.random_digits()})
        data = {
            'text': randomizer.upp2_data(),
        }
        response = authenticated_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()




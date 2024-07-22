import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Post,Comment

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.mark.django_db
def test_create_post(auth_client):
    url = reverse('post-list-create')  
    data = {'title': 'Test Post', 'content': 'This is a test post.', 'author' : 1}
    response = auth_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED  


@pytest.mark.django_db
def test_read_post(auth_client, user):
    post = Post.objects.create(title='Read Post', content='Read post content.', author=user)
    url = reverse('post-detail', kwargs={'pk': post.id})  
    response = auth_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK 


@pytest.mark.django_db
def test_update_post(auth_client, user):
    post = Post.objects.create(title='Old Title', content='Old content.', author=user)
    url = reverse('post-detail', kwargs={'pk': post.id})
    data = {'title': 'Updated Title', 'content': 'Updated content.' ,'author' : 1}
    response = auth_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_post(auth_client, user):
    post = Post.objects.create(title='Delete Post', content='Delete content.', author=user)
    url = reverse('post-detail', kwargs={'pk': post.id})
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_pagination(auth_client, user):
    for i in range(15):
        Post.objects.create(title=f'Post {i}', content='Content here', author=user)
    url = reverse('post-list-create')
    response = auth_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data
    assert len(response.data['results']) == 3  


@pytest.mark.django_db
def test_comment_create(auth_client, user):
    post = Post.objects.create(title='Old Title', content='Old content.', author=user)
    url = reverse('comment-list-create',kwargs={'post_id': post.id}) 
    data = {'text': 'Comment on Old Title', 'author': 1}
    response = auth_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED





@pytest.mark.django_db
def test_read_comments(auth_client, user):
    post = Post.objects.create(title='Post', content='post content.', author=user)
    url = reverse('comment-list-create',kwargs={'post_id': post.id}) 
    data = {'text': 'Comment on Post', 'author': 1}
    response = auth_client.get(url, format='json') 

    url = reverse('post-detail', kwargs={'pk': post.id})  
    response = auth_client.get(url, format='json')
    print(response.json)
    assert response.status_code == status.HTTP_200_OK  
    
  




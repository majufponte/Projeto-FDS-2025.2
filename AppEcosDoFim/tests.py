#AppEcosDoFim/tests.py

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from .models import DetecaoAudio, locais_explorado, Jogador, Itens

@pytest.fixture 
def create_user(db):
    user = User.objects.create_user(
        username='testuser',
        password='testpassword' 
    )
    return user

@pytest.mark_django_db
def test_user_success(client):
    url= reverse('register')
    response = client.post(url, {
        "username" : "newuser",
        "password1" : "newpassword"   
    })

    assert User.objects.filter(username="newuser").exists()
    assert response.status_code == 302 
    assert response.url == '/login/'

@pytest.mark.django_db
def test_register_user_fails_if_exist(client, test_user):
    url=reverse('register')
    user_count_before = User.objects.count()
    response=client.post(url,{
        "username": "testuser",
        "password1": "anotherpassword"
    })

    assert User.objects.count() == user_count_before
    assert response.status_code == 200
    assert response.template_name == 'registration/register.html'

@pytest.mark.django_db
def test_login_user_success(client, test_user):
    url= reverse('submit_login')
    response = client.post(url, {
        "username" : "testuser",
        "password" : "testpassword"   
    })

    assert response.status_code == 302 
    assert response.url == '/'
    assert  '_aut_user_id' in client.session
    assert client.session['_auth_user_id'] == str(test_user.id)

@pytest.mark.django_db
def test_login_fail_wrong_password(client, test_user):
    url= reverse('submit_login')
    response = client.post(url, {
        "username" : "testuser",
        "password" : "wrongpassword"   
    }, follow=True)

    assert 'auth_user_id' not in client.session
    assert response.redirect_chain[0][0] == '/login'
    assert response.redirect_chain[0][1] == 302
    assert b"Usuario ou senha incorretos." in response.content
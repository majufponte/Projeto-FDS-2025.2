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

@pytest.mark.django_db
def test_logout(client, test_user):
    client.login(username='testuser', password='testpassword')
    assert 'auth_user_id' in client.session
    url= reverse('logout')
    response = client.get(url)

    assert 'auth_user_id' not in client.session
    assert response.status_code == 302
    assert response.url == '/'


def test_escolher_dificuldade_sets_session(client):
    url = reverse('escolher_dificuldade')
    client.post(url, {'dificuldade': '3'})
    assert "limiar_dificuldade" in client.session
    assert client.session["limiar_dificuldade"] == -35

@pytest.mark.django_db
def test_testar_dificuldade_get_view(client):
    url = reverse('escolher_dificuldade')
    session= client.session 
    session ['limiar_dificuldade'] = -40
    session.save()
    url= reverse('testar_dificuldade')                       
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['limiar'] == -40

@pytest.mark.django_db
def test_testar_dificuldade_post_authenticated(client, test_user):
    client.login(username='testuser', password='testpassword')
    url=reverse ('testar_dificuldade')
    client.post(url, {"audio detectado": "1"})
    
    assert DetecaoAudio.objects.count() == 1
    detecao = DetecaoAudio.objects.first()
    assert detecao.usuario == test_user
    assert detecao.audio_detectado is True

@pytest.mark.django_db
def test_testar_dificuldade_post_anonymous(client):
    url=reverse ('testar_dificuldade')
    client.post(url, {"audio detectado": "0"})
    
    assert DetecaoAudio.objects.count() == 1
    detecao = DetecaoAudio.objects.first()
    assert detecao.usuario is None
    assert detecao.detectado is False

@pytest.mark.django_db
def test_mapa_post_saves_location(client, test_user):
    client.login(username='testuser', password='testpassword')
    url=reverse('mapa')
    
    assert locais_explorado.objects.count() == 0
    client.post( url, {"id_do_local": "10"})

    assert locais_explorado.objects.count() == 1
    explorado = locais_explorado.objects.first()
    assert explorado.usuario == test_user
    assert explorado.id_do_local == 10  

@pytest.mark.django_db
def test_mapa_get_loads_explored_locations(client, test_user):
    client.login(username='testuser', password='testpassword')
    url=reverse('mapa') 

    locais_explorado.objects.create(usuario=test_user, id_do_local=5)
    locais_explorado.objects.create(usuario=test_user, id_do_local=8)
    response = client.get(url)

    assert response.status_code == 200
    assert "explorados" in response.context
    explorados_list = response.context["explorados"]
    assert 5 in explorados_list
    assert 8 in explorados_list     
    assert 10 not in explorados_list




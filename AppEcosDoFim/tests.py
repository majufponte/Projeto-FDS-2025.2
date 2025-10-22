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


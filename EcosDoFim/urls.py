"""
URL configuration for EcosDoFim project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppEcosDoFim import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('EcosDofim/dificuldade', views.escolher_dificuldade, name='escolher_dificuldade'),
    path('EcosDofim/audio', views.testar_dificuldade, name='testar_dificuldade'),
    path("audio-detectado/", views.testar_dificuldade, name="audio_detectado"),
    path("mapa/", views.mapa,name='mapa'),
    path("",views.home,name="pagina_inicial"),
    path('login/', views.login_user, name='login_user'),
    path('login/submit/', views.submit_login, name='submit_login'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/',views.register_user,name='register_user')
]

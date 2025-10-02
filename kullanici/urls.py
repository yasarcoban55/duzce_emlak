from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('kayit/', views.kayit_ol, name='kayit_ol'),
    path('giris/', auth_views.LoginView.as_view(template_name='kullanici/giris.html'), name='giris'),
    path('cikis/', auth_views.LogoutView.as_view(template_name='kullanici/cikis.html'), name='cikis'),
    path('profil/', views.profil, name='profil'),
]
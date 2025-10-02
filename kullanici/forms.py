from django import forms
from django.contrib.auth.models import User
from .models import Profil

class KullaniciGuncellemeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfilGuncellemeForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['telefon', 'profil_resmi', 'aciklama', 'ilce']
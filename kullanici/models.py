from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    kullanici = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=15, blank=True)
    profil_resmi = models.ImageField(upload_to='profil_resimleri/', blank=True)
    aciklama = models.TextField(blank=True)
    ilce = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.kullanici.username
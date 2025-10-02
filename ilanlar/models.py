from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

class il(models.Model):
    ad=models.CharField(max_length=50)
    def __str__(self):
        return self.ad

class ilce(models.Model):
    il=models.ForeignKey(il,on_delete=models.CASCADE)
    ad=models.CharField(max_length=50)
    def __str__(self):
        return self.ad
    
class semt(models.Model):
    il= models.ForeignKey(il,on_delete=models.CASCADE)
    ilce=models.ForeignKey(ilce,on_delete=models.CASCADE)
    ad=models.CharField(max_length=50)
    def __str__(self):
        return self.ad



class Ilan(models.Model):
    EMLAK_TIPLERI = [
        ('satilik', 'Satılık'),
        ('kiralik', 'Kiralık'),
        ('gunluk_kiralik', 'Günlük Kiralık'),
    ]
    
    KATEGORILER = [
        ('daire', 'Daire'),
        ('villa', 'Villa'),
        ('mustakil', 'Müstakil Ev'),
        ('residence', 'Residence'),
        ('arsa', 'Arsa'),
        ('isyeri', 'İş Yeri'),
        ('depo', 'Depo'),
    ]
    
    baslik = models.CharField(max_length=200)
    aciklama = models.TextField()
    fiyat = models.DecimalField(max_digits=15, decimal_places=2)
    emlak_tipi = models.CharField(max_length=20, choices=EMLAK_TIPLERI)
    kategori = models.CharField(max_length=20, choices=KATEGORILER)
    metrekare = models.IntegerField()
    oda_sayisi = models.CharField(max_length=20)
    bina_yasi = models.IntegerField(null=True, blank=True)
    kat = models.IntegerField(null=True, blank=True)
    isitma = models.CharField(max_length=50, null=True, blank=True)
    esya_durumu = models.BooleanField(default=False)
    aidat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    il = models.ForeignKey(il, on_delete=models.SET_NULL, null=True, related_name='ilanlar_il')
    ilce = models.ForeignKey(ilce, on_delete=models.SET_NULL, null=True, related_name='ilanlar_ilce')
    mahalle=models.ForeignKey(semt,on_delete=models.SET_NULL,null=True,related_name='ilanlar_mahalle')
    adres = models.TextField()
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)
    guncellenme_tarihi = models.DateTimeField(auto_now=True)
    aktif = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, max_length=250)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_ilans')
    
    def save(self, *args, **kwargs):
        if not self.slug and self.baslik:
            self.slug = slugify(self.baslik, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('ilan_detay', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.baslik

    def publish(self, user=None):
        self.is_published = True
        self.published_at = timezone.now()
        if user:
            self.approved_by = user
        self.save()

class IlanResim(models.Model):
    ilan = models.ForeignKey(Ilan, related_name='resimler', on_delete=models.CASCADE)
    resim = models.ImageField(upload_to='ilan_resimleri/')
    sira = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['sira']

class IlanFavori(models.Model):
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    ilan = models.ForeignKey(Ilan, on_delete=models.CASCADE)
    eklenme_tarihi = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['kullanici', 'ilan']
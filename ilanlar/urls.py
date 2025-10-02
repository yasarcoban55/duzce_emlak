from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('ara/', views.ilan_ara, name='ilan_ara'),
    path('ilan/olustur/', views.ilan_olustur, name='ilan_olustur'),
    path('ilanlar/', views.ilan_list, name='ilan_list'),

    path('favori-ekle/<int:ilan_id>/', views.favori_ekle, name='favori_ekle'),
    path('favoriler/', views.favori_listesi, name='favori_listesi'),

    # AJAX yollarını admin/ ile başlamayacak şekilde bırak
    path('ajax/ilce-listesi/', views.ilce_listesi, name='ilce_listesi'),
    path('ajax/mahalle-listesi/', views.mahalle_listesi, name='mahalle_listesi'),

    # admin ile karışmasın diye prefix değiştirildi
    path('ajax/admin/ilce-filter/', views.ilce_filter, name='ilce_filter'),
    path('ajax/admin/ilce-list/', views.admin_ilce_list, name='admin_ilce_list'),

    # detay (genel slug en sonda)
    path('ilan/<slug:slug>/', views.ilan_detay, name='ilan_detay'),
]
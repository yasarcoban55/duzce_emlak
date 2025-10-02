from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ilanlar import views as ilan_views

urlpatterns = [
    # ÖNCE özel AJAX route'u koy
    path('admin/ajax/ilce-list/', ilan_views.admin_ilce_list, name='admin_ilce_list'),

    # sonra admin panelini koy
    path('admin/', admin.site.urls),

    path('', include('ilanlar.urls')),
    path('kullanici/', include('kullanici.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
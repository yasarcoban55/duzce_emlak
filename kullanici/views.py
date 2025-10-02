from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import KullaniciGuncellemeForm, ProfilGuncellemeForm
from .models import Profil

def kayit_ol(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profil.objects.create(kullanici=user)
            login(request, user)
            messages.success(request, 'Hesabınız başarıyla oluşturuldu!')
            return redirect('anasayfa')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'kullanici/kayit_ol.html', context)

@login_required
def profil(request):
    if request.method == 'POST':
        k_form = KullaniciGuncellemeForm(request.POST, instance=request.user)
        p_form = ProfilGuncellemeForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profil
        )
        
        if k_form.is_valid() and p_form.is_valid():
            k_form.save()
            p_form.save()
            messages.success(request, 'Profiliniz güncellendi!')
            return redirect('profil')
    else:
        k_form = KullaniciGuncellemeForm(instance=request.user)
        p_form = ProfilGuncellemeForm(instance=request.user.profil)
    
    context = {
        'k_form': k_form,
        'p_form': p_form,
        'aktif_ilan_count': 0,
        'toplam_ilan_count': 0,
        'favori_count': 0,
    }
    return render(request, 'kullanici/profil.html', context)
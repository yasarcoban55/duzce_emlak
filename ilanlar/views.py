import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Ilan, IlanFavori, IlanResim, ilce, semt
from .forms import IlanForm, IlanResimForm

def anasayfa(request):
    ilanlar = Ilan.objects.filter(aktif=True).order_by('-olusturulma_tarihi')[:12]
    populer_ilanlar = Ilan.objects.filter(aktif=True).order_by('-olusturulma_tarihi')[:6]
    
    context = {
        'ilanlar': ilanlar,
        'populer_ilanlar': populer_ilanlar,
    }
    return render(request, 'ilanlar/anasayfa.html', context)

def ilan_ara(request):
    sorgu = request.GET.get('q', '')
    emlak_tipi = request.GET.get('emlak_tipi', '')
    kategori = request.GET.get('kategori', '')
    min_fiyat = request.GET.get('min_fiyat', '')
    max_fiyat = request.GET.get('max_fiyat', '')
    ilce = request.GET.get('ilce', '')
    
    ilanlar = Ilan.objects.filter(aktif=True)
    
    if sorgu:
        ilanlar = ilanlar.filter(
            Q(baslik__icontains=sorgu) |
            Q(aciklama__icontains=sorgu) |
            Q(mahalle__icontains=sorgu) |
            Q(adres__icontains=sorgu)
        )
    
    if emlak_tipi:
        ilanlar = ilanlar.filter(emlak_tipi=emlak_tipi)
    
    if kategori:
        ilanlar = ilanlar.filter(kategori=kategori)
    
    if min_fiyat:
        ilanlar = ilanlar.filter(fiyat__gte=min_fiyat)
    
    if max_fiyat:
        ilanlar = ilanlar.filter(fiyat__lte=max_fiyat)
    
    if ilce:
        ilanlar = ilanlar.filter(ilce__icontains=ilce)
    
    context = {
        'ilanlar': ilanlar,
        'sorgu': sorgu,
        'filtreler': {
            'emlak_tipi': emlak_tipi,
            'kategori': kategori,
            'min_fiyat': min_fiyat,
            'max_fiyat': max_fiyat,
            'ilce': ilce,
        }
    }
    return render(request, 'ilanlar/ilan_ara.html', context)

def ilan_list(request):
    ilans = Ilan.objects.filter(is_published=True).order_by('-published_at')
    context = {
        'ilans': ilans,
    }
    return render(request, 'ilanlar/ilan_listesi.html', context)

def ilan_detay(request, slug):
    ilan = get_object_or_404(Ilan, slug=slug)  # veya slug=slug, is_published=True
    return render(request, 'ilanlar/ilan_detay.html', {'ilan': ilan})

@login_required
def ilan_olustur(request):
    if request.method == 'POST':
        form = IlanForm(request.POST, request.FILES)
        if form.is_valid():
            ilan = form.save(commit=False)
            ilan.user = request.user
            ilan.is_published = False   # önemli: admin onayı bekleyecek
            ilan.save()
            form.save_m2m()
            # yönlendir/göster mesaj
            return redirect('ilan_tesekkur') 
    else:
        form = IlanForm()
    return render(request, 'ilanlar/ilan_olustur.html', {'form': form})

@login_required
def favori_ekle(request, ilan_id):
    ilan = get_object_or_404(Ilan, id=ilan_id)
    favori, created = IlanFavori.objects.get_or_create(
        kullanici=request.user,
        ilan=ilan
    )
    
    if created:
        messages.success(request, 'İlan favorilere eklendi!')
    else:
        favori.delete()
        messages.info(request, 'İlan favorilerden çıkarıldı!')
    
    return redirect('ilan_detay', slug=ilan.slug)

@login_required
def favori_listesi(request):
    favori_ilanlar = IlanFavori.objects.filter(kullanici=request.user)
    context = {'favori_ilanlar': favori_ilanlar}
    return render(request, 'ilanlar/favori_listesi.html', context)

def ilce_listesi(request):
    il_id = request.GET.get('il')
    ilceler = ilce.objects.filter(il_id=il_id).order_by('ad')
    ilce_list = [{'id': i.id, 'ad': i.ad} for i in ilceler]
    return JsonResponse({'ilceler': ilce_list})

def mahalle_listesi(request):
    ilce_id = request.GET.get('ilce')
    mahalleler = semt.objects.filter(ilce_id=ilce_id).order_by('ad')
    data = [{'id': m.id, 'ad': m.ad} for m in mahalleler]
    return JsonResponse({'mahalleler': data})

def ilce_filter(request):
    il_id = request.GET.get('il_id')
    ilceler = ilce.objects.filter(il_id=il_id).order_by('ad')
    data = [{'id': i.id, 'ad': i.ad} for i in ilceler]
    return JsonResponse({'ilceler': data})

def admin_ilce_list(request):
    il_id = request.GET.get('il_id')
    if not il_id:
        return JsonResponse({'ilceler': []})
    ilceler = ilce.objects.filter(il_id=il_id).order_by('ad')
    data = [{'id': i.id, 'ad': i.ad} for i in ilceler]
    return JsonResponse({'ilceler': data})
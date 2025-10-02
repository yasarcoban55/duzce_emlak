from django import forms
from .models import Ilan, IlanResim, il, ilce, semt

class IlanForm(forms.ModelForm):
    il = forms.ModelChoiceField(queryset=il.objects.all(), required=True, label="İl")
    ilce = forms.ModelChoiceField(queryset=ilce.objects.none(), required=True, label="İlçe")
    mahalle = forms.ModelChoiceField(queryset=semt.objects.none(), required=True, label="Mahalle")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'il' in self.data:
            try:
                il_id = int(self.data.get('il'))
                self.fields['ilce'].queryset = ilce.objects.filter(il_id=il_id).order_by('ad')
            except (ValueError, TypeError):
                self.fields['ilce'].queryset = ilce.objects.none()
        elif self.instance.pk and self.instance.il:
            self.fields['ilce'].queryset = ilce.objects.filter(il=self.instance.il).order_by('ad')
        else:
            self.fields['ilce'].queryset = ilce.objects.none()

        if 'ilce' in self.data:
            try:
                ilce_id = int(self.data.get('ilce'))
                self.fields['mahalle'].queryset = semt.objects.filter(ilce_id=ilce_id).order_by('ad')
            except (ValueError, TypeError):
                self.fields['mahalle'].queryset = semt.objects.none()
        elif self.instance.pk and self.instance.ilce:
            self.fields['mahalle'].queryset = semt.objects.filter(ilce=self.instance.ilce).order_by('ad')
        else:
            self.fields['mahalle'].queryset = semt.objects.none()

    class Meta:
        model = Ilan
        fields = ['baslik', 'fiyat', 'emlak_tipi', 'kategori', 'metrekare', 'oda_sayisi', 'bina_yasi', 'kat', 'isitma', 'aidat', 'esya_durumu', 'il', 'ilce', 'mahalle', 'adres', 'aciklama']
        widgets = {
            'baslik': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'İlan Başlığı'}),
            'fiyat': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Fiyat'}),
            'emlak_tipi': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Emlak Tipi'}),
            'kategori': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Kategori'}),
            'metrekare': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Metrekare'}),
            'oda_sayisi': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Oda Sayısı'}),
            'bina_yasi': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bina Yaşı'}),
            'kat': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bulunduğu Kat'}),
            'isitma': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Isıtma'}),
            'aidat': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Aidat'}),
            'esya_durumu': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'il': forms.Select(attrs={'class': 'form-select', 'placeholder': 'İl'}),
            'ilce': forms.Select(attrs={'class': 'form-select', 'placeholder': 'İlçe'}),
            'mahalle': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Mahalle'}),
            'adres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adres'}),
            'aciklama': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detaylı Açıklama', 'style': 'height: 120px;'}),
        }

class IlanResimForm(forms.ModelForm):
    class Meta:
        model = IlanResim
        fields = ['resim', 'sira']
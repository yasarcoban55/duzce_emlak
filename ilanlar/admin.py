from django.contrib import admin
from django import forms
from django.utils import timezone
from .models import Ilan, IlanResim, IlanFavori, il, ilce, semt


class SemtAdminForm(forms.ModelForm):
    class Meta:
        model = semt
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'il' in self.data:
            try:
                il_id = int(self.data.get('il'))
                self.fields['ilce'].queryset = ilce.objects.filter(il_id=il_id)
            except (ValueError, TypeError):
                self.fields['ilce'].queryset = ilce.objects.none()
        elif self.instance.pk and self.instance.il:
            self.fields['ilce'].queryset = ilce.objects.filter(il=self.instance.il)
        else:
            self.fields['ilce'].queryset = ilce.objects.none()


@admin.register(il)
class ilAdmin(admin.ModelAdmin):
    list_display = ['ad']
    search_fields = ['ad']


@admin.register(ilce)
class ilceAdmin(admin.ModelAdmin):
    list_display = ['ad', 'il']
    search_fields = ['ad', 'il__ad']
    list_filter = ['il']


@admin.register(semt)
class semtAdmin(admin.ModelAdmin):
    form = SemtAdminForm
    list_display = ['ad', 'il', 'ilce']
    search_fields = ['ad', 'il__ad', 'ilce__ad']
    list_filter = ['il', 'ilce']

    class Media:
        js = ('ilanlar/js/semt_ilce_filter.js',)


class IlanResimInline(admin.TabularInline):
    model = IlanResim
    extra = 1


@admin.register(Ilan)
class IlanAdmin(admin.ModelAdmin):
    list_display = ('baslik','is_published', 'published_at')
    list_filter = ('is_published',)
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        updated = 0
        for ilan in queryset:
            if not ilan.is_published:
                ilan.is_published = True
                ilan.published_at = timezone.now()
                ilan.approved_by = request.user
                ilan.save()
                updated += 1
        self.message_user(request, f"{updated} ilan yayınlandı.")
    approve_selected.short_description = "Seçilen ilanları yayınla (admin onayı)"

admin.site.register(IlanFavori)
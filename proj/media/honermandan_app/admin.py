from django.contrib import admin

from .models import honermendan


@admin.register(honermendan)
class HonermendanAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_track', 'has_audio')
    search_fields = ('name', 'name_track')

    @admin.display(boolean=True, description='آهنگ آپلود شده؟')
    def has_audio(self, obj):
        return bool(obj.audio)

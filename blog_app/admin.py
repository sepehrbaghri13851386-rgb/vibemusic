from django.contrib import admin
from .models import Blog, FeaturedContent, FeaturedTrack

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_published']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'description', 'image')
        }),
        ('اطلاعات تکمیلی', {
            'fields': ('author', 'is_published')
        }),
        ('زمان', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FeaturedContent)
class FeaturedContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'order', 'active', 'created_at')
    list_filter = ('active',)
    list_editable = ('order', 'active')
    ordering = ('order', '-created_at')
    search_fields = ('title', 'description')
    fieldsets = (
        ('اطلاعات اصلی', {'fields': ('title', 'description', 'image')}),
        ('لینک و تنظیمات', {'fields': ('link_url', 'link_text', 'order', 'active')}),
    )


@admin.register(FeaturedTrack)
class FeaturedTrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'track_name', 'track_artist', 'order', 'active')
    list_filter = ('active',)
    list_editable = ('order', 'active')
    ordering = ('order',)
    raw_id_fields = ('track',)

    def track_name(self, obj):
        return obj.track.name_track
    track_name.short_description = 'نام آهنگ'

    def track_artist(self, obj):
        return obj.track.name
    track_artist.short_description = 'هنرمند'
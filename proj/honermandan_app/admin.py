from django.contrib import admin
from .models import honermendan, ArtistLike, HotSuggestion, Comment

@admin.register(honermendan)
class honermendanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_track', 'genre', 'audio_status')
    list_filter = ('genre', 'name')
    search_fields = ('name', 'name_track')
    ordering = ('name', '-id')
    list_per_page = 20
    autocomplete_fields = ()
    fields = ('name', 'name_track', 'genre', 'image', 'audio')

    def audio_status(self, obj):
        """نمایش وضعیت فایل آهنگ"""
        if obj.audio:
            return "✅ دارای آهنگ"
        return "❌ بدون آهنگ"
    audio_status.short_description = "وضعیت آهنگ"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('name', '-id')


@admin.register(ArtistLike)
class ArtistLikeAdmin(admin.ModelAdmin):
    list_display = ('artist_name', 'user', 'created_at')
    list_filter = ('artist_name',)
    search_fields = ('artist_name', 'user__username')


@admin.register(HotSuggestion)
class HotSuggestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'track_name', 'track_artist', 'order', 'active', 'created_at')
    list_filter = ('active',)
    search_fields = ('track__name', 'track__name_track')
    list_editable = ('order', 'active')
    ordering = ('order', '-created_at')
    list_per_page = 20
    raw_id_fields = ('track',)

    def track_name(self, obj):
        return obj.track.name_track
    track_name.short_description = 'نام آهنگ'

    def track_artist(self, obj):
        return obj.track.name
    track_artist.short_description = 'هنرمند'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'track_name', 'text_short', 'parent', 'is_reply', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username', 'track__name_track')
    raw_id_fields = ('track', 'user', 'parent')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 30

    def user_name(self, obj):
        return obj.user.username
    user_name.short_description = 'کاربر'

    def track_name(self, obj):
        return obj.track.name_track
    track_name.short_description = 'آهنگ'

    def text_short(self, obj):
        return obj.text[:80] + '...' if len(obj.text) > 80 else obj.text
    text_short.short_description = 'متن'
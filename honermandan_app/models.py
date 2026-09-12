import os
from django.db import models
from django.conf import settings
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from genres_app.models import Genre
from loginsogin_app.models import CustomUser

class honermendan(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    name_track = models.TextField(max_length=400)
    audio = models.FileField(
        upload_to='tracks/',
        blank=True,
        null=True,
        storage=RawMediaCloudinaryStorage(),
        verbose_name='فایل آهنگ',
        help_text='حتماً فایل mp3 را اینجا آپلود کن. فقط اسم و عکس برای پخش کافی نیست.'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tracks',
        verbose_name='سبک موسیقی',
        help_text='سبک این آهنگ را انتخاب کن (مثلاً ترپ، پاپ، قدیمی...)'
    )

    @property
    def has_image(self):
        """Check if an image file is attached (works with cloud storage too)."""
        return bool(self.image)

    @property
    def has_audio(self):
        """Check if an audio file is attached (works with cloud storage too)."""
        return bool(self.audio)

    def __str__(self):
        return f"{self.name} - {self.name_track}"


class ArtistLike(models.Model):
    """
    لایک هنرمند. چون مدل مستقلی برای «هنرمند» وجود نداره (هنرمندها فقط
    اسم‌های تکراری تو مدل آهنگ هستن)، لایک بر اساس نام هنرمند ذخیره میشه.
    هر کاربر فقط یک بار میتونه یک هنرمند رو لایک کنه.
    """
    artist_name = models.CharField(max_length=30, db_index=True)
    user = models.ForeignKey(
        'loginsogin_app.CustomUser',
        on_delete=models.CASCADE,
        related_name='artist_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('artist_name', 'user')
        verbose_name = 'لایک هنرمند'
        verbose_name_plural = 'لایک‌های هنرمندان'

    def __str__(self):
        return f"{self.user} ❤ {self.artist_name}"


class HotSuggestion(models.Model):
    """
    پیشنهادات داغ - آهنگ‌هایی که ادمین اضافه می‌کنه
    """
    track = models.ForeignKey(
        honermendan,
        on_delete=models.CASCADE,
        related_name='hot_suggestions',
        verbose_name='آهنگ'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'پیشنهاد داغ'
        verbose_name_plural = 'پیشنهادات داغ'

    def __str__(self):
        return f"🔥 {self.track.name_track} - {self.track.name}"


class Comment(models.Model):
    """
    کامنت روی آهنگ‌ها - کاربران عادی کامنت میذارن، ادمین جواب میده
    """
    track = models.ForeignKey(
        honermendan,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='آهنگ'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='کاربر'
    )
    text = models.TextField(verbose_name='متن کامنت')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='کامنت والد'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت‌ها'

    def __str__(self):
        return f"{self.user.username}: {self.text[:50]}"

    @property
    def is_reply(self):
        return self.parent is not None

    @property
    def is_admin_reply(self):
        return self.user.is_admin
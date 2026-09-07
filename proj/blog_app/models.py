from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from honermandan_app.models import honermendan

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='blog_images/', verbose_name="تصویر", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', verbose_name="نویسنده", null=True, blank=True)
    is_published = models.BooleanField(default=True, verbose_name="منتشر شده")
    
    class Meta:
        verbose_name = "پست بلاگ"
        verbose_name_plural = "پست‌های بلاگ"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'pk': self.pk})


class FeaturedContent(models.Model):
    """
    محتوای ویژه وبلاگ - بخش کناری وبلاگ که از ادمین مدیریت میشه
    """
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    image = models.ImageField(upload_to='featured/', verbose_name='تصویر', null=True, blank=True)
    link_url = models.URLField(blank=True, verbose_name='لینک خارجی')
    link_text = models.CharField(max_length=200, blank=True, verbose_name='متن لینک')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'محتوای ویژه'
        verbose_name_plural = 'محتواهای ویژه'

    def __str__(self):
        return self.title


class FeaturedTrack(models.Model):
    """
    آهنگ‌های برتر وبلاگ - لیست آهنگ‌هایی که در وبلاگ نمایش داده میشه
    """
    track = models.ForeignKey(
        honermendan,
        on_delete=models.CASCADE,
        related_name='featured_tracks',
        verbose_name='آهنگ'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')
    active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        ordering = ['order']
        verbose_name = 'آهنگ برتر وبلاگ'
        verbose_name_plural = 'آهنگ‌های برتر وبلاگ'

    def __str__(self):
        return f'{self.track.name_track} - {self.track.name}'
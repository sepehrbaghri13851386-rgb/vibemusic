from django.db import models

class honermendan(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images')
    name_track = models.TextField(max_length=400)
    audio = models.FileField(
        upload_to='tracks/',
        blank=True,
        null=True,
        verbose_name='فایل آهنگ',
        help_text='فایل mp3 آهنگ رو اینجا آپلود کن'
    )

    def __str__(self):
        return self.name
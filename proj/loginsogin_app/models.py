from django.db import models


class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # هش‌شده ذخیره می‌شود، هرگز متن خام نیست
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False, verbose_name='ادمین اصلی')

    reset_token = models.CharField(max_length=64, blank=True, null=True, unique=True)
    reset_token_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.username

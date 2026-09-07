from django.db import migrations
from django.utils.text import slugify


GENRES = [
    ('ترپ', 'سبک تیره و بیس‌سنگین، ریشه گرفته از هیپ‌هاپ جنوب آمریکا'),
    ('پاپ', 'ملودی‌های ساده و گیرا، پرطرفدارترین سبک روز'),
    ('قدیمی', 'آهنگ‌های کلاسیک و نوستالژیک'),
    ('هیپ‌هاپ', 'ریتم و ریپ، فرهنگ خیابانی'),
    ('راک', 'گیتار الکتریک و انرژی بالا'),
    ('الکترونیک', 'موسیقی ساخته‌شده با سینت و بیت الکترونیک'),
]


def seed_genres(apps, schema_editor):
    Genre = apps.get_model('genres_app', 'Genre')
    for name, description in GENRES:
        Genre.objects.get_or_create(
            name=name,
            defaults={
                'slug': slugify(name, allow_unicode=True),
                'description': description,
            }
        )


def remove_genres(apps, schema_editor):
    Genre = apps.get_model('genres_app', 'Genre')
    Genre.objects.filter(name__in=[n for n, _ in GENRES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('genres_app', '0002_alter_genre_options_delete_track'),
    ]

    operations = [
        migrations.RunPython(seed_genres, remove_genres),
    ]

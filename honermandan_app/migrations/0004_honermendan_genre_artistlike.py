import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genres_app', '0002_alter_genre_options_delete_track'),
        ('honermandan_app', '0003_alter_honermendan_audio'),
        ('loginsogin_app', '0002_customuser_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='honermendan',
            name='genre',
            field=models.ForeignKey(blank=True, help_text='سبک این آهنگ را انتخاب کن (مثلاً ترپ، پاپ، قدیمی...)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tracks', to='genres_app.genre', verbose_name='سبک موسیقی'),
        ),
        migrations.CreateModel(
            name='ArtistLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(db_index=True, max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artist_likes', to='loginsogin_app.customuser')),
            ],
            options={
                'verbose_name': 'لایک هنرمند',
                'verbose_name_plural': 'لایک\u200cهای هنرمندان',
                'unique_together': {('artist_name', 'user')},
            },
        ),
    ]
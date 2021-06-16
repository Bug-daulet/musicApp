# Generated by Django 3.0.6 on 2020-07-11 04:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('musicApp', '0002_playlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_fav', models.BooleanField(default=False)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicApp.Song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

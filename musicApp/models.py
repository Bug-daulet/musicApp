from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Song(models.Model):

    Genre_Choice = (
            ('Pop', 'Pop'),
            ('Rock', 'Rock'),
          )

    Category_Choice = (
        ('Nocategory', 'Nocategory'),
        ('Kazakh songs', 'Kazakh'),
        ('Russian pop', 'Russian_pop'),
        ('Kpop', 'Kpop')
    )

    name = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    genre = models.CharField(max_length=20, choices=Genre_Choice, default='Pop')
    category = models.CharField(max_length=20, choices=Category_Choice, default='Nocategory')
    song_img = models.FileField()
    year = models.IntegerField()
    singer = models.CharField(max_length=200)
    song_file = models.FileField()

    def __str__(self):
        return self.name


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=200)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class Recent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
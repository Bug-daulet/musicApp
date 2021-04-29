from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Song(models.Model):

    genre_type = (
        ('pop', 'pop'),
        ('rock', 'rock'),
    )

    name = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    song_img = models.FileField()
    genre = models.CharField(max_length=20,choices=genre_type,default='pop')
    singer = models.CharField(max_length=200)
    song_file = models.FileField()

    def __str__(self):
        return self.name


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=200)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


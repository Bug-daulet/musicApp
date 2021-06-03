from django.db import models


class Album(models.Model):
    artist = models.CharField(max_length=100)
    album_title = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    released_year = models.IntegerField()

    def __str__(self):
        return self.album_title + '-' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=100, default='')
    genre = models.CharField(max_length=50)
    is_favorite = models.BooleanField(default=False)

    def Song(self):
        return self.song_title

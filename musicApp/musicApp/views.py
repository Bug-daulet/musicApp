from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):

    songs_all = list(Song.objects.all().values('id').order_by('?'))
    sliced_ids = [each['id'] for each in songs_all][:5]
    indexpage_songs = Song.objects.filter(id__in=sliced_ids)

    songs_pop = list(Song.objects.filter(genre__exact="pop").values('id'))
    sliced_ids = [each['id'] for each in songs_pop][:5]
    indexpage_pop_songs = Song.objects.filter(id__in=sliced_ids)


    songs_english = list(Song.objects.filter(genre__exact="rock").values('id'))
    sliced_ids = [each['id'] for each in songs_english][:5]
    indexpage_rock_songs = Song.objects.filter(id__in=sliced_ids)

    context = {
        'all_songs':indexpage_songs,
        'pop':indexpage_pop_songs,
        'rock':indexpage_rock_songs,
    }
    return render(request, 'musicapp/index.html', context=context)


def pop_music(request):

    pop_music = Song.objects.filter(genre__exact="pop")
    context = {'music': pop_music}
    return render(request, 'musicapp/pop.html', context=context)


def rock_music(request):

    rock_music = Song.objects.filter(genre__exact="rock")
    context = {'music': rock_music}
    return render(request, 'musicapp/rock.html', context=context)


def all_songs(request):
    songs = Song.objects.all()
    context = {'music': songs}
    return render(request, 'musicapp/all_songs.html', context)

@login_required(login_url='login')
def detail(request, song_id):
    songs = Song.objects.filter(id=song_id).first()

    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
    is_favourite = Favourite.objects.filter(user=request.user).filter(song=song_id).values('is_fav')

    if request.method == "POST":
        if 'playlist' in request.POST:
            playlist_name = request.POST["playlist"]
            q = Playlist(user=request.user, song=songs, playlist_name=playlist_name)
            q.save()
            messages.success(request, "Song added to playlist!")
        elif 'add-fav' in request.POST:
            is_fav = True
            query = Favourite(user=request.user, song=songs, is_fav=is_fav)
            query.save()
            messages.success(request, "Added to favorite!")
            return redirect('detail', song_id=song_id)
        elif 'rm-fav' in request.POST:
            is_fav = True
            query = Favourite.objects.filter(user=request.user, song=songs, is_fav=is_fav)
            query.delete()
            messages.success(request, "Removed from favorite!")
            return redirect('detail', song_id=song_id)

    context = {'songs': songs, 'playlists': playlists, 'is_favourite': is_favourite}
    return render(request, 'musicapp/detail.html', context=context)


def my_music(request):
    return render(request, 'musicapp/mymusic.html')


def playlist(request):
    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
    context = {'playlists': playlists}
    return render(request, 'musicapp/playlist.html', context=context)


def playlist_songs(request, playlist_name):
    songs = Song.objects.filter(playlist__playlist_name=playlist_name, playlist__user=request.user).distinct()

    if 'delete' in request.POST:
        playlist_remove = Playlist.objects.filter(user=request.user, playlist_name=playlist_name)
        playlist_remove.delete()
        return redirect("playlist")

    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        playlist_song = Playlist.objects.filter(playlist_name=playlist_name, song__id=song_id, user=request.user)
        playlist_song.delete()
        messages.success(request, "Song removed from playlist!")

    context = {'playlist_name': playlist_name, 'songs': songs}

    return render(request, 'musicapp/playlist_songs.html', context=context)


def favourite(request):
    songs = Song.objects.filter(favourite__user=request.user, favourite__is_fav=True).distinct()

    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        favourite_song = Favourite.objects.filter(user=request.user, song__id=song_id, is_fav=True)
        favourite_song.delete()
        messages.success(request, "Removed from favourite!")
    context = {'songs': songs}
    return render(request, 'musicapp/favourite.html', context=context)


def search_by_music_info(request):
    if request.method == "POST" and len(request.POST.get("search_field"))>0:
        searching_text = request.POST.get("search_field")
        return redirect("index:search_success", text=searching_text)
    else:
        return render(request, "musicapp/search.html",
                    {"empty_res":"There is no song with such information"})


def search_success(request, text):
    if len(text)>0:
        search_res = Song.objects.filter(name__search=text, singer__search=text)
        return render(request, "musicapp/search.html",
                {"search_res":search_res,"empty_res":"There is no article"} )



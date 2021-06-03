from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import *
import random
import stripe

stripe.api_key = "sk_test_51Ivv6PLbueGO5tYB8iqFRw1jLpKTZphW9TyXgLOOgt14ROy6sHZ13kLPpQCZXCPlaBBkhgTV9HOZVm2vzgpgND8300Iq7t9Q9g"


# Create your views here.
def index(request):
    # Display recent songs
    if not request.user.is_anonymous:
        recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        recent_id = [each['song_id'] for each in recent][:5]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id, recent__user=request.user)
        recent_songs = list()
        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
    else:
        recent = None
        recent_songs = None

    first_time = False
    # Last played song
    if not request.user.is_anonymous:
        last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
        else:
            first_time = True
            last_played_song = Song.objects.get(id=17)

    else:
        first_time = True
        last_played_song = Song.objects.get(id=17)

    # Display all songs
    songs = Song.objects.all()

    # Display few songs on home page
    songs_all = list(Song.objects.all().values('id').order_by('?'))
    sliced_ids = [each['id'] for each in songs_all][:5]
    indexpage_songs = Song.objects.filter(id__in=sliced_ids)

    # Display Pop Songs
    songs_pop = list(Song.objects.filter(genre='Pop').values('id'))
    sliced_ids = [each['id'] for each in songs_pop][:5]
    indexpage_pop_songs = Song.objects.filter(id__in=sliced_ids)

    # Display Rock Songs
    songs_rock = list(Song.objects.filter(genre='Rock').values('id'))
    sliced_ids = [each['id'] for each in songs_rock][:5]
    indexpage_rock_songs = Song.objects.filter(id__in=sliced_ids)

    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        filtered_songs = songs.filter(Q(name__icontains=search_query)).distinct()
        context = {'all_songs': filtered_songs, 'last_played': last_played_song, 'query_search': True}
        return render(request, 'musicapp/index.html', context)

    context = {
        'all_songs': indexpage_songs,
        'recent_songs': recent_songs,
        'pop_songs': indexpage_pop_songs,
        'rock_songs': indexpage_rock_songs,
        'last_played': last_played_song,
        'first_time': first_time,
        'query_search': False,
    }
    return render(request, 'musicapp/index.html', context=context)


def pop_songs(request):
    pop_songs = Song.objects.filter(genre='Pop')

    # Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=17)

    query = request.GET.get('q')

    if query:
        pop_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'pop_songs': pop_songs}
        return render(request, 'musicapp/pop_songs.html', context)

    context = {'pop_songs': pop_songs, 'last_played': last_played_song}
    return render(request, 'musicapp/pop_songs.html', context=context)


def rock_songs(request):
    rock_songs = Song.objects.filter(genre='Rock')

    # Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        rock_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'rock_songs': rock_songs}
        return render(request, 'musicapp/rock_songs.html', context)

    context = {'rock_songs': rock_songs, 'last_played': last_played_song}
    return render(request, 'musicapp/rock_songs.html', context=context)


@login_required(login_url='login')
def play_song(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    return redirect('all_songs')


@login_required(login_url='login')
def play_song_index(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    return redirect('index')


@login_required(login_url='login')
def play_recent_song(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    return redirect('recent')


@login_required(login_url='login')
def play_random_song(request):
    random_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
    random_played_id = random.choice(random_played_list)['song_id']
    songs = Song.objects.filter(id=random_played_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    return redirect('index')


def all_songs(request):
    songs = Song.objects.all()

    first_time = False
    # Last played song
    if not request.user.is_anonymous:
        last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
    else:
        first_time = True
        last_played_song = Song.objects.get(id=17)

    # apply search filters
    qs_singers = Song.objects.values_list('singer').all()
    s_list = [s.split(',') for singer in qs_singers for s in singer]
    all_singers = sorted(list(set([s.strip() for singer in s_list for s in singer])))
    qs_genres = Song.objects.values_list('genre').all()
    all_genres = sorted(list(set([g.strip() for genre in qs_genres for g in genre])))

    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        search_singer = request.GET.get('singers') or ''
        search_genre = request.GET.get('genres') or ''
        filtered_songs = songs.filter(Q(name__icontains=search_query)).filter(
            Q(genre__icontains=search_genre)).filter(Q(singer__icontains=search_singer)).distinct()
        context = {
            'songs': filtered_songs,
            'last_played': last_played_song,
            'all_singers': all_singers,
            'all_genres': all_genres,
            'query_search': True,
        }
        return render(request, 'musicapp/all_songs.html', context)

    context = {
        'songs': songs,
        'last_played': last_played_song,
        'first_time': first_time,
        'all_singers': all_singers,
        'all_genres': all_genres,
        'query_search': False,
    }
    return render(request, 'musicapp/all_songs.html', context=context)


def recent(request):
    # Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=17)

    # Display recent songs
    recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
    if recent and not request.user.is_anonymous:
        recent_id = [each['song_id'] for each in recent]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id, recent__user=request.user)
        recent_songs = list()
        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
    else:
        recent_songs = None

    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        filtered_songs = recent_songs_unsorted.filter(Q(name__icontains=search_query)).distinct()
        context = {'recent_songs': filtered_songs, 'last_played': last_played_song, 'query_search': True}
        return render(request, 'musicapp/recent.html', context)

    context = {'recent_songs': recent_songs, 'last_played': last_played_song, 'query_search': False}
    return render(request, 'musicapp/recent.html', context=context)


@login_required(login_url='login')
def detail(request, song_id):
    songs = Song.objects.filter(id=song_id).first()

    # Add data to recent database
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()

    # Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=17)

    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
    is_favourite = Favourite.objects.filter(user=request.user).filter(song=song_id).values('is_fav')
    comments = Comments.objects.filter(song=song_id).order_by('date').reverse()

    if request.method == "POST":
        if 'playlist' in request.POST:
            playlist_name = request.POST["playlist"]
            q = Playlist(user=request.user, song=songs, playlist_name=playlist_name)
            q.save()
            messages.success(request, "Song added to playlist!")
        elif 'add-fav' in request.POST:
            is_fav = True
            query = Favourite(user=request.user, song=songs, is_fav=is_fav)
            print(f'query: {query}')
            query.save()
            messages.success(request, "Added to favorite!")
            return redirect('detail', song_id=song_id)
        elif 'rm-fav' in request.POST:
            is_fav = True
            query = Favourite.objects.filter(user=request.user, song=songs, is_fav=is_fav)
            print(f'user: {request.user}')
            print(f'song: {songs.id} - {songs}')
            print(f'query: {query}')
            query.delete()
            messages.success(request, "Removed from favorite!")
            return redirect('detail', song_id=song_id)
        elif 'comment' in request.POST:
            commentContent = request.POST["commentContent"]
            comment = Comments(user=request.user, song=songs, comment=commentContent)
            comment.save()
            return redirect('detail', song_id=song_id)

    context = {'songs': songs, 'playlists': playlists, 'is_favourite': is_favourite, 'last_played': last_played_song, 'comments': comments}
    return render(request, 'musicapp/detail.html', context=context)


def mymusic(request):
    return render(request, 'musicapp/mymusic.html')


def playlist(request):
    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
    context = {'playlists': playlists}
    return render(request, 'musicapp/playlist.html', context=context)


def playlist_songs(request, playlist_name):
    songs = Song.objects.filter(playlist__playlist_name=playlist_name, playlist__user=request.user).distinct()

    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        playlist_song = Playlist.objects.filter(playlist_name=playlist_name, song__id=song_id, user=request.user)
        playlist_song.delete()
        messages.success(request, "Song removed from playlist!")

    context = {'playlist_name': playlist_name, 'songs': songs}

    return render(request, 'musicapp/playlist_songs.html', context=context)


def favourite(request):
    songs = Song.objects.filter(favourite__user=request.user, favourite__is_fav=True).distinct()
    print(f'songs: {songs}')

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
                    {"empty_res": "There is no song with such information"})


def search_success(request, text):
    if len(text)>0:
        search_res = Song.objects.filter(name__search=text, singer__search=text)
        return render(request, "musicapp/search.html",
                {"search_res": search_res, "empty_res": "There is no such song"})


def profile(request):
    user_email = request.user.username
    if request.method == "POST":
        new_pass = request.POST.get("new_pass")
        u = User.objects.get(username=request.user.username)
        u.set_password(new_pass)
        u.save()
    return render(request, "musicapp/profile.html", {"user_email": user_email})


def payment(request):

    return render(request, "musicapp/payment.html")


def charge(request):

    if request.method == 'POST':
        print('Data: ', request.POST)

        customer = stripe.Customer.create(
            email=request.user.email,
            name=request.user.first_name,
            source=request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=100,
            currency='usd',
            description='Subscription'
        )

    return redirect('index')

def liked_music(request):
    popular_music = Song.objects.filter(favourite__is_fav=True).annotate(count=Count('favourite__song'))\
        .distinct().order_by('-count')
    context = {
        'popular_songs': popular_music,
    }
    return render(request, 'musicapp/liked_songs.html', context=context)

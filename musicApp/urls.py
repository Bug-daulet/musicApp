from django.urls import path
from . import views

# Add URLConf
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:song_id>/', views.detail, name='detail'),
    path('mymusic/', views.mymusic, name='mymusic'),
    path('playlist/', views.playlist, name='playlist'),
    path('playlist/<str:playlist_name>/', views.playlist_songs, name='playlist_songs'),
    path('favourite/', views.favourite, name='favourite'),
    path('all_songs/', views.all_songs, name='all_songs'),
    path('recent/', views.recent, name='recent'),
    path('pop_songs/', views.pop_songs, name='pop_songs'),
    path('rock_songs/', views.rock_songs, name='rock_songs'),
    path('play/<int:song_id>/', views.play_song, name='play_song'),
    path('play_song/<int:song_id>/', views.play_song_index, name='play_song_index'),
    path('play_recent_song/<int:song_id>/', views.play_recent_song, name='play_recent_song'),
    path('play_random_song', views.play_random_song, name='play_random_song'),
    path('profile/', views.profile, name='profile'),
    path('payment/', views.payment, name='payment'),
    path('charge/', views.charge, name='charge'),
    path('popular_songs/', views.liked_music, name='liked_songs'),
    path('suggested_songs/', views.suggested, name='suggested_songs'),
    path('categories/', views.categories, name='categories'),
    path('category_detail/<str:cat>', views.category_detail, name='category-detail'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('albums/', views.album_index, name='album-index'),
    path('albums/<int:album_id>', views.album_detail, name='album-detail'),

    path('albums/create/', views.AlbumCreate.as_view(), name='album-create'),
    path('albums/<int:pk>/update', views.AlbumUpdate.as_view(), name='album-update'),
    path('albums/<int:pk>/delete', views.AlbumDelete.as_view(), name='album-delete'),

    path('albums/<int:album_id>/add-listen', views.add_listen, name='add-listen'),

    path('albums/<int:album_id>/tracks/create/', views.create_track_for_album, name='create-track-for-album'),

    path('tracks/create/', views.TrackCreate.as_view(), name='track-create'),
    path('tracks/<int:pk>/', views.TrackDetail.as_view(), name='track-detail'),
    path('tracks/', views.TrackList.as_view(), name='track-index'),
    path('tracks/<int:pk>/update', views.TrackUpdate.as_view(), name='track-update'),
    path('tracks/<int:pk>/delete', views.TrackDelete.as_view(), name='track-delete'),

    path('albums/<int:album_id>/associate-track/<int:track_id>/', views.associate_track, name='associate-track'),
    path('albums/<int:album_id>/remove-track/<int:track_id>/', views.remove_track, name='remove-track'),

    path('accounts/signup/', views.signup, name='signup')
]

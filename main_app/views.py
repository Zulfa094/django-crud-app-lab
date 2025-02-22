from django.shortcuts import render, redirect
from .models import Album, Listen, Track
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView
from .forms import ListenForm, CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

class Home(TemplateView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

class AlbumCreate(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['title', 'artist', 'description', 'year']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AlbumUpdate(LoginRequiredMixin, UpdateView):
    model = Album
    fields = ['artist', 'description', 'year']

class AlbumDelete(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = '/albums/'

@login_required
def album_index(request):
    albums = Album.objects.filter(user=request.user)
    return render(request, 'albums/index.html', {'albums': albums})

@login_required
def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    tracks_album_doesnt_have = Track.objects.exclude(id__in = album.tracks.all().values_list('id'))
    listen_form = ListenForm()
    return render(request, 'albums/detail.html', {
        'album': album, 
        'listen_form': listen_form, 
        'tracks': tracks_album_doesnt_have
    })

@login_required
def add_listen(request, album_id):
    form = ListenForm(request.POST)
    if form.is_valid():
        new_listen = form.save(commit=False)
        new_listen.album_id = album_id
        new_listen.save()
    return redirect('album-detail', album_id=album_id)

class TrackCreate(LoginRequiredMixin, CreateView):
    model = Track
    fields = ['title', 'duration']

    def form_valid(self, form):
        track = form.save()
        return render(self.request, 'main_app/track_success.html', {
            'track': track,
            'albums': Album.objects.filter(user=self.request.user)
        })

class TrackList(LoginRequiredMixin, ListView):
    model = Track

class TrackDetail(LoginRequiredMixin, DetailView):
    model = Track

class TrackUpdate(LoginRequiredMixin, UpdateView):
    model = Track
    fields = ['title', 'duration']

class TrackDelete(LoginRequiredMixin, DeleteView):
    model = Track
    success_url = '/tracks/'

@login_required
def associate_track(request, album_id, track_id):
    Album.objects.get(id=album_id).tracks.add(track_id)
    return redirect('album-detail', album_id=album_id)

@login_required
def remove_track(request, album_id, track_id):
    Album.objects.get(id=album_id).tracks.remove(track_id)
    return redirect('album-detail', album_id=album_id)

@login_required
def create_track_for_album(request, album_id):
    album = Album.objects.get(id=album_id)
    
    if request.method == 'POST':
        track = Track.objects.create(
            title=request.POST['title'],
            duration=request.POST['duration']
        )
        album.tracks.add(track)
        return redirect('album-detail', album_id=album_id)
    
    return render(request, 'main_app/track_form_album.html', {
        'album': album
    })

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('album-index')
        else:
            error_message = 'Invalid sign up - try again'

    form = CustomUserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

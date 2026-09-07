from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from .models import Genre
from honermandan_app.models import honermendan, ArtistLike


def _hot_tracks(limit=4):
    """آهنگ‌های هنرمندان پرلایک"""
    top_artists = (
        ArtistLike.objects
        .values('artist_name')
        .annotate(like_count=Count('id'))
        .order_by('-like_count')[:limit]
    )
    top_names = [a['artist_name'] for a in top_artists]
    hot = []
    seen = set()
    for name in top_names:
        track = honermendan.objects.filter(name=name).first()
        if track and track.pk not in seen:
            track.like_count = ArtistLike.objects.filter(artist_name=name).count()
            hot.append(track)
            seen.add(track.pk)
    return hot


def genre_list(request):
    all_tracks = honermendan.objects.all().order_by('-id')

    genres = Genre.objects.annotate(track_count=Count('tracks')).order_by('name')

    selected_slug = request.GET.get('genre')

    selected_genre = None
    tracks = all_tracks

    if selected_slug:
        selected_genre = genres.filter(slug=selected_slug).first()
        if selected_genre:
            tracks = all_tracks.filter(genre=selected_genre)

    return render(
        request,
        'genres.html',
        {
            'genres': genres,
            'tracks': tracks,
            'all_tracks_count': all_tracks.count(),
            'selected_genre': selected_genre,
            'hot_tracks': _hot_tracks(),
        }
    )


def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)

    genres = Genre.objects.annotate(track_count=Count('tracks')).order_by('name')
    tracks = honermendan.objects.filter(genre=genre).order_by('-id')

    return render(
        request,
        'genres.html',
        {
            'genre': genre,
            'genres': genres,
            'tracks': tracks,
            'all_tracks_count': honermendan.objects.count(),
            'selected_genre': genre,
        }
    )

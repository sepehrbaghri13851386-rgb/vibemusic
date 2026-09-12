import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.conf import settings
from honermandan_app.models import honermendan, ArtistLike, HotSuggestion, Comment
from genres_app.models import Genre
from loginsogin_app.models import CustomUser
from blog_app.models import Blog
from django.db.models import Count, Q


def _file_exists(field_file):
    """Check if a FileField/ImageField file actually exists on disk."""
    if not field_file:
        return False
    try:
        return os.path.isfile(field_file.path)
    except (ValueError, OSError):
        return False


def _tracks():
    return honermendan.objects.all().order_by('-id')


def _like_counts():
    """دیکشنری {نام هنرمند: تعداد لایک}"""
    counts = {}
    for row in ArtistLike.objects.values('artist_name').all():
        counts[row['artist_name']] = counts.get(row['artist_name'], 0) + 1
    return counts


def home(request):
    tracks = _tracks()
    return render(request, 'index.html', {
        'tracks': tracks,
        'artists': tracks,
        'artists_count': tracks.values('name').distinct().count(),
    })


def artists(request):
    tracks = _tracks()
    
    names = tracks.values_list('name', flat=True).distinct()
    
    like_counts = _like_counts()
    user_id = request.session.get('user_id')
    liked_names = set()
    if user_id:
        liked_names = set(ArtistLike.objects.filter(user_id=user_id).values_list('artist_name', flat=True))

    artist_list = []
    seen_names = set()
    
    for name in names:
        if name in seen_names:
            continue
        seen_names.add(name)
        
        first = tracks.filter(name=name).first()
        if first:
            first.track_count = tracks.filter(name=name).count()
            first.like_count = like_counts.get(name, 0)
            first.liked_by_user = name in liked_names
            artist_list.append(first)

    hot_tracks = HotSuggestion.objects.filter(active=True).select_related('track')

    return render(request, 'artists.html', {
        'artists': artist_list,
        'artists_count': len(artist_list),
        'tracks': tracks,
        'top_tracks': tracks[:20],
        'hot_tracks': hot_tracks,
    })


def artist_detail(request, artist_id):
    first_track = get_object_or_404(honermendan, pk=artist_id)
    artist_name = first_track.name
    artist_tracks = _tracks().filter(name=artist_name)
    artist_info = artist_tracks.first()

    like_count = ArtistLike.objects.filter(artist_name=artist_name).count()
    user_id = request.session.get('user_id')
    liked_by_user = False
    is_admin = False
    current_user = None
    
    if user_id:
        current_user = CustomUser.objects.filter(pk=user_id).first()
        liked_by_user = ArtistLike.objects.filter(artist_name=artist_name, user_id=user_id).exists()
        if current_user:
            is_admin = current_user.is_admin

    comments = Comment.objects.filter(track=first_track, parent__isnull=True).select_related('user').prefetch_related('replies__user')

    if request.method == 'POST' and user_id:
        comment_text = request.POST.get('comment_text', '').strip()
        parent_id = request.POST.get('parent_id')
        if comment_text:
            parent_comment = None
            if parent_id:
                parent_comment = Comment.objects.filter(pk=parent_id, track=first_track).first()
            Comment.objects.create(
                track=first_track,
                user=current_user,
                text=comment_text,
                parent=parent_comment,
            )
            return redirect('artist_detail', artist_id=artist_id)

    return render(request, 'artist_detail.html', {
        'artist': artist_info,
        'tracks': artist_tracks,
        'track_count': artist_tracks.count(),
        'like_count': like_count,
        'liked_by_user': liked_by_user,
        'comments': comments,
        'comment_count': Comment.objects.filter(track=first_track).count(),
        'is_admin': is_admin,
        'current_user': current_user,
    })


def artist_detail_default(request):
    first_artist = honermendan.objects.first()
    if first_artist:
        return artist_detail(request, first_artist.pk)
    else:
        return render(request, 'artist_detail.html', {'artist': None, 'tracks': [], 'track_count': 0})


def charts(request):
    tracks = _tracks()

    like_counts = _like_counts()
    top_names = sorted(like_counts.items(), key=lambda x: x[1], reverse=True)[:4]

    top_artists = []
    for name, count in top_names:
        artist_track = tracks.filter(name=name).first()
        if artist_track:
            artist_track.like_count = count
            top_artists.append(artist_track)

    top_tracks = HotSuggestion.objects.filter(active=True).select_related('track')

    return render(request, 'charts.html', {'tracks': tracks, 'top_artists': top_artists, 'top_tracks': top_tracks})


def discover(request):
    tracks = _tracks()

    top_tracks = HotSuggestion.objects.filter(active=True).select_related('track')

    latest_tracks = list(tracks[:5])

    latest_posts = Blog.objects.filter(is_published=True).order_by('-created_at')[:3]

    return render(request, 'discover.html', {
        'tracks': tracks,
        'top_tracks': top_tracks,
        'latest_tracks': latest_tracks,
        'latest_posts': latest_posts,
    })


def blog(request):
    return render(request, 'blog.html')


def blog_detail(request):
    return render(request, 'blog.detail.html')


def item_detail(request, item_id=None):
    track = get_object_or_404(honermendan, pk=item_id) if item_id else _tracks().first()
    return render(request, 'item.detail.html', {'item': track, 'track': track})


def about(request):
    return render(request, 'page.about.html')


def not_found_demo(request):
    return render(request, '404.html', status=404)


def server_error_demo(request):
    return render(request, '505.html', status=500)


def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signin')
    
    user = get_object_or_404(CustomUser, pk=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        profile_image = request.FILES.get('profile_image')
        
        if username and username != user.username:
            if CustomUser.objects.filter(username=username).exclude(pk=user.pk).exists():
                from django.contrib import messages
                messages.error(request, 'این نام کاربری قبلاً استفاده شده است.')
                return render(request, 'profile.html', {'user': user})
            user.username = username
        
        if email and email != user.email:
            if CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
                from django.contrib import messages
                messages.error(request, 'این ایمیل قبلاً ثبت شده است.')
                return render(request, 'profile.html', {'user': user})
            user.email = email
        
        if profile_image:
            user.profile_image = profile_image
        
        user.save()
        from django.contrib import messages
        messages.success(request, 'پروفایل با موفقیت به‌روزرسانی شد.')
    
    return render(request, 'profile.html', {'user': user})


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '505.html', status=500)


def search(request):
    q = request.GET.get('q', '').strip()
    tracks = []
    artists_found = []
    if q:
        tracks = honermendan.objects.filter(
            Q(name_track__icontains=q) | Q(name__icontains=q)
        ).order_by('-id')[:30]
        
        artist_names = honermendan.objects.filter(name__icontains=q).values_list('name', flat=True).distinct()[:10]
        for name in artist_names:
            first_track = honermendan.objects.filter(name=name).first()
            if first_track:
                artists_found.append({
                    'name': name,
                    'id': first_track.pk,
                    'image': first_track.image,
                    'has_image': first_track.has_image,
                    'track_count': honermendan.objects.filter(name=name).count(),
                })
    return render(request, 'search.html', {
        'query': q,
        'tracks': tracks,
        'artists': artists_found,
    })
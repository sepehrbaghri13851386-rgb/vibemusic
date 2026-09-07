from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import honermendan, ArtistLike, HotSuggestion, Comment


def _tracks():
    return honermendan.objects.all().order_by('-id')


def _like_counts():
    """دیکشنری {نام هنرمند: تعداد لایک}"""
    counts = {}
    for row in ArtistLike.objects.values('artist_name').all():
        counts[row['artist_name']] = counts.get(row['artist_name'], 0) + 1
    return counts


def artists_list(request):
    """لیست هنرمندان"""
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
    """جزئیات هنرمند"""
    first_track = get_object_or_404(honermendan, pk=artist_id)
    artist_name = first_track.name
    artist_tracks = _tracks().filter(name=artist_name)
    artist_info = artist_tracks.first()

    if artist_info and not artist_info.image:
        artist_info.image = 'assets/img/a0.jpg'

    like_count = ArtistLike.objects.filter(artist_name=artist_name).count()
    user_id = request.session.get('user_id')
    liked_by_user = False
    is_admin = False
    current_user = None
    
    if user_id:
        from loginsogin_app.models import CustomUser
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
    """صفحه پیش‌فرض هنرمند (بدون ID)"""
    first_artist = honermendan.objects.first()
    if first_artist:
        return artist_detail(request, first_artist.pk)
    else:
        return render(request, 'artist_detail.html', {'artist': None, 'tracks': [], 'track_count': 0})


def toggle_artist_like(request, artist_id):
    """لایک/آنلایک هنرمند"""
    artist = get_object_or_404(honermendan, pk=artist_id)
    artist_name = artist.name
    
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signin')
    
    existing_like = ArtistLike.objects.filter(artist_name=artist_name, user_id=user_id).first()
    
    if existing_like:
        existing_like.delete()  # حذف لایک
    else:
        ArtistLike.objects.create(artist_name=artist_name, user_id=user_id)
    
    return redirect('artist_detail', artist_id=artist_id)

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from .models import honermendan, ArtistLike


def toggle_artist_like(request, artist_id):
    """
    لایک/آنلایک یک هنرمند. برای لایک کردن باید کاربر وارد شده باشه.
    """
    track = get_object_or_404(honermendan, pk=artist_id)
    artist_name = track.name

    user_id = request.session.get('user_id')
    if not user_id:
        messages.info(request, 'برای لایک کردن هنرمند، ابتدا وارد شوید.')
        login_url = reverse('signin')
        next_url = request.META.get('HTTP_REFERER', reverse('artist_detail', args=[artist_id]))
        return redirect(f'{login_url}?next={next_url}')

    like_qs = ArtistLike.objects.filter(artist_name=artist_name, user_id=user_id)
    if like_qs.exists():
        like_qs.delete()
    else:
        ArtistLike.objects.create(artist_name=artist_name, user_id=user_id)

    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('artist_detail', artist_id=artist_id)

from django.shortcuts import render, get_object_or_404
from .models import Blog, FeaturedContent, FeaturedTrack

def blog_list(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-created_at')
    featured_content = FeaturedContent.objects.filter(active=True).order_by('order')
    featured_tracks = FeaturedTrack.objects.filter(active=True).select_related('track').order_by('order')
    context = {
        'blogs': blogs,
        'featured_content': featured_content,
        'featured_tracks': featured_tracks,
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk, is_published=True)
    context = {
        'blog': blog
    }
    return render(request, 'blog/blog_detail.html', context)
"""
URL configuration for music_proje project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from loginsogin_app import views as auth_views
from genres_app import views as genres_views
from honermandan_app import views as honermandan_views


urlpatterns = [

    # =====================================================
    # ADMIN
    # =====================================================

    path('admin/', admin.site.urls),


    # =====================================================
    # HOME
    # =====================================================

    path('', views.home, name='home'),


    # =====================================================
    # AUTHENTICATION
    # =====================================================

    path('signup/', auth_views.signup, name='signup'),
    path('signin/', auth_views.signin, name='signin'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('forgot-password/', auth_views.forgot_password_view, name='forgot_password'),
    path('reset-password/<str:token>/', auth_views.reset_password_view, name='reset_password'),


    # =====================================================
    # ARTISTS
    # =====================================================

    path('artists/', views.artists, name='artists'),
    
    # صفحه هنرمند پیش‌فرض (بدون ID)
    path('artist/', views.artist_detail_default, name='artist_detail_default'),
    
    # صفحه هنرمند با ID
    path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),

    # لایک هنرمند
    path('artist/<int:artist_id>/like/', honermandan_views.toggle_artist_like, name='toggle_artist_like'),


    # =====================================================
    # GENRES
    # =====================================================

    path('genres/', genres_views.genre_list, name='genres'),
    path('genres/<slug:slug>/', genres_views.genre_detail, name='genre_detail'),


    # =====================================================
    # ITEMS / TRACKS
    # =====================================================

    path('item/', views.item_detail, name='item_detail'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail_with_id'),


    # =====================================================
    # BLOG
    # =====================================================

    path('blog/', include('blog_app.urls')),


    # =====================================================
    # CHARTS / DISCOVER
    # =====================================================

    path('charts/', views.charts, name='charts'),
    path('discover/', views.discover, name='discover'),


    # =====================================================
    # PROFILE
    # =====================================================

    path('profile/', views.profile, name='profile'),


    # =====================================================
    # OTHER PAGES
    # =====================================================

    path('about/', views.about, name='about'),


    # =====================================================
    # SEARCH
    # =====================================================

    path('search/', views.search, name='search'),


    # =====================================================
    # ERROR PAGES
    # =====================================================

    path('404/', views.not_found_demo, name='not_found_demo'),
    path('505/', views.server_error_demo, name='server_error_demo'),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
else:
    # On production (Render), also serve media files
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )


handler404 = 'music_proje.views.custom_404'
handler500 = 'music_proje.views.custom_500'
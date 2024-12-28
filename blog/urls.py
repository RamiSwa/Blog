from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<str:name>/', views.tag_posts, name='tag_posts'),
    path('<int:id>/like/', views.like_post, name='like_post'),
    path('<int:id>/dislike/', views.dislike_post, name='dislike_post'),
]

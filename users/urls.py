from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.register_user),

    path(
        'profile/<str:username>/',
        views.profile
    ),

    path('create-post/', views.create_post),

    path('posts/', views.get_posts),

    path(
        'like-post/<int:post_id>/',
        views.like_post
    ),

    path(
        'delete-post/<int:post_id>/',
        views.delete_post
    ),

    path(
        'comment/<int:post_id>/',
        views.add_comment
    ),

    path(
        'follow/<int:user_id>/',
        views.follow_user
    ),

    path('', views.home),
]
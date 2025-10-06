from django.urls import path
from . import views


urlpatterns = [
    path("posts/", views.post_list, name="post_list"),
    path("posts/<int:pk>/", views.post_details, name="post_details"),
    path("posts/<int:post_id>/comments/", views.comment_list, name="comment_list"),
    path(
        "posts/<int:post_id>/comments/<int:pk>/",
        views.comment_details,
        name="comment_details",
    ),
    path("posts/search/", views.post_search, name="post_search"),
]

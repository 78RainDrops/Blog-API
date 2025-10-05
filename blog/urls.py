from django.urls import path
from . import views


urlpatterns = [
    path("posts/", views.post_list, name="post_list"),
    path("posts/<int:pk>/", views.post_details, name="post_details"),
    path("posts/search/", views.post_search, name="post_search"),
]

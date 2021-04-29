from django.urls import path
from .views import post_comment_create_list_view,like_unlike_post_view, PostDeleteView,PostUpdateView

app_name = 'posts'
urlpatterns = [
    path('', post_comment_create_list_view, name = 'main-post-view'),
    path('like',like_unlike_post_view, name='like-post-view'),
    path('<pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update', PostUpdateView.as_view(), name='post-update'),
]
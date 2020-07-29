from django.urls import path
from .views import PostAPIView, LikeAPIView

urlpatterns = [
    path('posts', PostAPIView.as_view()),
    path('likes', LikeAPIView.as_view()),
]

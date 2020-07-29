from django.shortcuts import render
from Insta.models import Post, InstaUser, Like
from rest_framework import viewsets
from rest_framework import generics

from .serializers import PostSerializer, LikeSerializer

# Create your views here.


class PostAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeAPIView(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

from django.shortcuts import render
from rest_framework import viewsets
from . import models
from .serializer import PostSerializer

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
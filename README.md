# django rest_framework study 

- ***lecture: Likelion django restframework***
- framework: django, djangorestframework
- language: python

<br>

### install
- $pip install django
- $pip install djangorestframework

<br><br>

urls.py

~~~python
# router

from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register = ('post',views.PostViewSet)

urlpatterns = [
    path('',include(router.urls)),
]
~~~

~~~pyhton
# without router

from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("post", views.PostList.as_view()),
    path("post/<int:pk>", views.PostDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
~~~

<br>

## ***API VIEWS***

views.py
~~~python
# API VIEWS

from .models import Post
from .serializer import PostSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
~~~

<br>

## ***MIXIN***

views.py

~~~python
# MIXIN

from .models import Post
from .serializer import PostSerializer
from rest_framework import generics
from rest_framework import mixins


class PostList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    # 쿼리셋 등록
    queryset = Post.objects.all()
    # Serializer 클래스 등록
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    # 쿼리셋 등록
    queryset = Post.objects.all()
    # Serializer 클래스 등록
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
~~~

<br>

## ***GENERIC CBV***

views.py
~~~python
# GENERIC CBV

from .serializer import PostSerializer
from .models import Post
from rest_framework import generics

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
~~~

<br>

## ***VIEWSET***

~~~python
# VIEW SET

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [
        permission.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
~~~

### action decorator
- 커스텀 views 를 작성할 때 사용
- @action(method=['POST or GET ...'], detail=none, renderer_classes=[#])
    - renderer.JSONRenderer (default)
    - renderer.BrowsableAPIRenderer (default)
    - renderer.StaticHTMLRenderer
    - TemplateHTMLRenderer
    - ...
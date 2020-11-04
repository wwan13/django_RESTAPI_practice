from . import models
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['title','body']
        # fields = '__all__' # 모델에 있는 필드 전부 다 포함
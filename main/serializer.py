from . import models
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post 
        fields = ['id','title','body'] # 장고 기본의 pk값과 동일  __all__해도 나옴
        # fields = ['title','body']
        # fields = '__all__' # 모델에 있는 필드 전부 다 포함

        # read_only_field = ('title',) # read_only_field를 튜플 방식으로 설정
        # write_only_field = ('title',) # write_only_field를 튜플 방식으로 설정

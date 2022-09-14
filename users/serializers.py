from rest_framework import serializers
from users.models import Post


class PostSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user_id')
    title = serializers.CharField(max_length=200)
    body = serializers.CharField(max_length=1000)

    class Meta:
        model = Post
        fields = ('id', 'userId', 'title', 'body')

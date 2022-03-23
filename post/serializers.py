from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    body = serializers.CharField()
    date_pub = serializers.DateTimeField(read_only=True)
    author = serializers.CharField(read_only=True)
    likes_num = serializers.IntegerField(read_only=True)
    
    def validate(self, data):
        title = data.get('title', None)
        body = data.get('body', None)

        if title is None:
            raise serializers.ValidationError('Title is required')
        if body is None:
            raise serializers.ValidationError('Body is required')

        return {
            "title" : title,
            "body" : body
        }
    
    def save(self, validated_data, user):
        post = Post(**validated_data, author = user)
        return post.save()
    
    class Meta:
        model = Post
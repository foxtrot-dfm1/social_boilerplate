from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework import status, exceptions

from .mixins import LikeUnlikeMixin
from .models import Post
from .serializers import PostSerializer
from .renderers import *

class PostListView(GenericAPIView):
    permission_classes = (AllowAny, )

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class PostView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    renderer_classes = (PostJSONRenderer, )
    model = Post

    def get(self, request, id):
        try:
            post = self.model.objects.get(id = id)
        except self.model.DoesNotExist:
            raise exceptions.NotFound("Post is not found")

        serializer = self.serializer_class(post)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        post = request.data.get('post', {})
        serializer = self.serializer_class(data = post)
        serializer.is_valid(raise_exception = True)
        serializer.save(serializer.validated_data, user)

        return Response(serializer.data, status = status.HTTP_201_CREATED)

#todo: refactor like/unlike (may be join calsses)
class PostLike(APIView, LikeUnlikeMixin):
    permission_classes = (IsAuthenticated, )
    model = Post

    def get(self, request, id):
        if self.like(request.user, id):
            return Response({"like" : "ok"}, status = status.HTTP_200_OK)
        return Response(None, status = status.HTTP_409_CONFLICT)
        
class PostUnlike(APIView, LikeUnlikeMixin):
    permission_classes = (IsAuthenticated, )
    model = Post

    def get(self, request, id):
        if self.unlike(request.user, id):
            return Response({"like" : "removed"}, status = status.HTTP_200_OK)
        return Response(None, status = status.HTTP_409_CONFLICT)
    
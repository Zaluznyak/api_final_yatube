from rest_framework import viewsets, filters, permissions, mixins
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Group, Follow, Post
from .serializers import (
    PostSerializer, CommentSerializer,
    FollowSerializer, GroupSerializer
)
from .permissions import IsOwnerOrReadOnly


class MixinsViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    pass


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        comments = post.comments.all()
        return comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user,
                        post=post)


class FollowViewSet(MixinsViewSet):
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

    def get_queryset(self):
        return self.request.user.following.all()


class GroupViewSet(MixinsViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

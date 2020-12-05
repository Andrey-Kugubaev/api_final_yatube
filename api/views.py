from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import serializers

from .models import Post, Comment, Follow, Group
from .serializers import PostSerializer,\
    CommentSerializer,\
    FollowSerializer,\
    GroupSerializer

from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model


User = get_user_model()


class IsUserPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsUserPermission
    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsUserPermission
    )

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        queryset = Comment.objects.filter(post=post)
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, IsUserPermission)
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

    def get_queryset(self):
        queryset = Follow.objects.filter(
            following__username=self.request.user
        )
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        following = User.objects.filter(
            username=self.request.data.get('following')
        )
        if not following.exists():
            raise serializers.ValidationError()
        if Follow.objects.filter(
                user=user, following=following.first()
        ).exists():
            raise serializers.ValidationError()
        if self.request.user.username == self.request.data.get('following'):
            raise serializers.ValidationError()
        serializer.save(user=user, following=following.first())


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

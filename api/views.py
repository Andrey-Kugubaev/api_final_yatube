from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action

from .models import Post, Follow, Group
from .serializers import PostSerializer, \
    CommentSerializer, \
    FollowSerializer, \
    GroupSerializer

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
        post_id = self.kwargs['post_id']
        post = get_object_or_404(
            Post.objects.prefetch_related('comments').all(),
            id=post_id
        )
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


@action(detail=True, methods=['GET', 'POST'])
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
        serializer.save(user=user, following=following.first())


@action(detail=True, methods=['GET', 'POST'])
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

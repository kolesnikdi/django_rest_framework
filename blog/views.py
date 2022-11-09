from django.utils import timezone

from rest_framework import permissions, renderers, viewsets, generics, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response

from mysite.permissions import IsOwnerOrReadOnly, IsPostIdExists
from blog.models import Post, Comment
from blog.serializers import SnippetSerializer, CommentsSerializer, SnippetSerializerPutPost


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return SnippetSerializerPutPost
        return self.serializer_class

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        """open blog text in the new link"""
        blog_text = self.get_object()
        return Response(blog_text.text)

    def perform_create(self, serializer):
        """signs the post by name of user. Signs the post by current time"""
        serializer.save(author=self.request.user, published_date=timezone.now())


class CommentsView(generics.ListCreateAPIView):  # ListCreateAPIView gives list of the posts
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostIdExists]
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        # post = Post.objects.filter(id=self.kwargs['id'])
        # if not post:
        #     raise exceptions.NotFound()
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(author_id=user.id, blog_id=kwargs['id'])
        # blog_id gives id of the blog to the lookup_field

        return Response(
            self.serializer_class(instance=comment).data,
            status=status.HTTP_201_CREATED,
        )

    # def list(self, request, *args, **kwargs):
    #     """filter by id. if blog with request id doesn`t exist it will rise exception"""
    #     post = Post.objects.filter(id=self.kwargs['id'])
    #     if not post:
    #         raise exceptions.NotFound()
    #     return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """filter and returns the comments that belongs to current blog"""
        qs = self.queryset.filter(
            blog_id=self.kwargs['id'],
        )
        return qs

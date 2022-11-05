from django.utils import timezone

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mysite.permissions import IsOwnerOrReadOnly
from blog.models import Post
from blog.serializers import SnippetSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):  # open blog text in new link
        blog_text = self.get_object()
        return Response(blog_text.text)

    def perform_create(self, serializer):   # signs the post by name of user
        serializer.save(author=self.request.user, published_date=timezone.now())
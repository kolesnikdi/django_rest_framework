from django.urls import include, path

from blog import views

"""
FOR DRF
"""
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'_post', views.SnippetViewSet, basename="_post")

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('', include(router.urls)),  # """ FOR DRF """
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # """ FOR DRF """
]

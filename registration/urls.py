from django.urls import include, path, re_path
from rest_framework import routers

from registration import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('registration/', views.RegisterTryView.as_view(), name='registration'),
    re_path(r'registration/(?P<code>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/',
            views.RegisterConfirmView.as_view(), name='registration_confirm'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]

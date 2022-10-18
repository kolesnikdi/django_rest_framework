from django.contrib.auth.models import User
from django.core.mail import send_mail

from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from registration.models import RegistrationTry
from registration.serializers import RegisterConfirmSerializer, CreateRegisterTrySerializer, UserSerializer
from registration.business_logic import mail, final_creation
from mysite.permissions import IsNotAuthenticated, IsAdminUserOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    Can see blog text and can change author of the blog. Can create new author
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = RegisterConfirmSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class RegisterTryView(generics.CreateAPIView):
    serializer_class = CreateRegisterTrySerializer
    permission_classes = [IsNotAuthenticated]
    queryset = RegistrationTry.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reg_try = serializer.save()
        send_mail(**mail, recipient_list=[reg_try.email],
                  html_message=f"http://127.0.0.1:8000/registration/{reg_try.code}")
        # todo: How correctly write html_message?

        return Response(
            self.serializer_class(instance=reg_try).data,
            status=status.HTTP_201_CREATED,
        )


class RegisterConfirmView(generics.CreateAPIView):
    serializer_class = RegisterConfirmSerializer
    permission_classes = [IsNotAuthenticated]
    queryset = RegistrationTry.objects.all()
    lookup_field = 'code'

    def post(self, request, *args, **kwargs):
        serializer_context = {'request': request}  # need to use HyperlinkedModelSerializer in UserSerializer
        reg_try = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, reg_try = final_creation(serializer, reg_try)

        return Response(
            UserSerializer(instance=user, context=serializer_context).data,
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        """Check confirmation_time if it is null then allows to make registration"""
        qs = self.queryset.filter(
            confirmation_time__isnull=True,
        )
        return qs
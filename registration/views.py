import datetime

from django.contrib.auth.models import User

from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from registration.models import RegistrationTry
from registration.serializers import RegisterConfirmSerializer, CreateRegisterTrySerializer
from registration.send_mail import send_mail
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
        print(reg_try.code)
        send_mail(url=reg_try.code, text='Here is your registration url---> ', subject='DjangoBoy Blog registration-',
                  from_email='segareta@ukr.net', to_emails=[reg_try.email])  # in the beginning it was -> from_email=''

        return Response(
            self.serializer_class(instance=reg_try).data,
            status=status.HTTP_201_CREATED,
        )


class RegisterConfirmView(generics.CreateAPIView):
    serializer_class = RegisterConfirmSerializer
    permission_classes = [IsNotAuthenticated]
    queryset = RegistrationTry.objects.all()
    lookup_field = 'code'

    # todo: I get  response - HTTP 405 Method Not Allowed      "detail": "Method \"GET\" not allowed."

    def post(self, request, *args, **kwargs):
        reg_try = self.get_object()
        user = self.get_serializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save(email=reg_try.email)
        # todo: can't migrate 'user creation' from serializers. Problems with set email and password
        reg_try.confirmation_time = datetime.datetime.now().replace(microsecond=0)
        # todo: Can we change only - auto_now=True or we must import datetime and set?
        reg_try.save()

        return Response(
            RegisterConfirmSerializer(instance=user).data,  # change from instance=reg_try
            status=status.HTTP_200_OK,
        )  # todo: I get  response - HTTP 404 Not Found with     "detail": "Not found."

    def get_queryset(self):
        """Check confirmation_time if it is null then allows to make registration"""
        qs = self.queryset.filter(
            confirmation_time__isnull=True,
        )
        return qs
    # get = post

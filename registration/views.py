from django.contrib.auth.models import User

from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from registration.models import RegistrationTry
from registration.serializers import RegisterConfirmSerializer, CreateRegisterTrySerializer, UserSerializer
from registration.business_logic import final_send_mail, final_creation
from mysite.permissions import IsNotAuthenticated, IsAdminUserOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    # turn off post - viewsets.ReadOnlyModelViewSet чи generics.RetrieveAPIView чи ListAPIView
    """
    Allows Admin to change author of the blog and create new author with performing the previous action/
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserOrReadOnly]



class RegisterTryView(generics.CreateAPIView):
    serializer_class = CreateRegisterTrySerializer
    permission_classes = [IsNotAuthenticated]
    queryset = RegistrationTry.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reg_try = serializer.save()
        final_send_mail(reg_try)

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
        user = final_creation(serializer.validated_data, reg_try)

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

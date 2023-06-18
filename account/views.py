from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from account.serializers import UserRegisterSerializer, UserLoginSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({
            'data': serializer.data,
            'message': 'Member registration success'
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data
        response = Response(
            {
                'token': token,
                'message': 'Login success',
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie('access_token', token['access_token'])
        response.set_cookie('refresh_token', token['refresh_token'])

        return response

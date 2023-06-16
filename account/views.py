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


# class UserVerifyView(generics.GenericAPIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         access_token = request.COOKIES['access_token']
#         # refresh_token = request.COOKIES['refresh_token']
#
#         try:
#             if not access_token:
#                 raise serializers.ValidationError('Access token not found in JWT cookie.')
#             # Check if the access token is active
#             # RefreshToken(access_token).check_exp()
#         except TokenError:
#             try:
#                 # Check if the refresh token is active
#                 RefreshToken(refresh_token).check_exp()
#                 # If refresh token is active, generate new token
#                 new_tokens = RefreshToken(refresh_token).access_token
#                 # Send new tokens in cookies
#                 response = Response({"detail": "Access token refreshed"})
#                 response.set_cookie(key='access_token', value=str(new_tokens))
#                 return response
#             except TokenError:
#                 return Response({"detail": "Both tokens are expired"}, status=status.HTTP_400_BAD_REQUEST)
#
#             # If token is active, return OK response
#         return Response({"detail": "Token is active"}, status=status.HTTP_200_OK)

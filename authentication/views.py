from django.contrib.auth import login
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import LoginSerializer, UserSerializer, TwoFAVerifySerializer, RegistrationSerializer
from .utils import generate_otp_secret, send_otp_via_call
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class RegisterView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        otp=generate_otp_secret()
        user.otp_secret=otp
        phone=serializer.data.get("phone")
        if send_otp_via_call(phone,otp):
        # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Account created successfully.",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "phone": user.phone,
                    "email": user.email,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        else:
                return Response({"message": "OTP Service crashed."}, status=500)


class LoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user.is_2fa_enabled:
            # Generate and send OTP
            otp_secret = generate_otp_secret()
            user.otp_secret = otp_secret
            user.save()
            refresh = RefreshToken.for_user(user)
            if send_otp_via_call(user.phone, otp_secret):
                return Response({"message": "OTP sent to your phone.","AccessToken":str(refresh.access_token),"RefresToken":str(refresh)}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "OTP Service crashed."}, status=500)


        # Issue tokens if 2FA is not enabled
        refresh = RefreshToken.for_user(user)
        login(request, user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    


class Verify2FAView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = TwoFAVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        user = request.user
        if otp==user.otp_secret:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
    

    
class UserUpdateView(generics.UpdateAPIView):
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]  
    queryset=CustomUser.objects.all()
    lookup_field='pk'  


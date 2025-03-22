# myapp/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import SignupSerializer,VerifyOTPSerializer,UserSerializer,LoginSerializer,UpdatePasswordSerializer, SendOtpSerializer, ResetPasswordSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .utils import create_response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# from .models import OTP


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    @swagger_auto_schema(
        operation_summary="Signup a new user",
        operation_description="This endpoint allows a new user to sign up.",
        request_body=SignupSerializer,
        responses={201: 'User created successfully'}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(data=serializer.data, message="User created successfully", status_code=status.HTTP_201_CREATED)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        first_error_message = next(iter(serializer.errors.values()))[0]    
        return create_response(error= first_error_message, message="Validation errors", status_code=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class VerifyOtpView(APIView):
    serializer_class = VerifyOTPSerializer

    @swagger_auto_schema(
        operation_summary="Verify OTP",
        operation_description="This endpoint allows a user to verify OTP.",
        request_body=VerifyOTPSerializer,
        responses={200: 'OTP verified successfully'}
    )
    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():
            # You can access the updated user from serializer.validated_data
            user = serializer.validated_data['data']
            # return Response({"message": "OTP verified successfully", "data": UserSerializer(user).data}, status=status.HTTP_200_OK)
            return create_response(data=UserSerializer(user).data, message="OTP verified successfully", status_code=status.HTTP_200_OK)
        first_error_message = next(iter(serializer.errors.values()))[0]
        return create_response(error=first_error_message, message="Invalid OTP.", status_code=status.HTTP_400_BAD_REQUEST)
        # return Response({
        #     "errors": serializer.errors,
        #     "message": "Invalid OTP.",
        #     "status": status.HTTP_400_BAD_REQUEST
        # }, status=status.HTTP_400_BAD_REQUEST)
    


#######Login view
class LoginView(APIView):
    """
    Login a user using email and password after OTP verification and return JWT token.
    """

    @swagger_auto_schema(
        operation_summary="Login a user and return JWT token",
        operation_description="This endpoint allows a user to login using email and password after OTP verification.",
        request_body=LoginSerializer,
        responses={200: 'Login successful', 400: 'Invalid credentials or OTP not verified'}
    )
    def post(self, request, *args, **kwargs):
        # Extract email and password from the request
        email = request.data.get("email")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        print(f"user valeu {user}")
        if user is not None:
            if user.is_verified:
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                return create_response(
                    data={
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "full_name": user.full_name,
                            "contact_no": user.contact_no,
                            "is_verified": user.is_verified,
                        },
                        "access_token": str(access_token),
                        "refresh_token": str(refresh),
                    },
                    message="Login successful",
                    status_code=status.HTTP_200_OK
                )
            else:
                return create_response(
                    error="User OTP not verified. Please verify your OTP first.",
                    message="OTP not verified",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        else:
            return create_response(
                error="Invalid email or password.",
                message="Invalid credentials",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        #         return Response({
        #             "message": "Login successful",
        #             "data": {
        #                 "user": {
        #                     "id": user.id,
        #                     "email": user.email,
        #                     "full_name": user.full_name,
        #                     "contact_no": user.contact_no,
        #                     "is_verified": user.is_verified,
        #                 },
        #                 "access_token": str(access_token),
        #                 "refresh_token": str(refresh),
        #             }
        #         }, status=status.HTTP_200_OK)
        #     else:
        #         return Response({
        #             "message": "User OTP not verified. Please verify your OTP first."
        #         }, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({
        #         "message": "Invalid email or password."
        #     }, status=status.HTTP_400_BAD_REQUEST)
        


class UpdatePasswordView(APIView):
    """
    Update the user's password. Requires the user to be authenticated using JWT.
    """
  

    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated using JWT
    @swagger_auto_schema(
            operation_summary="Allows to update password",
            operation_description="Allows to update password",
            request_body=UpdatePasswordSerializer,
            responses={200: 'password updated successfully', 400: 'something went wrong'}
    )
    def post(self, request, *args, **kwargs):
        serializer = UpdatePasswordSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            # Save the new password
            serializer.save()
            return create_response(message="Password updated successfully.", status_code=status.HTTP_200_OK)
            # return Response({
            #     "message": "Password updated successfully."
            # }, status=status.HTTP_200_OK)
        first_error_message = next(iter(serializer.errors.values()))[0]
        return create_response(error=first_error_message, message="Failed to update password.", status_code=status.HTTP_400_BAD_REQUEST)

        # return Response({
        #     "errors": serializer.errors,
        #     "message": "Failed to update password."
        # }, status=status.HTTP_400_BAD_REQUEST)


class SendOtpView(APIView):
    serializer_class = SendOtpSerializer

    @swagger_auto_schema(
        operation_summary="Generate and return OTP",
        operation_description="This endpoint generates an OTP for the provided email address and returns it.",
        request_body=SendOtpSerializer,
        responses={200: 'OTP generated successfully', 400: 'Invalid email'}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            otp = serializer.save()
            return Response({"message": "OTP generated successfully", "otp": otp}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ResetPasswordView(APIView):
    @swagger_auto_schema(
        operation_summary="Reset user password",
        operation_description="This endpoint resets the user's password using the provided new password and confirmation.",
        request_body=ResetPasswordSerializer,
        responses={
            200: 'Password reset successfully',
            400: 'Bad Request (e.g., passwords do not match or missing fields)',
            404: 'User not found'
        }
    )
    def post(self, request, *args, **kwargs):
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        email = request.data.get('email')

        if not new_password or not confirm_password or not email:
            return Response({"error": "New password, confirm password, and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user.password = make_password(new_password)
        user.save()

        return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)

    
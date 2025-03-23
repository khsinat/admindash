# myapp/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import SignupSerializer,VerifyOTPSerializer,UserSerializer,LoginSerializer,UpdatePasswordSerializer, SendOtpSerializer, ResetPasswordSerializer, ForgotPasswordSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .utils import create_response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# from .models import OTP
from django.contrib.auth import get_user_model
from django.contrib.auth import logout


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
                        "id": user.id,
                        "email": user.email,
                        "full_name": user.full_name,
                        "contact_no": user.contact_no,
                        "is_verified": user.is_verified,
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
            user_value = serializer.save()
            return_value = {
                                "id": user_value.id,
                                "email": user_value.email,
                            }
            return create_response(return_value,message="Password updated successfully.", status_code=status.HTTP_200_OK)
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
    
    
User = get_user_model()

class ResetPasswordView(APIView):
    @swagger_auto_schema(
        operation_summary="Reset user password",
        operation_description="This endpoint resets the user's password using the provided new password, confirmation, and OTP.",
        request_body=ResetPasswordSerializer,
        responses={
            200: 'Password reset successfully',
            400: 'Bad Request (e.g., passwords do not match or invalid OTP)',
            404: 'User not found'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
class LogoutView(APIView):

    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(

        operation_summary="Log out the user",

        operation_description="This endpoint logs out the currently authenticated user.",

        responses={

            200: 'Logout successful',

            401: 'Unauthorized (user not authenticated)',

            400: 'Bad Request (invalid token format or other errors)',

        }

    )

    def post(self, request, *args, **kwargs):

        auth_header = request.headers.get('Authorization')

        if not auth_header:

            return Response({"error": "Authorization header not provided."}, status=status.HTTP_400_BAD_REQUEST)


        token_prefix = 'Bearer '

        if not auth_header.startswith(token_prefix):

            return Response({"error": "Invalid token format."}, status=status.HTTP_400_BAD_REQUEST)


        refresh_token = auth_header[len(token_prefix):]
        try:

            token = RefreshToken(refresh_token)
            print(token)
            token.blacklist()

            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)

        except Exception as e:

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer

    @swagger_auto_schema(
        operation_summary="Forgot Password",
        operation_description="This endpoint sends an OTP to the user's email for password reset.",
        request_body=ForgotPasswordSerializer,
        responses={200: 'OTP sent successfully', 400: 'Invalid email'}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            otp = serializer.save()
            return create_response(data={"message": "OTP sent successfully", "otp": otp}, message ="OTP sent successfully" ,status_code=status.HTTP_200_OK)
        first_error_message = next(iter(serializer.errors.values()))[0]
        return create_response(error=first_error_message, message="Invalid email.", status_code=status.HTTP_400_BAD_REQUEST)
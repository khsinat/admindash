# myapp/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import SignupSerializer,VerifyOTPSerializer,UserSerializer,LoginSerializer,UpdatePasswordSerializer, SendOtpSerializer, ResetPasswordSerializer, ForgotPasswordSerializer, ProfileSerializer, ContactUsSerializer, PageSerializer
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
from .models import Page
from rest_framework_simplejwt.tokens import AccessToken
from .models import BlacklistedToken , STATE_DELETED
from .serializers import ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404


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
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            file_name = user.profile_file.name
            custom_url = f"https://cannabis.nexusappdevelopers.com/api/profile-file?file_path={file_name}"
            return create_response(
                data={
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "contact_no": user.contact_no,
                    "is_verified": user.is_verified,
                    "access_token": str(access_token),
                    "refresh_token": str(refresh),
                    "profile_file" : custom_url
                },
                message="Otp Verified successfully",
                status_code=status.HTTP_200_OK
            )
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
        # Query the user by email and check if state_id is not equal to 3

        is_valid_user = User.objects.filter(email=email).exclude(state_id=STATE_DELETED)

        if is_valid_user.exists():
            user = is_valid_user.first()
             # Authenticate the user
            user = authenticate(request, email=email, password=password)
            print(f"user valeu {user}")
            if user is not None:
                if user.is_verified:
                    # Generate JWT token
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token
                    file_name = user.profile_file.name
                    custom_url = f"https://cannabis.nexusappdevelopers.com/api/profile-file?file_path={file_name}"
                    return create_response(
                        data={
                            "id": user.id,
                            "email": user.email,
                            "full_name": user.full_name,
                            "contact_no": user.contact_no,
                            "is_verified": user.is_verified,
                            "access_token": str(access_token),
                            "refresh_token": str(refresh),
                            "profile_file" : custom_url
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
        else:
            return create_response(
                    error="User does not exist.",
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
            return create_response(data=otp, message ="OTP generated successfully" ,status_code=status.HTTP_200_OK)
            # return Response({"message": "OTP generated successfully", "otp": otp}, status=status.HTTP_200_OK)
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
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Get the access token from the request
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Verify the token
                AccessToken(token)
                # Blacklist the token
                BlacklistedToken.objects.create(token=token)
                return create_response(message ="Successfully logged out." ,status_code=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Authorization header missing."}, status=status.HTTP_400_BAD_REQUEST)
        


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
    


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_summary="Fetch or Edit User Profile",
        operation_description="This endpoint allows fetching or editing the user's profile.",
        request_body=ProfileSerializer,
        responses={200: 'Profile fetched or updated successfully', 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return create_response(data=serializer.data, message="Profile updated successfully", status_code=status.HTTP_200_OK)
        return create_response(error=serializer.errors, message="Validation errors", status_code=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Fetch User Profile",
        operation_description="This endpoint allows fetching the user's profile.",
        responses={200: 'Profile fetched successfully'}
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileSerializer(user)
        return create_response(data=serializer.data, message="Profile fetched successfully", status_code=status.HTTP_200_OK)
    
class ContactUsView(APIView):
    @swagger_auto_schema(
        operation_summary="Contact Us",
        operation_description="This endpoint allows users to send a contact request.",
        request_body=ContactUsSerializer,
        responses={200: 'Contact request received successfully', 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        serializer = ContactUsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return create_response(serializer.data, message="Thanks for contacting Cannabis AI. You will receive a response shortly at your registered email address.", status_code=status.HTTP_200_OK)

        return create_response(serializer.errors, message="Something went wrong.", status_code=status.HTTP_400_BAD_REQUEST)
    

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Delete Account",
        operation_description="This endpoint allows the authenticated user to soft delete their account. "
                              "The account will be marked as deleted and the token will be blacklisted.",
        responses={
            200: "Account deleted successfully",
            401: "Unauthorized (user not authenticated)",
            403: "Forbidden (user does not have permission)"
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        user.state_id = STATE_DELETED
        user.save()

        # Get the access token from the request
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Verify the token
                AccessToken(token)
                # Blacklist the token
                BlacklistedToken.objects.create(token=token)
            except Exception as e:
                return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Authorization header missing."}, status=status.HTTP_400_BAD_REQUEST)

        return create_response(
                    message= "Account deleted successfully",
                    status_code=status.HTTP_200_OK
                )
    
    

class PageDetailView(generics.RetrieveAPIView):
    serializer_class = PageSerializer

    @swagger_auto_schema(
        operation_summary="Get Page by Type",
        operation_description="This endpoint allows fetching a page based on its type ID. "
                              "Type ID 1 corresponds to 'Terms of Service', and Type ID 2 corresponds to 'Privacy Policy'.",
        responses={200: 'Page retrieved successfully', 404: 'Page not found'}
    )
    def get(self, request, *args, **kwargs):
        type_id = kwargs.get('type_id')
        queryset = Page.objects.all()
        if type_id is not None:
            try:
                # Filter the queryset based on type_id
                page = Page.objects.get(type_id=type_id)
                serializer = PageSerializer(page)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Page.DoesNotExist:
                return create_response(
                    error="Page not found",
                    message="The requested page does not exist.",
                    status_code=status.HTTP_404_NOT_FOUND
                )
        return create_response(
                    error="Type ID is required",
                    status_code=status.HTTP_404_NOT_FOUND
                )
        return Response({"error": "Type ID is required"}, status=status.HTTP_400_BAD_REQUEST)   
    
    
    
 
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Change Password",
        operation_description="This endpoint allows the authenticated user to change their password by providing the old password and the new password.",
        request_body=ChangePasswordSerializer,
        responses={
            200: "Password changed successfully",
            400: "Invalid old password or new password does not meet the requirements",
            401: "Unauthorized (user not authenticated)"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keep the user logged in

                return create_response(message= "Password changed successfully", status_code=status.HTTP_200_OK)
            else:
                return create_response(error= "Invalid old password", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return create_response(error= serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        
        
class ProfileFileDownloadView(APIView):

    def get(self, request, *args, **kwargs):
        file_path = request.GET.get('file_path')
        if not file_path:
            return create_response(error="File path is required.", status_code=status.HTTP_400_BAD_REQUEST)

        # Find the user with the specified profile file
        user = get_object_or_404(User, profile_file=file_path)

        # Ensure the file exists
        try:
            file = user.profile_file.open(mode='rb')
            response = FileResponse(file, content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="{user.profile_file.name}"'
            return response
        except FileNotFoundError:
            raise Http404("File not found.")
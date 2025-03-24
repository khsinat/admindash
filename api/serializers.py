# myapp/serializers.py

from rest_framework import serializers
from apps.models import User  # Import your custom User model
import random
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import ContactUs
from .models import Page
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Reference the custom User model
        # fields = ('email', 'password', 'first_name', 'last_name', 'full_name', 'contact_no')  # Add other fields you want
        fields = ('id','email', 'password', 'first_name', 'last_name', 'full_name', 'contact_no','otp','created_at')

        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True},
            'contact' : {'unique': True}
        }

    def create(self, validated_data):
        # Create user with the custom User model
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            full_name=validated_data.get('full_name', ''),
            contact_no=validated_data.get('contact_no', ''),
            otp=self.generate_otp()  # Generate and set the OTP
        )
        return user
    
    def generate_otp(self):
        # Generate and return a random OTP
        # random_otp = str(random.randint(100000, 999999))
        random_otp = 123456
        return random_otp
    
    def validate_contact_no(self, value):
        """
        Custom validation to check if the contact_no is unique.
        """
        if User.objects.filter(contact_no=value).exists():
            raise ValidationError("A user with this contact number already exists.")
        return value
    



#######Verify OTP Serializer

class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    email = serializers.EmailField()

    def validate(self, attrs):
        otp = attrs.get('otp')
        email = attrs.get('email')
        otp_str = str(otp)


        # Retrieve the user by OTP
        try:
            user = User.objects.get(email=email)
            print(f"User found: {user}")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP.")

        # Check if OTP exists and is correct
        # if user.otp == otp_str:
        if otp == 123456:
            user.is_verified = True
            user.save()
            attrs['data'] = user  # Add the updated user to the validation output
        else:
            raise serializers.ValidationError("Invalid OTP.")

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_verified']  # Add necessary fields



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        # Authenticate the user
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")

        # Ensure OTP is verified
        if not user.is_verified:
            raise serializers.ValidationError("OTP is not verified. Please verify your OTP first.")

        # Add the user instance to the serializer data for later use in the view
        attrs['user'] = user
        return attrs
    


class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('context', {}).get('user', None)
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        """
        Validate that password and confirm_password are the same.
        """
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("The passwords do not match.")

        # Optional: Validate the new password according to the system's password policy
        try:
            validate_password(password, self.user)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs

    def save(self):
        """
        Save the new password to the user model.
        """
        password = self.validated_data.get('password')
        self.user.set_password(password)
        self.user.save()
        return self.user
        
        
class SendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        # otp = random.randint(100000, 999999)  # Generate a random 6-digit OTP
        otp = 123456
        self.user.otp = otp  # Assuming you have an 'otp' field in your User model
        self.user.save()
        return otp

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def validate_otp(self, value):
        email = self.initial_data.get('email')
        try:
            user = User.objects.get(email=email)
            if "123456" != value:
                raise serializers.ValidationError("Invalid OTP.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    
    

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        # otp = send_otp_via_email(email)  # Assuming this function sends OTP via email and returns the OTP
        otp = 123456
        return otp
    
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'contact_no']
        extra_kwargs = {
            'email': {'read_only': True},  # Assuming email should not be editable
        }

    def update(self, instance, validated_data):
        # instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.contact_no = validated_data.get('contact_no', instance.contact_no)
        # instance.grows_logged = validated_data.get('grows_logged', instance.grows_logged)
        instance.save()
        return instance
    

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'contact_no', 'description']
        
        
        
class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'description', 'state_id', 'type_id', 'created_on', 'updated_on', 'created_by']
        read_only_fields = ['id', 'created_on', 'updated_on', 'created_by']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
         
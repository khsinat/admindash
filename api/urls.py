# myapp/urls.py

from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import SignupView,VerifyOtpView,LoginView,UpdatePasswordView,SendOtpView,ResetPasswordView,LogoutView, ForgotPasswordView, ProfileView, ContactUsView, DeleteAccountView, PageDetailView, ChangePasswordView, ProfileFileDownloadView,AnalysisCreateView,GetAnalysisView,GetGrowLogs,AddToGrowLogs,UserGrowLogsListView


schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    # url='http://127.0.0.1:8000/'
    url='https://cannabis.nexusappdevelopers.com'

)

urlpatterns = [
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/signup', SignupView.as_view(), name='signup'),
    path('api/verify-otp', VerifyOtpView.as_view(), name='verify-otp'),
    path('api/login', LoginView.as_view(), name='login'),  # Add the login path here
    path('api/update-password', UpdatePasswordView.as_view(), name='update-password'),  # New update password path
    path('api/resend-otp', SendOtpView.as_view(), name='resend-otp'),
    path('api/reset-password', ResetPasswordView.as_view(), name='reset-password'),
    path('api/logout', LogoutView.as_view(), name='logout'),
    path('api/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/contact-us', ContactUsView.as_view(), name='contact-us'),
    path('api/delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path('api/page/<int:type_id>/', PageDetailView.as_view(), name='page-detail'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/profile-file', ProfileFileDownloadView.as_view(), name='profile-file-download'),
    path('api/analysis', AnalysisCreateView.as_view(), name='analysis-create'),
    path('api/get-analysis/', GetAnalysisView.as_view(), name='get-analysis'),
    path('api/get-grow-logs/', GetGrowLogs.as_view(), name='get-grow-logs'),
    path('api/add-to-grow-logs/', AddToGrowLogs.as_view(), name='add-to-grow-logs'),
    path('api/grow-logs/', UserGrowLogsListView.as_view(), name='grow-logs'),


    # path('api/signup/', signup, name='signup'),
    # path('api/login/', login, name='login'),
]

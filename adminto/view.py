import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

# Configure database error logger
db_logger = logging.getLogger("django.db.backends")

# Function to check if the user is an admin
def is_admin(user):
    return user.is_staff  # Only staff users (admins) can access the dashboard

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")  # Redirect to admin dashboard
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "custom/auth-pages/login.html")  # Render login page

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("admin_login")  # Redirect to login page

# Dashboard View (Admin-Only)
@method_decorator(login_required(login_url="/login/"), name="dispatch")
@method_decorator(user_passes_test(is_admin, login_url="/login/"), name="dispatch")
class DashboardView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        try:
            users = get_user_model().objects.all()  # Fetch users
            context["users"] = users
        except DatabaseError as e:
            db_logger.error(f"Database error occurred: {e}")  # Log error to file
            context["users"] = []  # Ensure template doesn't break
            context["db_error"] = f"Database error: {str(e)}"  # Display error in template
        return context

# Serve dashboard at '/'
index_view = DashboardView.as_view()

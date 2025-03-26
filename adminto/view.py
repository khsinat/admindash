import logging
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

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

class UsersView(TemplateView):

    template_name = "custom/extra-pages/user-list.html"


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        

        # Get all users

        user_list = get_user_model().objects.all()  # Replace with your actual user model

        paginator = Paginator(user_list, 10)  # Show 10 users per page


        # Get the current page number from the request

        page_number = self.request.GET.get('page')

        users = paginator.get_page(page_number)


        # Add the paginated users to the context

        context['users'] = users

        context['paginator'] = paginator  # Optional: if you want to use paginator info in the template


        return context


# Create an instance of the view

users_view = UsersView.as_view()

def user_detail(request, user_id):
    # Retrieve the user object or return a 404 error if not found
    user = get_user_model()
    user = get_object_or_404(user, id=user_id)

    # Pass the user object to the template
    return render(request, 'custom/extra-pages/user-detail.html', {'user': user})
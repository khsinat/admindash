import logging
from django.shortcuts import render, redirect,get_object_or_404,get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from api.models import Page,PAGE_TYPE_TERMS_AND_CONDITIONS,PAGE_TYPE_PRIVACY_POLICY
from django.contrib.auth import get_user_model
User = get_user_model()

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

class TotalGrowLogsView(TemplateView):

    template_name = "custom/extra-pages/total-grow-logs.html"
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

total_grow_logs_view= TotalGrowLogsView.as_view()
class TotalAnalysisView(TemplateView):

    template_name = "custom/extra-pages/total-analysis.html"
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

total_analysis_view= TotalAnalysisView.as_view()

class PackagesView(TemplateView):

    template_name = "custom/extra-pages/packages.html"
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

packages_view= PackagesView.as_view()

class EmailsInQueue(TemplateView):

    template_name = "custom/extra-pages/emails-in-queue.html"
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

emails_in_queue_view= EmailsInQueue.as_view()
class TransactionsView(TemplateView):

    template_name = "custom/extra-pages/transactions.html"
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

transactions_view= TransactionsView.as_view()
class ContactusView(TemplateView):

    template_name = "custom/extra-pages/contact-us.html"
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

contactus_view= ContactusView.as_view()
class CmsView(TemplateView):

    template_name = "custom/extra-pages/cms.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = Page.objects.all().order_by('-created_on')  # or any ordering you prefer
        return context
    def post(self, request, *args, **kwargs):
        page_id = request.POST.get("delete_page_id")
        if page_id:
            page = get_object_or_404(Page, type_id=page_id)
            if request.user == page.created_by or request.user.is_staff:  # optional permission check
                page.delete()
        return redirect('cms')


cms_view= CmsView.as_view()

class NotificationsView(TemplateView):

    template_name = "custom/extra-pages/notifications.html"
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

notifications_view= NotificationsView.as_view()

class SettingsView(TemplateView):

    template_name = "custom/extra-pages/settings.html"
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

settings_view= SettingsView.as_view()


class MyprofileView(TemplateView):

    template_name = "custom/extra-pages/myprofile.html"
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

myprofile_view= MyprofileView.as_view()

class EditUserView(TemplateView):

    template_name = "custom/extra-pages/edit-user.html"
    def post(self , request, *args, **kwargs):
        user_id=   kwargs.get('user_id') 
        user_obj= get_object_or_404(User,id=user_id)

        full_name=request.POST.get("full_name")
        email=request.POST.get("email")
        profile_file=request.FILES.get("profile_file")

        if full_name:
            user_obj.full_name=full_name
        if email:
            user_obj.email=email
        if profile_file:
            user_obj.profile_file=profile_file

        user_obj.save()
        return redirect('myprofile')
edit_user_view= EditUserView.as_view()
class AddPageView(TemplateView):
    template_name = "custom/extra-pages/add-page.html"


    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        type_id = request.POST.get("type_id")
        description = request.POST.get("description")

        if Page.objects.filter(type_id=type_id).exists():
            messages.error(request, "A page with this type already exists.")
            return redirect('cms')  # or wherever your 

        Page.objects.create(
            title=title,
            type_id=type_id or None,
            description=description,
            created_by=request.user
        )

        return redirect('cms')  # or another success page name



add_page_view= AddPageView.as_view()

class ViewPageView(TemplateView):
    template_name = "custom/extra-pages/view-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_id = self.kwargs.get('type_id')  # assuming you use <int:pk> in URL
        context['page'] = get_object_or_404(Page, type_id=page_id)
        return context


view_page_view= ViewPageView.as_view()

class EditPageView(TemplateView):
    template_name = "custom/extra-pages/edit-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_id = self.kwargs.get('type_id')  # assuming you use <int:pk> in URL
        context['page'] = get_object_or_404(Page, type_id=page_id)
        return context
    def post(self, request, *args, **kwargs):
        title= request.POST.get("title")
        type_id = request.POST.get("type_id")
        description = request.POST.get("description")
        try:
            page = Page.objects.get(type_id=type_id)
            page.title = title
            page.description = description
            page.save()
            return redirect('cms')
        except Page.DoesNotExist:
        # Optional: handle error if no page found with given type_id
            return render(request, 'error.html', {'message': 'Page not found.'})
        except Page.MultipleObjectsReturned:
        # Optional: handle duplicates
            return render(request, 'error.html', {'message': 'Multiple pages found for the given type_id.'})




edit_page_view= EditPageView.as_view()
# def user_detail(request, user_id):
#     # Retrieve the user object or return a 404 error if not found
#     user = get_user_model()
#     user = get_object_or_404(user, id=user_id)

#     # Pass the user object to the template
#     return render(request, 'custom/extra-pages/user-detail.html', {'user': user})

def user_detail(request, user_id):
    # Retrieve the user object or return a 404 error if not found
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)

    # Construct the custom URL for the profile image
    file_name = user.profile_file.name if user.profile_file else None
    profile_image_url = f"https://cannabis.nexusappdevelopers.com/api/profile-file?file_path={file_name}" if file_name else None

    # Pass the user object and profile image URL to the template
    context = {
        'user': user,
        'profile_image_url': profile_image_url,
    }
    return render(request, 'custom/extra-pages/user-detail.html', context)


def page_detail(request, type):
    page = get_object_or_404(Page, type_id=type)
    print(page.description,"page page")
    context = {
        'page': page,
        'title': page.title,
        'description': page.description,
        # 'copyright_year': COPYRIGHT_YEAR,
        # 'company_name': COMPANY_NAME,
        'terms_type': PAGE_TYPE_TERMS_AND_CONDITIONS,
        'privacy_policy_type': PAGE_TYPE_PRIVACY_POLICY,
    }
    return render(request, 'partials/page.html', context)


def delete_user(request, user_id):
    user = get_user_model()
    user = get_object_or_404(user, id=user_id)
    # Assuming state_id = 2 means the user is deleted or deactivated
    user.state_id = 2
    user.save()
    messages.success(request, 'User has been successfully deleted.')
    return redirect('users')  # Redirect to the user list page



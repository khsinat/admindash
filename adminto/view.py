import logging
import base64
from decouple import config
from openai import OpenAI

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
from api.models import Page,PAGE_TYPE_TERMS_AND_CONDITIONS,PAGE_TYPE_PRIVACY_POLICY,Package,Analysis
from django.contrib.auth import get_user_model,update_session_auth_hash
from .forms import PageForm, ChangePasswordForm,PackageForm
from django.utils import timezone
from datetime import timedelta
from api.models import ContactUs
client = OpenAI(api_key=config('OPENAI_API'))


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
            users = get_user_model().objects.filter(is_superuser=False)  # Fetch all users
            total_users = users.count()  # Count the total number of users

            one_month_ago = timezone.now() - timedelta(days=30)
            # recent_users = get_user_model().objects.filter(created_at=one_month_ago)
            recent_users = get_user_model().objects.filter(created_at=one_month_ago, is_superuser=False)
            recent_user_count = recent_users.count()  # Count users registered in the last month     
            if total_users > 0:
                increment = recent_user_count  # Increment is the count of recent users
            else:
                increment = 0  # No users registered yet
            context["users"] = users
            context["total_users"] = total_users  # Add total users to context
            context["increment"] = increment  # Add increment to context
        except DatabaseError as e:
            db_logger.error(f"Database error occurred: {e}")  # Log error to file
            context["users"] = []  # Ensure template doesn't break
            context["total_users"] = 0  # Set total users to 0 in case of error
            context["increment"] = 0  # Set increment to 0 in case of error
            context["db_error"] = f"Database error: {str(e)}"  # Display error in template
        return context

# Serve dashboard at '/'
index_view = DashboardView.as_view()

class UsersView(TemplateView):

    template_name = "custom/extra-pages/user-list.html"


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        

        # Get all users

        User = get_user_model()

        # Filter users where is_superuser is not 1
        user_list = User.objects.filter(is_superuser=False)
        paginator = Paginator(user_list, 10)  # Show 10 users per page


        # Get the current page number from the request

        page_number = self.request.GET.get('page')

        users = paginator.get_page(page_number)


        # Add the paginated users to the context

        context['users'] = user_list

        context['paginator'] = paginator  # Optional: if you want to use paginator info in the template


        return context


# Create an instance of the view

users_view = UsersView.as_view()

class TotalGrowLogsView(TemplateView):

    template_name = "custom/extra-pages/total-grow-logs.html"
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # Get all users
        context['grow_logs']=Analysis.objects.all().order_by('-created_at')
        return context
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

class GrowLogView(TemplateView):
    template_name="custom/extra-pages/grow-log.html"
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        analysis_id=self.kwargs.get('analysis_id')
        analysis=get_object_or_404(Analysis,id=analysis_id)
        context['analysis']=analysis
        selected_user=User.objects.get(id=analysis.created_by_id)
        context['selected_user']=selected_user

        return context

grow_log_view=GrowLogView.as_view()
        
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
        context['packages'] = Package.objects.all().order_by('-created_on')  # or any ordering you prefer
        return context
    def post(self, request, *args, **kwargs):
        package_id = request.POST.get("delete_package_id")
        if package_id:
            package = get_object_or_404(Package, id=package_id)
            if request.user == package.created_by or request.user.is_staff:  # optional permission check
                package.delete()
        return redirect('packages')

packages_view= PackagesView.as_view()



class AddPackageView(TemplateView):
    template_name = "custom/extra-pages/add-package.html"
    def post(self, request, *args, **kwargs):
        form = PackageForm(request.POST)
        if form.is_valid():
            Package.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                created_by=request.user
            )
            messages.success(request, "Package created successfully.")
            return redirect('packages')

        else:
            messages.error(request, "Please correct the errors below.")
        return render(request, self.template_name, {'form': form})


add_package_view = AddPackageView.as_view()

class ViewPackageView(TemplateView):
    template_name = "custom/extra-pages/view-package.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_id = self.kwargs.get('id')  # assuming you use <int:pk> in URL
        context['package'] = get_object_or_404(Package, id=package_id)
        return context


view_package_view= ViewPackageView.as_view()

class EditPackageView(TemplateView):

    template_name = "custom/extra-pages/edit-package.html"
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       package_id = self.kwargs.get('package_id')  # assuming you use <int:pk> in URL
       context['package'] = get_object_or_404(Package, id=package_id)
       return context
   
    def post(self , request, *args, **kwargs):
        package_id=kwargs.get('package_id') 
        package_obj= get_object_or_404(Package,id=package_id)

        title=request.POST.get("title")
        description=request.POST.get("description")
        price=request.POST.get("price")

        if title:
            package_obj.title=title
        if description:
            package_obj.description=description
        if price:
            package_obj.price=price

        package_obj.save()
        return redirect('packages')
edit_package_view= EditPackageView.as_view()

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
        contact_us_list = ContactUs.objects.all()
        paginator = Paginator(contact_us_list, 10)  # Show 10 users per page
        # Get the current page number from the request
        page_number = self.request.GET.get('page')
        users = paginator.get_page(page_number)

        # Add the paginated users to the context
        context['users'] = contact_us_list
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
            page = get_object_or_404(Page, id=page_id)
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
        prompt =  request.POST.get("prompt"); 
        cannabis_file=request.FILES.get("cannabis_file")
        b64_image = base64.b64encode(cannabis_file.read()).decode("utf-8")

        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {"type": "input_image", "image_url": f"data:image/png;base64,{b64_image}"},
                    ],
                }
            ],
        )
        return redirect('myprofile')
edit_user_view= EditUserView.as_view()
class AddPageView(TemplateView):
    template_name = "custom/extra-pages/add-page.html"
    def post(self, request, *args, **kwargs):
        form = PageForm(request.POST)
        if form.is_valid():
            Page.objects.create(
                title=form.cleaned_data['title'],
                type_id=form.cleaned_data['type_id'],
                description=form.cleaned_data['description'],
                created_by=request.user

            )
            messages.success(request, "Page created successfully.")
            return redirect('cms')

        else:
            messages.error(request, "Please correct the errors below.")
        return render(request, self.template_name, {'form': form})


add_page_view = AddPageView.as_view()

class ViewPageView(TemplateView):
    template_name = "custom/extra-pages/view-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_id = self.kwargs.get('type_id')  # assuming you use <int:pk> in URL
        context['page'] = get_object_or_404(Page, id=page_id)
        return context


view_page_view= ViewPageView.as_view()


class EditPageView(TemplateView):
    template_name = "custom/extra-pages/edit-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_id = self.kwargs.get('page_id')  # Use 'page_id' instead of 'type_id'
        context['page'] = get_object_or_404(Page, id=page_id)
        context['form'] = PageForm(initial={
            'title': context['page'].title,
            'type_id': context['page'].type_id,
            'description': context['page'].description,
        })
        return context

    def post(self, request, *args, **kwargs):
        page_id = self.kwargs.get('page_id')  # Use 'page_id' instead of 'type_id'
        form = PageForm(request.POST, page_id=page_id)

        if form.is_valid():
            try:
                page_instance = Page.objects.get(id=page_id)
            except Page.DoesNotExist:
                return render(request, 'error.html', {'message': 'Page not found.'})

            # Check if another page with the submitted type_id already exists
            if Page.objects.exclude(id=page_id).filter(type_id=form.cleaned_data['type_id']).exists():
                # Add the error message to the form
                form.add_error('type_id', f"A page with type ID '{form.cleaned_data['type_id']}' already exists.")
                return render(request, self.template_name, {'page': page_instance, 'form': form})

            try:
                page_instance.title = form.cleaned_data['title']
                page_instance.description = form.cleaned_data['description']
                page_instance.type_id = form.cleaned_data['type_id']
                page_instance.save()
                messages.success(request, "Page updated successfully.")
                return redirect('cms')
            except Exception as e:
                # Consider logging the error for debugging
                return render(request, 'error.html', {'message': f'An error occurred: {e}'})
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, self.template_name, {'page': get_object_or_404(Page, id=page_id), 'form': form})

edit_page_view = EditPageView.as_view()
# def user_detail(request, user_id):
#     # Retrieve the user object or return a 404 error if not found
#     user = get_user_model()
#     user = get_object_or_404(user, id=user_id)

#     # Pass the user object to the template
#     return render(request, 'custom/extra-pages/user-detail.html', {'user': user})


class ChangePasswordView(TemplateView):

    template_name = "custom/extra-pages/change-password.html"


    def post(self, request, *args, **kwargs):

        form = ChangePasswordForm(request.POST)

        user = request.user


        if form.is_valid():

            new_password = form.cleaned_data['new_password']

            user.set_password(new_password)

            user.save()

            update_session_auth_hash(request, user)  # Keeps user logged in

            messages.success(request, "Password changed successfully.")

            logout(request)

            return redirect("admin_login")

        

        # If the form is not valid, render the form with errors

        return render(request, self.template_name, {'form': form})


change_password_view= ChangePasswordView.as_view()
def user_detail(request, user_id):
    # Retrieve the user object or return a 404 error if not found
    User = get_user_model()
    selected_user = get_object_or_404(User, id=user_id)

    # Construct the custom URL for the profile image
    file_name = selected_user.profile_file.name if selected_user.profile_file else None
    profile_image_url = f"https://cannabis.nexusappdevelopers.com/api/profile-file?file_path={file_name}" if file_name else None

    # Pass the user object and profile image URL to the template
    context = {
        'selected_user': selected_user,
        'profile_image_url': profile_image_url,
    }
    return render(request, 'custom/extra-pages/user-detail.html', context)

class GrowLogsHistoryView(TemplateView):
    template_name = "custom/extra-pages/grow-logs-history.html"
grow_logs_history_view = GrowLogsHistoryView.as_view()

class TransactionHistoryView(TemplateView):
    template_name = "custom/extra-pages/transaction-history.html"
transaction_history_view = TransactionHistoryView.as_view()

grow_logs_history_view = GrowLogsHistoryView.as_view()
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

class UploadView(TemplateView):
    template_name = "custom/extra-pages/upload.html"
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        prompt=request.POST.get("prompt")
        cannabis_file=request.FILES.get("cannabis_file")
        b64_image = base64.b64encode(cannabis_file.read()).decode("utf-8")
        file_type=request.POST.get("file_type")
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {"type": "input_image", "image_url": f"data:image/{file_type};base64,{b64_image}"},
                    ],
                }
            ],
        )
        request.session['result'] = response.output_text

            # Redirect after successful POST
        return redirect(request.path)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'result' in request.session:
            context['response'] = request.session.pop('result')  # remove after reading

        return self.render_to_response(context)






upload_view= UploadView.as_view()

def delete_user(request, user_id):
    user = get_user_model()
    user = get_object_or_404(user, id=user_id)
    # Assuming state_id = 2 means the user is deleted or deactivated
    user.state_id = 2
    user.save()
    messages.success(request, 'User has been successfully deleted.')
    return redirect('users')  # Redirect to the user list page


def inactivate_user(request, user_id):
    user = get_user_model()
    user = get_object_or_404(user, id=user_id)
    # Assuming state_id = 1 means the user is inactive 
    user.state_id = 1
    user.save()
    messages.success(request, 'User has been successfully inactivated.')
    print(user)
    return redirect('users')  # Redirect to the user list page

def activate_user(request, user_id):
    user = get_user_model()
    user = get_object_or_404(user, id=user_id)
    # Assuming state_id = 0 means the user is active
    user.state_id = 0
    user.save()
    messages.success(request, 'User has been successfully activated.')
    return redirect('users')  # Redirect to the user list page
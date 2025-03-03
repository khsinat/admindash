from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

class CustomView(TemplateView):
    pass
class UserListView(CustomView):
    template_name = "custom/extra-pages/user-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        print("Users:", users)  # Print users in the console
        context['users'] = users
        return context

#Auth Pages
login_view = CustomView.as_view(template_name="custom/auth-pages/login.html")
register_view = CustomView.as_view(template_name="custom/auth-pages/register.html")
recoverpw_view = CustomView.as_view(template_name="custom/auth-pages/recoverpw.html")
lock_screen_view = CustomView.as_view(template_name="custom/auth-pages/lock-screen.html")
confirm_mail_view = CustomView.as_view(template_name="custom/auth-pages/confirm-mail.html")
logout_view = CustomView.as_view(template_name="custom/auth-pages/logout.html")

#Extra Pages
starter_view = CustomView.as_view(template_name="custom/extra-pages/starter.html")
pricing_view = CustomView.as_view(template_name="custom/extra-pages/pricing.html")
timeline_view = CustomView.as_view(template_name="custom/extra-pages/timeline.html")
invoice_view = CustomView.as_view(template_name="custom/extra-pages/invoice.html")
faqs_view = CustomView.as_view(template_name="custom/extra-pages/faqs.html")
gallery_view = CustomView.as_view(template_name="custom/extra-pages/gallery.html")
error_404_view = CustomView.as_view(template_name="custom/extra-pages/error-400.html")
error_500_view = CustomView.as_view(template_name="custom/extra-pages/error-500.html")
maintenance_view = CustomView.as_view(template_name="custom/extra-pages/maintenance.html")
coming_soon_view = CustomView.as_view(template_name="custom/extra-pages/coming-soon.html")
userlistview = UserListView.as_view()  



from django.urls import path

from custom.views import (
      userlistview,
      login_view,
      register_view,
      recoverpw_view,
      lock_screen_view,
      confirm_mail_view,
      logout_view,
      starter_view,
      pricing_view,
      timeline_view,
      invoice_view,
      faqs_view,
      gallery_view,
      error_404_view,
      error_500_view,
      maintenance_view,
      coming_soon_view
)

urlpatterns = [

   #Auth Pages
   path("login",  view=login_view, name="login"),
   path("register",  view=register_view, name="register"),
   path("recoverpw",  view=recoverpw_view, name="recoverpw"),
   path("lock-screen",  view=lock_screen_view, name="lock-screen"),
   path("confirm-mail",  view=confirm_mail_view, name="confirm-mail"),
   path("logout",  view=logout_view, name="logout"),
  
   #Extra Pages
   path("starter",  view=starter_view, name="starter"),
   path("pricing",  view=pricing_view, name="pricing"),
   path("timeline",  view=timeline_view, name="timeline"),
   path("invoice",  view=invoice_view, name="invoice"),
   path("faqs",  view=faqs_view, name="faqs"),
   path("gallery",  view=gallery_view, name="gallery"),
   path("404",  view=error_404_view, name="404"),
   path("500",  view=error_500_view, name="500"),
   path("maintenance",  view=maintenance_view, name="maintenance"),
   path("coming-soon",  view=coming_soon_view, name="coming-soon"),
   path("userlist",  view=userlistview, name="userlist"),





]
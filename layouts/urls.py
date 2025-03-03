from django.urls import path
from layouts.views import layout_horizontal, layout_preloader

urlpatterns = [
    # Layouts
    path("horizontal", view=layout_horizontal, name="horizontal"),
    path("preloader", view=layout_preloader, name="preloader"),
]

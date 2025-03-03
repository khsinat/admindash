from django.views.generic.base import TemplateView

class LayoutView(TemplateView):
    pass

# Layouts
layout_horizontal = LayoutView.as_view(template_name="custom/layouts/layouts-horizontal.html")
layout_preloader = LayoutView.as_view(template_name="custom/layouts/layouts-preloader.html")
from django.views.generic.base import TemplateView

class ComponentsView(TemplateView):
    pass


#Base UI
buttons_view = ComponentsView.as_view(template_name="components/base-ui/buttons.html")
cards_view = ComponentsView.as_view(template_name="components/base-ui/cards.html")
avatars_view = ComponentsView.as_view(template_name="components/base-ui/avatars.html")
tabs_accordions_view = ComponentsView.as_view(template_name="components/base-ui/tabs-accordions.html")
modals_view = ComponentsView.as_view(template_name="components/base-ui/modals.html")
progress_view = ComponentsView.as_view(template_name="components/base-ui/progress.html")
notifications_view = ComponentsView.as_view(template_name="components/base-ui/notifications.html")
offcanvas_view = ComponentsView.as_view(template_name="components/base-ui/offcanvas.html")
placeholders_view = ComponentsView.as_view(template_name="components/base-ui/placeholders.html")
spinners_view = ComponentsView.as_view(template_name="components/base-ui/spinners.html")
images_view = ComponentsView.as_view(template_name="components/base-ui/images.html")
carousel_view = ComponentsView.as_view(template_name="components/base-ui/carousel.html")
video_view = ComponentsView.as_view(template_name="components/base-ui/video.html")
dropdowns_view = ComponentsView.as_view(template_name="components/base-ui/dropdowns.html")
tooltips_popovers_view = ComponentsView.as_view(template_name="components/base-ui/tooltips-popovers.html")
general_view = ComponentsView.as_view(template_name="components/base-ui/general.html")
typography_view = ComponentsView.as_view(template_name="components/base-ui/typography.html")
grid_view = ComponentsView.as_view(template_name="components/base-ui/grid.html")

#Widgets
widgets_view = ComponentsView.as_view(template_name="components/widgets/widgets.html")

#Extended-UI
range_slider_view = ComponentsView.as_view(template_name="components/extended-ui/range-slider.html")
sweet_alerts_view = ComponentsView.as_view(template_name="components/extended-ui/sweet-alerts.html")
draggable_cards_view = ComponentsView.as_view(template_name="components/extended-ui/draggable-cards.html")
tour_view = ComponentsView.as_view(template_name="components/extended-ui/tour.html")
notification_view = ComponentsView.as_view(template_name="components/extended-ui/notification.html")
treeview_view = ComponentsView.as_view(template_name="components/extended-ui/treeview.html")

#Icons
feather_view = ComponentsView.as_view(template_name="components/icons/feather.html")
mdi_view = ComponentsView.as_view(template_name="components/icons/mdi.html")
dripicons_view = ComponentsView.as_view(template_name="components/icons/dripicons.html")
font_awesome_view = ComponentsView.as_view(template_name="components/icons/font-awesome.html")
themify_view = ComponentsView.as_view(template_name="components/icons/themify.html")

#Forms
elements_view = ComponentsView.as_view(template_name="components/forms/elements.html")
advanced_view = ComponentsView.as_view(template_name="components/forms/advanced.html")
validation_view = ComponentsView.as_view(template_name="components/forms/validation.html")
wizard_view = ComponentsView.as_view(template_name="components/forms/wizard.html")
quilljs_view = ComponentsView.as_view(template_name="components/forms/quilljs.html")
pickers_view = ComponentsView.as_view(template_name="components/forms/pickers.html")
file_uploads_view = ComponentsView.as_view(template_name="components/forms/file-uploads.html")
x_editable_view = ComponentsView.as_view(template_name="components/forms/x-editable.html")

#Tables
basic_view = ComponentsView.as_view(template_name="components/tables/basic.html")
datatables_view = ComponentsView.as_view(template_name="components/tables/datatables.html")
editable_view = ComponentsView.as_view(template_name="components/tables/editable.html")
responsive_view = ComponentsView.as_view(template_name="components/tables/responsive.html")
tablesaw_view = ComponentsView.as_view(template_name="components/tables/tablesaw.html")

#Charts
flot_view = ComponentsView.as_view(template_name="components/charts/flot.html")
morris_view = ComponentsView.as_view(template_name="components/charts/morris.html")
chartjs_view = ComponentsView.as_view(template_name="components/charts/chartjs.html")
chartist_view = ComponentsView.as_view(template_name="components/charts/chartist.html")
sparklines_view = ComponentsView.as_view(template_name="components/charts/sparklines.html")

#Maps
google_view = ComponentsView.as_view(template_name="components/maps/google.html")
vector_view = ComponentsView.as_view(template_name="components/maps/vector.html")
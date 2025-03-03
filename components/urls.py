from django.urls import path
from components.views import (
    buttons_view,
    cards_view,
    avatars_view,
    tabs_accordions_view,
    modals_view,
    progress_view,
    notifications_view,
    offcanvas_view,
    placeholders_view,
    spinners_view,
    images_view,
    carousel_view,
    video_view,
    dropdowns_view, 
    tooltips_popovers_view,
    general_view,
    typography_view,
    grid_view,
    widgets_view,
    range_slider_view,
    sweet_alerts_view,
    draggable_cards_view,
    tour_view,
    notification_view,
    treeview_view,
    feather_view,
    mdi_view,
    dripicons_view,
    font_awesome_view,
    themify_view,
    elements_view,
    advanced_view,
    validation_view,
    wizard_view,
    quilljs_view,
    pickers_view,
    file_uploads_view,
    x_editable_view,
    basic_view,
    datatables_view,
    editable_view,
    responsive_view,
    tablesaw_view,
    flot_view,
    morris_view,
    chartjs_view,
    chartist_view,
    sparklines_view,
    google_view,
    vector_view
)

urlpatterns = [

    #Base UI
    path("buttons",  view=buttons_view, name="buttons"),
    path("cards",  view=cards_view, name="cards"),
    path("avatars",  view=avatars_view, name="avatars"),
    path("tabs-accordions", view=tabs_accordions_view, name="tabs-accordions"),
    path("modals", view=modals_view, name="modals"),
    path("progress", view=progress_view, name="progress"),
    path("notifications", view=notifications_view, name="notifications"),
    path("offcanvas", view=offcanvas_view, name="offcanvas"),
    path("placeholders", view=placeholders_view, name="placeholders"),
    path("spinners", view=spinners_view, name="spinners"),
    path("images", view=images_view, name="images"),
    path("carousel", view=carousel_view, name="carousel"),
    path("video", view=video_view, name="video"),
    path("dropdowns", view=dropdowns_view, name="dropdowns"),
    path("tooltips-popovers", view=tooltips_popovers_view, name="tooltips-popovers"),
    path("general", view=general_view, name="general"),
    path("typography", view=typography_view, name="typography"),
    path("grid", view=grid_view, name="grid"),

    #Widgets
    path("widgets", view=widgets_view, name="widgets"),

    #Extended UI
    path("range-slider", view=range_slider_view, name="range-slider"),
    path("sweet-alerts", view=sweet_alerts_view, name="sweet-alerts"),
    path("draggable-cards", view=draggable_cards_view, name="draggable-cards"),
    path("tour", view=tour_view, name="tour"),
    path("notification", view=notification_view, name="notification"),
    path("treeview", view=treeview_view, name="treeview"),

    #Icons
    path("feather", view=feather_view, name="feather"),
    path("mdi", view=mdi_view, name="mdi"),
    path("dripicons", view=dripicons_view, name="dripicons"),
    path("font-awesome", view=font_awesome_view, name="font-awesome"),
    path("themify", view=themify_view, name="themify"),

    
    #Forms
    path("elements", view=elements_view, name="elements"),
    path("advanced", view=advanced_view, name="advanced"),
    path("validation", view=validation_view, name="validation"),
    path("wizard", view=wizard_view, name="wizard"),
    path("quilljs", view=quilljs_view, name="quilljs"),
    path("pickers", view=pickers_view, name="pickers"),
    path("file-uploads", view=file_uploads_view, name="file-uploads"),
    path("x-editable", view=x_editable_view, name="x-editable"),

    #Tables
    path("basic", view=basic_view, name="basic"),
    path("datatables", view=datatables_view, name="datatables"),
    path("editable", view=editable_view, name="editable"),
    path("responsive", view=responsive_view, name="responsive"),
    path("tablesaw", view=tablesaw_view, name="tablesaw"),

    #Charts
    path("flot", view=flot_view, name="flot"),
    path("morris", view=morris_view, name="morris"),
    path("chartjs", view=chartjs_view, name="chartjs"),
    path("chartist", view=chartist_view, name="chartist"),
    path("sparklines", view=sparklines_view, name="sparklines"),

    #Maps
    path("google", view=google_view, name="google"),
    path("vector", view=vector_view, name="vector")


    
]
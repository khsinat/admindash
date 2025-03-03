from django.urls import path
from apps.views import (
    calendar_view,
    chat_view,
    inbox_view,
    templates_view,
    templates_action_view,
    templates_alert_view,
    templates_billing_view,
    kanban_board_view,
    details_view,
    projects_view,
    list_view,
    profile_view

) 

urlpatterns = [

    #Calendar
    path("calendar", view=calendar_view, name="calendar"),

    #Chat
    path("chat", view=chat_view, name="chat"),

    #Email
    path("inbox", view=inbox_view, name="inbox"),
    path("templates", view=templates_view, name="templates"),
    path("templates-action", view=templates_action_view, name="templates-action"),
    path("templates-alert", view=templates_alert_view, name="templates-alert"),
    path("templates-billing", view=templates_billing_view, name="templates-billing"),

    #Tasks
    path("kanban-board", view=kanban_board_view, name="kanban-board"),
    path("details", view=details_view, name="details"),

    #Project
    path("projects", view=projects_view, name="projects"),

    #Contacts
    path("list", view=list_view, name="list"),
    path("profile", view=profile_view, name="profile")


]

from django.views.generic.base import TemplateView

class AppsView(TemplateView):
    pass

#Calendar
calendar_view = AppsView.as_view(template_name="apps/calendar.html")

#Chat
chat_view = AppsView.as_view(template_name="apps/chat.html")

#Email
inbox_view = AppsView.as_view(template_name="apps/email/inbox.html")
templates_view = AppsView.as_view(template_name="apps/email/templates.html")
templates_action_view = AppsView.as_view(template_name="apps/email/templates-action.html")
templates_alert_view = AppsView.as_view(template_name="apps/email/templates-alert.html")
templates_billing_view = AppsView.as_view(template_name="apps/email/templates-billing.html")

#Tasks
kanban_board_view = AppsView.as_view(template_name="apps/tasks/kanban-board.html")
details_view = AppsView.as_view(template_name="apps/tasks/details.html")

#Projects
projects_view = AppsView.as_view(template_name="apps/projects.html")

#Contacts
list_view = AppsView.as_view(template_name="apps/contacts/list.html")
profile_view = AppsView.as_view(template_name="apps/contacts/profile.html")
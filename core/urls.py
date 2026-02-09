from django.contrib import admin
from django.urls import path
from messaging.views import MessageCreateView, InboxView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/messages/", MessageCreateView.as_view(), name="create-message"),
    path("api/messages/inbox/", InboxView.as_view(), name="inbox"),
]

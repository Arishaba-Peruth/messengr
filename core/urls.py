from django.urls import path
from messaging.views import MessageCreateView, InboxView

urlpatterns = [
 path("api/messages/", MessageCreateView.as_view()),
 path("api/messages/inbox/", InboxView.as_view()),
]

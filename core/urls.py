#Added missing imports and admin path for Django admin interface
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token 
from django.urls import path
from messaging.views import MessageCreateView, InboxView

#Added unique Identifiers for urls as a django best practice
urlpatterns = [
     path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path("admin/", admin.site.urls),
    path("api/messages/", MessageCreateView.as_view(), name="create-message"),
    path("api/messages/inbox/", InboxView.as_view(), name="inbox"),
]

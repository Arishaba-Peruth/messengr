from django.urls import path
from . import views

urlpatterns = [
    path('api/messages/', views.MessageCreateView.as_view(), name='message-create'),  
    path('api/messages/inbox/', views.InboxView.as_view(), name='message-list'),
    path('api/messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message-delete'),
]
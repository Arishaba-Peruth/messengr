from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.MessageCreateView.as_view(), name='message-create'),  
    path('messages/inbox/', views.InboxView.as_view(), name='message-list'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message-delete'),
]
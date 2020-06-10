from django.urls import path
from .views import (
    MessageListView,
    MessageSentListView,
    MessageDetailView,
    MessageCreateView,
#    PostUpdateView,
#    PostDeleteView,
)
from . import views

app_name = 'messaging'

urlpatterns = [
    path('messages/', MessageListView.as_view(), name='messaging'),
    path('messages/sent/', MessageSentListView.as_view(), name='sent-messages'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('message/new/', MessageCreateView.as_view(), name='message-create'),

    path('search/', views.search, name='search')
]

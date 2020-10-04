from django.urls import path

from .views import homePageView, sendView, sentMessagesView

urlpatterns = [
    path('', homePageView, name='home'),
    path('send/', sendView, name='send'),
    path('sentmessages/<str:username>/', sentMessagesView, name='sentmessages')
]

from django.urls import path

from .views import homePageView, sendView, sentMessagesView, receivedMessagesView, sloganView, adminPanelView, userList

urlpatterns = [
    path('', homePageView, name='home'),
    path('send/', sendView, name='send'),
    path('sentmessages/<str:username>/', sentMessagesView, name='sentmessages'),
    path('receivedmessages/<str:username>/', receivedMessagesView, name='receivedmessages'),
    path('slogan/', sloganView, name='slogan'),
    path('adminpanel/', adminPanelView, name='adminpanel'),
    path('debug/userlist/', userList, name='userlist')
]

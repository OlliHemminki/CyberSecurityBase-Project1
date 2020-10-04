from django.urls import path

from .views import homePageView, sendView, sentMessagesView, sloganView, adminPanelView

urlpatterns = [
    path('', homePageView, name='home'),
    path('send/', sendView, name='send'),
    path('sentmessages/<str:username>/', sentMessagesView, name='sentmessages'),
    path('slogan/', sloganView, name='slogan'),
    path('adminpanel/', adminPanelView, name='adminpanel')
]

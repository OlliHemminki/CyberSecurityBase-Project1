from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Message

@login_required
def sendView(request):

	sender = User.objects.get(username=request.user)
	receiver = User.objects.get(username=request.POST.get('receiver'))
	content = request.POST.get('content')

	newMessage = Message.objects.create(sender=sender, receiver=receiver, content=content)
	newMessage.save()

	return redirect('/')

@login_required
def homePageView(request):

	user = User.objects.get(username=request.user)

	users = User.objects.filter(is_staff = False).exclude(username = user.username)
	receivedMessages = Message.objects.filter(receiver=user)
	sentMessages = Message.objects.filter(sender=user)

	return render(request, 'pages/index.html', {'users':users, 'receivedMessages': receivedMessages})

@login_required
def sentMessagesView(request, username):
	
	if username != request.user.username: #jos tämän poistaa, toteutuu riski nro 5
		return redirect('/')

	user = User.objects.get(username=username)
	sentMessages = Message.objects.filter(sender=user)
	return render(request, 'pages/sentmessages.html', {'sentMessages':sentMessages})

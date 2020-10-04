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
	users = User.objects.all()

	print(type(users))

	receivedMessages = Message.objects.filter(receiver=user)
	sentMessages = Message.objects.filter(sender=user)

	return render(request, 'pages/index.html', {'users':users, 'receivedMessages': receivedMessages, 'sentMessages':sentMessages})
 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import connection, transaction
from .models import Message, Slogan

@login_required
def adminPanelView(request):

	user = User.objects.get(username=request.user)
	admins = User.objects.filter(is_staff = True)

	if user.is_staff:	
		return render(request, 'pages/adminpanel.html')
	else:
		return render(request, 'pages/error.html', {'admins':admins})

@login_required
def sendView(request):

	sender = User.objects.get(username=request.user)
	receiver = User.objects.get(username=request.POST.get('receiver'))
	content = request.POST.get('content')

	newMessage = Message.objects.create(sender=sender, receiver=receiver, content=content)
	newMessage.save()

	return redirect('/')

@login_required
def sloganView(request):

	user = User.objects.get(username=request.user)
	content = request.POST.get('content')

	try:
		userID = User.objects.get(username=request.user).id		
		cursor = connection.cursor()
		cursor.execute("UPDATE pages_slogan SET content='" + content + "' WHERE user_id='" + str(userID) + "'")
		transaction.set_dirty()        
		transaction.commit()
	except:
		slogan = Slogan.objects.create(user=user, content=content)
		slogan.save()

	return redirect('/')

@login_required
def homePageView(request):

	user = User.objects.get(username=request.user)

	users = User.objects.filter(is_staff = False).exclude(username = user.username)
	receivedMessages = Message.objects.filter(receiver=user)

	slogan = None

	try:
		userID = User.objects.get(username=request.user).id
		slogan = Slogan.objects.raw('SELECT * FROM pages_slogan WHERE user_id=' + str(userID))[0]
		slogan = slogan.content
	except:
		slogan = "No slogan set yet."

	return render(request, 'pages/index.html', {'users':users, 'receivedMessages':receivedMessages, 'slogan':slogan})

@login_required
def sentMessagesView(request, username):
	user = User.objects.get(username=username)
	sentMessages = Message.objects.filter(sender=user)
	return render(request, 'pages/sentmessages.html', {'sentMessages':sentMessages})

def receivedMessagesView(request, username):
	user = User.objects.get(username=username)
	receivedMessages = Message.objects.filter(receiver=user)
	return render(request, 'pages/receivedmessages.html', {'receivedMessages':receivedMessages})

def userList(request):
	users = list(User.objects.values())
	print(users)
	return JsonResponse(users, safe=False)
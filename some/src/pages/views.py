from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Message, Slogan

# Poistamalla index.html -sivulta jostain POST-pyynnöstä {% csrf_token %}
# sallitaan Cross-Site Scripting, eli saadaan mukaan riski nro 7

# Yksi selkeä puute sovelluksessa on lokituksen ja monitoroinnin totaalinen puuttuminen.
# Toisin sanoen mukana on riski nro 10.

@login_required
def adminPanelView(request):

	# Poistamalla koko oma adminpanel käytöstä ja siirtymällä Djangon 
	# tarjoamaan admin-sivuun saataisiin korjattua ongelma, tai poistamalla
	# lista admineista error-sivulta. Nykyisellään selvästi tuo riskin nro 6 mukaan.

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

	# Tämä voidaan muuttaa suoraksi SQL-muokkaukseksi,
	# jolloin mahdollistuu väärin implementoitaessa injektointimahdollisuus. 
	# Nyt tehty implementaatio varsin toimiva (menee modelin läpi).
	# Tällä saadaan hoidettua riski nro 1

	user = User.objects.get(username=request.user)
	content = request.POST.get('content')

	try:
		slogan = Slogan.objects.get(user=user)
		slogan.content = content
		slogan.save()
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
		slogan = Slogan.objects.get(user=user).content
	except:
		slogan = "No slogan set yet."

	return render(request, 'pages/index.html', {'users':users, 'receivedMessages':receivedMessages, 'slogan':slogan})

@login_required
def sentMessagesView(request, username):
	
	if username != request.user.username: #jos tämän poistaa, toteutuu riski nro 5
		return redirect('/')

	user = User.objects.get(username=username)
	sentMessages = Message.objects.filter(sender=user)
	return render(request, 'pages/sentmessages.html', {'sentMessages':sentMessages})

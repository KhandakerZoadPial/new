from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import msg

# Create your views here.

def home(request):
	return render(request,"home.html")


def login(request):
	if request.method== 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user= auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('profile')
		else:
			messages.info(request,'Wrong Password or User name!')
			return redirect('login')

	else:
		u =request.user
		if u.is_authenticated:
			return redirect('profile')
		else:
			return render(request,'login.html')



def register(request):
	if request.method == 'POST' :
		first_name=request.POST['fname']
		last_name=request.POST['lname']
		username=request.POST['username']
		email=request.POST['email']
		password1=request.POST['password1']
		password2=request.POST['password2']

		if password1==password2 :
			if User.objects.filter(username=username).exists():
				messages.info(request,'User Name Taken')
				return redirect('register')
			elif User.objects.filter(email=email).exists():
				messages.info(request,'Email Taken')
				return redirect('register')
			else:	
			    user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
			    user.save();
			    return redirect('login')
		else:
		 	messages.info(request,'Password did not match')
		 	return redirect('register')
		return redirect('/')
	else:
		return render(request,"register.html")


def profile(request):
	user = request.user
	name = user.username
	if user.is_authenticated :
		x = msg.objects.filter(user_name=name)
		return render(request,"profile.html",{"posts":x})
	else:
		return redirect('login')


def logout(request):
	auth.logout(request)
	return redirect('/')


def search(request):
	if request.method == 'POST':
		temp=request.POST['search']
		xs = User.objects.filter(username__contains=temp)
		c=xs.count()
		if c>0:
			return render(request,"search.html",{"xs":xs})
		else:
			messages.info(request,'No such user found!')
			return render(request,"search.html",{"xs":xs})
	else:
		return render(request,"search.html",{"xs":None})
	
		



def post(request,username):
	x = User.objects.filter(username=username).exists()
	if request.method=='POST':
		des=request.POST['des']
		x=msg(user_name=username,description=des)
		x.save()
		messages.info(request,'Message was posted!')
		return render(request,"post.html",{"xs":username})
	else:
		u = request.user
		temp=request.user.username
		if u.is_authenticated:
			if temp==username:
				messages.info(request,'You can not post in your own profile!')
				return redirect('profile')
			else:
				return render(request,"post.html",{"xs":username})
		else:
			return render(request,"post.html",{"xs":username})
		

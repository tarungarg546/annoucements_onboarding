from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserRegistrationForm
from .models import Announcements

# Create your views here.


def home(request):
    user_id = request.user.id

    current_user_groups = User.objects.filter(id=user_id)[0].groups.all()
    valid_announcements = Announcements.objects.filter(groups__in=current_user_groups)\
        .exclude(sent_at=None).filter(has_expired=False)

    context = {
        'user_id': user_id,
        'valid_announcements': valid_announcements
               }
    return render(request, 'announcements/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')

    else:
        form = UserRegistrationForm()

    return render(request, 'announcements/register.html', {'form' : form})
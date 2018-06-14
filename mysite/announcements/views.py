from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from .forms import UserRegistrationForm
from .models import Announcements, Status
from django.contrib.auth.decorators import login_required
from .serializers import StatusSerializer
from rest_framework import generics


class ListStatusView(generics.RetrieveUpdateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


@login_required(login_url='/login')
def home(request):
    user_id = request.user.id

    current_user_groups = User.objects.filter(id=user_id)[0].groups.all()
    valid_announcements = Announcements.objects\
        .filter(sent_at__isnull=False, has_expired=False,groups__in=current_user_groups)

    context = {
        'user_id': user_id,
        'valid_announcements': valid_announcements
               }
    return render(request, 'announcements/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_obj = form.cleaned_data
            username = user_obj['username']
            email = user_obj['email']
            password = user_obj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')
            else:
                raise forms.ValidationError('Looks like a username with that username or email already exists')

    else:
        form = UserRegistrationForm()

    return render(request, 'announcements/register.html', {'form': form})

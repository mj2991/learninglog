from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register(request):
    """Register a new user"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.data)
        form.is_valid()
        new_user = form.save()
        #log in new user
        login(request, new_user)
        return redirect('learning_logs:index')
    context = {'form':form}
    return render(request, "registration/register.html", context)    
        
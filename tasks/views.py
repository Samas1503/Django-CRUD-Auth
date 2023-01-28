from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone

from .forms import TaskForm
from .models import Task

# Create your views here.
def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request,'Auth/signup.html',{
            'form':UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #register user
                user = User.objects.create_user(request.POST['username'],request.POST['password1'])
                user.set_password(request.POST['password2'])
                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                return render(request,'Auth/signup.html',{
                    'form':UserCreationForm,
                    'error':'User already exists'
                })
        else:
            return render(request,'Auth/signup.html',{
                'form':UserCreationForm,
                'error':'Password do not match'
            })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request,'Auth/signin.html',{
            'form': AuthenticationForm
        })
    else:
        usuario = request.POST['username']
        contrasenia = request.POST['password']
        print(usuario, contrasenia)
        print(authenticate(request, username=usuario, password=contrasenia))
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'Auth/signin.html',{
                'form': AuthenticationForm,
                'error': 'Username or Password is Incorrect'
            })
        else:
            login(request,user)
            return redirect('tasks')

@login_required  
def tasks(request):
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'Task/tasks.html',{
        'tasks' : tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'Task/tasks.html',{
        'tasks' : tasks,
        'esconder':True
    })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request,'Task/create_task.html',{
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'Task/create_task.html',{
                'form': TaskForm,
                'error':'Please provide valid data'
            })

@login_required
def delete_task(request,task_id):
    if request.method=='POST':
        task = Task.objects.filter(user=request.user,id=task_id)
        task.delete()
    return redirect('tasks')

@login_required
def complete_task(request,task_id):
    if request.method=='POST':
        task = get_object_or_404(Task,pk=task_id, user = request.user)
        task.datecompleted = timezone.now()
        task.save()
    return redirect('tasks')

@login_required 
def task_detail(request,task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task,id=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request,'Task/task_detail.html',{
            'task':task,
            'form':form
        })
    else:
        try:
            task = get_object_or_404(Task,id=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'Task/task_detail.html',{
                'task':task,
                'form':form,
                'error':'Error updating task'
            })
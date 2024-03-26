from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from user.forms import RegisterForm, LoginForm, PostForm
from django.contrib.auth import  login, logout
from user.utils.authenticate import authenticate_by_email
from django.contrib import messages

# Create your views here.

def register(request):
    form = RegisterForm()
    return render(request,'register.html',context={'form':form})

def create_register(request):
    form = RegisterForm(request.POST, request.FILES)
    if form.is_valid():
        user = form.save(commit=False) #salva os dados mas ainda não manda para o banco de dados
        user.set_password(user.password)
        user.photo = request.FILES['image']
        user.save()
        return redirect('login')
    else:
        return render(request, 'register.html', {'form': form})
    
def login_view(request):
    print('ola')
    form = LoginForm()
    return render(request,'login.html',context={'form':form})





def create_login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate_by_email(form.cleaned_data.get('email',''),
                                     form.cleaned_data.get('password'))

        if user is not None:
            login(request,user)
            messages.success(request,'login feito com sucesso')
            return redirect('home')

        elif user is None:
            messages.error(request,'Invalid credentials')

    return redirect('login')


def post(request):
    form = PostForm()
    return render(request,'create-post.html',context={'form':form})

def create_post(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
    else:
        print(form.errors)
    return redirect('home')


@login_required(login_url='register', redirect_field_name='next')
def logout_view(request):
    if request.GET:
        return redirect('login')

    logout(request)
    messages.success(request,'logout feito com sucesso')
    return redirect('home')

def profile(request):
    user = request.user
    
    return render(request, 'profile.html',context={'user':user})


def home(request):
    return render(request, 'home.html')


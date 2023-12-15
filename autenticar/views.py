from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth


def cadastro(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        if len(username.strip()) == 0 or len(username.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/auth/cadastro')
        
        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse nome cadastrado')
            return redirect('/auth/cadastro')
        
        try:
            user = User.objects.create_user(username=username, password=senha)
            user.save()
            messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
            return redirect('/auth/login')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro')
        

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
            return redirect('/auth/login')
        else:
            auth.login(request, usuario)
            return redirect('/')
        

def sair(request):
    auth.logout(request)
    return redirect('/auth/login')

from django.contrib.messages import constants
from django.contrib import messages
import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Função de Validação de Senha
def validar_senha(senha, confirmar_senha):
    if senha != confirmar_senha:
        return 'As senhas não coincidem'
    if len(senha.strip()) < 6:
        return 'Sua senha deve ter 6 ou mais caracteres'
    if not re.search(r'[^A-Za-z0-9]', senha):
        return 'Sua senha deve conter pelo menos 1 caractere especial'
    return None

# Cadastro de Usuário
def cadastro(request):
    if request.method == "GET":
        return render(request, 'acesso.html')
    else:
        nome = request.POST.get('nome')
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Validar senha
        mensagem = validar_senha(senha, confirmar_senha)
        if mensagem:
            messages.add_message(request, constants.ERROR, mensagem)
            return redirect('/usuarios/cadastro')

        # Verificar se o nome de usuário já existe
        if User.objects.filter(username=usuario).exists():
            messages.add_message(request, constants.ERROR, 'Nome de usuário já existe.')
            return redirect('/usuarios/cadastro')

        try:
            # Criar o usuário
            user = User.objects.create_user(first_name=nome, username=usuario, email=email, password=senha)
            user.save()
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso')
            return redirect('/usuarios/logar')
        except Exception as e:
            messages.add_message(request, constants.ERROR, f'Erro interno do sistema, contate um administrador: {str(e)}')
            return redirect('/usuarios/cadastro')

# Login do Usuário
def logar(request):
    if request.method == "GET":
        return render(request, 'acesso.html')
    else:
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        # Autenticar o usuário
        user = authenticate(username=usuario, password=senha)

        if user is not None:
            login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Usuário logado com sucesso.')
        if user is not None:
            login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Usuário logado com sucesso.')
            return redirect( '/salas')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return redirect('/usuarios/logar')

# Logout do Usuário
@login_required(login_url='/usuarios/logar')
def sair(request):
    logout(request)
    return redirect('/usuarios/logar')  # Redirecionando para a página de login após logout

# Alteração de Senha
@login_required(login_url='/usuarios/logar')
def trocar(request):
    if request.method == "GET":
        return render(request, 'trocarsenha.html')
    
    elif request.method == "POST":
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Validar senha
        mensagem = validar_senha(senha, confirmar_senha)
        if mensagem:
            messages.add_message(request, constants.ERROR, mensagem)
            return redirect('/usuarios/trocar')

        try:
            # Alterar a senha do usuário logado
            user = request.user
            user.set_password(senha)
            user.save()
            login(request, user)  # Reautenticar o usuário após alterar a senha
            messages.add_message(request, constants.SUCCESS, 'Senha alterada com sucesso')
            return redirect('/salas')
        except Exception as e:
            messages.add_message(request, constants.ERROR, f'Erro ao alterar a senha. Tente novamente ou contate um administrador')
            return redirect('/usuarios/trocar')

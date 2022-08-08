from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'contas/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.add_message(request, messages.ERROR, 'Usuário ou senhas inválidos')
        return render(request, 'contas/login.html')
    else:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Login realizado com sucesso')
        return render(request, 'contas/dashboard.html')

    return render(request, 'contas/login.html')


def register(request):
    if request.method != 'POST':
        return render(request, 'contas/register.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.add_message(request, messages.ERROR, 'Nenhum campo deve estar vazio')
        return render(request, 'contas/register.html')

    if len(senha) < 8:
        messages.add_message(request, messages.ERROR, 'Senha muito curta, insira mais que 7 caracteres')
        return render(request, 'contas/register.html')

    if senha != senha2:
        messages.add_message(request, messages.ERROR, 'Senhas não correspondentes')

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR, 'E-Mail inserido inválido')
        return render(request, 'contas/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.ERROR, 'Usuário já existe')
        return render(request, 'contas/register.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, 'E-Mail já está cadastrado')
        return render(request, 'contas/register.html')

    messages.add_message(request, messages.SUCCESS, 'Preencha os campos com os dados cadastrados')

    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()

    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'post':
        form = FormContato()
        return render(request, 'contas/dashboard.html', {'form': form})

    form = FormContato(request.POST)

    if not form.is_valid():
        messages.add_message(messages.ERROR, 'erro ao enviar formulário')
        form = FormContato()
        return render(request, 'contas/dashboard.html', {'form': form})

    form.save()
    messages.add_message(messages.SUCCESS, f'Contato {request.POST.get("nome")} adicionado')
    return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')

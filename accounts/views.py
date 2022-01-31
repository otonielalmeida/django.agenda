from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import FormContato

def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.add_message(request, messages.ERROR, 'Usuario ou senha invalidos')
        return render(request, 'accounts/login.html')
    if user:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Login efetuado com sucesso!')
        return redirect('dashboard')

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout efetuado com sucesso!')
    return redirect('dashboard')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or \
            not usuario or not senha or not senha2:
        messages.add_message(request, messages.ERROR, 'Todos os campos sao obrigatorios')
        return render(request, 'accounts/register.html')


    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR, 'Email invalido')
        return render(request, 'accounts/register.html')

    if len(senha) < 6:
        messages.add_message(request, messages.ERROR,
                             'Senha muito curta. Minimo de 6 caracteres necessarios')
        return render(request, 'accounts/register.html')

    if len(usuario) < 4:
        messages.add_message(request, messages.ERROR,
                             'Usuario muito curto. Minimo de 4 caracteres necessarios')
        return render(request, 'accounts/register.html')

    if senha != senha2:
        messages.add_message(request, messages.ERROR, 'Senhas nao conferem')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.ERROR, 'Usuario ja em uso')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, 'Email ja em uso')
        return render(request, 'accounts/register.html')

    messages.add_message(request, messages.SUCCESS, 'Cadastro realizado com sucesso!')

    user = User.objects.create_user(username=usuario,
                                    email=email, password=senha,
                                    first_name=nome, last_name=sobrenome)

    user.save()
    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})
    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.add_message(request, messages.ERROR, 'Erro ocorrido!')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.add_message(request, messages.ERROR, 'Descricao '
                                      'precisa de mais de 5 caracteres')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})
    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} '
                              f'salvo com sucesso')
    return redirect('dashboard')
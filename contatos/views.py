from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from . models import Contato
from django.http import Http404
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages

@login_required(redirect_field_name='login')
def index(request):

    contatos = Contato.objects.order_by('-id').filter(
        visivel=True
    )
    paginator = Paginator(contatos, 10)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/index.html', {
        'contatos' : contatos
    })

def ver_contato(request, contato_id):
    #contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)

    if not contato.visivel:
        raise Http404()
    return render(request, 'contatos/ver_contato.html', {
        'contato' : contato
    })

def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        messages.add_message(
            request,
            messages.ERROR,
            'Campo termo nao pode ficar vazio'
        )
        return redirect('index')
    else:
        messages.add_message(
        request,
        messages.SUCCESS,
        'Busca realizada com sucesso!'
    )
    campos = Concat('nome', Value(' '), 'sobrenome', 'telefone')

    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        nome_completo__icontains=termo
    )

    print(contatos.query)
    paginator = Paginator(contatos, 10)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })
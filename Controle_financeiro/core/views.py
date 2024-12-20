from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Entrada, Categoria

from django.db.models import Count
from django.db.models.functions import TruncMonth

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Sum, F, Q
from django.http import JsonResponse
from django.utils import timezone

from datetime import datetime, timedelta

import calendar



def sign_up(request):
    if request.method == 'GET':
        return render(request, 'auth/sign_up.html')
    
    # Verificar se é POST
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    # Validar se as senhas coincidem
    if password != confirm_password:
        messages.warning(request, "As senhas nao coincidem!")
        return render (request, "auth/sign_up.html")
    

    # Verificar se o nome de usuário já existe
    if User.objects.filter(username=username).exists():
        messages.warning(request, "Nome de usuario já existe!")
        return render (request, "auth/sign_up.html")

    # Verificar se o e-mail já foi usado
    if User.objects.filter(email=email).exists():
        messages.warning(request, "Email já cadastrado!")
        return render (request, "auth/sign_up.html")

    # Criar o usuário com senha criptografada
    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password)  # Criptografa a senha
    )

    messages.success(request, "Conta criada com sucesso!")
    return render (request, "auth/sign_in.html")

def sign_in(request):
    if request.method == "GET":
        return render(request, 'auth/sign_in.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            messages.success(request, "Login efetuado com sucesso!")
            login(request, user)
            return redirect("dashboard")
        else:
            messages.warning(request, "Usuário ou senha incorretos!")
            return render (request, "auth/sign_in.html")

def sign_out(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta com sucesso")
    return redirect('sign_in')
@login_required(login_url= "/sign_in")
def usuario_detalhes(request):
        return render(request, 'usuario/usuario_details.html')

@login_required(login_url="/sign_in")
def dashboard(request):
    # Obter todas as entradas do usuário logado
    entradas = Entrada.objects.filter(usuario=request.user).order_by('-data_operacao')

    # Obter categorias, anos e meses únicos
    categorias = Categoria.objects.filter(usuario=request.user)
    anos = entradas.dates('data_operacao', 'year', order='DESC')
    meses = entradas.dates('data_operacao', 'month', order='DESC')

    # Filtros
    categoria_selecionada = request.GET.get('categoria', 'Todas')
    ano_selecionado = request.GET.get('ano', 'Todos')
    mes_selecionado = request.GET.get('mes', 'Todos')

    # Filtrar por categoria
    if categoria_selecionada != 'Todas':
        entradas = entradas.filter(categoria_id=categoria_selecionada)

    # Filtrar por ano
    if ano_selecionado != 'Todos':
        entradas = entradas.filter(data_operacao__year=ano_selecionado)

    # Filtrar por mês
    if mes_selecionado != 'Todos':
        entradas = entradas.filter(data_operacao__month=mes_selecionado)
    
    # Ordenar novamente após os filtros
    entradas = entradas.order_by('-data_operacao')

    ganhos_totais = entradas.filter(valor__gt=0).aggregate(total=Sum('valor'))['total'] or 0
    gastos_totais = entradas.filter(valor__lt=0).aggregate(total=Sum('valor'))['total'] or 0
    saldo_total = entradas.aggregate(total=Sum('valor'))['total'] or 0 

    return render(request, 'entrada/dashboard.html', {
        'entradas': entradas,
        'categorias': categorias,
        'anos': anos,
        'meses': meses,
        'categoria_selecionada': categoria_selecionada,
        'ano_selecionado': ano_selecionado,
        'mes_selecionado': mes_selecionado,
        'ganhos_totais': ganhos_totais,
        'gastos_totais': gastos_totais,
        'saldo_total': saldo_total, 
    })

def index(request):
    return redirect('home') 
  
def home(request):
    return render(request, 'home.html')

def test(request):
    return render(request, 'infos/test.html')

def about(request):
    return render(request, 'infos/about.html')


def privacy_policy(request):
    return render(request, 'infos/privacy_policy.html')

def terms(request):
    return render(request, 'infos/terms.html')



@login_required(login_url='/sign_in')  
def estatisticas(request): 
    
    entradas = Entrada.objects.filter(usuario=request.user)
    hoje = timezone.now()
    ultimo_ano = hoje - timedelta(days=365)
    ultimo_mes = hoje - timedelta(days=30)
    ano_atual = hoje.year
    mes_atual = hoje.month



    ganhos_totais = entradas.filter(valor__gt=0).aggregate(total=Sum('valor'))['total'] or 0
    gastos_totais = entradas.filter(valor__lt=0).aggregate(total=Sum('valor'))['total'] or 0


    ganhos_totais_ano = entradas.filter(data_operacao__year=hoje.year, valor__gt=0).aggregate(total=Sum('valor'))['total'] or 0
    ganhos_totais_mes = entradas.filter(data_operacao__year=hoje.year, data_operacao__month=hoje.month, valor__gt=0).aggregate(total=Sum('valor'))['total'] or 0
    ganhos_totais_last_365 = entradas.filter(data_operacao__gte=ultimo_ano, valor__gt=0).aggregate(total=Sum('valor'))['total'] or 0
    ganhos_totais_last_30 = entradas.filter(data_operacao__gte=ultimo_mes, valor__gt=0).aggregate(total=Sum('valor'))['total'] or 0
    
    gastos_totais_ano = entradas.filter(data_operacao__gte=ultimo_ano, valor__lt=0).aggregate(total=Sum('valor'))['total'] or 0
    gastos_totais_mes = entradas.filter(data_operacao__gte=ultimo_mes, valor__lt=0).aggregate(total=Sum('valor'))['total'] or 0
    gastos_totais_last_365 = entradas.filter(data_operacao__gte=ultimo_ano, valor__lt=0).aggregate(total=Sum('valor'))['total'] or 0
    gastos_totais_last_30 = entradas.filter(data_operacao__gte=ultimo_mes, valor__lt=0).aggregate(total=Sum('valor'))['total'] or 0

    # Soma todas as entradas positivas e negativas dos últimos 30 dias.
    saldo_last_30 = entradas.filter(data_operacao__gte=ultimo_mes).aggregate(total=Sum('valor'))['total'] or 0
    saldo_last_365 = entradas.filter(data_operacao__gte=ultimo_ano).aggregate(total=Sum('valor'))['total'] or 0
    saldo_last_mes = entradas.filter(data_operacao__year=hoje.year, data_operacao__month=hoje.month).aggregate(total=Sum('valor'))['total'] or 0
    saldo_last_ano = entradas.filter(data_operacao__year=hoje.year).aggregate(total=Sum('valor'))['total'] or 0
    saldo_total = entradas.aggregate(total=Sum('valor'))['total'] or 0 

     # Filtra as categorias relacionadas ao usuário logado e calcula os totais por categoria
    # Filtra as categorias relacionadas ao usuário logado e calcula os totais por categoria
    categorias = Categoria.objects.filter(usuario=request.user).annotate(
        # Calcula os gastos no ano (valores negativos para gastos)
        gastos_ano=Sum('entrada__valor', filter=Q(entrada__valor__lt=0) & Q(entrada__data_operacao__year=ano_atual)),  # Gastos no ano
        gastos_mes=Sum('entrada__valor', filter=Q(entrada__valor__lt=0) & Q(entrada__data_operacao__month=mes_atual)),  # Gastos no mês
        gastos_365=Sum('entrada__valor', filter=Q(entrada__valor__lt=0) & Q(entrada__data_operacao__gte=ultimo_ano) & Q(entrada__data_operacao__lte=hoje)),  # Gastos nos últimos 365 dias
        gastos_30=Sum('entrada__valor', filter=Q(entrada__valor__lt=0) & Q(entrada__data_operacao__gte=ultimo_mes)),  # Gastos nos últimos 30 dias
        
        # Calcula os ganhos no ano (valores positivos para ganhos)
        ganhos_ano=Sum('entrada__valor', filter=Q(entrada__valor__gt=0) & Q(entrada__data_operacao__year=ano_atual)),  # Ganhos no ano
        ganhos_mes=Sum('entrada__valor', filter=Q(entrada__valor__gt=0) & Q(entrada__data_operacao__month=mes_atual)),  # Ganhos no mês
        ganhos_365=Sum('entrada__valor', filter=Q(entrada__valor__gt=0) & Q(entrada__data_operacao__gte=ultimo_ano) & Q(entrada__data_operacao__lte=hoje)),  # Ganhos nos últimos 365 dias
        ganhos_30=Sum('entrada__valor', filter=Q(entrada__valor__gt=0) & Q(entrada__data_operacao__gte=ultimo_mes)),  # Ganhos nos últimos 30 dias
    )

    
    ano_atual = datetime.now().year
    mes_atual = datetime.now().month
    context = {
        'ganhos_totais_ano': ganhos_totais_ano,  
        'ganhos_totais_mes': ganhos_totais_mes,  
        'ganhos_totais_last_365': ganhos_totais_last_365,  
        'ganhos_totais_last_30': ganhos_totais_last_30,  
        'gastos_totais_ano': gastos_totais_ano, 
        'gastos_totais_mes': gastos_totais_mes, 
        'gastos_totais_last_365': gastos_totais_last_365,  
        'gastos_totais_last_30': gastos_totais_last_30,  
        'saldo_last_30': saldo_last_30,  
        'saldo_last_365': saldo_last_365,  
        'saldo_last_mes': saldo_last_mes,  
        'saldo_last_ano': saldo_last_ano,
        'saldo_total': saldo_total, 
        'categorias': categorias,
        'ano_atual': ano_atual,
        'mes_atual': mes_atual,
        'ganhos_totais' : ganhos_totais,
        'gastos_totais' : gastos_totais,
    }

    return render(request, 'entrada/estatisticas.html', context)


@login_required(login_url='/sign_in')
def criar_entrada(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        valor = float(request.POST.get('valor'))  # Converte valor para float
        tipo = request.POST.get('tipo')  # Entrada ou Saída
        data_operacao = request.POST.get('data_operacao')
        categoria_id = request.POST.get('categoria')
        nova_categoria_nome = request.POST.get('nova_categoria')
        descricao = request.POST.get('descricao', '')

        # Ajusta o valor se for uma "Saída"
        if tipo == 'saida' and valor > 0:
            valor = -valor

        # Verifica se o usuário selecionou a opção "Nova Categoria"
        if categoria_id == 'nova' and nova_categoria_nome:
            # Cria uma nova categoria associada ao usuário
            categoria, created = Categoria.objects.get_or_create(
                nome=nova_categoria_nome,
                usuario=request.user
            )
        else:
            # Obtém a categoria existente
            categoria = get_object_or_404(Categoria, id=categoria_id, usuario=request.user)

        # Cria a nova entrada
        Entrada.objects.create(
            usuario=request.user,
            nome=nome,
            valor=valor,
            data_operacao=data_operacao,
            categoria=categoria,
            descricao=descricao
        )

        messages.success(request, "Entrada criada com sucesso!")
        return redirect('dashboard')

    # Carrega as categorias existentes para o formulário
    categorias = Categoria.objects.filter(usuario=request.user)
    return render(request, 'entrada/entrada_form.html', {'categorias': categorias})
# Editar Entrada
@login_required(login_url='/sign_in')
def editar_entrada(request, entrada_id):
    entrada = get_object_or_404(Entrada, id=entrada_id, usuario=request.user)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        valor = float(request.POST.get('valor'))
        tipo = request.POST.get('tipo')  # Entrada ou Saída
        data_operacao = request.POST.get('data_operacao')
        categoria_id = request.POST.get('categoria')
        descricao = request.POST.get('descricao', '')

        # Ajusta o valor baseado no tipo
        if tipo == 'saida' and valor > 0:
            valor = -valor  # Torna negativo para saída
        elif tipo == 'entrada' and valor < 0:
            valor = abs(valor)  # Torna positivo para entrada

        # Atualiza os dados da entrada
        entrada.nome = nome
        entrada.valor = valor
        entrada.data_operacao = data_operacao
        entrada.categoria = get_object_or_404(Categoria, id=categoria_id, usuario=request.user)
        entrada.descricao = descricao
        entrada.save()

        messages.success(request, "Entrada atualizada com sucesso!")
        return redirect('entrada_detalhes', entrada_id=entrada.id)

    # Determina o tipo baseado no sinal do valor
    tipo = 'saida' if entrada.valor < 0 else 'entrada'
    categorias = Categoria.objects.filter(usuario=request.user)

    return render(request, 'entrada/entrada_edit.html', {
        'entrada': entrada,
        'categorias': categorias,
        'tipo': tipo,
        'valor_absoluto': abs(entrada.valor)  # Garante que o valor exibido seja positivo
    })

@login_required(login_url='/sign_in')
def entrada_detalhes(request, entrada_id):
    entrada = get_object_or_404(Entrada, id=entrada_id, usuario=request.user)

    return render(request, 'entrada/entrada_detalhes.html', {
        'entrada': entrada,
        'valor_absoluto': abs(entrada.valor),  # Garante que o valor exibido seja positivo
    })

@login_required(login_url='/sign_in')
def confirmar_exclusao(request, entrada_id):
    entrada = get_object_or_404(Entrada, id=entrada_id, usuario=request.user)
    return render(request, 'entrada/entrada_confirm_delete.html', {'entrada': entrada})
                  
# Excluir Entrada
@login_required(login_url='/sign_in')
def excluir_entrada(request, entrada_id):
    entrada = get_object_or_404(Entrada, id=entrada_id, usuario=request.user)
    if request.method == 'POST':
        entrada.delete()
        messages.success(request, "Entrada excluída com sucesso!")
        return redirect('dashboard')

    return render(request, 'entrada/entrada_confirm_delete.html', {'entrada': entrada})

@login_required(login_url="/sign_in")
def editar_usuario(request):
    if request.method == "POST":
        user = request.user
        username = request.POST.get("username")
        email = request.POST.get("email")
        
        # Atualiza os dados do usuário
        user.username = username
        user.email = email
        user.save()

        messages.success(request, "Usuário atualizado com sucesso!")
        return redirect("usuario_detalhes")  # Nome da URL para detalhes do usuário

    return render(request, "usuario/usuario_edit.html")

@login_required(login_url="/sign_in")
def soft_delete_usuario(request):
    user = request.user
    if request.method == "POST":
        # Desmarca o usuário como ativo (soft delete)
        user.is_active = False
        user.save()

        messages.success(request, "Sua conta foi desativada com sucesso!")
        return redirect("sign_in")  # Redireciona para a página de login

    return render(request, "usuario/soft_delete_usuario.html")
# Create your views here.

@login_required(login_url="/sign_in")
def buscar_graficos(request):
    anos = Entrada.objects.values_list('data_operacao__year', flat=True).distinct()  # Lista de anos disponíveis
    meses = list(range(1, 13))  # Lista fixa de meses (1 a 12)
    dados_ano = []
    dados_mes = []

    ano_escolhido = None
    mes_escolhido = None

    if request.method == 'GET' and 'ano' in request.GET and 'mes' in request.GET:
        ano_escolhido = int(request.GET.get('ano'))
        mes_escolhido = int(request.GET.get('mes'))

        # Dados para o gráfico do ano
        dados_ano_raw = (
            Entrada.objects.filter(usuario=request.user, data_operacao__year=ano_escolhido)
            .values('data_operacao__month')
            .annotate(total=Sum('valor'))
            .order_by('data_operacao__month')
        )

        # Preenchendo os meses sem movimentações
        dados_ano = [
            {"data_operacao__month": mes, "total": 0} for mes in meses
        ]
        for dado in dados_ano_raw:
            for item in dados_ano:
                if item["data_operacao__month"] == dado["data_operacao__month"]:
                    item["total"] = dado["total"]

        # Dados para o gráfico do mês
        num_dias = calendar.monthrange(ano_escolhido, mes_escolhido)[1]  # Total de dias no mês escolhido
        dias = list(range(1, num_dias + 1))  # Lista de dias no mês

        dados_mes_raw = (
            Entrada.objects.filter(
                usuario=request.user, 
                data_operacao__year=ano_escolhido, 
                data_operacao__month=mes_escolhido
            )
            .values('data_operacao__day')
            .annotate(total=Sum('valor'))
            .order_by('data_operacao__day')
        )

        # Preenchendo os dias sem movimentações
        dados_mes = [
            {"data_operacao__day": dia, "total": 0} for dia in dias
        ]
        for dado in dados_mes_raw:
            for item in dados_mes:
                if item["data_operacao__day"] == dado["data_operacao__day"]:
                    item["total"] = dado["total"]

    return render(request, 'buscar_graficos.html', {
        'anos': anos,
        'meses': meses,
        'ano_escolhido': ano_escolhido,
        'mes_escolhido': mes_escolhido,
        'dados_ano': dados_ano,
        'dados_mes': dados_mes,
    })
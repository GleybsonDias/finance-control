from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import calendar

from .models import Category, Transaction, Goal
from .forms import RegisterForm, ProfileForm, CategoryForm, TransactionForm, GoalForm

# ========================================
# VIEW: Registrar Novo Usuário
# ========================================
def register_view(request):
    """
    Página para um novo usuário se registrar.
    
    POST: Processa o formulário de registro
    GET: Mostra o formulário
    """
    if request.method == 'POST':
        # Recebe os dados do formulário
        form = RegisterForm(request.POST)
        
        # Valida o formulário
        if form.is_valid():
            # Salva o novo usuário no banco
            user = form.save()
            
            # Cria as categorias padrão para o novo usuário
            categorias_padrao = [
                'Alimentação', 'Transporte', 'Estudos', 
                'Moradia', 'Lazer', 'Saúde', 'Renda', 'Outros'
            ]
            
            for cat_name in categorias_padrao:
                Category.objects.create(user=user, name=cat_name)
            
            # Mensagem de sucesso
            messages.success(request, 'Usuário registrado com sucesso! Faça login.')
            
            # Redireciona para a página de login
            return redirect('login')
        # Nota: Se houver erros, o formulário com erros é passado automaticamente para o template
    else:
        # GET: Mostra o formulário vazio
        form = RegisterForm()
    
    return render(request, 'finance/register.html', {'form': form})


# ========================================
# VIEW: Login de Usuário
# ========================================
def login_view(request):
    """
    Página de login do sistema.
    
    POST: Autentica o usuário
    GET: Mostra o formulário de login
    """
    if request.method == 'POST':
        # Recebe nome de usuário e senha
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Valida o usuário
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Usuário encontrado, faz login
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
            
            # Redireciona para o dashboard
            return redirect('dashboard')
        else:
            # Credenciais inválidas
            messages.error(request, 'Usuário ou senha incorretos.')
    
    return render(request, 'finance/login.html')


# ========================================
# VIEW: Logout
# ========================================
def logout_view(request):
    """
    Faz logout do usuário e redireciona para login.
    """
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')


# ========================================
# VIEW: Dashboard Principal
# ========================================
@login_required(login_url='login')  # Só usuários logados podem acessar
def dashboard_view(request):
    """
    Página principal com resumo financeiro e gráficos.
    Mostra: saldo, entradas, saídas, gráficos de despesas.
    """
    # Pega o usuário logado
    user = request.user
    
    # Pega o mês/ano atual (ou usa um parâmetro se vir pela URL)
    hoje = timezone.now()
    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))
    
    # Pega todas as transações do usuário neste mês/ano
    transacoes = Transaction.objects.filter(
        user=user,
        date__month=mes,
        date__year=ano
    )
    
    # Calcula totais
    entradas = transacoes.filter(type='entrada').aggregate(Sum('value'))['value__sum'] or Decimal('0.00')
    saidas = transacoes.filter(type='saida').aggregate(Sum('value'))['value__sum'] or Decimal('0.00')
    saldo = entradas - saidas
    
    # Pega a meta do mês (se existir)
    try:
        meta = Goal.objects.get(user=user, month=mes, year=ano)
        meta_valor = meta.total_goal
        percentual_gasto = (saidas / meta_valor * 100) if meta_valor > 0 else 0
    except Goal.DoesNotExist:
        meta = None
        meta_valor = Decimal('0.00')
        percentual_gasto = 0
    
    # Gastos por categoria
    gastos_por_categoria = {}
    for transacao in transacoes.filter(type='saida'):
        cat = transacao.category.name if transacao.category else 'Sem categoria'
        if cat not in gastos_por_categoria:
            gastos_por_categoria[cat] = Decimal('0.00')
        gastos_por_categoria[cat] += transacao.value
    
    # Últimas 5 transações
    ultimas_transacoes = transacoes[:5]
    
    # Contexto para o template
    context = {
        'mes': mes,
        'ano': ano,
        'entradas': entradas,
        'saidas': saidas,
        'saldo': saldo,
        'meta': meta,
        'meta_valor': meta_valor,
        'percentual_gasto': percentual_gasto,
        'gastos_por_categoria': gastos_por_categoria,
        'ultimas_transacoes': ultimas_transacoes,
        'num_transacoes': len(transacoes),
    }
    
    return render(request, 'finance/dashboard.html', context)


# ========================================
# VIEW: Listar Transações
# ========================================
@login_required(login_url='login')
def transaction_list_view(request):
    """
    Página que lista todas as transações do usuário com filtros.
    Permite buscar por data, categoria, tipo, etc.
    """
    user = request.user
    
    # Começa com todas as transações do usuário
    transacoes = Transaction.objects.filter(user=user)
    
    # FILTROS
    # Filtro por tipo (entrada/saída)
    tipo_filtro = request.GET.get('tipo')
    if tipo_filtro:
        transacoes = transacoes.filter(type=tipo_filtro)
    
    # Filtro por categoria
    categoria_filtro = request.GET.get('categoria')
    if categoria_filtro:
        transacoes = transacoes.filter(category_id=categoria_filtro)
    
    # Filtro por data inicial
    data_inicio = request.GET.get('data_inicio')
    if data_inicio:
        transacoes = transacoes.filter(date__gte=data_inicio)
    
    # Filtro por data final
    data_fim = request.GET.get('data_fim')
    if data_fim:
        transacoes = transacoes.filter(date__lte=data_fim)
    
    # Pega todas as categorias para o formulário de filtro
    categorias = user.categories.all()
    
    # Contexto para o template
    context = {
        'transacoes': transacoes,
        'categorias': categorias,
        'tipo_filtro': tipo_filtro,
        'categoria_filtro': categoria_filtro,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    
    return render(request, 'finance/transaction_list.html', context)


# ========================================
# VIEW: Criar/Editar Transação
# ========================================
@login_required(login_url='login')
def transaction_form_view(request, id=None):
    """
    Página para criar uma nova transação ou editar uma existente.
    
    GET: Mostra o formulário
    POST: Salva a transação
    """
    user = request.user
    transacao = None
    
    # Se é edição, busca a transação
    if id:
        transacao = get_object_or_404(Transaction, id=id, user=user)
    
    if request.method == 'POST':
        # Recebe os dados do formulário
        form = TransactionForm(request.POST, instance=transacao)
        
        if form.is_valid():
            # Salva mas não faz commit ainda (precisa adicionar o usuário)
            transacao = form.save(commit=False)
            
            # Adiciona o usuário logado
            transacao.user = user
            
            # Salva no banco
            transacao.save()
            
            messages.success(request, 'Transação salva com sucesso!')
            return redirect('transaction-list')
    else:
        # GET: Mostra o formulário
        form = TransactionForm(instance=transacao)
        
        # Filtra categorias apenas do usuário logado
        form.fields['category'].queryset = user.categories.all()
    
    context = {
        'form': form,
        'transacao': transacao,
        'titulo': 'Editar Transação' if transacao else 'Nova Transação'
    }
    
    return render(request, 'finance/transaction_form.html', context)


# ========================================
# VIEW: Deletar Transação
# ========================================
@login_required(login_url='login')
def transaction_delete_view(request, id):
    """
    Deleta uma transação do usuário.
    """
    user = request.user
    transacao = get_object_or_404(Transaction, id=id, user=user)
    
    if request.method == 'POST':
        transacao.delete()
        messages.success(request, 'Transação deletada com sucesso!')
        return redirect('transaction-list')
    
    return render(request, 'finance/transaction_confirm_delete.html', {'transacao': transacao})


# ========================================
# VIEW: Listar Categorias
# ========================================
@login_required(login_url='login')
def category_list_view(request):
    """
    Página que lista todas as categorias do usuário.
    Permite criar, editar e deletar categorias.
    """
    user = request.user
    categorias = user.categories.all()
    
    context = {
        'categorias': categorias,
    }
    
    return render(request, 'finance/category_list.html', context)


# ========================================
# VIEW: Criar/Editar Categoria
# ========================================
@login_required(login_url='login')
def category_form_view(request, id=None):
    """
    Página para criar ou editar uma categoria.
    """
    user = request.user
    categoria = None
    
    # Se é edição
    if id:
        categoria = get_object_or_404(Category, id=id, user=user)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=categoria)
        
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.user = user
            categoria.save()
            
            messages.success(request, 'Categoria salva com sucesso!')
            return redirect('category-list')
    else:
        form = CategoryForm(instance=categoria)
    
    context = {
        'form': form,
        'categoria': categoria,
        'titulo': 'Editar Categoria' if categoria else 'Nova Categoria'
    }
    
    return render(request, 'finance/category_form.html', context)


# ========================================
# VIEW: Deletar Categoria
# ========================================
@login_required(login_url='login')
def category_delete_view(request, id):
    """
    Deleta uma categoria do usuário.
    Não permite deletar se a categoria tem transações.
    """
    user = request.user
    categoria = get_object_or_404(Category, id=id, user=user)
    
    # Verifica se a categoria tem transações
    if categoria.transactions.exists():
        messages.error(request, 'Não pode deletar categoria com transações!')
        return redirect('category-list')
    
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria deletada com sucesso!')
        return redirect('category-list')
    
    return render(request, 'finance/category_confirm_delete.html', {'categoria': categoria})


# ========================================
# VIEW: Listar Metas
# ========================================
@login_required(login_url='login')
def goal_list_view(request):
    """
    Página que lista todas as metas do usuário.
    Mostra metas passadas, presente e futuras.
    """
    user = request.user
    metas = user.goals.all().order_by('-year', '-month')
    
    # Adiciona informação de gasto atual para cada meta
    for meta in metas:
        saidas = Transaction.objects.filter(
            user=user,
            type='saida',
            date__month=meta.month,
            date__year=meta.year
        ).aggregate(Sum('value'))['value__sum'] or Decimal('0.00')
        
        meta.gasto_atual = saidas
        meta.percentual = (saidas / meta.total_goal * 100) if meta.total_goal > 0 else 0
    
    context = {
        'metas': metas,
    }
    
    return render(request, 'finance/goal_list.html', context)


# ========================================
# VIEW: Criar/Editar Meta
# ========================================
@login_required(login_url='login')
def goal_form_view(request, id=None):
    """
    Página para criar ou editar uma meta mensal.
    """
    user = request.user
    meta = None
    
    # Se é edição
    if id:
        meta = get_object_or_404(Goal, id=id, user=user)
    
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=meta)
        
        if form.is_valid():
            meta = form.save(commit=False)
            meta.user = user
            meta.save()
            
            messages.success(request, 'Meta salva com sucesso!')
            return redirect('goal-list')
    else:
        form = GoalForm(instance=meta)
    
    context = {
        'form': form,
        'meta': meta,
        'titulo': 'Editar Meta' if meta else 'Nova Meta'
    }
    
    return render(request, 'finance/goal_form.html', context)


# ========================================
# VIEW: Deletar Meta
# ========================================
@login_required(login_url='login')
def goal_confirm_delete_view(request, id):
    """
    Deleta uma meta do usuário.
    """
    user = request.user
    meta = get_object_or_404(Goal, id=id, user=user)
    
    if request.method == 'POST':
        meta.delete()
        messages.success(request, 'Meta deletada com sucesso!')
        return redirect('goal-list')
    
    return render(request, 'finance/goal_confirm_delete.html', {'meta': meta})


# ========================================
# VIEW: Perfil do Usuário
# ========================================
@login_required(login_url='login')
def profile_view(request):
    """
    Página do perfil do usuário.
    Permite editar nome, email, etc.
    """
    user = request.user
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)
    
    context = {
        'form': form,
        'user': user,
    }
    
    return render(request, 'finance/profile.html', context)

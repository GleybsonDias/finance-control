from django.contrib import admin
from .models import Category, Transaction, Goal

# ========================================
# ADMIN: Categoria
# ========================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Interface no admin para gerenciar categorias.
    Mostra: ID, Nome, Usuário, Data de criação
    """
    # Quais colunas mostrar na lista
    list_display = ('id', 'name', 'user', 'created_at')
    
    # Permite buscar por nome e usuário
    search_fields = ('name', 'user__username')
    
    # Permite filtrar por usuário
    list_filter = ('user', 'created_at')
    
    # Campos que aparecem no formulário
    fields = ('user', 'name')


# ========================================
# ADMIN: Transação
# ========================================
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Interface no admin para gerenciar transações.
    Mostra informações detalhadas de cada transação.
    """
    # Quais colunas mostrar na lista
    list_display = ('id', 'user', 'type', 'value', 'category', 'date', 'recurring')
    
    # Permite buscar por descrição, usuário
    search_fields = ('description', 'user__username', 'category__name')
    
    # Permite filtrar por tipo, usuário, categoria, mês
    list_filter = ('type', 'user', 'category', 'date', 'recurring')
    
    # Campos que aparecem no formulário
    fieldsets = (
        ('Informações Principais', {
            'fields': ('user', 'type', 'value', 'category')
        }),
        ('Descrição e Data', {
            'fields': ('description', 'date')
        }),
        ('Configurações', {
            'fields': ('recurring',)
        }),
    )
    
    # Ordenação padrão: mais recentes primeiro
    ordering = ('-date',)


# ========================================
# ADMIN: Meta Mensal
# ========================================
@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    """
    Interface no admin para gerenciar metas mensais.
    Mostra a meta de gasto para cada mês/ano.
    """
    # Quais colunas mostrar na lista
    list_display = ('id', 'user', 'month', 'year', 'total_goal', 'created_at')
    
    # Permite buscar por usuário
    search_fields = ('user__username',)
    
    # Permite filtrar por usuário, mês, ano
    list_filter = ('user', 'month', 'year')
    
    # Campos que aparecem no formulário
    fields = ('user', 'month', 'year', 'total_goal')
    
    # Ordenação: ano/mês mais recentes primeiro
    ordering = ('-year', '-month')

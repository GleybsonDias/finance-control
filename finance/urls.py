from django.urls import path
from . import views

# ========================================
# URLS do APP FINANCE
# ========================================
# Aqui definimos todas as rotas (URLs) do nosso sistema

urlpatterns = [
    # ========== AUTENTICAÇÃO ==========
    # /register - Página de registro
    path('register/', views.register_view, name='register'),
    
    # /login - Página de login
    path('login/', views.login_view, name='login'),
    
    # /logout - Fazer logout
    path('logout/', views.logout_view, name='logout'),
    
    # ========== DASHBOARD ==========
    # / - Dashboard principal (resumo financeiro)
    path('', views.dashboard_view, name='dashboard'),
    
    # ========== TRANSAÇÕES ==========
    # /transactions - Listar todas as transações
    path('transactions/', views.transaction_list_view, name='transaction-list'),
    
    # /transactions/new - Criar nova transação
    path('transactions/new/', views.transaction_form_view, name='transaction-create'),
    
    # /transactions/<id> - Editar uma transação
    path('transactions/<int:id>/', views.transaction_form_view, name='transaction-edit'),
    
    # /transactions/<id>/delete - Deletar uma transação
    path('transactions/<int:id>/delete/', views.transaction_delete_view, name='transaction-delete'),
    
    # ========== CATEGORIAS ==========
    # /categories - Listar categorias
    path('categories/', views.category_list_view, name='category-list'),
    
    # /categories/new - Criar nova categoria
    path('categories/new/', views.category_form_view, name='category-create'),
    
    # /categories/<id> - Editar categoria
    path('categories/<int:id>/', views.category_form_view, name='category-edit'),
    
    # /categories/<id>/delete - Deletar categoria
    path('categories/<int:id>/delete/', views.category_delete_view, name='category-delete'),
    
    # ========== METAS ==========
    # /goals - Listar metas
    path('goals/', views.goal_list_view, name='goal-list'),
    
    # /goals/new - Criar nova meta
    path('goals/new/', views.goal_form_view, name='goal-create'),
    
    # /goals/<id> - Editar meta
    path('goals/<int:id>/', views.goal_form_view, name='goal-edit'),
    
    # /goals/<id>/delete - Deletar meta
    path('goals/<int:id>/delete/', views.goal_confirm_delete_view, name='goal-delete'),
    
    # ========== PERFIL ==========
    # /profile - Página do perfil do usuário
    path('profile/', views.profile_view, name='profile'),
]

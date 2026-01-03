from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

# ========================================
# MODELO: Categoria
# ========================================
# Armazena as categorias de transações (Alimentação, Transporte, etc)
# Cada usuário pode ter suas próprias categorias
class Category(models.Model):
    """
    Modelo para categorizar transações financeiras.
    Exemplo: Alimentação, Transporte, Saúde, etc.
    """
    # Ligação com o usuário (uma categoria pertence a um usuário)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    
    # Nome da categoria (ex: "Alimentação")
    name = models.CharField(max_length=100)
    
    # Data de criação
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Garante que o mesmo usuário não pode criar duas categorias com o mesmo nome
        unique_together = ('user', 'name')
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name


# ========================================
# MODELO: Transação
# ========================================
# Armazena cada movimento financeiro (entrada ou saída)
class Transaction(models.Model):
    """
    Modelo para registrar transações financeiras.
    Pode ser uma entrada (renda) ou saída (despesa).
    """
    # Opções de tipo: Entrada ou Saída
    TRANSACTION_TYPES = [
        ('entrada', 'Entrada'),  # Renda, bônus, etc
        ('saida', 'Saída'),       # Despesa, gasto, etc
    ]
    
    # Ligação com o usuário
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    
    # Ligação com a categoria
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions')
    
    # Tipo de transação (entrada ou saída)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    
    # Valor da transação (não pode ser negativo)
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    
    # Data da transação
    date = models.DateField()
    
    # Descrição (ex: "Compra no supermercado")
    description = models.TextField(blank=True, null=True)
    
    # Se marca como verdadeiro, a transação se repete todo mês
    recurring = models.BooleanField(default=False)
    
    # Data de quando foi criado o registro
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Data de última modificação
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Ordena as transações por data mais recente primeiro
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.type.upper()} - R$ {self.value} - {self.date}"


# ========================================
# MODELO: Meta Mensal
# ========================================
# Armazena as metas financeiras do usuário
class Goal(models.Model):
    """
    Modelo para definir metas de gastos mensais.
    O usuário define quanto quer gastar por mês.
    """
    # Ligação com o usuário
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    
    # Mês (1-12)
    month = models.IntegerField()
    
    # Ano (ex: 2025)
    year = models.IntegerField()
    
    # Valor total que o usuário quer gastar neste mês
    total_goal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    
    # Data de criação
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Garante que cada usuário tem apenas uma meta por mês/ano
        unique_together = ('user', 'month', 'year')
    
    def __str__(self):
        return f"{self.month}/{self.year} - R$ {self.total_goal}"

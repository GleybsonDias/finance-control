from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Category, Transaction, Goal

# ========================================
# FORM: Registro de Usuário
# ========================================
class RegisterForm(UserCreationForm):
    """
    Formulário para novo usuário se registrar.
    Herda da UserCreationForm do Django com validações de senha.
    """
    # Email é requerido (por padrão não é no Django)
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',  # Classe do Bootstrap
            'placeholder': 'seu@email.com'
        })
    )
    
    # Nome de usuário
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário'
        })
    )
    
    # Primeira senha
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha'
        })
    )
    
    # Confirmação da senha
    password2 = forms.CharField(
        label='Confirme a senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        """Salva o usuário e também atualiza o email"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# ========================================
# FORM: Perfil do Usuário
# ========================================
class ProfileForm(UserChangeForm):
    """
    Formulário para editar informações do perfil do usuário.
    Permite mudar nome, email e outras informações.
    """
    # Email editável
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )
    
    # Primeiro nome
    first_name = forms.CharField(
        label='Nome',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    # Último nome
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


# ========================================
# FORM: Categoria
# ========================================
class CategoryForm(forms.ModelForm):
    """
    Formulário para criar/editar categorias.
    """
    class Meta:
        model = Category
        # Só permite editar o nome (usuário é automático)
        fields = ('name',)
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Alimentação'
            })
        }


# ========================================
# FORM: Transação
# ========================================
class TransactionForm(forms.ModelForm):
    """
    Formulário para criar/editar transações.
    Permite escolher tipo, valor, categoria, data, etc.
    """
    class Meta:
        model = Transaction
        # Campos que o usuário pode editar
        # (user é automático, created_at/updated_at são automáticos)
        fields = ('type', 'value', 'category', 'date', 'description', 'recurring')
        
        widgets = {
            # Tipo: Entrada ou Saída
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            
            # Valor da transação
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            
            # Categoria
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            
            # Data
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # Cria um seletor de data nativo
            }),
            
            # Descrição
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da transação'
            }),
            
            # Marcar como recorrente
            'recurring': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


# ========================================
# FORM: Meta Mensal
# ========================================
class GoalForm(forms.ModelForm):
    """
    Formulário para criar/editar metas mensais.
    O usuário define quanto quer gastar neste mês.
    """
    class Meta:
        model = Goal
        # Campos que o usuário pode editar
        fields = ('month', 'year', 'total_goal')
        
        widgets = {
            # Mês (1-12)
            'month': forms.Select(
                choices=[(i, f'{i:02d}') for i in range(1, 13)],
                attrs={
                    'class': 'form-control'
                }
            ),
            
            # Ano
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2020,
                'max': 2099
            }),
            
            # Valor da meta
            'total_goal': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            })
        }

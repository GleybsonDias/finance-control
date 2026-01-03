# Finance — Sistema de Controle Financeiro Pessoal ✅

[![Python](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/) [![Django](https://img.shields.io/badge/django-5.2.8-green)](https://www.djangoproject.com/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Deploy](https://img.shields.io/badge/deploy-local-yellow)](https://img.shields.io/)

## Descrição rápida

**Finance** é uma aplicação web para controle financeiro pessoal desenvolvida com Django, utilizando renderização server-side com templates HTML.
O sistema permite registrar entradas e saídas, organizar despesas por categoria, definir metas mensais e acompanhar os dados por meio de um dashboard com gráficos.

Este projeto foi desenvolvido de forma individual, ao longo do semestre, como trabalho da disciplina Desenvolvimento Rápido de Aplicações em Python (3º período do curso de Análise e Desenvolvimento de Sistemas), evoluindo conforme novos requisitos foram sendo propostos.
---

## Principais funcionalidades

- Registro, login e perfil do usuário
- Adição, edição e remoção de transações (entradas/saídas)
- Filtragem de transações por tipo, categoria e período
- Categorias personalizáveis (cria categorias padrão ao registrar)
- Metas mensais de gastos com acompanhamento do progresso
- Dashboard com gráficos (Chart.js) e resumo financeiro
- Interface administrativa via Django Admin

---

## Tecnologias

- **Linguagem**: Python 3.x
- **Framework**: Django 5.2.8
- **Banco de dados**: SQLite (embutido)
- **Frontend**: HTML + Bootstrap 5
- **Gráficos**: Chart.js

---

## Como rodar localmente (Windows / PowerSh

1. Clone o repositório

```bash
git clone <URL-do-repositório>
cd finance
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# ou, se já há um ambiente no repositório:
.\Scripts\Activate.ps1
```

3. Instale dependências

- Se existir `requirements.txt`:

```bash
pip install -r requirements.txt
```

- Senão, instale Django (versão usada no projeto):

```bash
pip install "django==5.2.8"
```

4. Aplique migrações e crie usuário administrador

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Rode o servidor de desenvolvimento

```bash
python manage.py runserver
```

6. Acesse a aplicação

- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

> Dica: se a porta 8000 estiver ocupada use `python manage.py runserver 8001`.

---

## Onde acessá-lo em funcionamento

- Localmente: `http://127.0.0.1:8000/` após executar `runserver`.
- Observação: **Não há deploy público no momento** — a aplicação está disponível apenas para execução local. Se futuramente houver um deploy público, a URL será adicionada aqui.

---

## Notas sobre o projeto

- Estrutura Django com separação de models, views, forms e templates
- Uso de boas práticas de segurança (hash de senha, CSRF, autorização por usuário)
- Implementação de funcionalidades reais de produto (CRUD de transações, metas e categorias)
- Código pronto para estender — testes automatizados podem ser adicionados (no momento não há testes automatizados)

---

## Melhorias possíveis / trabalho futuro

- Adicionar testes unitários e de integração
- Internacionalização (i18n) e suporte a moedas/formatos locais
- API REST com Django REST Framework
- Deploy contínuo e demonstração pública

---

## Licença

Este projeto está disponível sob a licença **MIT** — sinta-se à vontade para usar e adaptar com atribuição.

---

## Créditos / Contexto do projeto

Desenvolvido como projeto da disciplina **Desenvolvimento Rápido de Aplicações em Python** (3º período do curso Análise e Desenvolvimento de Sistemas). Trabalho realizado individualmente pelo autor do repositório.

---

## Contato

Se quiser ver o projeto em funcionamento público, tirar dúvidas ou avaliar o código, me avise e eu envio a URL do deploy / instruções adicionais.

**Obrigado!**


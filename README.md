# Sistema de Trading Django

## 📋 Visão Geral

Este é um sistema de trading automatizado desenvolvido em Django que integra com a API da Bybit para gerenciar operações de trading de criptomoedas. O sistema permite gerenciar múltiplos usuários de trading, executar ordens automatizadas e monitorar saldos.

## 🏗️ Arquitetura do Projeto

```
projeto/
├── core/                    # Configurações principais do Django
│   ├── settings.py          # Configurações do projeto
│   ├── urls.py              # URLs principais
│   ├── wsgi.py              # Configuração WSGI
│   └── asgi.py              # Configuração ASGI
├── trading/                 # Aplicação principal de trading
│   ├── models.py            # Modelos de dados
│   ├── views.py             # Views da API
│   ├── urls.py              # URLs da aplicação
│   ├── trading_api.py       # Integração com API da Bybit
│   ├── admin.py             # Configuração do admin
│   └── migrations/          # Migrações do banco de dados
├── db.sqlite3               # Banco de dados SQLite
└── manage.py                # Script de gerenciamento Django
```

## 🚀 Tecnologias Utilizadas

- **Framework**: Django 5.2.6
- **Banco de Dados**: SQLite3
- **API Trading**: Bybit (via pybit)
- **Interface Admin**: Jazzmin (interface moderna para Django Admin)
- **Linguagem**: Python
- **Timezone**: America/Sao_Paulo
- **Idioma**: Português Brasileiro

## 📊 Modelos de Dados

### TradingUser
Modelo principal que representa um usuário de trading:

```python
class TradingUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Usuário Django
    created_at = models.DateTimeField(auto_now_add=True)         # Data de criação
    updated_at = models.DateTimeField(auto_now=True)             # Última atualização
    api_key = models.CharField(max_length=255)                   # Chave API Bybit
    api_secret = models.CharField(max_length=255)                # Secret API Bybit
    testnet = models.BooleanField(default=False)                 # Usar testnet?
    is_active = models.BooleanField(default=True)                # Usuário ativo?
```

## 🔌 API Endpoints

### Base URL: `/trading/`

| Endpoint | Método | Descrição | Parâmetros |
|----------|--------|-----------|------------|
| `get-balance/` | GET | Obtém saldo de todos os usuários | - |
| `place-order/` | POST | Executa ordem para usuários ativos | JSON com dados da ordem |
| `close-order/` | POST | Fecha posições abertas | JSON com categoria e símbolo |
| `switch-position-mode/` | POST | Altera modo de posição | JSON com configurações |
| `set-leverage/` | POST | Define alavancagem | JSON com configurações |

### Exemplos de Uso

#### 1. Consultar Saldos
```bash
GET /trading/get-balance/
```

**Resposta:**
```json
{
    "status": "completed",
    "results": [
        {
            "id": 1,
            "username": "trader1",
            "is_active": true,
            "testnet": false,
            "saldo": 1000.50
        }
    ],
    "total_users": 1,
    "successful_orders": 1
}
```

#### 2. Executar Ordem
```bash
POST /trading/place-order/
Content-Type: application/json

{
    "percent": 10,
    "category": "linear",
    "symbol": "BTCUSDT",
    "profit": 2.5,
    "max_loss": 1.5,
    "side": "Buy"
}
```

**Resposta:**
```json
{
    "status": "completed",
    "results": [
        {
            "user_id": "trader1",
            "status": "success",
            "order": {
                "orderId": "12345",
                "symbol": "BTCUSDT",
                "side": "Buy"
            }
        }
    ],
    "total_users": 1,
    "successful_orders": 1
}
```

#### 3. Fechar Posições
```bash
POST /trading/close-order/
Content-Type: application/json

{
    "category": "linear",
    "symbol": "BTCUSDT"
}
```

## 🔧 Classe TradingApi

A classe `TradingApi` é responsável pela integração com a API da Bybit:

### Principais Métodos:

- `get_usdt_balance()`: Obtém saldo em USDT
- `place_order_tp_sl()`: Executa ordem com Take Profit e Stop Loss
- `_get_symbol_price()`: Obtém preço atual de um símbolo
- `close_all_positions()`: Fecha todas as posições abertas
- `set_leverage()`: Define alavancagem para um símbolo
- `switch_position_mode()`: Altera modo de posição

### Configuração:
```python
session = TradingApi(
    api_key="sua_api_key",
    api_secret="sua_api_secret",
    testnet=True  # Para ambiente de teste
)
```

## ⚙️ Configurações

### Configurações Principais (settings.py):

- **DEBUG**: `True` (desenvolvimento)
- **LANGUAGE_CODE**: `'pt-br'`
- **TIME_ZONE**: `'America/Sao_Paulo'`
- **DATABASE**: SQLite3
- **INSTALLED_APPS**: Inclui Jazzmin para interface admin moderna

### Middleware Configurado:
- SecurityMiddleware
- SessionMiddleware
- CommonMiddleware
- CsrfViewMiddleware
- AuthenticationMiddleware
- MessageMiddleware
- ClickjackingMiddleware

## 🚀 Como Executar

### 1. Preparar Ambiente
```bash
# Instalar dependências (você precisará criar requirements.txt)
pip install django pybit jazzmin

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

### 2. Executar Servidor
```bash
python manage.py runserver
```

### 3. Acessar Interfaces
- **Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/trading/

## 🔐 Segurança

### ⚠️ Pontos de Atenção:
1. **SECRET_KEY**: Está exposta no código - deve ser movida para variáveis de ambiente
2. **API Keys**: Armazenadas em texto plano no banco - considere criptografia
3. **DEBUG**: Está ativado - desativar em produção
4. **ALLOWED_HOSTS**: Vazio - configurar para produção

### Recomendações:
```python
# settings.py - Versão segura
import os
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
```

## 📝 Funcionalidades Principais

### 1. Gerenciamento de Usuários
- Cadastro de usuários de trading
- Configuração de API keys da Bybit
- Ativação/desativação de usuários
- Suporte a testnet e produção

### 2. Operações de Trading
- Execução de ordens com Take Profit e Stop Loss
- Fechamento de posições
- Consulta de saldos
- Configuração de alavancagem
- Alteração de modo de posição

### 3. Monitoramento
- Consulta de saldos em tempo real
- Histórico de operações
- Status de usuários ativos

### 4. Interface Administrativa
- Interface moderna com Jazzmin
- Gerenciamento de usuários
- Configurações do sistema

## 🔄 Fluxo de Operação

1. **Cadastro**: Admin cadastra usuário com API keys da Bybit
2. **Ativação**: Usuário é marcado como ativo
3. **Operação**: Sistema recebe requisição via API
4. **Execução**: Para cada usuário ativo, executa a operação
5. **Resposta**: Retorna resultado consolidado

## 📋 Dependências Identificadas

Com base no código analisado, o projeto utiliza:

```txt
Django>=5.2.6
django-jazzmin
pybit
```

## 🚧 Melhorias Sugeridas

1. **Segurança**:
   - Implementar criptografia para API keys
   - Usar variáveis de ambiente
   - Implementar autenticação JWT

2. **Funcionalidades**:
   - Sistema de logs detalhado
   - Histórico de operações
   - Notificações em tempo real
   - Dashboard com métricas

3. **Infraestrutura**:
   - Migrar para PostgreSQL
   - Implementar cache (Redis)
   - Containerização com Docker
   - Testes automatizados

4. **Monitoramento**:
   - Health checks
   - Métricas de performance
   - Alertas de erro

## 📞 Suporte

Para dúvidas sobre o sistema:
1. Consulte a documentação da API Bybit
2. Verifique os logs do Django
3. Teste primeiro no ambiente testnet

---

**Nota**: Este sistema manipula operações financeiras reais. Sempre teste em ambiente testnet antes de usar em produção e implemente medidas de segurança adequadas.
# Guia de Instalação - Sistema de Trading Django

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

## 🚀 Instalação Passo a Passo

### 1. Preparar o Ambiente

```bash
# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 2. Instalar Dependências

```bash
# Instalar dependências do projeto
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar o arquivo .env com suas configurações
# Pelo menos configure a SECRET_KEY
```

### 4. Configurar Banco de Dados

```bash
# Aplicar migrações
python manage.py migrate

# Criar superusuário para acessar o admin
python manage.py createsuperuser
```

### 5. Executar o Servidor

```bash
# Iniciar servidor de desenvolvimento
python manage.py runserver
```

## 🔧 Configuração da API Bybit

### 1. Criar Conta na Bybit
1. Acesse [Bybit](https://www.bybit.com)
2. Crie uma conta
3. Ative a autenticação de dois fatores

### 2. Gerar API Keys
1. Acesse "API Management" no painel da Bybit
2. Crie uma nova API key
3. Configure as permissões necessárias:
   - ✅ Read
   - ✅ Trade
   - ✅ Wallet (para consultar saldos)

### 3. Configurar no Sistema
1. Acesse o admin: http://localhost:8000/admin/
2. Vá em "Trading Users"
3. Adicione um novo usuário de trading
4. Preencha as API keys da Bybit
5. Marque "Testnet" se estiver testando

## 🧪 Testando o Sistema

### 1. Testar Conexão com API
```bash
# Consultar saldos
curl http://localhost:8000/trading/get-balance/
```

### 2. Testar Ordem (Testnet)
```bash
curl -X POST http://localhost:8000/trading/place-order/ \
  -H "Content-Type: application/json" \
  -d '{
    "percent": 1,
    "category": "linear",
    "symbol": "BTCUSDT",
    "profit": 1.0,
    "max_loss": 0.5,
    "side": "Buy"
  }'
```

## 🔐 Configurações de Segurança

### Para Produção:
1. **Altere a SECRET_KEY**:
   ```python
   # Gere uma nova secret key
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Configure DEBUG=False**
3. **Configure ALLOWED_HOSTS**
4. **Use HTTPS**
5. **Configure banco de dados PostgreSQL**

## 📁 Estrutura de Arquivos Importantes

```
projeto/
├── README.md              # Documentação principal
├── INSTALL.md            # Este arquivo
├── requirements.txt      # Dependências Python
├── .env.example         # Exemplo de variáveis de ambiente
├── manage.py            # Script de gerenciamento Django
├── db.sqlite3           # Banco de dados (criado após migrate)
├── core/                # Configurações Django
└── trading/             # Aplicação principal
```

## 🆘 Solução de Problemas

### Erro: "No module named 'pybit'"
```bash
pip install pybit
```

### Erro: "SECRET_KEY not found"
```bash
# Configure a SECRET_KEY no arquivo .env
echo "SECRET_KEY=sua-secret-key-aqui" >> .env
```

### Erro: "API key invalid"
1. Verifique se as API keys estão corretas
2. Confirme se as permissões estão configuradas
3. Teste primeiro no testnet

### Erro: "CSRF token missing"
- As views de POST têm `@csrf_exempt`
- Se removido, inclua o token CSRF nas requisições

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs do Django
2. Teste no ambiente testnet primeiro
3. Consulte a documentação da API Bybit
4. Verifique se todas as dependências estão instaladas

## ⚠️ Avisos Importantes

1. **Sempre teste no testnet primeiro**
2. **Nunca compartilhe suas API keys**
3. **Use pequenas quantias para testes iniciais**
4. **Monitore suas operações constantemente**
5. **Implemente stop-loss adequados**

---

**Lembre-se**: Este sistema opera com dinheiro real. Use com responsabilidade!
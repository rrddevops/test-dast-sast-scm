# Test DAST SAST SCM Flask

Aplicação Flask de exemplo com pipeline CI/CD (SAST, SCM, DAST) e **vulnerabilidades controláveis** para testar a esteira de segurança.

## 🔒 Aplicação com Vulnerabilidades Controláveis

Esta aplicação contém vulnerabilidades intencionais que podem ser **ativadas/desativadas** via variáveis de ambiente para testar cada ferramenta da esteira de segurança:

- **🔍 SAST**: XSS, SQL Injection, Command Injection
- **📦 SCM**: Hardcoded Secrets, Insecure Dependencies  
- **🛡️ DAST**: Path Traversal, Insecure Headers

## 🚀 Como rodar localmente

### 1. Instalação básica
```sh
pip install -r requirements.txt
python app.py
```

### 2. Configurar vulnerabilidades
```sh
# Todas vulnerabilidades ativas (padrão)
export SAST_VULNS=true
export SCM_VULNS=true
export DAST_VULNS=true
python app.py
```

### 3. Cenários de teste específicos
```sh
# Apenas SAST
export SAST_VULNS=true
export SCM_VULNS=false
export DAST_VULNS=false
python app.py

# Apenas SCM
export SAST_VULNS=false
export SCM_VULNS=true
export DAST_VULNS=false
python app.py

# Aplicação segura
export SAST_VULNS=false
export SCM_VULNS=false
export DAST_VULNS=false
python app.py
```

Acesse: http://localhost:5000

## 🐳 Como rodar com Docker

### Build e execução básica
```sh
docker build -t test-dast-sast-scm-flask .
docker run -p 5000:5000 test-dast-sast-scm-flask
```

### Com vulnerabilidades específicas
```sh
docker run -p 5000:5000 \
  -e SAST_VULNS=true \
  -e SCM_VULNS=false \
  -e DAST_VULNS=true \
  test-dast-sast-scm-flask
```

## 🧪 Testando a Esteira de Segurança

### 1. **Teste SAST (SonarCloud)**
```sh
export SAST_VULNS=true
export SCM_VULNS=false
export DAST_VULNS=false
# Faça commit e push - SonarCloud deve detectar vulnerabilidades
```

### 2. **Teste SCM (Trivy)**
```sh
export SAST_VULNS=false
export SCM_VULNS=true
export DAST_VULNS=false
# Faça commit e push - Trivy deve detectar dependências vulneráveis
```

### 3. **Teste DAST (ZAP Proxy)**
```sh
export SAST_VULNS=false
export SCM_VULNS=false
export DAST_VULNS=true
# Faça commit e push - ZAP deve detectar vulnerabilidades web
```

## 📊 Interface Web

A aplicação possui uma interface web em http://localhost:5000 com:

- **Status visual** das vulnerabilidades (ativo/inativo)
- **Botões de teste** para cada tipo de vulnerabilidade
- **Feedback em tempo real** dos testes
- **Configuração via variáveis de ambiente**

## 🔍 Vulnerabilidades Implementadas

### SAST (Static Application Security Testing)
- **XSS**: Cross-Site Scripting via innerHTML
- **SQL Injection**: String concatenation em queries SQL
- **Command Injection**: Execução direta de comandos do sistema

### SCM (Software Composition Management)
- **Hardcoded Secrets**: Senhas e chaves hardcoded no código
- **Insecure Dependencies**: Versões vulneráveis de bibliotecas

### DAST (Dynamic Application Security Testing)
- **Path Traversal**: Acesso a arquivos sem validação de path
- **Insecure Headers**: Headers HTTP que expõem informações

## 🛡️ Pipeline de Segurança

O workflow do GitHub Actions executa automaticamente:

1. **SAST (SonarCloud):**
   - Analisa o código fonte em busca de vulnerabilidades
   - Necessário configurar o segredo `SONAR_TOKEN`

2. **SCM (Trivy):**
   - Analisa a imagem Docker e filesystem
   - Resultados enviados para a aba Security do GitHub

3. **DAST (ZAP Proxy):**
   - Executa testes dinâmicos de segurança
   - Resultados disponíveis como artefatos do workflow

## 🔑 Segredos necessários no GitHub

- `SONAR_TOKEN`: Token do SonarCloud
- `SONAR_PROJECTKEY`: Project key do SonarCloud
- `SONAR_ORGANIZATION`: Organization do SonarCloud
- `DOCKER_USERNAME`: Usuário do Docker Hub
- `DOCKER_PASSWORD`: Token de acesso do Docker Hub

## 📁 Estrutura do Projeto

```
├── app.py                    # Aplicação Flask com vulnerabilidades
├── requirements.txt          # Dependências (incluindo vulneráveis)
├── Dockerfile               # Build da aplicação
├── vulnerability-config.md  # Guia de configuração
├── sonar-project.properties # Configuração SonarCloud
└── .github/workflows/
    └── security-pipeline.yml # Pipeline CI/CD
```

## ⚠️ Aviso de Segurança

⚠️ **ATENÇÃO**: Esta aplicação contém vulnerabilidades intencionais para fins de teste. 
NUNCA use em ambiente de produção ou com dados reais!

## 📖 Documentação Adicional

Veja `vulnerability-config.md` para detalhes completos sobre configuração e cenários de teste. 
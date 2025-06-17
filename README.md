# 🔒 Security Testing Pipeline - SAST, SCM, DAST

Pipeline completo de CI/CD com testes de segurança integrados usando GitHub Actions, SonarCloud (SAST), Trivy (SCM) e ZAP Proxy (DAST).

## 🚀 Funcionalidades

- **SAST (Static Application Security Testing)**: Análise estática com SonarCloud
- **SCM (Software Composition Management)**: Análise de dependências com Trivy
- **DAST (Dynamic Application Security Testing)**: Testes dinâmicos com ZAP Proxy
- **Build & Deploy**: Containerização com Docker e deploy no Docker Hub
- **Security Summary**: Relatório consolidado de segurança
- **Vulnerability Control**: Controle de vulnerabilidades via variáveis de ambiente

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│  GitHub Actions │───▶│  Security Tools │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SonarCloud    │    │   Docker Hub    │    │   ZAP Proxy     │
│     (SAST)      │    │   (Registry)    │    │     (DAST)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Tecnologias

- **Backend**: Python Flask
- **Container**: Docker
- **CI/CD**: GitHub Actions
- **SAST**: SonarCloud
- **SCM**: Trivy
- **DAST**: ZAP Proxy
- **Registry**: Docker Hub

## 📋 Pré-requisitos

### Secrets do GitHub (Obrigatórios)

Configure em `Settings` > `Secrets and variables` > `Actions`:

#### **SonarCloud**
- `SONAR_TOKEN` - Token de acesso do SonarCloud
- `SONAR_PROJECTKEY` - Project key (ex: `rrddevops_test-dast-sast-scm`)
- `SONAR_ORGANIZATION` - Organization (ex: `rrddevops`)

#### **Docker Hub**
- `DOCKER_USERNAME` - Seu usuário do Docker Hub
- `DOCKER_PASSWORD` - Token de acesso do Docker Hub

### Secrets para Controle de Vulnerabilidades (Opcionais)

Para testar diferentes cenários de segurança:

```bash
# Controle Geral
SAST_VULNS=true/false
SCM_VULNS=true/false
DAST_VULNS=true/false

# Controle Específico
XSS_VULN=true/false
SQL_INJECTION_VULN=true/false
COMMAND_INJECTION_VULN=true/false
PATH_TRAVERSAL_VULN=true/false
HARDCODED_SECRETS_VULN=true/false
INSECURE_DEPENDENCIES=true/false
```

## 🚀 Como Usar

### 1. Clone o Repositório
```bash
git clone https://github.com/rrddevops/test-dast-sast-scm.git
cd test-dast-sast-scm
```

### 2. Configure os Secrets
Siga o guia em [github-secrets-config.md](github-secrets-config.md)

### 3. Execute o Pipeline
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 4. Monitore os Resultados
- Acesse a aba **Actions** no GitHub
- Verifique o **Security Summary** no final do workflow
- Consulte os relatórios individuais de cada ferramenta

## 🧪 Cenários de Teste

### Aplicação Segura (Padrão)
Não configure secrets de vulnerabilidade - todos serão `false` por padrão.

### Teste SAST
```bash
SAST_VULNS=true
XSS_VULN=true
SQL_INJECTION_VULN=true
COMMAND_INJECTION_VULN=true
```

### Teste SCM
```bash
SCM_VULNS=true
HARDCODED_SECRETS_VULN=true
INSECURE_DEPENDENCIES=true
```

### Teste DAST
```bash
DAST_VULNS=true
PATH_TRAVERSAL_VULN=true
```

### Teste Completo
```bash
SAST_VULNS=true
SCM_VULNS=true
DAST_VULNS=true
# + todas as vulnerabilidades específicas
```

## 📊 Workflow Stages

### 1. **SAST - SonarCloud**
- Análise estática do código
- Detecção de vulnerabilidades de código
- Quality Gate enforcement
- Upload de resultados SARIF

### 2. **SCM - Trivy**
- Scan de dependências vulneráveis
- Análise de Docker image
- Upload de resultados SARIF
- Categorização única para evitar conflitos

### 3. **Build & Deploy**
- Build da Docker image
- Push para Docker Hub
- Deploy da aplicação

### 4. **DAST - ZAP Proxy**
- Testes dinâmicos da aplicação
- Scan de vulnerabilidades web
- Análise de headers e configurações
- Upload de resultados

### 5. **Security Summary**
- Consolidação de resultados
- Status de cada ferramenta
- Links para relatórios detalhados
- Próximos passos recomendados

## 🔍 Verificação Local

### Executar Aplicação
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar (vulnerabilidades desativadas por padrão)
python app.py

# Ou com vulnerabilidades ativas
export SAST_VULNS=true
export SCM_VULNS=true
export DAST_VULNS=true
python app.py
```

### Testar com Docker
```bash
# Build da imagem
docker build -t security-test-app .

# Executar container
docker run -p 5000:5000 \
  -e SAST_VULNS=false \
  -e SCM_VULNS=false \
  -e DAST_VULNS=false \
  security-test-app
```

### Verificar Status
```bash
# Status das vulnerabilidades
curl http://localhost:5000/api/config

# Health check
curl http://localhost:5000/health
```

## 📁 Estrutura do Projeto

```
test-dast-sast-scm/
├── .github/
│   └── workflows/
│       └── security-pipeline.yml    # Pipeline principal
├── src/
│   └── app.py                       # Aplicação Flask
├── requirements.txt                 # Dependências Python
├── Dockerfile                      # Containerização
├── nginx.conf                      # Configuração Nginx
├── sonar-project.properties        # Configuração SonarCloud
├── vulnerability-config.md         # Guia de configuração
├── github-secrets-config.md        # Configuração de secrets
└── README.md                       # Este arquivo
```

## 🔧 Configurações

### SonarCloud
- **Project Key**: Configurado via `SONAR_PROJECTKEY`
- **Organization**: Configurado via `SONAR_ORGANIZATION`
- **Quality Gate**: Bloqueia merge se falhar

### Trivy
- **Severity**: CRITICAL, HIGH, MEDIUM
- **Format**: SARIF para integração com GitHub
- **Categories**: Únicas para evitar conflitos

### ZAP Proxy
- **Scan Type**: Baseline scan
- **Target**: Aplicação Flask rodando no container
- **Timeout**: 15 minutos

## 📈 Resultados Esperados

### Com Vulnerabilidades Desativadas
- ✅ SAST: SonarCloud passa sem problemas críticos
- ✅ SCM: Trivy detecta poucas ou nenhuma vulnerabilidade
- ✅ DAST: ZAP encontra poucos problemas
- ✅ Quality Gate: Aprovado

### Com Vulnerabilidades Ativadas
- ⚠️ SAST: SonarCloud detecta vulnerabilidades de código
- ⚠️ SCM: Trivy detecta dependências vulneráveis
- ⚠️ DAST: ZAP detecta vulnerabilidades web
- ❌ Quality Gate: Pode falhar dependendo da configuração

## 🚨 Troubleshooting

### Problema: Build falha no Docker
**Solução**: 
- As dependências foram drasticamente simplificadas para evitar problemas de compilação
- Removemos `cryptography`, `urllib3`, `pyyaml` que causavam erros de build
- Usamos apenas `flask`, `gunicorn` e `requests` (versões estáveis)
- Configuração do pip força uso de binários pré-compilados
- Use `python test-build.py` para testar dependências localmente

### Problema: SonarCloud não encontra o projeto
**Solução**: Verifique se `SONAR_PROJECTKEY` e `SONAR_ORGANIZATION` estão corretos.

### Problema: ZAP não consegue acessar a aplicação
**Solução**: Verifique se a aplicação está rodando e acessível na porta 5000.

### Problema: Vulnerabilidades não estão sendo ativadas
**Solução**: Verifique se os secrets estão configurados corretamente no GitHub.

## 🧪 Teste Local

### Verificar Dependências
```bash
# Teste se todas as dependências funcionam
python test-build.py
```

### Executar Aplicação
```bash
# Instalar dependências (mínimas)
pip install -r requirements.txt

# Executar (vulnerabilidades desativadas por padrão)
python app.py

# Ou com vulnerabilidades ativas
export SAST_VULNS=true
export SCM_VULNS=true
export DAST_VULNS=true
python app.py
```

## 📚 Documentação Adicional

- [Configuração de Secrets](github-secrets-config.md)
- [Configuração de Vulnerabilidades](vulnerability-config.md)
- [SonarCloud Documentation](https://docs.sonarcloud.io/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [ZAP Proxy Documentation](https://www.zaproxy.org/docs/)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🔗 Links Úteis

- [GitHub Actions](https://github.com/features/actions)
- [SonarCloud](https://sonarcloud.io/)
- [Docker Hub](https://hub.docker.com/)
- [ZAP Proxy](https://www.zaproxy.org/) 
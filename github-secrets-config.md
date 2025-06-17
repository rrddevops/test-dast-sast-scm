# 🔧 Configuração de Secrets no GitHub

Este guia explica como configurar os secrets no GitHub para controlar as vulnerabilidades na esteira de segurança.

## 🎛️ Secrets para Controle de Vulnerabilidades

### Secrets Obrigatórios

Configure estes secrets em `Settings` > `Secrets and variables` > `Actions`:

#### **SonarCloud**
- `SONAR_TOKEN` - Token de acesso do SonarCloud
- `SONAR_PROJECTKEY` - Project key do SonarCloud (ex: `rrddevops_test-dast-sast-scm`)
- `SONAR_ORGANIZATION` - Organization do SonarCloud (ex: `rrddevops`)

#### **Docker Hub**
- `DOCKER_USERNAME` - Seu usuário do Docker Hub (ex: `rodrigordavila`)
- `DOCKER_PASSWORD` - Token de acesso do Docker Hub

### Secrets para Controle de Vulnerabilidades (Opcionais)

Estes secrets controlam quais vulnerabilidades estão ativas durante os testes:

#### **Controle Geral**
- `SAST_VULNS` - `true` ou `false` (padrão: `false`)
- `SCM_VULNS` - `true` ou `false` (padrão: `false`)
- `DAST_VULNS` - `true` ou `false` (padrão: `false`)

#### **Controle Específico**
- `XSS_VULN` - `true` ou `false` (padrão: `false`)
- `SQL_INJECTION_VULN` - `true` ou `false` (padrão: `false`)
- `COMMAND_INJECTION_VULN` - `true` ou `false` (padrão: `false`)
- `PATH_TRAVERSAL_VULN` - `true` ou `false` (padrão: `false`)
- `HARDCODED_SECRETS_VULN` - `true` ou `false` (padrão: `false`)
- `INSECURE_DEPENDENCIES` - `true` ou `false` (padrão: `false`)

## 🧪 Cenários de Teste

### 1. **Aplicação Segura (Padrão)**
Não configure nenhum secret de vulnerabilidade - todos serão `false` por padrão.

### 2. **Teste SAST**
```
SAST_VULNS=true
XSS_VULN=true
SQL_INJECTION_VULN=true
COMMAND_INJECTION_VULN=true
```

### 3. **Teste SCM**
```
SCM_VULNS=true
HARDCODED_SECRETS_VULN=true
INSECURE_DEPENDENCIES=true
```

### 4. **Teste DAST**
```
DAST_VULNS=true
PATH_TRAVERSAL_VULN=true
```

### 5. **Teste Completo**
```
SAST_VULNS=true
SCM_VULNS=true
DAST_VULNS=true
XSS_VULN=true
SQL_INJECTION_VULN=true
COMMAND_INJECTION_VULN=true
PATH_TRAVERSAL_VULN=true
HARDCODED_SECRETS_VULN=true
INSECURE_DEPENDENCIES=true
```

## 🔍 Como Verificar a Configuração

### 1. **Via Interface Web**
Acesse a aplicação em http://localhost:5000 (ou URL do container) e veja o status das vulnerabilidades.

### 2. **Via API**
```bash
curl http://localhost:5000/api/config
```

### 3. **Via Logs**
Os logs da aplicação mostram o status das vulnerabilidades no startup:
```
INFO:__main__:Vulnerability Status:
INFO:__main__:  SAST_VULNS: false
INFO:__main__:  SCM_VULNS: false
INFO:__main__:  DAST_VULNS: false
```

## 🚀 Como Configurar

### Passo a Passo

1. **Acesse o repositório no GitHub**
2. **Vá em Settings** > **Secrets and variables** > **Actions**
3. **Clique em "New repository secret"**
4. **Adicione cada secret** conforme necessário
5. **Faça commit e push** para executar o pipeline

### Exemplo de Configuração

Para testar apenas SAST:

1. Adicione o secret `SAST_VULNS` com valor `true`
2. Adicione o secret `XSS_VULN` com valor `true`
3. Adicione o secret `SQL_INJECTION_VULN` com valor `true`
4. Faça commit e push

## 📊 Resultados Esperados

### Com Vulnerabilidades Desativadas
- **SAST**: SonarCloud deve passar sem problemas críticos
- **SCM**: Trivy deve detectar poucas ou nenhuma vulnerabilidade
- **DAST**: ZAP deve encontrar poucos problemas

### Com Vulnerabilidades Ativadas
- **SAST**: SonarCloud deve detectar vulnerabilidades de código
- **SCM**: Trivy deve detectar dependências vulneráveis
- **DAST**: ZAP deve detectar vulnerabilidades web

## ⚠️ Importante

- **Secrets não configurados** assumem valor `false` (vulnerabilidades desativadas)
- **Mudanças nos secrets** só afetam novos builds
- **Logs da aplicação** mostram o status atual das vulnerabilidades
- **Interface web** reflete o status em tempo real

## 🔧 Troubleshooting

### Problema: Vulnerabilidades não estão sendo ativadas
**Solução**: Verifique se os secrets estão configurados corretamente e se os valores são `true` (não `True` ou `TRUE`).

### Problema: Build falha no Docker
**Solução**: As dependências foram atualizadas para versões compatíveis. Se ainda houver problemas, verifique os logs do build.

### Problema: ZAP não encontra vulnerabilidades
**Solução**: Verifique se `DAST_VULNS=true` está configurado e se a aplicação está rodando corretamente. 
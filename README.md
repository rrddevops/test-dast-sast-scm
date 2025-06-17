# Test DAST SAST SCM Flask

Aplicação Flask de exemplo com pipeline CI/CD (SAST, SCM, DAST).

## Como rodar localmente

```sh
pip install -r requirements.txt
python app.py
```

Acesse: http://localhost:5000

## Como rodar com Docker

```sh
docker build -t test-dast-sast-scm-flask .
docker run -p 5000:5000 test-dast-sast-scm-flask
```

## Pipeline

- SAST: SonarCloud
- SCM: Trivy
- DAST: ZAP Proxy

Configure o segredo SONAR_TOKEN no GitHub.

## 🛡️ Pipeline de Segurança (CI/CD)

O workflow do GitHub Actions executa automaticamente:

1. **SAST (SonarCloud):**
   - Analisa o código fonte em busca de vulnerabilidades e problemas de qualidade.
   - Necessário configurar o segredo `SONAR_TOKEN` no repositório.

2. **SCM (Trivy):**
   - Analisa a imagem Docker e o filesystem do projeto em busca de vulnerabilidades.
   - Resultados enviados para a aba Security do GitHub.

3. **Build & Deploy:**
   - Faz build e push da imagem Docker para o GitHub Container Registry.
   - (Personalize o deploy conforme sua infraestrutura.)

4. **DAST (ZAP Proxy):**
   - Executa testes dinâmicos de segurança na aplicação publicada.
   - Necessário configurar o segredo `TARGET_URL` com a URL do ambiente de staging/produção.
   - Resultados disponíveis como artefatos do workflow.

5. **Resumo de Segurança:**
   - Gera um relatório resumido no GitHub Actions.

---

## 🔑 Segredos necessários no GitHub

- `SONAR_TOKEN`: Token do SonarCloud para análise SAST
- `TARGET_URL`: URL da aplicação para o ZAP Proxy executar os testes DAST

Adicione esses segredos em: `Settings` > `Secrets and variables` > `Actions`

---

## 📂 Estrutura do Projeto

```
├── Dockerfile
├── nginx.conf
├── package.json
├── package-lock.json
├── public/
│   └── index.html
├── src/
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── sonar-project.properties
└── .github/
    └── workflows/
        └── security-pipeline.yml
```

---

## 📢 Observações
- O deploy real deve ser configurado no passo "Deploy to staging" do workflow.
- O arquivo `.zap/rules.tsv` pode ser personalizado para regras do ZAP.
- O projeto é um exemplo educacional e pode ser expandido conforme sua necessidade.

---

## 📝 Licença
MIT 
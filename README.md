# 📚 PlanoEdu — Sistema de Gerenciamento de Planos de Aula

Sistema web para cadastro, organização e consulta de planos de aula, com assistente de IA integrado para sugestões pedagógicas automáticas.

---

## 🚀 Link do Deploy

Link direto: [https://plano-de-aula-desafio-production.up.railway.app](https://plano-de-aula-desafio-production.up.railway.app)

---

## 📹 Vídeo de Apresentação (Até 5 minutos)

Assista ao vídeo demonstrativo apresentando a solução desenvolvida, arquitetura, escolhas técnicas e os itens bônus implementados:

▶️ **[Clique aqui para assistir ao vídeo de apresentação do projeto](LINK_DO_SEU_VIDEO_AQUI)**



---

## ✨ Funcionalidades & Diferenciais

### 📝 CRUD de Planos de Aula
* Cadastro completo: Título, Disciplina, Objetivo, Ementa, Conteúdos, Recursos, Data Prevista e Tags.
* Listagem com paginação e busca dinâmica em tempo real.
* Filtros avançados por título, disciplina, tag e data.
* Edição simplificada e exclusão segura com confirmação.

### 🪄 Smart Assist — IA Integrada
* Geração automática de planos utilizando a API do Groq.
* Preenchimento inteligente e automatizado do formulário (Objetivo, Conteúdos, Recursos e Tags) a partir do Título e Disciplina informados.
* Feedback visual de carregamento adaptável.

### 🐳 Containerização (Diferencial)
* Ambiente isolado e idêntico utilizando **Docker** e **Docker Compose**.
* Inicialização completa de todas as camadas com um único comando (`docker compose up --build`).

### 📊 Observabilidade & Health Check (Diferencial)
* **Logs Estruturados:** Monitoramento ativo no backend registrando chamadas cruciais do sistema e métricas de desempenho da IA.
  * *Exemplo de log registrado:* `[INFO] AI Request: Title="Introdução ao OSPF", Discipline="Redes", TokenUsage=180, Latency=1.4s.`
* **Endpoint de Health Check:** Rota dedicada `/health` mapeada para monitorar a saúde da aplicação e integridade do banco de dados na nuvem.

---

## 🏗️ Estrutura do Projeto

```text
plano-de-aula-desafio/
│   docker-compose.yml
│
└───backend/
    │   Dockerfile
    │   requirements.txt
    │   run.py
    │   config.py
    │
    └───app/
        │   models.py        # Modelos do banco de dados
        │   __init__.py      # Factory da aplicação Flask e logs
        │
        ├───rotas/
        │   │   plano_aula.py  # CRUD de planos e health check
        │   │   ai.py          # Endpoint Smart Assist com logs estruturados
        │
        ├───servicos/
        │   │   ia_servicos.py # Integração com Groq
        │
        └───templates/
                index.html     # SPA (frontend)

---

## 💻 Como Rodar o Projeto Localmente

### Pré-requisitos
* Docker Desktop instalado
* Uma chave da API do Groq

### Passo a passo
```bash
# 1. Clone o repositório e acesse a pasta
git clone [https://github.com/vitoriaduran/plano-de-aula-desafio.git](https://github.com/vitoriaduran/plano-de-aula-desafio.git)
cd plano-de-aula-desafio

# 2. Configure as variáveis de ambiente
# Crie o arquivo backend/.env com base no exemplo abaixo
GROQ_API_KEY=sua_chave_aqui
FLASK_ENV=development
SECRET_KEY=uma-string-secreta

# 3. Suba a aplicação com um único comando
docker compose up --build

---

## 🔌 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/planos` | Listar planos (filtros + paginação) |
| POST | `/api/planos` | Criar novo plano |
| GET | `/api/planos/<id>` | Buscar plano por ID |
| PUT | `/api/planos/<id>` | Editar plano |
| DELETE | `/api/planos/<id>` | Deletar plano |
| POST | `/api/ai/gerar` | Gerar sugestões com IA |
| GET | `/health` |Endpoint de verificação de integridade |

---

## 🛠️ Stack Utilizada

| Camada | Tecnologia |
|--------|------------|
| Backend | Python + Flask |
| Banco de dados | SQLite + SQLAlchemy |
| IA | Groq API |
| Frontend | HTML + CSS + JavaScript (SPA) |
| DevOps | Docker + Docker Compose |
| Deploy | Railway |


---
## 🔒 Segurança
 
- A chave da API **nunca está no código** — é lida via variável de ambiente
- O arquivo `.env` está no `.gitignore` e não vai para o repositório
- O arquivo `.env.example` serve como modelo seguro para novos desenvolvedores
---

## 👩‍💻 Autora

**Vitória Duran**
[github.com/vitoriaduran](https://github.com/vitoriaduran)

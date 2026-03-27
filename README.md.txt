AI Support Platform (Prototype)

Este projeto é um protótipo de uma plataforma de suporte com uso de IA, criado como estudo de LLM, embeddings e busca semântica aplicados a tickets de atendimento.

A ideia é simular como um sistema de suporte poderia:

analisar automaticamente mensagens de usuários

classificar tickets

gerar embeddings

buscar tickets semelhantes

fornecer respostas automáticas baseadas em contexto

O objetivo não é ser um sistema pronto para produção, mas sim demonstrar arquitetura, integração com IA e conceitos de RAG.

Arquitetura do projeto

O projeto foi dividido em módulos simples para manter o código organizado.

app/
 ├── api.py                # endpoints FastAPI
 ├── models.py             # modelo do banco de dados
 ├── database.py           # configuração do banco
 ├── config.py             # variáveis de configuração
 ├── ai_service.py         # análise de tickets com LLM
 ├── embedding_service.py  # geração de embeddings
 ├── search_service.py     # busca semântica
 ├── rag_service.py        # base simples de FAQ (RAG)

Fluxo básico:

Usuário envia ticket
        ↓
LLM analisa mensagem
        ↓
Sistema gera embedding
        ↓
Ticket é salvo no banco
        ↓
Sistema permite busca semântica
Tecnologias usadas

Python

FastAPI

SQLAlchemy

SQLite

OpenAI API

Numpy

O banco é SQLite apenas para facilitar o protótipo.

Funcionalidades
Criar ticket

Analisa automaticamente o ticket com IA:

categoria

prioridade

sentimento

resposta sugerida

Endpoint:

POST /ticket

Exemplo:

{
  "message": "Meu pagamento foi recusado e não sei o motivo"
}
Buscar tickets semelhantes

Busca tickets usando similaridade semântica com embeddings.

Endpoint:

POST /search

Exemplo:

{
  "query": "problema com pagamento"
}
Analytics simples

Retorna estatísticas básicas do sistema:

quantidade por categoria

prioridade

sentimento

Endpoint:

GET /analytics
Configuração

Criar um arquivo .env ou definir a variável de ambiente:

OPENAI_API_KEY=your_api_key
Instalação

Clone o repositório:

git clone <repo>
cd ai-support-platform

Crie o ambiente virtual:

python -m venv venv
source venv/bin/activate

Instale as dependências:

pip install -r requirements.txt
Rodando o projeto

Execute:

uvicorn app.api:app --reload

A API ficará disponível em:

http://localhost:8000

Documentação automática:

http://localhost:8000/docs
Observações

Este projeto foi feito como protótipo para explorar:

integração com LLMs

classificação automática de tickets

embeddings

busca semântica

conceitos básicos de RAG

Algumas simplificações foram feitas propositalmente:

uso de SQLite

embeddings armazenados em JSON

ranking feito em memória

Em um sistema real, o ideal seria utilizar:

PostgreSQL + pgvector

banco vetorial dedicado

pipelines de processamento

filas de eventos
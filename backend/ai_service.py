import json
from openai import OpenAI
from .config import settings
from .rag_service import search_faq

client = OpenAI(api_key=settings.openai_api_key)

def analyze_ticket(message: str) -> dict:
    faq_context = search_faq(message)

    prompt = f"""
Você é um assistente de suporte.

Analise o ticket abaixo e responda SOMENTE com JSON válido.
Não escreva explicações, não use markdown, não coloque ```json.

As chaves obrigatórias são:
- categoria
- prioridade
- sentimento
- resposta

Categorias possíveis:
- Pagamentos
- Conta
- Login
- Cartão
- Suporte Técnico
- Outros

Prioridades possíveis:
- Baixa
- Média
- Alta

Sentimentos possíveis:
- Positivo
- Neutro
- Negativo

Contexto FAQ:
{faq_context if faq_context else "Sem contexto adicional"}

Ticket:
{message}
"""

    fallback = {
        "categoria": "Outros",
        "prioridade": "Baixa",
        "sentimento": "Neutro",
        "resposta": "Não foi possível analisar automaticamente."
    }

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        result = (response.output_text or "").strip()

        if not result:
            return {
                **fallback,
                "resposta": "Falha na análise automática: resposta vazia do modelo."
            }

        start = result.find("{")
        end = result.rfind("}")

        if start == -1 or end == -1:
            return {
                **fallback,
                "resposta": f"Falha na análise automática: resposta não veio em JSON. Retorno: {result}"
            }

        json_text = result[start:end + 1]
        data = json.loads(json_text)

        return {
            "categoria": data.get("categoria", "Outros"),
            "prioridade": data.get("prioridade", "Baixa"),
            "sentimento": data.get("sentimento", "Neutro"),
            "resposta": data.get("resposta", "Sem resposta sugerida.")
        }

    except Exception as e:
        return {
            **fallback,
            "resposta": f"Falha na análise automática: {str(e)}"
        }
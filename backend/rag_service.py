faq = [
    {
        "pergunta": "pagamento recusado",
        "resposta": "Verifique saldo disponível, limite e dados do cartão.",
    },
    {
        "pergunta": "não consigo acessar conta",
        "resposta": "Utilize a opção de recuperação de senha e confirme seu e-mail.",
    },
    {
        "pergunta": "pix não caiu",
        "resposta": "Valide o comprovante, horário da transação e status no extrato.",
    },
]


def search_faq(message: str) -> str:
    """
    RAG simples para estudo: procura um contexto curto em uma FAQ local.
    """
    normalized = message.lower()

    for item in faq:
        if item["pergunta"] in normalized:
            return item["resposta"]

    return ""

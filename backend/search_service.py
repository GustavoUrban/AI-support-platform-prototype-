import numpy as np
from sqlalchemy.orm import Session

from .embedding_service import get_embedding
from .models import Ticket


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Similaridade cosseno com proteção contra divisão por zero.
    """
    vector_a = np.array(a, dtype=float)
    vector_b = np.array(b, dtype=float)

    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(np.dot(vector_a, vector_b) / (norm_a * norm_b))


def search_tickets(query: str, db: Session) -> list[dict]:
    query_embedding = get_embedding(query)
    tickets = db.query(Ticket).all()

    results = []
    for ticket in tickets:
        if not ticket.embedding:
            continue

        score = cosine_similarity(query_embedding, ticket.embedding)
        results.append(
            {
                "id": ticket.id,
                "message": ticket.message,
                "categoria": ticket.categoria,
                "score": float(score),
            }
        )

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5]

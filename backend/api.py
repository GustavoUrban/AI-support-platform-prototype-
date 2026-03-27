from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .ai_service import analyze_ticket
from .config import settings
from .database import Base, engine, get_db
from .embedding_service import get_embedding
from .models import Ticket
from .schemas import TicketRequest
from .search_service import search_tickets

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Support Platform")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "ok",
        "project": "AI Support Platform",
        "mode": "prototipo",
    }


@app.post("/ticket")
def create_ticket(ticket: TicketRequest, db: Session = Depends(get_db)):
    try:
        analysis = analyze_ticket(ticket.message)
        embedding = get_embedding(ticket.message)

        new_ticket = Ticket(
            message=ticket.message,
            categoria=analysis.get("categoria", "Outros"),
            prioridade=analysis.get("prioridade", "Baixa"),
            sentimento=analysis.get("sentimento", "Neutro"),
            embedding=embedding,
        )

        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)

        return {
            "message": "ticket criado",
            "ticket_id": new_ticket.id,
            "analysis": analysis,
        }
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/search")
def search(query: str, db: Session = Depends(get_db)):
    try:
        return search_tickets(query, db)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()

    categorias = {}
    prioridades = {}
    sentimentos = {}

    for ticket in tickets:
        categorias[ticket.categoria] = categorias.get(ticket.categoria, 0) + 1
        prioridades[ticket.prioridade] = prioridades.get(ticket.prioridade, 0) + 1
        sentimentos[ticket.sentimento] = sentimentos.get(ticket.sentimento, 0) + 1

    return {
        "total_tickets": len(tickets),
        "categorias": categorias,
        "prioridades": prioridades,
        "sentimentos": sentimentos,
    }

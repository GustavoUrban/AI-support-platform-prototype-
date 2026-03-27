from sqlalchemy import Column, Integer, JSON, String

from .database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    categoria = Column(String, nullable=False, default="Outros")
    prioridade = Column(String, nullable=False, default="Baixa")
    sentimento = Column(String, nullable=False, default="Neutro")
    embedding = Column(JSON, nullable=True)

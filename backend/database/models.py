from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from sqlalchemy.orm import declarative_base


Base = declarative_base()


class MarketPrice(Base):

    __tablename__ = "market_prices"


    id = Column(
        Integer,
        primary_key=True
    )


    symbol = Column(
        String
    )


    price = Column(
        Float
    )


    created_at = Column(
        DateTime
    )


class AIDecision(Base):

    __tablename__ = "ai_decisions"


    id = Column(
        Integer,
        primary_key=True
    )


    symbol = Column(
        String
    )


    decision = Column(
        String
    )


    score = Column(
        Integer
    )


    created_at = Column(
        DateTime
    )

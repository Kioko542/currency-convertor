# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class ExchangeRate(Base):
    __tablename__ = 'exchange_rates'

    id = Column(Integer, primary_key=True)
    base_currency = Column(String, nullable=False)
    target_currency = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

def initialize_database():
    engine = create_engine('sqlite:///exchange_rates.db', echo=True)
    Base.metadata.create_all(bind=engine)
    return engine

def add_exchange_rate(session, base_currency, target_currency, rate):
    new_rate = ExchangeRate(base_currency=base_currency, target_currency=target_currency, rate=rate)
    session.add(new_rate)
    session.commit()

def get_exchange_rate(session, base_currency, target_currency):
    rate = session.query(ExchangeRate).filter_by(base_currency=base_currency, target_currency=target_currency).first()
    if rate:
        return rate.rate
    return None

def convert_currency(session, amount, base_currency, target_currency):
    rate = get_exchange_rate(session, base_currency, target_currency)
    if rate is not None:
        converted_amount = amount * rate
        return converted_amount, target_currency
    return None, None

def view_all_exchange_rates(session):
    print("\nAll Exchange Rates:")
    exchange_rates = session.query(ExchangeRate).all()
    for rate in exchange_rates:
        print(f"{rate.base_currency} to {rate.target_currency}: {rate.rate} (Added on: {rate.timestamp})")

def update_exchange_rate(session, base_currency, target_currency, new_rate):
    rate = session.query(ExchangeRate).filter_by(base_currency=base_currency, target_currency=target_currency).first()
    if rate:
        rate.rate = new_rate
        session.commit()
        print(f"Exchange rate updated: {base_currency} to {target_currency} = {new_rate}")
    else:
        print("Exchange rate not found.")

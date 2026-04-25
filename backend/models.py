from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

# Stworzenie klasy reprezentującej pojedynczy wpis w bazie danych
class CurrencyRate(Base):
    __tablename__ = "currency_rates" # Nazwa tabeli w bazie danych

    id = Column(Integer, primary_key=True, index=True) # Unikalny identyfikator
    currency = Column(String, index=True) # Nazwa waluty (np. "dolar amerykański")
    code = Column(String, index=True) # Kod waluty (np. "USD")
    mid = Column(Float) # Kurs średni
    effective_date = Column(Date, index=True) # Data obowiązywania kursu
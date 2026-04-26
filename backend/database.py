import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Szukanie zmiennej środowiskowej DATABASE_URL podawanej przez Docker. W przypadku jej braku, awaryjnie używany jest SQLite
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./currencies.db")

# Utworzenie silnika bazy danych, który będzie używany do komunikacji z bazą danych
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Utworzenie klasy SessionLocal, która będzie używana do tworzenia sesji do bazy danych
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Utworzenie klasy Base, z której będą dziedziczyć modele tabel w bazie danych
Base = declarative_base()

# Funkcja pomocnicza, która w bezpieczny sposób otwiera i zamyka połączenie z bazą danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
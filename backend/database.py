from sqlalchemy import create_engine
from sqlalchemy.orm import declerative_base, sessionmaker

# Adres URL do bazy danych SQLite, która będzie używana do przechowywania danych o kursach walut
# Plik bazy danych będzie znajdował się w tym samym katalogu i będzie nazywał się "currencies.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./currencies.db"

# Utworzenie silnika bazy danych, który będzie używany do komunikacji z bazą danych
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Utworzenie klasy SessionLocal, która będzie używana do tworzenia sesji do bazy danych
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Utworzenie klasy Base, z której będą dziedziczyć modele tabel w bazie danych
Base = declerative_base()

# Funkcja pomocnicza, która w bezpieczny sposób otwiera i zamyka połączenie z bazą danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
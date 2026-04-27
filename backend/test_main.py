from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db

# Konfiguracja wirtualnej bazy danych do testów
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Stworzenie tabel w bazie testowej
Base.metadata.create_all(bind=engine)

# Podmiana bazy domyślnej na testową
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# Testowanie połączenie z bazą danych
def test_db_connection():
    db = TestingSessionLocal()
    assert db is not None # Sprawdzenie, czy obiekt sesji bazy istnieje
    db.close()

# Testowaie poprawności odpowiedzi API
def test_api_response_history():
    response = client.get("/currencies/history/all")
    assert response.status_code == 200 # Sprawdzenie, czy serwer odpowiada kodem 200 OK
    assert isinstance(response.json(), list) # Sprawdzenie, czy odpowiedź to lista (nawet pusta, ponieważ baza testowa nie ma jeszcze danych)

# Testowanie poprawności odpowiedzi API (dla błędnych danych)
def test_api_validation_error():
    response = client.post("/currencies/fetch?days=abc") # Wysłanie typu string zamiast liczby dni
    assert response.status_code == 422 # API powinno wyłapać błąd walidacji i zwrócić 422 Unprocessable Entity
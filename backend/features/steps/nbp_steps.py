from behave import given, when, then
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import modułów z aplikacji i bazy danych
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from main import app
from database import Base, get_db
from models import CurrencyRate

# Stworzenie osobnej, testowej bazy w pamięci
SQLALCHEMY_DATABASE_URL = "sqlite:///./behave_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@given('Baza danych jest pusta')
def database_is_empty(context):
    # Wyczyszczenie starej bazy i tworzenie nowej - pustej
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@when('Użytkownik wysyła zadanie pobrania kursów z ostatnich "{days}" dni')
def user_sends_request_to_fetch_currencies(context, days):
    # Symulacja kliknięcia przycisku pobierania kursów walut
    context.response = client.post(f"/currencies/fetch?days={days}")

@then('API powinno zwrócić kod sukcesu {status_code:d}')
def API_should_return_success_code(context, status_code):
    # Sprawdzenie, czy odpowiedź API zawiera kod sukcesu
    assert context.response.status_code == status_code

@then('Baza danych powinna zawierać nowe rekordy')
def database_should_contain_new_records(context):
    # Sprawdzenie, czy baza danych zawiera nowe rekordy
    db = TestingSessionLocal()
    count = db.query(CurrencyRate).count()
    db.close()

    # Powinno być więcej niż 0 zapisanych walut
    assert count > 0, f"Oczekiwano nowych rekordów w bazie danych, ale znaleziono {count}."
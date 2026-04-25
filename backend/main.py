import requests
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import CurrencyRate

# Utworzenie bazy danych i tabel, jeśli jeszcze nie istnieją
Base.metadata.create_all(bind=engine)

# Stworzenie głównej instancji aplikacji FastAPI
app = FastAPI(title="Currency Dashboard API")

@app.post("/currencies/fetch")
def fetch_and_save_currencies(db: Session = Depends(get_db)):
    # Zdefiniowanie URL do API NBP, które zwraca aktualne kursy walut w formacie JSON
    url = "http://api.nbp.pl/api/exchangerates/tables/A/?format=json"

    # Wysłanie żądania GET do API NBP
    response = requests.get(url)

    # Sprawdzenie, czy odpowiedź z API jest poprawna (status code 200)
    if response.status_code == 200:
        data = response.json()
        table_data = data[0]
        
        # Wyciągnięcie daty obowiązywania kursów walut oraz listy kursów walut z odpowiedzi JSON
        effective_date_str = table_data['effectiveDate']
        rates = table_data['rates']

        # Konwersja daty z formatu string na obiekt datetime
        effective_date = datetime.strptime(effective_date_str, "%Y-%m-%d").date()

        added_count = 0 # Licznik dodanych kursów walut do bazy danych

        # Zapisanie kursów walut do bazy danych
        for rate in rates:
            # Sprawdzenie, czy kurs waluty o danym kodzie i dacie obowiązywania już istnieje w bazie danych
            existing_rate = db.query(CurrencyRate).filter(
                CurrencyRate.code == rate['code'],
                CurrencyRate.effective_date == effective_date
            ).first()

            # Jeśli kurs waluty o danym kodzie i dacie obowiązywania nie istnieje w bazie danych następuje jego dodanie do bazy danych
            if not existing_rate:
                new_rate = CurrencyRate(
                    currency=rate['currency'],
                    code=rate['code'],
                    mid=rate['mid'],
                    effective_date=effective_date
                )
                db.add(new_rate) # Dodanie nowego kursu waluty do sesji bazy danych
                added_count += 1 # Zwiększenie licznika dodanych kursów walut

        # Zatwierdzenie zmian w bazie danych
        db.commit()

        return {"message": f"Pobrano i zapisano {added_count} nowych kursów walut z API NBP z dnia {effective_date}."}
    else:
        # Jeśli odpowiedź z API NBP nie jest poprawna następuje zwrócenie błędu HTTP 500 z odpowiednim komunikatem
        raise HTTPException(status_code=500, detail="Nie można pobrać danych z API NBP")


# Endpoint do pobierania aktualnych kursów walut z API NBP
@app.get("/currencies")
def get_currencies():
    # Zdefiniowanie URL do API NBP, które zwraca aktualne kursy walut w formacie JSON
    url = "http://api.nbp.pl/api/exchangerates/tables/A/?format=json"

    # Wysłanie żądania GET do API NBP
    response = requests.get(url)

    # Sprawdzenie, czy odpowiedź z API jest poprawna (status code 200)
    if response.status_code == 200:
        # Parsowanie odpowiedzi JSON i wyciągnięcie kursów walut
        data = response.json()
        rates = data[0]['rates']
        return {"currencies": rates}
    else:
        # Jeśli odpowiedź z API NBP nie jest poprawna następuje zwrócenie błędu HTTP 500 z odpowiednim komunikatem
        raise HTTPException(status_code=500, detail="Nie można pobrać danych z API NBP")
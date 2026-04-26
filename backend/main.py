import requests
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import CurrencyRate

# Utworzenie bazy danych i tabel, jeśli jeszcze nie istnieją
Base.metadata.create_all(bind=engine)

# Stworzenie głównej instancji aplikacji FastAPI
app = FastAPI(title="Currency Dashboard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], # Adres pod którym będzie działać frontend Angular
    allow_credentials=True,
    allow_methods=["*"], # Pozwolenie na wszystkie metody HTTP (GET, POST, itp.)
    allow_headers=["*"]
)

# Endpoint do pobierania aktualnych kursów walut z API NBP i zapisywania ich do bazy danych
@app.post("/currencies/fetch")
def fetch_and_save_currencies(days: int = 1, db: Session = Depends(get_db)):
    # Adres URL do API NBP, który zwraca kursy walut z ostatnich X dni w formacie JSON
    url = f"http://api.nbp.pl/api/exchangerates/tables/A/last/{days}/?format=json"

    # Wysłanie żądania GET do API NBP
    response = requests.get(url)

    # Sprawdzenie, czy odpowiedź z API jest poprawna (status code 200)
    if response.status_code == 200:
        data = response.json()
        added_count = 0 # Licznik dodanych kursów walut do bazy danych
        
        for table_data in data:
            effective_date_str = table_data['effectiveDate'] # Pobranie daty obowiązywania kursów walut w formacie string
            effective_date = datetime.strptime(effective_date_str, "%Y-%m-%d").date() # Konwersja daty z formatu string na obiekt datetime.date
            rates = table_data['rates'] # Pobranie listy kursów walut z odpowiedzi API NBP

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
        return {"message": f"Pobrano i zapisano {added_count} nowych kursów z ostatnich {days} notowań."}
    else:
        # Jeśli odpowiedź z API NBP nie jest poprawna następuje zwrócenie błędu HTTP 500 z odpowiednim komunikatem
        raise HTTPException(status_code=500, detail="Nie można pobrać danych z API NBP")
    

@app.get("/currencies")
def get_available_currencies(db: Session = Depends(get_db)):
    # Pobranie unikalnych kodów walut dostępnych w bazie danych
    currencies = db.query(CurrencyRate.code, CurrencyRate.currency).distinct().all()

    # Konwersja wyników zapytania do listy kodów walut
    return [{"code": c.code, "currency": c.currency} for c in currencies]


@app.get("/currencies/{date}")
def get_currencies_by_date(date: str, db: Session = Depends(get_db)):
    # Konwersja daty z formatu string na obiekt datetime
    # Jeśli format daty jest nieprawidłowy, zostanie zwrócony błąd HTTP 400 z odpowiednim komunikatem
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Nieprawidłowy format daty. Użyj formatu YYYY-MM-DD.")
    
    # Pobranie kursów walut z bazy danych dla podanej daty obowiązywania
    # Jeśli nie zostaną znalezione żadne kursy walut dla podanej daty, zostanie zwrócony błąd HTTP 404 z odpowiednim komunikatem
    rates = db.query(CurrencyRate).filter(CurrencyRate.effective_date == target_date).all()
    if not rates:
        raise HTTPException(status_code=404, detail=f"Nie znaleziono kursów walut dla daty {date}.")
    
    # Konwersja wyników zapytania do listy słowników zawierających informacje o kursach walut
    return [
        {
            "id": r.id,
            "code": r.code,
            "currency": r.currency,
            "mid": r.mid,
            "effective_date": r.effective_date
        } for r in rates
    ]

# Endpoint do pobierania historii kursów walut z bazy danych, posortowanej malejąco według daty obowiązywania
@app.get("/currencies/history/all")
def get_all_history(db: Session = Depends(get_db)):
    rates = db.query(CurrencyRate).order_by(CurrencyRate.effective_date.desc()).all()

    return [
        {
            "id": r.id,
            "code": r.code,
            "currency": r.currency,
            "mid": r.mid,
            "effective_date": r.effective_date
        } for r in rates
    ]
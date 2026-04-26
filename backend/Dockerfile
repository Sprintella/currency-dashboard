# Użycie oficjalnego obrazu Pythona w wersji 3.10
FROM python:3.10-slim
# Ustawienie katalogu roboczego w kontenerze na /app
WORKDIR /app
# Skopiowanie pliku requirements.txt z lokalnego systemu do katalogu roboczego w kontenerze
COPY requirements.txt .
# Instalacja zależności z pliku requirements.txt bez użycia cache, co pozwala na mniejsze rozmiary obrazów Dockera
RUN pip install --no-cache-dir -r requirements.txt
# Skopiowanie wszystkich plików z lokalnego systemu do katalogu roboczego w kontenerze
COPY . .
# Otwarcie portu 8000, na którym będzie działać aplikacja FastAPI
EXPOSE 8000
# Uruchomienie aplikacji FastAPI za pomocą Uvicorn, nasłuchującej na wszystkich interfejsach sieciowych (0.0.0.0) i porcie 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
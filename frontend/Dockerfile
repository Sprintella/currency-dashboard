# Użycie oficjalnego obrazu Node.js w wersji 20 na bazie Alpine Linux, który jest lekki i zoptymalizowany pod kątem bezpieczeństwa
FROM node:20-alpine
# Ustawienie katalogu roboczego w kontenerze na /app
WORKDIR /app
# Skopiowanie plików package.json i package-lock.json z lokalnego systemu do katalogu roboczego w kontenerze
COPY package*.json ./
# Instalacja pakietów Angulara
RUN npm install
# Skopiowanie wszystkich plików z lokalnego systemu do katalogu roboczego w kontenerze
COPY . .
# Otwarcie portu 4200, na którym będzie działać aplikacja Angular
EXPOSE 4200
# Uruchomienie aplikacji Angular za pomocą polecenia ng serve, nasłuchującej na wszystkich interfejsach sieciowych (0.0.0.0) i porcie 4200
CMD ["npx", "ng", "serve", "--host", "0.0.0.0"]
Feature: Pobieranie kursów walut z NBP

    Scenario: Użytkownik pobiera dzisiejsze kursy i zapisuje je w bazie
      Given Baza danych jest pusta
      When Użytkownik wysyła zadanie pobrania kursów z ostatnich "1" dni
      Then API powinno zwrócić kod sukcesu 200
      And Baza danych powinna zawierać nowe rekordy
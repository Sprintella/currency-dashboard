import { Component, inject, ChangeDetectorRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  http = inject(HttpClient); // Wskrzyknięcie HttpClient do komponentu
  cdr = inject(ChangeDetectorRef); // Wskrzyknięcie ChangeDetectorRef do ręcznego wywoływania detekcji zmian
  rates: any[] = []; // Tablica do przechowywania danych o walutach
  isLoading: boolean = false; // Flaga do zarządzania stanem ładowania danych
  message: string = ''; // Zmienna do przechowywania komunikatów o błędach lub innych informacji

  // Metoda do pobierania danych z NBP
  fetchFromNBP() {
    this.isLoading = true; // Ustawienie flagi ładowania na true
    this.message = 'Pobieranie danych z NBP...'; // Ustawienie komunikatu o pobieraniu danych

    this.http.post('http://127.0.0.1:8000/currencies/fetch', {}).subscribe({
      next: (response: any) => {
        this.message = response.message; // Ustawienie komunikatu z odpowiedzi serwera
        this.isLoading = false; // Ustawienie flagi ładowania na false
        this.cdr.detectChanges(); // Ręczne wywołanie detekcji zmian, aby zaktualizować widok
      },
      error: (error) => {
        this.message = 'Wystąpił błąd podczas pobierania danych z NBP'; // Ustawienie komunikatu o błędzie
        this.isLoading = false; // Ustawienie flagi ładowania na false
        this.cdr.detectChanges(); // Ręczne wywołanie detekcji zmian, aby zaktualizować widok
      }
    });
  }

  getRatesForDate(date: string) {
    if (!date) {
      this.message = 'Proszę wybrać datę'; // Ustawienie komunikatu, jeśli data nie została wybrana
      return;
    }

    this.isLoading = true; // Ustawienie flagi ładowania na true
    this.message = `Pobieranie danych dla daty ${date}...`; // Ustawienie komunikatu o pobieraniu danych dla wybranej daty

    this.http.get(`http://127.0.0.1:8000/currencies/${date}`).subscribe({
      next: (data: any) => {
        this.rates = data; // Przypisanie pobranych danych do tablicy rates
        this.message = `Znaleziono w bazie ${data.length} walut dla daty ${date}`; // Ustawienie komunikatu o liczbie znalezionych walut
        this.isLoading = false; // Ustawienie flagi ładowania na false
        this.cdr.detectChanges(); // Ręczne wywołanie detekcji zmian, aby zaktualizować widok
      },
      error: (error) => {
        this.rates = []; // Czyszczenie tablicy rates w przypadku błędu
        this.message = `Wystąpił błąd podczas pobierania danych dla daty ${date}`; // Ustawienie komunikatu o błędzie
        this.isLoading = false; // Ustawienie flagi ładowania na false
        this.cdr.detectChanges(); // Ręczne wywołanie detekcji zmian, aby zaktualizować widok
      }
    });
  }
}
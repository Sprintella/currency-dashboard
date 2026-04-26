import { Component, inject, ChangeDetectorRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  // Wskrzyknięcie HttpClient do komponentu
  http = inject(HttpClient);
  cdr = inject(ChangeDetectorRef); // Wskrzyknięcie ChangeDetectorRef do ręcznego wywoływania detekcji zmian

  // Tablica do przechowywania danych o walutach
  currencies: any[] = [];

  isLoading: boolean = false; // Flaga do zarządzania stanem ładowania danych

  // Metoda do pobierania danych z backendu
  fetchData() {
    this.isLoading = true; // Ustawienie flagi ładowania na true

    this.http.get('http://127.0.0.1:8000/currencies').subscribe({
      next: (data: any) => {
        this.currencies = data; // Przypisanie pobranych danych do zmiennej currencies
        this.isLoading = false; // Ustawienie flagi ładowania na false po zakończeniu pobierania danych

        this.cdr.detectChanges(); // Ręczne wywołanie detekcji zmian, aby Angular zaktualizował widok po otrzymaniu danych
      },
      error: (error) => {
        console.error('Error fetching data:', error);
        this.isLoading = false; // Ustawienie flagi ładowania na false w przypadku błędu
        this.cdr.detectChanges(); // Ręczne wywołanie detekcji zmian, aby Angular zaktualizował widok po wystąpieniu błędu
      }
    });
  }
}

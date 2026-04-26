import { Component, inject, ChangeDetectorRef, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App implements OnInit {
  http = inject(HttpClient); // Wskrzyknięcie HttpClient do komponentu
  cdr = inject(ChangeDetectorRef); // Wskrzyknięcie ChangeDetectorRef do ręcznego wywoływania detekcji zmian

  isLoading: boolean = false; // Flaga do zarządzania stanem ładowania danych
  message: string = ''; // Zmienna do przechowywania komunikatów o błędach lub innych informacji

  allRates: any[] = []; // Tablica do przechowywania wszystkich kursów walut
  filteredRates: any[] = []; // Tablica do przechowywania przefiltrowanych kursów walut
  totalCount: number = 0; // Zmienna do przechowywania całkowitej liczby wpisów w bazie

  // Zmienne do filtrowania danych
  selectedYear: string = '';
  selectedQuarter: string = '';
  selectedMonth: string = '';
  selectedDay: string = '';

  availableYears = ['2026', '2025', '2024']; // Tablica do przechowywania dostępnych lat w danych
  quarters = [
    { id: '1', name: 'I Kwartał' }, { id: '2', name: 'II Kwartał' },
    { id: '3', name: 'III Kwartał' }, { id: '4', name: 'IV Kwartał' }
  ];
  months = [
    'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 
    'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'
  ];

  // Metoda wywoływana automatycznie po włączeniu strony
  ngOnInit() {
    this.getAllHistory();
  }

  // Metoda do pobierania danych z NBP
  fetchFromNBP(days: number = 1) {
    this.isLoading = true; // Ustawienie flagi ładowania na true
    this.message = `Łączenie z NBP (pobieranie danych z ostatnich ${days} dni)...`; // Ustawienie komunikatu o pobieraniu danych

    this.http.post(`http://127.0.0.1:8000/currencies/fetch?days=${days}`, {}).subscribe({
      next: (response: any) => {
        this.message = response.message; // Ustawienie komunikatu z odpowiedzi serwera
        this.getAllHistory(true); // Pobranie wszystkich danych po udanym pobraniu z NBP. True oznacza brak komunkatu o pobieraniu historii
        this.cdr.detectChanges(); // Ręczne wywołanie detekcji zmian, aby zaktualizować widok
      },
      error: (error) => {
        this.message = 'Wystąpił błąd podczas pobierania danych z NBP';
        this.isLoading = false; // Ustawienie flagi ładowania na false
        this.cdr.detectChanges(); // Ręczne wywołanie detekcji zmian, aby zaktualizować widok
      }
    });
  }

  // Metoda do pobierania całej historii kursów walut z bazy danych
  getAllHistory(silent: boolean = false) {
    if (!silent) {
      this.isLoading = true; // Ustawienie flagi ładowania na true
      this.message = 'Pobieranie historii kursów walut...'; // Ustawienie komunikatu o pobieraniu historii
    }

    this.http.get('http://127.0.0.1:8000/currencies/history/all').subscribe({
      next: (data: any) => {
        this.allRates = data; // Przypisanie pobranych danych do tablicy allRates
        this.totalCount = data.length; // Ustawienie całkowitej liczby wpisów w bazie

        if (!silent) {
          this.message = 'Pobieranie historii kursów walut zakończone.';
        }

        this.isLoading = false; // Ustawienie flagi ładowania na false
        this.applyFilters(); // Zastosowanie filtrów do pobranych danych
        this.cdr.detectChanges(); // Ręczne wywołanie detekcji zmian, aby zaktualizować widok
      },
      error: (error) => {
        this.message = 'Wystąpił błąd podczas pobierania historii kursów walut';
        this.isLoading = false; // Ustawienie flagi ładowania na false
        this.cdr.detectChanges(); // Ręczne wywołanie detekcji zmian, aby zaktualizować widok
      }
    });
  }

  // Metoda do filtrowania danych na podstawie wybranych kryteriów
  applyFilters() {
    this.filteredRates = this.allRates.filter(rate => {
      // Rozdzielenie daty na części (rok, miesiąc, dzień)
      const dateParts = rate.effective_date.split('-');
      const year = dateParts[0];
      const month = parseInt(dateParts[1], 10);

      // Obliczenie kwartału na podstawie miesiąca
      const quarter = Math.ceil(month / 3).toString();

      // Sprawdzenie, czy dany rekord pasuje do wybranych filtrów
      const matchYear = this.selectedYear ? year === this.selectedYear : true;
      const matchQuarter = this.selectedQuarter ? quarter === this.selectedQuarter : true;
      const matchMonth = this.selectedMonth ? month.toString() === this.selectedMonth : true;
      const matchDay = this.selectedDay ? rate.effective_date === this.selectedDay : true;

      return matchYear && matchQuarter && matchMonth && matchDay;
    });
  }

  clearFilters() {
    this.selectedYear = '';
    this.selectedQuarter = '';
    this.selectedMonth = '';
    this.selectedDay = '';
    this.applyFilters(); // Po wyczyszczeniu filtrów następuje ponowne zastosowanie filtrów, aby pokazać wszystkie dane
  }
}
/// <reference types="jasmine" />

import { TestBed, ComponentFixture } from '@angular/core/testing';
import { App } from './app';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { By } from '@angular/platform-browser';

describe('App', () => {
  let component: App;
  let fixture: ComponentFixture<App>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(App);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('Powinien wywołać funkcję pobierania po kliknięciu przycisku (NBP)', () => {
    spyOn(component, 'fetchFromNBP');

    const buttonDebug = fixture.debugElement.query(By.css('.btn-primary'));
    buttonDebug.triggerEventHandler('click', null);

    expect(component.fetchFromNBP).toHaveBeenCalledWith(1); // Sprawdzenie, czy funkcja została wywołana z parametrem 1
  });

  it('Powinien poprawnie wyświetlać dane w tabeli', () => {
    // Podstawienie sztucznych danych, aby wymusić na Angularze narysowanie tabeli
    component.filteredRates = [
      { id: 1, effective_date: '2026-04-24', code: 'USD', currency: 'dolar amerykanski', mid: 4.05 }
    ];

    fixture.detectChanges(); // Wymuszenie przerywania widoku HTML

    const tableRows = fixture.debugElement.queryAll(By.css('tbody tr'));
    expect(tableRows.length).toBe(1); // Tabela powinna mieć dokładnie 1 wiersz

    // Wyciągnięcie komórek z pierwszego wiersza i sprawdzenie ich zawartości
    const rowCells = tableRows[0].queryAll(By.css('td'));
    expect(rowCells[0].nativeElement.textContent.trim()).toBe('2026-04-24');
    expect(rowCells[1].nativeElement.textContent.trim()).toBe('USD');
  });
});
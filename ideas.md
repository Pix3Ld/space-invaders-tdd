pygame space invaders trudnawe + łatwo zrobić unittesty automatyczne  


## 2. Sposób bieżącej kontroli wyników nauczania

Na zakończenie (i zaliczenie) zajęć do wykonania będzie projekt zaliczeniowy i jego obrona.
Możliwa jest dodatkowa odpytka w celu wyjaśnienia wątpliwości co do samodzielności wykonania
pracy. Zalecane jest dobrze znać swój projekt :)

### 3.1 Aplikacja

1. Aplikacja powinna składać się z minimum 3 modułów (plików .py).
2. Każdy moduł powinien zawierać co najmniej 2 klasy lub funkcje.
3. Aplikacja może obsługiwać podstawowe operacje wejścia/wyjścia (np. odczyt/zapis do
pliku, interakcja z użytkownikiem).
4. Kod powinien być zgodny z konwencją PEP 8.
5. Należy zastosować obsługę wyjątków.
6. Jeśli zastosowano konstrukcję type hinting (wskazywanie typów), to musi być stosowana
konsekwetnie. Jej stosowanie nie jest obowiązkowe.

### 3.2 Testy jednostkowe


1. Testy należy zaimplementować przy użyciu bibliotek omawianach na ćwiczeniach.
2. Łącznie należy stworzyć ok. 100-150 różnorodnych testów.
3. Należy zastosować minimum 5 różnych rodzajów asercji.
4. Wymagane jest użycie parametryzacji testów.
5. Testy powinny być zorganizowane w logiczne grupy za pomocą klas testowych.
6. Kod testów powinien być zgodny z konwencją PEP 8.
7. Należy zaimplementować testy negatywne (sprawdzające obsługę błędów).
8. Należy osiągnąć pokrycie kodu testami na poziomie minimum 80%.

### 3.3 Kryteria oceny

#### 3.3.1 Kod aplikacji (30 pkt)
1. Zgodność z wymaganiami technicznymi (5 pkt)
2. Jakość i czytelność kodu (10 pkt)
3. Poprawność działania aplikacji (10 pkt)
4. Odpowiednia struktura projektu (5 pkt)

#### 3.3.2 Testy jednostkowe (60 pkt)
1. Kompletność testów (czy wszystkie funkcjonalności są testowane) (10 pkt)
2. Różnorodność rodzajów testów (5 pkt)
3. Poprawność implementacji testów (30 pkt)
4. Zastosowanie zaawansowanych technik testowania (5pkt)
5. Osiągnięcie wymaganego pokrycia kodu (10 pkt)

#### 3.3.3 Obrona projektu (10pkt)
1. Odpowiedź na zadanie pytania do oddanego projektu (10 pkt)
> !!! UWAGA !!!
>
> Jeżeli w tym kroku zostanie wykryta niesamodzielność pracy to skutkuje to
> wyzerowaniem punktów z projektu zaliczeniowego!

Obrona projektu będzie dokonana w trakcie zajęć przy innych osobach

### 3.4 Przykładowa struktura projektu

```text
projekt/
    src/
        __init__.py
        modul_1.py
        modul_2.py
        modul_3.py
    tests/
        __init__.py
        test_modul_1.py
        test_modul_2.py
        test_modul_3.py
    requirements.txt
    README.md
```

## 4. Termin i forma oddania projektu

1. Projekt należy oddać w formie spakowanego kodu do wystawionego zadania na utworzonym zespole MS Teams.
2. Termin oddania: 27.05.2025 do godz 23:59
3. Projekt powinien zawierać plik README.md z krótką dokumentacją (nie rozwijajmy się za specjalnie w tym kroku - ważne, aby było opis czego dotyczy aplikacja, co robi, jak uruchomić i apkę i testy, itd.)
4. W arcxhiwum (preferowany zip) powinien znajdować się plik requirements.txt z listą zależności (potrzebnych bibliotek, ich wersji, wersji pythona itd.)

## 5. Przykładowe tematy aplikacji

1. System zarządzania biblioteką.
2. Aplikacja do zarządzania zadaniami (todo list).
3. Prosty system bankowy.
4. Kalkulator z zaawansowanymi funkcjami.
5. Parser danych w określonym formacie (CSV, JSON, XML).
6. Gra tekstowa.
7. System rezerwacji (hoteli, biletów, etc.).
8. API do konwersji walut.

Można oczywiście swoje aplikacje.

Przykładowy projekt od [Pana Doktora Jastrzębskiego](https://github.com/pjastr/PFsample), który jest zdecydowanie mniejszą skalą niżli projekt do wykonania na zaliczenie przedmiotu - **proszę zwracać uwagę na wymagania co do zaliczenia!!!!**

## Uwagi dodatkowe

1. Projekt jest indywidualny.
2. Konsultacje w sprawie projektu możliwe są podczas zajęć oraz w godzinach konsultacji.
3. Ocena uwzględnia terminowość oddania projektu.
4. Plagiat/niesamodzielność skutkuje niezaliczeniem projektu.

## 6. Możliwość korzystania z materiałów pomocniczych podczas zaliczenia

Można korzystać z dowolnych materiałów o ile ich licencja umożliwia skorzystanie z nich na cele edukacyjne. Wszystkie wykorzystane materiały powinny być odpowiednio [oznaczone](https://piojas.pl/wp-content/uploads/2025/03/licencje-1.pdf) - skąd wzięte, jaka licencja, link, itd. . W trakcie obrony projektu wgląd będzie tylko do własnego kodu i dokumentacji bibliotek. Oceniana również będzie tylko część wykonana samodzielnie przez osobę studencką.

## 7. Zasada ustalania oceny końcowej zaliczenia przedmiotu

Zaliczenie ćwiczeń będzie przyznane tym uczestnikom zajęć, którzy uzyskają sumę co najmniej 51 punktów do oceny końcowej. Maksymalna
liczba punktów do zdobycia to 100 (nadmiarowe punkty, o ile takowe będą, nie będą uwzględniane). Ocena końcowa zostanie wyznaczona według następującego wzoru:
```
0  – 50 pkt   – ndst (2,0)
51 – 60 pkt   – dst  (3,0)
61 – 70 pkt   – dst+ (3,5)
71 – 80 pkt   – db   (4,0)
81 – 90 pkt   – db+  (4,5)
91 – 100+ pkt – bdb  (5,0)
```

Z przedmiotu w zakresie ćwiczeń nie jest przewidzian poprawa (Chyba, że ktoś zdąży do końca zajęć poprawić projekt, bo nie zaliczył - jestem skory do niektórych pertrakcji :) )

## 8. Inne

Wszystkie sprawy nieuregulowane lub sporne rozstrzyga koordynator przedmiotu (poza sytuacjami określonymi w odrębnych przepisach).

## Prawdopodobny rozkład zajęć

1. 25.02: Sylabus. Wprowadzenie do unittest cz. 1.
2. 04.03: Wprowadzenie do unittest cz. 2 - dokańczanie zadań.
3. 11.03: TDD w unittest
4. 18.03: Analiza statyczna, wyrażenia regularne
5. 25.03: Atrapy obiektów (mock) w testowaniu modułowym
6. 01.04: Pokrycie kodu (moduł coverage)
7. 15.04: Techniki testowania
8. 22.04: Moduł pytest 
9. 29.04: Moduł pytest-bdd
10. 06.05: Analiza wartości brzegowych
11. 13.05: Przejścia miedzy stanami
12. 20.05: Praca nad projektami cz. 1. Konsultacje projektowe.
13. 27.05: Praca nad projektami cz. 2. Konsultacje projektowe.
14. 03.06: Obrona projektów cz. 1.
15. 10.06: Obrona projektów cz. 2.


## Literatura

1.  Roman, A., Stapp, L., & Pilaeten, M. (2024). Certyfikowany tester ISTQB Poziom
podstawowy (wyd. II) [Certyfikowany tester ISTQB: Poziom podstawowy]. Helion.
2. Stapp, L., & Roman, A. (2024). Certyfikowany tester ISTQB. Poziom podstawowy.
Pytania i odpowiedzi. Helion.
3. Jadczyk, K. (2021). Pasja testowania. Wydanie II rozszerzone. Helion.
4. Pajankar, A. (2017). Python unit test automation: Automate, organize, and execute
unit tests in Python. Apress.
5. Dooley, J. F., & Kazakova, V. A. (2020). Software development, design, and coding:
With patterns, debugging, unit testing, and refactoring. Apress

<br>

## Kontakt
mgr inż. Adrian Albrecht:
- chat (wiadomość prywatna) na MS Teams
- mail 📧 [adrian.albrecht@matman.uwm.edu.pl](mailto:adrian.albrecht@matman.uwm.edu.pl)
- Konsultacje: środa 13:30 – 16:30 (czasami możliwe wtorki od 11:30 po wcześniejszym ustaleniu)
    - sala E1/20 (lub inna ustalona wcześniej z osobami studenckimi sala w przypadku konsultacji zbiorowych) 



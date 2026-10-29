# Lotto Lab — archiwum i statystyki

Statyczna strona GitHub Pages do analizy Lotto 6/49. Zawiera **101 ręcznie przepisanych wyników z przesłanych zrzutów ekranu** (numery 7323–7423), w tym losowanie z 27.10.2026. Daty historyczne w tych rekordach są puste — zachowano numery losowań i liczby. Nie deklarujemy 500 rekordów, dopóki automat ich nie pobierze.

## Uruchomienie

1. Utwórz publiczne repozytorium GitHub, wgraj **całą zawartość folderu** (także `.github/workflows/update.yml`, `scripts/update.py`, `data/draws.json`).
2. W repozytorium wejdź w **Settings → Pages → Build and deployment → Deploy from a branch**, wybierz `main` i `/ (root)`.
3. W **Actions → Aktualizacja wyników Lotto → Run workflow** uruchom pierwszy import ręcznie. Włącz Actions, jeśli GitHub o to poprosi.
4. Po wykonaniu workflow odśwież stronę. Sprawdź licznik wczytanych wyników. Automat próbuje pobrać ostatnie lata i zapisuje **maksymalnie 500** najnowszych losowań.

## Jak działa aktualizacja

GitHub Actions uruchamia skrypt dwa razy wokół nocy po losowaniu (harmonogram UTC, więc aktualizacja może nastąpić z opóźnieniem). Skrypt pobiera publiczne tabele archiwum `mbnet.com.pl`, sprawdza numery, daty, unikalność i zakres 1–49, usuwa duplikaty i zapisuje do `data/draws.json`. Jeśli strona archiwum zmieni strukturę lub zablokuje pobieranie, workflow może się nie powieść; dotychczasowe dane zostają zachowane. GitHub Pages nie uruchamia kodu Python w przeglądarce — robi to GitHub Actions.

Dane z archiwum **nie są oficjalnym API**. Oficjalne LOTTO OpenAPI wymaga indywidualnego klucza API: https://developers.lotto.pl/. Nie umieszczaj takiego klucza w publicznym HTML. Przed użyciem wyników w grze zweryfikuj je z https://www.lotto.pl/.

## Bezpieczeństwo i ograniczenia

- Lokalnie dodane wyniki są zapisywane w `localStorage` **tylko na danym urządzeniu** i nadpisują identyczne numery z pliku zdalnego; eksport JSON pozwala wykonać kopię.
- Backtest porównuje metody na wcześniejszych wynikach, ale nie dowodzi przewidywania losowań.
- Wszystkie zestawy 6 z 49 mają identyczne prawdopodobieństwo trafienia szóstki.
- Zmiany struktury źródła mogą wymagać aktualizacji parsera w `scripts/update.py`.


## Wersja 3.0
Dodano analizę parzystych/nieparzystych, rozkład liczby parzystych w szóstce, medianę i zakres sum, generator łączony (częstotliwość + rzędy + średnia + parzystość) oraz jego backtest. Generator dopasowuje opisowe cechy historyczne, ale nie przewiduje losowań.

## Wersja 4.0
Jeden generator łączy sumę/średnią, rzędy, parzystość, częstotliwość, współwystępowanie par i przerwy. Dodatkowo zestawia okresy 20/50/100/500 oraz testuje generator z losowym punktem odniesienia. Losowe przeszukiwanie kandydatów daje różne szóstki przy kolejnych kliknięciach. Dane startowe: 101 rekordów ze zdjęć, 7323–7423; do 500 rozbuduje je workflow dopiero po uruchomieniu i udanym pobraniu.

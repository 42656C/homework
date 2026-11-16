# Mini-raport podatności

## LAB24 - SQL INJECTION, UNION,COMMAND DVWA oraz JUICE SHOP

## Nazwa podatności

SQL Injection (SQLi) w DVWA, z możliwością odczytu danych przez UNION-based SQL Injection. W laboratorium sprawdzono również Command Injection w DVWA oraz obejście logowania w Juice Shop.

## Środowisko

- System: Kali Linux, aplikacje uruchomione lokalnie w kontenerach Docker.
- DVWA: `http://127.0.0.1:8080`, moduł `SQL Injection`, początkowo poziom `Low`.
- Juice Shop: `http://127.0.0.1:3000`.
- Narzędzia: przeglądarka Firefox, DevTools oraz SQLMap.

## Opis podatnosci

Parametr `id`, przesyłany metodą `GET` do `/vulnerabilities/sqli/`. W osobnym teście Command Injection podatnym wejściem było pole adresu IP.

## Kroki odtworzenia (DVWA SQL Injection)

1. Zalogowano się do lokalnego DVWA i ustawiono poziom `Low`.
2. W module `SQL Injection` podano `1` jako wartość kontrolną — zwrócono konto `admin`.
3. Wprowadzono `1' OR '1'='1` — aplikacja wyświetliła pięć rekordów zamiast jednego.
4. Przeprowadzono test UNION i potwierdzono możliwość odczytu danych z tabeli `users`.
5. SQLMap potwierdził podatność parametru `id`; w kontrolowanym ćwiczeniu rozpoznano bazy, tabele i kolumny.
6. Zmieniono poziom na `High` i porównano wyniki: widoczny był jeden rekord, a test UNION zakończył się komunikatem `Something went wrong.`.

## Obserwowane rezultaty

Na poziomie `Low` aplikacja traktowała wejście jako część zapytania SQL. SQLMap wskazał cztery techniki SQL Injection: boolean-based blind, error-based, time-based blind i UNION query. Wykryto bazy `dvwa` i `information_schema` oraz tabele `guestbook` i `users`. W wyznaczonym środowisku odczytano pięć testowych rekordów użytkowników, w tym hashe haseł; hasła do przykładowych kont odzyskano testem słownikowym. Na poziomie `High` poprzednie próby zwróciły mniej danych lub komunikat błędu, co samo w sobie nie dowodzi usunięcia podatności.

W dodatkowym teście Command Injection wynik `whoami` wskazał `www-data`, a aplikacja pozwoliła odczytać `/etc/passwd`. W Juice Shop test wykazał obejście logowania i zalogowanie na konto `admin@juice-sh.op`.

## Wpływ

Podatność SQL Injection może prowadzić do ujawnienia informacji o użytkownikach i hashy haseł, a w innych warunkach także do zmiany danych. Command Injection może umożliwiać wykonywanie poleceń z uprawnieniami procesu aplikacji. Obejście logowania może skutkować nieuprawnionym dostępem do konta administratora.

## Rekomendacja

Stosować zapytania parametryzowane (prepared statements), walidację danych, allow-listy SQL i minimalne uprawnienia konta bazy. Nie pokazywać użytkownikowi szczegółowych błędów SQL i nie przechowywać haseł przy użyciu funkcji skrótu takich jak MD5 — do haseł używać m.in. Argon2id. Przy funkcjach systemowych unikać wywołań powłoki, przekazywać argumenty jako listę i ograniczać uprawnienia procesu. Wdrożyć logowanie zdarzeń bezpieczeństwa.

## Zakres testów

Wszystkie działania przeprowadzono wyłącznie w autoryzowanym, lokalnym laboratorium DVWA/Juice Shop. Odczyt przykładowych rekordów i hashy, kontrolowane polecenia systemowe oraz próba obejścia logowania dotyczyły wyłącznie środowiska laboratoryjnego.

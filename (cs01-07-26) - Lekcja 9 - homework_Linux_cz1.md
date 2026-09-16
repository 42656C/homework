# Laboratorium 09 — polecenia do wykonania

## Przygotowanie katalogu roboczego

1. Utwórz katalog `work`.
cd lab-linux
mkdir -p work
2. Skopiuj katalog `materials/linux-lab` do `work/linux-lab`, zachowując atrybuty plików.
cp -a /home/vboxuser/lab-linux/linux-lab /home/vboxuser/lab-linux/work/linux-lab
3. Przejdź do `work/linux-lab`.
cd work/linux-lab
4. Wyświetl bieżącą ścieżkę.
pwd
5. Wyświetl szczegółową listę plików, również ukrytych.
ls -la

## 1. Rozpoznanie dystrybucji, kernela i architektury

1. Wyświetl zawartość `/etc/os-release`.
cat /etc/os-release
2. Zanotuj wartości `PRETTY_NAME`, `ID`, `VERSION_ID`, jeśli występuje, oraz `VERSION_CODENAME`, jeśli występuje.
PRETTY_NAME="Ubuntu 26.04 LTS"
ID=ubuntu
ID_LIKE=debian
VERSION_ID="26.04"
VERSION_CODENAME=resolute
3. Sprawdź wersję kernela.
uname -r
"VERSION_CODENAME=resolute"
4. Sprawdź architekturę systemu.
uname -m
x86_64
5. Sprawdź główną architekturę pakietów.
dpkg --print-architecture
amd64
6. Sprawdź dodatkowe architektury pakietów.
dpkg --print-foreign-architectures
7. Jeśli narzędzie `hostnamectl` jest dostępne, wyświetl informacje o systemie.
 Static hostname: Ubuntu
       Icon name: computer-vm
         Chassis: vm 🖴
      Machine ID: bf14bb0302954b509fcde3d95c867a0b
         Boot ID: b4609d06de014977a1d4cdf11eb4f002
  Virtualization: oracle
Operating System: Ubuntu 26.04 LTS                
          Kernel: Linux 7.0.0-30-generic
    Architecture: x86-64
 Hardware Vendor: innotek GmbH
  Hardware Model: VirtualBox
Hardware Version: 1.2
Firmware Version: VirtualBox
   Firmware Date: Fri 2006-12-01
    Firmware Age: 19y 9month 2w 1d   
8. Odpowiedz, czy wersja uzyskana przez `uname -r` dotyczy dystrybucji, czy kernela.
Wersje kernela
9. Porównaj nazwę architektury uzyskaną przez `uname -m` z nazwą zwracaną przez `dpkg --print-architecture`.
x86_64 vs amd64
10. Określ, czy pracujesz na systemie ogólnego przeznaczenia, czy dystrybucji specjalistycznej.
Jest to system ogolnego przeznaczenia, nie wersja specjalistyczna
11. Określ, czy środowisko wygląda na maszynę wirtualną, kontener, system live czy pełną instalację.
Po poleceniu: "hostnamectl": Virtualization: oracle
12. Przygotuj notatkę zawierającą dystrybucję, wydanie lub kryptonim, kernel, architekturę systemu, architekturę pakietów oraz model wydania.
Dystrybucja: Ubuntu
Wydanie: Ubuntu 26.04 LTS
Kryptonim: Resolute Raccon
Kernel: resolute
Architektura systemu: x86_64
Architektura pakietow: amd64
Model wydania: LTS (Long Term Support)

## 2. Terminal, powłoka i składnia polecenia

1. Sprawdź urządzenie terminala.
tty
/dev/pts/1
2. Sprawdź rozmiar terminala.
stty size
24 80
3. Wyświetl wartość zmiennej `TERM`.
printf '%s\n' "$TERM"
xterm-256color
4. Wyświetl wartość zmiennej `SHELL`.
printf '%s\n' "$SHELL"
/bin/bash
5. Sprawdź nazwę procesu aktualnej powłoki.
ps -p $$ -o comm=
bash
6. Sprawdź typ polecenia `cd`.
type cd
cd is a shell builtin
7. Sprawdź typ polecenia `grep`.
type grep
grep is aliased to `grep --color=auto'
8. Znajdź ścieżkę programu `grep`.
which grep
/usr/bin/grep
9. Wyświetl wartość zmiennej `PATH`.
printf '%s\n' "$PATH"
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin
10. Uruchom polecenie `true` i wyświetl jego kod zakończenia z etykietą „Kod po true”.
true
echo "Kod po true: $?"
Kod po true: 0
11. Uruchom polecenie `false` i wyświetl jego kod zakończenia z etykietą „Kod po false”.
false
echo "Kod po false: $?"
Kod po false: 1
12. Wyszukaj tekst `ERROR` w `logs/application.log` i wyświetl kod zakończenia z etykietą „Kod po grep z trafieniem”.
grep "ERROR" logs/application.log; echo "Kod po grep z trafieniem: $?"
2026-07-18T08:12:43Z ERROR app=portal component=db message="connection timeout" retry=1
2026-07-18T08:47:55Z ERROR app=portal src=198.51.100.23 action=request path=/api/debug status=404
Kod po grep z trafieniem: 0
13. Wyszukaj tekst `NIE_MA_TAKIEGO_TEKSTU` w `logs/application.log` i wyświetl kod zakończenia z etykietą „Kod po grep bez trafienia”.
grep "NIE_MA_TAKIEGO_TEKSTU" logs/application.log; echo "Kod po grep bez trafienia: $?"
Kod po grep bez trafienia: 1
14. Odpowiedz, czy brak dopasowania w programie `grep` oznacza awarię programu.
Kod zakonczenia 1 w programie grep oznacza, ze nie znaleziono dopasowania. Wiec nie.

## 3. Poruszanie się po systemie plików

1. Wyświetl bieżącą ścieżkę.
pwd
/home/vboxuser/lab-linux/linux-lab/linux-lab copy
2. Wyświetl podstawową listę plików.
ls
README.txt  archive-source  config  downloads  logs  reports  users.csv
3. Wyświetl szczegółową listę plików, również ukrytych.
ls -la
4. Wyświetl szczegółową listę plików z czytelnymi rozmiarami.
ls -lh
5. Przejdź do katalogu `logs`.
cd logs
6. Wyświetl bieżącą ścieżkę i szczegółową listę plików, również ukrytych.
pwd
/home/vboxuser/lab-linux/linux-lab/linux-lab copy/logs
ls -la
total 20
drwxrwx--- 2 vboxuser vboxuser 4096 Aug 31 18:45 .
drwxrwx--- 7 vboxuser vboxuser 4096 Aug 31 18:45 ..
-rwxrwx--- 1 vboxuser vboxuser 1023 Aug 31 18:45 application.log
-rwxrwx--- 1 vboxuser vboxuser 1075 Aug 31 18:45 auth.log
-rwxrwx--- 1 vboxuser vboxuser  400 Aug 31 18:45 old-application.log
7. Wróć do katalogu nadrzędnego i wyświetl bieżącą ścieżkę.
cd ..
pwd
/home/vboxuser/lab-linux/linux-lab/linux-lab copy
8. Przejdź do katalogu `reports` i wyświetl bieżącą ścieżkę.
cd reports
pwd
/home/vboxuser/lab-linux/linux-lab/linux-lab copy/reports
9. Wróć do poprzedniego katalogu i ponownie wyświetl bieżącą ścieżkę.
cd ..
pwd
/home/vboxuser/lab-linux/linux-lab/linux-lab copy
10. Wyjaśnij różnicę między przykładową ścieżką bezwzględną `/home/student/lab`, ścieżką `home/student/lab` oraz ścieżkami względnymi `./logs` i `../reports`.
/home/student/lab to sciezka brana pod uwage od katalogu glownego systemu, poniewaz na poczatku znak "/"
home/student/lab to sciezka brana pod uwage od biezacego katalogu, poniewaz brak znaku na poczatku
./logs to katalog biezacy widoczny z obecnego miejsca, znak  "./"
../reports bedzie to katalog nadrzedny, znak "../"
11. Porównaj zwykłą listę plików ze szczegółową listą uwzględniającą pliki ukryte.
ls - to podstawowa lista plikow
ls -la - pokazuje nam ukryte pliki, uprawnienia, wlasciciela, grupe, rozimar, date modyfikacji, nazwe pliku
12. Otwórz plik `.analyst-note` w przeglądarce tekstowej.
less .analyst-note
Ukryta notatka:
Sprawdz, czy student pamieta o ls -la.

## 4. Tworzenie katalogu sprawy i praca na kopii

1. Utwórz strukturę `case-001/evidence`, `case-001/notes` i `case-001/output`.
mkdir -p case-001/evidence case-001/notes case-001/output
ls -la
drwxrwxr-x 5 vboxuser vboxuser 4096 Sep 15 21:40 case-001
2. Wyświetl rekurencyjnie strukturę katalogu `case-001`.
ls -R case-001
case-001:
evidence  notes  output

case-001/evidence:

case-001/notes:

case-001/output:
3. Skopiuj katalog `logs` do `case-001/evidence/`, zachowując atrybuty.
cp -a logs case-001/evidence
4. Skopiuj katalog `reports` do `case-001/evidence/`, zachowując atrybuty.
cp -a reports case-001/evidence
5. Skopiuj plik `users.csv` do `case-001/evidence/`, zachowując atrybuty.
cp -a users.csv case-001/evidence
6. Sprawdź typ pliku `case-001/evidence/logs/application.log`.
file case-001/evidence/logs/application.log
case-001/evidence/logs/application.log: ASCII text
7. Sprawdź typ pliku `case-001/evidence/users.csv`.
file case-001/evidence/users.csv
case-001/evidence/users.csv: CSV ASCII text
8. Sprawdź typ pliku `case-001/evidence/reports/report-2026.txt`.
file case-001/evidence/reports/report-2026.txt
case-001/evidence/reports/report-2026.txt: ASCII text
9. Utwórz pusty plik `case-001/notes/timeline.txt`.
touch case-001/notes/timeline.txt
10. Wyświetl szczegółowe informacje o utworzonym pliku.
file case-001/notes/timeline.txt
case-001/notes/timeline.txt: empty

## 5. Czytanie logów bez utraty kontroli

1. Wyświetl rozmiary `logs/application.log` i `logs/auth.log` w czytelnej postaci.
ls -lh logs/application.log logs/auth.log
-rwxrwx--- 1 vboxuser vboxuser 1023 Aug 31 18:45 logs/application.log
-rwxrwx--- 1 vboxuser vboxuser 1.1K Aug 31 18:45 logs/auth.log
2. Sprawdź typ obu plików.
file logs/application.log logs/auth.log
logs/application.log: ASCII text
logs/auth.log:        ASCII text
3. Policz wiersze w obu plikach.
wc -l logs/application.log logs/auth.log
  12 logs/application.log
  10 logs/auth.log
  22 total
4. Wyświetl pierwszych pięć wierszy `logs/application.log`.
head -n 5 logs/application.log
5. Wyświetl ostatnich pięć wierszy `logs/application.log`.
tail -n 5 logs/application.log
6. Otwórz `logs/application.log` w programie `less` bez zawijania długich wierszy.
less -S logs/application.log
7. Wyszukaj w otwartym pliku tekst `ERROR`.
/ERROR
8. Przejdź do następnego dopasowania.
n
9. Przejdź na koniec pliku.
G
10. Wróć na początek pliku.
g
11. Zamknij program `less`.
q
12. Odpowiedz, dlaczego `less` jest bezpieczniejsze niż `cat` dla dużych plików.
cat wypisuje cala zawartosc pliku od razu, less pozwala kontrolowac ilosc wyswietlanych danych
13. Odpowiedz, co może się stać po wyświetleniu pliku binarnego w terminalu.
Widzimy nieczytelny tekst, zmiane wygladu, zaburzenia wyswietlania, problemy z komendami

## 6. Wyszukiwanie informacji przez grep

1. Znajdź tekst `ERROR` w `logs/application.log`.
grep "ERROR" logs/application.log
2026-07-18T08:12:43Z ERROR app=portal component=db message="connection timeout" retry=1
2026-07-18T08:47:55Z ERROR app=portal src=198.51.100.23 action=request path=/api/debug status=404
2. Powtórz wyszukiwanie z numerami wierszy.
grep -n "ERROR" logs/application.log
4:2026-07-18T08:12:43Z ERROR app=portal component=db message="connection timeout" retry=1
8:2026-07-18T08:47:55Z ERROR app=portal src=198.51.100.23 action=request path=/api/debug status=404
3. Znajdź tekst `failed` w `logs/auth.log` bez rozróżniania wielkości liter.
grep -i "failed" logs/auth.log
Jul 18 08:05:33 lab-vm sshd[1210]: Failed password for invalid user admin from 203.0.113.44 port 49821 ssh2
Jul 18 08:05:38 lab-vm sshd[1210]: Failed password for invalid user admin from 203.0.113.44 port 49821 ssh2
Jul 18 08:21:17 lab-vm sshd[1262]: Failed password for root from 198.51.100.23 port 53310 ssh2
Jul 18 09:10:58 lab-vm sshd[1302]: Failed password for guest from 198.51.100.23 port 54001 ssh2
Jul 18 09:11:02 lab-vm sshd[1302]: Failed password for guest from 198.51.100.23 port 54001 ssh2
4. Powtórz wyszukiwanie z numerami wierszy.
grep -in "failed" logs/auth.log
5. Policz dopasowania tekstu `failed` w `logs/auth.log`, nie rozróżniając wielkości liter.
grep -ic "failed" logs/auth.log
5
6. Rekurencyjnie znajdź aktywność adresu `198.51.100.23` w bieżącym katalogu, pokazując nazwy plików i numery wierszy.
grep -rn "198.51.100.23" .
7. W ten sam sposób znajdź aktywność adresu `203.0.113.44`.
grep -rn "203.0.113.44" .
8. Wyświetl `config/service.conf` z pominięciem wierszy zaczynających się znakiem komentarza.
grep -v '^#' config/service.conf
service_name=training-portal
listen=127.0.0.1:8080
log_level=INFO
maintenance=false
owner=soc-training
9. W ten sam sposób wyświetl `config/example.sources`.
grep -v '^#' config/example.sources
Types: deb
URIs: http://deb.debian.org/debian
Suites: trixie
Components: main
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
10. W trybie cichym wyszukaj `198.51.100.23` w `logs/auth.log` i wyświetl kod z etykietą „Kod po trafieniu”.
grep -q "198.51.100.23" logs/auth.log; echo "Kod po trafieniu: $?"
Kod po trafieniu: 0
11. W trybie cichym wyszukaj `10.10.10.10` w `logs/auth.log` i wyświetl kod z etykietą „Kod po braku trafienia”.
grep -q "10.10.10.10" logs/auth.log; echo "Kod po braku trafienia: $?"
Kod po braku trafienia: 1
12. Użyj niepoprawnego wzorca `[` podczas przeszukiwania `logs/auth.log` i wyświetl kod z etykietą „Kod po blednym wzorcu”.
grep -q '[' logs/auth.log; echo "Kod po blednym wzorcu: $?"
grep: Invalid regular expression
Kod po blednym wzorcu: 2
13. Ustal, które kody oznaczają trafienie, brak trafienia i błąd.
0 - znalezione dopasowanie
1 - nie znalezione dopasowanie
2 - wystapienie bledu

## 7. Wyszukiwanie plików przez find

1. Znajdź wszystkie zwykłe pliki w bieżącym katalogu i jego podkatalogach.
find . -type f
./README.txt
./users.csv
./.analyst-note
./case-001/notes/timeline.txt
./case-001/evidence/users.csv
./case-001/evidence/logs/old-application.log
./case-001/evidence/logs/application.log
./case-001/evidence/logs/auth.log
./case-001/evidence/reports/report-2026.txt
./case-001/evidence/reports/report-2025.txt
./config/example.sources
./config/service.conf
./logs/old-application.log
./logs/application.log
./logs/auth.log
./archive-source/notes.txt
./archive-source/timeline.txt
./reports/report-2026.txt
./reports/report-2025.txt
2. Znajdź zwykłe pliki o nazwach kończących się na `.log`.
find . -type f -name '*.log'
./case-001/evidence/logs/old-application.log
./case-001/evidence/logs/application.log
./case-001/evidence/logs/auth.log
./logs/old-application.log
./logs/application.log
./logs/auth.log
3. Znajdź zwykłe pliki zawierające w nazwie słowo `report`, bez rozróżniania wielkości liter.
find . -type f -iname "*report*"
./case-001/evidence/reports/report-2026.txt
./case-001/evidence/reports/report-2025.txt
./reports/report-2026.txt
./reports/report-2025.txt
4. Znajdź zwykłe pliki zmodyfikowane w ostatniej dobie.
find . -type f -mtime -1
./case-001/notes/timeline.txt
5. Wyświetl listę wszystkich znalezionych logów.
find . -type f -name "*log"
./case-001/evidence/logs/old-application.log
./case-001/evidence/logs/application.log
./case-001/evidence/logs/auth.log
./logs/old-application.log
./logs/application.log
./logs/auth.log
6. Dla każdego znalezionego logu sprawdź typ pliku.
find . -type f -name "*log" -exec file {} +
./case-001/evidence/logs/old-application.log: ASCII text
./case-001/evidence/logs/application.log:     ASCII text
./case-001/evidence/logs/auth.log:            ASCII text
./logs/old-application.log:                   ASCII text
./logs/application.log:                       ASCII text
./logs/auth.log:                              ASCII text

## 8. Potoki i przekierowania

1. Zapisz nieudane logowania z `logs/auth.log` do `case-001/output/failed-logins.txt`, nie rozróżniając wielkości liter.
grep -i "failed" logs/auth.log > case-001/output/failed-logins.txt
2. Policz wiersze w zapisanym pliku i dopisz wynik do `case-001/output/summary.txt`.
wc -l case-001/output/failed-logins.txt >> case-001/output/summary.txt
3. Wyszukaj w `/etc` pliki o nazwach kończących się na `.conf`; zapisz wyniki do `case-001/output/etc-conf-files.txt`, a błędy do `case-001/output/etc-errors.txt`.
find /etc -type f -name "*.conf" > case-001/output/etc-conf-files.txt 2> case-001/output/etc-errors.txt
4. Powtórz wyszukiwanie, zapisując wynik i błędy razem w `case-001/output/etc-combined.txt`.
find /etc -type f -name "*.conf" > case-001/output/etc-combined.txt 2>&1
5. Wykonaj przekierowanie wyniku do `case-001/output/order-a.txt`, a następnie skieruj błędy do tego samego miejsca.
find /etc -type f -name "*.conf" > case-001/output/order-a.txt 2>&1
6. Powtórz operację w odwrotnej kolejności i zapisz wynik do `case-001/output/order-b.txt`.
find /etc -type f -name "*.conf" 2>&1 > case-001/output/order-b.txt
find: ‘/etc/polkit-1/rules.d’: Permission denied
find: ‘/etc/credstore.encrypted’: Permission denied
find: ‘/etc/credstore’: Permission denied
find: ‘/etc/ssl/private’: Permission denied
find: ‘/etc/cups/ssl’: Permission denied
7. Porównaj rezultaty obu kolejności przekierowań.
wc -l case-001/output/order-a.txt case-001/output/order-b.txt
  258 case-001/output/order-a.txt
  253 case-001/output/order-b.txt
  511 total
8. Wyszukaj nieudane logowania, zapisz wynik pośredni do `case-001/output/failed-with-tee.txt` i jednocześnie policz wiersze.
grep -i "failed" logs/auth.log | tee case-001/output/failed-with-tee.txt | wc -l
5
9. Spróbuj wyszukać nieudane logowania w nieistniejącym pliku `missing.log`, przekazując wynik do liczenia wierszy.
grep -i "failed" missing.log | wc -l
grep: missing.log: No such file or directory
0
10. W powłoce Bash wyświetl statusy wszystkich elementów ostatniego potoku.
echo "${PIPESTATUS[@]}"
2 0

## 9. Edycja notatki w Nano

1. Otwórz `case-001/notes/timeline.txt` w edytorze Nano.
nano case-001/notes/timeline.txt
2. Dodaj wpis o serii nieudanych logowań dla użytkownika `admin` z adresu `203.0.113.44` o godzinie 08:05.
OK
3. Dodaj wpis o nieudanym logowaniu użytkownika `root` z adresu `198.51.100.23` o godzinie 08:21.
OK
4. Dodaj wpis o odmowie wykonania `sudo` przez użytkownika `jan.zielinski` o godzinie 08:42.
OK
5. Zapisz plik, zatwierdź jego nazwę i zamknij edytor.
Ctrl + O potem klawisz ENTER
6. Wyświetl zawartość `case-001/notes/timeline.txt`.
cat case-001/notes/timeline.txt
08:05 - serii nieudanych logowań dla użytkownika `admin` z adresu `203.0.113.44`
08:21 - nieudanym logowaniu użytkownika `root` z adresu `198.51.100.23`
08:42 - odmowa wykonania `sudo` przez użytkownika `jan.zielinski`

## 10. Minimum Vim

1. Otwórz `case-001/notes/timeline.txt` w edytorze Vim.
vim case-001/notes/timeline.txt
2. Przejdź do trybu wstawiania.
i
3. Dopisz wniosek, że widoczne są próbne zdarzenia brute force.
OK
4. Wróć do trybu normalnego.
Esc
5. Zapisz plik i zamknij edytor.
:wq
6. Otwórz ten sam plik ponownie.
vim case-001/notes/timeline.txt
7. Przejdź do trybu wstawiania i dopisz linię testową.
i
8. Wróć do trybu normalnego.
Esc
9. Zamknij edytor bez zapisywania zmian.
:q!
10. Wyświetl plik i sprawdź, czy linia testowa nie została zapisana.
vim case-001/notes/timeline.txt - linai testowa zgodnie z instrukcjami nie zostala zapisana

## 11. Tworzenie i sprawdzanie archiwum

1. Utwórz skompresowane archiwum `case-001.tar.gz` zawierające katalog `case-001/`.
tar -czf case-001.tar.gz case-001/
2. Sprawdź typ archiwum.
file case-001.tar.gz
case-001.tar.gz: gzip compressed data, from Unix, original size modulo 2^32 61440
3. Wyświetl jego zawartość w programie `less` bez rozpakowywania.
tar -tzf case-001.tar.gz | less
4. Oblicz sumę SHA-256 archiwum i zapisz wynik w `case-001.tar.gz.sha256`.
sha256sum case-001.tar.gz > case-001.tar.gz.sha256
5. Wyświetl zapisany plik sumy kontrolnej.
cat case-001.tar.gz.sha256
f44c6d8a7094798d6fb4e45c9091edd13ddce8dca6ee2c9dbc1cff3f06a9edc9  case-001.tar.gz
6. Utwórz katalog `extracted/case-001-test`.
mkdir -p extracted/case-001-test
7. Rozpakuj archiwum do tego katalogu.
tar -xzf case-001.tar.gz -C extracted/case-001-test
8. Znajdź wszystkie zwykłe pliki w rozpakowanej strukturze.
find extracted/case-001-test -type f
extracted/case-001-test/case-001/notes/timeline.txt
extracted/case-001-test/case-001/evidence/users.csv
extracted/case-001-test/case-001/evidence/logs/old-application.log
extracted/case-001-test/case-001/evidence/logs/application.log
extracted/case-001-test/case-001/evidence/logs/auth.log
extracted/case-001-test/case-001/evidence/reports/report-2026.txt
extracted/case-001-test/case-001/evidence/reports/report-2025.txt
extracted/case-001-test/case-001/output/order-a.txt
extracted/case-001-test/case-001/output/failed-with-tee.txt
extracted/case-001-test/case-001/output/etc-errors.txt
extracted/case-001-test/case-001/output/summary.txt
extracted/case-001-test/case-001/output/failed-logins.txt
extracted/case-001-test/case-001/output/order-b.txt
extracted/case-001-test/case-001/output/etc-conf-files.txt
extracted/case-001-test/case-001/output/etc-combined.txt

## 12. Pobieranie danych przez curl i wget

1. Wyświetl nagłówki odpowiedzi adresu `https://example.com/`.
curl -I https://example.com/
HTTP/2 200 
date: Wed, 16 Sep 2026 11:59:29 GMT
content-type: text/html
server: cloudflare
last-modified: Tue, 15 Sep 2026 23:41:26 GMT
allow: GET, HEAD
accept-ranges: bytes
age: 10166
cf-cache-status: HIT
cf-ray: a3bfb4913f2c1e85-WAW
2. Pobierz ten adres przez `curl` do `downloads/example-curl.html`.
curl -o downloads/example-curl.html https://example.com/
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed
100    559   0    559   0      0   6980      0  
3. Pobierz ten sam adres przez `wget` do `downloads/example-wget.html`.
wget -O downloads/example-wget.html https://example.com/
--2026-09-16 12:01:59--  https://example.com/
Resolving example.com (example.com)... 104.20.23.154, 172.66.147.243, 2606:4700:10::6814:179a, ...
Connecting to example.com (example.com)|104.20.23.154|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
Saving to: ‘downloads/example-wget.html’

downloads/example-wget     [ <=>                         ]     559  --.-KB/s    in 0s      

2026-09-16 12:01:59 (6.44 MB/s) - ‘downloads/example-wget.html’ saved [559]
4. Sprawdź typ obu pobranych plików.
file downloads/example-curl.html downloads/example-wget.html
downloads/example-curl.html: HTML document, ASCII text, with very long lines (558)
downloads/example-wget.html: HTML document, ASCII text, with very long lines (558)
5. Wyświetl szczegółową listę katalogu `downloads/` z czytelnymi rozmiarami.
ls -lh downloads/
total 8.0K
-rw-rw-r-- 1 vboxuser vboxuser 559 Sep 16 12:00 example-curl.html
-rw-rw-r-- 1 vboxuser vboxuser 559 Sep 15 23:41 example-wget.html
6. Wyświetl pierwszych pięć wierszy `downloads/example-curl.html`.
head -n 5 downloads/example-curl.html
<!doctype html><html lang="en"><head><title>Example Domain</title><link rel="icon" href="data:,"><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{background:#eee;width:60vw;margin:15vh auto;font-family:system-ui,sans-serif}h1{font-size:1.5em}div{opacity:0.8}a:link,a:visited{color:#348}</style></head><body><div><h1>Example Domain</h1><p>This domain is for use in documentation examples without needing permission. Avoid use in operations.</p><p><a href="https://iana.org/domains/example">Learn more</a></p></div></body></html>
7. Oblicz sumy SHA-256 obu pobranych plików.
sha256sum downloads/example-curl.html downloads/example-wget.html
ff67a9d764d6a2367a187734e697f6a53217db9a21c101d410a113ca871a299d  downloads/example-curl.html
ff67a9d764d6a2367a187734e697f6a53217db9a21c101d410a113ca871a299d  downloads/example-wget.html
8. Nie uruchamiaj pobranych plików.
To przezorne rozwiazanie, najpierw trzeba sprawdzic ich typ i zawartosc
9. Wyjaśnij kolejność działań: pobranie, sprawdzenie, przeczytanie, zweryfikowanie i dopiero potem rozważenie uruchomienia.
a) pobranie pliku
b) sprawdzenie typu pliku
c) przejrzenie zawartosci pliku
d) sprawdzenie pochodzenia pliku
e) jak jest w porzadku przy wczesniejszych krokach, to dopiero uruchomienie
10. Nie pobieraj skryptu instalacyjnego bezpośrednio do powłoki.
Czyli dla przykladu najpierw curl -o 'nazwa skryptu' 'adres'
file 'nazwa skryptu'
less 'nazwa skryptu'
sha256sum 'nazwa skryptu'

## 13. Pakiety i repozytoria bez instalowania

1. Sprawdź, czy program `apt` jest dostępny.
apt --version
apt 3.2.0 (amd64)
2. Wyszukaj pakiet `jq`.
apt search jq
3. Wyświetl informacje o pakiecie `jq`.
apt show jq
4. Sprawdź politykę i źródła wersji pakietu `jq`.
apt-cache policy jq
jq:
  Installed: 1.8.1-4ubuntu2
  Candidate: 1.8.1-4ubuntu2
  Version table:
 *** 1.8.1-4ubuntu2 500
        500 http://pl.archive.ubuntu.com/ubuntu resolute-updates/main amd64 Packages
        500 http://security.ubuntu.com/ubuntu resolute-security/main amd64 Packages
        100 /var/lib/dpkg/status
     1.8.1-4ubuntu1 500
        500 http://pl.archive.ubuntu.com/ubuntu resolute/main amd64 Packages
5. Wyświetl listę zainstalowanych pakietów w programie `less`.
apt list --installed | less
6. Wyświetl w programie `less` pakiety oznaczone jako zainstalowane ręcznie.
apt-mark showmanual | less
7. Wyświetl pakiety wstrzymane.
apt-mark showhold
8. Rekurencyjnie wyświetl niezakomentowane wpisy z `/etc/apt/sources.list` i `/etc/apt/sources.list.d/`, pokazując numery wierszy i ukrywając komunikaty o błędach.
rep -Rnhv '^[[:space:]]*#' /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null
3:
32:Types: deb
33:URIs: http://archive.ubuntu.com/ubuntu/
34:Suites: resolute resolute-updates resolute-backports
35:Components: main universe restricted multiverse
36:Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
37:
40:Types: deb
41:URIs: http://security.ubuntu.com/ubuntu/
42:Suites: resolute-security
43:Components: main universe restricted multiverse
44:Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
3:Types: deb
4:URIs: https://packages.microsoft.com/repos/code
5:Suites: stable
6:Components: main
7:Architectures: amd64
8:Signed-By: /usr/share/keyrings/microsoft.gpg
1:deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu   resolute stable
1:Types: deb
2:URIs: http://pl.archive.ubuntu.com/ubuntu/
3:Suites: resolute resolute-updates resolute-backports
4:Components: main restricted universe multiverse
5:Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
6:
7:Types: deb
8:URIs: http://security.ubuntu.com/ubuntu/
9:Suites: resolute-security
10:Components: main restricted universe multiverse
11:Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
9. Wyświetl ogólną politykę źródeł pakietów.
apt policy
10. Odpowiedz, co robi `apt update`, a czego nie robi.
Pobiera informacje o dostepnych pakietach i ich wersjach
Nie instaluje ani nie aktualizuje tych pakietow
11. Wyjaśnij, dlaczego `apt upgrade` zmienia system.
Instaluje nowsze wersje juz zainstalowanych w systemie pakietow
Zmienia tym samym pliki programow, bibliotek
12. Wyjaśnij, dlaczego zewnętrzne repozytorium rozszerza granicę zaufania.
Dodajac cos z zewnatrz, system pobiera i instaluje pakiety od dostawcy, wiec od teraz system
moze byc narazony przez to dodatkowe repozytorium
13. Wyjaśnij, dlaczego sam numer wersji programu nie zawsze wystarcza do potwierdzenia podatności.
Dystrybucje moga stosowac poprawki bezpieczenstwa do starszych wersjii bez zmiany glownej wersji programu

## 14. Zadanie końcowe

1. Umieść kopie logów, raportów i `users.csv` w `case-001/evidence/`.
cp -a logs case-001/evidence/
cp -a reports case-001/evidence/
cp -a users.csv case-001/evidence/
2. Umieść linie nieudanych logowań w `case-001/output/failed-logins.txt`.
grep -i "failed" logs/auth.log > case-001/output/failed-logins.txt
3. Umieść liczbę nieudanych logowań w `case-001/output/summary.txt`.
grep -ic "failed" logs/auth.log > case-001/output/summary.txt
4. Umieść trzy najważniejsze obserwacje w `case-001/notes/timeline.txt`.
Wpisane juz wczesniej za pomoca edytora, sprawdzenie:
cat case-001/notes/timeline.txt 
08:05 - serii nieudanych logowań dla użytkownika `admin` z adresu `203.0.113.44`
08:21 - nieudanym logowaniu użytkownika `root` z adresu `198.51.100.23`
08:42 - odmowa wykonania `sudo` przez użytkownika `jan.zielinski`
Wniosek: widoczne sa probne zdarzenia brute force
5. Utwórz `case-001.tar.gz` zawierające katalog `case-001/`.
tar -czf case-001.tar.gz case-001/
6. Zapisz hash archiwum w `case-001.tar.gz.sha256`.
sha256sum case-001.tar.gz > case-001.tar.gz.sha256
7. Wyświetl wszystkie zwykłe pliki w `case-001`.
find case-001 -type f
case-001/notes/timeline.txt
case-001/evidence/users.csv
case-001/evidence/logs/old-application.log
case-001/evidence/logs/application.log
case-001/evidence/logs/auth.log
case-001/evidence/reports/report-2026.txt
case-001/evidence/reports/report-2025.txt
case-001/output/order-a.txt
case-001/output/failed-with-tee.txt
case-001/output/etc-errors.txt
case-001/output/summary.txt
case-001/output/failed-logins.txt
case-001/output/order-b.txt
case-001/output/etc-conf-files.txt
case-001/output/etc-combined.txt
8. Wyświetl zawartość `case-001.tar.gz` bez rozpakowywania.
tar -tzf case-001.tar.gz | less
9. Zweryfikuj sumę kontrolną zapisaną w `case-001.tar.gz.sha256`.
sha256sum -c case-001.tar.gz.sha256
case-001.tar.gz: OK

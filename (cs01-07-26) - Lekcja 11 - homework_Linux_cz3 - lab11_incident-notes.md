# Notatka analityczna - laboratorium 11

## Kontekst

```text
Data i czas: Sun Sep 27 04:50:46 PM UTC 2026
Host: Ubuntu
Użytkownik: vboxuser
Dystrybucja: Ubuntu 26.04.1 LTS (Resolute Raccoon)
```

## Fakty o systemie

1. Nazwa hosta to Ubuntu. Biezacy uzytkownik to vboxuser (UID 1000)
nalezy do grup sudo, docker i vboxsf
2. W systemie aktywne sa uslugi cron, docker, systemd-journald
3. System dziala jako maszyna wirtualana VirtualBoX. Logi to potwierdzaja

## Proces wymagający uwagi

```text
PID: 4925
PPID: 4912
USER: vboxuser
CMD: [xdg-terminal-ex] <defunct>
Powód zainteresowania: Proces ma stan Z (zombie / defunct). Wymaga analizy, nie oznacza jednak zlosliwego procesu.
```

## Usługa

```text
Nazwa usługi: cron.service
Stan aktywny: active (running)
Autostart: nie sprawdzono
Ostatnie logi: 27.09.2026 16:05:01 - cron uruchomil u uzytkownika vboxuser polecenie /usr/bin/uptime i zakonczyl.
```

## Logi

```text
Źródło logów: journalctl/systemd
Zakres czasu: ostatnia godzina
Najważniejsze wpisy:
- CRON usuchomil /usr/bin/uptime dla vboxuser
- watchdog: BUG: soft lockup - CPU#0 stuck for 21s!
- rtkit-daemon zaraportowal problemy z canary
```

## Zadania zaplanowane

```text
Crontab użytkownika: brak aktywnych zadan, tylko same komentarze
Crontab root: brak danych
/etc/cron.d: .placeholder, anacron, e2scrub_all
atq: brak zadan
```

## Hipotezy

1.Wpis z logow:
watchdog: BUG: soft lockup - CPU#0 stuck for 21s!
a nastepnie komunikaty rtkit-daemon o watku canary
Hipoteza:
Dochodzi do chwilowego problemu z dostepem do czasu procesora. Nie moge odnalezc pewnej przyczyny. Nie uznaje tego za incydent bezpieczenstwa.
2. Kolejne zdarzenie z logow:
Sep 27 16:05:01 Ubunru CRON[42020]:
(vboxuser) CMD (/usr/bin/uptime >> /tmp/uptime.log 2>&1)
Hipoteza:
Jest to oznaka prawidlowo wykonanego wczesniej zadania z lab11 cron uruchamiajacego uptime co 5 minut.


## Co wymaga dalszej analizy

1. Wykryto:
watchdog: BUG: soft lockup - CPU#0 stuck for 21s!
- zdarzenie wystapilo 27.09.2026 o 16:06:19 i bylo powiazane z komunikatami rtkit-daemon o problemach z dostepem do przydzielonych watkow CPU.
Nalezy sprawdzic obciazenie maszyny wirtualnej w tym czasie i ustalic, czy to bylo jednorazowe obciazenie maszyny wirtualnej, czy wystepuje =cyklicznie.

## Decyzja / następny krok

```text
Czy potrzebna izolacja hosta: NIE
Czy potrzebna eskalacja: NIE
Czy potrzebne zabezpieczenie plików: TAK
```


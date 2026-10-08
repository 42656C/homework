# Laboratorium 15 — zadania do wykonania

## Cel laboratorium

W tym laboratorium wykonasz podstawowe operacje związane z kodowaniem, funkcjami skrótu, szyfrowaniem symetrycznym, kryptografią asymetryczną i HTTPS. Następnie połączysz szyfrowanie symetryczne i asymetryczne w uproszczony model szyfrowania hybrydowego.

Ten wariant instrukcji celowo nie zawiera gotowych komend terminalowych. Twoim zadaniem jest samodzielne dobranie narzędzi, składni i parametrów potrzebnych do osiągnięcia opisanego rezultatu.

Po zakończeniu laboratorium powinieneś umieć:

- odróżnić kodowanie od szyfrowania,
- wyjaśnić rolę funkcji skrótu,
- zaszyfrować i odszyfrować plik metodą symetryczną,
- rozpoznać różnicę między hasłem a losowym kluczem,
- utworzyć parę kluczy RSA,
- użyć właściwego klucza do szyfrowania i deszyfrowania,
- wyjaśnić zasadę działania szyfrowania hybrydowego,
- wskazać podstawowe informacje dostępne podczas diagnostyki HTTPS.

## Sposób pracy

1. Przed każdym etapem zapisz, jaki rezultat chcesz uzyskać.
2. Samodzielnie ustal właściwe polecenie i wymagane parametry.
3. Przed uruchomieniem wyjaśnij znaczenie każdego elementu przygotowanej składni.
4. Wykonaj operację na plikach testowych.
5. Sprawdź rezultat inną metodą niż samo istnienie pliku.
6. Zapisz obserwacje i wnioski.

## Przygotowanie środowiska

1. Przejdź do katalogu **content/15/lab**.
cd /home/vboxuser/lab15
mkdir -p content/15/lab
cd content/15/lab/

2. Potwierdź, że pracujesz we właściwej lokalizacji.
pwd
/home/vboxuser/lab15/content/15/lab
3. Wyświetl pliki i katalogi dostępne w laboratorium.
ls -la
4. Sprawdź, czy OpenSSL jest dostępny.
openssl -v command
OpenSSL 3.5.5 27 Jan 2026 (Library: OpenSSL 3.5.5 27 Jan 2026)
openssl version

5. Zanotuj wersję OpenSSL w szablonie notatek.
nano materials/lab-notes-template.md
OpenSSL 3.5.5 27 Jan 2026 (Library: OpenSSL 3.5.5 27 Jan 2026)
Ctrl+O
Enter
Ctrl+X

6. Utwórz katalog **work**, jeżeli jeszcze nie istnieje.
mkdir work

7. Skopiuj **materials/sample-secret.txt** do katalogu roboczego jako **secret.txt**.
cp materials/sample-secret.txt work/secret.txt

8. Skopiuj **materials/lab-notes-template.md** do katalogu roboczego jako **lab-notes.md**.
cp materials/lab-notes-template.md work/lab-notes.md

9. Przejdź do katalogu **work**.
cd work

10. Potwierdź, że oba pliki istnieją i są czytelne.
ls -l
total 8
-rwxrwx--- 1 vboxuser vboxuser 1628 Oct  5 13:35 lab-notes.md
-rw-r--r-- 1 vboxuser vboxuser  219 Oct  5 13:34 secret.txt

11. Otwórz **secret.txt** i upewnij się, że zawiera wyłącznie testową wiadomość.
cat secret.txt
To jest testowa poufna wiadomość do laboratorium z kryptografii.
Nie zawiera prawdziwych sekretów, haseł ani danych osobowych.
Cel: sprawdzić kodowanie, hashowanie, szyfrowanie symetryczne, RSA i model hybrydowy.

Kryterium ukończenia:

- pracujesz w katalogu **work**,
- znajdują się w nim pliki **secret.txt** i **lab-notes.md**,
- znasz wersję używanego OpenSSL,
- żaden prawdziwy sekret nie został użyty.

## 1. Kodowanie to nie szyfrowanie

### Zadania

1. Odczytaj zawartość **secret.txt**.
cat secret.txt
To jest testowa poufna wiadomość do laboratorium z kryptografii.
Nie zawiera prawdziwych sekretów, haseł ani danych osobowych.
Cel: sprawdzić kodowanie, hashowanie, szyfrowanie symetryczne, RSA i model hybrydowy.

2. Zakoduj zawartość pliku przy użyciu Base64.
base64 secret.txt
VG8gamVzdCB0ZXN0b3dhIHBvdWZuYSB3aWFkb21vxZvEhyBkbyBsYWJvcmF0b3JpdW0geiBrcnlw
dG9ncmFmaWkuCk5pZSB6YXdpZXJhIHByYXdkeml3eWNoIHNla3JldMOzdywgaGFzZcWCIGFuaSBk
YW55Y2ggb3NvYm93eWNoLgpDZWw6IHNwcmF3ZHppxIcga29kb3dhbmllLCBoYXNob3dhbmllLCBz
enlmcm93YW5pZSBzeW1ldHJ5Y3puZSwgUlNBIGkgbW9kZWwgaHlicnlkb3d5LgoK

3. Najpierw obejrzyj wynik bez zapisywania go do pliku.
Wynik stout zobaczylismy na ekranie, nie zostal zapisany do zadnego pliku

4. Następnie zapisz zakodowaną reprezentację jako **secret.base64.txt**.
base64 secret.txt > secret.base64.txt

5. Otwórz zapisany plik i oceń, czy oryginalny tekst jest bezpośrednio czytelny.
cat secret.base64.txt 
VG8gamVzdCB0ZXN0b3dhIHBvdWZuYSB3aWFkb21vxZvEhyBkbyBsYWJvcmF0b3JpdW0geiBrcnlw
dG9ncmFmaWkuCk5pZSB6YXdpZXJhIHByYXdkeml3eWNoIHNla3JldMOzdywgaGFzZcWCIGFuaSBk
YW55Y2ggb3NvYm93eWNoLgpDZWw6IHNwcmF3ZHppxIcga29kb3dhbmllLCBoYXNob3dhbmllLCBz
enlmcm93YW5pZSBzeW1ldHJ5Y3puZSwgUlNBIGkgbW9kZWwgaHlicnlkb3d5LgoK

6. Odkoduj **secret.base64.txt**.
base64 -d secret.base64.txt
To jest testowa poufna wiadomość do laboratorium z kryptografii.
Nie zawiera prawdziwych sekretów, haseł ani danych osobowych.
Cel: sprawdzić kodowanie, hashowanie, szyfrowanie symetryczne, RSA i model hybrydowy.

7. Porównaj odkodowaną treść z pierwotnym **secret.txt**.
base64 -d secret.base64.txt > decoded-base64.txt
cmp secret.txt decoded-base64.txt
cmp secret.txt decoded-base64.txt && echo $?
0
(0 - identyczne, 1 - pliki roznia sie, 2 - blad)

8. Sprawdź, czy odkodowanie wymagało hasła, klucza albo innego sekretu.
Nie wymagalo

### Do zapisania w notatkach

- wynik kodowania Base64,
- informacja, czy Base64 wymaga sekretu,
- informacja, czy Base64 zapewnia poufność,
- własne wyjaśnienie różnicy między kodowaniem a szyfrowaniem.

### Kryterium ukończenia

- plik **secret.base64.txt** istnieje,
- zakodowane dane można odwrócić bez sekretu,
- po odkodowaniu otrzymujesz pierwotną wiadomość.

### Pytania kontrolne

1. Jaki problem rozwiązuje kodowanie Base64?
Przedstawia dane binarne przy uzyciu drukowalnych znakow tekstowych (znakow ASCII).
Przydaje sie tam, gdzie dane musza byc przeslane lub przechowane w formie tekstowej.
2. Dlaczego zmiana wyglądu danych nie oznacza ich ochrony?
Sposob ich przeszkatlcenia jest publicznie znany. Kazdy bez trudu moglby odkodowac tresc.
3. Czy osoba posiadająca wyłącznie **secret.base64.txt** może odzyskać treść?
Tak, do tegu celu uzylem base64 -d nazwa_pliku
4. W jakich sytuacjach Base64 jest użyteczne mimo braku poufności?
Tam gdzie trzeba przedstawic dane binarne jako tekst.

## 2. Hash pliku i integralność

### Zadania

1. Oblicz skrót SHA-256 pliku **secret.txt**.
sha256sum secret.txt
18a64d61a7b3f1735b4e0d148cb85a4d5e8e5b7a23acc1f9a896555450e5101a  secret.txt

2. Zapisz pierwszy wynik w pliku **secret.sha256**.
sha256sum secret.txt > secret.sha256

3. Zanotuj wartość skrótu również w **lab-notes.md**.
cat secret.sha256
18a64d61a7b3f1735b4e0d148cb85a4d5e8e5b7a23acc1f9a896555450e5101a  secret.txt
nano lab-notes.md
4. Dodaj do **secret.txt** krótką linię testową.
echo "test" >> secret.txt
To jest testowa poufna wiadomość do laboratorium z kryptografii.
Nie zawiera prawdziwych sekretów, haseł ani danych osobowych.
Cel: sprawdzić kodowanie, hashowanie, szyfrowanie symetryczne, RSA i model hybrydowy.

test

5. Ponownie oblicz skrót SHA-256 zmodyfikowanego pliku.
sha256sum secret.txt
0bde33dd38dfc0790b4b75dfdc116f4892df34d1a12aabc5af6b9d60027bb8f3  secret.txt

6. Porównaj nową wartość z wartością zapisaną wcześniej. "test" 
cat secret.sha256
18a64d61a7b3f1735b4e0d148cb85a4d5e8e5b7a23acc1f9a896555450e5101a  secret.txt
sha256sum secret.txt
0bde33dd38dfc0790b4b75dfdc116f4892df34d1a12aabc5af6b9d60027bb8f3  secret.txt

7. Ustal, czy na podstawie samego skrótu można odtworzyć treść pliku.
Nie

8. Przywróć **secret.txt** z pliku startowego znajdującego się w **materials**.
cp ../materials/sample-secret.txt secret.txt

9. Ponownie oblicz skrót i sprawdź, czy odpowiada wynikowi sprzed modyfikacji.
sha256sum secret.txt
18a64d61a7b3f1735b4e0d148cb85a4d5e8e5b7a23acc1f9a896555450e5101a  secret.txt
sha256sum -c secret.sha256
secret.txt: OK

### Do zapisania w notatkach

- pierwszy skrót SHA-256,
- skrót po zmianie danych,
- obserwacja dotycząca wpływu małej zmiany na wynik,
- wyjaśnienie, dlaczego hash nie zapewnia poufności,
- informacja, czy funkcja skrótu jest odwracalna.

### Kryterium ukończenia

- plik **secret.sha256** zawiera pierwszy wynik,
- zmiana danych powoduje zmianę skrótu,
- po przywróceniu identycznej treści otrzymujesz pierwotny skrót,
- **secret.txt** ponownie zawiera wyłącznie wiadomość startową.

### Pytania kontrolne

1. Co oznacza zgodność dwóch skrótów?
Oznacza, ze porownywane dane sa zgodne z tymi, dla ktorych obliczono pierwotny hash.
2. Czy różne skróty dowodzą, że pliki mają inną zawartość?
Tak. Jezeli dwa porownane ze soba pliki maja rozny skrot SHA-256, to ich zawartosc jest rozna od siebie.
3. Dlaczego hash nie jest szyfrowaniem?
Nie uzywamy klucza ani sekretu, nie sluzy do przywrocenia danych. Hash sluzy do sprawdzenia integralnosci danych.

## 3. Szyfrowanie symetryczne AES

### Zadania

1. Zaszyfruj **secret.txt** algorytmem AES-256 w trybie CBC.
openssl enc -aes-256-cbc -salt -pbkdf2 -in secret.txt -out secret.enc

2. Włącz użycie losowej soli.
-salt
3. Użyj mechanizmu PBKDF2 do wyprowadzenia klucza z hasła.
-pbkdf2
4. Zapisz szyfrogram jako **secret.enc**.
-out secret.enc
5. Użyj wyłącznie hasła testowego, którego nie stosujesz w żadnym innym miejscu.
Y
6. Porównaj typ, rozmiar i wygląd **secret.txt** oraz **secret.enc**.
ls -l secret.txt secret.enc 
-rw-rw-r-- 1 vboxuser vboxuser 240 Oct  5 14:27 secret.enc
-rw-r--r-- 1 vboxuser vboxuser 219 Oct  5 14:14 secret.txt
file  secret.txt secret.enc 
secret.txt: Unicode text, UTF-8 text
secret.enc: openssl enc'd data with salted password

7. Spróbuj wyświetlić zawartość szyfrogramu i zapisz obserwację.
cat secret.enc 
Salted__�@Y)C
             :�
\4��U�I�Ǟ�6!�J&*8e,���j¸޸�sТ8���ƭ��;@������08�G O�y����`@���<:�q
2H��%.������ˣ�':�Q}G��g�_��j����$V��1wgڳqe�a�P���dh�/� ���`�%$�����J5�����C��l0l�s�^�U�f����8}p��j=?�

8. Odszyfruj **secret.enc** poprawnym hasłem do pliku **decoded.txt**.
openssl enc -aes-256-cbc -d -salt -pbkdf2 -in secret.enc -out decoded.txt
enter AES-256-CBC decryption password:

9. Porównaj **decoded.txt** z **secret.txt** w sposób pozwalający wykryć każdą różnicę.
cmp secret.txt decoded.txt && echo $?
0

10. Powtórz próbę deszyfrowania z błędnym hasłem, zapisując wynik do osobnego pliku.
openssl enc -aes-256-cbc -d -salt -pbkdf2 -in secret.enc -out decoded-wrong.txt

11. Zachowaj komunikat błędu albo opisz, dlaczego otrzymany wynik jest niepoprawny.
enter AES-256-CBC decryption password:
bad decrypt
40B7E437E3770000:error:1C800064:Provider routines:ossl_cipher_unpadblock:bad decrypt:../providers/implementations/ciphers/ciphercommon_block.c:107:

cmp secret.txt decoded-wrong.txt 
secret.txt decoded-wrong.txt differ: byte 1, line 1

Bledne haslo nie odtworzylo po deszyfracji poprawnej wiadomosci.

12. Nie nadpisuj poprawnie odszyfrowanego pliku wynikiem nieudanej próby.
Y

### Do zapisania w notatkach

- użyty algorytm i tryb,
- rola soli,
- rola PBKDF2,
- rezultat porównania pliku jawnego i poprawnie odszyfrowanego,
- zachowanie narzędzia po podaniu błędnego hasła,
- wyjaśnienie, dlaczego nieczytelny wygląd danych nie jest sam w sobie dowodem poprawnego szyfrowania.

### Kryterium ukończenia

- istnieją **secret.enc** i **decoded.txt**,
- **decoded.txt** jest identyczny z **secret.txt**,
- błędne hasło nie odtwarza poprawnej wiadomości,
- potrafisz wyjaśnić znaczenie użytych parametrów.

### Pytania kontrolne

1. Dlaczego szyfrowanie i deszyfrowanie wymagają tego samego sekretu?
Poniewaz zastosowany AES jest szyfrem symetrycznym.
Uzywamy tego samego hasla do zaszyfrowania i odszyfrowania danych.
2. Jaką rolę pełni sól?
Jest dodatkowa losowa wartoscia. Utrudnia ataki brute force.
3. Dlaczego hasło człowieka nie powinno być bezpośrednio traktowane jak wysokiej jakości klucz?
Hasla tworzone przez ludzi maja niska entropie, wiec sa przewidywalne.
4. Co może się wydarzyć po próbie deszyfrowania błędnym hasłem?
OpenSSL moze zglosic blad, z uzyskany wynik nie bedzie taki jak oryginalna wiadomosc.

## 4. Hasło, klucz i losowość

### Zadania

1. Wygeneruj kryptograficznie losowy sekret o długości 32 bajtów.
openssl rand -hex 32 > aes.key

2. Zapisz go w reprezentacji heksadecymalnej jako **aes.key**.
-hex 32 > aes.key
cat aes.key
60c5c3bb4f50a51ae7f48f75ff1f57f6cd33847e7413f422e0cf1c6837182e37

3. Sprawdź liczbę znaków w pliku.
cat aes.key
60c5c3bb4f50a51ae7f48f75ff1f57f6cd33847e7413f422e0cf1c6837182e37
wc -c aes.key
65 aes.key

4. Wyjaśnij zależność między 32 bajtami, 256 bitami i 64 znakami heksadecymalnymi.
1 bajt = 8 bitow
32 bajty = 32 x 8 = 256 bitow
1 znak heksadecymalny = 4 bity
256 bitow / 4 bity = 64 znaki heksadecymalne

5. Ustal, czy narzędzie dodało znak końca linii.
cat -A aes.key 
60c5c3bb4f50a51ae7f48f75ff1f57f6cd33847e7413f422e0cf1c6837182e37$
$ - znak konca linii.

6. Zaszyfruj **secret.txt**, pobierając sekret z **aes.key**.
openssl enc -aes-256-cbc -salt -pbkdf2 -pass file:aes.key -in secret.txt -out secret-with-keyfile.enc

7. Zapisz szyfrogram jako **secret-with-keyfile.enc**.
-out secret-with-keyfile.enc
Sprawdzenie:
ls -l secret-with-keyfile.enc
8. Odszyfruj go do **decoded-with-keyfile.txt**, używając tego samego pliku z sekretem.
openssl enc -aes-256-cbc -d -salt -pbkdf2 -pass file:aes.key -in secret-with-keyfile.enc -out decoded-with-keyfile.txt

9. Porównaj wynik z pierwotnym plikiem.
cmp secret.txt decoded-with-keyfile.txt && echo "DOBRZE - pliki sa identyczne"
DOBRZE - pliki sa identyczne

10. Ogranicz uprawnienia **aes.key** tak, aby dostęp miał wyłącznie właściciel.
chmod 600 aes.key

11. Sprawdź i zanotuj końcowe uprawnienia.
ls -l aes.key 
-rw------- 1 vboxuser vboxuser 65 Oct  8 12:19 aes.key
Odczyt i zapis posiada tylko wlasciciel pliku.
Grupa i pozostali uzytkownicy nie maja dostepu.

12. Rozważ, co stanie się z poufnością danych, jeśli napastnik zdobędzie jednocześnie szyfrogram i **aes.key**.
Jezeli napastnik jednoczesnie posiada secret-with-keyfile.enc i aes.key
to ma jednoczesnie zaszyfrowane dane i sekret potrzebny do ich odszyfrowania.

### Do zapisania w notatkach

- sposób uzyskania losowości,
- długość wygenerowanego materiału,
- różnica między hasłem zapamiętywanym przez człowieka a losowym sekretem,
- końcowe uprawnienia pliku **aes.key**,
- ograniczenia ochrony zapewnianej wyłącznie przez uprawnienia systemu plików.

### Kryterium ukończenia

- istnieją **aes.key**, **secret-with-keyfile.enc** i **decoded-with-keyfile.txt**,
- odszyfrowany plik jest identyczny z **secret.txt**,
- **aes.key** nie jest dostępny dla innych użytkowników systemu,
- rozumiesz, że plik z kluczem musi być przechowywany oddzielnie od chronionych danych.

### Pytania kontrolne

1. Dlaczego losowy sekret jest trudniejszy do odgadnięcia niż typowe hasło?
Poniewaz jest generowany losowo, w wyborach czlowieka najczesciej sa schematy, slowa. Losowy sekret ma wieksza nieprzewidywalnosc - wyzsza entropie.
2. Czy ograniczenie uprawnień szyfruje plik z kluczem?
Nie. chmod 600 tylko ogranicza dostep do innych uzytkownikow poza wlascicielem. Zawartosc pliku z kluczem "aes.key" nadal nie jest zaszyfrowana.
3. Gdzie należałoby przechowywać klucz w systemie produkcyjnym?
W oddzielnym miejscu od zaszyfrowanych danych. Dostep tylko dla uprawnionych uzytkownikow.
4. Jak utrata klucza wpływa na możliwość odzyskania danych?
Brak klucza lub jego kopii moze uniemozliwic odszyfrowanie danych.
5. Dlaczego kopia klucza przechowywana obok szyfrogramu osłabia ochronę?
Gdy napastnik uzyska dostep do jednego miejsca, tego w ktorym sa pliki zaszyfrowane i klucz jednoczesnie. Moze zdobyc obydwie rzeczy i odszyfrowywac zaszyfrowane pliki
za pomoca tego klucza.

## 5. Generowanie pary kluczy RSA

### Zadania

1. Wygeneruj prywatny klucz RSA o długości 3072 bitów.
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out private-rsa.pem

2. Zapisz go jako **private-rsa.pem**.
Y
3. Natychmiast ogranicz dostęp do klucza prywatnego wyłącznie do właściciela.
chmod 600 private-rsa.pem
4. Na podstawie klucza prywatnego wyprowadź odpowiadający mu klucz publiczny.
openssl pkey -in private-rsa.pem -pubout -out public-rsa.pem

5. Zapisz klucz publiczny jako **public-rsa.pem**.
Y - openssl pkey -in private-rsa.pem -pubout -out public-rsa.pem

6. Porównaj nagłówki, rozmiary i uprawnienia obu plików.
head -n 5 private-rsa.pem
-----BEGIN PRIVATE KEY-----
MIIG/QIBADANBgkqhkiG9w0BAQEFAASCBucwggbjAgEAAoIBgQC9yRBIQeQ3MQdQ
7sFR9AaexP3PryoNZwGUo7QCjCv5Oe/xHenOBuWdo/yE7JpPIHQXQ5cF8tl5WL9q
DSapUjBwn8imgOaoBUciY694BveG/Z4pAI5UpI7UrL7MYQUrrh4fsxK6G/IbS4o+
BPnlB1eQm6knRZeefz6lzmVudhTsQTtiS1aZwYeh1168nrKZ+JZgNfgx5+BhqIS8
head -n 5 public-rsa.pem 
-----BEGIN PUBLIC KEY-----
MIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEAvckQSEHkNzEHUO7BUfQG
nsT9z68qDWcBlKO0Aowr+Tnv8R3pzgblnaP8hOyaTyB0F0OXBfLZeVi/ag0mqVIw
cJ/IpoDmqAVHImOveAb3hv2eKQCOVKSO1Ky+zGEFK64eH7MSuhvyG0uKPgT55QdX
kJupJ0WXnn8+pc5lbnYU7EE7YktWmcGHoddevJ6ymfiWYDX4MefgYaiEvEN2qm4s
la -la public-rsa.pem private-rsa.pem
-rw------- 1 vboxuser vboxuser 2484 Oct  5 16:24 private-rsa.pem
-rw-rw-r-- 1 vboxuser vboxuser  625 Oct  5 16:32 public-rsa.pem

7. Ustal, który plik może zostać udostępniony odbiorcy.
Udostepniamy public-rsa.pem
Czyli publiczny

8. Wyjaśnij, dlaczego klucz publiczny nadal powinien być przekazany w sposób pozwalający potwierdzić jego autentyczność.
Musimy potwierdzic, ze nalezy do osoby, ktorej chcemy wyslac poufne dane.

9. Nie kopiuj klucza prywatnego poza katalog roboczy.
Y

### Do zapisania w notatkach

- nazwy plików obu kluczy,
- rozmiar zastosowanego klucza RSA,
- końcowe uprawnienia klucza prywatnego,
- informacja, który klucz można udostępnić,
- wyjaśnienie, dlaczego autentyczność klucza publicznego ma znaczenie.

### Kryterium ukończenia

- istnieją **private-rsa.pem** i **public-rsa.pem**,
- klucz publiczny pochodzi z przygotowanego klucza prywatnego,
- prywatny klucz ma ograniczone uprawnienia,
- potrafisz wskazać konsekwencje ujawnienia każdego z plików.

### Pytania kontrolne

1. Dlaczego klucz publiczny można udostępnić?
Zostal zaprojektowany do publicznego uzycia.
2. Dlaczego klucz prywatny musi pozostać tajny?
Umozliwia operacje tylko wlascicielowy pary klucy. Odszyfrowanie danych zaszyfrowanych odpowiednim kluczem prywatnym.
3. Czy znajomość klucza publicznego pozwala wyprowadzić odpowiadzający mu klucz prywatny?
Przy odpowiedniej dlugosci klucza nie jest to wykonalne.
4. Co może się wydarzyć, jeśli odbiorca zaakceptuje podmieniony klucz publiczny?
Moze zaszyfrowac dane, ktore odszyfruje napastnik (wlasciciel podmienionego klucza publicznego), a nie wlasciwy odbiorca, do ktorego nadawca chcial wyslac zaszyfrowana wiadomosc.
5. Czym różni się poufność klucza od potwierdzenia jego autentyczności?
Poufnosc oznacza, ze klucz jest ukryty przed nieuprawionymi osobami. Natomiast autentycznosc oznacza,
ze klucz nalezy do osoby, do ktorej go przypisujemy.

## 6. Szyfrowanie i deszyfrowanie małego pliku RSA

### Zadania

1. Utwórz krótki plik **short-message.txt** zawierający testową wiadomość dla odbiorcy.
echo "Testowa wiadomosc dla docelowego odbiorcy." > short-message.txt

2. Zaszyfruj wiadomość za pomocą **public-rsa.pem**.
openssl pkeyutl -encrypt -pubin -inkey public-rsa.pem -in short-message.txt -out short-message.rsa.enc

3. Zapisz szyfrogram jako **short-message.rsa.enc**.
-out short-message.rsa.enc

4. Odszyfruj szyfrogram za pomocą **private-rsa.pem**.
openssl pkeyutl -decrypt -inkey private-rsa.pem -in shorter-message.rsa.enc -out short-message.decoded.txt

5. Zapisz wynik jako **short-message.decoded.txt**.
-out short-message.decoded.txt

6. Porównaj wynik z oryginalną wiadomością.
cmp short-message.txt short-message.decoded.txt && echo "DOBRZE - pliki sa identyczne"
DOBRZE - pliki sa identyczne

7. Spróbuj wyjaśnić, dlaczego szyfrowanie wymaga klucza publicznego, a odtworzenie danych — odpowiadającego klucza prywatnego.
Klucz publiczny sluzy do zaszyfrowania wiadomosci i moze byc udostepniony nadawcy.
Odszyfrowanie wymaga odpowiadajacego mu klucza prywatnego, ktory to musi pozostac tajny.
Dzieki temu nadawca nie musi znac klucza prywatnego odbiorcy zaszyfrowanej wiadomosci.

8. Sprawdź, co stanie się po próbie zaszyfrowania pliku znacznie większego od krótkiej wiadomości.
Napierw tworze plik o rozmiarze 1024 bajty:
head -c 1024 /dev/zero > large-message.bin
Sprawdzam rozmiar:
wc -c large-message.bin
1024 large-message.bin
Szyfrowanie:
openssl pkeyutl -encrypt -pubin -inkey public-rsa.pem -in large-message.bin -out large-message.rsa.enc
Public Key operation error
402768C10D7B0000:error:0200006E:rsa routines:ossl_rsa_padding_add_PKCS1_type_2_ex:data too large for key size:../crypto/rsa/rsa_pk1.c:132:

Pokazuje blad, dane wejsciowe sa zbyt duze.

9. Zachowaj komunikat o ograniczeniu rozmiaru, ale nie próbuj obchodzić go przez dzielenie dużego pliku na wiele bloków RSA.
openssl pkeyutl -encrypt -pubin -inkey public-rsa.pem -in large-message.bin -out large-message.rsa.enc 2> rsa-size-error.txt
Sprawdzam wynik sterr do pliku "rsa-size-error.txt":
cat rsa-size-error.txt
Public Key operation error
40F74FAAFB760000:error:0200006E:rsa routines:ossl_rsa_padding_add_PKCS1_type_2_ex:data too large for key size:../crypto/rsa/rsa_pk1.c:132:

### Do zapisania w notatkach

- rozmiar wiadomości wejściowej,
- rezultat porównania pliku pierwotnego i odszyfrowanego,
- rola klucza publicznego,
- rola klucza prywatnego,
- obserwacja dotycząca ograniczenia rozmiaru danych dla RSA.

### Kryterium ukończenia

- istnieją **short-message.rsa.enc** i **short-message.decoded.txt**,
- odszyfrowany tekst jest identyczny z wiadomością wejściową,
- rozumiesz, że bezpośrednie RSA nie jest właściwym mechanizmem szyfrowania dużych plików.

### Pytania kontrolne

1. Dlaczego autor wiadomości nie potrzebuje klucza prywatnego odbiorcy?
Do zaszyfrowania wiadomosci potrzebujemy klucz publicznego odbiorcy docelowego.
Klucz prywatny potrzebny jest do odszyfrowania wiadomosci nadawcy i musi byc tajny.
2. Co umożliwiłoby ujawnienie klucza prywatnego?
Umozliwia odszyfrowanie dane zaszyfrowane odpowiadajacym mu kluczem publicznym.
3. Dlaczego RSA ma ograniczenie rozmiaru danych wejściowych?
Nie mozna zaszyfrowac dowolnie duzego pliku, poniewaz ?
4. Dlaczego w praktyce nie szyfruje się dużego pliku blok po bloku samym RSA?
RSA ma ograniczony rozmiar, nie jest przeznaczony do szyfrowania duzej ilosci danych. Co do zasady nie dzielimy danych na miejsze bloki.
5. Jak ten problem rozwiązuje szyfrowanie hybrydowe?
Duzy plik szyfruje sie algorytmem symetrycznym, np. AES, w klucz algorytmu AES szyfruje sie kluczem publicznym RSA. Odbiorca odszyfrowuje klucz AES swoim kluczem prywatnym RSA
i uzywa klucza AES do odszyfrowania np. duzej porcji informacji.

## 7. Prosty model szyfrowania hybrydowego

### Zadania

1. Wygeneruj nowy, niezależny sekret symetryczny o długości 32 bajtów.
openssl rand -hex 32 > hybrid-aes.key

2. Zapisz go jako **hybrid-aes.key**.
> hybrid-aes.key

3. Ogranicz dostęp do pliku wyłącznie do właściciela.
chmod 600 hybrid-aes.key

4. Użyj tego sekretu do symetrycznego zaszyfrowania **secret.txt**.
openssl enc -aes-256-cbc -salt -pbkdf2 -pass file:hybrid-aes.key -in secret.txt -out hybrid-message.enc

5. Zapisz zaszyfrowane dane jako **hybrid-message.enc**.
-out hybrid-message.enc

6. Zabezpiecz **hybrid-aes.key** za pomocą klucza publicznego RSA odbiorcy.
openssl pkeyutl -encrypt -pubin -inkey public-rsa.pem -in hybrid-aes.key -out hybrid-aes.key.enc

7. Zapisz zaszyfrowany klucz jako **hybrid-aes.key.enc**.
-out hybrid-aes.key.enc

8. Zasymuluj odbiorcę i odzyskaj klucz symetryczny za pomocą klucza prywatnego RSA.
openssl pkeyutl -decrypt -inkey private-rsa.pem -in hybrid-aes.key.enc -out hybrid.aes.recovered.key

9. Zapisz odzyskany sekret jako **hybrid-aes.recovered.key**.
-out hybrid.aes.recovered.key

10. Ogranicz dostęp do odzyskanego klucza.
ls -l hybrid-aes.key hybrid-aes.recovered.key
-rw------- 1 vboxuser vboxuser 65 Oct  8 13:14 hybrid-aes.key
-rw------- 1 vboxuser vboxuser 65 Oct  8 13:21 hybrid-aes.recovered.key

11. Użyj odzyskanego klucza do odszyfrowania **hybrid-message.enc**.
openssl enc -aes-256-cbc -d -salt -pbkdf2 -pass file:hybrid-aes.recovered.key -in hybrid-message.enc -out hybrid-message.decoded.txt

12. Zapisz wynik jako **hybrid-message.decoded.txt**.
-out hybrid-message.decoded.txt

13. Porównaj wynik z **secret.txt**.
cmp secret.txt hybrid-message.decoded.txt && echo "DOBRZE - pliki sa identyczne"
DOBRZE - pliki sa identyczne

14. Narysuj przepływ wskazujący, które dane są szyfrowane symetrycznie, a które asymetrycznie.
NADAWCA
Utworzony hybrid-aes.key
Szyfrujemy synchronicznie dane algorytmem AES-256-CBC ---> hybrid-message.enc
Szyfrujemy klucz hybrid-aes.key asynchronicznie algorytmem RSA za pomoca klucz publicznego odbiorcy public-rsa.pem do pliku hybrid-aes.key.enc
<<<<<<WYSYLAMY>>>>>>
U ODBIORCY: hybrid-aes.key.enc (zaszyfrowany algorytmem asynchronicznym RSA klucz od szyfrowania symetrycznego)
Deszyfracja pliku: hybrid-aes.key za pomoca algorytmu asynchronicznego RSA z uzyciem klucza prywatnego odbiorcy private-rsa.pem
Powstaje plik: hybrid-aes.recovered.key z odszyfrowanym kluczem
Odszyfrowuje plik z danymi: hybrid-message.enc zaszyfrowany synchronicznym algorytmem AES (AES-256-CBC) dajac wynik: hybrid-message.decoded.txt

### Model do odtworzenia

1. Nadawca generuje losowy klucz symetryczny.
2. Dane są szyfrowane szybko za pomocą mechanizmu symetrycznego.
3. Mały klucz symetryczny jest zabezpieczany kluczem publicznym odbiorcy.
4. Odbiorca odzyskuje klucz symetryczny swoim kluczem prywatnym.
5. Odzyskany klucz służy do odszyfrowania danych.

### Do zapisania w notatkach

- nazwa pliku zawierającego zaszyfrowane dane,
- nazwa pliku zawierającego zaszyfrowany klucz,
- informacja, który klucz RSA wykorzystywany jest na każdym etapie,
- rezultat porównania danych,
- wyjaśnienie korzyści wynikających z połączenia obu mechanizmów.

### Kryterium ukończenia

- istnieją **hybrid-message.enc**, **hybrid-aes.key.enc**, **hybrid-aes.recovered.key** i **hybrid-message.decoded.txt**,
- końcowy plik jest identyczny z **secret.txt**,
- potrafisz wskazać osobno chronione dane i chroniony klucz,
- potrafisz wyjaśnić, dlaczego model hybrydowy jest praktyczniejszy od bezpośredniego szyfrowania danych RSA.


## 8. CyberChef — kodowanie i szyfrowanie

### Zadania

1. Otwórz oficjalną instancję CyberChef w przeglądarce.
https://gchq.github.io/CyberChef/

2. Wklej wyłącznie testową zawartość **secret.txt**.
To jest testowa poufna wiadomość do laboratorium z kryptografii.
Nie zawiera prawdziwych sekretów, haseł ani danych osobowych.
Cel: sprawdzić kodowanie, hashowanie, szyfrowanie symetryczne, RSA i model hybrydowy.
DO POLA Input

3. Zakoduj tekst do Base64.
VG8gamVzdCB0ZXN0b3dhIHBvdWZuYSB3aWFkb21vxZvEhyBkbyBsYWJvcmF0b3JpdW0geiBrcnlwdG9ncmFmaWkuCk5pZSB6YXdpZXJhIHByYXdkeml3eWNoIHNla3JldMOzdywgaGFzZcWCIGFuaSBkYW55Y2ggb3NvYm93eWNoLgpDZWw6IHNwcmF3ZHppxIcga29kb3dhbmllLCBoYXNob3dhbmllLCBzenlmcm93YW5pZSBzeW1ldHJ5Y3puZSwgUlNBIGkgbW9kZWwgaHlicnlkb3d5Lgo=

4. Dodaj operację odwrotną i potwierdź odzyskanie oryginału.
To jest testowa poufna wiadomoÅÄ do laboratorium z kryptografii.
Nie zawiera prawdziwych sekretÃ³w, haseÅ ani danych osobowych.
Cel: sprawdziÄ kodowanie, hashowanie, szyfrowanie symetryczne, RSA i model hybrydowy.

5. Usuń wcześniejsze operacje.
Przycisk "Clear Recipe"

6. Przekształć tekst do reprezentacji heksadecymalnej.
54 6f 20 6a 65 73 74 20 74 65 73 74 6f 77 61 20 70 6f 75 66 6e 61 20 77 69 61 64 6f 6d 6f c5 9b c4 87 20 64 6f 20 6c 61 62 6f 72 61 74 6f 72 69 75 6d 20 7a 20 6b 72 79 70 74 6f 67 72 61 66 69 69 2e 0a 4e 69 65 20 7a 61 77 69 65 72 61 20 70 72 61 77 64 7a 69 77 79 63 68 20 73 65 6b 72 65 74 c3 b3 77 2c 20 68 61 73 65 c5 82 20 61 6e 69 20 64 61 6e 79 63 68 20 6f 73 6f 62 6f 77 79 63 68 2e 0a 43 65 6c 3a 20 73 70 72 61 77 64 7a 69 c4 87 20 6b 6f 64 6f 77 61 6e 69 65 2c 20 68 61 73 68 6f 77 61 6e 69 65 2c 20 73 7a 79 66 72 6f 77 61 6e 69 65 20 73 79 6d 65 74 72 79 63 7a 6e 65 2c 20 52 53 41 20 69 20 6d 6f 64 65 6c 20 68 79 62 72 79 64 6f 77 79 2e 0a

7. Przywróć tekst do pierwotnej postaci.
To jest testowa poufna wiadomoÅÄ do laboratorium z kryptografii.
Nie zawiera prawdziwych sekretÃ³w, haseÅ ani danych osobowych.
Cel: sprawdziÄ kodowanie, hashowanie, szyfrowanie symetryczne, RSA i model hybrydowy.

8. Przetestuj kodowanie znaków na potrzeby adresów URL.
Test%20dla%208%2E8

9. Znajdź operację AES i zaszyfruj krótki tekst testowy za pomocą wybranego sekretu laboratoryjnego.
c1426e7fbf6ef0397af569427d6c08dc8f0e82e9d0012e3ec6f42cb5d6ab168f378173a14cafd3b5e5cce1521b257eeec6ef2364fdb55b7478b6bd9c354ac7c6071bc41e95c02403890838696e57cc8ad957b53e2a893797c9b471515095e38a76214040231951c4edd34f0a9ec253ad696fd71bb8d488fc48e14b088cbfa2c183dfa6a87a0eefcca0a55a95a1e6f7345d0c94bc51020e1b9f403600168d847f3e6cd62cfcf0057b8c95fc96f403b3e2552cef8d9e6268ea3de920c49d10e89c9534d1f6c3da493d614d9a8ea8c22a900c193e5b0e300d91cd196a56b29c3261

10. Dodaj odpowiadającą operację deszyfrowania i sprawdź wynik.
To jest testowa poufna wiadomnZ do laboratorium z kryptografii.
Nie zawiera prawdziwych sekretów, hasdB ani danych osobowych.
Cel: sprawdzi kodowanie, hashowanie, szyfrowanie symetryczne, RSA i model hybrydowy.

11. Porównaj operacje niewymagające sekretu z operacją AES.
Base64:
To kodowanie. Nie wymaga hasla ani klucza. Dane mozna odkodowac bez sekretu.

Hex:
Reprezentacja danych w systemie szesnastkowym.
Nie wymaga sekretu i mozna latwo odwrocic.

URL Encode:
Kodowanie znakow do postaci odpowiedniej dla adresow URL.
Nie wymaga sekretu.

AES:
Szyfrowanie. Wymaga odpowiedniego klucza.
Bez poprawnego sekretu nie mozna normalnie odsyzkac pierwotnych informacji.

12. Zapisz albo udokumentuj przepis CyberChef wykorzystany w ćwiczeniu.
To Base64
From Base64

To Hex
from Hex

URL Encode
URL Decode

AES Encrypt
AES Decrypt

W Key i IV wpisac dla przykladu: ciag HEX z aes.key

### Zasady bezpieczeństwa

- nie wklejaj prawdziwych haseł, kluczy, tokenów ani danych prywatnych,
- upewnij się, że korzystasz z właściwej strony,
- pamiętaj, że możliwość odwrócenia operacji nie oznacza automatycznie użycia kryptografii,
- nie traktuj samego wyglądu wyniku jako dowodu bezpieczeństwa.

### Do zapisania w notatkach

- operacje będące kodowaniem,
- operacja będąca szyfrowaniem,
- informacja, które operacje wymagały sekretu,
- różnica między odwracalnością kodowania a deszyfrowaniem z kluczem.

### Kryterium ukończenia

- potrafisz odtworzyć dane zakodowane w Base64 i hex,
- potrafisz wskazać cel URL encoding,
- test AES wymaga odpowiedniego sekretu,
- potrafisz sklasyfikować każdą użytą operację.

## 9. Diagnostyka HTTPS

### Zadania

1. Wybierz publiczną domenę testową obsługującą HTTPS.
github.com

2. Nawiąż połączenie TLS do portu HTTPS za pomocą OpenSSL.
openssl s_client -connect github.com:443 -servername github.com

3. Podaj nazwę serwera w sposób umożliwiający prawidłowy wybór certyfikatu przez usługę.
-servername github.com

4. Odszukaj w wyniku łańcuch certyfikatów.
openssl s_client -connect github.com:443 -servername github.com -showcerts
- showcerts w celu zawezenia poszukiwan

5. Zidentyfikuj certyfikat serwera i jego wystawcę.
Certificate chain
 0 s:CN=github.com
   i:C=GB, O=Sectigo Limited, CN=Sectigo Public Server Authentication CA DV E36
   a:PKEY: EC, (prime256v1); sigalg: ecdsa-with-SHA256
   v:NotBefore: Sep  1 00:00:00 2026 GMT; NotAfter: Nov 29 23:59:59 2026 GMT
-----BEGIN CERTIFICATE-----
MIID7TCCA5SgAwIBAgIRAKWevbWWdR239cCVB5YTlTwwCgYIKoZIzj0EAwIwYDEL
MAkGA1UEBhMCR0IxGDAWBgNVBAoTD1NlY3RpZ28gTGltaXRlZDE3MDUGA1UEAxMu
U2VjdGlnbyBQdWJsaWMgU2VydmVyIEF1dGhlbnRpY2F0aW9uIENBIERWIEUzNjAe
Fw0yNjA5MDEwMDAwMDBaFw0yNjExMjkyMzU5NTlaMBUxEzARBgNVBAMTCmdpdGh1
Yi5jb20wWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAASFNhs0vLNR9yDpqprL6Cct
YNExex040djH16D6WrHxLyjnmVFGYSI4sj6wK3V17ADiaabPE04vQk76djW0DT8q
o4ICeDCCAnQwHwYDVR0jBBgwFoAUF5moBMFv5C1wqAoQPQPT6Rq4JmMwHQYDVR0O
BBYEFGaY7EwRNfdLUISLqBw2ZdAXVtTgMA4GA1UdDwEB/wQEAwIHgDAMBgNVHRMB
Af8EAjAAMBMGA1UdJQQMMAoGCCsGAQUFBwMBMEkGA1UdIARCMEAwNAYLKwYBBAGy
MQECAgcwJTAjBggrBgEFBQcCARYXaHR0cHM6Ly9zZWN0aWdvLmNvbS9DUFMwCAYG
Z4EMAQIBMIGEBggrBgEFBQcBAQR4MHYwTwYIKwYBBQUHMAKGQ2h0dHA6Ly9jcnQu
c2VjdGlnby5jb20vU2VjdGlnb1B1YmxpY1NlcnZlckF1dGhlbnRpY2F0aW9uQ0FE
VkUzNi5jcnQwIwYIKwYBBQUHMAGGF2h0dHA6Ly9vY3NwLnNlY3RpZ28uY29tMIIB
BAYKKwYBBAHWeQIEAgSB9QSB8gDwAHYA1219ENGn9XfCx+lf1wC/+YLJM1pl4dCz
AXMXwMjFaXcAAAGgWk2g0QAABAMARzBFAiB6u6CCyQsap+pmTuz7Ab9THPLWVtQR
PTqSNuC8ZWO6eQIhALM3rJpdu0XVcvSW2985RjODh+9BBR5n8fB5lL7LOXnmAHYA
yKPEf8ezrbk1awE/anoSbeM6TkOlxkb5l605dZkdz5oAAAGgWk2grQAABAMARzBF
AiBwsQvwfVSuEcGqKp4lN/jWPUUuudUX+St4fImVDxCKmQIhANHJvWdzsXH/A9uC
rSz1sQ4k3yowTYxtVtfTJc91oze2MCUGA1UdEQQeMByCCmdpdGh1Yi5jb22CDnd3
dy5naXRodWIuY29tMAoGCCqGSM49BAMCA0cAMEQCIBdBV7Y/5t2o988vMBDGLJEl
LWALzPJkt3dphmsZk9CEAiAJqxa/1c8JYYWHsGy1rQNUb3ffuCJU7pnjjqJfdiim
hQ==
-----END CERTIFICATE-----
 1 s:C=GB, O=Sectigo Limited, CN=Sectigo Public Server Authentication CA DV E36
   i:C=GB, O=Sectigo Limited, CN=Sectigo Public Server Authentication Root E46
   a:PKEY: EC, (prime256v1); sigalg: ecdsa-with-SHA384
   v:NotBefore: Mar 22 00:00:00 2021 GMT; NotAfter: Mar 21 23:59:59 2036 GMT
-----BEGIN CERTIFICATE-----
MIIDXzCCAuagAwIBAgIQNuBZ7YiN1Xrt1XC2cn+b2jAKBggqhkjOPQQDAzBfMQsw
CQYDVQQGEwJHQjEYMBYGA1UEChMPU2VjdGlnbyBMaW1pdGVkMTYwNAYDVQQDEy1T
ZWN0aWdvIFB1YmxpYyBTZXJ2ZXIgQXV0aGVudGljYXRpb24gUm9vdCBFNDYwHhcN
MjEwMzIyMDAwMDAwWhcNMzYwMzIxMjM1OTU5WjBgMQswCQYDVQQGEwJHQjEYMBYG
A1UEChMPU2VjdGlnbyBMaW1pdGVkMTcwNQYDVQQDEy5TZWN0aWdvIFB1YmxpYyBT
ZXJ2ZXIgQXV0aGVudGljYXRpb24gQ0EgRFYgRTM2MFkwEwYHKoZIzj0CAQYIKoZI
zj0DAQcDQgAEaKGnbAUnBYljHDmn/yUhxe3TLxKYuyzc9VXoSaCEV5F73Fhfa/Si
/RMsmwTFW3R9s7J6JpYZFmu4do3vk/Vgl6OCAYEwggF9MB8GA1UdIwQYMBaAFNEi
2kxZ8UtfJjiqndbu6w3D+6lhMB0GA1UdDgQWBBQXmagEwW/kLXCoChA9A9PpGrgm
YzAOBgNVHQ8BAf8EBAMCAYYwEgYDVR0TAQH/BAgwBgEB/wIBADAdBgNVHSUEFjAU
BggrBgEFBQcDAQYIKwYBBQUHAwIwGwYDVR0gBBQwEjAGBgRVHSAAMAgGBmeBDAEC
ATBUBgNVHR8ETTBLMEmgR6BFhkNodHRwOi8vY3JsLnNlY3RpZ28uY29tL1NlY3Rp
Z29QdWJsaWNTZXJ2ZXJBdXRoZW50aWNhdGlvblJvb3RFNDYuY3JsMIGEBggrBgEF
BQcBAQR4MHYwTwYIKwYBBQUHMAKGQ2h0dHA6Ly9jcnQuc2VjdGlnby5jb20vU2Vj
dGlnb1B1YmxpY1NlcnZlckF1dGhlbnRpY2F0aW9uUm9vdEU0Ni5wN2MwIwYIKwYB
BQUHMAGGF2h0dHA6Ly9vY3NwLnNlY3RpZ28uY29tMAoGCCqGSM49BAMDA2cAMGQC
MFsKnBQDh64l+v+aUYWjDCJKQMxHUUGmcwAYDIjJ9pbRYItMCIx5xu0oUb6sIfTX
qQIwPddcsDE4KdeLu1hJdpHgdLvsHAK3vygyLGujMU9xBJCDackRT93VHEE0gppg
NqdV
-----END CERTIFICATE-----
 2 s:C=GB, O=Sectigo Limited, CN=Sectigo Public Server Authentication Root E46
   i:C=US, ST=New Jersey, L=Jersey City, O=The USERTRUST Network, CN=USERTrust ECC Certification Authority
   a:PKEY: EC, (secp384r1); sigalg: ecdsa-with-SHA384
   v:NotBefore: Mar 22 00:00:00 2021 GMT; NotAfter: Jan 18 23:59:59 2038 GMT
-----BEGIN CERTIFICATE-----
MIIDRjCCAsugAwIBAgIQGp6v7G3o4ZtcGTFBto2Q3TAKBggqhkjOPQQDAzCBiDEL
MAkGA1UEBhMCVVMxEzARBgNVBAgTCk5ldyBKZXJzZXkxFDASBgNVBAcTC0plcnNl
eSBDaXR5MR4wHAYDVQQKExVUaGUgVVNFUlRSVVNUIE5ldHdvcmsxLjAsBgNVBAMT
JVVTRVJUcnVzdCBFQ0MgQ2VydGlmaWNhdGlvbiBBdXRob3JpdHkwHhcNMjEwMzIy
MDAwMDAwWhcNMzgwMTE4MjM1OTU5WjBfMQswCQYDVQQGEwJHQjEYMBYGA1UEChMP
U2VjdGlnbyBMaW1pdGVkMTYwNAYDVQQDEy1TZWN0aWdvIFB1YmxpYyBTZXJ2ZXIg
QXV0aGVudGljYXRpb24gUm9vdCBFNDYwdjAQBgcqhkjOPQIBBgUrgQQAIgNiAAR2
+pmpbiDt+dd34wc7qNs9Xzjoq1WmVk/WSOrsfy2qw7LFeeyZYX8QeccCWvkEN/U0
NSt3zn8gj1KjAIns1aeibVvjS5KToID1AZTc8GgHHs3u/iVStSBDHBv+6xnOQ6Oj
ggEgMIIBHDAfBgNVHSMEGDAWgBQ64QmG1M8ZwpZ2dEl23OA1xmNjmjAdBgNVHQ4E
FgQU0SLaTFnxS18mOKqd1u7rDcP7qWEwDgYDVR0PAQH/BAQDAgGGMA8GA1UdEwEB
/wQFMAMBAf8wHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMBEGA1UdIAQK
MAgwBgYEVR0gADBQBgNVHR8ESTBHMEWgQ6BBhj9odHRwOi8vY3JsLnVzZXJ0cnVz
dC5jb20vVVNFUlRydXN0RUNDQ2VydGlmaWNhdGlvbkF1dGhvcml0eS5jcmwwNQYI
KwYBBQUHAQEEKTAnMCUGCCsGAQUFBzABhhlodHRwOi8vb2NzcC51c2VydHJ1c3Qu
Y29tMAoGCCqGSM49BAMDA2kAMGYCMQCMCyBit99vX2ba6xEkDe+YO7vC0twjbkv9
PKpqGGuZ61JZryjFsp+DFpEclCVy4noCMQCwvZDXD/m2Ko1HA5Bkmz7YQOFAiNDD
49IWa2wdT7R3DtODaSXH/BiXv8fwB9su4tU=
-----END CERTIFICATE-----


6. Sprawdź nazwę domeny oraz daty ważności certyfikatu.
 0  v:NotBefore: Sep  1 00:00:00 2026 GMT; NotAfter: Nov 29 23:59:59 2026 GMT
 1  v:NotBefore: Mar 22 00:00:00 2021 GMT; NotAfter: Mar 21 23:59:59 2036 GMT
 2  v:NotBefore: Mar 22 00:00:00 2021 GMT; NotAfter: Jan 18 23:59:59 2038 GMT

7. Odczytaj wynegocjowaną wersję TLS i zestaw szyfrów.
New, TLSv1.3, Cipher is TLS_AES_128_GCM_SHA256
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_128_GCM_SHA256

Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_128_GCM_SHA256


8. Sprawdź wynik walidacji certyfikatu.
openssl s_client -connect github.com:443 -servername github.com -verify_hostname github.com -verify_return_error </dev/null
SSL handshake has read 3087 bytes and written 1616 bytes
Verification: OK
Verified peername: github.com

9. Zakończ połączenie, jeżeli narzędzie oczekuje na dalsze dane.
Ctrl+c

10. Pobierz same nagłówki odpowiedzi przez HTTPS.
BEZ:
curl -I github.com
HTTP/1.1 301 Moved Permanently
Content-Length: 0
Location: https://github.com/
Z HTTPS:
curl -I https://github.com
HTTP/2 200 
date: Thu, 08 Oct 2026 14:23:48 GMT
content-type: text/html; charset=utf-8
content-language: en-US

11. Wykonaj analogiczną próbę przez HTTP.
curl -I http://github.com
HTTP/1.1 301 Moved Permanently
Content-Length: 0
Location: https://github.com/

12. Sprawdź, czy usługa przekierowuje ruch z HTTP do HTTPS.
TAK:
HTTP/1.1 301 Moved Permanently
Content-Length: 0
Location: https://github.com/

13. Porównaj ochronę kanału z bezpieczeństwem samej aplikacji.
HTTPS chroni kanal komunikacji,
nie gwarantuje jednak, ze sama aplikacja jest bezpieczna.

### Do zapisania w notatkach

- testowana domena,
- nazwa podmiotu certyfikatu,
- wystawca,
- okres ważności,
- wynegocjowana wersja TLS,
- zestaw szyfrów,
- wynik walidacji,
- zachowanie HTTP,
- najważniejszy wniosek dotyczący zakresu ochrony HTTPS.

### Kryterium ukończenia

- potrafisz odnaleźć podstawowe informacje o certyfikacie i połączeniu,
- potrafisz sprawdzić nagłówki odpowiedzi HTTPS,
- potrafisz ustalić, czy HTTP jest przekierowywane,
- rozumiesz, że HTTPS chroni transmisję, ale nie usuwa podatności aplikacji.

### Pytania kontrolne

1. Dlaczego klient sprawdza nazwę domeny w certyfikacie?
Upewnia sie, ze certyfikat zostal wystawiony dla serwera z ktorym chcemy sie polaczyc, a nie do kogos innego.
2. Jaką rolę pełni urząd certyfikacji?
CA podpisuje certyfikat i potwierdza jego powiazanie z okreslona domena lub firma
3. Co oznacza data wygaśnięcia certyfikatu?
Okresla moment, po ktorym nie powinnismy juz ufac temu nieaktualnemu certyfikatowi i stronie z ktora sie laczymy.
4. Dlaczego nazwa serwera przekazana podczas zestawiania połączenia ma znaczenie?
Jeden serwer moze obslugiwac wiele domen, nazwa pozwala wybrac wlasciwa certyfikat dla zadanej domeny.
5. Co może chronić HTTPS?
Chroni dane przesylane pomiedzy klientem, a serwerem przed podsluchalem tresci i nieautoryzowana modyfikacja. Pozwala tez na weryfikacje tozsamosci na podstawie certyfikatu strony.
6. Jakich błędów aplikacji HTTPS nie naprawia?
HTTPS nie usuwa podatnosci w kodzie aplikacji, jak znane np. SQL Injection, XSS, bledne autoryzacje, zla konfiguracja.

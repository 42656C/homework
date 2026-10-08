# Laboratorium 15 - notatki

## Srodowisko

Wersja OpenSSL: OpenSSL 3.5.5

Uwagi:


## 1. Kodowanie to nie szyfrowanie

Wynik Base64: VG8gamVzdCB0ZXN0b3dhIHBvdWZuYSB3aWFkb21vxZvEhyBkbyBsYWJvcmF0b3JpdW0geiBrcnlw
dG9ncmFmaWkuCk5pZSB6YXdpZXJhIHByYXdkeml3eWNoIHNla3JldMOzdywgaGFzZcWCIGFuaSBk
YW55Y2ggb3NvYm93eWNoLgpDZWw6IHNwcmF3ZHppxIcga29kb3dhbmllLCBoYXNob3dhbmllLCBz
enlmcm93YW5pZSBzeW1ldHJ5Y3puZSwgUlNBIGkgbW9kZWwgaHlicnlkb3d5LgoK

Czy Base64 wymaga sekretu: Nie, poniewaz do zakodowania i odkodowania danych nie jest wymagane haslo ani klucz.

Czy Base64 zapewnia poufnosc: Nie - dane mozna latwo i szybko odkodowac.

Roznica miedzy kodowaniem a szyfrowaniem:
Kodowanie zmienia sposob pokazywania danych i jest odwracalne.
Szyfrowanie ma za zadanie zapewniac poufnosc danych i aby te dane odszyfrowac wymagany jest odpowiedni klucz lub sekret.


## 2. Hash pliku i integralnosc

Pierwszy SHA-256: 18a64d61a7b3f1735b4e0d148cb85a4d5e8e5b7a23acc1f9a896555450e5101a

SHA-256 po zmianie danych: 0bde33dd38dfc0790b4b75dfdc116f4892df34d1a12aabc5af6b9d60027bb8f3

Obserwacje:
Dodanie nowej linii do pliku spowodowalo zmiane wartosci SHA-256. Otrzymalismy inna wartosc niz pierwotna.

Czy hash zapewnia poufnosc:
Nie. Hash sluzy do kontroli integralnosci danych i ich nie szyfruje, nie ukrywa zawartosci.

Czy funkcja skrotu jest odwracalna:
Na podstawie samej wartosci SHA-256 nie jest mozliwe w prosty sposob odtworzenie pierwotnej/oryginalnej zawartosci pliku.


## 3. Szyfrowanie symetryczne AES

Algorytm i tryb:
AES-256-CBC

Rola soli:
Nie musi byc tajna. Uzycie tego samego hasla z inna sola daje inny material do kryptografii.

Rola PBKDF2:
Wprowadza klucz kryptograficzny z hasla przy wykorzystaniu soli i iteracji. Ma za zadanie utrudnic szybkie odgadniecie hasla.

Wynik porownania plikow:
decoded.txt jest taki sami jak secret.txt
Polecenie cmp (compare) nie pokazalo roznicy.

Wynik proby z blednym haslem:
Bledne haslo nie deszyfrowalo nam pliku do pierwotnej wartosci wiadomosci.
OpenSSL zglosil blad.

Wnioski:
Poprawnosc szyfrowania zostala sprawdzona przez odszyfrowanie i porownanie wyniku z oryginalnym plikiem.


## 4. Haslo, klucz i losowosc

Sposob uzyskania losowosci:
Sekret wygenerowano za pomoca:
openssl rand -hex 32 > aes.key

Dlugosc sekretu:
32 bajty = 256 bitow = 64 znaki heksadecymalne (kazdy po 4 bity)
Plik zawiera dodatkowo znak konca linii "$" (65 znakow)

Roznica miedzy haslem a losowym sekretem:
Haslo stworzone przez czlowieka najczesciej bywa przewidywalne o niskiej entropii.
Sekret wykonany kryptograficznie jest bardziej losowy i trudniejszy do odgadniecia.

Uprawnienia aes.key:
-rw------- 1 vboxuser vboxuser 65 Oct  8 12:19 aes.key
Dostep do pliku ma tylko jego wlasciciel.

Ograniczenia ochrony:
Jesli napastnik zdobedzie zarowno zaszyfrowany plik jak i aes.key (w naszym przypadku),
bedzie mogl wykorzystac ten sekret z pliku aes.key do odszyfrowania danych.
Klucz powinien byc przechowywany oddzielnie od szyfrogramu.

## 5. Para kluczy RSA

Klucz prywatny:
private-rsa.pem

Klucz publiczny:
public-rsa.pem

Rozmiar RSA:
3072 bity

Uprawnienia klucza prywatnego:
600, czyli rw-------
Dostep do pliku ma tylko jego wlascidiel.

Ktory klucz mozna udostepnic:
Tylko publiczny: public-rsa.pem

Znaczenie autentycznosci klucza publicznego:
Musimy potwierdzic, ze klucz publiczny ktory dostalismy, rzeczywiscie nalezy do docelowego odbiory.

## 6. RSA - szyfrowanie malego pliku

Rozmiar wiadomosci:
43

Wynik porownania:
short-message.txt i short.message.decoded.txt sa identyczne,
poniewaz polecenie cmp nie wykazalo roznicy.

Rola klucza publicznego:
Klucz publiczny odbiorcy zostaje wykorzystany do zaszyfrowania wiadomosci.
Sluzy do udostepnienia go nadawcom.

Rola klucza prywatnego:
Klucz prywatny sluzy do odszyfrowania wiadomosci i musi byc tajny.

Ograniczenie rozmiaru RSA:
Zbyt duzy rozmiar danych wejsciowych powoduje blad. Nie mozna szyfrowac tym sposobem dowolnie duzych plikow.

## 7. Szyfrowanie hybrydowe

Plik z zaszyfrowanymi danymi:
hybrid-message.enc

Plik z zaszyfrowanym kluczem:
hybrid-aes.key.enc

Uzyte klucze RSA:
public-rsa.pem zostal wykorzystany do zaszyfrowania sekretu hybrid-aes.key

Wynik porownania:
hybrid-aes.key i hybrid-aes.recovered.key sa identyczne.
secret.txt i hybrid-message.decoded.txt sa identyczne.

Korzyści modelu hybrydowego:
Duza ilosc informacji szyfrowana jest za pomoca algorytmu szyfrujacego synchronicznie AES.
Szyfrowanie asynchroniczne RSA sluzy do zabezpieczenia sekretu symetrycznego.
Mozna w ten sposob bezpiecznie przekazac sekret od szyfrowania synchronicznego odbiorcy bez koniecznosci proby szyfrowania duzego pliku za pomoca RSA.

## 8. CyberChef

Operacje kodowania:
To Base64
From Base64

To Hex
From Hex

URL Encode
URL Decode

Operacja szyfrowania:
AES Encrypt
AES Decrypt

Ktore operacje wymagaly sekretu:
AES wymagal odpowiedniego klucza z sekretem.

Kodowanie a deszyfrowanie:
Zakodowane dane mozna przywrocic bez znajomosci klucza.
W przypadku AES do odszyfrowania potrzebny jest pasujacy sekret.


## 9. Diagnostyka HTTPS

Domena:
github.com

Podmiot certyfikatu:
s:CN=github.com

Wystawca:
i:C=GB, O=Sectigo Limited, CN=Sectigo Public Server Authentication CA DV E36

Okres waznosci:
v:NotBefore: Sep  1 00:00:00 2026 GMT; NotAfter: Nov 29 23:59:59 2026 GMT

Wersja TLS:
TLSv1.3

Zestaw szyfrow:
Cipher    : TLS_AES_128_GCM_SHA256

Wynik walidacji:
SSL handshake has read 3087 bytes and written 1616 bytes
Verification: OK
Verified peername: github.com

Zachowanie HTTP:
Polaczenie przez HTTP zostalo przekierowane do HTTPS.
Serwer zwrocil kod 300 oraz Location wskazujacy adres z HTTPS.

Wniosek:
HTTPS chroni transmisje pomiedzy klientem a serwerem,
zapewnia miedzy innymi pufnosc i integralnosc danych
oraz mozliwosc uwierzytelnienia serwera przez certyfikat.
HTTPS jednak nie usuwa bledow bezpieczenstwa samej aplikacji.

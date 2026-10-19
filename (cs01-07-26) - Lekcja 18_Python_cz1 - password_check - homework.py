## password = input("Podaj haslo: ")
## valid, problems = validate_password(password)

def validate_password(password, min_lenght=12):
    problems = []

    if password == "":
        problems.append("BLAD - Haslo nie moze byc puste")

    if len(password) < min_lenght:
        problems.append("BLAD - Haslo ma mniej niz 12 znakow")

    if password.startswith(" ") or password.endswith(" "):
        problems.append("BLAD - Haslo ma spacje na poczatku lub na koncu")

    has_lowercase = False
    has_uppercase = False
    has_digit = False
    has_special = False
    special_chars = set("!@#$%^&*")

    for char in password:
        if char.islower():
            has_lowercase = True
        if char.isupper():
            has_uppercase = True
        if char.isdigit():
            has_digit = True
        if char in special_chars:
            has_special = True

    if not has_lowercase:
        problems.append("Brak malej litery")
    if not has_uppercase:
        problems.append("Brak wielkiej litery")
    if not has_digit:
        problems.append("Brak cyfry")
    if not has_special:
        problems.append("Brak znaku specjalnego")

    is_valid = len(problems) == 0
    return is_valid, problems

def print_result(is_valid, problems):
    if is_valid:
        print("Haslo spelnia polityke")
    else:
        print("Haslo nie spelnia polityki:")
        for problem in problems:
            print("-", problem)

def run_tests():
    test_cases = {
        "Puste haslo": "",
        "Za krotskie haslo": "admin",
        "Brak malej litery": "PASSWORD123!",
        "Brak wielkiej litery": "password123!",
        "Brak cyfry": "PasswordTest!",
        "Brak znaku specjalnego": "Password1234",
        "Znak spoza dozwolonego zestawu": "Password123?",
        "Spacje na brzegach": " Password123! ",
        "Poprawne haslo": "VeryStrongPassword2026!",
    }

    print("\n--- Testy dla minimalnej dlugosci 12 znakow ---")

    for name, test_password in test_cases.items():
        test_valid, test_problems = validate_password(test_password)
        print("\nPrzypadek:", name)
        print_result(test_valid, test_problems)

def main():
    setting = input("Minimalna dlugosc hasla (Enter = 12):")

    if setting == "":
        min_lenght = 12
    else:
        try:
            min_lenght = int(setting)
        except ValueError:
            print("Blad konfiguracji: podaj liczbe calkowita.")
            return

    if min_lenght < 1:
        print("Blad konfiguracji: dlugosc musi byc wieksza od zera.")
        return

    password = input("Podaj haslo: ")

    is_valid, problems = validate_password(password, min_lenght)
    
    print_result(is_valid, problems)

    run_tests()

main()
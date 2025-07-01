import requests

def stahni_ciselnik_pravnich_forem():
    """
    Načte číselník právních forem z ARES API.

    :return: Seznam položek číselníku právních forem nebo prázdný list při chybě.
    """
    url = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ciselniky-nazevniky/vyhledat"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "kodCiselniku": "PravniForma",
        "zdrojCiselniku": "res"
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return response.json()["ciselniky"][0]["polozkyCiselniku"]
        else:
            print("Nepodařilo se načíst číselník právních forem.")
    except requests.exceptions.RequestException as e:
        print(f"Chyba při načítání číselníku: {e}")
    return []

def najdi_pravni_formu(kod, ciselnik):
    """
    Vrátí název právní formy podle kódu z číselníku.

    :param kod: Kód právní formy (např. "112")
    :param ciselnik: Seznam položek číselníku
    :return: Název právní formy v češtině nebo "Neznámá právní forma"
    """
    for polozka in ciselnik:
        if polozka.get("kod") == kod:
            nazvy = polozka.get("nazev", [])
            for nazev in nazvy:
                if nazev.get("kodJazyka") == "cs":
                    return nazev.get("nazev", "Neznámá právní forma")
    return "Neznámá právní forma"

def vyhledej_subjekty_dle_nazvu(nazev):
    """
    Zavolá ARES API a vrátí seznam subjektů podle obchodního jména.

    :param nazev: Hledaný název subjektu
    :return: Slovník s výsledky nebo None při chybě
    """
    url = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {"obchodniJmeno": nazev}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print("Subjekt nebyl nalezen (404 Not Found).")
        elif response.status_code == 400:
            print("Špatný požadavek (400 Bad Request). Zkontroluj formát názvu.")
        elif response.status_code == 500:
            print("Chyba na straně serveru (500 Internal Server Error).")
        else:
            print("Došlo k jiné chybě.")
    except requests.exceptions.RequestException as e:
        print(f"Chyba při komunikaci s API: {e}")
    return None

def zobraz_subjekty(vysledky, ciselnik):
    """
    Vypíše seznam subjektů s obchodním jménem, IČO a právní formou.

    :param vysledky: Slovník vrácený API
    :param ciselnik: Seznam právních forem
    """
    pocet = vysledky.get("pocetCelkem", 0)
    print(f"Nalezeno subjektů: {pocet}")

    if pocet == 0:
        print("Nebyl nalezen žádný subjekt s tímto názvem.")
        return

    for subjekt in vysledky.get("ekonomickeSubjekty", []):
        jmeno = subjekt.get("obchodniJmeno", "Neznámý název")
        ico = subjekt.get("ico", "Neznámé IČO")
        kod_formy = subjekt.get("pravniForma", {}).get("kod") if isinstance(subjekt.get("pravniForma"), dict) else subjekt.get("pravniForma")
        nazev_formy = najdi_pravni_formu(kod_formy, ciselnik)
        print(f"{jmeno}, {ico}, {nazev_formy}")

def spust_dotaz():
    """
    Spustí vyhledávání subjektů podle názvu s interaktivním vstupem.
    """
    nazev = input("Zadej název subjektu pro hledání: ").strip()
    vysledky = vyhledej_subjekty_dle_nazvu(nazev)
    if vysledky:
        ciselnik = stahni_ciselnik_pravnich_forem()
        zobraz_subjekty(vysledky, ciselnik)

# Spuštění skriptu
spust_dotaz()

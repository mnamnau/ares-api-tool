import requests #request to a web page

#ico 03650120
#přidávám právní formu

def stahni_ciselnik_pravnich_forem(): #načte čísleník právních forem
    url = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ciselniky-nazevniky/vyhledat"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "kodCiselniku": "PravniForma",
        "zdrojCiselniku": "res"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["ciselniky"][0]["polozkyCiselniku"]
    else:
        print("Nepodařilo se načíst číselník právních forem.")
        return []

def najdi_pravni_formu(kod, ciselnik):
    for polozka in ciselnik:
        if polozka.get("kod") == kod:
            nazvy = polozka.get("nazev", [])
            for nazev in nazvy:
                if nazev.get("kodJazyka") == "cs":
                    return nazev.get("nazev", "Neznámá právní forma")
    return "Neznámá právní forma"

def najdi_subjekt_dle_nazvu():
    nazev = input("Zadej název subjektu pro hledání: ").strip()  # definice názvu subjektu

    url = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {"obchodniJmeno": nazev}

    response = requests.post(url, headers=headers, json=data)

    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Všechno proběhlo v pořádku (200 OK).")
        vysledky = response.json()

        pocet = vysledky.get("pocetCelkem", 0)
        print(f"Nalezeno subjektů: {pocet}")

        if pocet == 0:
            print("Nebyl nalezen žádný subjekt s tímto názvem.")
            return

        # Načteme číselník právních forem
        pravni_formy = stahni_ciselnik_pravnich_forem()

        # Výpis subjektů včetně právní formy
        for subjekt in vysledky.get("ekonomickeSubjekty", []):
            jmeno = subjekt.get("obchodniJmeno", "Neznámý název")
            ico = subjekt.get("ico", "Neznámé IČO")
            #kod_formy = subjekt.get("pravniForma", {}).get("kod") #nefunční, předpokládá se, že bude vrácen slovník
            pravni_forma = subjekt.get("pravniForma")
            if isinstance(pravni_forma, dict):
                kod_formy = pravni_forma.get("kod")
            else:
                kod_formy = pravni_forma  # použiju řetězec (např. "112")
            nazev_formy = najdi_pravni_formu(kod_formy, pravni_formy)
            print(f"{jmeno}, {ico}, {nazev_formy}")

    elif response.status_code == 404:
        print("Subjekt nebyl nalezen (404 Not Found).")
    elif response.status_code == 400:
        print("Špatný požadavek (400 Bad Request). Zkontroluj formát názvu.")
    elif response.status_code == 500:
        print("Chyba na straně serveru (500 Internal Server Error).")
    else:
        print("Došlo k jiné chybě.")

najdi_subjekt_dle_nazvu()

import requests #request to a web page

#hledám podle ICO
#ico 03650120

def najdi_subjekt_dle_ico():
    """
    Vyhledá subjekt podle zadaného IČO pomocí ARES API.

    :param ico: IČO subjektu jako řetězec (string)
    :return: Slovník s výsledky nebo chybová zpráva
    """
    ico = input("Zadej IČO subjektu: ").strip() #odstraněné mezery
    url = f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}" #vkládám  URL
    """
    doplněná podmínka timeout, aby se program nezasekl při neodpovídajícím API
    """
    try:
        response = requests.get(url, timeout=10)  # přidán timeout
    except requests.exceptions.Timeout:
        print("Požadavek vypršel (timeout). Zkuste to prosím znovu.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Nastala chyba při komunikaci s API: {e}")
        return

    print(f"Status code: {response.status_code}") #doplněno pro přehlednost
    if response.status_code == 200:
        print("Všechno proběhlo v pořádku (200 OK).")
        data = response.json() #ve formátu json
        obchodni_jmeno = data.get("obchodniJmeno", "Neznámé jméno") #viz testovaci_script_json
        adresa = data.get("sidlo", {}).get("textovaAdresa", "Neznámá adresa")

        print(obchodni_jmeno)
        print(adresa)

    elif response.status_code == 404:
        print("Subjekt s tímto IČO nebyl nalezen (404 Not Found).")
    elif response.status_code == 400:
        print("Špatný požadavek (400 Bad Request). Zkontroluj formát IČO.")
    elif response.status_code == 500:
        print("Chyba na straně serveru (500 Internal Server Error).")
    else:
        print("Došlo k jiné chybě.")

najdi_subjekt_dle_ico()

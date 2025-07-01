import requests #request to a web page

#ico 03650120
#hledám podle názvu

def najdi_subjekt_dle_nazvu():
    """
    Vyhledá subjekt podle zadaného IČO pomocí ARES API.

    :param ico: IČO subjektu jako řetězec (string)
    :return: Slovník s výsledky nebo chybová zpráva
    """
    nazev = input("Zadej název subjektu pro hledání: ").strip() #definuju název subjektu
    url = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat"
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    data = {"obchodniJmeno": nazev} 
    # Připravuji data pro POST požadavek jako JSON, kde "obchodniJmeno" je název subjektu, který hledám.
    # Používám slovník, který bude převeden na JSON formát při odeslání požadavku.
    # Přidávám timeout pro případ, že API neodpovídá, aby se program nezasekl.
    # Pokud by API neodpovídalo, program vypíše chybovou zprávu a skončí.   
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
    except requests.exceptions.Timeout:
        print("Požadavek vypršel (timeout). Zkuste to prosím znovu.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Nastala chyba při komunikaci s API: {e}")
        return
    
    print(f"Status code: {response.status_code}") 
    #doplněno pro přehlednost
    # Zpracování odpovědi:
    # Pokud je odpověď úspěšná (status code 200), zpracuji JSON data.
    # Pokud je odpověď s chybou, vypíšu příslušnou chybovou zprávu.
    if response.status_code == 200:     # Zpracování odpovědi podle typu výsledku:
        print("Všechno proběhlo v pořádku (200 OK).")
        vysledky = response.json() # Dostanu obsah odpovědi jako JSON (slovník)

        pocet = vysledky.get("pocetCelkem", 0) # Dostanu vypsaný celkový počet nalezených subjektů
        print(f"Nalezeno subjektů: {pocet}")

        if pocet == 0: #přidáno jako info, že zadávany subjekt neexistuje
            print("Nebyl nalezen žádný subjekt s tímto názvem.")
            return

        for subjekt in vysledky.get("ekonomickeSubjekty", []): # Projde jednotlivé nalezené subjekty a vytáhne jejich jméno a IČO
            jmeno = subjekt.get("obchodniJmeno", "Neznámý název")
            ico = subjekt.get("ico", "Neznámé IČO")
            print(f"{jmeno}, {ico}")

    # Zpracování různých typů chyb:
    elif response.status_code == 404:
        print("Subjekt nebyl nalezen (404 Not Found).")
    elif response.status_code == 400:
        print("Špatný požadavek (400 Bad Request). Zkontroluj formát názvu.")
    elif response.status_code == 500:
        print("Chyba na straně serveru (500 Internal Server Error).")
    else:
        print("Došlo k jiné chybě.")

najdi_subjekt_dle_nazvu()

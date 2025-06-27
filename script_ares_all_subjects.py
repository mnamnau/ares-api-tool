import requests
import json

#vypíše všechny údaje k subjektu

def vypis_json_pro_ico():
    ico = input("Zadej IČO subjektu: ").strip()
    url = f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False)) # Vypíše celý JSON
    else:
        print(f"Chyba při dotazu. Status code: {response.status_code}")

vypis_json_pro_ico()

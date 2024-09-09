import json
import os
import requests
from dotenv import dotenv_values

# Carica la chiave API da .env
dotenv = dotenv_values()
api_key = dotenv.get("API_KEY")

# Funzione per cercare il POI nel database per ID o nome
def trova_poi(poi_input, poi_dict):
    if poi_input in poi_dict:  # Cerca per ID
        return poi_input
    else:  # Cerca per nome
        for poi_id, nome in poi_dict.items():
            if nome.lower() == poi_input.lower():
                return poi_id
    return None

# Funzione per verificare se ci sono nuove recensioni da aggiungere
def aggiungi_recensioni(poi_id, recensioni_per_location, api_key):
    url = f"https://api.content.tripadvisor.com/api/v1/location/{poi_id}/reviews?key={api_key}&language=it"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    REC = response.json()

    nuove_recensioni = 0
    if 'data' in REC:
        for elemento in REC['data']:
            id_rec = elemento.get('id')
            id_loc = elemento.get('location_id')
            data = elemento.get('published_date')
            url = elemento.get('url')
            rating = elemento.get('rating')
            recensione = elemento.get('text')

            if id_loc not in recensioni_per_location:
                recensioni_per_location[id_loc] = {}

            if id_rec not in recensioni_per_location[id_loc]:
                recensioni_per_location[id_loc][id_rec] = {
                    'rating': rating, 'recensione': recensione, 'data': data, 'url': url
                }
                nuove_recensioni += 1

    return nuove_recensioni

# Funzione principale
def main(poi_input):
    # Carica il dizionario dei POI (id:nome)
    with open('poi.json', 'r', encoding='utf-8') as f:
        poi_dict = json.load(f)
    
    # Carica il file delle recensioni esistenti
    recensioni_path = 'recensioni_per_location.json'
    if os.path.exists(recensioni_path):
        with open(recensioni_path, 'r', encoding='utf-8') as f:
            recensioni_per_location = json.load(f)
    else:
        recensioni_per_location = {}

    # Cerca il POI nel database per ID o nome
    poi_id = trova_poi(poi_input, poi_dict)

    if poi_id is None:
        print(f"L'operazione non è andata a buon fine: non esiste alcun POI con quel nome/id")
        return
    
    # Verifica se ci sono recensioni già presenti nel database per questo POI
    if poi_id in recensioni_per_location:
        print(f"L'operazione non è andata a buon fine: le recensioni relative a quel POI sono già presenti nel database")
        return
    
    # Recupera le recensioni dall'API
    nuove_recensioni = aggiungi_recensioni(poi_id, recensioni_per_location, api_key)

    if nuove_recensioni > 0:
        # Salva il file aggiornato con le nuove recensioni
        with open(recensioni_path, 'w', encoding='utf-8') as f:
            json.dump(recensioni_per_location, f, ensure_ascii=False, indent=4)
        print(f"L'operazione è andata a buon fine: sono state aggiunte al database {nuove_recensioni} recensioni relative al POI {poi_dict[poi_id]}")
    else:
        print(f"L'operazione non è andata a buon fine: non ci sono nuove recensioni per il POI {poi_dict[poi_id]}")

# Esecuzione dello script
if __name__ == "__main__":
    # Esempio di input, potrebbe essere sostituito da input dinamico con input() o argomenti da riga di comando
    poi_input = input("Inserisci il nome o l'ID del POI: ")
    main(poi_input)

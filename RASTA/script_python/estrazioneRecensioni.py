'''
Script per estrarre le recensioni da Tripadvisor dei POI precedentemente scaricati.
Lo fa periodicamente per evitare di superare i limiti di richiesta dell'API e per 
tenere sempre aggiornate le recensioni.

'''
import json
import os
from dotenv import dotenv_values
import requests

dotenv = dotenv_values()
api_key = dotenv.get("API_KEY");

# Inizializzo un dizionario vuoto per memorizzare gli ID e i nomi dei POI
poi_dict = {}

# Leggo il contenuto del file riga per riga
with open('script_python/poi.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # Divido la riga usando ': ' come separatore solo alla prima occorrenza
        id, resto = line.strip().split(': ', 1)
        # Divido il resto della riga usando ', ' come separatore per ottenere il nome del POI
        nome = resto.split(', ')[0]
        # Aggiungo l'id e il nome al dizionario
        poi_dict[id] = nome

# il dizionario ora conterrà gli ID come chiavi e i nomi dei POI come valori
# print(poi_dict)
print(len(poi_dict))

# salvo il dizionario in un file json
dizionario_json = "script_python/poi.json"

# Salvataggio del dizionario nel file JSON
with open(dizionario_json, "w") as file:
    json.dump(poi_dict, file)

# Dizionario per memorizzare le recensioni per ogni location
recensioni_per_location = {}

# salvo tutti gli id delle recensioni in questa variabile
id_recensioni = []

# Verifico che il dizionario esista, e se esiste già, salvo il contenuto in recensioni_per_location
if os.path.exists('script_python/recensioni_per_location.json'):
    with open('script_python/recensioni_per_location.json', 'r') as file:
        recensioni_per_location = json.load(file)

        # Estraggo gli ID delle recensioni e li aggiungo alla lista id_recensioni
        for id_loc in recensioni_per_location.values():
            for id_rec in id_loc.keys():
                id_recensioni.append(id_rec)
else:
    recensioni_per_location = {}

# Recupero le recensioni relative ai POI estratti
items_list = list(poi_dict.items())

# Itero sui POI e recupera le recensioni
for id in items_list[:3]:
    url = "https://api.content.tripadvisor.com/api/v1/location/" + id[0] + "/reviews?key=" + api_key + "&language=it"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    REC = response.json()

    # Estraggo le recensioni di ciascun POI e le aggiungo al dizionario
    for elemento in REC['data']:
        id_rec = elemento.get('id')
        id_loc = elemento.get('location_id')
        data = elemento.get('published_date')
        url = elemento.get('url')
        rating = elemento.get('rating')
        recensione = elemento.get('text')

         # Se la location_id non è già presente nel dizionario, l'aggiungo come chiave con una lista vuota come valore
        if id_loc not in recensioni_per_location:
            recensioni_per_location[id_loc] = {}

        if id_rec not in id_recensioni:
            # Aggiungo la recensione al dizionario nidificato utilizzando l'id della recensione come chiave
            recensioni_per_location[id_loc][id_rec] = {'rating': rating, 'recensione': recensione, 'data': data, 'url': url}
            
            # Aggiungo l'id della recensione alla lista id_recensioni
            id_recensioni.append(id_rec)

# Scrivo il dizionario di recensioni su un file JSON
with open('script_python/recensioni_per_location.json', 'w') as file:
    json.dump(recensioni_per_location, file)
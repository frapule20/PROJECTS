'''
Script per estrarre le recensioni da Tripadvisor dei POI precedentemente scaricati.
Lo fa periodicamente per evitare di superare i limiti di richiesta dell'API e per 
tenere sempre aggiornate le recensioni.

'''
import json
import os
import time
import requests
from dotenv import dotenv_values

dotenv = dotenv_values()
api_key = dotenv.get("API_KEY")

# File per tenere traccia dello stato
state_file = 'last_processed_poi.json'

# Funzione per caricare lo stato dell'ultimo POI processato
def load_last_processed_poi():
    if os.path.exists(state_file):
        with open(state_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('last_processed_index', 0)
    return 0

# Funzione per salvare l'indice dell'ultimo POI processato
def save_last_processed_poi(last_processed_index):
    with open(state_file, 'w', encoding='utf-8') as file:
        json.dump({'last_processed_index': last_processed_index}, file)

# Inizializzo un dizionario vuoto per memorizzare gli ID e i nomi dei POI
poi_dict = {}

# Leggo il contenuto del file POI riga per riga
with open('poi.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # Divido la riga usando ': ' come separatore solo alla prima occorrenza
        id, resto = line.strip().split(': ', 1)
        nome = resto.split(', ')[0]
        poi_dict[id] = nome

# Converti il dizionario in una lista di tuple (id, nome) per un accesso ordinato
items_list = list(poi_dict.items())

# Carico l'ultimo POI processato
last_processed_index = load_last_processed_poi()

# Numero di POI da processare ogni giorno
num_poi_per_day = 5

# Calcolo gli indici dei prossimi POI da elaborare
start_index = last_processed_index
end_index = start_index + num_poi_per_day

# Seleziono i prossimi POI da processare
poi_to_process = items_list[start_index:end_index]

# Dizionario per memorizzare le recensioni per ogni location
recensioni_per_location = {}

# Verifico che il dizionario esista, e se esiste già, salvo il contenuto in recensioni_per_location
if os.path.exists('recensioni_per_location.json'):
    with open('recensioni_per_location.json', 'r', encoding='utf-8') as file:
        recensioni_per_location = json.load(file)
else:
    recensioni_per_location = {}

 # Conteggio delle nuove recensioni
nuove_recensioni = 0
    
# Itero sui POI selezionati e recupero le recensioni
for poi in poi_to_process:
    location_id = poi[0]
    nome_poi = poi[1]
    
    url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/reviews?key={api_key}&language=it"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)


    # Se la richiesta ha successo, estraggo le recensioni
    if response.status_code == 200:
        REC = response.json()


        # Estraggo le recensioni di ciascun POI e le aggiungo al dizionario
        for elemento in REC.get('data', []):
            id_rec = elemento.get('id')
            id_loc = elemento.get('location_id')
            data = elemento.get('published_date')
            url = elemento.get('url')
            rating = elemento.get('rating')
            recensione = elemento.get('text')

            nuove_recensioni += 1

            # Se la location_id non è già presente nel dizionario, l'aggiungo come chiave con una lista vuota come valore
            if id_loc not in recensioni_per_location:
                recensioni_per_location[id_loc] = {}

            # Verifica se la recensione esiste già per questa location nel dizionario
            if id_rec not in recensioni_per_location[id_loc]:
                # Aggiungo la recensione al dizionario nidificato utilizzando l'id della recensione come chiave
                recensioni_per_location[id_loc][id_rec] = {
                    'rating': rating, 
                    'recensione': recensione, 
                    'data': data, 
                    'url': url
                }
    time.sleep(1)  # Pausa per evitare di superare i limiti dell'API

# Aggiorno l'indice dell'ultimo POI processato
save_last_processed_poi(end_index)

# stampo su schermo il numero di recensioni aggiunte
print(f"Aggiunte {nuove_recensioni} recensioni per i POI selezionati.")

# Scrivo il dizionario di recensioni su un file JSON
with open('recensioni_per_location.json', 'w', encoding='utf-8') as file:
    json.dump(recensioni_per_location, file, ensure_ascii=False, indent=4)


'''
Script per estrarre i POI da Tripadvisor sulla base delle coordinate geografiche
'''


from dotenv import dotenv_values
import os
import requests


# Salvo le coordinate in una lista
coordinate = []

with open('script_python/coordinate.txt', 'r') as file:
    for line in file:
        # Rimuovi spazi bianchi o newline, quindi dividi la riga in due parti
        lat, lon = line.strip().split(',')
        
        # Converti le parti in numeri float e aggiungi come tupla alla lista
        coordinate.append((float(lat), float(lon)))

# Recupero la chiave API
dotenv = dotenv_values()
api_key = dotenv.get("API_KEY")

# Estraggo i POI relativi a poche coordinate alla volta (limiti di richiesta)
# 2700:3000 indica che sto considerando le coordinate dalla 2700 alla 3000 
# (per i limiti imposti dall'API non le ho scarivate tutte in una volta)
poche_coordinate = coordinate[2700:3000]

# print(poche_coordinate)

# Creo un insieme per memorizzare gli ID già presenti nel file.
# Crea un insieme vuoto: Un set in Python è una collezione non ordinata di elementi unici, 
# il che significa che non possono esserci duplicati all'interno di un set.
# Memorizza gli ID: L'insieme id_presenti viene creato per memorizzare gli ID 
# (o qualunque altro tipo di dato che verrà aggiunto successivamente) già presenti. 
# Questo è utile se vuoi tenere traccia degli ID che hai già processato, per evitare di elaborare 
# gli stessi ID più di una volta.
id_presenti = set()

# Se il file esiste, leggo il contenuto attuale del file e memorizzo gli ID
if os.path.exists('poi.txt'):
    with open('poi.txt', 'r', encoding='latin-1') as file:
        for line in file:
            # Divido la riga usando ': ' come separatore solo alla prima occorrenza
            id, resto = line.strip().split(': ', 1)
            # Aggiungo l'ID all'insieme (non ci saranno duplicati nell'insieme)
            id_presenti.add(id)



# Creo la lista vuota di POI da salvare
poi = []

# Mi salvo nella lista l'id e il nome del POI solo se l'id non è già presente
for coordinate in poche_coordinate:
    url = "https://api.content.tripadvisor.com/api/v1/location/nearby_search?latLong=" + str(coordinate[0]) + "%2C" + str(coordinate[1]) + "&key=" + api_key + "&category=attractions&language=it"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
   
    POI = response.json()

    # Estraggo l'id e il nome di ciascun POI e li aggiungo alla lista di POI se l'id non è già presente
    for elemento in POI['data']:
        nome = elemento.get('name')
        id = elemento.get('location_id')
        citta = elemento.get('address_obj')
        if nome is not None and id is not None and id not in id_presenti:
            poi.append((id, nome, citta))
            # Aggiungo l'id all'insieme degli ID presenti
            id_presenti.add(id)

# Apro il file in modalità append
with open('script_python/poi.txt', 'a', encoding='utf-8') as file:
    # Itero sulla lista di POI e scrivo ciascun POI nel file solo se l'id non è già presente
    for id, nome, citta in poi:
        file.write(f"{id}: {nome}, {citta}\n")

print(poi)

# Funzione per rimuovere duplicati dal file
def remove_duplicates(file_path):
    seen = set()
    with open(file_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    with open(file_path, 'w', encoding='utf-8') as outfile:
        for line in lines:
            id = line.split(':')[0]
            if id not in seen:
                seen.add(id)
                outfile.write(line)

# Rimuovi duplicati dal file
remove_duplicates('script_python/poi.txt')
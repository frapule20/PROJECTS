
'''
Script per estrarre i POI da Tripadvisor sulla base delle coordinate geografiche
'''
import os
from dotenv import dotenv_values
import requests
import time

def load_coordinates(filepath):
    coordinate = []
    with open(filepath, 'r') as file:
        for line in file:
            lat, lon = line.strip().split(',')
            coordinate.append((float(lat), float(lon)))
    return coordinate

def get_existing_ids(filepath):
    id_presenti = set()
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                id, _ = line.strip().split(': ', 1)
                id_presenti.add(id)
    return id_presenti

def fetch_poi(coordinate, api_key):
    poi = []
    for lat, lon in coordinate:
        url = f"https://api.content.tripadvisor.com/api/v1/location/nearby_search?latLong={lat},{lon}&key={api_key}&category=attractions&language=it"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Errore nella richiesta API: {response.status_code}")
            continue

        POI = response.json()

        for elemento in POI.get('data', []):
            nome = elemento.get('name')
            id = elemento.get('location_id')
            citta = elemento.get('address_obj', {}).get('city')
            if nome and id:
                poi.append((id, nome, citta))
        
        time.sleep(1)  # Pausa per evitare di superare i limiti dell'API

    return poi

def save_poi(filepath, poi):
    with open(filepath, 'a', encoding='utf-8') as file:
        for id, nome, citta in poi:
            file.write(f"{id}: {nome}, {citta}\n")

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

def main():
    coordinate = load_coordinates('script_python/coordinate.txt')
    dotenv = dotenv_values()
    api_key = dotenv.get("API_KEY")    
    if not api_key:
        print("API_KEY non trovata. Assicurati che sia configurata correttamente.")
        return

    # Fatti tutti
    poche_coordinate = coordinate[3101:]    # Per evitare di superare i limiti dell'API
    id_presenti = get_existing_ids('script_python/poi.txt')
    poi = fetch_poi(poche_coordinate, api_key)

    # Filtra i POI per escludere quelli con ID già presenti
    poi_da_salvare = [p for p in poi if p[0] not in id_presenti]

    save_poi('script_python/poi.txt', poi_da_salvare)
    remove_duplicates('script_python/poi.txt')
    if poi_da_salvare:
        print(f"Aggiunti {len(poi_da_salvare)} nuovi POI")
    else:
        print("Nessun nuovo POI aggiunto")

if __name__ == "__main__":
    main()

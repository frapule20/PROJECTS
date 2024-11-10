'''
Script per l'estrazione dei POI da Tripadvisor 
dato un file .csv con coordinate e nomi dei POI

1. Leggo il file csv
2. Estraggo i POI da Tripadvisor
    2.1. Controllo se il POI è già presente nel database
        2.1.1. se è presente, scarico le relative recensioni e, se non presenti nel database, le aggiungo
        2.1.2. se non è presente, estraggo il POI e le recensioni e le aggiungo al database
3. Salvo i risultati in un file Excel
4. Estraggo le recensioni dei POI
5. Salvo le recensioni in un file Excel
6. Calcolo il sentiment delle recensioni
7. Salvo il sentiment in un file Excel

'''
import json
import os
import time
import pandas as pd
import requests
from sklearn.metrics import classification_report
from bma_ import bma_test
import sentiment_models

def load_file(filepath):
    # Carica il file CSV (se ci arriva un file CSV)
    df = pd.read_csv(filepath)
    return df

# caricamento del database
def load_database(path):
    # Carica il database (excel)
    database = pd.read_excel(path)
    return database

# controllo se il POI è già presente nel database
def exist_poi(database, id_poi):
    for id in database.itertuples():
        if id.id == id_poi:
            return True
    return False

# controllo se esiste la recensione
def exist_review(database, id_review):
    for id in database.itertuples():
        if id.id_recensione == id_review:
            return True
    return False

# estrazione di recensioni
# def extract_reviews(id_poi, api_key)
# def calculate_sentiment

# estrazione dei POI
def extract_poi(df, api_key, headers, database):
    # Dichiarare la lista per tutte le recensioni all'inizio, fuori dal ciclo
    recensioni_totali = []  # Lista per accumulare tutte le recensioni di tutti i POI

    for i in df.itertuples():
        id_poi = i.id_openstreetmap
        nome_poi = i.nome
        lat = i.latitude
        lon = i.longitude

        # Lista per salvare i risultati delle API
        risultati_api = []

        # Se il POI non esiste nel database, estraggo il POI
        if not exist_poi(database, id_poi):
            # Creo l'URL con i parametri
            url = f"https://api.content.tripadvisor.com/api/v1/location/search?key={api_key}&searchQuery={nome_poi}&latLong={lat}%2C{lon}&radius=1&radiusUnit=km&language=it"
            response = requests.get(url, headers=headers)

            # Se la risposta non ha successo, saltiamo il POI
            if response.status_code != 200:
                print(f"Errore nella richiesta API per {nome_poi}: {response.status_code}")
                continue

            # Processiamo la risposta JSON
            data = response.json()

            # Controlliamo se ci sono risultati e salviamo il primo
            if 'data' in data and len(data['data']) > 0:
                primo_risultato = data['data'][0]
            
                risultati_api.append({
                    'id_osm': id_poi,
                    'nome_poi_osm': nome_poi,
                    'latitude_osm': lat,
                    'longitude_osm': lon,
                    'tripadvisor_id': primo_risultato.get('location_id'),
                    'tripadvisor_nome': primo_risultato.get('name'),
                    'tripadvisor_distance_from_osm': float(primo_risultato.get('distance')) * 1.609,
                })
            else:
                print(f"Nessun risultato trovato per {nome_poi}")

            print(f"POI {nome_poi} trovato su Tripadvisor")
            time.sleep(1)  # Pausa di 1 secondo per rispettare i limiti dell'API

            # Converto i risultati in un DataFrame
            df_risultati = pd.DataFrame(risultati_api)

            # Aggiungo i nuovi dati alla fine del DataFrame esistente
            df_completo = pd.concat([pd.read_excel("risultati.xlsx"), df_risultati], ignore_index=True)

            # Salvo il file Excel aggiornato
            df_completo.to_excel("risultati.xlsx", index=False)

            # Recupero le recensioni (con la funzione extract_reviews)
            location_id = primo_risultato.get('location_id')
            url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/reviews?key={api_key}&language=it"
            response = requests.get(url, headers=headers)

            # Se la richiesta ha successo, estraggo le recensioni
            if response.status_code == 200:
                REC = response.json()

            # Estraggo le recensioni di ciascun POI e le aggiungo alla lista delle recensioni
            for elemento in REC.get('data', []):
                id_rec = elemento.get('id')
                rating = elemento.get('rating')
                recensione = elemento.get('text')

                # associo a gs il sentiment sulla base del rating
                if rating >= 4:
                    gs = 'positive' # positivo
                elif rating == 3:
                    gs = 'neutral'
                else:
                    gs = 'negative'

                # normalizzo i valori senza il neutrale
                if rating >= 3:
                    gs_norm = 'positive'
                else:
                    gs_norm = 'negative'
  

                bert_df = sentiment_models.predict_bert(recensione)
                feelit_df = sentiment_models.predict_feelit(recensione)
                multilingual_df = sentiment_models.predict_multilingual(recensione)

                # Calcolo il sentiment con BMA
                #results = bma
                

                # Aggiungi ogni recensione alla lista complessiva
                recensioni_totali.append({
                    'id': id_poi,
                    'POI': nome_poi,
                    'id_recensione': id_rec,
                    'rating': rating,
                    'recensione': recensione,
                    'GS': gs,  
                    'BERT': bert_df['sentiment'].values[0],  
                    'FEEL_IT': feelit_df['sentiment'].values[0],  
                    'MULTILINGUAL': multilingual_df['sentiment'].values[0],
                    'GS_norm': gs_norm, 
                    'pred_BMA': '',  
                    'prob_BMA': '' 
                })

                print(f"Recensione trovata per {nome_poi}")

            time.sleep(1)  # Pausa per evitare di superare i limiti dell'API

    # Dopo aver elaborato tutte le recensioni, converto la lista in un DataFrame
    if recensioni_totali:  # Controlliamo se ci sono recensioni da salvare
        df_recensioni_totali = pd.DataFrame(recensioni_totali)

        # Leggiamo il file Excel esistente se c'è
        try:
            df_completo = pd.read_excel("sentiment_comparison.xlsx")
        except FileNotFoundError:
            # Se il file non esiste, creiamo un DataFrame vuoto
            df_completo = pd.DataFrame()

        # Concateno le nuove recensioni con il database esistente
        df_completo = pd.concat([df_completo, df_recensioni_totali], ignore_index=True)

        # Salvo il DataFrame completo nel file Excel
        df_completo.to_excel("sentiment_comparison.xlsx", index=False)

        print("Tutte le recensioni salvate correttamente!")
    else:
        print("Nessuna recensione trovata.")


    '''
    devo fare il caso in cui l'id del poi è presente nel database, ma non le recensioni
    else:
        if not exist_review(database, id_rec):
            # Recupero le recensioni (con la funzione extract_reviews)
           
    '''

def main():
    # Chiave API e intestazioni
    api_key = "050EA5F13201453ABE972400F314E949"
    headers = {"accept": "application/json"}

    df = load_file("poi_Umbria.csv") # Inserire il path del file CSV
    database = load_database("sentiment_comparison.xlsx") # Inserire il path del database
    extract_poi(df, api_key, headers, database)
    # calcolo il sentiment delle recensioni aggiunte
    # calcolo il sentiment dei singoli POI


if __name__ == "__main__":
    main()


# Script che calcola la media su tutto il sentiment
# tengo il valor medio e l'aggiorno ogni volta
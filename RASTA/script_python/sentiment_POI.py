'''
Script che, dato in input il nome di un POI (o l'ID), restituisce il sentiment delle recensioni.
'''

import json
import pandas as pd

def load_excel(file_path=None):
    if not file_path:
        file_path = input("Inserisci il percorso del file Excel: ")
    return pd.read_excel(file_path)

df = load_excel()


# Visualizzo le prime righe del dataframe per capire la struttura dei dati
# print(df.head())


def calculate_sentiment(df, poi_name_or_id):
    
    # Filtra il dataframe in base all'ID o al nome del POI
    filtered_df = df[(df['id'] == poi_name_or_id) | (df['POI'] == poi_name_or_id)]
    
    if filtered_df.empty:
        print(f"Nessuna recensione trovata per il POI con nome o ID: {poi_name_or_id}")
        exit()  # Interrompe l'esecuzione dello script
    
    # Conta il numero di recensioni positive e negative basate sulla colonna pred_BMA
    positive_count = (filtered_df['pred_BMA'] == 'positive').sum()
    negative_count = (filtered_df['pred_BMA'] == 'negative').sum()
    
    # Calcola il sentiment totale
    if positive_count == negative_count:
        sentiment = "neutro"
    elif (positive_count > negative_count):
        sentiment = "positivo"
    else:
        sentiment = "negativo"
    
    poi_name = filtered_df['POI'].iloc[0]
    poi_id = filtered_df['id'].iloc[0]
    
    return poi_name, poi_id, sentiment, positive_count, negative_count


poi = input("Inserisci il nome o l'id del POI di cui vuoi conoscere il sentiment: ")

# Esempio di utilizzo: Calcoliamo il sentiment per "Palazzo Cesi"
poi_name, poi_id, sentiment, positive_count, negative_count = calculate_sentiment(df, poi)

print("Il sentiment del POI '" + poi_name + "' con id '" + str(poi_id) + "' è: " + sentiment)
print("Recensioni positive: " + str(positive_count))
print("Recensioni negative: " + str(negative_count))


'''
- Devo fare una visualizzazione a schermo tipo interfaccia grafica?
- Per ora non sta calcolando sentiment neutro, dovrei farlo?
'''
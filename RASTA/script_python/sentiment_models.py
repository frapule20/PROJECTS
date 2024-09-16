# Importazione delle librerie necessarie
import pandas as pd
import torch
from tqdm import tqdm
from sklearn.metrics import classification_report
from torch import nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from feel_it import SentimentClassifier
from sklearn.metrics import classification_report


def predict_bert(sentence):
    # Carica il modello e il tokenizer
    tokenizer = AutoTokenizer.from_pretrained("neuraly/bert-base-italian-cased-sentiment")
    bert_model = AutoModelForSequenceClassification.from_pretrained("neuraly/bert-base-italian-cased-sentiment")
    bert_model.eval()  # Imposta il modello in modalità valutazione

    # Tokenizza la frase della recensione usando il tokenizer specificato
    input_ids = tokenizer.encode(sentence, add_special_tokens=True, truncation=True, max_length=512)

    # Crea un tensore, usa .cuda() per trasferire il tensore alla GPU se disponibile
    tensor = torch.tensor(input_ids).long().unsqueeze(0)
    if torch.cuda.is_available():
        tensor = tensor.cuda()
        bert_model.cuda()

    # Chiama il modello BERT e ottiene i logits (uscite grezze prima dell'applicazione della funzione softmax)
    with torch.no_grad():
        logits = bert_model(tensor)
    
    # Rimuove la dimensione fittizia del batch dai logits
    logits = logits.logits.squeeze(0)

    # Applica la funzione softmax per ottenere le probabilità
    proba = nn.functional.softmax(logits, dim=0)

    # Estrae le probabilità per le classi negativo, neutro e positivo
    negative, neutral, positive = proba

    df = pd.DataFrame(columns=['negative', 'neutral', 'positive'])

     # Crea un DataFrame per le probabilità
    df = pd.DataFrame({
        'negative': [proba[0].item()],
        'neutral': [proba[1].item()],
        'positive': [proba[2].item()],
    })

    df['sentiment'] = ['negative', 'neutral', 'positive'][proba.argmax().item()]

    return df


def predict_feelit(sentence):
    # Carica il tokenizer e il modello
    tokenizer = AutoTokenizer.from_pretrained("MilaNLProc/feel-it-italian-sentiment")
    feelit_model = AutoModelForSequenceClassification.from_pretrained("MilaNLProc/feel-it-italian-sentiment")
    feelit_model.eval()

    # Definisci il dispositivo (usa la GPU se disponibile, altrimenti CPU)
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    feelit_model.to(device)

    # Tokenizza la frase
    encodings = tokenizer(sentence, truncation=True, padding=True, max_length=500, return_tensors='pt')
    input_ids = encodings['input_ids'].to(device)
    attention_mask = encodings['attention_mask'].to(device)

    # Fai una previsione senza calcolare i gradienti
    with torch.no_grad():
        outputs = feelit_model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits

    # Applica softmax per ottenere le probabilità
    probabilities = F.softmax(logits, dim=-1).cpu().numpy()

    # Estrai le probabilità dalla lista
    prob = probabilities[0]  # poiché stiamo processando solo una frase

    # Crea il DataFrame con le probabilità
    df = pd.DataFrame({
        'negative': [prob[0]],
        'positive': [prob[1]],
        'sentiment': ['positive' if prob[1] > prob[0] else 'negative']
    })

    return df


def predict_multilingual(sentence):
    # Carica il modello e il tokenizer
    # Load model directly from the Hugging Face Hub
    tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    multilingual_model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    
    input_ids = tokenizer.encode(sentence, add_special_tokens=True, truncation=True, max_length=512)

    # Create tensor, use .cuda() to transfer the tensor to GPU
    tensor = torch.tensor(input_ids).long()
    # Fake batch dimension
    tensor = tensor.unsqueeze(0)

    # Call the model and get the logits
    logits = multilingual_model(tensor)
    # Remove the fake batch dimension
    logits = logits.logits.squeeze(0)

    # The model was trained with a Log Likelyhood + Softmax combined loss, hence to extract probabilities we need a softmax on top of the logits tensor
    proba = nn.functional.softmax(logits, dim=0)

    # Aggiungi le probabilità alle colonne appropriate
    proba = proba.to("cpu")

    df = pd.DataFrame({
        '1': [proba[0].item()],
        '2': [proba[1].item()],
        '3': [proba[2].item()],
        '4': [proba[3].item()],
        '5': [proba[4].item()]
    })


    # Calcola il sentimento prevalente
    df['MULTILINGUAL'] = df[['1', '2', '3', '4', '5']].idxmax(axis=1)
    df.drop(columns=['1', '2', '3', '4', '5'], inplace=True)
    # Tentare di convertire i valori della colonna 'MULTILINGUAL' in numerici, ignorando gli errori
    df['sentiment_pred_numeric'] = pd.to_numeric(df['MULTILINGUAL'], errors='coerce')

    # Applicare le trasformazioni solo ai valori numerici
    df.loc[df['sentiment_pred_numeric'] >= 4, 'MULTILINGUAL'] = 'positive'
    df.loc[df['sentiment_pred_numeric'] <= 2, 'MULTILINGUAL'] = 'negative'
    df.loc[df['sentiment_pred_numeric'] == 3, 'MULTILINGUAL'] = 'neutral'
    # Rimuovere la colonna temporanea utilizzata per la conversione
    df.drop(columns=['sentiment_pred_numeric'], inplace=True)
        
    return df

sentence = 'Il cibo era delizioso e il servizio era eccellente.'
bert_df = predict_bert(sentence)
feelit_df = predict_feelit(sentence)
multilingual_df = predict_multilingual(sentence)

print("BERT Model Prediction:" + str(bert_df))
print("Feel-it Model Prediction:" + str(feelit_df))
print("Multilingual Model Prediction:" + str(multilingual_df))
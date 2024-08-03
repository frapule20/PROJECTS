# Progetto RASTA

## Introduzione
Questa cartella contiene il codice sorgente e i dati relativi al progetto RASTA, in particolar modo della fase di sentiment, estrazione di topic e REST. 

## Struttura della Cartella
RASTA/
│
├── delivery/
│   ├── Topic Modeling.docx
│   └── REST.docx
│
├── REST/
│
├── sentiment/
│   ├── results
│   │   ├── BERT.xlsx
│   │   ├── BERT_classification_report.xlsx
│   │   ├── BERT_value_counts.csv
│   │   ├── FEEL_IT.xlsx
│   │   ├── FEEL_IT_classification_report.xlsx
│   │   ├── FEEL_IT_results.csv
│   │   ├── MULTILINGUAL.xlsx
│   │   ├── MULTILINGUAL_classification_report.xlsx
│   │   ├── MULTILINGUAL_results.csv
│   │   ├── rec_neg_to_pos.xlsx
│   │   ├── rec_pos_to_neg.xlsx
│   │   └── sentiment_comparison.xlsx
│   └── script
│       ├── bma_.py
│       └── sentiment.ipynb
└── topic_extraction.txt


## Descrizione dei File
- `delivery/Topic Modeling.docx`: Il delivery relativo all'estrazione di topic.


- `sentiment/results/BERT.xlsx`: Contiene i risultati del modello BERT, normalizzati senza il neutrale e non
- `sentiment/results/BERT_classification_report.xlsx`: Contiene il report della classificazione del modello BERT
- `sentiment/results/BERT_value_counts.csv`: Contiene i valori della classificazione senza normalizzazione
- `sentiment/results/FEEL_IT.xlsx`: Contiene i risultati del modello FEEL_IT 
- `sentiment/results/FEEL_IT_classification_report.xlsx`: Contiene il report della classificazione del modello FEEL_IT
- `sentiment/results/FEEL_IT_results.csv`: Contiene i valori della classificazione  
- `sentiment/results/MULTILINGUAL.xlsx`: Contiene i risultati del modello MULTILINGUAL, normalizzati senza il neutrale e non 
- `sentiment/results/MULTILINGUAL_classification_report.xlsx`: Contiene il report della classificazione del modello MULTILINGUAL
- `sentiment/results/MULTILINGUAL_results.csv`: Contiene i valori della classificazione senza normalizzazione 
- `sentiment/results/rec_neg_to_pos.xlsx`: Contiene tutte le recensioni che secondo le stelle lasciate dagli utenti erano negative, ma che sono state classificate come positive, con relative distribuzioni
- `sentiment/results/rec_pos_to_neg.xlsx`: Contiene tutte le recensioni che secondo le stelle lasciate dagli utenti erano positive, ma che sono state classificate come negative, con relative distribuzioni 
- `sentiment/results/sentiment_comparison.xlsx`: Contiene i risultati di tutti i modelli

- `sentiment/script/bma_.py`: Contiene lo script della funzione di BMA
- `sentiment/script/sentiment.ipynb`: Contiene il codice dell'analisi del sentiment e della BMA



- `readme.txt`: Questo file di documentazione.





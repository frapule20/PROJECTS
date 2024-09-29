'''
Servizio che utilizza la Latent Dirichlet Allocation (LDA) per determinare la probabilità 
che un POI (Point of Interest) appartenga a ciascun TOI (Topic of Interest)

'''
from matplotlib import pyplot as plt
from ttkbootstrap import Style, ttk  # Importa ttk da ttkbootstrap
import tkinter as tk
from tkinter import Image, scrolledtext
from PIL import Image, ImageTk  # Per gestire immagini più grandi
from tkinter.ttk import Style
import numpy as np
from octis.models.LDA import LDA
from octis.dataset.dataset import Dataset
from gensim.corpora.dictionary import Dictionary
import spacy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.font as tkFont
from nltk.corpus import stopwords
import string

# Carica il vocabolario corretto dal file
def load_vocabulary(vocabulary_path):
    with open(vocabulary_path, 'r', encoding='utf-8') as f:
        vocabulary = [line.strip() for line in f]  # Rimuove i newline
    return vocabulary

# Crea una mappatura id2word per Gensim
vocabulary = load_vocabulary(r'C:\Users\franc\Desktop\PROJECTS\PROJECTS\RASTA\datasetNostriPOI\dataset_LDA_Zipf\vocabulary.txt')
id2word = Dictionary([vocabulary])

# Carica il dataset preprocessato
dataset_save = r'C:\Users\franc\Desktop\PROJECTS\PROJECTS\RASTA\datasetNostriPOI\dataset_LDA_Zipf'
dataset = Dataset()
dataset.load_custom_dataset_from_folder(dataset_save)

# Addestra il modello LDA
model = LDA(num_topics=12, random_state=42)
model_output = model.train_model(dataset)

# Carica il modello per l'italiano
nlp = spacy.load("it_core_news_sm")

# Funzione per preprocessare il testo
def preprocess_text(text):
    doc = nlp(text.lower())  # Converte tutto in minuscolo
    stop_words_lista = list(set(stopwords.words('italian')))
    stop_words_lista += ["due", "altri", "it", "m", "d", "s", 'essere', 'avere', 'trovare', 
                         'dopo', 'fino', 'altro', 'via', 'fare', 'chiesa', 'san', 'secolo',
                         'comune', 'parte', 'città', 'via', 'venire', 'monte', 'interno', 
                         'territorio', 'secondo', 'poi', 'collegamento', 'url']

    tokens = []
    for token in doc:
        lemma = token.lemma_
        if lemma not in stop_words_lista and lemma not in string.punctuation:
            if lemma in ["santa", "santo", "sant'", "santi"]:
                lemma = "san"
            tokens.append(lemma)
    
    # Filtra i token che non fanno parte del vocabolario
    tokens = [token for token in tokens if token in vocabulary]
    
    # Verifica se tutti i token sono presenti nel dizionario id2word
    bow = id2word.doc2bow(tokens)
    
    # Filtra token fuori vocabolario
    bow = [(token_id, freq) for token_id, freq in bow if token_id < len(id2word)]
    
    return bow


# Funzione per predire la distribuzione di probabilità di un nuovo POI
def predict_poi_description(lda_model, preprocessed_poi):
    document_topics = lda_model.trained_model.get_document_topics(preprocessed_poi, minimum_probability=0)

    topic_distribution = np.zeros(lda_model.hyperparameters['num_topics'])

    for topic_num, prob in document_topics:
        topic_distribution[topic_num] = prob

    return topic_distribution

# Variabile globale per la distribuzione dei topic
topic_distribution_global = None

# Genera automaticamente le parole associate a ciascun topic dal modello LDA
topic_words = []
for i, topic in enumerate(model_output['topics']):
    words = " ".join(topic)
    topic_words.append(f"Topic {i + 1}: {words}")

# Funzione per calcolare la distribuzione di probabilità
def calcola_distribuzione():
    global topic_distribution_global  # Usa la variabile globale
    input_text = text_input.get("1.0", tk.END).strip()  # Prendi il testo inserito
    preprocessed_poi = preprocess_text(input_text)  # Preprocessa il testo
    topic_distribution_global = predict_poi_description(model, preprocessed_poi)  # Calcola la distribuzione

    # Mostra la distribuzione nei risultati
    result_text.delete(1.0, tk.END)
    for i, prob in enumerate(topic_distribution_global):
        result_text.insert(tk.END, f"Topic {i}: {prob:.4f}\n")

# Funzione per mostrare il grafico a barre
def mostra_grafico():
    if topic_distribution_global is not None:
        fig, ax = plt.subplots()
        ax.bar(range(len(topic_distribution_global)), topic_distribution_global, color='skyblue')
        ax.set_xlabel("Topic")
        ax.set_ylabel("Probabilità")
        ax.set_title("Distribuzione di probabilità")
        
        # Aggiungi il grafico alla finestra Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)  # Usa la finestra del grafico come master
        canvas.draw()
        canvas.get_tk_widget().pack()  # Aggiungi il widget del canvas

# Creazione dell'interfaccia grafica con Tkinter
root = tk.Tk()
root.title("Distribuzione LDA per POI")

root.iconbitmap('icon.ico') 

# Crea un canvas e una scrollbar per la finestra principale
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# Configura il canvas
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Aggiungi la scrollbar al canvas
canvas.configure(yscrollcommand=scrollbar.set)

# Imposta la dimensione del canvas
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Visualizzazione dei topic
topics_frame = tk.Frame(scrollable_frame)
topics_frame.pack(pady=10)

tk.Label(topics_frame, text="Topics (parole associate):", font=("Arial", 12, "bold")).pack(anchor='center')  # Allinea a sinistra

for i, topic in enumerate(topic_words):
    tk.Label(topics_frame, text=f"Topic {i + 1}: {topic}", font=("Arial", 10), anchor='w').pack(fill='x')

# Barra di input per la descrizione del POI
input_frame = tk.Frame(scrollable_frame)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Inserisci la descrizione del POI:", font=("Arial", 12)).pack()

text_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=60, height=5)
text_input.pack(pady=5)

# Pulsante per calcolare la distribuzione
calc_button = tk.Button(input_frame, text="Calcola Distribuzione", command=calcola_distribuzione, font=("Arial", 12), bg='lightblue')
calc_button.pack(pady=5)

# Pulsante per mostrare il grafico
show_graph_button = tk.Button(input_frame, text="Mostra Grafico", command=mostra_grafico, font=("Arial", 12), bg='lightgreen')
show_graph_button.pack(pady=5)

# Area di output per mostrare i risultati
result_frame = tk.Frame(scrollable_frame)
result_frame.pack(pady=10)

tk.Label(result_frame, text="Risultati:", font=("Arial", 12, "bold")).pack()

result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=60, height=10)
result_text.pack(pady=5)

# Frame per il grafico
graph_frame = tk.Frame(scrollable_frame)
graph_frame.pack(pady=10)

# Avvia l'interfaccia grafica
root.mainloop()



'''
text1 = "Sant'Agata dei Goti è un comune italiano di 11.000 abitanti della provincia di Benevento."
text2 = "Il Duomo di Milano è una chiesa monumentale che si trova nel cuore della città di Milano."
text3 = "Il Colosseo è un anfiteatro di epoca romana situato nel centro della città di Roma."

'''
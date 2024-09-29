'''
Servizio che utilizza la Latent Dirichlet Allocation (LDA) per determinare la probabilità 
che un POI (Point of Interest) appartenga a ciascun TOI (Topic of Interest)

'''
import numpy as np
from octis.models.LDA import LDA
from octis.dataset.dataset import Dataset
from gensim.corpora.dictionary import Dictionary
import spacy
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

print("TOPICS:")
for t in model_output['topics']:
  print(" ".join(t))

# Carica il modello per l'italiano
nlp = spacy.load("it_core_news_sm")

# Funzione per preprocessare il testo
def preprocess_text(text):
    print(type(text))
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
    
    # Trasforma in formato id2word per predizione con LDA
    bow = id2word.doc2bow(tokens)
    return bow

# Funzione per predire la distribuzione di probabilità di un nuovo POI
# Funzione per predire la distribuzione di probabilità di un nuovo POI
def predict_poi_description(lda_model, preprocessed_poi):
    # Ottieni la distribuzione di topic per il nuovo POI
    document_topics = lda_model.trained_model.get_document_topics(preprocessed_poi, minimum_probability=0)

    # Crea un array vuoto per la distribuzione di probabilità
    topic_distribution = np.zeros(lda_model.hyperparameters['num_topics'])

    for topic_num, prob in document_topics:
        topic_distribution[topic_num] = prob

    return topic_distribution

# esempio:
text = "Sant'Agata dei Goti è un comune italiano di 11.000 abitanti della provincia di Benevento."
text2 = "Il Duomo di Milano è una chiesa monumentale che si trova nel cuore della città di Milano."
text3 = "Il Colosseo è un anfiteatro di epoca romana situato nel centro della città di Roma."

preprocessed_poi = preprocess_text(text)
preprocessed_poi2 = preprocess_text(text2)
preprocessed_poi3 = preprocess_text(text3)

# Calcolare la distribuzione di probabilità
topic_distribution = predict_poi_description(model, preprocessed_poi)
topic_distribution2 = predict_poi_description(model, preprocessed_poi2)
topic_distribution3 = predict_poi_description(model, preprocessed_poi3)

# Visualizzare i risultati
for i, prob in enumerate(topic_distribution):
    print(f"Topic {i}: {prob:.4f}")

for i, prob in enumerate(topic_distribution2):
    print(f"Topic {i}: {prob:.4f}") 

for i, prob in enumerate(topic_distribution3):
    print(f"Topic {i}: {prob:.4f}")
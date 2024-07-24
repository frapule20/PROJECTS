'''
Invece di calcolare le probabilità per ogni token, calcoliamo le probabilità per 
l'intera frase utilizzando le probabilità globali fornite.
Utilizza le probabilità delle classi dai diversi modelli e le pondera in base alla 
loro affidabilità (F1-score) per ottenere una predizione finale per ciascuna frase.

Alla fine, la funzione bma_test restituisce una lista di etichette predette per ciascuna 
frase nel dataset. Queste etichette rappresentano la classe più probabile per ogni frase, 
basata sulla combinazione delle probabilità fornite dai modelli e delle loro affidalibilità.
'''

from tqdm import tqdm

def bma_test(probs, reliabilities, model_list, classes, source_tokens):
    sentence_preds = []

    num_classes = len(classes[model_list[0]])  # Numero di classi, assunto lo stesso per tutti i modelli

    for i in tqdm(range(len(source_tokens))):
        bma_probs = [0] * num_classes

        for p in range(num_classes):
            marginal_p = 0

            for model in model_list:
                try:
                    # Recupera la probabilità per la classe p della frase i
                    prob = probs[model][i][p]
                    # Recupera l'affidabilità per la classe p
                    reliability = reliabilities[model][classes[model][p]]["f1-score"]
                    # Aggiorna la probabilità marginale
                    marginal_p += prob * reliability

                except (IndexError, KeyError) as e:
                    print(f"Error: {e}")
                    print(f"Model: {model}, i: {i}, p: {p}")
                    raise

            # Assegna la probabilità marginale
            bma_probs[p] = marginal_p

        # Normalizza le probabilità
        total_prob = sum(bma_probs)
        norm_probs = [prob / total_prob for prob in bma_probs] if total_prob > 0 else [0] * num_classes

        # Trova la classe con la probabilità più alta
        max_prob = max(norm_probs)
        indice_max = norm_probs.index(max_prob)
        sentence_preds.append(classes[model_list[0]][indice_max])

    return sentence_preds

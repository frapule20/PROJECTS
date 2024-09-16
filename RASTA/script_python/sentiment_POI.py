'''
Script che, dato in input il nome di un POI (o l'ID), restituisce il sentiment delle recensioni.
'''

import tkinter as tk
from tkinter import Image, ttk, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk  # Per gestire immagini più grandi
import pandas as pd
import json

def load_excel(file_path=None):
    if not file_path:
        file_path = input("Inserisci il percorso del file Excel: ")
    return pd.read_excel(file_path)


# df = load_excel()


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

    # Converto i valori string della colonna prob_BMA in valori float
    positive = []
    negative = []

    for prob in filtered_df['prob_BMA']:
        # print(prob)
        virgola = prob.find(',')
        # print(virgola)
        #print(type(virgola))
        n = prob[1:virgola]
        p = prob[virgola+1:len(prob)-1]
        pos = float(p)
        neg = float(n)
        positive.append(pos)
        negative.append(neg)

    # print(positive) 
    # print(negative)

    # Calcola la distribuzione delle recensioni
    distribution = [sum(positive) / len(positive), sum(negative) / len(negative)]
    
    # Calcola il sentiment totale
    if positive_count == negative_count:
        sentiment = "neutro"
    elif (positive_count > negative_count):
        sentiment = "positivo"
    else:
        sentiment = "negativo"
    
    poi_name = filtered_df['POI'].iloc[0]
    poi_id = filtered_df['id'].iloc[0]
    
    return poi_name, poi_id, sentiment, positive_count, negative_count, distribution

# Funzione per aprire il dialogo di selezione file
def browse_file():
    filename = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        title="Seleziona un file Excel"
    )
    if filename:
        excel_path.set(filename)
        
# Funzione per gestire il pulsante di ricerca
def on_submit():
    poi_input = poi_entry.get()
    if not poi_input:
        messagebox.showerror("Errore", "Inserisci un nome o ID del POI.")
        return
    
    try:
        df = pd.read_excel(excel_path.get())
        poi_name, poi_id, sentiment, positive_count, negative_count, distribution = calculate_sentiment(df, poi_input)
        
        if poi_name is None:
            messagebox.showinfo("Informazione", f"Nessuna recensione trovata per il POI con nome o ID: {poi_input}")
        else:
            result = (f"Il sentiment del POI '{poi_name}' con id '{poi_id}' è: {sentiment}\n"
                      f"Recensioni positive: {positive_count}\n"
                      f"Recensioni negative: {negative_count}\n"
                      f"Distribuzione: {distribution}")
            messagebox.showinfo("Risultato", result)
    
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {e}")

# Funzione per centrare la finestra
def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    root.geometry(f'{width}x{height}+{position_right}+{position_top}')

# Creazione della finestra grafica
root = tk.Tk()
root.title("Sentiment delle Recensioni di un dato POI")

# Dimensioni fisse per la finestra
window_width = 400
window_height = 390
center_window(root, window_width, window_height)  # Centrare la finestra
root.resizable(False, False)  # Disabilita il ridimensionamento

# Aggiungi un'icona alla finestra (se disponibile)
# root.iconbitmap('icon.ico')  

# Definire il tema ttk
style = ttk.Style()
style.theme_use("clam")  # Altri temi disponibili: 'alt', 'default', 'clam'

# Colori personalizzati
root.configure(bg="#f0f0f0")  # Colore di sfondo della finestra

# Creare un frame per allineare i widget centralmente
main_frame = ttk.Frame(root, padding="20 20 20 20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Label e campo di input
poi_label = ttk.Label(main_frame, text="Inserisci il nome o l'ID del POI:", font=("Helvetica", 12))
poi_label.grid(row=3, column=0, pady=10)

poi_entry = ttk.Entry(main_frame, width=40, font=("Helvetica", 11))
poi_entry.grid(row=4, column=0, pady=10)

# Label e campo di input per il percorso del file Excel
excel_label = ttk.Label(main_frame, text="Seleziona o inserisci il file Excel:", font=("Helvetica", 12))
excel_label.grid(row=1, column=0, pady=10)

# Campo di input
excel_path = tk.StringVar()
excel_entry = ttk.Entry(main_frame, textvariable=excel_path, width=28, font=("Helvetica", 11))
excel_entry.grid(row=2, column=0, pady=0, padx=(0, 5), sticky=tk.W)  # Padding destro per distanziare il pulsante

# Pulsante per aprire il dialogo di selezione file
browse_button = ttk.Button(main_frame, text="Sfoglia", command=browse_file)
browse_button.grid(row=2, column=0, pady=0, padx=(245, 0), sticky=tk.E)  # Padding sinistro per avvicinare al campo di input

# Configura la larghezza delle colonne
main_frame.grid_columnconfigure(0, weight=1)


# Pulsante per inviare il form
submit_button = ttk.Button(main_frame, text="Calcola Sentiment", command=on_submit, style="Accent.TButton")
submit_button.grid(row=5, column=0, pady=20)

# Aggiungere un padding attorno ai widget per evitare che siano troppo attaccati
for widget in main_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)

# Aggiungi un'icona alla finestra 
root.iconbitmap('icon.ico') 

# Creare un frame per le immagini
image_frame = ttk.Frame(main_frame)
image_frame.grid(row=0, column=0, pady=10, padx=10)

# Caricare e visualizzare la prima immagine
try:
    img1 = Image.open("large_icon.png")  # Aggiungi il tuo file .png qui
    img1 = img1.resize((100, 100), Image.ANTIALIAS)  # Ridimensiona l'immagine
    photo1 = ImageTk.PhotoImage(img1)
    img_label1 = tk.Label(image_frame, image=photo1, background="#f0f0f0")
    img_label1.image = photo1  # Mantieni un riferimento all'immagine
    img_label1.grid(row=0, column=0, padx=10)
except Exception as e:
    print("Errore nel caricamento dell'immagine large_icon.png:", e)

# Caricare e visualizzare la seconda immagine
try:
    img2 = Image.open("RASTA.png")  # Aggiungi il tuo file .png qui
    img2 = img2.resize((140, 100), Image.ANTIALIAS)  # Ridimensiona l'immagine
    photo2 = ImageTk.PhotoImage(img2)
    img_label2 = tk.Label(image_frame, image=photo2, background="#f0f0f0")
    img_label2.image = photo2  # Mantieni un riferimento all'immagine
    img_label2.grid(row=0, column=1, padx=10)
except Exception as e:
    print("Errore nel caricamento dell'immagine RASTA.png:", e)
    
# Definire uno stile personalizzato per i bottoni
style.configure("Accent.TButton", foreground="white", background="#9B2D30", font=("Helvetica", 11))
style.map("Accent.TButton", background=[('active', 'white')], foreground=[('active', '#9B2D30')])

# Avvio della finestra Tkinter
root.mainloop()
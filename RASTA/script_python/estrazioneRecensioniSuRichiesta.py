import json
import os
from tkinter import Image, messagebox
import requests
from dotenv import dotenv_values
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  # Per gestire immagini più grandi

#from sentiment_models import predict_feelit, predict_multilingual, predict_bert


# Carica la chiave API da .env
dotenv = dotenv_values()
api_key = dotenv.get("API_KEY")


# Funzione per cercare il POI nel database per ID o nome
def trova_poi(poi_input, poi_dict):
    if poi_input in poi_dict:  # Cerca per ID
        return poi_input
    else:  # Cerca per nome
        for poi_id, nome in poi_dict.items():
            if nome.lower() == poi_input.lower():
                return poi_id
    return None

# Funzione per verificare se ci sono nuove recensioni da aggiungere
def aggiungi_recensioni(poi_id, recensioni_per_location, api_key):
    url = f"https://api.content.tripadvisor.com/api/v1/location/{poi_id}/reviews?key={api_key}&language=it"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    REC = response.json()

    nuove_recensioni = 0
    if 'data' in REC:
        for elemento in REC['data']:
            id_rec = elemento.get('id')
            id_loc = elemento.get('location_id')
            data = elemento.get('published_date')
            url = elemento.get('url')
            rating = elemento.get('rating')
            recensione = elemento.get('text')

            if id_loc not in recensioni_per_location:
                recensioni_per_location[id_loc] = {}

            if id_rec not in recensioni_per_location[id_loc]:
                recensioni_per_location[id_loc][id_rec] = {
                    'rating': rating, 'recensione': recensione, 'data': data, 'url': url
                }
                nuove_recensioni += 1

    return nuove_recensioni

# Funzione principale
def main(poi_input):
    # Carica il dizionario dei POI (id:nome)
    with open('poi.json', 'r', encoding='utf-8') as f:
        poi_dict = json.load(f)
    
    # Carica il file delle recensioni esistenti
    recensioni_path = 'recensioni_per_location.json'
    if os.path.exists(recensioni_path):
        with open(recensioni_path, 'r', encoding='utf-8') as f:
            recensioni_per_location = json.load(f)
    else:
        recensioni_per_location = {}

    # Cerca il POI nel database per ID o nome
    poi_id = trova_poi(poi_input, poi_dict)

    if poi_id is None:
        messagebox.showerror("Errore", "Non esiste alcun POI con quel nome/id.")
        return
    
    # Verifica se ci sono recensioni già presenti nel database per questo POI
    if poi_id in recensioni_per_location:
        messagebox.showinfo("Informazione", "Le recensioni relative a quel POI sono già presenti nel database.")
        return
    
    # Recupera le recensioni dall'API
    nuove_recensioni = aggiungi_recensioni(poi_id, recensioni_per_location, api_key)

    if nuove_recensioni > 0:
        # Salva il file aggiornato con le nuove recensioni
        with open(recensioni_path, 'w', encoding='utf-8') as f:
            json.dump(recensioni_per_location, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Successo", f"Sono state aggiunte {nuove_recensioni} nuove recensioni per il POI {poi_dict[poi_id]}.")
    else:
        messagebox.showinfo("Informazione", f"Non ci sono nuove recensioni per il POI {poi_dict[poi_id]}.")

# Funzione per gestire il pulsante
def on_submit():
    poi_input = poi_entry.get()
    main(poi_input)

# Funzione per centrare la finestra
def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    root.geometry(f'{width}x{height}+{position_right}+{position_top}')

# Creazione della finestra grafica
root = tk.Tk()
root.title("Recensioni POI")

# Dimensioni fisse per la finestra
window_width = 400
window_height = 250
center_window(root, window_width, window_height)  # Centrare la finestra
root.resizable(False, False)  # Disabilita il ridimensionamento

# Aggiungi un'icona alla finestra 
root.iconbitmap('icon.ico')  

# Definire il tema ttk
style = ttk.Style()
style.theme_use("clam")  # Altri temi disponibili: 'alt', 'default', 'clam'

# Colori personalizzati
root.configure(bg="#f0f0f0")  # Colore di sfondo della finestra

# Creare un frame per allineare i widget centralmente
main_frame = ttk.Frame(root, padding="20 20 20 20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
second_frame = ttk.Frame(root, padding="20 90 20 20")

# Caricare un'immagine più grande da mostrare in alto
try:
    img = Image.open("large_icon.png")  # Aggiungi il tuo file .png qui
    img = img.resize((100, 100), Image.ANTIALIAS)  # Ridimensiona l'immagine
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(main_frame, image=photo, background="#f0f0f0")
    img_label.grid(row=0, column=0, pady=0)
except Exception as e:
    print("Errore nel caricamento dell'immagine:", e)


# Label e campo di input
poi_label = ttk.Label(second_frame, text="Inserisci il nome o l'ID del POI:", font=("Helvetica", 12))
poi_label.grid(row=0, column=0, pady=10)

poi_entry = ttk.Entry(main_frame, width=40, font=("Helvetica", 11))
poi_entry.grid(row=1, column=0, pady=10)

# Pulsante per inviare il form
submit_button = ttk.Button(main_frame, text="Cerca Recensioni", command=on_submit, style="Accent.TButton")
submit_button.grid(row=2, column=0, pady=20)

# Aggiungere un padding attorno ai widget per evitare che siano troppo attaccati
for widget in main_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)

# Definire uno stile personalizzato per i bottoni
style.configure("Accent.TButton", foreground="white", background="#9B2D30", font=("Helvetica", 11))
style.map("Accent.TButton", background=[('active', 'white')], foreground=[('active', '#9B2D30')])


# Avvio della finestra Tkinter
root.mainloop()

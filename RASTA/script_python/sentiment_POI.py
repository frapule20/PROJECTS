'''
Script che, dato in input il nome di un POI (o l'ID), restituisce il sentiment delle recensioni.
'''
import tkinter as tk
from ttkbootstrap import Style, ttk  # Importa ttk da ttkbootstrap
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk  # Per gestire immagini più grandi
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.font as tkFont



def load_excel(file_path=None):
    if not file_path:
        file_path = input("Inserisci il percorso del file Excel: ")
    return pd.read_excel(file_path)

def check_excel_format(df):
    required_columns = {'id', 'POI', 'rating', 'recensione'}
    if not required_columns.issubset(df.columns):
        raise ValueError("Il file Excel selezionato non rispetta il formato richiesto")

def populate_poi_dropdown(df):
    poi_names = df['POI'].unique().tolist()
    poi_dropdown['values'] = poi_names
    if poi_names:
        poi_dropdown.current(0)

def calculate_sentiment(df, poi_name_or_id):
    filtered_df = df[(df['id'] == poi_name_or_id) | (df['POI'] == poi_name_or_id)]
    
    if filtered_df.empty:
        print(f"Nessuna recensione trovata per il POI con nome o ID: {poi_name_or_id}")
        exit()
    
    positive_count = (filtered_df['pred_BMA'] == 'positive').sum()
    negative_count = (filtered_df['pred_BMA'] == 'negative').sum()

    positive = []
    negative = []

    for prob in filtered_df['prob_BMA']:
        virgola = prob.find(',')
        n = prob[1:virgola]
        p = prob[virgola+1:len(prob)-1]
        pos = float(p)
        neg = float(n)
        positive.append(pos)
        negative.append(neg)

    distribution = [sum(positive) / len(positive), sum(negative) / len(negative)]
    
    sentiment = "neutro" if positive_count == negative_count else "positivo" if positive_count > negative_count else "negativo"
    
    poi_name = filtered_df['POI'].iloc[0]
    poi_id = filtered_df['id'].iloc[0]
    
    return poi_name, poi_id, sentiment, positive_count, negative_count, distribution

def browse_file():
    filename = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        title="Seleziona un file Excel"
    )
    if filename:
        try:
            df = load_excel(filename)
            check_excel_format(df)
            excel_path.set(filename)
            populate_poi_dropdown(df)
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore: {e}")

def on_submit():
    poi_input = poi_dropdown.get()
    if not poi_input:
        messagebox.showerror("Errore", "Seleziona un POI dal menù a tendina.")
        return
    
    try:
        df = pd.read_excel(excel_path.get())
        poi_name, poi_id, sentiment, positive_count, negative_count, distribution = calculate_sentiment(df, poi_input)
        
        # Crea una nuova finestra per i risultati
        result_window = tk.Toplevel(root)
        result_window.title("Risultati del Sentiment")
        result_window.iconbitmap('icon.ico') 

        # Dimensioni della finestra di risultato
        result_window_width = 500
        result_window_height = 630
    
        # Ottieni le dimensioni dello schermo
        screen_width = result_window.winfo_screenwidth()
        screen_height = result_window.winfo_screenheight()

        # Calcola la posizione per centrare la finestra
        position_top = int(screen_height / 2 - result_window_height / 2)
        position_right = int(screen_width / 2 - result_window_width / 2)

        # Imposta la geometria della finestra con la nuova posizione
        result_window.geometry(f'{result_window_width}x{result_window_height}+{position_right}+{position_top}')
        
        # Crea un widget Text
        text_widget = tk.Text(result_window, wrap=tk.WORD, height=13, width=50)
        text_widget.pack(pady=10)

        # Definisci un font in grassetto
        bold_font = tkFont.Font(weight="bold", size=12)
        normal_font = tkFont.Font(size=12)

        # Inserisci i risultati nel widget Text
        text_widget.insert(tk.END, f"Il sentiment del POI ", 'normal')
        text_widget.insert(tk.END, poi_name, 'bold')
        text_widget.insert(tk.END, ' con id ', 'normal')
        text_widget.insert(tk.END, poi_id, 'bold')
        text_widget.insert(tk.END, ' è: ', 'normal')
        text_widget.insert(tk.END, sentiment + '\n' + '\n', 'bold')

        text_widget.insert(tk.END, f"Recensioni positive: ", 'bold')
        text_widget.insert(tk.END, str(positive_count) + '\n', 'normal')
        text_widget.insert(tk.END, f"Recensioni negative: ", 'bold')
        text_widget.insert(tk.END, str(negative_count), 'normal')

        text_widget.insert(tk.END, '\n\nDistribuzione: ' + '\n', 'bold')
        text_widget.insert(tk.END, f"Positivo-> {distribution[0]}", 'normal')
        text_widget.insert(tk.END, f"\nNegativo-> {distribution[1]}", 'normal')

        # Applica lo stile al testo in grassetto
        text_widget.tag_config('bold', font=bold_font)
        text_widget.tag_config('normal', font=normal_font)

        # Disabilita la modifica del testo
        text_widget.config(state=tk.DISABLED)

        # Crea il grafico a torta
        labels = ['Positivo', 'Negativo']

        pos = distribution[0]
        neg = distribution[1]
        sizes = [pos, neg]
        colors = ['#66c2a5', '#fc8d62']
        explode = (0.1, 0)  # Esplodi solo il primo pezzo

        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
               autopct='%1.1f%%', shadow=True, startangle=90)
        ax.axis('equal')  # Garantisce che il grafico sia un cerchio

        # Aggiungi il grafico alla finestra dei risultati
        canvas = FigureCanvasTkAgg(fig, master=result_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {e}")


    
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {e}")

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    root.geometry(f'{width}x{height}+{position_right}+{position_top}')


def plot_sentiment_distribution(positive_count, negative_count):
    plot_window = tk.Toplevel(root)
    plot_window.title("Distribuzione del Sentiment")

    labels = ['Positivo', 'Negativo']
    sizes = [positive_count, negative_count]
    colors = ['#66c2a5', '#fc8d62']
    explode = (0.1, 0)

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Usare ttkbootstrap per uno stile moderno
style = Style(theme="litera")  # Altri temi: 'darkly', 'cosmo', 'litera', etc.
root = style.master
root.title("Sentiment delle Recensioni di un POI")

window_width = 390
window_height = 440
center_window(root, window_width, window_height)
root.resizable(False, False)


# Creare il frame principale per i contenuti
main_frame = ttk.Frame(root, padding="20 20 20 20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

poi_label = ttk.Label(main_frame, text="Seleziona un POI:", font=("Roboto", 12))
poi_label.grid(row=4, column=0, pady=10)

poi_dropdown = ttk.Combobox(main_frame, width=38, font=("Roboto", 11))
poi_dropdown.grid(row=5, column=0, pady=10)

excel_label = ttk.Label(main_frame, text="Seleziona un file Excel:", font=("Roboto", 12))
excel_label.grid(row=1, column=0, pady=10)

note_label = ttk.Label(main_frame, text="Il file excel deve rispettare il formato 'id', 'POI', 'rating', 'recensione'", font=("Roboto", 8), foreground="gray")
note_label.grid(row=2, column=0, pady=5)
                
excel_path = tk.StringVar()
excel_entry = ttk.Entry(main_frame, textvariable=excel_path, width=28, font=("Roboto", 11))
excel_entry.grid(row=3, column=0, pady=0, padx=(0, 5), sticky=tk.W)


main_frame.grid_columnconfigure(0, weight=1)


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
    
# Definire uno stile personalizzato per il pulsante "Calcola Sentiment"
style.configure("Custom.TButton", foreground="white", background="#A4224B", font=("Roboto", 11), borderwidth=0,)
style.map("Custom.TButton", background=[('active', '#A4224B')], foreground=[('active', 'white')])

submit_button = ttk.Button(main_frame, text="Calcola Sentiment", command=on_submit, style="Custom.TButton", bootstyle="success")
submit_button.grid(row=6, column=0, pady=20)

browse_button = ttk.Button(main_frame, text="Sfoglia", command=browse_file, style="Custom.TButton", bootstyle="primary")
browse_button.grid(row=3, column=0, pady=0, padx=(245, 0), sticky=tk.E)


for widget in main_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)

# Avvio della finestra Tkinter
root.mainloop()

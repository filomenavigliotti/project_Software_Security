import pandas as pd
import json

def genera_csv_giornalieri(file_json, prefisso_output):
    print("Lettura del dataset originale...")
    with open(file_json, 'r') as f:
        dati = json.load(f)
    
    # 1 giorno = 24 ore * 60 minuti = 1440 campioni (campioniamo ogni minuto)
    campioni_per_giorno = 1440
    intervallo_ms = 60000 
    
    righe_csv = []
    ms_correnti = 0
    giorno_corrente = 1
    
    for i, record in enumerate(dati):
        riga = {'timestamp': ms_correnti}
        riga.update(record['sensori'])
        righe_csv.append(riga)
        
        # Avanza di un minuto
        ms_correnti += intervallo_ms
        
        # Se abbiamo raggiunto la fine di un giorno (1440 campioni) o la fine del file
        if (i + 1) % campioni_per_giorno == 0 or (i + 1) == len(dati):
            df = pd.DataFrame(righe_csv)
            nome_file = f"{prefisso_output}_giorno_{giorno_corrente}.csv"
            df.to_csv(nome_file, index=False)
            
            # Reset delle variabili per iniziare un nuovo file pulito
            righe_csv = []
            ms_correnti = 0 # Azzeriamo il tempo per il nuovo giorno (Edge Impulse preferisce così)
            giorno_corrente += 1
            
    print(f"Fatto! Sono stati creati {giorno_corrente - 1} file CSV giornalieri.")

# Esecuzione script
genera_csv_giornalieri('dataset_storico_training.json', 'training_pulito')
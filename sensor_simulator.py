import json
import math
import random
from datetime import datetime, timedelta

def genera_dataset_industriale_complesso(num_campioni=20000, intervallo_secondi=60):
    dati_simulati = []
    # Partiamo da 30 giorni fa per simulare un log storico reale
    timestamp_corrente = datetime.now() - timedelta(days=30)
    
    for i in range(num_campioni):
        # 1. MACRO-CICLI: Turni di lavoro e Temperatura ambientale
        ora = timestamp_corrente.hour
        
        # Turno diurno (08:00 - 18:00): Pieno carico
        # Turno notturno: Carico ridotto o mantenimento
        if 8 <= ora <= 18:
            rpm_base = 2900
            rumore_rpm = 15.0
        else:
            rpm_base = 1450  # La pompa va a mezza velocità di notte
            rumore_rpm = 8.0
            
        # Variazione temperatura ambientale (Curva cosinusoidale: picco di caldo alle 14:00, freddo alle 02:00)
        # Escursione termica di circa +/- 7°C
        temp_ambientale_delta = 7.0 * math.cos((ora - 14) * math.pi / 12)
        
        # 2. MICRO-CICLI: Fluttuazioni e Usura
        # Leggero degrado lineare nel tempo (simula l'usura dei cuscinetti e filtri nei 30 giorni)
        fattore_usura = (i / num_campioni) 
        
        # Fluttuazione operativa a breve termine
        fluttuazione_breve = math.sin(i * 0.05) * (30 if rpm_base == 2900 else 10)
        
        # --- CALCOLO VARIABILI FISICHE ---
        
        rpm = rpm_base + fluttuazione_breve + random.normalvariate(0, rumore_rpm)
        rapporto_rpm = rpm / 2900.0
        
        # Corrente (Aumenta leggermente con l'usura meccanica)
        corrente = 15.0 * (rapporto_rpm ** 3) + random.normalvariate(0, 0.2) + (fattore_usura * 0.5)
        
        pressione_aspirazione = 1.5 - (rapporto_rpm - 1.0) * 0.2 + random.normalvariate(0, 0.05)
        # La pressione di mandata cala leggermente per usura girante
        pressione_mandata = 6.0 * (rapporto_rpm ** 2) + random.normalvariate(0, 0.1) - (fattore_usura * 0.2)
        
        portata = 250.0 * rapporto_rpm + random.normalvariate(0, 3.0)
        
        # Le temperature ora dipendono anche dal ciclo diurno/notturno del capannone
        temperatura_fluido = 25.0 + temp_ambientale_delta + (corrente * 0.1) - (portata * 0.005) + random.normalvariate(0, 0.2)
        
        # Le vibrazioni aumentano visibilmente con il passare dei giorni (usura)
        vibrazione_base = 1.2 * (rapporto_rpm ** 1.5) + (fattore_usura * 0.8)
        vibrazione_cuscinetto_ant = vibrazione_base + random.normalvariate(0, 0.1)
        vibrazione_cuscinetto_post = (vibrazione_cuscinetto_ant * 0.85) + random.normalvariate(0, 0.08)
        
        # Temperatura motore influenzata da carico, ambiente e usura
        temperatura_motore = 45.0 + temp_ambientale_delta + (corrente - 15.0) * 1.5 + (fattore_usura * 2.0) + random.normalvariate(0, 0.5)
        
        # L'efficienza degrada col tempo
        efficienza = 88.0 - (temperatura_motore - 45.0) * 0.2 - abs(rpm_base - rpm) * 0.01 - (fattore_usura * 3.0) + random.normalvariate(0, 0.3)
        
        # Costruzione del log
        record = {
            "timestamp": timestamp_corrente.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "sensori": {
                "S1_Pompa_RPM": round(rpm, 2),
                "S2_Corrente_A": round(corrente, 2),
                "S3_Pres_Aspirazione_bar": round(pressione_aspirazione, 2),
                "S4_Pres_Mandata_bar": round(pressione_mandata, 2),
                "S5_Portata_Lmin": round(portata, 2),
                "S6_Temp_Fluido_C": round(temperatura_fluido, 2),
                "S7_Vib_Cuscinetto_Ant_mms": round(vibrazione_cuscinetto_ant, 2),
                "S8_Vib_Cuscinetto_Post_mms": round(vibrazione_cuscinetto_post, 2),
                "S9_Temp_Motore_C": round(temperatura_motore, 2),
                "S10_Efficienza_Pct": round(efficienza, 2)
            }
        }
        
        dati_simulati.append(record)
        # Avanza di X secondi (1 minuto)
        timestamp_corrente += timedelta(seconds=intervallo_secondi)
        
    return dati_simulati

# Generiamo 40.000 campioni (a 1 minuto di distanza, coprono circa 27 giorni interi)
print("Generazione dataset in corso...")
dataset_storico = genera_dataset_industriale_complesso(40000, 60)

nome_file = "dataset_storico_training.json"
with open(nome_file, "w") as f:
    json.dump(dataset_storico, f, indent=4)

print(f"Fatto! File '{nome_file}' generato. Contiene {len(dataset_storico)} log.")
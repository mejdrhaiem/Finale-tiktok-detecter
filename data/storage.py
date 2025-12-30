import os
import sys
import pandas as pd
from datetime import datetime

# Gérer les chemins pour PyInstaller (exécutable)
if getattr(sys, 'frozen', False):
    # Si l'application est exécutée comme un exécutable PyInstaller
    base_path = sys._MEIPASS
    DATA_DIR = os.path.join(os.path.dirname(sys.executable), "data")
else:
    # Si l'application est exécutée comme script Python normal
    base_path = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(base_path, "data")

os.makedirs(DATA_DIR, exist_ok=True)
TXT_FILE = os.path.join(DATA_DIR, "phones.txt")
CSV_FILE = os.path.join(DATA_DIR, "phones.csv")

phones_set = set()

def save_phone(phone, suite, user):
    key = f"{phone}-{suite}"

    if key in phones_set:
        return False

    phones_set.add(key)

    # Obtenir le timestamp actuel
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_display = datetime.now().strftime("%H:%M:%S")

    # Sauvegarde dans le fichier TXT
    with open(TXT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {phone} | {suite} | {user}\n")

    # Sauvegarde dans le fichier CSV
    df = pd.DataFrame(
        [[timestamp, user, phone, suite]],
        columns=["Time", "User", "Phone", "Suite_Commentaire"]
    )

    if not os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, index=False, encoding="utf-8")
    else:
        # Pour ajouter au CSV existant, on utilise append mode
        with open(CSV_FILE, "a", encoding="utf-8", newline="") as f:
            df.to_csv(f, header=False, index=False)

    return True


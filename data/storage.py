import os
import pandas as pd

DATA_DIR = "data"
TXT_FILE = os.path.join(DATA_DIR, "phones.txt")
CSV_FILE = os.path.join(DATA_DIR, "phones.csv")

os.makedirs(DATA_DIR, exist_ok=True)

phones_set = set()

def save_phone(phone, suite, user):
    key = f"{phone}-{suite}"

    if key in phones_set:
        return False

    phones_set.add(key)

    # Sauvegarde dans le fichier TXT
    with open(TXT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{phone} | {suite} | {user}\n")

    # Sauvegarde dans le fichier CSV
    df = pd.DataFrame(
        [[phone, suite, user]],
        columns=["Phone", "Suite_Commentaire", "User"]
    )

    if not os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, index=False, encoding="utf-8")
    else:
        # Pour ajouter au CSV existant, on utilise append mode
        with open(CSV_FILE, "a", encoding="utf-8", newline="") as f:
            df.to_csv(f, header=False, index=False)

    return True


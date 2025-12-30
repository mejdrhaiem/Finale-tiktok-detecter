import re

def extract_phone_and_suite(text):
    """
    Détecte TOUS les numéros contenant exactement 8 chiffres,
    même avec espaces/tirets/points placés n'importe où entre les chiffres.

    Ex:
    22 555 366  (8 chiffres: 2 2 5 5 5 3 6 6)
    225 55 366  (8 chiffres: 2 2 5 5 5 3 6 6)
    2 2 5 5 5 3 6 6  (8 chiffres séparés)
    22555366    (8 chiffres sans espace)
    +216 22 555 366  (avec indicatif)
    22-555-366  (avec tirets)
    22.555.366  (avec points)
    """

    results = []

    # Regex améliorée : trouve des séquences avec chiffres et séparateurs
    # La regex est plus permissive pour capturer différents formats, puis on vérifie exactement 8 chiffres
    pattern = re.compile(
        r"""
        (?<!\d)                       # pas précédé par un chiffre
        (?:\+216[\s\-\.]*)?           # indicatif optionnel +216
        (                              # groupe 1: séquence à analyser
            (?:                        # groupe non-capturant pour répétition
                \d                     # un chiffre
                [\s\-\.]*              # séparateurs optionnels (espaces, tirets, points)
            ){8}                       # exactement 8 fois (pour garantir 8 chiffres)
        )
        (?![\d\-\.])                  # pas suivi par un chiffre, tiret ou point
        """,
        re.VERBOSE
    )

    for match in pattern.finditer(text):
        raw_sequence = match.group(1)
        
        # Nettoyer: extraire uniquement les chiffres
        clean = re.sub(r"\D", "", raw_sequence)
        
        # Vérifier qu'on a exactement 8 chiffres (pas plus, pas moins)
        if len(clean) == 8:
            # Extraire la suite du commentaire (tout le texte sauf le numéro détecté)
            full_match = match.group(0)
            suite = text.replace(full_match, "", 1).strip()
            
            results.append((clean, suite))

    return results

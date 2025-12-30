import re

def extract_phone_and_suite(text):
    """
    Détecte TOUS les numéros contenant exactement 8 chiffres,
    même avec espaces/tirets/points placés n'importe où.

    Ex:
    22 666 666
    222 66 666
    22 66 66 66
    2 26 66 666
    22266666
    +216 22 666 666
    """

    results = []

    # Regex universelle : 8 chiffres avec séparateurs optionnels
    pattern = re.compile(
        r"""
        (?<!\d)                       # pas précédé par un chiffre
        (?:\+216[\s\-\.]*)?           # indicatif optionnel
        ((?:\d[\s\-\.]*){8})          # exactement 8 chiffres, séparateurs libres
        (?!\d)                        # pas suivi par un chiffre
        """,
        re.VERBOSE
    )

    for match in pattern.finditer(text):
        raw = match.group(1)

        # Nettoyage total
        clean = re.sub(r"\D", "", raw)

        # Sécurité absolue
        if len(clean) == 8:
            suite = text.replace(match.group(0), "").strip()
            results.append((clean, suite))

    return results

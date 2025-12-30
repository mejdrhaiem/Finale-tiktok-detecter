from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent
import time

from detector import extract_phone_and_suite
from storage import save_phone
from config import USERNAME, PROXY

# Fonction pour créer et configurer le client
def create_client():
    """Crée un nouveau client TikTok Live"""
    client_config = {
        "unique_id": USERNAME,
    }
    
    # Ajouter le proxy si configuré
    if PROXY:
        client_config["proxy"] = PROXY
    
    client = TikTokLiveClient(**client_config)
    
    # Événement commentaire
    @client.on(CommentEvent)
    async def on_comment(event: CommentEvent):
        try:
            text = event.comment
            user = event.user.nickname  # ✅ Utilise 'nickname' ici

            print(f"💬 {user}: {text}")

            # EXTRACTION numéro + suite commentaire
            results = extract_phone_and_suite(text)

            for phone, suite in results:
                if save_phone(phone, suite, user):
                    print(f"📞 {phone} | 📝 {suite} | 👤 {user}")
        except Exception as e:
            # Gérer les erreurs silencieusement pour éviter les opérations qui se chevauchent
            print(f"⚠️ Erreur lors du traitement du commentaire: {e}")
    
    return client

# Fonction pour lancer le client avec retry en cas d'erreur
def run_with_retry(max_retries=5, delay=5):
    """Lance le client avec retry en cas d'erreur de blocage"""
    client = None
    for attempt in range(max_retries):
        try:
            # Créer un nouveau client à chaque tentative pour éviter les chevauchements
            if client is not None:
                try:
                    client.stop()
                except:
                    pass
                time.sleep(1)  # Attendre un peu avant de recréer
            
            client = create_client()
            if PROXY:
                print("🔒 Utilisation d'un proxy configuré")
            print(f"Tentative de connexion {attempt + 1}/{max_retries}...")
            print("🔴 En attente du LIVE TikTok...")
            client.run()
        except KeyboardInterrupt:
            print("\n⚠️ Arrêt demandé par l'utilisateur")
            if client is not None:
                try:
                    client.stop()
                except:
                    pass
            break
        except Exception as e:
            error_msg = str(e)
            error_type = type(e).__name__
            
            # Gérer les erreurs 500 API sign (erreur serveur TikTok temporaire)
            if "500" in error_msg or "api sign" in error_msg.lower() or "Internal Server Error" in error_msg:
                print(f"⚠️ Erreur API serveur TikTok (500): {error_msg}")
                if attempt < max_retries - 1:
                    print(f"⏳ Attente de {delay} secondes avant de réessayer...")
                    # Nettoyer le client actuel
                    if client is not None:
                        try:
                            client.stop()
                        except:
                            pass
                    time.sleep(delay)
                    delay *= 2  # Augmenter le délai à chaque tentative
                else:
                    print("\n❌ Échec après plusieurs tentatives.")
                    print("💡 L'erreur 500 est souvent temporaire. Solutions:")
                    print("   1. Attendre 5-10 minutes et réessayer")
                    print("   2. Vérifier votre connexion internet")
                    print("   3. Utiliser un VPN ou un proxy")
                    raise
            # Gérer les erreurs de blocage
            elif "DEVICE_BLOCKED" in error_msg or "WebcastBlocked" in error_msg:
                print(f"❌ Erreur de blocage détectée: {error_msg}")
                if attempt < max_retries - 1:
                    print(f"⏳ Attente de {delay} secondes avant de réessayer...")
                    time.sleep(delay)
                    delay *= 2  # Augmenter le délai à chaque tentative
                else:
                    print("\n❌ Échec après plusieurs tentatives.")
                    print("💡 Solutions possibles:")
                    print("   1. Attendre quelques minutes et réessayer")
                    print("   2. Utiliser un VPN ou un proxy")
                    print("   3. Vérifier que le compte TikTok est bien en live")
                    print("   4. Essayer avec un autre compte TikTok")
                    raise
            # Gérer les erreurs de chevauchement/cancellation
            elif "cancelled" in error_msg.lower() or "overlapped" in error_msg.lower() or "CancelledError" in error_type:
                print(f"⚠️ Erreur de chevauchement détectée: {error_msg}")
                if attempt < max_retries - 1:
                    print(f"⏳ Attente de {delay} secondes avant de réessayer...")
                    # Nettoyer le client actuel
                    if client is not None:
                        try:
                            client.stop()
                        except:
                            pass
                    time.sleep(delay)
                    delay *= 2  # Augmenter le délai à chaque tentative
                else:
                    print("\n❌ Échec après plusieurs tentatives.")
                    raise
            else:
                print(f"❌ Erreur inattendue: {error_type}: {error_msg}")
                raise

# Lancer le client
if __name__ == "__main__":
    run_with_retry()

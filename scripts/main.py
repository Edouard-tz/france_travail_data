"Module permettant de faire les appelles à l'API et génerer les fichier"

from scripts.config_loader import load_config
from scripts.client_api import APIclient


def main():
    # Charger la configuration
    config = load_config()

    # Initialiser le client API
    client = APIclient(config)

    # Appel dynamique d'un endpoint
    client.fetch_and_load()


if __name__ == "__main__":
    main()

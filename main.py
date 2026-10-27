from dotenv import load_dotenv
from models import init_db


# Charge le contenu du fichier .env dans les variables d'environnement
load_dotenv()

init_db()

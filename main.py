from dotenv import load_dotenv
import migrations as migrations
from models import init_db, populate_db
from alembic.config import Config

# Charge le contenu du fichier .env dans les variables d'environnement
load_dotenv()

# Charger la configuration depuis le fichier alembic.ini
config = Config("alembic.ini")

init_db()
migrations.upgrade(config, "head")

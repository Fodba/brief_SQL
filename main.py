import os
import psycopg2
from psycopg2 import sql  
import pydantic
from dotenv import load_dotenv
from models import Base
from sqlalchemy import create_engine, inspect, text


# Charge le contenu du fichier .env dans les variables d'environnement
load_dotenv()

# ==========================================
# ÉTAPE 1 : Création de la base 
# ==========================================
try:
    # 1. Connexion à la base par défaut "postgres"
    conn = psycopg2.connect(
        dbname="postgres", 
        port=os.getenv("PG_PORT"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
    )

    # TRÈS IMPORTANT : PostgreSQL interdit l'exécution de CREATE DATABASE
    # à l'intérieur d'une transaction. Il faut activer l'autocommit.
    conn.autocommit = True
    cursor = conn.cursor()

    # 2. Vérifier si la base existe déjà
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s;", (os.getenv('PG_DATABASE'),)
    )
    exists = cursor.fetchone()

    if not exists:
        # 3. Créer la base de données (avec des guillemets pour respecter la casse)
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(os.getenv('PG_DATABASE')))
        )
        print(f"Base de données '{os.getenv('PG_DATABASE')}' créée avec succès via psycopg2 !")
    else:
        print(f"La base de données '{os.getenv('PG_DATABASE')}' existe déjà.")

    # Fermeture du curseur et de la connexion
    cursor.close()
    conn.close()

except Exception as e:
  print(f"Erreur lors de la création de la base de données : {e}")
  exit(1)

# ÉTAPE 2 : Connexion à la nouvelle base "CFTech" pour créer les tables
try:
    conn_pg = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT", "5432"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DATABASE"),
    )
    curseur = conn_pg.cursor()
    curseur.execute("SELECT version()")
    print("✅ Connecté à", curseur.fetchone()[0].split(" on ")[0])
except psycopg2.OperationalError as erreur:
    conn_pg = None
    print("⚠️ PostgreSQL indisponible :", erreur)


url_pg = (
    f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
    f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}"
)

if conn_pg:
    engine = create_engine(url_pg)


# Création de toutes les tables définies dans Base
Base.metadata.create_all(engine)
print("Toutes les tables ont été créées avec succès dans la base !")
print("Tables présentes dans la base :", inspect(engine).get_table_names())
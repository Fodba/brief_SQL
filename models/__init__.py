# models/__init__.py
import os
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine, inspect

from .base import Base
from .access_level import AccessLevel
from .classroom import Classroom
from .job import Job
from .study_level import StudyLevel
from .user import User
from .admin import Admin
from .staff import Staff
from .student import Student
from .teacher import Teacher
from .session import Session
from .registration import Registration

def connect(database, query):
    try:
        # 1. Connexion à la base par défaut "postgres"
        conn = psycopg2.connect(
            dbname=database, 
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
        )
        
        conn.autocommit = True
        # 2. execution de la requête
        cursor = conn.cursor()
        print(query)
        cursor.execute(query)
        return cursor, conn
    except Exception as e:
        print(f"Erreur lors de la connection de la base de données : {e}")
        exit(1)


def init_db():
    # ÉTAPE 1 : Création de la base 

    cursor, conn = connect("postgres", f"SELECT 1 FROM pg_database WHERE datname = '{os.getenv('PG_DATABASE')}';")

    exists = cursor.fetchall()

    if not exists:
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(os.getenv('PG_DATABASE')))
        )
        print(f"Base de données '{os.getenv('PG_DATABASE')}' créée avec succès via psycopg2 !")
    else:
        print(f"La base de données '{os.getenv('PG_DATABASE')}' existe déjà.")

    # Fermeture du curseur et de la connexion
    cursor.close()
    conn.close()


def populate_db():
    # ÉTAPE 2 : Connexion à la nouvelle base "CFTech" pour créer les tables
    cursor, conn_pg = connect(os.getenv("PG_DATABASE"), "SELECT version()")
    print("✅ Connecté à", cursor.fetchone()[0].split(" on ")[0])

    url_pg = (
        f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
        f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}"
    )

    if conn_pg:
        engine = create_engine(url_pg)


    # Création de toutes les tables définies dans Base
    Base.metadata.create_all(engine)

    cursor.close()
    conn_pg.close()
    print("Toutes les tables ont été créées avec succès dans la base !")
    print("Tables présentes dans la base :", inspect(engine).get_table_names())

    
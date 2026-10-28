from datetime import date
import os
import sys
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy

path_projet = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if path_projet not in sys.path:
    sys.path.insert(0, path_projet)

from models import (
    Base, AccessLevel, Classroom, Job, StudyLevel, 
    User, Admin, Staff, Student, Teacher, Session, Registration
)

load_dotenv()
app = Flask(__name__)

# --- Connexion base de données ---
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}"
# Ajoutez une clé secrète (obligatoire pour utiliser flash)
app.config["SECRET_KEY"] = "une_cle_secrete_tres_securisee"

# Initialisation de l'extension
db = SQLAlchemy(app)


@app.route("/")
def index():
   return render_template("index.html")

@app.route("/users", methods=["GET"])
def manage_users():
    all_users = db.session.query(User).order_by(User.id.desc()).limit(5).all()
    study_levels = db.session.query(StudyLevel).all()
    # On envoie la liste des produits au fichier HTML
    return render_template("users.html", all_users= all_users, study_level= study_levels)


@app.route("/users", methods=["POST"])
def register_user():
    account_type = request.form.get("account_type")

    if account_type == "student":
        try:
            # Étape A : Insertion dans la table commune 'users'
            new_user = User(
                firstname=request.form.get("firstname"),
                lastname=request.form.get("lastname"),
                email=request.form.get("email"),
                creation_date=date.today(),  # Date du jour générée automatiquement
                is_active=True,
            )
            db.session.add(new_user)

            # On force SQLAlchemy à générer l'ID de l'utilisateur sans valider définitivement la transaction
            db.session.flush()

            # Étape B : Liaison et insertion dans la table spécifique 'students'
            new_student = Student(
                id_1=new_user.id,  # Récupère l'ID généré par la table 'users'
                birth_date=date.fromisoformat(request.form.get("birth_date")),
                phone=request.form.get("phone"),
                obtained_certification=request.form.get("obtained_certification"),
                registration_date=date.today(),
                id=int(
                    request.form.get("study_level_id")
                ),  # ID Clé étrangère vers study_level
            )
            db.session.add(new_student)

            # Validation finale des deux opérations en base de données
            db.session.commit()
            flash(
                "Inscription réussie ! Votre compte Étudiant a été enregistré en base de données.",
                "success",
            )
            # 3. On redirige sur la page du formulaire au lieu d'une page blanche
            return redirect(url_for("manage_users"))

        except Exception as e:
            db.session.rollback()  # Annule tout en cas d'erreur (évite les données orphelines)
            flash(f"Erreur lors de l'inscription de l'étudiant : {str(e)}", "danger")
            return redirect(url_for("manage_users"))
    elif account_type == "teacher":
        try:
            # Étape A : Insertion dans la table commune 'users'
            new_user = User(
                firstname=request.form.get("firstname"),
                lastname=request.form.get("lastname"),
                email=request.form.get("email"),
                creation_date=date.today(),
                is_active=True,
            )
            db.session.add(new_user)
    
            # On force la génération de l'ID utilisateur
            db.session.flush()
    
            # Étape B : Liaison et insertion dans la table spécifique 'teachers'
            new_teacher = Teacher(
                id=new_user.id,  # Récupère l'ID généré (PK et FK vers users)
                specialty=request.form.get("specialty"),
                hire_date=date.today(),
                hourly_rate=float(request.form.get("hourly_rate")),
                biography=request.form.get("biography"),
            )
            db.session.add(new_teacher)
    
            # Validation finale en base de données
            db.session.commit()
            flash(
                "Inscription réussie ! Votre compte Professeur a été enregistré en base de données.",
                "success",
            )
            # 3. On redirige sur la page du formulaire au lieu d'une autre page
            return redirect(url_for("manage_users"))
    
        except Exception as e:
            db.session.rollback()  # Sécurité : annule la transaction si une erreur survient
            flash(f"Erreur lors de l'inscription du professeur : {str(e)}", "danger")
            return redirect(url_for("manage_users"))
    

if __name__ == "__main__":
    app.run(debug=True)
    
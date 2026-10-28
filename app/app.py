from datetime import date
import os
import sys
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
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


# Initialisation de l'extension
db = SQLAlchemy(app)

with app.app_context():
    # Vous mappez votre classe Python à la table existante
    class Users(db.Model):
        # Indiquez le nom exact de la table dans votre BDD
        __tablename__ = "users"

        # Déclarez au moins la clé primaire et les colonnes à utiliser
        id = db.Column(db.Integer, primary_key=True)
        firstname = db.Column(db.String)
        lastname = db.Column(db.String)
        email = db.Column(db.String)

    class StudyLevel(db.Model):
        # Indiquez le nom exact de la table dans votre BDD
        __tablename__ = "study_level"
        id = db.Column(db.Integer, primary_key=True)
        label = db.Column(db.String)




@app.route("/")
def index():
   return render_template("index.html")

@app.route("/users", methods=["GET"])
def list_users():
    all_users =  Users.query.order_by(Users.id.desc()).limit(5).all()
    study_level = StudyLevel.query.all()
    # On envoie la liste des produits au fichier HTML
    return render_template("users.html", all_users= all_users, study_level= study_level)


@app.route("/users/student", methods=["POST"])
def register_student():
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
        return redirect(url_for("success"))

    except Exception as e:
        db.session.rollback()  # Annule tout en cas d'erreur (évite les données orphelines)
        return f"Erreur lors de l'inscription de l'étudiant : {str(e)}", 400


# ==========================================
# 3. TRAITEMENT DE L'INSCRIPTION PROFESSEUR (POST)
# ==========================================
@app.route("/users/teacher", methods=["POST"])
def register_teacher():
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
        return redirect(url_for("success"))

    except Exception as e:
        db.session.rollback()  # Sécurité : annule la transaction si une erreur survient
        return f"Erreur lors de l'inscription du professeur : {str(e)}", 400




if __name__ == "__main__":
    app.run(debug=True)
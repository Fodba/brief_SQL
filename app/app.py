import sys
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

from schemas import (pydandic_registration, pydantic_teacher, pydantic_study_level,
pydantic_student, pydantic_session, pydantic_classroom, pydantic_admin, pydandic_user,
pydandic_staff, pydandic_job, pydantic_access_level)

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
   all_users = db.session.query(User).order_by(User.id.desc()).limit(5).all()
   return render_template("index.html", 
                           all_users = all_users)

@app.route("/users", methods=["GET"])
def manage_users():
    all_users = db.session.query(User).order_by(User.id.desc()).limit(5).all()
    study_levels = db.session.query(StudyLevel).all()
    job_list = db.session.query(Job).all()
    access_list = db.session.query(AccessLevel).all()
    # On envoie la liste des produits au fichier HTML
    return render_template("users.html", 
                           all_users = all_users, 
                           study_level = study_levels, 
                           job_list = job_list,
                           access_list = access_list)


@app.route("/users", methods=["POST"])
def register_user():
    account_type = request.form.get("account_type")

    try:
        # Étape A : Insertion dans la table commune 'users'

        # On met les données dans un dictionnaire
        data = {
            "firstname" : request.form.get("firstname"),
            "lastname" : request.form.get("lastname"),
            "email" : request.form.get("email"),
            "creation_date" : date.today(),  # Date du jour générée automatiquement
            "is_active" : True
        }
        
        # On passe les données dans le modèle Pydantic pour les vérifier
        validate = pydandic_user.User(**data)
        new_user = User(**validate.model_dump())
        db.session.add(new_user)
        db.session.flush()

        # On force SQLAlchemy à générer l'ID de l'utilisateur sans valider définitivement la transaction
        

        # Étape B : Liaison et insertion dans les tables spécifiques
        match account_type:
            case "student":
                data = {
                    "id_1" : new_user.id,  # Récupère l'ID généré par la table 'users'
                    "birth_date" : date.fromisoformat(request.form.get("birth_date")),
                    "phone" : request.form.get("phone"),
                    "obtained_certification" : request.form.get("obtained_certification"),
                    "registration_date" : date.today(),
                    "id" : int(
                        request.form.get("study_level_id")
                    )
                }
                validate = pydantic_student.Student(**data)
                new_student=Student(**validate.model_dump())
                db.session.add(new_student)
                db.session.flush()

            case "teacher":
                data={
                    "id" : new_user.id,  # Récupère l'ID généré (PK et FK vers users)
                    "specialty" :request.form.get("specialty"),
                    "hire_date" : date.today(),
                    "hourly_rate" : float(request.form.get("hourly_rate")),
                    "biography" : request.form.get("biography")
                }
                validate = pydantic_teacher.Teacher(**data)
                new_teacher=Teacher(**validate.model_dump())
                db.session.add(new_teacher)
                db.session.flush()
            case "staff":
                data={
                    "id_1" : new_user.id,  # Récupère l'ID généré (PK et FK vers users)
                    "start_date" : date.fromisoformat(request.form.get("start_date")),
                    "responsabilities" : request.form.get("responsabilities"),
                    "id" : int(
                        request.form.get("job_id")
                    )
                }
                validate = pydandic_staff.Staff(**data)
                new_staff=Staff(**validate.model_dump())
                db.session.add(new_staff)
                db.session.flush()
            case "admin":
                data={
                    "id_1" :new_user.id,  # Récupère l'ID généré (PK et FK vers users)
                    "promotion_date" : date.fromisoformat(request.form.get("promotion_date")),
                    "id" : int(
                        request.form.get("access_level_id")
                    ),
                }
                validate = pydantic_admin.Admin(**data)
                new_admin = Admin(**validate.model_dump())
                db.session.add(new_admin)
                db.session.flush()

        # Validation finale en base de données
        db.session.commit()
        flash(
            "Inscription réussie ! Votre compte a été enregistré en base de données.",
            "success",
        )
        # 3. On redirige sur la page du formulaire au lieu d'une autre page
        return redirect(url_for("manage_users"))
    
    except Exception as e:
        db.session.rollback()  # Annule tout en cas d'erreur (évite les données orphelines)
        flash(f"Erreur lors de l'inscription : {str(e)}", "danger")
        return redirect(url_for("manage_users"))


@app.route("/study", methods=["GET"])
def study():
   study_level = db.session.query(StudyLevel).all()
   return render_template("study.html", study_level = study_level)


@app.route("/study", methods=["POST"])
def add_study_level():
    try:
        data={
            "label" : request.form.get("label")
        }
        validate = pydantic_study_level.StudyLevel(**data)

        new_role = StudyLevel(**validate.model_dump())
        db.session.add(new_role)
        db.session.flush()
        db.session.commit()
        flash(
            "Enregistrement réussie !",
            "success",
        )
        # 3. On redirige sur la page du formulaire au lieu d'une autre page
        return redirect(url_for("study"))
    
    except Exception as e:
        db.session.rollback() 
        flash(f"Erreur lors de l'enregistrement : {str(e)}", "danger")
        return redirect(url_for("study"))


@app.route("/job", methods=["GET"])
def job():
   job_list = db.session.query(Job).all()
   return render_template("job.html", job_list = job_list)


@app.route("/job", methods=["POST"])
def add_job():
    try:
        data={
            "label" : request.form.get("label")
        }
        validate = pydandic_job.Job(**data)
        new_job = Job(**validate.model_dump())
        db.session.add(new_job)
        db.session.flush()
        db.session.commit()
        flash(
            "Enregistrement réussie !",
            "success",
        )
        # 3. On redirige sur la page du formulaire au lieu d'une autre page
        return redirect(url_for("job"))
    
    except Exception as e:
        db.session.rollback() 
        flash(f"Erreur lors de l'enregistrement : {str(e)}", "danger")
        return redirect(url_for("job"))



@app.route("/role", methods=["GET"])
def role():
   role_list = db.session.query(AccessLevel).all()
   return render_template("role.html", role_list = role_list)


@app.route("/role", methods=["POST"])
def add_access_level():
    try:
        data={
            "label" : request.form.get("label")
        }
        validate = pydantic_access_level.AccessLevel(**data)
        new_role = AccessLevel(**validate.model_dump())
        db.session.add(new_role)
        db.session.flush()
        db.session.commit()
        flash(
            "Enregistrement réussie !",
            "success",
        )
        # 3. On redirige sur la page du formulaire au lieu d'une autre page
        return redirect(url_for("role"))
    
    except Exception as e:
        db.session.rollback() 
        flash(f"Erreur lors de l'enregistrement : {str(e)}", "danger")
        return redirect(url_for("role"))



@app.route("/classroom", methods=["GET"])
def classroom():
   classroom_list = db.session.query(Classroom).all()
   return render_template("classroom.html", classroom_list = classroom_list)

@app.route("/classroom", methods=["POST"])
def add_classroom():
    try:
        data={
            "name" : request.form.get("label"),
            "capacity" : request.form.get("capacity"),
            "location" : request.form.get("location"),
            "is_active" : bool(request.form.get("is_active")),
            "equipments" : request.form.get("equipments")
        }
        validate = pydantic_classroom.Classroom(**data)
        new_classroom = Classroom(**validate.model_dump())
        db.session.add(new_classroom)
        db.session.flush()
        db.session.commit()
        flash(
            "Enregistrement réussie !",
            "success",
        )
        return redirect(url_for("classroom"))
    
    except Exception as e:
        db.session.rollback() 
        flash(f"Erreur lors de l'enregistrement : {str(e)}", "danger")
        return redirect(url_for("classroom"))

@app.route("/session", methods=["GET"])
def session():
   session_list = db.session.query(Session).order_by(Session.id.desc()).limit(10).all()
   status_list = db.session.query(Session).order_by(Session.status.desc()).all()
   teacher_list = db.session.query(Teacher).all()
   classroom_list = db.session.query(Classroom).all()
   return render_template("session.html", 
                          session_list = session_list, 
                          status_list = status_list,
                          teacher_list = teacher_list,
                          classroom_list = classroom_list)

@app.route("/session", methods=["POST"])
def add_session():
    try:
        if request.form.get("type") == "add_session":
            data={
                "status" : "OUVERT",
                "title" : request.form.get("title"),
                "description" : request.form.get("description"),
                "start_date" : date.fromisoformat(request.form.get("start_date")),
                "end_date" : date.fromisoformat(request.form.get("end_date")),
                "max_capacity" : request.form.get("max_capacity"),
                "prerequisite"  : request.form.get("prerequisite"),
                "id_1" : int(
                    request.form.get("classroom_id")
                ),  # ID Clé étrangère vers classroom_id
                "id_2" : int(
                    request.form.get("teacher_id")
                )
            }
            validate = pydantic_session.Session(**data)
            new_session = Session(**validate.model_dump())
            db.session.add(new_session)
            db.session.flush()
            db.session.commit()
            flash(
                "Enregistrement réussie !",
                "success",
            )
            return redirect(url_for("session"))
        elif request.form.get("type") == "manage_session":
            session_to_update = db.session.query(Session).get(int(request.form.get("session_id")))
            session_to_update.status = request.form.get("status")
            
            db.session.commit()
            flash(
                "Mis à jour réussie !",
                "success",
            )
            return redirect(url_for("session"))
    
    except Exception as e:
        db.session.rollback() 
        flash(f"Erreur lors de l'enregistrement : {str(e)}", "danger")
        return redirect(url_for("session"))

@app.route("/registration", methods=["GET"])
def registration():
   registration_list = db.session.query(Registration).all()
   student_list = db.session.query(Student).all()
   session_list = db.session.query(Session).order_by(Session.id.desc()).all()
   return render_template("registration.html", 
                          registration_list = registration_list,
                          student_list = student_list,
                          session_list = session_list)

@app.route("/registration", methods=["POST"])
def add_registration():
    try:
        data={
            "register_date" : date.fromisoformat(request.form.get("registration_date")),
            "status" : "EN_ATTENTE",
            "id_1" : int(request.form.get("student_id")), # FK vers students
            "id_2" : int(request.form.get("session_id"))# FK vers session
        }
        validate = pydandic_registration.Registration(**data)
        new_registration = Registration(**validate.model_dump())
        db.session.add(new_registration)
        db.session.flush()
        db.session.commit()
        flash(
            "Enregistrement réussie !",
            "success",
        )
        return redirect(url_for("registration"))
    except Exception as e:
        db.session.rollback() 
        flash(f"Erreur lors de l'enregistrement : {str(e)}", "danger")
        return redirect(url_for("registration"))



if __name__ == "__main__":
    app.run(debug=True)
    
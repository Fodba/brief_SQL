import os
from dotenv import load_dotenv
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (
    connect,
    Base, AccessLevel, Classroom, Job, StudyLevel, 
    User, Admin, Staff, Student, Teacher, Session, Registration
)

def add_data():
    load_dotenv()

    # Connect PostgreSQL 
    cursor, conn_pg = connect(os.getenv("PG_DATABASE"), "SELECT version()")
    url_pg = (
        f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
        f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}"
    )

    if conn_pg:
        engine = create_engine(url_pg)

    # Create session for prepare multiple query before send to DB
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as session:
        # Try to make transaction, else rollback
        try:
            print("- Insertion tables de base")
            
            # AccessLevel 
            lvl_admin = AccessLevel(label="Administrateur Général")
            lvl_mod = AccessLevel(label="Accès Restreint")
            session.add_all([lvl_admin, lvl_mod])

            # Classroom
            room1 = Classroom(
                name="Salle Multimédia 202", 
                capacity=24, 
                location="Aile Nord", 
                is_active=True, 
                equipments="Vidéoprojecteur, Tableaux blancs"
            )
            session.add(room1)

            # Job
            job_sec = Job(label="Secrétaire Académique")
            session.add(job_sec)

            # StudyLevel
            study_bts = StudyLevel(label="BTS Informatique (SIO)")
            session.add(study_bts)

            # Send temp query and check validity of auto-id
            session.flush()

        
            print("- Insertion Users")
            # Users 
            u_admin = User(lastname="Martin", firstname="Alice", email="alice.martin@cftech.fr", creation_date=date(2026, 1, 1), is_active=True)
            u_staff = User(lastname="Durand", firstname="Bob", email="bob.durand@cftech.fr", creation_date=date(2026, 2, 1), is_active=True)
            u_teacher = User(lastname="Dupont", firstname="Jean", email="jean.dupont@cftech.fr", creation_date=date(2026, 3, 1), is_active=True)
            u_student = User(lastname="Bernard", firstname="Lucas", email="lucas.bernard@cftech.fr", creation_date=date(2026, 9, 1), is_active=True)

            # add multiple object in same time
            session.add_all([u_admin, u_staff, u_teacher, u_student])
            session.flush()

            
            print("- Insertion utilisateurs spécifiques")

            # Admin 
            admin_entry = Admin(
                id_1=u_admin.id,
                promotion_date=date(2026, 1, 15), 
                id=lvl_admin.id
            )
            session.add(admin_entry)

            # Staff 
            staff_entry = Staff(
                id_1=u_staff.id, 
                job="Coordinateur", 
                start_date=date(2026, 2, 15), 
                responsabilities="Planification et suivi des inscriptions.",
                id=job_sec.id
            )
            session.add(staff_entry)

            # Teacher
            teacher_entry = Teacher(
                id=u_teacher.id,
                specialty="Développement Python & SQL",
                hire_date=date(2026, 3, 1),
                hourly_rate=45.50,
                biography="Expert en architectures logicielles et bases de données relationnelles."
            )
            session.add(teacher_entry)

            # Student 
            student_entry = Student(
                id_1=u_student.id,
                birth_date=date(2005, 6, 20), 
                phone="0102030405", 
                obtained_certification="Baccalauréat STI2D", 
                registration_date=date(2026, 9, 1), 
                id=study_bts.id              
            )
            session.add(student_entry)

            session.flush()

            print("- Insertion des cours")

            # Session 
            session_entry = Session(
                status="OUVERT",             
                title="Maîtrise de l'ORM SQLAlchemy", 
                description="Cours théorique et pratique sur la gestion des schémas et l'insertion de données.", 
                start_date=date(2026, 10, 1), 
                end_date=date(2026, 10, 5), 
                max_capacity=25, 
                prerequisite="Bases de la syntaxe Python 3",
                id_1=room1.id,               
                id_2=teacher_entry.id        
            )
            session.add(session_entry)
            session.flush()

            print("- Insertion Inscriptions des étudiants")

            # Registration 
            registration_entry = Registration(
                register_date=date(2026, 9, 10), 
                presence=None,              
                status="ENREGISTRÉ",
                id_1=student_entry.id_1,     
                id_2=session_entry.id        
            )
            session.add(registration_entry)

            # send data inside PostgreSQL
            session.commit()
            print("✅ Félicitations : Toutes les données ont été insérées !")
            

        except Exception as e:
            session.rollback()
            print(f"❌ Annulation de la transaction suite à une erreur : {e}")
            raise e
        
    cursor.close()
    conn_pg.close()

if __name__ == "__main__":
    add_data()
    
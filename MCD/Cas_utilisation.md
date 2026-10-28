# Cas d'utilisation de l'application CFTech

## Acteurs

* Users
* Student
* Teacher
* Staff
* Admin

## Liste des verbes d'action

* utiliser plateforme
* Gérer utilisateurs (admin/staff):
    * Créer/activer/désactiver compte apprenants (staff/admin)
    * Créer/activer/désactiver compte formateur (staff/admin)
    * Créer/activer/désactiver compte STAFF (staff/admin)
    * Créer/activer/désactiver compte admin (admin)
* Enregistrer inscriptions:
    * enregistrer 
    * mettre en attente
    * désinscrire
* Valider données d'entrée

* S'inscrire à une formation: 
    * inscription à la plateforme (apprenant)
    * inscription à la session (staff)
* Créer un parcours de formation (staff):
    * Trouver professeur
    * Choisir salle
    * Définir dates
    * Inscrire les apprenants


## CRUD + acteur

### Student

* Create: Student/Staff
* Read: Student/Staff/Teacher
* Update: Staff
* Delete: Staff

### Teacher

* Create: Staff
* Read: Staff/Teacher
* Update: Staff
* Delete: Staff

### Staff

* Create: Staff/Admin
* Read: Staff/Admin
* Update: Staff/Admin
* Delete: Staff/Admin

### Admin

* Create: Admin
* Read: Admin
* Update: Admin
* Delete: Admin

### Classroom

* Create: Staff
* Read: Staff
* Update: Staff
* Delete: Staff

### Registrations

* Create: Staff
* Read: Staff
* Update: Staff
* Delete: Staff

### Session

* Create: Staff
* Read: Staff
* Update: Staff
* Delete: Staff

## Scenarios des cas d'utilisations

### Users

Cas d'utilisation commun à tous les utilisateur

CU1: S'authentifier
CU2: Consulter son profil

### Students

CU03: Créer son compte
CU04: Consulter les sessions
CU05: Visualiser l'historique des inscriptions
CU06: Visualiser l'historique des présences

### Teachers

CU07: Voir le planning
CU08: Visualiser liste des inscrits
CU09: Noter les présences

### Staff

CU10: gérer les comptes apprenants
CU11: gérer les comptes formateurs
CU12: gérer les salles
CU13: planifier session
CU14: modifier session
CU15: inscrire un apprenant
CU16: placer en liste attente
CU17: désinscrire apprenant
CU18: gérer les statuts (inscriptions et session)

### Admin

CU19: Créer les comptes Staff
CU20: activer/desactiver compte
CU21: Gérer les droits d'accès



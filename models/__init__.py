# models/__init__.py
# 1. Base (doit être importée en premier)
from .base import Base

# 2. Tables indépendantes (aucune clé étrangère)
from .access_level import AccessLevel
from .classroom import Classroom
from .job import Job
from .role import Role
from .study_level import StudyLevel

# 3. Tables dépendantes de niveau 1 (ex: User dépend de Role)
from .user import User

# 4. Tables dépendantes de niveau 2 (étendent ou lient User aux autres)
from .admin import Admin
from .staff import Staff
from .student import Student
from .teacher import Teacher

# 5. Tables dépendantes de niveau 3 (Session dépend de Classroom et Teacher)
from .session import Session

# 6. Table finale (Registration dépend de Student et Session)
from .registration import Registration
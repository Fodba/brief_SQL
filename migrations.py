from alembic.config import Config
from alembic import command


def migrer():
    # Charger la configuration depuis le fichier alembic.ini
    config = Config("alembic.ini")


def upgrade(config, level="head"):
    # Exécuter la migration (upgrade, downgrade, etc.)
    command.upgrade(config, level)


def downgrade(config, level):
    # Exécuter la migration (downgrade, downgrade, etc.)
    command.downgrade(config, level)

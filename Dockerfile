# Utiliser Python 3.13 comme base
FROM python:3.13

# Installer les dépendances nécessaires et Poetry
RUN apt-get update && apt-get install -y libpq-dev gcc git curl && \
    # Installer Poetry
    curl -sSL https://install.python-poetry.org | python3 -

# Ajouter Poetry au PATH
ENV PATH="/root/.local/bin:$PATH"

# Copier les fichiers de configuration Poetry
COPY pyproject.toml poetry.lock* /app/

# Définit le répertoire de travail
WORKDIR /app

# Copier tout le reste du code source
COPY . .

# Installer les dépendances via Poetry et lancer le bot
CMD sh -c "poetry install && poetry run python main.py"

# Documentation du Bot Discord

Ce projet consiste en un bot Discord développé en Python qui permet de réaliser trois fonctionnalités principales :

1. **Rechercher les 10 vidéos les plus pertinentes sur un thème choisi.**
2. **Récupération automatique des actualités technologiques chaque jour à 9h30.**
3. **Utiliser un modèle d'intelligence artificielle personnel via Llama 3.2.**

## Prérequis

Avant de pouvoir utiliser le bot, assurez-vous d'avoir les éléments suivants :

- **Python 3.x** installé sur votre machine. (**Poetry**)
- **Docker** et **Docker Compose** pour exécuter le projet dans un environnement conteneurisé.
- **Clés API** pour les services externes utilisés par le bot (par exemple, YouTube API, API de nouvelles, etc.).


- **DISCORD**: https://discord.com/developers/applications
- **YOUTUBE**: https://console.cloud.google.com/projectselector2/apis/dashboard
- **NEWSAPI**: https://newsapi.org/


## Installation

### Clonez le dépôt Git

Commencez par cloner ce dépôt sur votre machine locale :

```bash
git clone https://github.com/dlsptm/discord-bot-assistant.git
cd discord-bot-assistant
cp .env.dev .env
```

Ouvrez ensuite le fichier `.env` et remplissez les clés API nécessaires pour les services que vous utilisez.


# Lancer le bot avec Docker

Une fois que le fichier `.env` est correctement configuré, vous pouvez démarrer le projet à l'aide de Docker.
Exécutez la commande suivante pour construire et démarrer les services avec Docker Compose :

```bash
docker-compose up --build
```

# Fonctionnalités

**1. Recherche de vidéos pertinentes**

Le bot utilise un service pour rechercher les 10 vidéos les plus pertinentes sur un thème choisi. Il vous suffit de saisir le thème dans un canal Discord où le bot est présent, et il répondra avec une liste de vidéos.

**2. Recherche des actualités technologiques**

Le bot vous permet d'accéder aux actualités technologiques récentes en les résumant pour vous.
Un cron (planificateur) est configuré pour exécuter cette tâche tous les jours à 9h30, envoyant automatiquement les dernières nouvelles dans le canal Discord prévu à cet effet.
Cette fonctionnalité permet de rester informé sans même avoir à interagir avec le bot.

**3. Intégration de Llama 3.2 pour l'IA**

Le bot intègre Llama 3.2, un modèle d'intelligence artificielle que vous pouvez utiliser directement dans Discord pour interagir avec lui. Il vous suffit de lui poser des questions ou de lui donner des instructions, et Llama 3.2 vous répondra en fonction de son entraînement.



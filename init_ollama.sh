#!/bin/bash

# Démarre Ollama en arrière-plan
ollama serve &

# Attends que l'API soit disponible
sleep 10

# Tire le modèle llama3.2
echo "📦 Chargement du modèle llama3.2..."
ollama pull llama3.2

# Garde le conteneur vivant (ou relance proprement Ollama)
wait

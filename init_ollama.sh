#!/bin/bash

# Démarre Ollama en arrière-plan
ollama serve &

# Attends que l'API soit disponible
until curl -s http://localhost:11434 > /dev/null; do
  echo "⏳ En attente de Ollama..."
  sleep 1
done

# Tire le modèle llama3.2
echo "📦 Chargement du modèle llama3.2..."
ollama pull llama3.2

# Garde le conteneur vivant (ou relance proprement Ollama)
wait

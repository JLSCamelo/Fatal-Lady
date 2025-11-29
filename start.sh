#!/bin/bash

# Caminho do projeto
PROJECT_DIR="/home/vboxuser/Fatal-LadyTeste"

# Ativa o venv
cd $PROJECT_DIR
source venv/bin/activate

# Porta da sua aplicação
PORT=8000

# Inicia o FastAPI em background
echo "[INFO] Iniciando servidor FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload > server.log 2>&1 &

# Pega o PID
SERVER_PID=$!
echo "[INFO] Servidor iniciado com PID: $SERVER_PID"

# Espera 2 segundos pro servidor subir
sleep 2

# Inicia o LocalTunnel
echo "[INFO] Iniciando LocalTunnel..."
lt --port $PORT

#!/bin/bash

# Script para iniciar los servicios del proyecto
echo "🚀 Iniciando servicios del proyecto AI..."

# Verificar que Docker esté disponible
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está disponible. Verificando configuración..."
    echo "💡 Asegúrate de que Docker Desktop esté corriendo"
    exit 1
fi

echo "✅ Docker está disponible"

# Verificar que docker-compose esté disponible
if ! docker compose version > /dev/null 2>&1; then
    echo "❌ Docker Compose no está disponible"
    exit 1
fi

echo "✅ Docker Compose está disponible"

# Detener contenedores existentes si los hay
echo "🛑 Deteniendo contenedores existentes..."
docker compose down 2>/dev/null || true

# Construir y levantar los servicios
echo "🔨 Construyendo y levantando servicios..."
docker compose up -d --build

# Verificar que los servicios estén corriendo
echo "⏳ Esperando que los servicios estén listos..."
sleep 15

# Verificar estado de los contenedores
echo "📊 Estado de los contenedores:"
docker compose ps

echo "🎉 Servicios iniciados. Puedes acceder a:"
echo "   - API: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo "   - MongoDB: localhost:27017"
echo ""
echo "💡 Para ver logs: docker compose logs -f"
echo "💡 Para detener: docker compose down"


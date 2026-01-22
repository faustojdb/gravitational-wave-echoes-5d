#!/bin/bash
# Script para instalar dependencias para visual_sym.py

echo "🔧 Instalando dependencias para Klein visualization..."

# Activar entorno virtual si existe
if [ -d "klein_env" ]; then
    source klein_env/bin/activate
    echo "✅ Entorno virtual activado"
else
    echo "⚠️ No se encontró entorno virtual klein_env"
fi

# Instalar dependencias principales
pip install numpy matplotlib imageio pillow scipy

echo "✅ Dependencias instaladas exitosamente"
echo "📊 Ahora puedes ejecutar: python3 visual_sym.py"
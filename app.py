from flask import Flask, render_template, request, jsonify
import sqlite3
import uuid
from datetime import datetime
import os
from openai import OpenAI

app = Flask(__name__)
DB_NAME = "cotizaciones.db"

# Inicializa el cliente OpenAI con la clave tomada automáticamente de la variable de entorno
client = OpenAI()

print("Clave OpenAI usada:", client.api_key)


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS cotizaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE,
                nombre TEXT,
                email TEXT,
                tipo_servicio TEXT,
                precio REAL,
                fecha TEXT,
                descripcion TEXT
            )
        ''')

init_db()

def analizar_con_ia(descripcion, tipo_servicio):
    prompt = f"""
    Analiza este caso legal: {descripcion}
    Tipo de servicio: {tipo_servicio}

    Evalúa:
    1. Nivel de complejidad (Baja/Media/Alta)
    2. Recomendación de ajuste de precio (0%, 25%, 50%)
    3. Servicios adicionales sugeridos
    4. Genera una propuesta profesional para el cliente (2-3 párrafos)
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente legal profesional."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        texto_ia = response.choices[0].message.content
        return texto_ia
    except Exception as e:
        print(f"Error llamando a IA: {e}")
        return "Error al generar análisis con IA."

@app.route("/", methods=["GET"])
def formulario():
    return render_template("form.html")

@app.route("/cotizar", methods=["POST"])
def cotizar():
    data = request.form
    nombre = data.get("nombre")
    email = data.get("email")
    tipo = data.get("tipo_servicio")
    descripcion = data.get("descripcion")

    precios = {
        "Constitución de empresa": 1500,
        "Defensa laboral": 2000,
        "Consultoría tributaria": 800
    }

    precio = precios.get(tipo, 0)
    numero = f"COT-2025-{str(uuid.uuid4())[:8].upper()}"
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO cotizaciones (numero, nombre, email, tipo_servicio, precio, fecha, descripcion) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (numero, nombre, email, tipo, precio, fecha, descripcion)
        )

    propuesta_ia = analizar_con_ia(descripcion, tipo)

    resultado = {
        "numero": numero,
        "nombre": nombre,
        "email": email,
        "tipo_servicio": tipo,
        "precio": precio,
        "fecha": fecha,
        "descripcion": descripcion,
        "propuesta_ia": propuesta_ia
    }

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)

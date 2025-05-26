from flask import Flask, render_template, request, jsonify
import sqlite3
import uuid
from datetime import datetime
import os
import json
from openai import OpenAI

app = Flask(__name__)
DB_NAME = "cotizaciones.db"

# Obtiene la clave de entorno
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("No se encontró la variable de entorno OPENAI_API_KEY")

# Inicializa cliente OpenAI con la clave
client = OpenAI(api_key=api_key)
print("Clave OpenAI usada:", api_key)  # Confirmar en consola

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
    1. Complejidad (Baja/Media/Alta)
    2. Ajuste de precio recomendado (0%, 25%, 50%)
    3. Servicios adicionales necesarios
    4. Genera propuesta profesional para cliente (2-3 párrafos)

    Responde estrictamente en formato JSON con las siguientes claves:
    {{
      "complejidad": "...",
      "ajuste_precio": ...,
      "servicios_adicionales": [...],
      "propuesta_texto": "..."
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente legal profesional."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        texto_ia = response.choices[0].message.content.strip()

        # Limpiar bloque markdown si existe
        if texto_ia.startswith("```json"):
            texto_ia = texto_ia[len("```json"):].strip()
        if texto_ia.endswith("```"):
            texto_ia = texto_ia[:-len("```")].strip()

        resultado_json = json.loads(texto_ia)
        return resultado_json

    except json.JSONDecodeError:
        print("Error al parsear JSON. Respuesta IA:", texto_ia)
        return {
            "complejidad": None,
            "ajuste_precio": None,
            "servicios_adicionales": [],
            "propuesta_texto": texto_ia
        }
    except Exception as e:
        print(f"Error llamando a IA: {e}")
        return {
            "complejidad": None,
            "ajuste_precio": None,
            "servicios_adicionales": [],
            "propuesta_texto": "Error al generar análisis con IA."
        }

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

    resultado_ia = analizar_con_ia(descripcion, tipo)

    resultado = {
        "numero": numero,
        "nombre": nombre,
        "email": email,
        "tipo_servicio": tipo,
        "precio": precio,
        "fecha": fecha,
        "descripcion": descripcion,
        "complejidad": resultado_ia.get("complejidad"),
        "ajuste_precio": resultado_ia.get("ajuste_precio"),
        "servicios_adicionales": resultado_ia.get("servicios_adicionales"),
        "propuesta_texto": resultado_ia.get("propuesta_texto"),
    }

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import sqlite3
import uuid
from datetime import datetime

app = Flask(__name__)
DB_NAME = "cotizaciones.db"

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

    resultado = {
        "numero": numero,
        "nombre": nombre,
        "email": email,
        "tipo_servicio": tipo,
        "precio": precio,
        "fecha": fecha,
        "descripcion": descripcion
    }

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)

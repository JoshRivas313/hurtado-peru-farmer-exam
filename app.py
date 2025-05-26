from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import uuid

app = Flask(__name__)
DB_NAME = 'database.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS cotizaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT,
                nombre TEXT,
                email TEXT,
                tipo_servicio TEXT,
                precio REAL,
                fecha TEXT,
                descripcion TEXT
            )
        ''')

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        tipo_servicio = request.form['tipo_servicio']
        descripcion = request.form['descripcion']

        precios = {
            'Constitución de empresa': 1500,
            'Defensa laboral': 2000,
            'Consultoría tributaria': 800
        }

        precio = precios.get(tipo_servicio, 0)
        numero = f"COT-2025-{str(uuid.uuid4())[:8].upper()}"
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('''
                INSERT INTO cotizaciones (numero, nombre, email, tipo_servicio, precio, fecha, descripcion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (numero, nombre, email, tipo_servicio, precio, fecha, descripcion))

        return redirect(url_for('resultado', numero=numero))

    return render_template('form.html')

@app.route('/resultado/<numero>')
def resultado(numero):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute('SELECT * FROM cotizaciones WHERE numero = ?', (numero,))
        cotizacion = cursor.fetchone()

    if cotizacion:
        data = {
            'numero': cotizacion[1],
            'nombre': cotizacion[2],
            'email': cotizacion[3],
            'tipo_servicio': cotizacion[4],
            'precio': cotizacion[5],
            'fecha': cotizacion[6],
            'descripcion': cotizacion[7]
        }
        return render_template('resultado.html', cotizacion=data)
    else:
        return "Cotización no encontrada", 404

if __name__ == '__main__':
    app.run(debug=True)

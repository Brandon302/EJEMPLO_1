import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para las ventas de videojuegos
class Venta(db.Model):
    __tablename__ = 'ventas'
    id_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_juego = db.Column(db.String, nullable=False)
    plataforma = db.Column(db.String, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_venta = db.Column(db.DateTime, default=datetime.utcnow)

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

# Ruta raíz: listar ventas
@app.route('/')
def index():
    ventas = Venta.query.all()
    return render_template('index.html', ventas=ventas)

# Crear nueva venta
@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre_juego = request.form['nombre_juego']
        plataforma = request.form['plataforma']
        precio = float(request.form['precio'])
        cantidad = int(request.form['cantidad'])

        nueva_venta = Venta(
            nombre_juego=nombre_juego,
            plataforma=plataforma,
            precio=precio,
            cantidad=cantidad
        )
        db.session.add(nueva_venta)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('crear.html')

# Editar una venta
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    venta = Venta.query.get_or_404(id)
    if request.method == 'POST':
        venta.nombre_juego = request.form['nombre_juego']
        venta.plataforma = request.form['plataforma']
        venta.precio = float(request.form['precio'])
        venta.cantidad = int(request.form['cantidad'])
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', venta=venta)

# Eliminar una venta
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

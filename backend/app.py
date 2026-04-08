from flask import Flask, render_template, redirect, url_for, request, flash
<<<<<<< HEAD
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
import numpy as np
from sklearn.linear_model import LinearRegression
import os

# Importar configuración y base de datos
from config import Config
from database import db

# Crear aplicación
app = Flask(__name__)
app.config.from_object(Config)

# =============================
# IMPORTAR BLUEPRINT SERVICIOS
# =============================

from servicios import servicios_bp
app.register_blueprint(servicios_bp)
from sensores import sensores_bp
app.register_blueprint(sensores_bp)

from reportes import reportes_bp
app.register_blueprint(reportes_bp)

from alertas import alertas_bp
app.register_blueprint(alertas_bp)

from configuraciones import configuraciones_bp
app.register_blueprint(configuraciones_bp)

# Inicializar base de datos
db.init_app(app)

# Importar modelos DESPUÉS de init_app
from models import Usuario, Consumo

# Seguridad
=======
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# --- CONFIGURACIÓN DE SEGURIDAD Y BASE DE DATOS ---
# Usa una clave del sistema en la web, o una por defecto en local
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'clave_segura_ecovida_2026'

# Configuración dinámica de la base de datos (SQLite local / PostgreSQL web)
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///ecovida.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
>>>>>>> 006627f3f467490a9c67d9eaf0e27da417467c19
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

<<<<<<< HEAD

# =============================
# LOGIN MANAGER
# =============================

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# =============================
# REGISTRO
# =============================

@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')

        # Validar campos
        if not nombre or not correo or not password:
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('register'))

        # Verificar si ya existe
        exists = Usuario.query.filter_by(correo=correo).first()

        if exists:
            flash('El correo ya está registrado', 'danger')
            return redirect(url_for('register'))

        hashed_pw = bcrypt.generate_password_hash(
            password
        ).decode('utf-8')

        nuevo_usuario = Usuario(
            nombre=nombre,
            correo=correo,
            password=hashed_pw
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Cuenta creada con éxito', 'success')

        return redirect(url_for('login'))

    return render_template('register.html')

# =============================
# LOGIN
# =============================

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        correo = request.form.get('correo')
        password = request.form.get('password')

        user = Usuario.query.filter_by(correo=correo).first()

        if user and bcrypt.check_password_hash(
            user.password,
            password
        ):
            login_user(user)

            return redirect(url_for('index'))

        flash('Login fallido', 'danger')

    return render_template('login.html')


# =============================
# LOGOUT
# =============================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for('login'))


# =============================
# AGREGAR CONSUMO
# =============================

@app.route("/agregar_consumo", methods=['POST'])
@login_required
def agregar_consumo():

    energia = request.form.get('energia')
    agua = request.form.get('agua')
    residuos = request.form.get('residuos')

    if energia:

        nuevo_consumo = Consumo(
            usuario_id=current_user.id,
            fecha=np.datetime64('today'),
            energia=float(energia),
            agua=float(agua),
            residuos=float(residuos)
        )

        db.session.add(nuevo_consumo)
        db.session.commit()

    return redirect(url_for('index'))


# =============================
# DASHBOARD
# =============================

@app.route("/")
@login_required
def index():

    consumos = Consumo.query.filter_by(
        usuario_id=current_user.id
    ).all()

    datos = [c.energia for c in consumos]

    if not datos:

        return render_template(
            "index.html",
            promedio=0,
            maximo=0,
            minimo=0,
            prediccion=0,
            consumo=[]
        )

    promedio = round(np.mean(datos), 2)
    maximo = max(datos)
    minimo = min(datos)

    if len(datos) > 1:

        X = np.array(range(len(datos))).reshape(-1, 1)
        y = np.array(datos)

        modelo = LinearRegression()
        modelo.fit(X, y)

        prediccion = round(
            modelo.predict([[len(datos)]])[0],
            2
        )

    else:

        prediccion = datos[0]

    return render_template(
        "index.html",
        promedio=promedio,
        maximo=maximo,
        minimo=minimo,
        prediccion=prediccion,
        consumo=datos
    )


# =============================
# IR A SERVICIOS
# =============================

@app.route("/servicios")
@login_required
def ver_servicios():

    return redirect(
        url_for("servicios.listar_servicios")
    )


# =============================
# MANEJO DE ERRORES
# =============================

@app.errorhandler(404)
def pagina_no_encontrada(error):

    return "Página no encontrada", 404


@app.errorhandler(500)
def error_servidor(error):

    return "Error interno del servidor", 500


# =============================
# MAIN
# =============================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        print(
            "Base de datos EcoVida creada correctamente"
        )

=======
# --- MODELOS DE BASE DE DATOS ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    consumos = db.relationship('Consumo', backref='autor', lazy=True)

class Consumo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kwh = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- RUTAS DE AUTENTICACIÓN ---
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Verificar si el email ya existe
        exists = User.query.filter_by(email=request.form['email']).first()
        if exists:
            flash('El correo ya está registrado', 'danger')
            return redirect(url_for('register'))
            
        hashed_pw = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(empresa=request.form['empresa'], email=request.form['email'], password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Cuenta creada con éxito. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login fallido. Verifica correo y contraseña', 'danger')
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- ACCIONES DE DATOS ---
@app.route("/agregar_consumo", methods=['POST'])
@login_required
def agregar_consumo():
    dato_kwh = request.form.get('kwh')
    if dato_kwh:
        nuevo_registro = Consumo(kwh=float(dato_kwh), user_id=current_user.id)
        db.session.add(nuevo_registro)
        db.session.commit()
    return redirect(url_for('index'))

# --- DASHBOARD PRINCIPAL ---
@app.route("/")
@login_required
def index():
    # Obtener consumos específicos de la empresa logueada
    user_consumos = [c.kwh for c in current_user.consumos]
    
    if not user_consumos:
        return render_template("index.html", promedio=0, maximo=0, minimo=0, prediccion=0, alertas=[], consumo=[], empresa=current_user.empresa)

    # Cálculos estadísticos
    promedio = round(np.mean(user_consumos), 2)
    maximo = max(user_consumos)
    minimo = min(user_consumos)

    # IA: Predicción (Simple Linear Regression)
    # Solo predice si hay más de 1 dato
    if len(user_consumos) > 1:
        X = np.array(range(len(user_consumos))).reshape(-1, 1)
        y = np.array(user_consumos)
        modelo = LinearRegression().fit(X, y)
        prediccion = round(modelo.predict([[len(user_consumos)]])[0], 2)
    else:
        prediccion = user_consumos[0]

    # Alertas
    limite = 160
    alertas = [c for c in user_consumos if c > limite]

    return render_template(
        "index.html",
        promedio=promedio, maximo=maximo, minimo=minimo,
        prediccion=prediccion, alertas=alertas, consumo=user_consumos,
        empresa=current_user.empresa
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
>>>>>>> 006627f3f467490a9c67d9eaf0e27da417467c19
    app.run(debug=True)
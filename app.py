from flask import Flask, render_template, redirect, url_for, request, flash
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

# Inicializar base de datos y seguridad
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

db.init_app(app)

# Importar modelos
from models import Usuario, Consumo

# =============================
# IMPORTAR BLUEPRINTS
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

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

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

        if user and bcrypt.check_password_hash(user.password, password):
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

    app.run(debug=True)
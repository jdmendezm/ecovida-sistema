<<<<<<< HEAD
from database import db
from datetime import datetime
from flask_login import UserMixin

# =============================
# ROLES
# =============================

class Rol(db.Model):

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    descripcion = db.Column(
        db.String(200)
    )


# =============================
# USUARIOS
# =============================

class Usuario(UserMixin, db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    correo = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    activo = db.Column(
        db.Boolean,
        default=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    consumos = db.relationship(
        "Consumo",
        backref="usuario",
        lazy=True
    )

    roles = db.relationship(
        "Rol",
        secondary="usuario_roles",
        lazy="subquery"
    )


# =============================
# RELACION USUARIO - ROL
# =============================

class UsuarioRol(db.Model):

    __tablename__ = "usuario_roles"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id")
    )

    rol_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id")
    )


# =============================
# EDIFICIOS
# =============================

class Edificio(db.Model):

    __tablename__ = "edificios"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100))

    direccion = db.Column(db.String(200))

    tipo = db.Column(db.String(50))


# =============================
# SENSORES
# =============================

class Sensor(db.Model):

    __tablename__ = "sensores"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100))

    tipo = db.Column(db.String(50))

    edificio_id = db.Column(
        db.Integer,
        db.ForeignKey("edificios.id")
    )


# =============================
# CONSUMOS
# =============================

class Consumo(db.Model):

    __tablename__ = "consumo"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    fecha = db.Column(
        db.Date,
        nullable=False
    )

    energia = db.Column(
        db.Float,
        nullable=False
    )

    agua = db.Column(
        db.Float,
        nullable=False
    )

    residuos = db.Column(
        db.Float,
        nullable=False
    )


# =============================
# ALERTAS
# =============================

class Alerta(db.Model):

    __tablename__ = "alertas"

    id = db.Column(db.Integer, primary_key=True)

    tipo = db.Column(db.String(50))

    mensaje = db.Column(db.String(200))

    nivel = db.Column(db.String(20))

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    consumo_id = db.Column(
        db.Integer,
        db.ForeignKey("consumo.id")
    )


# =============================
# PREDICCIONES
# =============================

class Prediccion(db.Model):

    __tablename__ = "predicciones"

    id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.DateTime)

    valor_predicho = db.Column(db.Float)

    modelo = db.Column(db.String(100))


# =============================
# RECOMENDACIONES
# =============================

class Recomendacion(db.Model):

    __tablename__ = "recomendaciones"

    id = db.Column(db.Integer, primary_key=True)

    descripcion = db.Column(db.String(300))

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ==============================
# SERVICIOS TI
# ==============================

class ServicioTI(db.Model):

    __tablename__ = "servicios_ti"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    descripcion = db.Column(
        db.String(200),
        nullable=False
    )

    estado = db.Column(
        db.String(50),
        default="Abierto"
    )

    prioridad = db.Column(
        db.String(50),
        nullable=False
    )

    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # IMPORTANTE:
    # cada empresa (usuario) tendrá sus servicios

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )


# =============================
# INCIDENTES
# =============================

class Incidente(db.Model):

    __tablename__ = "incidentes"

    id = db.Column(db.Integer, primary_key=True)

    descripcion = db.Column(db.String(300))

    prioridad = db.Column(db.String(50))

    estado = db.Column(db.String(50))

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =============================
# LOGS DEL SISTEMA
# =============================

class LogSistema(db.Model):

    __tablename__ = "logs_sistema"

    id = db.Column(db.Integer, primary_key=True)

    accion = db.Column(db.String(200))

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id")
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

=======
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Relación: Un usuario (empresa) tiene muchos registros de consumo
    consumos = db.relationship('Consumo', backref='propietario', lazy=True)

class Consumo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kwh = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
>>>>>>> 006627f3f467490a9c67d9eaf0e27da417467c19

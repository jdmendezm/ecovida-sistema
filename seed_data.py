from database import db
from models import Rol, Usuario, UsuarioRol

def crear_datos_iniciales():

    # Crear roles
    admin = Rol(nombre="Administrador")
    tecnico = Rol(nombre="Tecnico")
    usuario = Rol(nombre="Usuario")

    db.session.add_all([
        admin,
        tecnico,
        usuario
    ])

    db.session.commit()

    # Crear usuario admin

    admin_user = Usuario(
        nombre="Admin",
        correo="admin@ecovida.com",
        password="admin123"
    )

    db.session.add(admin_user)
    db.session.commit()

    # Asignar rol

    relacion = UsuarioRol(
        usuario_id=admin_user.id,
        rol_id=admin.id
    )

    db.session.add(relacion)
    db.session.commit()

    print("Datos iniciales creados correctamente")
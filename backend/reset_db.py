from app import app
from database import db
from sqlalchemy import text

with app.app_context():

    print("Eliminando todas las tablas con CASCADE...")

    db.session.execute(
        text("DROP SCHEMA public CASCADE;")
    )

    db.session.execute(
        text("CREATE SCHEMA public;")
    )

    db.session.commit()

    print("Creando tablas nuevas...")

    db.create_all()

    print("Base de datos reiniciada correctamente")
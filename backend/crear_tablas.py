from app import app
from database import db

with app.app_context():
    db.drop_all()     # BORRA las tablas
    db.create_all()   # CREA las tablas nuevas
    print("Tablas creadas correctamente")
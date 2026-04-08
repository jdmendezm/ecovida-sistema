from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Sensor

sensores_bp = Blueprint(
    "sensores",
    __name__,
    url_prefix="/sensores"
)

# =============================
# LISTAR
# =============================

@sensores_bp.route("/listar_sensores")
@login_required
def listar_sensores():

    sensores = Sensor.query.all()

    return render_template(
        "sensores/listar_sensores.html",
        sensores=sensores
    )


# =============================
# CREAR
# =============================

@sensores_bp.route(
    "/crear",
    methods=["GET", "POST"]
)
@login_required
def crear_sensor():

    if request.method == "POST":

        nombre = request.form.get("nombre")
        tipo = request.form.get("tipo")
        ubicacion = request.form.get("ubicacion")

        nuevo = Sensor(
            nombre=nombre,
            tipo=tipo,
            ubicacion=ubicacion,
            usuario_id=current_user.id
        )

        db.session.add(nuevo)
        db.session.commit()

        flash(
            "Sensor creado correctamente",
            "success"
        )

        return redirect(
            url_for("sensores.listar_sensores")
        )

    return render_template(
        "sensores/crear_sensor.html"
    )
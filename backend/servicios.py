from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from database import db
from models import ServicioTI

# Crear Blueprint
servicios_bp = Blueprint(
    "servicios",
    __name__
)


# =============================
# LISTAR SERVICIOS
# =============================

@servicios_bp.route("/listar_servicios")
@login_required
def listar_servicios():

    servicios = ServicioTI.query.filter_by(
        usuario_id=current_user.id
    ).all()

    return render_template(
        "listar_servicios.html",
        servicios=servicios
    )


# =============================
# CREAR SERVICIO
# =============================

@servicios_bp.route(
    "/crear_servicio",
    methods=["GET", "POST"]
)
@login_required
def crear_servicio():

    if request.method == "POST":

        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        estado = request.form.get("estado")
        prioridad = request.form.get("prioridad")  # ← FALTABA

        # Validación básica profesional
        if not prioridad:
            flash(
                "Debe seleccionar una prioridad",
                "danger"
            )
            return redirect(
                url_for(
                    "servicios.crear_servicio"
                )
            )

        nuevo_servicio = ServicioTI(
            nombre=nombre,
            descripcion=descripcion,
            estado=estado,
            prioridad=prioridad,  # ← IMPORTANTE
            usuario_id=current_user.id
        )

        db.session.add(nuevo_servicio)
        db.session.commit()

        flash(
            "Servicio creado correctamente",
            "success"
        )

        return redirect(
            url_for(
                "servicios.listar_servicios"
            )
        )

    return render_template(
        "crear_servicio.html"
    )


# =============================
# EDITAR SERVICIO
# =============================

@servicios_bp.route(
    "/editar_servicio/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar_servicio(id):

    servicio = ServicioTI.query.get_or_404(id)

    # Verificar que el servicio pertenece al usuario
    if servicio.usuario_id != current_user.id:

        flash(
            "No tienes permiso para editar este servicio",
            "danger"
        )

        return redirect(
            url_for(
                "servicios.listar_servicios"
            )
        )

    if request.method == "POST":

        servicio.nombre = request.form.get("nombre")
        servicio.descripcion = request.form.get("descripcion")
        servicio.estado = request.form.get("estado")

        db.session.commit()

        flash(
            "Servicio actualizado correctamente",
            "success"
        )

        return redirect(
            url_for(
                "servicios.listar_servicios"
            )
        )

    return render_template(
        "editar_servicio.html",
        servicio=servicio
    )


# =============================
# ELIMINAR SERVICIO
# =============================

@servicios_bp.route(
    "/eliminar_servicio/<int:id>"
)
@login_required
def eliminar_servicio(id):

    servicio = ServicioTI.query.get_or_404(id)

    # Verificar que pertenece al usuario
    if servicio.usuario_id != current_user.id:

        flash(
            "No tienes permiso para eliminar este servicio",
            "danger"
        )

        return redirect(
            url_for(
                "servicios.listar_servicios"
            )
        )

    db.session.delete(servicio)
    db.session.commit()

    flash(
        "Servicio eliminado correctamente",
        "success"
    )

    return redirect(
        url_for(
            "servicios.listar_servicios"
        )
    )
    



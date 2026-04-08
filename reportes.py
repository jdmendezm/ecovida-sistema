from flask import Blueprint, render_template
from flask_login import login_required
from models import ServicioTI

reportes_bp = Blueprint(
    "reportes",
    __name__,
    url_prefix="/reportes"
)

@reportes_bp.route("/")
@login_required
def ver_reportes():

    total = ServicioTI.query.count()

    activos = ServicioTI.query.filter_by(
        estado="Activo"
    ).count()

    return render_template(
        "reportes/listar_reportes.html",
        total=total,
        activos=activos
    )
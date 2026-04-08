from flask import Blueprint, render_template
from flask_login import login_required

configuraciones_bp = Blueprint(
    "configuraciones",
    __name__,
    url_prefix="/configuraciones"
)

@configuraciones_bp.route("/")
@login_required
def configuracion():

    return render_template(
        "configuraciones/listar_configuraciones.html"
    )
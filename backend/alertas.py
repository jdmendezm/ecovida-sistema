from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Alerta

alertas_bp = Blueprint(
    "alertas",
    __name__,
    url_prefix="/alertas"
)

@alertas_bp.route("/")
@login_required
def listar_alertas():

    alertas = Alerta.query.filter_by(
        usuario_id=current_user.id
    ).all()

    return render_template(
        "alertas/listar_alertas.html",
        alertas=alertas
    )
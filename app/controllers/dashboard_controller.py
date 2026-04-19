from flask import Blueprint, render_template
from app.controllers.auth_controller import login_required
from app.utils.decorators import role_required

bp = Blueprint('/', __name__, url_prefix='/')

@bp.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')
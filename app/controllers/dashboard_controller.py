from flask import Blueprint, render_template, request, redirect
from app.controllers.auth_controller import login_required

bp = Blueprint('/', __name__, url_prefix='/')

@bp.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')
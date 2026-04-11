from flask import Flask
from app.controllers.dashboard_controller import bp as dashboard_bp
from app.controllers.employee_controller import bp as employee_bp
from app.controllers.auth_controller import bp as auth_bp
from app.controllers.attendance_controller import bp as attendance_bp
from app.controllers.payroll_controller import bp as controller_bp

from app.utils.format import format_rupiah

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.jinja_env.filters['rupiah'] = format_rupiah

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(controller_bp)

    return app
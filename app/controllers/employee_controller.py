from flask import Blueprint, render_template, request, redirect,session
from app.models.employee import Employee
from app.controllers.auth_controller import login_required
from app.utils.decorators import role_required

bp = Blueprint('employee', __name__, url_prefix='/employees')

@bp.route('/')
@login_required
@role_required(['admin', 'hr'])
def index():
    print(session.get('role'))
    employees = Employee.get_all()
    return render_template('employees/index.html', employees=employees)

@bp.route('/create', methods=['POST'])
@login_required
@role_required(['admin', 'hr'])
def create():
    data = request.form
    Employee.create(data)
    return redirect('/employees')

@bp.route('/save', methods=['POST'])
@login_required
@role_required(['admin', 'hr'])
def save():
    data = request.form.to_dict()

    data['gaji_pokok'] = request.form['gaji_pokok'].replace('.', '')
    data['tunj_jabatan'] = request.form['tunj_jabatan'].replace('.', '')
    data['tunj_makan'] = request.form['tunj_makan'].replace('.', '')
    data['tunj_transport'] = request.form['tunj_transport'].replace('.', '')
    data['premi_kehadiran'] = request.form['premi_kehadiran'].replace('.', '')

    if data.get('id'):  # UPDATE
        Employee.update(data)
    else:  # INSERT
        Employee.create(data)

    return redirect('/employees')


@bp.route('/delete/<int:id>')
@login_required
@role_required(['admin', 'hr'])
def delete(id):
    Employee.delete(id)
    return redirect('/employees')
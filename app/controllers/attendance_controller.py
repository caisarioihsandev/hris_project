from flask import Blueprint, render_template, request, redirect
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.controllers.auth_controller import login_required

bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@bp.route('/')
def index():
    data = Attendance.get_all()
    employees = Employee.get_all()
    return render_template('attendance/index.html', data=data, employees=employees)


@bp.route('/save', methods=['POST'])
@login_required
def save():
    data = request.form.to_dict()

    data['check_in'] = request.form.get('check_in')
    data['check_out'] = request.form.get('check_out')

    if data.get('id'):  # UPDATE
        Attendance.update(data)
    else:  # INSERT
        Attendance.create(data)

    return redirect('/attendance')

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    Attendance.delete(id)
    return redirect('/attendance')
from flask import Blueprint, make_response, render_template, request, redirect, url_for, jsonify
from app.models.payroll import Payroll
from app.models.employee import Employee
from weasyprint import HTML


bp = Blueprint('payroll', __name__, url_prefix='/payroll')

@bp.route('/')
def index():
    data = Payroll.get_all()
    employees = Employee.get_all()
    return render_template('payroll/index.html', data=data, employees=employees)

@bp.route('/get-karyawan/<int:id>')
def get_karyawan(id):
    employee = Employee.get_karyawan(id)
    return jsonify(employee) # mengkonversi data menjadi json agar dapat ditarik di script

@bp.route('/save', methods=['POST'])
def save():
    data = request.form.to_dict()

    if data.get('id'):  # UPDATE
        Payroll.update(data)
    else:  # INSERT
        Payroll.create(data)

    Payroll.create(data)
    return redirect(url_for('payroll.index'))


@bp.route('/update', methods=['POST'])
def update():
    data = request.form.to_dict()
    Payroll.update(data)
    return redirect(url_for('payroll.index'))

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    Payroll.delete(id)
    return redirect(url_for('payroll.index'))

@bp.route('/slip/<int:id>')
def slip(id):
    data = Payroll.get_one(id)

    html = render_template('payroll/slip.html', data=data)

    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=slip_gaji.pdf'

    return response
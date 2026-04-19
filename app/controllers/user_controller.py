from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.controllers.auth_controller import login_required
from app.utils.decorators import role_required

bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('/')
@login_required
@role_required(['admin'])
def index():
    users = User.get_all()
    return render_template('users/index.html', users=users)


@bp.route('/save', methods=['POST'])
@login_required
@role_required(['admin'])
def save():
    data = request.form.to_dict()
    
    if data['password'] != data['confirm']:
        flash('Password tidak sama!')
    
    data['password'] = generate_password_hash(request.form['password'])

    if data.get('id'):
        User.update(data)
        flash('User berhasil diupdate', 'success')
    else:
        User.create(data)
        flash('User berhasil ditambahkan', 'success')

    return redirect(url_for('user.index'))


@bp.route('/delete/<int:id>')
@login_required
@role_required(['admin'])
def delete(id):
    User.delete(id)
    flash('User berhasil dihapus', 'danger')
    return redirect(url_for('user.index'))
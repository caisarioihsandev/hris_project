from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

# REGISTER
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()

        if data['password'] != data['confirm']:
            flash('Password tidak sama!')
            return redirect('/auth/register')

        if User.find_by_username(data['username']):
            flash('Username sudah digunakan!')
            return redirect('/auth/register')

        data['password'] = generate_password_hash(data['password'])
        User.create(data)

        flash('Registrasi berhasil!')
        return redirect('/auth/login')

    return render_template('auth/register.html')


# LOGIN
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()

        user = User.find_by_username(data['username'])

        if user and check_password_hash(user['password'], data['password']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

            return redirect('/')  # redirect ke dashboard
        else:
            flash('Username atau password salah!')

    return render_template('auth/login.html')


# LOGOUT
@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/auth/login')

# Middleware Login Required
import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/auth/login')
        return view(*args, **kwargs)
    return wrapped_view
from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('auth.login'))

            if session.get('role') not in roles:
                flash('Akses ditolak!', 'danger')
                return redirect(url_for('dashboard.index'))

            return f(*args, **kwargs)
        return wrapped
    return decorator
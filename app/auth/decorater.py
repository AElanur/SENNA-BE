from functools import wraps
from flask import request, jsonify, g

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_key = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = g.user_service.validate_session(session_key)
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(user_id=user_id, *args, **kwargs)
    return decorated_function

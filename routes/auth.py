from flask import Blueprint, request, jsonify
from models.user import User
from flask_login import login_manager, current_user, login_required, login_user, logout_user
from repository.database import db

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

login_manager.login_view = 'login'

@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.json
  email = data.get('email')
  password = data.get('password')

  if not email or not password:
    return jsonify({'error': 'Invalid data'}), 400

  user = User.query.filter(User.email == email).first()

  print('User found:', user)

  if not user or not user.password == password:
    return jsonify({'error': 'Invalid credentials'}), 401
  
  login_user(user)
  return jsonify({'message': 'Logged in successfully'}), 200

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
  try:
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password= data.get('password')

    if not name or not email or not password:
      return jsonify({'error': 'Invalid data'}), 400
    
    if User.query.filter(User.email == email).first():
      return jsonify({'error': 'Email already exists'}), 400
    
    user = User(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': f"User {name} registered successfully"}), 201
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
  user = current_user
  return jsonify({
    'id': user.id,
    'name': user.name,
    'email': user.email,
    'created_at': user.created_at,
    'updated_at': user.updated_at
  }), 200


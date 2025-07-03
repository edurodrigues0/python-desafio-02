from models.user import User
from flask import Flask, request, jsonify
from repository.database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.filter(User.id == user_id).first()

@app.route('/login', methods=['POST'])
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

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/register', methods=['POST'])
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

@app.route('/me', methods=['GET'])
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

@app.route('/hello', methods=['GET'])
def hello():
  return jsonify({'message': 'hello world'})

if __name__ == '__main__':
  app.run(debug=True)
from models.user import User
from models.diet import Diet

from flask import Flask, request, jsonify
from repository.database import db
from flask_login import LoginManager
from routes.auth import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
  return User.query.filter(User.id == user_id).first()


@app.route('/hello', methods=['GET'])
def hello():
  return jsonify({'message': 'hello world'})

if __name__ == '__main__':
  app.run(debug=True)
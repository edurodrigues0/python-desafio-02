from flask import Blueprint, request, jsonify
from models.diet import Diet
from flask_login import login_required, current_user
from repository.database import db
from datetime import datetime

diet_bp = Blueprint('diet_bp', __name__, url_prefix='/diets')

@diet_bp.route('/', methods=['POST'])
@login_required
def create_diet():
  data = request.json
  name = data.get('name')
  description = data.get('description')
  on_diet = data.get('on_diet', True)
  date_hour = data.get('date_hour')

  if not name or not date_hour:
    return jsonify({'error': 'Invalid data'}), 400
  
  try:
    date_hour = datetime.fromisoformat(date_hour)
  except (TypeError, ValueError):
    return jsonify({'error': 'Invalid date format, use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400

  user = current_user

  diet = Diet(name=name,
              description=description,
              on_diet=on_diet,
              date_hour=date_hour,
              user_id=user.id
            )
  db.session.add(diet)
  db.session.commit()
  return jsonify({'message': f'Diet {name} created successfully'})

@diet_bp.route('/', methods=['GET'])
@login_required
def get_diets():
  user = current_user
  diets = Diet.query.filter(Diet.user_id == user.id).all()

  return jsonify([diet.to_dict() for diet in diets]), 200
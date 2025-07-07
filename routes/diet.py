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
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', 10, type=int)

  if page < 1 or per_page < 1:
    return jsonify({'error': 'Invalid pagination parameters'}), 400
  
  offset = (page - 1) * per_page
  diets = Diet.query.filter(Diet.user_id == user.id).offset(offset).limit(per_page).all()
  total_diets = Diet.query.filter(Diet.user_id == user.id).count()

  diets_list = [diet.to_dict() for diet in diets]

  return jsonify({
    'diets': diets_list,
    'total_count_diets': total_diets,
    'page': page,
    'per_page': per_page
  }), 200

@diet_bp.route('/<int:diet_id>', methods=['GET'])
@login_required
def get_diet(diet_id):
  diet = Diet.query.get_or_404(diet_id)

  if diet.user_id != current_user.id:
    return jsonify({'error': 'Unauthorized access'}), 403

  return jsonify(diet.to_dict()), 200

@diet_bp.route('/<int:diet_id>', methods=['PUT'])
@login_required
def update_diet(diet_id):
  data = request.json
  name = data.get('name')
  description = data.get('description')
  on_diet = data.get('on_diet')
  date_hour = data.get('date_hour')

  print('Received data for update:', data)

  diet = Diet.query.get_or_404(diet_id)

  if diet.user_id != current_user.id:
    return jsonify({'error': 'Unauthorized access'}), 403

  if name is not None:
    diet.name = name
  if description is not None:
    diet.description = description
  if on_diet is not None:
    diet.on_diet = on_diet
  if date_hour is not None:
    try:
      diet.date_hour = datetime.fromisoformat(date_hour)
    except (TypeError, ValueError):
      return jsonify({'error': 'Invalid date format, use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
  db.session.commit()

  return jsonify({'message': f'Diet {diet.name} updated successfully'})

@diet_bp.route('/<int:diet_id>', methods=['DELETE'])
@login_required
def delete_diet(diet_id):
  diet = Diet.query.get_or_404(diet_id)

  if diet.user_id != current_user.id:
    return jsonify({'error': 'Unauthorized access'}), 403
  
  db.session.delete(diet)
  db.session.commit()

  return jsonify({'message': f'Diet {diet.name} deleted successfully'}), 200
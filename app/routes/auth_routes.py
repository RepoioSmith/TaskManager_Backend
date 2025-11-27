from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User

# Usamos 'auth_bp' para mantener consistencia con __init__.py
auth_bp = Blueprint('auth_bp', __name__)

# --- Rutas de Autenticación (Login/Register) ---

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validaciones: Ahora verificamos 'nombre' en lugar de 'username'
    if not data or not data.get('email') or not data.get('password') or not data.get('nombre'):
        return jsonify({"msg": "Faltan datos obligatorios"}), 400

    if User.find_by_email(data['email']):
        return jsonify({"msg": "El usuario ya existe"}), 400

    if len(data['password']) < 6:
        return jsonify({"msg": "La contraseña debe tener al menos 6 caracteres"}), 400

    try:
        # Llamamos al modelo pasando 'nombre'
        user_id = User.create_user(data['nombre'], data['email'], data['password'])
        return jsonify({"msg": "Usuario creado exitosamente", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"msg": "Error interno", "error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Faltan datos"}), 400

    user = User.find_by_email(data['email'])

    # Validamos usando el método del modelo
    if user and User.check_password(user['password'], data['password']):
        access_token = create_access_token(identity=str(user['_id']))
        # Devolvemos 'nombre' en la respuesta del login
        return jsonify({"access_token": access_token, "nombre": user['nombre']}), 200

    return jsonify({"msg": "Credenciales inválidas"}), 401

# --- Rutas de Gestión de Usuarios (CRUD Extra) ---

#
@auth_bp.route('/', methods=['GET'])
@jwt_required()
def get_all():
    # Convertimos ObjectId a string para que sea serializable en JSON
    users = User.get_all_users()
    for user in users:
        user['_id'] = str(user['_id'])
        if 'password' in user: del user['password'] # No devolver passwords por seguridad
    return jsonify(users), 200

@auth_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_one(user_id):
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    
    user['_id'] = str(user['_id'])
    if 'password' in user: del user['password']
    return jsonify(user), 200

@auth_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_one(user_id):
    current_user_id = get_jwt_identity()
    
    # Solo el propio usuario puede borrarse a sí mismo (seguridad básica)
    if current_user_id != user_id:
        return jsonify({"msg": "No autorizado para eliminar este usuario"}), 403

    User.delete_user(user_id)
    return jsonify({"msg": "Usuario eliminado"}), 200

@auth_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_one(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"msg": "No autorizado"}), 403
    
    data = request.get_json()
    # Filtramos solo lo que permitimos editar
    update_data = {}
    
    # Aquí también cambiamos username por nombre
    if 'nombre' in data: update_data['nombre'] = data['nombre']
    if 'password' in data: update_data['password'] = data['password'] # El modelo se encarga de hashear

    if not update_data:
        return jsonify({"msg": "Nada que actualizar"}), 400

    User.update_user(user_id, update_data)
    return jsonify({"msg": "Usuario actualizado"}), 200
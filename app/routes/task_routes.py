from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.tasks import Task

task_bp= Blueprint('task_bp', __name__)

#Obtener todas las tareas del usuario autenticado
@task_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id= get_jwt_identity()
    tasks= Task.get_by_user(current_user_id)

    output=[]
    for task in tasks:
        task['_id']= str(task['_id'])
        task['user_id']= str(task['user_id'])
        output.append(task)

    return jsonify(output), 200

#Crear una nueva tarea
@task_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    current_user_id= get_jwt_identity()
    data= request.get_json()

    if not data or not data.get('title'):
        return jsonify({"msg": "Faltan datos obligatorios"}), 400
    try:
        task_id=Task.create_task(
            title=data['title'],
            description=data.get('description', ''),
            user_id=current_user_id
        )
        return jsonify({"msg": "Tarea creada", "task_id": task_id}), 201
    except Exception as e:
        return jsonify({"msg": "Error al crear tarea", "error": str(e)}), 500

#Actualizar una tarea
@task_bp.route('/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user_id=get_jwt_identity()
    data=request.get_json()

    task= Task.get_by_id(task_id)
    if not task:
        return jsonify({"msg": "Tarea no encontrada"}), 404
    if str(task['user_id']) != current_user_id:
        return jsonify({"msg": "No autorizado"}), 403
    if Task.update_task(task_id, data):
        return jsonify({"msg": "Tarea actualizada"}), 200
    else:
        return jsonify({"msg": "No hubo cambios"}), 200
    
@task_bp.route('/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user_id=get_jwt_identity()
    task= Task.get_by_id(task_id)
    if not task:
        return jsonify({"msg": "Tarea no encontrada"}), 404
    if str(task['user_id']) != current_user_id:
        return jsonify({"msg": "No autorizado"}), 403
    if Task.delete_task(task_id):
        return jsonify({"msg": "Tarea eliminada"}), 200
    else:
        return jsonify({"msg": "Error al eliminar tarea"}), 500
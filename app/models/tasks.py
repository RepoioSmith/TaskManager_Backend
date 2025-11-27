from app import mongo
from bson import ObjectId
from datetime import datetime

class Task:
    @staticmethod
    def create_task(title, description, user_id):
        task_doc = {
            "title": title,
            "description": description,
            "status": "pending",  # Estado por defecto
            "user_id": ObjectId(user_id), # Importante: Guardar como ObjectId para relacionar
            "created_at": datetime.utcnow()
        }
        # CORRECCIÓN: Usamos mongo.cx.get_database() para evitar errores de conexión
        result = mongo.db.tasks.insert_one(task_doc) 
        return str(result.inserted_id)

    @staticmethod
    def get_by_user(user_id):
        # Buscamos todas las tareas que tengan el ID del usuario
        return list(mongo.cx.get_database().tasks.find({"user_id": ObjectId(user_id)}))

    @staticmethod
    def get_by_id(task_id):
        try:
            return mongo.cx.get_database().tasks.find_one({"_id": ObjectId(task_id)})
        except:
            return None

    @staticmethod
    def update_task(task_id, data):
        # Filtramos solo los campos permitidos
        update_fields = {}
        if 'title' in data: update_fields['title'] = data['title']
        if 'description' in data: update_fields['description'] = data['description']
        if 'status' in data: update_fields['status'] = data['status']
        
        if not update_fields:
            return False

        result = mongo.cx.get_database().tasks.update_one(
            {"_id": ObjectId(task_id)}, 
            {"$set": update_fields}
        )
        return result.modified_count > 0

    @staticmethod
    def delete_task(task_id):
        result = mongo.cx.get_database().tasks.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0
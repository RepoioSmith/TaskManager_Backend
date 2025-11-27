from app import mongo, bcrypt
from bson import ObjectId

class User:
    @staticmethod
    def create_user(nombre, email, password):
        # Hasheamos la contraseña
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        user_doc = {
            "nombre": nombre,  # Usamos 'nombre' como pediste
            "email": email,
            "password": hashed_password,
            "tasks": [] 
        }
        # Usamos cx.get_database() para evitar el error 'NoneType'
        result = mongo.cx.get_database().users.insert_one(user_doc)
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email):
        # Corrección crítica: mongo.cx.get_database() es más seguro que mongo.db
        return mongo.cx.get_database().users.find_one({"email": email})

    @staticmethod
    def check_password(stored_password_hash, password_attempt):
        return bcrypt.check_password_hash(stored_password_hash, password_attempt)

    @staticmethod
    def get_all_users():
        return list(mongo.cx.get_database().users.find())

    @staticmethod
    def get_by_id(user_id):
        try:
            return mongo.cx.get_database().users.find_one({"_id": ObjectId(user_id)})
        except:
            return None

    @staticmethod
    def delete_user(user_id):
        db = mongo.cx.get_database()
        db.tasks.delete_many({"user_id": user_id}) 
        return db.users.delete_one({"_id": ObjectId(user_id)})

    @staticmethod
    def update_user(user_id, data):
        if 'password' in data:
            data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            
        return mongo.cx.get_database().users.update_one({"_id": ObjectId(user_id)}, {"$set": data})
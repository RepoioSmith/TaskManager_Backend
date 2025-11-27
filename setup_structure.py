import os

def create_structure():
    # Definición de la estructura
    structure = {
        "app": [
            "__init__.py",
            "config.py",
        ],
        "app/models": [
            "__init__.py",
            "user.py",
            "task.py"
        ],
        "app/routes": [
            "__init__.py",
            "auth_routes.py",
            "task_routes.py"
        ],
        "app/utils": [
            "__init__.py",
            "validators.py"
        ],
        ".": [ # Raíz
            ".env",
            ".gitignore",
            "run.py",
            "requirements.txt",
            "README.md"
        ]
    }

    print("🚀 Creando estructura del proyecto Task Manager...")

    for folder, files in structure.items():
        # Crear carpeta si no es la raíz y no existe
        if folder != "." and not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 Carpeta creada: {folder}")
        
        # Crear archivos
        for file in files:
            path = os.path.join(folder, file)
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    # Contenido inicial básico para ciertos archivos
                    if file == ".gitignore":
                        f.write("venv/\n.env\n__pycache__/\n*.pyc")
                    elif file == "requirements.txt":
                        f.write("Flask\nflask-pymongo\nflask-jwt-extended\npython-dotenv\nflask-cors")
                    elif file == ".env":
                        f.write("MONGO_URI=mongodb://localhost:27017/taskmanager\nJWT_SECRET_KEY=cambia_esto_por_una_clave_secreta")
                    else:
                        pass # Archivo vacío
                print(f"📄 Archivo creado: {path}")
            else:
                print(f"⚠️  El archivo ya existe: {path}")

    print("\n✅ ¡Estructura creada exitosamente!")
    print("👉 Siguientes pasos:")
    print("1. Crea tu entorno virtual: python -m venv venv")
    print("2. Actívalo e instala dependencias: pip install -r requirements.txt")

if __name__ == "__main__":
    create_structure()
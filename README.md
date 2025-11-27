# 📝 Task Manager Backend

Este es el backend para una aplicación de gestión de tareas (Task Manager). Está construido con **Python** y **Flask**, utilizando **MongoDB** (Atlas) como base de datos y **JWT** para la autenticación segura.

## 🚀 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

* **Python 3.x**
* **Git** (Opcional, para clonar el repositorio)
* Una cuenta y un clúster activo en **MongoDB Atlas**.

## 🛠️ Instalación y Configuración

Sigue estos pasos para configurar el proyecto en tu máquina local:

### 1. Clonar el repositorio (o descargar el código)
```
bash
git clone <URL_DEL_TU_REPOSITORIO>
cd taskmanager_backend
```

### 2. Crear un entorno virtual
```
Es recomendable usar un entorno virtual para aislar las dependencias.

Windows:
    python -m venv venv
    .\venv\Scripts\activate

macOS / Linux:
    python3 -m venv venv
    source venv/bin/activate
```
### 3. Instalar dependencias
```
Instala todas las librerías necesarias listadas en requirements.txt:
    pip install -r requirements.txt

⚙️ Configuración de Variables de Entorno (.env)
Este es el paso más importante para conectar tu base de datos correctamente.

Crea un archivo llamado .env en la raíz del proyecto (al mismo nivel que run.py).

Copia el siguiente contenido y reemplaza con tus datos reales:
    # Configuración de MongoDB Atlas
    # IMPORTANTE: Asegúrate de incluir "/taskmanager" después de "mongodb.net" y antes del "?"
    MONGO_URI=mongodb+srv://<TU_USUARIO>:<TU_CONTRASEÑA>@<TU_CLUSTER>.mongodb.net/taskmanager?retryWrites=true&w=majority

    # Clave secreta para firmar los tokens JWT (Cámbiala por una cadena larga y segura)
    JWT_SECRET_KEY=super-secreto-cambiar-esto-en-produccion

⚠️ Nota sobre MongoDB: Si tu conexión falla con No default database defined, verifica que tu MONGO_URI termine con el nombre de la base de datos (ej: /taskmanager) antes de los parámetros de consulta.
```

### ▶️ Ejecución
```
Una vez configurado el .env y activado el entorno virtual, corre el servidor:
    python run.py
Deberías ver algo como: * Running on http://127.0.0.1:5000
```
📡 Endpoints de la API
Aquí tienes una lista rápida para probar en Postman.

🔐 Autenticación (/api/auth)

```
POST	/register	Registrar nuevo usuario	{"nombre": "...", "email": "...", "password": "..."}
POST	/login	Iniciar sesión	{"email": "...", "password": "..."}
```
Nota: Al hacer login, recibirás un access_token. Copiálo, lo necesitarás para las rutas de tareas.

📋 Tareas (/api/tasks)
Requiere Header: Authorization: Bearer <TU_TOKEN>
```
GET	/	Ver todas mis tareas	N/A
POST	/	Crear tarea	{"title": "...", "description": "..."}
PUT	/<id>	Actualizar tarea	{"title": "...", "status": "completed"}
DELETE	/<id>	Eliminar tarea	N/A
```

📂 Estructura del Proyecto
```
taskmanager_backend/
├── app/
│   ├── __init__.py      # Inicialización de Flask y plugins (Mongo, JWT, Bcrypt)
│   ├── config.py        # Carga de variables de entorno
│   ├── models/          # Modelos de datos (User, Task)
│   └── routes/          # Rutas de la API (Auth, Tasks)
├── run.py               # Punto de entrada de la aplicación
├── requirements.txt     # Lista de dependencias
├── .env                 # Variables de entorno (NO subir a GitHub)
└── .gitignore           # Archivos ignorados por Git
```
## Solución de Problemas Comunes
Error pymongo.errors.ConfigurationError: Falta el nombre de la base de datos en tu MONGO_URI.

Error bad auth : authentication failed: Tu usuario o contraseña en el .env son incorrectos (verifica en MongoDB Atlas > Database Access).

Error de conexión (Timeout): Tu IP no está permitida. Ve a MongoDB Atlas > Network Access y agrega tu IP actual (o 0.0.0.0/0 para pruebas).

```
### Fuentes utilizadas para generar este documento:
* `requirements.txt`: Para la sección de instalación.
* `run.py`: Para la instrucción de ejecución.
* `app/routes/auth_routes.py` y `app/routes/task_routes.py`: Para documentar los endpoints.
* `app/config.py`: Para explicar las variables de entorno necesarias.
* Contexto de la conversación: Para las notas específicas sobre la conexión a MongoDB y errores comunes.
```




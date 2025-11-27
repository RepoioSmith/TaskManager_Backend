from app import create_app

# Creamos la aplicación usando la configuración que definimos en la carpeta 'app'
app = create_app()

if __name__ == '__main__':
    # Iniciamos el servidor en modo debug
    app.run(debug=True)
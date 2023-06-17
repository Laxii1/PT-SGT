from app import app
#Este codigo se utiliza para iniciar el servidor de la aplicación Flask solo cuando el archivo se ejecuta directamente.
if __name__ == "__main__":      
    app.run(debug = True)
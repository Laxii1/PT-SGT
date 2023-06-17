# PT-SGT
Prueba técnica que consiste en el desarrollo de un sistema de gestión de tareas.

Para ejecutar el proyecto en un ambiente local se debe contar con:

- Una base de datos en Postgresql 14, con el nombre de SDGT-LOCAL y luego utilizar e ingresar el script que está guardado en la carpeta script-db .

- Python, pip y las librerias Flask, SQLAlchemy, bcrypt, Flask-SQLAlchemy , psycopg2 y flask-cors.

-Utilizar Visual Studio Code y con la extensión Thunder Client probar las rutas , utilizando el botón new request.

Supuestos de la solución.

- Se necesita un login para poder acceder a los datos e información del sistema.
- Se establece seguridad en la contraseña, utilizando la libreria bcrypt que utiliza un algoritmo de hash de contraseñas.
- Los proyectos tambien tienen estado y descripción.
- Los usuarios cuentan con un nombre y apellido.
- El usuario por defecto (admin) puede crear otros usuarios.
- Hay dos tipos de usuarios, 1 corresponde a usuario admin y 2 corresponde a usuario normal.
- Las tareas cuando se actualizan solo pueden cambiar su estado entre pendiente y en proceso, ya que existe una función aparte para establecerlas como completadas.


Explicación de la solución.

- La base de datos fue modelada pensando en las 3 entidades identificadas en el enunciado, las cuales son Usuario, Tarea y Proyecto.Siendo Tarea una entidad dependiente de un usuario y un proyecto.

- La estructura de la aplicación contiene un archivo run.py que se encarga de mantener andando la aplicación, un archivo __init__.py donde se crea la instancia de la aplicación y se establece la conexión con la base de datos alojada en postgresql, un archivo models.py donde se codifica la estructura de la base de datos y de esta manera trabajar con ella a través de consultas u otras acciones.

- Dentro de la carpeta aplicación, está la carpeta module donde estan almacenados los archivos python que corresponden a los CRUDS pedidos en el enunciado, un CU de login y un archivo __init__.py que permite indicar que la carpeta Module es un paquete reconocido por Python. El archivo usuario.py contiene funciones para ver, crear y eliminar usuarios, el archivo proyectos contiene las funciones para crear, ver, actualizar y eliminar proyectos, y finalmente el archivo tareas contiene las funciones para crear, ver, actualizar, eliminar, asignar usuario y completar tarea .
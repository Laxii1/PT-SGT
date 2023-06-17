from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
import bcrypt

#Esta instancia se utiliza para interactuar con la base de datos de la aplicación
db=SQLAlchemy()

#Clase correspondiente a la tabla sdgt_proyecto
class SDGT_PROYECTO(db.Model):
    __tablename__ = 'sdgt_proyecto'
    pro_id = db.Column('pro_id',db.Integer, primary_key = True)
    pro_nombre = db.Column('pro_nombre',db.String(100))
    pro_descripcion=db.Column('pro_descripcion',db.Text)
    pro_estado = db.Column('pro_estado',db.String(15))
# Función que retorna los valores de una tupla de base de datos en un diccionario de datos, para posteriormente retornarlos en un JSON
    def to_dict(self):
        return {
            'pro_id': self.pro_id,
            'pro_nombre': self.pro_nombre,
            'pro_descripcion': self.pro_descripcion,
            'pro_estado':self.pro_estado
        }
#Clase correspondiente a la tabla sdgt_tarea
class SDGT_TAREA(db.Model):
    __tablename__ = 'sdgt_tarea'
    tea_id = db.Column('tea_id',db.Integer, primary_key = True)
    pro_id = db.Column('pro_id',db.Integer)
    usr_id = db.Column('usr_id', db.Integer)
    tea_titulo = db.Column('tea_titulo',db.String(100))
    tea_descripcion = db.Column('tea_descripcion',db.Text)
    tea_fechaven=db.Column('tea_fechavencimiento',db.Date)
    tea_estado = db.Column('tea_estado',db.String(15))
# Función que retorna los valores de una tupla de base de datos en un diccionario de datos, para posteriormente retornarlos en un JSON
    def to_dict(self):
        return {
            'tea_id': self.tea_id,
            'pro_id': self.pro_id,
            'usr_id': self.usr_id,
            'tea_titulo':self.tea_titulo,
            'tea_descripcion': self.tea_descripcion,
            'tea_fechaven':self.tea_fechaven,
            'tea_estado':self.tea_estado
        }

#Clase correspondiente a la tabla sdgt_usuario
class SDGT_Usuario(db.Model):
    __tablename__ = 'sdgt_usuario'
    usr_id = db.Column('usr_id', db.Integer, primary_key = True)
    usr_nombre = db.Column('usr_nombre', db.String(50))
    usr_apellido= db.Column('usr_apellido',db.String(50))
    usr_contrasena = db.Column('usr_pass', db.String(255))
    usr_email = db.Column('usr_email', db.String(100))
    usr_tipo = db.Column('usr_tipo',db.Integer)
#Las siguientes funciones se utilizan para el manejo de la columna contrasena, debido al uso del algoritmo hash de la libreria bcrypt    
    @property
    def password(self):
        raise AttributeError('password not readable')
    @password.setter
    def password(self, password):
        pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.usr_contrasena=pw.decode('utf-8')
        print(self.usr_contrasena)
# Esta función verifica si la contraseña recibida en el parametro es la misma almacenada y codificada en la base de datos        
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.usr_contrasena)
    
    def __init__(self, id,nombre,apellido, email,password,tipo):
        self.usr_id=id
        self.usr_nombre=nombre
        self.usr_apellido=apellido
        self.password = password
        self.usr_email = email
        self.usr_tipo=tipo
# Función que retorna los valores de una tupla de base de datos en un diccionario de datos, para posteriormente retornarlos en un JSON
    def to_dict(self):
        return {
            'usr_id': self.usr_id,
            'usr_nombre': self.usr_nombre,
            'usr_apellido': self.usr_apellido,
            'usr_contrasena':self.usr_contrasena,
            'usr_email': self.usr_email,
            'usr_tipo' : self.usr_tipo
        }
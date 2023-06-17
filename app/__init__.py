from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #Se utiliza para la comunicación de los dos servidores (la API de Python Flask y el Front End de REACT)

app.config["SECRET_KEY"] = 'Secret'

#Dependiendo de las credenciales de postgres el valor admin correspondiente a la contraseña de la base de datos, puede ser distinto
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:admin@127.0.0.1:5432/SDGT_LOCAL' 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'scrtcript'
app.config['SECURITY_PASSWORD_SALT'] = 'fhasdgihwntlgy8f'

from app import models,module
models.db.init_app(app)
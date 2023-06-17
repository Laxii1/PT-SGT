from app import app
from app import models as db
import bcrypt
from flask import  request,session, jsonify
from flask_cors import cross_origin

@app.route('/api/logout')
@cross_origin()
def logout(): #Función para cerrar sesión del usuario
    session.clear()
    return jsonify({'message': 'Cierre de sesión'}),200

@app.route('/api/login',methods=['POST'])
@cross_origin()
def login(): #Función para iniciar sesión de un usuario
    email = request.json['email']   #Elemento del form de login del front end
    pw = request.json['pw']         #Elemento del form de login del front end
    usuario=db.db.session.query(db.SDGT_Usuario).filter(db.SDGT_Usuario.usr_email == email).first() #Consulta que devuelve el usuario que está accediendo
    if usuario != None: #Si el usuario existe verifica la contraseña
        if bcrypt.checkpw(pw.encode('utf-8'), usuario.usr_contrasena.encode('utf-8')):                
            return jsonify({'success':True,'usuario': usuario.usr_email, 'tipo': usuario.usr_tipo}),200 #Retorna un JSON con el email y el tipo de usuario, además de la respuesta 200 de HTTP
        else:
            return jsonify({'success':False}),401 #Retorna la respuesta 401 de HTTP
    else:
        return jsonify({'success':False}),401 #Retorna la respuesta 401 de HTTP
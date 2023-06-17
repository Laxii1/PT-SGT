from flask_cors import cross_origin
from app import app
from app import models as db
from flask import  request,jsonify
from sqlalchemy import func

@app.route('/api/ingresar_usuario',methods=['POST'])
@cross_origin()
def ingresar_usuario():#Función para ingresar usuarios nuevos al sistema
    #Variables obtenidas del Front End
    nombre= request.json['nombre'] 
    apellido=request.json['apellido']
    password = request.json['password']
    email = request.json['email']

    
    tipo=2  #Usuario normal    
    if db.db.session.query(db.SDGT_Usuario).filter(db.SDGT_Usuario.usr_email==email).first() == None : #Consulta para saber si el email ingresado ya está en uso
        if (db.db.session.query(func.max(db.SDGT_Usuario.usr_id)).scalar() == None): #En esta parte se establece la id del usuario
            max_id_usr = 1
        else:
            max_id_usr = db.db.session.query(func.max(db.SDGT_Usuario.usr_id)).scalar() + 1

        usuario_nuevo= db.SDGT_Usuario(max_id_usr,nombre,apellido,email,password , tipo) #Se crea la tupla con todos los datos necesarios
        db.db.session.add(usuario_nuevo)#Se guarda la nueva tupla
        db.db.session.commit()  #Se confirman los cambios
        return jsonify({'message': 'Usuario registrado exitosamente'}),201 #Se retorna el código HTTP de solicitud exitosa
    else:           
        return jsonify({'message': 'El email ya está en uso'}),409 #Se retorna el código HTTP que indica conflicto en la solicitud

@app.route('/api/ver_usuarios')
@cross_origin()
def ver_usuarios():#Función que retorna la lista de todos los usuarios
    usuarios = db.db.session.query(db.SDGT_Usuario).all() #Consulta para guardar todas las tuplas de la tabla Usuario
    lista_usuarios=[usuarios.to_dict() for usuario in usuarios]  #Se convierten las tuplas en una lista de diccionario de datos    
    return jsonify(lista_usuarios),200 #Se retorna la lista y el código HTTP de solicitud procesada correctamente

@app.route('/api/ver_usuarios/<int:usr_id>', methods=['DELETE'])
@cross_origin()
def eliminar_usuario(usr_id): #Función que elimina un usuario
    usuario = db.db.session.query(db.SDGT_Usuario).filter(db.SDGT_Usuario.usr_id==usr_id).first() #Consulta para encontrar al usuario a eliminar
    if usuario !=None: 
        if usuario.usr_id==0: #usuario admin por defecto, no se puede eliminar
            return jsonify({'message':'No se puede eliminar este usuario'}),403 #Retorna el código HTTP de que la acción no está permitida
        tareas=db.db.session.query(db.SDGT_TAREA).filter(db.SDGT_TAREA.usr_id==usr_id).all() #Se busca las tareas asociadas al usuario a eliminar
        if tareas != None: #Si hay tareas asociadas a dicho usuario, se les cambia el id del usuario al usuario por defecto
            for tarea in tareas:
                tarea.usr_id=0
        db.db.session.commit()
        db.db.session.delete(usuario) #Se elimina el usuario de la base de datos
        db.db.session.commit() #Se guardan los cambios
        return jsonify({'message':'Usuario eliminado correctamente'}),200 # Se retorna el código HTTP de solicitud procesada correctamente
    return jsonify({'message':'No se ha podido encontrar al usuario'}),404 #Se retorna el código HTTP de que no se ha encontrado el elemento
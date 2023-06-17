from flask_cors import cross_origin
from app import app
from app import models as db
from flask import request,jsonify
from sqlalchemy import func

@app.route('/api/crear_tarea',methods=['POST'])
@cross_origin()
def crear_tarea(): #Función que permite crear una tarea nueva
    usuario=0 #Usuario por defectp
    #Variables obtenidas del Front End
    proyecto=request.json['pro_id']
    titulo= request.json['titulo']
    descripcion=request.json['descripcion']
    fechaven = request.json['fechaven']
    estado = request.json['estado']
       
    if db.db.session.query(db.SDGT_TAREA).filter(db.SDGT_TAREA.tea_titulo==titulo).first() == None : #Se verifica que el título de la tarea no está repetido
        if (db.db.session.query(func.max(db.SDGT_TAREA.tea_id)).scalar() == None):#Se establece el id de la tarea
            max_id_tea = 1
        else:
            max_id_tea = db.db.session.query(func.max(db.SDGT_TAREA.tea_id)).scalar() + 1
        tarea_nueva= db.SDGT_TAREA(tea_id=max_id_tea,pro_id=proyecto,usr_id=usuario,tea_titulo=titulo,tea_descripcion=descripcion, tea_fechaven=fechaven, tea_estado=estado) #Se crea una tupla nueva de la tabla Tarea
        db.db.session.add(tarea_nueva) #Se guarda dicha tupla en la base de datos
        db.db.session.commit()  #Se confirman los cambios
        return jsonify({'message': 'Tarea registrada exitosamente'}),201 #Se retorna el código HTTP de solicitud exitosa
    else:           
        return jsonify({'message': 'El título de la tarea ya está en uso'}),409 #Se retorna el código HTTP que indica conflicto en la solicitud

@app.route('/api/ver_tareas')
@cross_origin()
def ver_tareas(): #Función que retorna todas las tareas de la base de datos
    tareas = db.db.session.query(db.SDGT_TAREA).all() #Consulta que devuelve todas las tuplas de la tabla tarea
    lista_tareas=[tareas.to_dict() for tarea in tareas] #Se convierten las tuplas en una lista de diccionario de datos 
    return jsonify(lista_tareas),200 #Se retorna la lista y el código HTTP de solicitud procesada correctamente

@app.route('/api/actualizar_tarea/<int:tea_id>',methods=['PUT'])
@cross_origin()
def actualizar_tarea(tea_id): #Función que permite actualizar los datos de una tarea
    tarea = db.db.session.query(db.SDGT_TAREA).filter(db.SDGT_TAREA.tea_id==tea_id).first() #Se busca el id de la tarea
    if tarea == None:
        return jsonify({'message':'No se ha podido encontrar la tarea'}),404 #Si no se encuentra se devuelve el código HTTP de no encontrado
    #Variables obtenidas del Front End
    titulo= request.json['titulo']
    descripcion=request.json['descripcion']
    fechaven=request.json['fechaven']
    estado=request.json['estado']

    #Actualización de los datos de la tarea
    tarea.tea_titulo=titulo
    tarea.tea_descripcion=descripcion
    tarea.tea_fechaven=fechaven
    tarea.tea_estado=estado
    db.db.session.commit() #Se confirman los cambios
    return jsonify({'message':'Tarea actualizada correctamente'}),200 #Se retorna el código HTTP de solicitud procesada correctamente

@app.route('/api/asignar_tarea/<int:tea_id>', methods=['PUT'])
@cross_origin()
def asignar_tarea(tea_id): #Función que permite asignar una tarea a un usuario
    tarea = db.db.session.query(db.SDGT_TAREA).filter(db.SDGT_TAREA.tea_id==tea_id).first()#Se busca el id de la tarea
    if tarea == None:
        return jsonify({'message':'No se ha encontrado la tarea'}),404 #Si no se encuentra se devuelve el código HTTP de no encontrado
    
    #Variable obtenida del Front End correspondiente al usuario asignado
    usuario=request.json['usuario']

    tarea.usr_id=usuario #Se actualiza el dato de la tarea
    db.db.session.commit()# Se confirman los cambios
    return jsonify({'message':'Tarea asignada correctamente'}),200 #Se retorna el código HTTP de solicitud procesada correctamente

@app.route('/api/completar_tarea/<int:tea_id>', methods=['PUT'])#
@cross_origin()
def completar_tarea(tea_id): #Función que permite completar una tarea
    tarea = db.db.session.query(db.SDGT_TAREA).filter(db.SDGT_TAREA.tea_id==tea_id).first() #Se busca el id de la tarea
    if tarea == None:
        return jsonify({'message':'No se ha encontrado la tarea'}),404 #Si no se encuentra se devuelve el código HTTP de no encontrado
    tarea.tea_estado='COMPLETADA' #Se cambia el estado de la tarea
    db.db.session.commit() #Se confirman los cambios
    return jsonify({'message':'Tarea completada'}),200 #Se retorna el código HTTP de solicitud procesada correctamente

@app.route('/api/ver_tareas/<int:tea_id>', methods=['DELETE'])
@cross_origin()
def eliminar_tarea(tea_id): #Función que permite eliminar una tarea
    tarea = db.db.session.query(db.SDGT_TAREA).filter(db.SDGT_TAREA.tea_id==tea_id).first() #Se busca el id de la tarea
    if tarea !=None:
        db.db.session.delete(tarea) #Se elimina la tarea de base de datos
        db.db.session.commit() #Se confirman los cambios
        return jsonify({'message':'Tarea eliminada correctamente'}),200 #Se retorna el código HTTP de solicitud procesada correctamente
    return jsonify({'message':'No se ha encontrado la tarea'}),404 #Se retorna el código HTTP de no encontrado
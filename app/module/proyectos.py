from flask_cors import cross_origin
from app import app
from app import models as db
from flask import  request,jsonify
from sqlalchemy import func

@app.route('/api/crear_proyecto',methods=['POST'])
@cross_origin()
def crear_proyecto():#Función para crear un proyecto nuevo
    #Variables obtenidas del Front End
    nombre= request.json['nombre']
    descripcion=request.json['descripcion']
    estado = request.json['estado']
    
    #Se busca si existe un proyecto con el mismo nombre
    if db.db.session.query(db.SDGT_PROYECTO).filter(db.SDGT_PROYECTO.pro_nombre==nombre).first() == None :
        #Se establece el id del proyecto
        if (db.db.session.query(func.max(db.SDGT_PROYECTO.pro_id)).scalar() == None):
            max_id_pro = 1
        else:
            max_id_pro = db.db.session.query(func.max(db.SDGT_PROYECTO.pro_id)).scalar() + 1
        #Se crea la tupla de nuevo proyecto
        proyecto_nuevo= db.SDGT_PROYECTO(pro_id=max_id_pro,pro_nombre=nombre,pro_descripcion=descripcion,pro_estado=estado) 
        db.db.session.add(proyecto_nuevo)#Se agrega la tupla a la base de datos
        db.db.session.commit()  #Se confirman los cambios
        return jsonify({'message': 'Proyecto creado exitosamente'}),201 #Se retorna el código HTTP de solicitud exitosa
    else:           
        return jsonify({'message': 'El nombre de proyecto ya está en uso'}),409 #Se retorna el código HTTP que indica conflicto en la solicitud

@app.route('/api/ver_proyectos')
@cross_origin()
def ver_proyectos():#Función que retorna todos los proyectos de la base de datos
    proyectos = db.db.session.query(db.SDGT_PROYECTO).all() #Consulta que retorna las tuplas de los proyectos
    lista_proyectos=[proyectos.to_dict() for proyecto in proyectos] #Se convierten las tuplas en una lista de diccionario de datos    
    return jsonify(lista_proyectos),200 #Se retorna la lista y el código HTTP de solicitud procesada correctamente

@app.route('/api/actualizar_proyecto/<int:pro_id>',methods=['PUT'])
@cross_origin()
def actualizar_proyecto(pro_id): #Función que permite actualizar los valores de una tupla de la tabla proyecto
    proyecto = db.db.session.query(db.SDGT_PROYECTO).filter(db.SDGT_PROYECTO.pro_id==pro_id).first()# Se busca el proyecto por la id
    if proyecto == None:
        return jsonify({'message':'No se ha encontrado el proyecto'}),404 #Si no se encuentra el id del proyecto retorna el código HTTP no encontrado
    
    #Variables obtenidas del Front End
    nombre= request.json['nombre']
    descripcion=request.json['descripcion']
    estado = request.json['estado']

    #Actualización de los datos
    proyecto.pro_nombre=nombre
    proyecto.pro_descripcion=descripcion
    proyecto.pro_estado=estado
    db.db.session.commit() #Se confirman los cambios

    return jsonify({'message':'Proyecto actualizado correctamente'}),200# Se retorna el código HTTP de solicitud procesada correctamente

@app.route('/api/ver_proyectos/<int:pro_id>', methods=['DELETE'])
@cross_origin()
def eliminar_proyectos(pro_id):#Función que elimina un proyecto
    proyecto = db.db.session.query(db.SDGT_PROYECTO).filter(db.SDGT_PROYECTO.pro_id==pro_id).first() #Se busca el id del proyecto a eliminar
    if proyecto !=None:
        tareas=db.db.session.query(db.SDGT_TAREA).filter(db.SDGT_TAREA.pro_id==pro_id).all() #Se buscan las tareas asociadas a dicho proyecto
        if tareas != None:
            for tarea in tareas:
                db.db.session.delete(tarea) #Se eliminan todas las tareas asociadas al proyecto
        db.db.session.commit()
        db.db.session.delete(proyecto) # Se elimina el proyecto
        db.db.session.commit() #Se confirman los cambios
        return jsonify({'message':'Proyecto eliminado correctamente'}),200 # Se retorna el código HTTP de solicitud procesada correctamente
    return jsonify({'message':'No se ha encontrado el proyecto'}),404 #Se retorna el código HTTP de que no se ha encontrado el elemento
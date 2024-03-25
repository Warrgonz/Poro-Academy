from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import db.conexion as database 
from bson import ObjectId
from models.eventos import Eventos
from models.calificaciones import Calificaciones

app = Flask(__name__)

db = database.dbConnection()

#metodo para enrutar al index
@app.route('/')
def home(): 
     return render_template('index.html')

#Metodo para enrutar
@app.route('/eventosUser')
def eventosUser(): 
    eventos = db['Eventos'] 
    listaEventos = eventos.find()
    return render_template('eventosUser.html', eventos=listaEventos)

'''
Metodos para administrar eventos
'''
#metodo para enrutar y mostar la lista de eventos
@app.route('/eventos')
def eventos(): 
    eventos = db['Eventos'] 
    listaEventos = eventos.find()
    return render_template('eventos.html', eventos=listaEventos)


#metodo para mostrar el error 404
@app.errorhandler(404)
def notFound(error = None):
    message = {
        'message' : 'No encontrado' + request.url,
        'status' : '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

# Método get agregar
@app.route('/eventos/add_evento', methods=['GET'])
def get_add_evento():
    # Renderiza el formulario para agregar un nuevo evento
    return render_template('add_evento.html')

# Método post agregar
@app.route('/eventos/add_evento', methods=['POST'])
def addEventos():
    eventos = db['Eventos']
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']

        if nombre and descripcion and fecha:
            evento = Eventos(nombre, descripcion, fecha)
            eventos.insert_one(evento.toDBCollection())
            return redirect(url_for('eventos'))
        else:
            return notFound()
    else:
        return "Método no permitido"  # Manejar el caso de que se intente acceder con otro método que no sea POST


#Metodo Get Edit
@app.route('/eventos/edit_evento/<string:Eventos_id>', methods=['GET'])
def get_edit_evento(Eventos_id):
    eventos = db['Eventos']
    # Obtener el evento de la base de datos
    evento = eventos.find_one({'_id': ObjectId(Eventos_id)})
    if evento:
        # Pasar los datos del evento a la plantilla para mostrarlos en el formulario
        return render_template('edit_evento.html', event=evento)
    else:
        # Manejar el caso en que el evento no se encuentre en la base de datos
        return "Evento no encontrado"

#Metodo Post Edit
@app.route('/eventos/edit_evento/<string:Eventos_id>', methods=['POST'])
def edit_evento(Eventos_id):
    eventos = db['Eventos']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']

    if nombre and descripcion and fecha:
        eventos.update_one({'_id': ObjectId(Eventos_id)}, {'$set': {'nombre': nombre, 'descripcion': descripcion, 'fecha': fecha}})
        return redirect(url_for('eventos'))
    else:
        return notFound()

# Método DELETE
@app.route('/eventos/delete/<string:Eventos_id>', methods=['POST'])
def delete(Eventos_id):
    eventos = db['Eventos']
    eventos.delete_one({'_id': ObjectId(Eventos_id)})
    return redirect(url_for('eventos'))


'''
Metodos para administrar calificaciones
'''

#metodo para enrutar y mostar la lista de calificaciones
@app.route('/calificaciones')
def calificaciones(): 
    calificaciones = db['Calificaciones'] 
    listaCalificaciones = calificaciones.find()
    return render_template('calificaciones.html', calificaciones=listaCalificaciones)


# Método get agregar
@app.route('/calificaciones/add_calificacion', methods=['GET'])
def get_add_calificacion():
    # Renderiza el formulario para agregar una nueva calificacion
    return render_template('add_calificacion.html')

# Método post agregar
@app.route('/calificaciones/add_calificacion', methods=['POST'])
def addCalificaciones():
    calificaciones = db['Calificaciones']
    if request.method == 'POST':
        nombre_estudiante = request.form['nombre_estudiante']
        nombre_curso = request.form['nombre_curso']
        seccion = request.form['seccion']
        rubro = request.form['rubro']
        calificacion = request.form['calificacion']

        if nombre_estudiante and nombre_curso and seccion and rubro and calificacion:
            calificacion = Calificaciones(nombre_estudiante, nombre_curso, seccion, rubro, calificacion)
            calificaciones.insert_one(calificacion.toDBCollection())
            return redirect(url_for('calificaciones'))
        else:
            return notFound()
    else:
        return "Método no permitido"  # Manejar el caso de que se intente acceder con otro método que no sea POST

#Metodo Get Edit
@app.route('/calificaciones/edit_calificacion/<string:Calificaciones_id>', methods=['GET'])
def get_edit_calificacion(Calificaciones_id):
    calificaciones = db['Calificaciones']
    # Obtener el evento de la base de datos
    calificacion = calificaciones.find_one({'_id': ObjectId(Calificaciones_id)})
    if calificacion:
        # Pasar los datos del evento a la plantilla para mostrarlos en el formulario
        return render_template('edit_calificacion.html', event=calificacion)
    else:
        # Manejar el caso en que el evento no se encuentre en la base de datos
        return "Calificación no encontrada"

#Metodo Post Edit
@app.route('/calificaciones/edit_calificacion/<string:Calificaciones_id>', methods=['POST'])
def edit_calificacion(Calificaciones_id):
    calificaciones = db['Calificaciones']
    nombre_estudiante = request.form['nombre_estudiante']
    nombre_curso = request.form['nombre_curso']
    seccion = request.form['seccion']
    rubro = request.form['rubro']
    calificacion = request.form['calificacion']

    if nombre_estudiante and nombre_curso and seccion and rubro and calificacion:
        calificaciones.update_one({'_id': ObjectId(Calificaciones_id)}, {'$set': {'nombre_estudiante': nombre_estudiante, 
                                                                                  'nombre_curso': nombre_curso, 
                                                                                  'seccion': seccion, 
                                                                                  'rubro': rubro, 
                                                                                  'calificacion': calificacion}})
        return redirect(url_for('calificaciones'))
    else:
        return notFound()
    
# Método DELETE
@app.route('/calificaciones/delete/<string:Calificaciones_id>', methods=['POST'])
def deleteCalificacion(Calificaciones_id):
    calificaciones = db['Calificaciones']
    calificaciones.delete_one({'_id': ObjectId(Calificaciones_id)})
    return redirect(url_for('calificaciones'))

# Lanzar aplicación
if __name__ == '__main__':
    app.run(debug=True, port=4000)

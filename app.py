from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import db.conexion as database 
from bson import ObjectId
from models.eventos import Eventos
from models.cursos import Cursos

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
CRUD cursos 
'''
# Método para mostrar la lista de cursos
@app.route('/cursos')
def cursos(): 
    cursos = db['Cursos']  # Ajusta esto a tu colección de cursos
    listaCursos = cursos.find()
    return render_template('cursos.html', cursos=listaCursos)

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

# Método GET para agregar un curso
@app.route('/cursos/agregar_curso', methods=['GET'])
def get_agregar_curso():
    return render_template('agregar_curso.html')

# Método POST para agregar un curso
@app.route('/cursos/agregar_curso', methods=['POST'])
def agregar_curso():
    cursos = db['Cursos']  # Ajusta esto a tu colección de cursos
    if request.method == 'POST':
        nombre = request.form['nombre']
        profesor = request.form['profesor']
        descripcion = request.form['descripcion']
        if nombre and profesor and descripcion:
            curso = Cursos(nombre, profesor, descripcion)
            cursos.insert_one(curso.toDBCollection())
            return redirect(url_for('cursos'))
        else:
            return "Todos los campos son requeridos."
    else:
        return "Método no permitido" 


# Método GET para editar un curso
@app.route('/cursos/editar_curso/<string:curso_id>', methods=['GET'])
def get_editar_curso(curso_id):
    cursos = db['Cursos']  
    # Obtener el curso de la base de datos
    curso = cursos.find_one({'_id': ObjectId(curso_id)})
    if curso:
        # Pasar los datos del curso a la plantilla para mostrarlos en el formulario
        return render_template('editar_curso.html', curso=curso)
    else:
        # Manejar el caso en que el curso no se encuentre en la base de datos
        return "Curso no encontrado"

# Método POST para editar un curso
@app.route('/cursos/editar_curso/<string:curso_id>', methods=['POST'])
def editar_curso(curso_id):
    cursos = db['Cursos']  
    nombre = request.form['nombre']
    profesor = request.form['profesor']
    descripcion = request.form['descripcion']
    if nombre and profesor and descripcion:
        cursos.update_one({'_id': ObjectId(curso_id)}, {'$set': {'nombre': nombre, 'profesor': profesor, 'descripcion': descripcion}})
        return redirect(url_for('cursos'))
    else:
        return "Todos los campos son requeridos."

# Método POST para eliminar un curso
@app.route('/cursos/eliminar_curso/<string:curso_id>', methods=['POST'])
def eliminar_curso(curso_id):
    cursos = db['Cursos']  # Ajusta esto a tu colección de cursos
    cursos.delete_one({'_id': ObjectId(curso_id)})
    return redirect(url_for('cursos'))


# Lanzar aplicación
if __name__ == '__main__':
    app.run(debug=True, port=4000)

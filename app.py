from flask import Flask, render_template, request, Response, jsonify, redirect, url_for, session
import db.conexion as database 
from bson import ObjectId
from models.eventos import Eventos
from models.cursos import Cursos
from models.calificaciones import Calificaciones
from models.Usuario import Usuario
from functools import wraps
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = b'g\x13\x94z\xec\xfc\xf5g\xf9\xc9\x05\xf2;9F\x9b'

db = database.dbConnection()

usuario = Usuario(app)

usuario.crearUsuarioAdmin()

# Roles

def roles_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))

            correo_usuario = session['user']['correo_electronico']

            roles_usuario = usuario.obtenerRolesPorCorreo(correo_usuario)

            if roles_usuario not in roles:
                return redirect(url_for('login'))  # Sin rol adecuado.

            return view_func(*args, **kwargs)
        return wrapper
    return decorator

# Login y validaciones

# Formato del correo electrónico
def validar_correo(correo):
    if not correo.endswith("@poro.com"):
        return jsonify({"error": "El dominio ingresado no cumple con las normas."}), 401
    return None

# Usuario existente
def validar_usuario(correo):
    user = usuario.obtenerUsuarioPorCorreo(correo)
    if not user:
        return jsonify({"error": "Favor solicite un usuario al administrador local."}), 401
    return None

@app.route('/user/login', methods=['POST'])
def login():
    correo = request.form['correo']
    password = request.form['password']

    # Validar si los campos están vacíos
    if not correo or not password:
        return jsonify({"error": "Favor llenar los campos solicitados."}), 401

    # Validación del formato del correo electrónico
    error = validar_correo(correo)
    if error:
        return error

    # Validación si el usuario existe en Poro
    error = validar_usuario(correo)
    if error:
        return error

    user = usuario.obtenerUsuarioPorCorreo(correo)

    # Validar contraseña incorrecta si el correo existe
    if not check_password_hash(user['contrasena'], password):
        return jsonify({"error": "La contraseña es incorrecta."}), 401

    # Autenticación exitosa
    session['logged_in'] = True
    session['user'] = user
    if user['rol'] == 'ADMIN':
        return redirect(url_for('dashboard')) #Busco a la ruta /dashboard.
    else:
        return redirect(url_for('user_dashboard'))

   
    
@app.route('/dashboard')
@roles_required(['ADMIN']) # Asi se especifica a qué lugares va poder acceder cada rol.
def dashboard():
    return render_template('dashboard.html')

#metodo para enrutar al index
@app.route('/')
def home(): 
     return render_template('index.html')

# Usuarios

@app.route('/login.html')
def login_html():
    return render_template('login.html')

@app.route('/user/signup', methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        Usuario().registroUsuario(request.form)  
        return redirect(url_for('registro'))
    else:
        usuarios = Usuario().obtenerUsuarios()
        return render_template('registroUsuarios.html', usuarios=usuarios)
    
@app.route('/user/signout')
def salir():
    return Usuario().cerrarSesion()


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

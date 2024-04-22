from flask import Flask, render_template, request, Response, jsonify, redirect, url_for, session
import db.conexion as database 
from bson import ObjectId
from models.eventos import Eventos
from models.secciones import Secciones
from models.cursos import Cursos
from models.calificaciones import Calificaciones
from models.asistencias import Asistencias
from models.Usuario import Usuario
from models.Personal import Personal
from functools import wraps
from werkzeug.security import check_password_hash
from models.Contacto import Contacto

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

@app.route('/user/login', methods=['POST'])
def login():
    correo = request.form['correo']
    password = request.form['password']

    user = usuario.obtenerUsuarioPorCorreo(correo)

    # Verificar si el usuario existe y la contraseña coincide
    if user and check_password_hash(user['contrasena'], password):
        session['logged_in'] = True
        session['user'] = user
        if user['rol'] == 'ADMIN':
            return redirect(url_for('dashboard'))
        elif user['rol'] in ['ESTUDIANTE', 'PROFESOR']:
            return redirect(url_for('user_dashboard'))
        else:
            return jsonify({"error": "credenciales invalidas"}), 400
    else:
        return jsonify({"error": "credenciales invalidas"}), 400

@app.route('/dashboard')
@roles_required(['ADMIN']) # Asi se especifica a qué lugares va poder acceder cada rol.
def dashboard():
    return render_template('dashboard.html')

@app.route('/userDashboard')
@roles_required(['ESTUDIANTE', 'PROFESOR'])
def user_dashboard():
    return render_template('user_dashboard.html')

# Rutas publicas

#metodo para enrutar al index
@app.route('/')
def home(): 
     return render_template('index.html')

@app.route('/nosotros')
def nosotros(): 
     return render_template('nosotros.html')

@app.route('/contacto')
def contacto(): 
     return render_template('contacto.html')

@app.route('/login')
def login_html():
    return render_template('login.html')

# Usuarios

@app.route('/user/signup', methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario.registroUsuario(request.form)  
        usuarios = usuario.obtenerUsuarios()
        usuarios_con_indice = list(enumerate(usuarios, start=1))  
        return render_template('registroUsuarios.html', usuarios=usuarios_con_indice)
    else:
        usuarios = usuario.obtenerUsuarios()
        usuarios_con_indice = list(enumerate(usuarios, start=1)) 
        return render_template('registroUsuarios.html', usuarios=usuarios_con_indice)

@app.route('/user/signout')
def salir():
    return Usuario().cerrarSesion()

# Contacto

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    if request.method == 'POST':
        nombre = request.form['fullname']
        email = request.form['email']
        telefono = request.form.get('phone', '')  
        mensaje = request.form['message']
        
        contacto = Contacto()  # Crear una instancia de la clase Contacto
        if contacto.insertar_contacto(nombre, email, telefono, mensaje):
            print("¡Formulario enviado correctamente!")
            return redirect(url_for('contacto'))
        else:
            print("Error al procesar el formulario. Por favor, inténtalo de nuevo.")
            return redirect(url_for('contacto'))

        
# Bandeja 
          
@app.route('/bandeja')
def bandeja():
    numero_mensajes = Contacto.contar_mensajes_recibidos()
    solicitudes = Contacto.obtener_todas_solicitudes(db)
    return render_template('bandeja.html', solicitudes=solicitudes, numero_mensajes=numero_mensajes)


@app.route('/bandeja/resueltos')
def bandejaResueltos():
    solicitudes = Contacto.obtener_todas_solicitudes(db)
    return render_template('bandejaResueltos.html', solicitudes=solicitudes)

@app.route('/bandeja/eliminados')
def bandejaEliminados():
    solicitudes = Contacto.obtener_todas_solicitudes(db)
    return render_template('bandejaEliminados.html', solicitudes=solicitudes)

@app.route('/bandeja/spam')
def bandejaSpam():
    solicitudes = Contacto.obtener_todas_solicitudes(db)
    return render_template('bandejaSpam.html', solicitudes=solicitudes)

@app.route('/ver_solicitud/<id_solicitud>')
def ver_solicitud(id_solicitud):
    # Solicitud por su ID
    solicitud = Contacto.obtener_solicitud_por_id(db, id_solicitud)
    return render_template('leer_contacto.html', solicitud=solicitud)

@app.route("/actualizar_solicitud", methods=["POST"])
def actualizar_solicitud():
    id_solicitud = request.json["id_solicitud"]
    accion = request.json["accion"]

    if accion == "resolver":
        Contacto.resolver_solicitud(id_solicitud, db)
    elif accion == "marcar_spam":
        Contacto.marcar_spam(id_solicitud, db)
    elif accion == "eliminar":
        Contacto.eliminar_solicitud(id_solicitud, db)
        pass
    else:
        return "Acción no válida", 400

    return "OK", 200

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
@roles_required(['ADMIN']) 
@app.route('/eventos/add_evento', methods=['GET'])
def get_add_evento():
    return render_template('add_evento.html')

# Método post agregar
@roles_required(['ADMIN']) 
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
@roles_required(['ADMIN']) 
@app.route('/eventos/edit_evento/<string:Eventos_id>', methods=['GET'])
def get_edit_evento(Eventos_id):
    eventos = db['Eventos']
    evento = eventos.find_one({'_id': ObjectId(Eventos_id)})
    if evento:
        return render_template('edit_evento.html', event=evento)
    else:
        return "Evento no encontrado"

#Metodo Post Edit
@roles_required(['ADMIN']) 
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
@roles_required(['ADMIN']) 
@app.route('/eventos/delete/<string:Eventos_id>', methods=['POST'])
def delete(Eventos_id):
    eventos = db['Eventos']
    eventos.delete_one({'_id': ObjectId(Eventos_id)})
    return redirect(url_for('eventos'))

'''
Metodo para mostrar los secciones a los usuarios profesores 
'''
# Método para mostrar el error 404
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'No encontrado' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response


#Metodo para enrutar
@app.route('/secciones')
def secciones():
    secciones = db['Secciones']
    lista_secciones = secciones.find()
    cursos = list(db['Cursos'].find())  

    secciones_unicas = set()
    for seccion in lista_secciones:
        secciones_unicas.add(seccion['seccion'])

    return render_template('secciones.html', secciones=list(secciones_unicas), cursos=cursos)

@app.route('/secciones/seccionCursos/<string:Secciones_seccion>', methods=['GET'])
def seccionCursos(Secciones_seccion):
    secciones_collection = db['Secciones']
    cursos_collection = db['Cursos']
    cursos = list(db['Cursos'].find())  

    secciones_cursor = secciones_collection.find({'seccion': Secciones_seccion})

    secciones = []
    for seccion in secciones_cursor:
        curso_id = seccion['curso_id']
        curso = cursos_collection.find_one({'_id': ObjectId(curso_id)})
        profesor = curso.get('profesor', 'Profesor Desconocido')
        seccion['curso'] = curso['nombre']
        seccion['profesor'] = profesor
        secciones.append(seccion)

    return render_template('seccionCursos.html', secciones=secciones, cursos=cursos)

#Metodo get add
@app.route('/secciones/add_seccion', methods=['GET'])
def get_add_seccion():
    cursos = list(db['Cursos'].find())  
    return render_template('secciones.html', cursos=cursos)

# Método POST add
@app.route('/secciones/add_seccion', methods=['POST'])
def add_seccion():
    secciones = db['Secciones']
    if request.method == 'POST':
        curso_id = request.form['curso']
        seccion = request.form['seccion']
        horario = request.form['horario']
        estudiantes_asignados = request.form['estudiantesAsignados'].split(',')

        if curso_id and seccion and horario and estudiantes_asignados:
            seccion = Secciones(curso_id, seccion, horario, estudiantes_asignados)
            secciones.insert_one(seccion.toDBCollection())
            return redirect(url_for('secciones'))
        else:
            return not_found()
    else:
        return "Método no permitido"

# Método GET para editar una sección
@app.route('/secciones/edit_seccion/<string:Secciones_id>', methods=['GET'])
def get_edit_seccion(Secciones_id):
    secciones = db['Secciones']
    seccion = secciones.find_one({'_id': ObjectId(Secciones_id)})
    cursos = list(db['Cursos'].find())  

    if seccion:
        return render_template('edit_seccion.html', seccion=seccion, cursos=cursos)
    else:
        return "Sección no encontrada", 404 

# Método POST para editar una sección
@app.route('/secciones/edit_seccion/<string:Secciones_id>', methods=['POST'])
def edit_seccion(Secciones_id):
    secciones = db['Secciones']
    curso_id = request.form.get('curso')
    seccion_name = request.form.get('seccion')
    horario = request.form.get('horario')
    estudiantes_asignados = request.form['estudiantesAsignados'].split(',')

    if curso_id and seccion_name and horario and estudiantes_asignados:
        result = secciones.find_one_and_update(
            {'_id': ObjectId(Secciones_id)},
            {'$set': {'curso_id': curso_id, 'seccion': seccion_name, 'horario': horario, 'estudiantesAsignados': estudiantes_asignados}}
        )
        
        if result:
            return redirect(url_for('secciones'))
        else:
            return "Error al actualizar la sección", 500
    else:
        return "Faltan campos requeridos", 400  


# Método DELETE
@app.route('/secciones/seccionCursos/<string:Secciones_seccion>/delete/<string:Secciones_id>', methods=['POST'])
def deleteS(Secciones_seccion, Secciones_id):
    secciones = db['Secciones']
    secciones.delete_one({'_id': ObjectId(Secciones_id)})
    return redirect(url_for('secciones'))


@app.route('/user/seccion')
@roles_required(['ESTUDIANTE'])
def user_seccion():
    nombre_estudiante = session['user']['nombre_completo']
    
    # Obtener las secciones en las que el estudiante está asignado
    secciones = db['Secciones'].find({'estudiantesAsignados': {'$in': [nombre_estudiante]}})
    
    # Convertir el resultado de la consulta a una lista de diccionarios
    secciones_list = list(secciones)
    
    # Iterar sobre cada sección y modificar el formato de estudiantesAsignados
    for seccion in secciones_list:
        estudiantes_asignados = seccion.get('estudiantesAsignados', {})
        estudiantes_list = [estudiantes_asignados[key] for key in sorted(estudiantes_asignados.keys())]
        seccion['estudiantesAsignados'] = estudiantes_list
    
    return render_template('user_seccion.html', secciones=secciones_list)

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
CRUD asistencia 
'''
# Método para enrutar y mostrar la lista de asistencias
@app.route('/asistencias')
def asistencias(): 
    asistencias = db['Asistencias'] 
    listaAsistencias = asistencias.find()
    return render_template('asistencias.html', asistencias=listaAsistencias)

# Método get para agregar asistencia
@app.route('/asistencias/add_asistencia', methods=['GET'])
def get_add_asistencia():
    # Renderiza el formulario para agregar una nueva asistencia
    return render_template('add_asistencia.html')

    
@app.route('/asistencias/add_asistencia', methods=['POST'])
def addAsistencia():
    asistencias = db['Asistencias']  
    if request.method == 'POST':
        nombre_estudiante = request.form['nombre_estudiante']
        fecha = request.form['fecha']
        estado = request.form['estado']

        if nombre_estudiante and fecha and estado:
            asistencia = Asistencias(nombre_estudiante, fecha, estado)
            asistencias.insert_one(asistencia.toDBCollection())
            return redirect(url_for('asistencias'))
        else:
            return "Todos los campos son requeridos."
    else:
        return "Método no permitido"



# Método Get para editar asistencia
@app.route('/asistencias/edit_asistencia/<string:Asistencias_id>', methods=['GET'])
def get_edit_asistencia(Asistencias_id):
    asistencias = db['Asistencias']
    # Obtener la asistencia de la base de datos
    asistencia = asistencias.find_one({'_id': ObjectId(Asistencias_id)})
    if asistencia:
        # Pasar los datos de la asistencia a la plantilla para mostrarlos en el formulario
        return render_template('edit_asistencia.html', asistencia=asistencia)
    else:
        # Manejar el caso en que la asistencia no se encuentre en la base de datos
        return "Asistencia no encontrada"

# Método Post para editar asistencia
@app.route('/asistencias/edit_asistencia/<string:Asistencias_id>', methods=['POST'])
def edit_asistencia(Asistencias_id):
    asistencias = db['Asistencias']
    nombre_estudiante = request.form['nombre_estudiante']
    fecha = request.form['fecha']
    estado = request.form['estado']

    if nombre_estudiante and fecha and estado:
        asistencias.update_one({'_id': ObjectId(Asistencias_id)}, {'$set': {'nombre_estudiante': nombre_estudiante, 
                                                                              'fecha': fecha, 
                                                                              'estado': estado}})
        return redirect(url_for('asistencias'))
    else:
        return notFound()

# Método DELETE
@app.route('/asistencias/delete/<string:Asistencias_id>', methods=['POST'])
def deleteAsistencia(Asistencias_id):
    asistencias = db['Asistencias']
    asistencias.delete_one({'_id': ObjectId(Asistencias_id)})
    return redirect(url_for('asistencias'))

'''
Metodos para administrar personal
'''

#Metodo para enrutar
@app.route('/listaPersonal', methods=["GET", "POST"])
def personal(): 
    personal = db['Personal'] 
    listaPersonal = personal.find()
    return render_template('listaPersonal.html', personal=listaPersonal)

# Método get agregar
@app.route('/listaPersonal/add_personal', methods=['GET'])
def get_add_personal():
    # Renderiza el formulario para agregar una nueva calificacion
    return render_template('add_personal.html')

# Método post agregar
@app.route('/listaPersonal/add_personal', methods=['POST'])
def addPersonal():
    personal = db['Personal']
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        puesto = request.form['puesto']
        correo_electronico = request.form['correo_electronico']
        telefono = request.form['telefono']

        if nombre_completo and puesto and correo_electronico and telefono:
            persona = Personal(nombre_completo, puesto, correo_electronico, telefono)
            personal.insert_one(persona.toDBCollection())
            return redirect(url_for('personal'))
        else:
            return notFound()
    else:
        return "Método no permitido"  # Manejar el caso de que se intente acceder con otro método que no sea POST

#Metodo Get Edit
@app.route('/listaPersonal/edit_personal/<string:Personal_id>', methods=['GET'])
def get_edit_personal(Personal_id):
    personal = db['Personal']
    # Obtener el evento de la base de datos
    persona = personal.find_one({'_id': ObjectId(Personal_id)})
    if persona:
        # Pasar los datos del evento a la plantilla para mostrarlos en el formulario
        return render_template('edit_personal.html', event=persona)
    else:
        # Manejar el caso en que el evento no se encuentre en la base de datos
        return "Persona no encontrada"

#Metodo Post Edit
@app.route('/listaPersonal/edit_personal/<string:Personal_id>', methods=['POST'])
def edit_personal(Personal_id):
    personal = db['Personal']
    nombre_completo = request.form['nombre_completo']
    puesto = request.form['puesto']
    correo_electronico = request.form['correo_electronico']
    telefono = request.form['telefono']

    if nombre_completo and puesto and correo_electronico and telefono:
        personal.update_one({'_id': ObjectId(Personal_id)}, {'$set': {'nombre_completo': nombre_completo, 
                                                                                  'puesto': puesto, 
                                                                                  'correo_electronico': correo_electronico, 
                                                                                  'telefono': telefono}})
        return redirect(url_for('personal'))
    else:
        return notFound()
    
# Método DELETE
@app.route('/listaPersonal/delete/<string:Personal_id>', methods=['POST'])
def deletePersonal(Personal_id):
    personal = db['Personal']
    personal.delete_one({'_id': ObjectId(Personal_id)})
    return redirect(url_for('personal'))

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

'''
Metodos para mostrar las calificaciones del estudiante
'''
@app.route('/user/calificaciones')
@roles_required(['ESTUDIANTE'])
def user_calificaciones():
    calificaciones = db['Calificaciones'].find({'nombre_estudiante': session['user']['nombre_completo']})
    return render_template('user_calificaciones.html', calificaciones=calificaciones)

# Lanzar aplicación
if __name__ == '__main__':
    app.run(debug=True, port=4000)

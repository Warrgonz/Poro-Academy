from flask import request, jsonify, session, redirect, url_for, render_template
from db.conexion import dbConnection
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash 
from functools import wraps
import uuid

db = dbConnection()

class Usuario:

    def __init__(self, app=None):
        self.app = app
    
    def start_session(self, Usuario):
        session['logged_in'] = True
        session['user'] = Usuario
        return jsonify(Usuario), 200

    def obtenerUsuarioPorCorreo(self, correo):
        return db.Usuarios.find_one({"correo_electronico": correo})
    
    def obtenerRolesPorCorreo(self, correo):
        usuario = db.Usuarios.find_one({"correo_electronico": correo})
        if usuario:
            return usuario.get('rol')
        else:
            return None
        
    def obtenerUsuarios(self):
        usuarios = list(db.Usuarios.find())
        return usuarios
    
    def crearUsuarioAdmin(self):
        with self.app.app_context():
            # Tenemos admin?
            admin_user = db.Usuarios.find_one({"correo_electronico": "admin@poro.com"})
            if admin_user:
                return jsonify({"message": "El usuario administrador ya existe."}), 200

            # Si el usuario administrador no existe, hagalo!
            hashed_password = generate_password_hash("12345")
            usuario_admin = {
                "_id": uuid.uuid4().hex,
                "nombre_completo": "Marvin Solano Campos",
                "cedula": "1105687219",
                "correo_electronico": "admin@poro.com",
                "contrasena": hashed_password,
                "rol": "ADMIN"
            }
            db.Usuarios.insert_one(usuario_admin)

            return jsonify({"message": "Usuario administrador creado con éxito."}), 200

    def registroUsuario(self, form_data):
        hashed_password = generate_password_hash(form_data.get('password'))  # Cifra la contraseña

     # Obtener el valor seleccionado del campo 'rol'
        rol = form_data.get('rol')

    # Verificar si el rol es uno de los valores permitidos
        roles_permitidos = ['ADMIN', 'PROFESOR', 'ESTUDIANTE']
        if rol not in roles_permitidos:
            return "Rol no válido", 400

        usuario = {
        "_id": uuid.uuid4().hex,
        "nombre_completo": form_data.get('nombre'),
        "cedula": form_data.get('cedula'),
        "correo_electronico": form_data.get('correo'),
        "contrasena": hashed_password,
        "rol": rol  # Utiliza el valor seleccionado del campo 'rol'
    }

        if db.Usuarios.find_one({"correo_electronico": usuario['correo_electronico']}):
            return "El correo ya está en uso", 400

        if db.Usuarios.insert_one(usuario):
            return "Usuario creado con éxito", 200

        return "Error interno del servidor", 500


    def editarUsuario(self, usuario_data):
        # Obtener el ID del usuario a editar
        usuario_id = usuario_data.get('_id')
        # Consultar el usuario en la base de datos
        usuario_existente = db.Usuarios.find_one({"_id": usuario_id})

        if not usuario_existente:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Actualizar los campos del usuario con los nuevos datos del formulario
        usuario_existente['nombre_completo'] = usuario_data.get('nombre')
        usuario_existente['cedula'] = usuario_data.get('cedula')
        usuario_existente['correo_electronico'] = usuario_data.get('correo')
        usuario_existente['rol'] = usuario_data.get('rol')

        # Actualizar el usuario en la base de datos
        db.Usuarios.update_one({"_id": usuario_id}, {"$set": usuario_existente})

        return jsonify({"message": "Usuario actualizado correctamente"}), 200  


    def cerrarSesion(self):
        session.clear()
        return redirect('/')
    







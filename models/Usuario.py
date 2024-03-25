from flask import request, jsonify, session, redirect, url_for, render_template
from db.conexion import dbConnection
import uuid

db = dbConnection()

class Usuario:
    def start_session(self, Usuario):
        session['logged_in'] = True
        session['user'] = Usuario
        return jsonify(Usuario), 200

    def registroUsuario(self, form_data):
        usuario = {
            "_id": uuid.uuid4().hex,
            "nombre_completo": form_data.get('nombre'),
            "cedula": form_data.get('cedula'),
            "correo_electronico": form_data.get('correo'),
            "contrasena": form_data.get('password'),
            "rol": form_data.get('rol')
        }

        if db.Usuarios.find_one({"email": usuario['correo_electronico']}):
            return jsonify({"error": "el correo ya está en uso"}), 400
        
        if db.Usuarios.insert_one(usuario):
           return self.start_session(usuario)

        return jsonify({"error": "Signup failed"}), 400
    
    def obtenerUsuarios(self):
        usuarios = list(db.Usuarios.find())
        return usuarios

    def iniciarSesion(self):
        user = db.users.find_one({
            "email": request.form.get('email')
        })
        # Validación de roles
        # if Usuario:
        #     return self.start_session(Usuario)
        # return jsonify({"error: Credenciales invalidas"}), 401
# Validacion de roles
    
# if Usuario:
#    return self.start_session(Usuario)
    
#return jsonify({"error: Credenciales invalidas"}), 401
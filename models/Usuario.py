from flask import Flask, jsonify, request, session
from db.conexion import dbConnection

db = dbConnection()

class Usuario:

    def start_session(self, Usuario):
        session['logged_in'] = True
        session['user'] = Usuario
        return jsonify(Usuario), 200

    def registroUsuario(self):

        usuario = {
            "_id": "",
            "nombre_completo": "",
            "cedula": "",
            "correo_electronico": "",
            "contrasena": "",
            "rol": ""
        }

        return jsonify(usuario), 200

def iniciarSesion(self):
    user = db.users.find_one({
        "email": request.form.get('email')
    })

# Validacion de roles
    
# if Usuario:
#    return self.start_session(Usuario)
    
#return jsonify({"error: Credenciales invalidas"}), 401
from flask import redirect, url_for
from db.conexion import dbConnection

class Contacto:
    @staticmethod
    def obtener_contador_solicitudes():
        db = dbConnection()
        contador = db.Contador.find_one()
        if contador:
            return contador['contador']
        else:
            # Si no existe el contador, crearlo con valor inicial 0
            db.Contador.insert_one({'contador': 0})
            return 0

    @staticmethod
    def actualizar_contador_solicitudes(contador):
        db = dbConnection()
        db.Contador.update_one({}, {'$set': {'contador': contador}})

    @staticmethod
    def generar_id_solicitud(contador):
        return f'C{contador:05d}'

    @staticmethod
    def insertar_contacto(nombre, email, telefono, mensaje):
        db = dbConnection()
        if db is not None: 

            contador = Contacto.obtener_contador_solicitudes()
            Contacto.actualizar_contador_solicitudes(contador + 1)

            id_solicitud = Contacto.generar_id_solicitud(contador)

            db.Contacto.insert_one({
                'id_solicitud': id_solicitud,
                'nombre': nombre,
                'email': email,
                'telefono': telefono,
                'mensaje': mensaje
            })
            return True
        else:
            return False
        
   


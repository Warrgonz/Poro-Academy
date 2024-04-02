from pymongo import MongoClient
import certifi

#url para conectarse al Mongo Atlas del proyecto 
MONGO_URI = 'mongodb+srv://admin:Contra1234@cluster0.f9piac4.mongodb.net/'
ca = certifi.where()

#metodo para conectarse a la BD
def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["PoroAcademy"]  # Accedemos a la base de datos
    except ConnectionError:
        print('Error de conexión con la base de datos')#mensaje de error
        return None  # Devolvemos None en caso de error
    return db

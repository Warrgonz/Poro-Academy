class Eventos:
    def __init__(self, nombre, descripcion, fecha):
       self.nombre = nombre
       self.descripcion = descripcion
       self.fecha = fecha

    def toDBCollection(self):
        return{
            'nombre' :self.nombre,
            'descripcion': self.descripcion,
            'fecha' : self.fecha
        } 

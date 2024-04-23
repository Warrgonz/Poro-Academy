class Cursos:
    def __init__(self, nombre, descripcion, profesor):
       self.nombre = nombre
       self.descripcion = descripcion
       self.profesor = profesor

    def toDBCollection(self):
        return{
            'nombre' :self.nombre,
            'descripcion': self.descripcion,
            'profesor' : self.profesor
        }
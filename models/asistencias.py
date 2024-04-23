class Asistencias:
    def __init__(self, nombre_estudiante, nombre_curso,fecha, estado):
       
       self.nombre_estudiante = nombre_estudiante
       self.nombre_curso = nombre_curso
       self.fecha = fecha
       self.estado = estado
       

    def toDBCollection(self):
        return{
            'nombre_estudiante' :self.nombre_estudiante,
            'nombre_curso' :self.nombre_curso,
            'fecha': self.fecha,
            'estado' : self.estado,
        }
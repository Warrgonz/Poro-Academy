class Asistencias:
    def __init__(self, nombre_estudiante, fecha, estado):
       
       self.nombre_estudiante = nombre_estudiante
       self.fecha = fecha
       self.estado = estado
       

    def toDBCollection(self):
        return{
            'nombre_estudiante' :self.nombre_estudiante,
            'fecha': self.fecha,
            'estado' : self.estado,
        }
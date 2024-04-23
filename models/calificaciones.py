class Calificaciones:
    def __init__(self, nombre_estudiante, nombre_curso, seccion, rubro, calificacion):
       
       self.nombre_estudiante = nombre_estudiante
       self.nombre_curso = nombre_curso
       self.seccion = seccion
       self.rubro = rubro
       self.calificacion = calificacion

    def toDBCollection(self):
        return{
            'nombre_estudiante' :self.nombre_estudiante,
            'nombre_curso': self.nombre_curso,
            'seccion' : self.seccion,
            'rubro' : self.rubro,
            'calificacion' : self.calificacion
        } 

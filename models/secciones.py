class Secciones:
    def __init__(self, materia, profesor, seccion, horario, estudiantes_asignados):
        self.materia = materia
        self.profesor = profesor
        self.seccion = seccion
        self.horario = horario
        self.estudiantesAsignados = estudiantes_asignados

    def toDBCollection(self):
        if not isinstance(self.estudiantesAsignados, list):
            self.estudiantesAsignados = [self.estudiantesAsignados]
        return {
            'materia': self.materia,
            'profesor': self.profesor,
            'seccion': self.seccion,
            'horario': self.horario,
            'estudiantesAsignados': self.estudiantesAsignados
        }

class Secciones:
    def __init__(self, curso_id, seccion, horario, estudiantes_asignados):
        self.curso_id = curso_id
        self.seccion = seccion
        self.horario = horario
        self.estudiantesAsignados = estudiantes_asignados

    def toDBCollection(self):
        if not isinstance(self.estudiantesAsignados, list):
            self.estudiantesAsignados = [self.estudiantesAsignados]
        return {
            'curso_id': self.curso_id,
            'seccion': self.seccion,
            'horario': self.horario,
            'estudiantesAsignados': self.estudiantesAsignados
        }
